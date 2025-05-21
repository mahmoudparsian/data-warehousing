import sys
import json
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

#-----------------------------------------
# Database config is given as a JSON file
# read a JSON file and return a dictionary
#
#  *** AVIOID THE  FOLLOWING: ***
#  Connect to MySQL database

def read_json(json_config_file):
    with open(json_config_file) as f:
        # Load the JSON data into a dictionary
        config_as_dict = json.load(f)
        return config_as_dict
#end-def
#-----------------------------------------
# Commit and close the connection
def close_db_resources(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()
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
# Define connection parameters
DATABASE_URL = "mysql+pymysql://root:mp22pass@localhost/sales_database"

# Create transactional database engine
transactional_engine = create_engine(DATABASE_URL)

# Load data from MySQL tables
sales_df = pd.read_sql('SELECT * FROM sales', transactional_engine)
print("sales_df", sales_df)

customers_df = pd.read_sql('SELECT * FROM customers', transactional_engine)
print("customers_df", customers_df)

products_df = pd.read_sql('SELECT * FROM products', transactional_engine)
print("products_df", products_df)

stores_df = pd.read_sql('SELECT * FROM stores', transactional_engine)
print("stores_df", stores_df)


# Commit and close the connection
close_db_resources(source_conn, source_cursor)


#------------------------------------------
# 2. Transform the data to fit the star schema
#    Transform data for star schema
#------------------------------------------

# Create Date Dimension Table
dates = pd.date_range(start='2025-01-01', end='2025-12-31', freq='D')
date_dim_df = pd.DataFrame(dates, columns=['date'])
date_dim_df['date_key'] = date_dim_df['date'].dt.strftime('%Y%m%d').astype(int)
date_dim_df['year'] = date_dim_df['date'].dt.year
date_dim_df['month'] = date_dim_df['date'].dt.month
date_dim_df['day'] = date_dim_df['date'].dt.day
date_dim_df['quarter'] = date_dim_df['date'].dt.quarter
#date_dim_df['week'] = date_dim_df['date'].dt.week
date_dim_df["week"] = date_dim_df["date"].dt.isocalendar().week

# Create SQLAlchemy engine to store data into a data warehouse
# engine = create_engine('mysql+mysqlconnector://root:password@localhost/data_warehouse')
target_engine = create_engine(f"mysql+mysqlconnector://{target_db_config['user']}:{target_db_config['password']}@{target_db_config['host']}/{target_db_config['database']}")

#----------------------------------
# 3. Load data into the data warehouse
#----------------------------------
sales_df.to_sql('fact_sales', target_engine, if_exists='replace', index=False)
customers_df.to_sql('dim_customers', target_engine, if_exists='replace', index=False)
products_df.to_sql('dim_products', target_engine, if_exists='replace', index=False)
stores_df.to_sql('dim_stores', target_engine, if_exists='replace', index=False)
date_dim_df.to_sql('dim_dates', target_engine, if_exists='replace', index=False)

# Commit and close the connection
close_db_resources(target_conn, target_cursor)
