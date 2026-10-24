# Transactional DB (DuckDB) --> ETL --> Star Schema (DuckDB)
#
# Usage (from the ETL_movies_to_star_schema/ folder):
#     python3 step_2_etl_to_star_schema/etl_duckdb.py movies_db.duckdb movies_dw.duckdb
#
#     sys.argv[1] = source: the transactional database built in step 1
#     sys.argv[2] = target: the star-schema database (created / replaced)
#
# Requirements:  pip install duckdb
#
# Star schema (see star_schema.drawio.png):
#
#                 dates_dim
#                     |
#     movies_dim -- ratings_fact -- users_dim
#
# Grain of ratings_fact: one row per rating (one user rates one movie on one day).
#
# The MySQL version of this program (etl.py, using pandas + mysql-connector)
# is kept in ../mysql_version/ for reference.

import sys
import duckdb

#-----------------------------------------
# Command line parameters
#-----------------------------------------
if len(sys.argv) != 3:
    print("usage: python3 etl_duckdb.py <source.duckdb> <target.duckdb>")
    sys.exit(1)

source_db = sys.argv[1]
target_db = sys.argv[2]
print("source (transactional) db =", source_db)
print("target (star schema)   db =", target_db)

# Connect to the TARGET and attach the SOURCE read-only:
# one connection can then read from src.* and write to the warehouse.
con = duckdb.connect(target_db)
con.execute(f"ATTACH '{source_db}' AS src (READ_ONLY)")

#------------------------------------------
# 1. Extract: what is in the source?
#------------------------------------------
for t in ["movies", "users", "ratings"]:
    n = con.execute(f"SELECT COUNT(*) FROM src.{t}").fetchone()[0]
    print(f"extract: src.{t:8} {n:>10,} rows")

#------------------------------------------
# 2. Transform + 3. Load: build the dimensions
#------------------------------------------

# movies_dim: one row per movie.
#   genre in the source is a list ("Comedy, Fantasy, Romance"):
#   we keep the full list as all_genres and use the FIRST genre as genre,
#   so "per genre" analysis has one genre per movie.
con.execute("""
CREATE OR REPLACE TABLE movies_dim AS
SELECT movie_id,
       imdb_title_id,
       title                              AS movie_title,
       TRIM(split_part(genre, ',', 1))    AS genre,
       genre                              AS all_genres,
       year                               AS release_year,
       duration                           AS duration_minutes,
       country,
       director,
       avg_vote                           AS imdb_avg_vote,
       votes                              AS imdb_votes
FROM src.movies
""")

# users_dim: one row per user.
con.execute("""
CREATE OR REPLACE TABLE users_dim AS
SELECT user_id, user_name
FROM src.users
""")

# dates_dim: one row per distinct rating date.
#   date_id is a "smart" integer key: YYYYMMDD (e.g. 20230315).
con.execute("""
CREATE OR REPLACE TABLE dates_dim AS
SELECT CAST(strftime(rating_date, '%Y%m%d') AS INTEGER) AS date_id,
       rating_date,
       year(rating_date)      AS year,
       quarter(rating_date)   AS quarter,
       month(rating_date)     AS month,
       monthname(rating_date) AS month_name,
       day(rating_date)       AS day,
       dayname(rating_date)   AS day_name
FROM (SELECT DISTINCT rating_date FROM src.ratings)
ORDER BY rating_date
""")

#------------------------------------------
# Build the fact table
#------------------------------------------
con.execute("""
CREATE OR REPLACE TABLE ratings_fact AS
SELECT r.rating_id,
       r.movie_id,
       r.user_id,
       d.date_id,
       r.rating
FROM src.ratings r
JOIN dates_dim d ON d.rating_date = r.rating_date
""")

#------------------------------------------
# 4. Validate: the warehouse must match the source
#------------------------------------------
checks = con.execute("""
SELECT
  (SELECT COUNT(*) FROM movies_dim)                       AS movies_dim,
  (SELECT COUNT(*) FROM users_dim)                        AS users_dim,
  (SELECT COUNT(*) FROM dates_dim)                        AS dates_dim,
  (SELECT COUNT(*) FROM ratings_fact)                     AS ratings_fact,
  (SELECT COUNT(*) FROM src.ratings)                      AS src_ratings,
  (SELECT SUM(rating) FROM ratings_fact)                  AS fact_rating_sum,
  (SELECT SUM(rating) FROM src.ratings)                   AS src_rating_sum,
  (SELECT COUNT(*) FROM ratings_fact f
     WHERE f.movie_id NOT IN (SELECT movie_id FROM movies_dim)
        OR f.user_id  NOT IN (SELECT user_id  FROM users_dim)) AS orphan_facts
""").fetchone()

names = ["movies_dim", "users_dim", "dates_dim", "ratings_fact",
         "src_ratings", "fact_rating_sum", "src_rating_sum", "orphan_facts"]
for name, value in zip(names, checks):
    print(f"load:    {name:16} {value:>12,}")

ok = (checks[3] == checks[4]) and (checks[5] == checks[6]) and (checks[7] == 0)
print("VALIDATION:", "PASSED" if ok else "FAILED")

con.execute("DETACH src")
con.close()
sys.exit(0 if ok else 1)
