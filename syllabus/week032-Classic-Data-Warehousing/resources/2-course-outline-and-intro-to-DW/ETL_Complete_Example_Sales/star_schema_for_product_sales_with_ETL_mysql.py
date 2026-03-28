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
```sql
CREATE DATABASE IF NOT EXISTS sales_db;
USE sales_db;

-- Create transactional tables
CREATE TABLE IF NOT EXISTS sales_transactions (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    customer_id INT,
    location_id INT,
    sale_date DATE,
    quantity INT,
    total_amount INT
);

CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(50),
    category VARCHAR(50),
    price INT
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(50),
    age INT,
    gender VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50)
);

-- Insert sample data into transactional tables
INSERT INTO sales_transactions (product_id, customer_id, location_id, sale_date, quantity, total_amount) VALUES
(1, 1, 1, '2025-01-01', 2, 1999),
(2, 2, 2, '2025-01-02', 1, 499),
(3, 3, 3, '2025-01-03', 3, 899);

INSERT INTO products (product_name, category, price) VALUES
('Laptop', 'Electronics', 999),
('Smartphone', 'Electronics', 499),
('Tablet', 'Electronics', 299);

INSERT INTO customers (customer_name, age, gender) VALUES
('Alice', 30, 'Female'),
('Bob', 25, 'Male'),
('Charlie', 35, 'Male');

INSERT INTO locations (city, state, country) VALUES
('New York', 'NY', 'USA'),
('San Francisco', 'CA', 'USA'),
('Los Angeles', 'CA', 'USA');
```
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
sales_df = pd.read_sql('SELECT * FROM sales_transactions', source_conn)
print("sales_df.count()=", sales_df.count())
print("sales_df=", sales_df)

products_df = pd.read_sql('SELECT * FROM products', source_conn)
print("products_df.count()=", products_df.count())
print("products_df=", products_df)

customers_df = pd.read_sql('SELECT * FROM customers', source_conn)
print("customers_df.count()=", customers_df.count())
print("customers_df=", customers_df)

locations_df = pd.read_sql('SELECT * FROM locations', source_conn)
print("locations_df.count()=", locations_df.count())
print("locations_df=", locations_df)

# Commit and close the connection
source_conn.commit()
source_cursor.close()
source_conn.close()

#------------------------------------------
# 2. Transform the data to fit the star schema
#------------------------------------------

#---------------------------------
# Create the dates dimension table
#---------------------------------
dates_df = sales_df[['sale_date']].drop_duplicates().reset_index(drop=True)
dates_df['date_id'] = dates_df.index + 1
dates_df['date'] = pd.to_datetime(dates_df['sale_date'])
dates_df['day'] = dates_df['date'].dt.day
dates_df['month'] = dates_df['date'].dt.month
dates_df['year'] = dates_df['date'].dt.year
dates_df['quarter'] = dates_df['date'].dt.quarter

#-----------------------
# Create the fact table
#-----------------------
fact_sales_df = sales_df.merge(dates_df[['sale_date', 'date_id']], on='sale_date')
fact_sales_df = fact_sales_df[['sale_id', 'product_id', 'customer_id', 'location_id', 'date_id', 'quantity', 'total_amount']]


#---------------------------------------------------------
# 3. Load the transformed data into the star schema tables
#---------------------------------------------------------

# Create an SQLAlchemy engine for pandas to_sql method
target_engine = create_engine(f"mysql+mysqlconnector://{target_db_config['user']}:{target_db_config['password']}@{target_db_config['host']}/{target_db_config['database']}")

# Create dimension tables in Target database
target_cursor.execute('''
CREATE TABLE IF NOT EXISTS products_dim (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(50),
    category VARCHAR(50),
    price INT
);
''')

target_cursor.execute('''
CREATE TABLE IF NOT EXISTS customers_dim (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(50),
    age INT,
    gender VARCHAR(10)
);
''')

target_cursor.execute('''
CREATE TABLE IF NOT EXISTS locations_dim (
    location_id INT PRIMARY KEY,
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50)
);
''')

target_cursor.execute('''
CREATE TABLE IF NOT EXISTS dates_dim (
    date_id INT PRIMARY KEY,
    date DATE,
    day INT,
    month INT,
    year INT,
    quarter INT
);
''')

target_cursor.execute('''
CREATE TABLE IF NOT EXISTS sales_fact (
    sale_id INT PRIMARY KEY,
    product_id INT,
    customer_id INT,
    location_id INT,
    date_id INT,
    quantity INT,
    total_amount INT,
    FOREIGN KEY (product_id) REFERENCES products_dim (product_id),
    FOREIGN KEY (customer_id) REFERENCES customers_dim (customer_id),
    FOREIGN KEY (location_id) REFERENCES locations_dim (location_id),
    FOREIGN KEY (date_id) REFERENCES dates_dim (date_id)
);
''')

# Insert data into dimension tables
products_df.to_sql('products_dim', target_engine, if_exists='append', index=False)
customers_df.to_sql('customers_dim', target_engine, if_exists='append', index=False)
locations_df.to_sql('locations_dim', target_engine, if_exists='append', index=False)
dates_df[['date_id', 'date', 'day', 'month', 'year', 'quarter']].to_sql('dates_dim', target_engine, if_exists='append', index=False)

# Insert data into fact table
fact_sales_df.to_sql('sales_fact', target_engine, if_exists='append', index=False)

# Commit and close the connection
target_conn.commit()
target_cursor.close()
target_conn.close()




"""
### Step 4: Sample OLAP Queries

Finally, we can perform some OLAP queries to analyze the data.

1. **Total Sales Amount by Product:**
   ```sql
   SELECT p.product_name, SUM(s.total_amount) AS total_sales_amount
   FROM sales_fact s
   JOIN products_dim p ON s.product_id = p.product_id
   GROUP BY p.product_name;
   
   SELECT p.product_name, SUM(s.total_amount) AS total_sales_amount
   FROM sales_fact s
   JOIN products_dim p ON s.product_id = p.product_id
   GROUP BY p.product_name
   ORDER by total_sales_amount;
   ```

2. **Sales Quantity by Customer:**
   ```sql
   SELECT c.customer_name, SUM(s.quantity) AS total_quantity
   FROM sales_fact s
   JOIN customers_dim c ON s.customer_id = c.customer_id
   GROUP BY c.customer_name
   ORDER by total_quantity DESC;
   ```

3. **Total Sales by Location:**
   ```sql
   SELECT l.city, SUM(s.total_amount) AS total_sales_amount
   FROM sales_fact s
   JOIN locations_dim l ON s.location_id = l.location_id
   GROUP BY l.city
   ORDER by total_sales_amount DESC;
   ```

4. **Sales Amount by Year/Month:**
   ```sql
   SELECT d.year, d.month, SUM(s.total_amount) AS total_sales_amount
   FROM sales_fact s
   JOIN dates_dim d ON s.date_id = d.date_id
   GROUP BY d.year, d.month
   ORDER by total_sales_amount DESC;

   ```

5. **Average Sales Amount by Customer Age Group:**


6. **Find top-2 selling products per country**
    
"""