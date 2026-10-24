-- ------------------------------------------------------------
-- Step 1: Build the TRANSACTIONAL (OLTP) database in DuckDB
--
-- Run from the ETL_movies_to_star_schema/ folder:
--     duckdb movies_db.duckdb < step_1_build_transacational_db/build_transactional_db.sql
--
-- Result: movies_db.duckdb with 3 operational tables:
--     movies   (5,486 rows)  IMDB movies 2000-2020
--     users    (100,000 rows)
--     ratings  (2,000,000 rows) one row per (user rates movie)
-- ------------------------------------------------------------

-- movies: the CSV has no integer id. ratings.movie_id refers to the
-- movie's position in the file (1, 2, 3, ...), so we add movie_id
-- from the row order (DuckDB keeps the file order when loading).
CREATE OR REPLACE TABLE movies_raw AS
SELECT * FROM read_csv('step_1_build_transacational_db/IMDB_Movies_2000_2020.csv',
                       header = true, auto_detect = true);

CREATE OR REPLACE TABLE movies AS
SELECT CAST(rowid + 1 AS INTEGER) AS movie_id, *
FROM movies_raw;

DROP TABLE movies_raw;

CREATE OR REPLACE TABLE users AS
SELECT * FROM read_csv('step_1_build_transacational_db/users.csv', header = true, auto_detect = true);

CREATE OR REPLACE TABLE ratings AS
SELECT * FROM read_csv('step_1_build_transacational_db/ratings.csv', header = true, auto_detect = true);

-- Quick check
SELECT 'movies'  AS table_name, COUNT(*) AS n_rows FROM movies
UNION ALL SELECT 'users',   COUNT(*) FROM users
UNION ALL SELECT 'ratings', COUNT(*) FROM ratings;
