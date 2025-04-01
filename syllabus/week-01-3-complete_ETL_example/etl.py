"""
provide a complete working example of an ETL 
in python, which reads mysql table (include sample 
records), does some useful transformations and 
then loads into another mysql table.

What This ETL Does

✅ Extracts data from source_table

✅ Transforms:
    •    Fills NULL age with 25
    •    Fills NULL salary with 40000
    •    Computes tax = salary * 10%
    
✅ Loads data into destination_table


Here’s a complete working ETL (Extract, Transform, Load) 
pipeline in Python using MySQL. 

The example covers:

    1.    Extract: Reads data from a MySQL table (source_table).
    
    2.    Transform: Cleans data and performs some transformations.
    
    3.    Load: Inserts transformed data into another MySQL table 
                (destination_table).

You’ll need:
    •    mysql-connector-python (pip install mysql-connector-python)
    •    A running MySQL server

⸻
Python Libraries:

pip3 install mysql-connector
pip3 install pandas
pip3 install sqlalchemy
pip install mysql-connector-python

1. MySQL Setup

Before running the script, create the source and destination tables in MySQL:

CREATE DATABASE homeworks;
USE homeworks;

CREATE TABLE source_table (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    age INT,
    salary INT
);

INSERT INTO source_table (name, age, salary) 
VALUES 
('Alice', 30, 50000),
('Charlie', 35, 70000),
('Bob', NULL, 60000),
('Jason', NULL, 70000),
('David', 28, NULL),
('Rafa', 38, NULL);

mysql> use homeworks;
ERROR 1049 (42000): Unknown database 'homeworks'
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

mysql> create database homeworks;
Query OK, 1 row affected (0.01 sec)

mysql> use homeworks;
Database changed
mysql> CREATE TABLE source_table (
    ->     id INT PRIMARY KEY AUTO_INCREMENT,
    ->     name VARCHAR(50),
    ->     age INT,
    ->     salary INT
    -> );
Query OK, 0 rows affected (0.00 sec)

mysql>
mysql> INSERT INTO source_table (name, age, salary)
    -> VALUES
    -> ('Alice', 30, 50000),
    -> ('Charlie', 35, 70000),
    -> ('Bob', NULL, 60000),
    -> ('Jason', NULL, 70000),
    -> ('David', 28, NULL),
    -> ('Rafa', 38, NULL);
Query OK, 6 rows affected (0.01 sec)
Records: 6  Duplicates: 0  Warnings: 0

mysql> select * from source_table;
+----+---------+------+--------+
| id | name    | age  | salary |
+----+---------+------+--------+
|  1 | Alice   |   30 |  50000 |
|  2 | Charlie |   35 |  70000 |
|  3 | Bob     | NULL |  60000 |
|  4 | Jason   | NULL |  70000 |
|  5 | David   |   28 |   NULL |
|  6 | Rafa    |   38 |   NULL |
+----+---------+------+--------+
6 rows in set (0.00 sec)

CREATE TABLE destination_table (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(50),
    age INT,
    salary INT,
    tax INT
);

mysql> CREATE TABLE destination_table (
    ->     id INT PRIMARY KEY AUTO_INCREMENT,
    ->     full_name VARCHAR(50),
    ->     age INT,
    ->     salary INT,
    ->     tax INT
    -> );
Query OK, 0 rows affected (0.01 sec)

mysql> select * from destination_table;
+----+-----------+------+--------+------+
| id | full_name | age  | salary | tax  |
+----+-----------+------+--------+------+
|  1 | Alice     |   30 |  50000 | 5000 |
|  2 | Charlie   |   35 |  70000 | 7000 |
|  3 | Bob       |   25 |  60000 | 6000 |
|  4 | Jason     |   25 |  70000 | 7000 |
|  5 | David     |   28 |  40000 | 4000 |
|  6 | Rafa      |   38 |  40000 | 4000 |
+----+-----------+------+--------+------+
6 rows in set (0.00 sec)

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
# ETL Functions: 1: Extract
#--------------------------
def extract_data(database_config):
    """Extract data from source_table in MySQL."""
    conn = mysql.connector.connect(**database_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM source_table")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records

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


#----------------------------
# ETL Functions: 2: Transform
#----------------------------
def transform_data(records):
    """Perform transformations: 
    - Handle NULL values by replacing them with defaults.
    - Calculate a new tax field (10% of salary).
    """
    transformed = []
    for record in records:
        name = record["name"]
        age = record["age"] if record["age"] is not None else 25  # Default age = 25
        salary = record["salary"] if record["salary"] is not None else 40000  # Default salary = 40K
        tax = calculate_10_percent(salary)  # 10% tax on salary
        #
        transformed.append((name, age, salary, tax))
    #end-for
    
    return transformed

#----------------------------
# ETL Functions: 3: Load
#----------------------------
def load_data(transformed_records, database_config):
    """Load transformed data into destination_table."""
    conn = mysql.connector.connect(**database_config)
    cursor = conn.cursor()
    
    query = "INSERT INTO destination_table (full_name, age, salary, tax) VALUES (%s, %s, %s, %s)"
    
    cursor.executemany(query, transformed_records)
    conn.commit()
    
    print(f"{cursor.rowcount} records inserted successfully into destination_table.")
    
    cursor.close()
    conn.close()

#---------------------------
# ETL Pipeline Execution
#---------------------------

#-----------------------------------------
# Database config is given as a JSON file
# read a JSON file and return a dictionary
# Database Configuration
"""
DB_CONFIG = {
    "host": "localhost",
    "user": "your_username",
    "password": "your_password",
    "database": "etl_demo"
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
# Source and Target Database connection details
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

#--------------
# 2. Transform
#--------------
transformed_data = transform_data(extracted_data)
print("transformed_data=", transformed_data)

#--------------
# 3. Load
#--------------
load_data(transformed_data, target_db_config)



"""
3. Running the ETL

Run the script:

python etl.py

4. Expected Output in destination_table

SELECT * FROM destination_table;

id   full_name    age    salary      tax
1    Alice         30    50000.00    5000.00
2    Bob           25    60000.00    6000.00
3    Charlie       35    70000.00    7000.00
4    David         28    40000.00    4000.00

"""




