"""
Working Example of an ETL

Provide a complete working example of an 
ETL in python,  which reads  2 MySQL  tables

    source_table
    continents (has 2 columns: country, continent)
    
(include sample records), does some useful 
transformations and then loads transformed 
data into another MySQL table.

What This ETL Does

✅ Extracts data from source_table

✅ Transforms:
    •    1. Fills NULL age with 25
    •    2. Fills NULL salary with 40000
    •    3. Computes tax = salary * 10%
    •    4. adds a "continent" column to the destination_table 
            by a look up
    
    
✅ Loads data into destination_table


Here’s a complete working ETL (Extract, Transform, Load) 
pipeline in Python using MySQL. 

The example covers:

    1. Extract: Reads data from a MySQL tables 
       (source_table and continents).
    
    2. Transform: Cleans data and performs some transformations.
    
    3. Load: Inserts transformed data into another MySQL table 
                (destination_table).

⸻
Required Python Libraries:

     pip3 install mysql-connector
     pip3 install pandas
     pip3 install sqlalchemy
     pip3 install mysql-connector-python

⸻

1. MySQL Setup

Before running the script, create the  
source and destination tables in MySQL:

CREATE DATABASE scu_homeworks;
USE scu_homeworks;

CREATE TABLE source_table (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    age INT,
    country VARCHAR(20),
    salary INT
);

INSERT INTO source_table (name, age, country, salary) 
VALUES 
('Alice', 30,  'USA', 50000),
('George', 40,  'USA', 80000),
...
;

mysql> select * from source_table;
+----+---------+------+---------+--------+
| id | name    | age  | country | salary |
+----+---------+------+---------+--------+
|  1 | Alice   |   30 | USA     |  50000 |
|  2 | George  |   40 | USA     |  80000 |
...

MySQL: Add the continents Table

USE scu_homeworks;

CREATE TABLE continents (
    continent VARCHAR(30),
    country   VARCHAR(20),
    PRIMARY KEY (country)
);

INSERT INTO continents (continent, country) VALUES
('North America', 'USA'),
('North America', 'CANADA'),
('North America', 'MEXICO'),
('Asia', 'INDIA');

SELECT * FROM continents;
+---------------+---------+
| continent     | country |
+---------------+---------+
| North America | USA     |
| North America | CANADA  |
| North America | MEXICO  |
| Asis          | INDIA   |
+---------------+---------+


mysql> use scu_homeworks;
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.00 sec)

mysql> create database scu2_homeworks;
Query OK, 1 row affected (0.01 sec)

mysql> use scu2_homeworks;
Database changed



CREATE TABLE destination_table (
    id INT,
    name VARCHAR(50),
    age INT,
    country VARCHAR(20),
    salary INT,
    tax INT,
    continent VARCHAR(20)
);

mysql> CREATE TABLE destination_table (
    ->     id INT,
    ->     name VARCHAR(50),
    ->     age INT,
    ->     country VARCHAR(20),
    ->     salary INT,
    ->     tax INT,
    ->     continent VARCHAR(20)
    -> );
Query OK, 0 rows affected (0.01 sec)

mysql> select * from destination_table;
+------+---------+------+---------+--------+------+---------------+
| id   | name    | age  | country | salary | tax  | continent     |
+------+---------+------+---------+--------+------+---------------+
|    1 | Alice   |   30 | USA     |  50000 | 5000 | North America |
|    2 | George  |   40 | USA     |  80000 | 8000 | North America |
...



⸻

2. Python ETL Script

Save this as etl.py and run it.
"""

import sys
import json
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine


#--------------------------
# Build a Lookup Dictionary
#
def build_country_to_continent_map(continent_records):
    """
    Converts:
      [{'country': 'USA', 'continent': 'North America'}, ...]
    into:
      {'USA': 'North America', ...}
    """
    return {r["country"]: r["continent"] for r in continent_records}
#end-def
#--------------------------

# Extract Continents Table
#
def extract_continents(database_config):
    conn = mysql.connector.connect(**database_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT country, continent FROM continents")
    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return records
#end-def

#--------------------------
# ETL Functions: 1: Extract
#
# Extract data from source_table in MySQL.
#
#--------------------------
def extract_data(database_config):

    # create a database connection object
    conn = mysql.connector.connect(**database_config)
    
    # create a cursor: acting as a control structure 
    # to traverse and manipulate database records
    # return results as a list of dictionaries
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM source_table")
    records = cursor.fetchall()
    
    # close database resources
    cursor.close()
    conn.close()
    
    return records
#end-def

#---------------------------------
# Calculates 10% of a given salary.
#---------------------------------
def calculate_10_percent(salary):
    """
    Args:
       salary: The salary amount (numeric).

    Returns:
       10% of the salary.
    """
    return int(salary * 0.1)
#end-def


#----------------------------
# ETL Functions: 2: Transform
#
# Perform transformations: 
#    -- Handle NULL values by replacing them with defaults.
#
#    -- Calculate a new tax field (10% of salary).
#
#----------------------------

def transform_data(records, country_to_continent):
    transformed = []

    for record in records:
        id = record["id"]
        name = record["name"]
        country = record["country"]

        continent = country_to_continent.get(country, "UNKNOWN")

        age = record["age"] if record["age"] is not None else 25
        salary = record["salary"] if record["salary"] is not None else 40000
        tax = calculate_10_percent(salary)

        transformed.append(
            (id, name, age, country, salary, tax, continent)
        )

    return transformed
#end-def

#----------------------------
# ETL Functions: 3: Load
#
# Load transformed data into destination_table.
#
#----------------------------

def load_data(transformed_records, database_config):

    conn = mysql.connector.connect(**database_config)
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO destination_table
        (id, name, age, country, salary, tax, continent)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.executemany(insert_query, transformed_records)
    conn.commit()

    print(f"{cursor.rowcount} records inserted successfully.")

    cursor.close()
    conn.close()
#end-def

#-----------------------------------------
# Database config is given as a JSON file
# read a JSON file and return a dictionary
# Database Configuration
"""
config_as_dict = 
{
    "host": "localhost",
    "user": "your_username",
    "password": "your_password",
    "database": "your_database"
}
"""
def read_json(json_config_file):
    with open(json_config_file) as f:
        # Load the JSON data into a Python dictionary
        config_as_dict = json.load(f)
        return config_as_dict
#end-def
#-----------------------------------------
#
#---------------------------
# ETL Pipeline Execution
#---------------------------
#
# Source and Target Database connection details
#
#
#-------------------------------------------------
# Command Line Parameter 1: "db_config_source.json"
#-------------------------------------------------
# This is for a Transactional Database
# db_config_source_file = "db_config_source.json"
db_config_source_file = sys.argv[1]
print("db_config_source_file=", db_config_source_file)

#-------------------------------------------------
# Command Line Parameter 2: "db_config_target.json"
#-------------------------------------------------
# This is for a "Star Schema" Database
# db_config_target_file = "db_config_target.json"
db_config_target_file = sys.argv[2]
print("db_config_target_file=", db_config_target_file)

source_db_config = read_json(db_config_source_file)
print("source_db_config=", source_db_config)

target_db_config = read_json(db_config_target_file)
print("target_db_config=", target_db_config)


#------------
# 1. Extract
#------------
extracted_data = extract_data(source_db_config)
print("extracted_data=", extracted_data)

continent_data = extract_continents(source_db_config)
print("continent_data=", continent_data)

#--------------
# 2. Transform
#--------------
country_to_continent = build_country_to_continent_map(continent_data)
transformed_data = transform_data(extracted_data, country_to_continent)
print("transformed_data=", transformed_data)


#--------------
# 3. Load
#--------------
load_data(transformed_data, target_db_config)



"""
3. Running the ETL

Run the script:

    python3 etl.py db_config_source.json db_config_target.json

4. Expected Output in destination_table

mysql> SELECT * FROM destination_table;
+------+---------+------+---------+--------+------+---------------+
| id   | name    | age  | country | salary | tax  | continent     |
+------+---------+------+---------+--------+------+---------------+
|    1 | Alice   |   30 | USA     |  50000 | 5000 | North America |
|    2 | George  |   40 | USA     |  80000 | 8000 | North America |
...
"""
