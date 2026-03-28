# MySQL Transactional --> ETL --> Star Schema

Using python, MySQL database, Provide 
a complete ETL from transactional data, 
which contains sales of products (as a 
set of relational table) to customers. 
This python based ETL should produce a 
star schema. 

This python-based ETL should read data 
from relational tables and then provide 
a complete star schema. This ETL should 
perform some solid transformations and 
then load data to a star schema based 
warehouse.  

This  ETL process with examples with sale 
of products for customers in different 
dates and locations. The dimension tables 
should be products, customers, locations, 
and dates. Provide a detailed examples and 
data for a fact table and its associated 
dimension tables and some sample OLAP 
queries for the given star schema.

Let's walk through a complete ETL process 
using Python and MySQL to transform transactional 
data into a star schema. We'll use the Python's
`mysql-connector-python` library for database 
operations and `pandas` for data manipulation.

### Step 1: Set Up the Environment

First, we need to install the required libraries:

```bash
pip install pandas
pip install mysql-connector-python 
```

### Step 2: Define the Transactional Data

We'll define the sample transactional data as 
relational tables in MySQL. Below is the SQL 
script to create and populate the tables:

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
    total_amount DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(50),
    category VARCHAR(50),
    price DECIMAL(10, 2)
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
(1, 1, 1, '2025-01-01', 2, 1999.98),
(2, 2, 2, '2025-01-02', 1, 499.99),
(3, 3, 3, '2025-01-03', 3, 899.97);

INSERT INTO products (product_name, category, price) VALUES
('Laptop', 'Electronics', 999.99),
('Smartphone', 'Electronics', 499.99),
('Tablet', 'Electronics', 299.99);

INSERT INTO customers (customer_name, age, gender) VALUES
('Alice', 30, 'Female'),
('Bob', 25, 'Male'),
('Charlie', 35, 'Male');

INSERT INTO locations (city, state, country) VALUES
('New York', 'NY', 'USA'),
('San Francisco', 'CA', 'USA'),
('Los Angeles', 'CA', 'USA');
```

### Step 3: ETL Process

Now we'll implement the ETL process in Python.

```python
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

# Database connection details
db_config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'database': 'sales_db'
}

# Create a connection to the MySQL database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Extract data from transactional tables
sales_df = pd.read_sql('SELECT * FROM sales_transactions', conn)
products_df = pd.read_sql('SELECT * FROM products', conn)
customers_df = pd.read_sql('SELECT * FROM customers', conn)
locations_df = pd.read_sql('SELECT * FROM locations', conn)

# Transform the data to fit the star schema

# Create the dates dimension table
dates_df = sales_df[['sale_date']].drop_duplicates().reset_index(drop=True)
dates_df['date_id'] = dates_df.index + 1
dates_df['date'] = pd.to_datetime(dates_df['sale_date'])
dates_df['day'] = dates_df['date'].dt.day
dates_df['month'] = dates_df['date'].dt.month
dates_df['year'] = dates_df['date'].dt.year
dates_df['quarter'] = dates_df['date'].dt.quarter

# Create the fact table
fact_sales_df = sales_df.merge(dates_df[['sale_date', 'date_id']], on='sale_date')
fact_sales_df = fact_sales_df[['sale_id', 'product_id', 'customer_id', 'location_id', 'date_id', 'quantity', 'total_amount']]

# Load the transformed data into the star schema tables

# Create an SQLAlchemy engine for pandas to_sql method
engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")

# Create dimension tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS products_dim (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(50),
    category VARCHAR(50),
    price DECIMAL(10, 2)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS customers_dim (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(50),
    age INT,
    gender VARCHAR(10)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS locations_dim (
    location_id INT PRIMARY KEY,
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS dates_dim (
    date_id INT PRIMARY KEY,
    date DATE,
    day INT,
    month INT,
    year INT,
    quarter INT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS sales_fact (
    sale_id INT PRIMARY KEY,
    product_id INT,
    customer_id INT,
    location_id INT,
    date_id INT,
    quantity INT,
    total_amount DECIMAL(10, 2),
    FOREIGN KEY (product_id) REFERENCES products_dim (product_id),
    FOREIGN KEY (customer_id) REFERENCES customers_dim (customer_id),
    FOREIGN KEY (location_id) REFERENCES locations_dim (location_id),
    FOREIGN KEY (date_id) REFERENCES dates_dim (date_id)
);
''')

# Insert data into dimension tables
products_df.to_sql('products_dim', engine, if_exists='append', index=False)
customers_df.to_sql('customers_dim', engine, if_exists='append', index=False)
locations_df.to_sql('locations_dim', engine, if_exists='append', index=False)
dates_df[['date_id', 'date', 'day', 'month', 'year', 'quarter']].to_sql('dates_dim', engine, if_exists='append', index=False)

# Insert data into fact table
fact_sales_df.to_sql('sales_fact', engine, if_exists='append', index=False)

# Commit and close the connection
conn.commit()
cursor.close()
conn.close()
```

### Step 4: Sample OLAP Queries

Finally, we can perform some OLAP queries to analyze the data.

1. **Total Sales Amount by Product:**

   ```sql
   SELECT p.product_name, SUM(s.total_amount) AS total_sales_amount
   FROM sales_fact s
   JOIN products_dim p ON s.product_id = p.product_id
   GROUP BY p.product_name;
   ```

2. **Sales Quantity by Customer:**

   ```sql
   SELECT c.customer_name, SUM(s.quantity) AS total_quantity
   FROM sales_fact s
   JOIN customers_dim c ON s.customer_id = c.customer_id
   GROUP BY c.customer_name;
   ```

3. **Total Sales by Location:**

   ```sql
   SELECT l.city, SUM(s.total_amount) AS total_sales_amount
   FROM sales_fact s
   JOIN locations_dim l ON s.location_id = l.location_id
   GROUP BY l.city;
   ```

4. **Sales Amount by Month:**

   ```sql
   SELECT d.month, SUM(s.total_amount) AS total_sales_amount
   FROM sales_fact s
   JOIN dates_dim d ON s.date_id = d.date_id
   GROUP BY d.month;
   ```

5. **Average Sales Amount by Customer Age Group:**

   ```sql
   SELECT
       CASE
           WHEN c.age < 20 THEN 'Under 20'
           WHEN c.age BETWEEN 20 AND 29 THEN '20-29'
           WHEN c.age BETWEEN 30 AND 39 THEN '30-39'
           ELSE '40 and above'
       END AS age_group,
       AVG(s.total_amount) AS average_sales_amount
   FROM sales_fact s
   JOIN customers_dim c ON s.customer_id = c.customer_id
   GROUP BY age_group;
   ```

6. **Find top-2 selling products per country**

~~~sql
WITH RankedSales AS (
    SELECT
        P.product_name as product,
        L.country as country,
        SUM(F.total_amount) AS total_sales,
        RANK() OVER (PARTITION BY F.location_id ORDER BY SUM(F.total_amount) DESC) AS sales_rank
    FROM sales_fact F
    JOIN products_dim P on  F.product_id = P.product_id
    JOIN locations_dim L on F.location_id = L.location_id
    GROUP BY product, country
)
SELECT
    product,
    country,
    total_sales,
    sales_rank
FROM RankedSales
WHERE sales_rank <= 2
ORDER BY country, sales_rank;
~~~

Explanation:

~~~
WITH RankedSales AS (...): This Common Table Expression (CTE)
     calculates the total sales for each product in each
     country and assigns a rank based on the total sales amount.

SUM(total_amount): Aggregates the total sales amount for each
    product within each country.

RANK() OVER (PARTITION BY country ORDER BY SUM(total_amount) DESC):
       Assigns a rank to each product within each country based on
       the total sales amount, with the highest sales amount getting rank 1.

SELECT ... FROM RankedSales WHERE sales_rank <= 2: Filters the
    results to include only the top-2 products for each country.

ORDER BY country, sales_rank: Orders the final results by country
      and then by the rank.
~~~

### find the top-2 selling products per country

	To find the top-2 selling products per country 
	based on the total amount sold, you can use the 
	following SQL query.
	
	This query uses window functions to rank the products 
	by their total sales amount within each country and 
	then filters to keep only the top-2 products for each country.

~~~sql
-- PARTITION BY F.location_id
mysql> WITH RankedSales AS (
    ->     SELECT
    ->         P.product_name as product,
    ->         L.country as country,
    ->         SUM(F.total_amount) AS total_sales,
    ->         RANK() OVER (PARTITION BY F.location_id ORDER BY SUM(F.total_amount) DESC) AS sales_rank
    ->     FROM sales_fact F
    ->     JOIN products_dim P on  F.product_id = P.product_id
    ->     JOIN locations_dim L on F.location_id = L.location_id
    ->     GROUP BY product, country
    -> )
    -> SELECT
    ->     product,
    ->     country,
    ->     total_sales,
    ->     sales_rank
    -> FROM RankedSales
    -> WHERE sales_rank <= 2
    -> ORDER BY country, sales_rank;
+------------+---------+-------------+------------+
| product    | country | total_sales | sales_rank |
+------------+---------+-------------+------------+
| Cooler     | CANADA  |  2723400.00 |          1 |
| Laptop     | CANADA  |  8253900.00 |          1 |
| TV         | CANADA  |  7456260.00 |          1 |
| Ladder     | CANADA  |  1061280.00 |          2 |
| Ipad       | CANADA  |  6563900.00 |          2 |
| Smartphone | CANADA  |  4184550.00 |          2 |
| TV         | USA     | 19873520.00 |          1 |
| Ipad       | USA     | 16804200.00 |          1 |
| Ladder     | USA     |  2878200.00 |          1 |
| Laptop     | USA     | 21704400.00 |          1 |
| Cooler     | USA     |  7350900.00 |          1 |
| Modem      | USA     |  4873000.00 |          1 |
| Table      | USA     |  4157690.00 |          1 |
| Tablet     | USA     |  6840680.00 |          2 |
| Charger    | USA     |  1336445.00 |          2 |
| Smartphone | USA     | 10792800.00 |          2 |
| Cooker     | USA     |  1220900.00 |          2 |
| Chair      | USA     |   964120.00 |          2 |
+------------+---------+-------------+------------+
18 rows in set (0.57 sec)
~~~


~~~sql
-- PARTITION BY L.country
WITH RankedSales AS (
    SELECT
        P.product_name as product,
        L.country as country,
        SUM(F.total_amount) AS total_sales,
        RANK() OVER (PARTITION BY L.country ORDER BY SUM(F.total_amount) DESC) AS sales_rank
    FROM sales_fact F
    JOIN products_dim P on  F.product_id = P.product_id
    JOIN locations_dim L on F.location_id = L.location_id
    GROUP BY product, country
)
SELECT
    product,
    country,
    total_sales,
    sales_rank
FROM RankedSales
WHERE sales_rank <= 2
ORDER BY country, sales_rank;

mysql> WITH RankedSales AS (
    ->     SELECT
    ->         P.product_name as product,
    ->         L.country as country,
    ->         SUM(F.total_amount) AS total_sales,
    ->         RANK() OVER (PARTITION BY L.country ORDER BY SUM(F.total_amount) DESC) AS sales_rank
    ->     FROM sales_fact F
    ->     JOIN products_dim P on  F.product_id = P.product_id
    ->     JOIN locations_dim L on F.location_id = L.location_id
    ->     GROUP BY product, country
    -> )
    -> SELECT
    ->     product,
    ->     country,
    ->     total_sales,
    ->     sales_rank
    -> FROM RankedSales
    -> WHERE sales_rank <= 2
    -> ORDER BY country, sales_rank;
+---------+---------+-------------+------------+
| product | country | total_sales | sales_rank |
+---------+---------+-------------+------------+
| Laptop  | CANADA  |  8253900.00 |          1 |
| TV      | CANADA  |  7456260.00 |          2 |
| Laptop  | USA     | 21704400.00 |          1 |
| TV      | USA     | 19873520.00 |          2 |
+---------+---------+-------------+------------+
4 rows in set (0.56 sec)
~~~


# Summary 

This complete ETL process demonstrates how to 
extract data from transactional tables, transform 
and load it into a star schema, and perform OLAP 
queries for data analysis using Python and MySQL.

