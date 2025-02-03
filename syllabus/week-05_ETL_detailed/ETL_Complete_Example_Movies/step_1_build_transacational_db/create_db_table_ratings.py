import sys
import pandas as pd

import sys
import json
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

#----------------------------------------
#                                argv[1]     argv[2]    
# python3 create_table_movies.py <db-config> <csv-file> 
#
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
# Transactional Database connection details
#

#-------------------------------------------------
# Command Line Parameter 1: "db_config.json"
#-------------------------------------------------
# This is for a Transactional Database
# db_config_file = "db_config.json"
db_config_file_as_json = sys.argv[1]
print("db_config_file_as_json=", db_config_file_as_json)
db_config = read_json(db_config_file_as_json)

#-------------------------------------------------
# Command Line Parameter 2: <filename>.csv
#-------------------------------------------------
csv_file_name = sys.argv[2]
print("csv_file_name=", csv_file_name)



# Create a connection to the Source MySQL database
db_conn = mysql.connector.connect(**db_config)
db_cursor = db_conn.cursor()


# Read CSV file and Create a Database Table
df = pd.read_csv(csv_file_name)


#### Load CSV into Database  Table
#### Loading Data into MySQL
# We will load the data from the DataFrames into the MySQL tables.
#
for _, row in df.iterrows():
    db_cursor.execute('''
    INSERT INTO ratings (rating_id, movie_id, user_id, rating, rating_date)
    VALUES (%s, %s, %s, %s, %s)
    ''', tuple(row))

# Commit and close
db_conn.commit()
db_cursor.close()
db_conn.close()

"""
use movies_db;

mysql> show tables;
+---------------------+
| Tables_in_movies_db |
+---------------------+
| movies              |
| ratings             |
| users               |
+---------------------+
3 rows in set (0.01 sec)

mysql> select * from ratings;
+-----------+----------+---------+--------+-------------+
| rating_id | movie_id | user_id | rating | rating_date |
+-----------+----------+---------+--------+-------------+
|         1 |        1 |     101 |      9 | 2023-01-01  |
|         2 |        1 |     102 |      9 | 2023-01-02  |
|         3 |        2 |     103 |     10 | 2023-01-03  |
|         4 |        2 |     101 |      9 | 2023-01-04  |
|         5 |        3 |     102 |      8 | 2023-01-05  |
|         6 |        4 |     100 |      8 | 2023-03-05  |
|         7 |        4 |     101 |     10 | 2023-03-06  |
|         8 |        5 |     104 |      8 | 2023-03-05  |
|         9 |        5 |     105 |     10 | 2023-02-06  |
|        10 |        5 |     106 |      5 | 2023-02-16  |
|        11 |        5 |     102 |      9 | 2023-01-16  |
|        12 |        5 |     101 |      8 | 2023-01-16  |
+-----------+----------+---------+--------+-------------+
12 rows in set (0.00 sec)
"""

