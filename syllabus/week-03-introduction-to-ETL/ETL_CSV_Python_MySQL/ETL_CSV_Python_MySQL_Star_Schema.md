# ETL to Create Star Schema using Python & MySQL

## 1. Introduction

	Using python and mysql, provide a complete 
	example of ETL to create a star schema by 
	reading CSV files for sales transaction, 
	products, customers and locations, then 
	create a star schema with an added date 
	dimension. Also provide sample CSV data 
	for sales, products, customers, and locations

----

	Here is a complete example of an ETL process 
	using Python and MySQL to create a star schema 
	from CSV files. The process includes reading 
	CSV files for sales transactions, products, 
	customers, and locations, and then creating a 
	star schema with an added date dimension.

## Sample CSV Data

#### sales_transactions.csv
```csv
transaction_id,transaction_date,product_id,customer_id,location_id,quantity,total_amount
1,2025-01-01,101,201,301,2,200.00
2,2025-01-02,102,202,302,1,150.00
3,2025-01-03,103,203,303,5,500.00
```

#### products.csv
```csv
product_id,product_name,category,price
101,ProductA,Category1,100.00
102,ProductB,Category2,150.00
103,ProductC,Category1,100.00
```

#### customers.csv
```csv
customer_id,customer_name,email,phone
201,John Doe,john@example.com,123-456-7890
202,Jane Smith,jane@example.com,234-567-8901
203,Bob Johnson,bob@example.com,345-678-9012
```

#### locations.csv
```csv
location_id,city,state,country
301,New York,NY,USA
302,Los Angeles,CA,USA
303,Chicago,IL,USA
```

## Step-by-Step ETL Process

#### Step 1: Reading CSV Files
We will use the `pandas` library to read the CSV files.

```python
import pandas as pd

# Read CSV files
transactions_df = pd.read_csv('sales_transactions.csv')
products_df = pd.read_csv('products.csv')
customers_df = pd.read_csv('customers.csv')
locations_df = pd.read_csv('locations.csv')
```

#### Step 2: Creating a Date Dimension
We will create a date dimension from the transaction date column.

```python
import pandas as pd

# Create date dimension
min_date = pd.to_datetime(transactions_df['transaction_date']).min()
max_date = pd.to_datetime(transactions_df['transaction_date']).max()
date_range = pd.date_range(min_date, max_date, freq='D')

date_dimension = pd.DataFrame({
    'date_id': date_range,
    'year': date_range.year,
    'month': date_range.month,
    'day': date_range.day,
    'weekday': date_range.weekday,
    'quarter': date_range.quarter
})
```

#### Step 3: Connecting to MySQL
We will use the `mysql-connector-python` library to connect to the MySQL database.

```python
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='your_username',
    password='your_password',
    database='your_database'
)
cursor = conn.cursor()
```

#### Step 4: Creating Tables in MySQL
We will create tables for the star schema in MySQL.

```python
# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS DateDimension (
    date_id DATE PRIMARY KEY,
    year INT,
    month INT,
    day INT,
    weekday INT,
    quarter INT
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(255),
    price DECIMAL(10, 2)
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50)
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Locations (
    location_id INT PRIMARY KEY,
    city VARCHAR(255),
    state VARCHAR(255),
    country VARCHAR(255)
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS SalesTransactions (
    transaction_id INT PRIMARY KEY,
    transaction_date DATE,
    product_id INT,
    customer_id INT,
    location_id INT,
    quantity INT,
    total_amount DECIMAL(10, 2),
    FOREIGN KEY (transaction_date) REFERENCES DateDimension(date_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (location_id) REFERENCES Locations(location_id)
)''')
```

#### Step 5: Loading Data into MySQL
We will load the data from the DataFrames into the MySQL tables.

```python
# Load date dimension
for _, row in date_dimension.iterrows():
    cursor.execute('''
    INSERT INTO DateDimension (date_id, year, month, day, weekday, quarter)
    VALUES (%s, %s, %s, %s, %s, %s)
    ''', tuple(row))

# Load products
for _, row in products_df.iterrows():
    cursor.execute('''
    INSERT INTO Products (product_id, product_name, category, price)
    VALUES (%s, %s, %s, %s)
    ''', tuple(row))

# Load customers
for _, row in customers_df.iterrows():
    cursor.execute('''
    INSERT INTO Customers (customer_id, customer_name, email, phone)
    VALUES (%s, %s, %s, %s)
    ''', tuple(row))

# Load locations
for _, row in locations_df.iterrows():
    cursor.execute('''
    INSERT INTO Locations (location_id, city, state, country)
    VALUES (%s, %s, %s, %s)
    ''', tuple(row))

# Load transactions
for _, row in transactions_df.iterrows():
    cursor.execute('''
    INSERT INTO SalesTransactions (transaction_id, transaction_date, product_id, customer_id, location_id, quantity, total_amount)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', tuple(row))
```

#### Step 6: Commit and Close Connection
Finally, we commit the changes and close the connection.

```python
# Commit and close
conn.commit()
cursor.close()
conn.close()
```

-------

## Complete Code Example
Here is the complete code example for the ETL process:

```python
import pandas as pd
import mysql.connector

#-----------------------
# Step 1: Read CSV files
#-----------------------

transactions_df = pd.read_csv('sales_transactions.csv')
products_df = pd.read_csv('products.csv')
customers_df = pd.read_csv('customers.csv')
locations_df = pd.read_csv('locations.csv')

#------------------------------
# Step 2: Create date dimension
#------------------------------
min_date = pd.to_datetime(transactions_df['transaction_date']).min()
max_date = pd.to_datetime(transactions_df['transaction_date']).max()
date_range = pd.date_range(min_date, max_date, freq='D')

date_dimension = pd.DataFrame({
    'date_id': date_range,
    'year': date_range.year,
    'month': date_range.month,
    'day': date_range.day,
    'weekday': date_range.weekday,
    'quarter': date_range.quarter
})

#--------------------------
# Step 3: Connect to MySQL
#--------------------------

conn = mysql.connector.connect(
    host='localhost',
    user='your_username',
    password='your_password',
    database='your_database'
)
cursor = conn.cursor()

#-----------------------
# Step 4: Create tables
#-----------------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS DateDimension (
    date_id DATE PRIMARY KEY,
    year INT,
    month INT,
    day INT,
    weekday INT,
    quarter INT
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(255),
    price DECIMAL(10, 2)
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50)
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Locations (
    location_id INT PRIMARY KEY,
    city VARCHAR(255),
    state VARCHAR(255),
    country VARCHAR(255)
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS SalesTransactions (
    transaction_id INT PRIMARY KEY,
    transaction_date DATE,
    product_id INT,
    customer_id INT,
    location_id INT,
    quantity INT,
    total_amount DECIMAL(10, 2),
    FOREIGN KEY (transaction_date) REFERENCES DateDimension(date_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (location_id) REFERENCES Locations(location_id)
)''')

#-----------------------------
# Step 5: Load data into MySQL
#-----------------------------
for _, row in date_dimension.iterrows():
    cursor.execute('''
    INSERT INTO DateDimension (date_id, year, month, day, weekday, quarter)
    VALUES (%s, %s, %s, %s, %s, %s)
    ''', tuple(row))

for _, row in products_df.iterrows():
    cursor.execute('''
    INSERT INTO Products (product_id, product_name, category, price)
    VALUES (%s, %s, %s, %s)
    ''', tuple(row))

for _, row in customers_df.iterrows():
    cursor.execute('''
    INSERT INTO Customers (customer_id, customer_name, email, phone)
    VALUES (%s, %s, %s, %s)
    ''', tuple(row))

for _, row in locations_df.iterrows():
    cursor.execute('''
    INSERT INTO Locations (location_id, city, state, country)
    VALUES (%s, %s, %s, %s)
    ''', tuple(row))

for _, row in transactions_df.iterrows():
    cursor.execute('''
    INSERT INTO SalesTransactions (transaction_id, transaction_date, product_id, customer_id, location_id, quantity, total_amount)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', tuple(row))

#--------------------------
# Step 6: Commit and close
#--------------------------
conn.commit()
cursor.close()
conn.close()
```
## Parameterization

### Read Database Configurtion from  files:

~~~python
#
# Source and Target Database connection details
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

# Command Line Parameter 1: "db_config_source.json"
# This is for a Transactional Database
# db_config_source_file = "db_config_source.json"
db_config_source_file = sys.argv[1]

# Command Line Parameter 2: "db_config_target.json"
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
~~~

## Summary

	This example demonstrated how to implement 
	an ETL process using Python and MySQL to 
	create a star schema from CSV files. Adjust 
	the CSV file paths and database connection 
	details according to your environment.