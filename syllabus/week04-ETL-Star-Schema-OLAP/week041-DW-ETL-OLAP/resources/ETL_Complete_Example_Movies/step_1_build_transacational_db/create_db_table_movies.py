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
    INSERT INTO movies (movie_id, movie_title, genre, release_year)
    VALUES (%s, %s, %s, %s)
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

mysql> select * from movies;
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
"""

