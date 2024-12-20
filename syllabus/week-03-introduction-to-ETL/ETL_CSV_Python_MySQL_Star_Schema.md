# ETL to Create Star Schema using Python & MySQL

	1. Using Python and MySQL, provide 
	   a complete  example of  ETL  to 
	   create a star schema. 
	
	2. Provide sample input data as well.

	3. Let's walk through a complete example 
	   of ETL (Extract, Transform, Load) to 
	   create a star schema using Python and MySQL. 
	
	4. We'll start with sample input data and 
	   then proceed with the ETL process.

## High-Level Steps Explanation:

1. **Extract**: Load the data from CSV files using `pandas`.

2. **Transform**:
   - Convert the `date` column to datetime format.
   - Create a new `year` column from `date` 
   - Create a new `quarter` column from `date` 
   - Create dimension tables (`date_dim`, `product_dim`, `store_dim`).
   - Create a fact table (`fact_sales`) with a calculated `total_sales` column.
   
3. **Load**:
   - Establish a connection to MySQL.
   - Create the necessary tables if they do not exist.
   - Insert data into the dimension and fact tables.


## Sample Input Data

We'll use three CSV files representing sales, products, and stores:


### `sales.csv`

~~~
date,product_id,store_id,quantity,price
2024-12-01,1,1,10,20.00
2024-12-01,2,1,5,30.00
2024-12-02,1,2,7,20.00
2024-12-02,3,2,3,40.00
~~~

### `products.csv`

```
product_id,product_name,category
1,Widget A,Widgets
2,Widget B,Widgets
3,Gadget A,Gadgets
```

### `stores.csv`

```
store_id,store_name,location
1,Store One,New York
2,Store Two,Los Angeles
```

## Step-by-Step ETL Process

### 1. Extract Data

In this step, we read data from multiple sources:

#### 1.1  Extract Data from CSV files ...

```python
import pandas as pd

# Method-1: Load data from CSV files
sales_data = pd.read_csv('sales.csv')
product_data = pd.read_csv('products.csv')
store_data = pd.read_csv('stores.csv')
```

#### 1.2  Extract Data from database tables ...
```python
# Method-2: EXERCISE: Load data from MySQL Tables
sales_data = ...
product_data = ...
store_data = ...
```

### 2. Transform Data

In this step, we perform transformations:

* create FACT and DIMENSION tables
* clean up data
* data conversions
* data type conversions
* create new columns
* create derived columns
* ...

#### 2.1 Understand data type conversion

```python
>>> import pandas as pd
>>> d = '2024-12-18'
>>> d2 = pd.to_datetime(d)
>>> d
'2024-12-18'
>>> d2
Timestamp('2024-12-18 00:00:00')
>>> type(d)
<class 'str'>
>>> type(d2)
<class 'pandas._libs.tslibs.timestamps.Timestamp'>
```

#### 2.2 Transformations ...

```python
# Convert date column to pandas datetime object
sales_data['date'] = pd.to_datetime(sales_data['date'])

# Create a date dimension
date_dim = sales_data['date'].dt.date.unique()
date_dim = pd.DataFrame(date_dim, columns=['date'])

# Create 'year' column from a 'date' column
date_dim['year'] = date_dim['date'].dt.year

# Each year has 4 quarters: 1, 2, 3, 4
# Create 'quarter' column from a 'date' column
date_dim['quarter'] = date_dim['date'].dt.quarter


# Create a product dimension
product_dim = product_data[['product_id', 'product_name', 'category']]

# Create a store dimension
store_dim = store_data[['store_id', 'store_name', 'location']]

# Create a fact table
fact_sales = sales_data[['date', 'product_id', 'store_id', 'quantity', 'price']]
fact_sales['date'] = fact_sales['date'].dt.date
fact_sales['total_sales'] = fact_sales['quantity'] * fact_sales['price']
```

### 3. Load Data into MySQL

#### 3.1 Create database Tables

```python
import mysql.connector

# Establish MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database"
)
cursor = conn.cursor()

# Create tables
# quarter: 1, 2, 3, 4
cursor.execute("""
CREATE TABLE IF NOT EXISTS date_dim (
    date DATE PRIMARY KEY,
    year INT,
    quarter INT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS product_dim (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(255)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS store_dim (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(255),
    location VARCHAR(255)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS fact_sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    product_id INT,
    store_id INT,
    quantity INT,
    price DECIMAL(10, 2),
    total_sales DECIMAL(10, 2),
    FOREIGN KEY (date) REFERENCES date_dim(date),
    FOREIGN KEY (product_id) REFERENCES product_dim(product_id),
    FOREIGN KEY (store_id) REFERENCES store_dim(store_id)
)
""")
```

#### 3.2 Load Data into MySQL

	---- NOTE: ---------------------
	In this example, we load data row-by-row, 
	which might not be  an  ideal  case from 
	performance point of view. You should use 
	BULK-LOADERS to load rows from text (or 
	Parquet) files

#### Insert data into dimension tables

```python 
date_insert = """
INSERT IGNORE INTO date_dim (date, year, quarter) 
VALUES (%s, %s, %s)
"""
for _, row in date_dim.iterrows():
    cursor.execute(date_insert, (row['date'], row['year'], row['quarter']))


product_insert = """
INSERT IGNORE INTO product_dim (product_id, product_name, category) 
VALUES (%s, %s, %s)
"""
for _, row in product_dim.iterrows():
    cursor.execute(product_insert,
     (row['product_id'], row['product_name'], row['category']))


store_insert = """
INSERT IGNORE INTO store_dim (store_id, store_name, location)
 VALUES (%s, %s, %s)
"""
for _, row in store_dim.iterrows():
    cursor.execute(store_insert,
     (row['store_id'], row['store_name'], row['location']))
```

####  Insert data into fact table

```python
fact_insert = """
    INSERT INTO fact_sales 
    (date, product_id, store_id, quantity, price, total_sales)
    VALUES (%s, %s, %s, %s, %s, %s)
"""
for _, row in fact_sales.iterrows():
    cursor.execute(fact_insert, 
    (row['date'], row['product_id'], row['store_id'], 
     row['quantity'], row['price'], row['total_sales']))

# Commit and close connection
conn.commit()
cursor.close()
conn.close()
```


### Notes:

* This example demonstrates a basic ETL process to create a star schema in a MySQL database using Python. 

* Adjust the column names and data types as needed for your specific use case.
