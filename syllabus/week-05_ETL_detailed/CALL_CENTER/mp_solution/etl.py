# CSV --> ETL --> MySQL

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
CREATE DATABASE IF NOT EXISTS call_center;
USE call_center;

CREATE TABLE calls (
	id VARCHAR(50),
	customer_name VARCHAR(50),
	sentiment VARCHAR(20),
	csat_score INT,
	call_timestamp VARCHAR(10),
	call_date DATE,              -- added
	quarter INT,                 -- added
	day_of_week VARCHAR(10),     -- added
	day_of_month INT,            -- added
	reason VARCHAR(20),
	city VARCHAR(20),
	state VARCHAR(20),
	channel VARCHAR(20),
	response_time VARCHAR(20),
	call_duration_minutes INT,   -- renamed
	call_center VARCHAR (20)
);

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
# Command Line Parameter 1: "Call_Center.csv"
#-------------------------------------------------
# This is input for call center calls
# call_center_as_csv = "Call_Center.csv"
call_center_as_csv = sys.argv[1]

#-------------------------------------------------
# Command Line Parameter 2: "db_config_target.json"
#-------------------------------------------------
# This is for a "Star Schema" Database
# db_config_target_file = "db_config_target.json"
db_config_target_file = sys.argv[2]

target_db_config = read_json(db_config_target_file)
print("target_db_config=", target_db_config)

# Create a connection to the Target MySQL database
target_conn = mysql.connector.connect(**target_db_config)
target_cursor = target_conn.cursor()

#------------------------------------------
# 1. Extract data from transactional data
#------------------------------------------
df = pd.read_csv(call_center_as_csv)
print("df.count()=", df.count())
print("df=", df)

#------------------------------------------
# 2. Transform the data to fit the star schema
#------------------------------------------

# 2. Transformations:


# Step: Convert the column to datetime
df['call_date'] = pd.to_datetime(df['call_timestamp'], format='%m/%d/%Y')

# Step: Extract the day of the week
# Create a day field/column from `call_timestamp` 
# (values will be Saturday, Sunday, Monday, Tuesday, Wednesday, Friday)
df['day_of_week'] = df['call_date'].dt.day_name()

# 2.1 from call_timestamp column, create a new column/field 
# as day of a month (the values will be in range of 1, 2, ..., 31)
df['day_of_month'] = df['call_date'].dt.day


# 2.4 The `csat_score` has to be greater than 0.
# If any value is less than or equal to zero, then set it to NULL.
# Step 2: Convert scores less than or equal to zero to NULL
df['csat_score'] = df['csat_score'].apply(lambda x: None if x <= 0 else x)

# 2.5 rename a column:
# "call duration in minutes" => CONVERT TO: "call_duration_minutes"
# Rename the column
df = df.rename(columns={'call duration in minutes': 'call_duration_minutes'})

# Create a quarter
df['quarter'] = df['call_date'].dt.quarter

print("df=", df)


#---------------------------------------------------------
# 3. Load the transformed data into the star schema tables
#---------------------------------------------------------

# Create an SQLAlchemy engine for pandas to_sql method
target_engine = create_engine(f"mysql+mysqlconnector://{target_db_config['user']}:{target_db_config['password']}@{target_db_config['host']}/{target_db_config['database']}")


# Insert data into calls table
df.to_sql('calls', target_engine, if_exists='append', index=False)

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