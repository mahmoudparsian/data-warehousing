# Transactional Database --> ETL --> Star Schema --> OLAP Queries

The goal of this exercise is to show a complete story of 
creating a "star schema" from a transactional database 
by using a Python ETL. Once a "star schema" is created, 
then we can write our Business Intelligence SQL queries.


# 1. Database configurations
Database configurations are defined as JSON files:

* Transactional (Source) Database:
	* [`db_config_source.json`](./step_2_etl_to_star_schema/db_config_source.json) 

* Star Schema (Target) Database:
	* [`db_config_target.json`](./step_2_etl_to_star_schema/db_config_target.json) 


# 2. Transactional Database

The following 2 steps show how to create a 
Transactional Database:

Transactional Database is created from CSV files



~~~sh
python3 create_table.py <csv-file> <db-config> <table-name> 
~~~

--------

# 3. ETL

## 3.1 [ETL --> Star Schema](./etl.py)


## 3.2 To run ETL:


~~~sh
ETL="et.py"
SOURCE_DB="db_config_source.json"
TARGET_DB="db_config_target.json"
python3 ${ETL} ${SOURCE_DB} ${TARGET_DB}
~~~
-------

# 4. Star Schema

![](./star_schema.drawio.png)

-------


1. **Create a transactional database** with movies and user ratings.
2. **Python ETL script** to transform the transactional database into a **star schema**.
3. **OLAP SQL queries** using the star schema.

---

## **1. Create a Transactional Database**

### Tables and Sample Data

#### Table: `movies`
| movie_id | movie_title          | genre       | release_year |
|----------|----------------------|-------------|--------------|
| 1        | Inception            | Sci-Fi      | 2010         |
| 2        | The Dark Knight      | Action      | 2008         |
| 3        | Interstellar         | Sci-Fi      | 2014         |
| 4        | The Matrix           | Sci-Fi      | 1999         |
| 5        | Gladiator            | Action      | 2000         |

#### Table: `users`
| user_id | user_name  |
|---------|------------|
| 101     | John Doe   |
| 102     | Jane Smith |
| 103     | Alice Brown|

#### Table: `ratings`
| rating_id | movie_id | user_id | rating | rating_date  |
|-----------|----------|---------|--------|--------------|
| 1         | 1        | 101     | 9.0    | 2023-01-01   |
| 2         | 1        | 102     | 8.5    | 2023-01-02   |
| 3         | 2        | 103     | 9.5    | 2023-01-03   |
| 4         | 2        | 101     | 9.0    | 2023-01-04   |
| 5         | 3        | 102     | 8.0    | 2023-01-05   |

---

## **2. Python ETL Script to Convert to Star Schema**

### Star Schema Design

#### Fact Table: `fact_ratings`
| rating_id | movie_id | user_id | rating | rating_date  |
|-----------|----------|---------|--------|--------------|

#### Dimension Tables:
1. `dim_movies`
   | movie_id | movie_title | genre | release_year |
2. `dim_users`
   | user_id | user_name |
3. `dim_date`
   | date_id | rating_date | year | month | day |

---

### Python ETL Script

```python
import sqlite3
import pandas as pd

# Connect to the transactional database
source_conn = sqlite3.connect('transactional.db')
source_cursor = source_conn.cursor()

# Extract data from transactional database
movies_df = pd.read_sql_query("SELECT * FROM movies", source_conn)
users_df = pd.read_sql_query("SELECT * FROM users", source_conn)
ratings_df = pd.read_sql_query("SELECT * FROM ratings", source_conn)

# Transform data for star schema
# Create dim_movies
dim_movies = movies_df.copy()

# Create dim_users
dim_users = users_df.copy()

# Create dim_date
ratings_df['rating_date'] = pd.to_datetime(ratings_df['rating_date'])
dim_date = ratings_df[['rating_date']].drop_duplicates().reset_index(drop=True)
dim_date['date_id'] = dim_date.index + 1
dim_date['year'] = dim_date['rating_date'].dt.year
dim_date['month'] = dim_date['rating_date'].dt.month
dim_date['day'] = dim_date['rating_date'].dt.day
dim_date['quarter'] = dim_date['rating_date'].dt.quarter

# Create fact_ratings
fact_ratings = ratings_df.merge(dim_date, on='rating_date', how='left')
fact_ratings = fact_ratings[['rating_id', 'movie_id', 'user_id', 'rating', 'date_id']]

# Load data into the target database (star schema)
target_conn = sqlite3.connect('star_schema.db')
target_cursor = target_conn.cursor()

# Create tables in the target database
target_cursor.execute('''
CREATE TABLE IF NOT EXISTS dim_movies (
    movie_id INTEGER PRIMARY KEY,
    movie_title TEXT,
    genre TEXT,
    release_year INTEGER
)
''')

target_cursor.execute('''
CREATE TABLE IF NOT EXISTS dim_users (
    user_id INTEGER PRIMARY KEY,
    user_name TEXT
)
''')

target_cursor.execute('''
CREATE TABLE IF NOT EXISTS dim_date (
    date_id INTEGER PRIMARY KEY,
    rating_date DATE,
    year INTEGER,
    month INTEGER,
    day INTEGER
)
''')

target_cursor.execute('''
CREATE TABLE IF NOT EXISTS fact_ratings (
    rating_id INTEGER PRIMARY KEY,
    movie_id INTEGER,
    user_id INTEGER,
    rating REAL,
    date_id INTEGER,
    FOREIGN KEY (movie_id) REFERENCES dim_movies(movie_id),
    FOREIGN KEY (user_id) REFERENCES dim_users(user_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
)
''')

# Insert data into the target database
dim_movies.to_sql('dim_movies', target_conn, if_exists='replace', index=False)
dim_users.to_sql('dim_users', target_conn, if_exists='replace', index=False)
dim_date.to_sql('dim_date', target_conn, if_exists='replace', index=False)
fact_ratings.to_sql('fact_ratings', target_conn, if_exists='replace', index=False)

# Close connections
source_conn.close()
target_conn.close()
```

---

