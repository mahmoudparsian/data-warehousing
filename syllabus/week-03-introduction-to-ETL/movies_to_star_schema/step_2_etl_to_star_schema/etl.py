# MySQL Transactional --> ETL --> Star Schema

# Let's walk through a complete ETL process 
# using Python and MySQL to transform transactional 
# data into a star schema. We'll use the 
# `mysql-connector-python` library for database 
# operations and `pandas` for data manipulation.

### Step 1: Set Up the Environment

# First, we need to install the required libraries:

## pip install pandas
## pip install mysql-connector-python 
## pip install flask_sqlalchemy
## pip install simplejson

### Step 2: Define the Transactional Data

# We'll define the sample transactional data as 
# relational tables in MySQL. Below is the SQL 
# script to create and populate the tables:

"""
Transactional Database:

CREATE DATABASE IF NOT EXISTS movies2;
USE movies2;

-- #### Table: `movies`
CREATE TABLE movies (
    imdm_title_id VARCHAR(255),
    title VARCHAR(255),
    original_title VARCHAR(255),
    year int,
    date_published VARCHAR(255),
    genre VARCHAR(255),
    duration INT,
    country  VARCHAR(255),
    language_1  VARCHAR(255),
    language_2  VARCHAR(255),
    language_3  VARCHAR(255),
    director  VARCHAR(255),
    writer  VARCHAR(255),
    actors  VARCHAR(955),
    actors_1  VARCHAR(955),
    actors_f2  VARCHAR(955),
    description  VARCHAR(255),
    desc35  VARCHAR(255),
    avg_vote DOUBLE,
    votes INT,
    budget INT,
    usa_gross_income INT,
    worlwide_gross_income INT,
    reviews_from_users INT
) CHARACTER SET utf8 COLLATE utf8_general_ci;

-- #### Table: `users`
create table users(
    user_id INT,
    user_name VARCHAR(60)      
);

-- #### Table: `ratings`
create table ratings(
    rating_id INT,
    movie_id INT,     
    user_id INT,
    rating INT, -- 1, 2, 3, ..., 10
    rating_date Date
);

-- Star Schema Tables:
drop table movies_dim;
drop table users_dim;
drop table dates_dim;
drop table ratings_fact;


"""

### Step 3: ETL Process

# Now we'll implement the ETL process in Python.

import sys
import json
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine


#-----------------------------------------
# Database config is given as a JSON file
# read a JSON file and return a dictionary
def read_json(json_config_file):
    with open(json_config_file) as f:
        # Load the JSON data into a Python dictionary
        config_as_dict = json.load(f)
        return config_as_dict
#end-def
#-----------------------------------------
#
# Source and Target Database connection details
#

#-------------------------------------------------
# Command Line Parameter 1: "db_config_source.json"
# denoting the Transactional Database
#-------------------------------------------------
# This is for a Transactional Database
# db_config_source_file = "db_config_source.json"
db_config_source_file = sys.argv[1]

#-------------------------------------------------
# Command Line Parameter 2: "db_config_target.json"
#-------------------------------------------------
# This is for a "Star Schema" Database
# db_config_target_file = "db_config_target.json"
db_config_target_file = sys.argv[2]

source_db_config = read_json(db_config_source_file)
print("source_db_config=", source_db_config)

target_db_config = read_json(db_config_target_file)
print("target_db_config=", target_db_config)

# Create a connection to the Source MySQL database
source_conn = mysql.connector.connect(**source_db_config)
source_cursor = source_conn.cursor()

# Create a connection to the Target MySQL database
target_conn = mysql.connector.connect(**target_db_config)
target_cursor = target_conn.cursor()

#------------------------------------------
# 1. Extract data from transactional tables
#------------------------------------------

#-------------
# READ movies:
#-------------
movies_df = pd.read_sql('SELECT * FROM movies', source_conn)
print("movies_df.count()=", movies_df.count())
print("movies_df=", movies_df)

#-------------
# READ users:
#-------------
users_df = pd.read_sql('SELECT * FROM users', source_conn)
print("users_df.count()=", users_df.count())
print("users_df=", users_df)

#-------------
# READ ratings:
#-------------
ratings_df = pd.read_sql('SELECT * FROM ratings', source_conn)
print("ratings_df.count()=", ratings_df.count())
print("ratings_df=", ratings_df)

# Commit and close the connection
source_conn.commit()
source_cursor.close()
source_conn.close()


#------------------------------------------
# 2. Transform the data to fit the star schema
#    Transform data for star schema
#------------------------------------------

# Create dim_movies
dim_movies = movies_df.copy()

# Create dim_users
dim_users = users_df.copy()

#------------------------------
# Create NEW DIMENSION dim_date
#------------------------------
ratings_df['rating_date'] = pd.to_datetime(ratings_df['rating_date'])
dim_date = ratings_df[['rating_date']].drop_duplicates().reset_index(drop=True)
dim_date['date_id'] = dim_date.index + 1
dim_date['year'] = dim_date['rating_date'].dt.year
dim_date['month'] = dim_date['rating_date'].dt.month
dim_date['day'] = dim_date['rating_date'].dt.day
dim_date['quarter'] = dim_date['rating_date'].dt.quarter

#---------------------
# Create fact_ratings
#---------------------
fact_ratings = ratings_df.merge(dim_date, on='rating_date', how='left')
fact_ratings = fact_ratings[['rating_id', 'movie_id', 'user_id', 'rating', 'date_id']]

#--------------------------------------
# Create tables in the target database
#--------------------------------------
target_cursor.execute('''
CREATE TABLE IF NOT EXISTS movies_dim (
    movie_id INT PRIMARY KEY,
    title TEXT,
    genre TEXT,
    release_year INT
)
''')

target_cursor.execute('''
CREATE TABLE IF NOT EXISTS users_dim (
    user_id INT PRIMARY KEY,
    user_name TEXT
)
''')

target_cursor.execute('''
CREATE TABLE IF NOT EXISTS dates_dim (
    date_id INT PRIMARY KEY,
    rating_date DATE,
    year INT,
    month INT,
    day INT,
    quarter INT
)
''')

target_cursor.execute('''
CREATE TABLE IF NOT EXISTS ratings_fact (
    rating_id INT,
    movie_id INT,
    user_id INT,
    rating REAL,
    date_id INT
)
''')

"""
target_cursor.execute('''
CREATE TABLE IF NOT EXISTS ratings_fact (
    rating_id INTEGER PRIMARY KEY,
    movie_id INTEGER,
    user_id INTEGER,
    rating REAL,
    date_id INTEGER,
    FOREIGN KEY (movie_id) REFERENCES movies_dim(movie_id),
    FOREIGN KEY (user_id) REFERENCES users_dim(user_id),
    FOREIGN KEY (date_id) REFERENCES dates_dim(date_id)
)
''')
"""

#--------------------------------------
# Insert data into the target database
#--------------------------------------

# Create an SQLAlchemy engine for pandas to_sql method
target_engine = create_engine(f"mysql+mysqlconnector://{target_db_config['user']}:{target_db_config['password']}@{target_db_config['host']}/{target_db_config['database']}")

#--------------------------------------------
# WRITE data/records into the target database
#--------------------------------------------
dim_movies.to_sql('movies_dim', target_engine, if_exists='replace', index=False)
dim_users.to_sql('users_dim', target_engine, if_exists='replace', index=False)
dim_date.to_sql('dates_dim', target_engine, if_exists='replace', index=False)
fact_ratings.to_sql('ratings_fact', target_engine, if_exists='replace', index=False)



# Commit and close the connection
target_conn.commit()
target_cursor.close()
target_conn.close()


"""
mysql> show tables;
+---------------------------------+
| Tables_in_movies_star_schema_db |
+---------------------------------+
| dates_dim                       |
| movies_dim                      |
| users_dim                       |
| ratings_fact                    |
+---------------------------------+
4 rows in set (0.00 sec)

mysql> use movies_star_schema_db;
Database changed

mysql> select * from dates_dim;
+---------------------+---------+------+-------+------+---------+
| rating_date         | date_id | year | month | day  | quarter |
+---------------------+---------+------+-------+------+---------+
| 2023-01-01 00:00:00 |       1 | 2023 |     1 |    1 |       1 |
| 2023-01-02 00:00:00 |       2 | 2023 |     1 |    2 |       1 |
| 2023-01-03 00:00:00 |       3 | 2023 |     1 |    3 |       1 |
| 2023-01-04 00:00:00 |       4 | 2023 |     1 |    4 |       1 |
| 2023-01-05 00:00:00 |       5 | 2023 |     1 |    5 |       1 |
| 2023-03-05 00:00:00 |       6 | 2023 |     3 |    5 |       1 |
| 2023-03-06 00:00:00 |       7 | 2023 |     3 |    6 |       1 |
| 2023-02-06 00:00:00 |       8 | 2023 |     2 |    6 |       1 |
| 2023-02-16 00:00:00 |       9 | 2023 |     2 |   16 |       1 |
| 2023-01-16 00:00:00 |      10 | 2023 |     1 |   16 |       1 |
+---------------------+---------+------+-------+------+---------+
10 rows in set (0.00 sec)

mysql> select * from users_dim;
+---------+--------------+
| user_id | user_name    |
+---------+--------------+
|     100 | Rafa Nadal   |
|     101 | John Doe     |
|     102 | Jane Smith   |
|     103 | Alice Brown  |
|     104 | Alec Baldwin |
|     105 | Max Smith    |
|     106 | Maggy Taylor |
|     107 | John Goodman |
|     108 | Mary Basman  |
|     109 | Henry Good   |
+---------+--------------+
10 rows in set (0.00 sec)

mysql> select * from movies_dim;
+----------+-----------------+--------+--------------+
| movie_id | movie_title     | genre  | release_year |
+----------+-----------------+--------+--------------+
|        1 | Inception       | Sci-Fi |         2010 |
|        2 | The Dark Knight | Action |         2008 |
|        3 | Interstellar    | Sci-Fi |         2014 |
|        4 | The Matrix      | Sci-Fi |         1999 |
|        5 | Gladiator       | Action |         2000 |
+----------+-----------------+--------+--------------+
5 rows in set (0.00 sec)


mysql> select * from ratings_fact;
+-----------+----------+---------+--------+---------+
| rating_id | movie_id | user_id | rating | date_id |
+-----------+----------+---------+--------+---------+
|         1 |        1 |     101 |      9 |       1 |
|         2 |        1 |     102 |      9 |       2 |
|         3 |        2 |     103 |     10 |       3 |
|         4 |        2 |     101 |      9 |       4 |
|         5 |        3 |     102 |      8 |       5 |
|         6 |        4 |     100 |      8 |       6 |
|         7 |        4 |     101 |     10 |       7 |
|         8 |        5 |     104 |      8 |       6 |
|         9 |        5 |     105 |     10 |       8 |
|        10 |        5 |     106 |      5 |       9 |
|        11 |        5 |     102 |      9 |      10 |
|        12 |        5 |     101 |      8 |      10 |
+-----------+----------+---------+--------+---------+
12 rows in set (0.00 sec)


"""

