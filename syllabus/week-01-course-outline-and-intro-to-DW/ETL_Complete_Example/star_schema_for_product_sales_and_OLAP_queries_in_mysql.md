# Star Schema and OLAP Queries

Using python, MySQL database, Provide  a 
star schema, which is about customers, 
sales of products in different locations 
then provide some sample OLAP queries 
for the given star schema.

Let's create a star schema for a sales 
database that includes customers, sales 
of products, and different locations. 
We'll use Python to interact with a 
MySQL database.

This script creates the star schema, inserts 
sample data, and performs OLAP queries using 
Python and MySQL.


### Step 1: Define the Star Schema

The star schema will consist of:

1. **Fact Table: `sales_fact`**
   - sale_id (INT)
   - product_id (INT)
   - customer_id (INT)
   - location_id (INT)
   - date_id (INT)
   - quantity (INT)
   - total_amount (DECIMAL)

2. **Dimension Table: `products_dim`**
   - product_id (INT)
   - product_name (VARCHAR)
   - category (VARCHAR)
   - price (DECIMAL)

3. **Dimension Table: `customers_dim`**
   - customer_id (INT)
   - customer_name (VARCHAR)
   - age (INT)
   - gender (VARCHAR)

4. **Dimension Table: `locations_dim`**
   - location_id (INT)
   - city (VARCHAR)
   - state (VARCHAR)
   - country (VARCHAR)

5. **Dimension Table: `dates_dim`**
   - date_id (INT)
   - date (DATE)
   - day (INT)
   - month (INT)
   - year (INT)
   - quarter (INT)

### Step 2: Create the Schema in MySQL

Here is the SQL script to create the schema:

```sql
CREATE DATABASE IF NOT EXISTS sales_db;
USE sales_db;

-- Create dimension tables
CREATE TABLE IF NOT EXISTS products_dim (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(50),
    category VARCHAR(50),
    price DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS customers_dim (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(50),
    age INT,
    gender VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS locations_dim (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS dates_dim (
    date_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    day INT,
    month INT,
    year INT,
    quarter INT
);

-- Create fact table
CREATE TABLE IF NOT EXISTS sales_fact (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
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
```

### Step 3: Insert Sample Data

Here is the SQL script to insert sample data:

```sql
USE sales_db;

-- Insert data into dimension tables
INSERT INTO products_dim (product_name, category, price) VALUES
('Laptop', 'Electronics', 999.99),
('Smartphone', 'Electronics', 499.99),
('Tablet', 'Electronics', 299.99);

INSERT INTO customers_dim (customer_name, age, gender) VALUES
('Alice', 30, 'Female'),
('Bob', 25, 'Male'),
('Charlie', 35, 'Male');

INSERT INTO locations_dim (city, state, country) VALUES
('New York', 'NY', 'USA'),
('San Francisco', 'CA', 'USA'),
('Los Angeles', 'CA', 'USA');

INSERT INTO dates_dim (date, day, month, year, quarter) VALUES
('2025-01-01', 1, 1, 2025, 1),
('2025-01-02', 2, 1, 2025, 1),
('2025-01-03', 3, 1, 2025, 1);

-- Insert data into fact table
INSERT INTO sales_fact (product_id, customer_id, location_id, date_id, quantity, total_amount) VALUES
(1, 1, 1, 1, 2, 1999.98),
(2, 2, 2, 2, 1, 499.99),
(3, 3, 3, 3, 3, 899.97);
```

### Step 4: Perform OLAP Queries

Here are some sample OLAP queries:

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

6. **Find top-2 selling products per country**


### Step 5: Python Script to Create Schema and Insert Data

Here is a Python script to create the schema, insert data, and run the OLAP queries:

```python
import mysql.connector
import pandas as pd

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

# Create dimension tables and fact table
cursor.execute('''
CREATE TABLE IF NOT EXISTS products_dim (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(50),
    category VARCHAR(50),
    price DECIMAL(10, 2)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS customers_dim (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(50),
    age INT,
    gender VARCHAR(10)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS locations_dim (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS dates_dim (
    date_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    day INT,
    month INT,
    year INT,
    quarter INT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS sales_fact (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
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

# Insert sample data into dimension tables and fact table
cursor.execute('''
INSERT INTO products_dim (product_name, category, price) VALUES
('Laptop', 'Electronics', 999.99),
('Smartphone', 'Electronics', 499.99),
('Tablet', 'Electronics', 299.99);
''')

cursor.execute('''
INSERT INTO customers_dim (customer_name, age, gender) VALUES
('Alice', 30, 'Female'),
('Bob', 25, 'Male'),
('Charlie', 35, 'Male');
''')

cursor.execute('''
INSERT INTO locations_dim (city, state, country) VALUES
('New York', 'NY', 'USA'),
('San Francisco', 'CA', 'USA'),
('Los Angeles', 'CA', 'USA');
''')

cursor.execute('''
INSERT INTO dates_dim (date, day, month, year, quarter) VALUES
('2025-01-01', 1, 1, 2025, 1),
('2025-01-02', 2, 1, 2025, 1),
('2025-01-03', 3, 1, 2025, 1);
''')

cursor.execute('''
INSERT INTO sales_fact (product_id, customer_id, location_id, date_id, quantity, total_amount) VALUES
(1, 1, 1, 1, 2, 1999.98),
(2, 2, 2, 2, 1, 499.99),
(3, 3, 3, 3, 3, 899.97);
''')

# Commit the transaction
conn.commit()

# Perform OLAP queries
# Total Sales Amount by Product
query = '''
SELECT p.product_name, SUM(s.total_amount) AS total_sales_amount
FROM sales_fact s
JOIN products_dim p ON s.product_id = p.product_id
GROUP BY p.product_name;
'''
df = pd.read_sql(query, conn)
print(df)

# Sales Quantity by Customer
query = '''
SELECT c.customer_name, SUM(s.quantity) AS total_quantity
FROM sales_fact s
JOIN customers_dim c ON s.customer_id = c.customer_id
GROUP BY c.customer_name;
'''
df = pd.read_sql(query, conn)
print(df)

# Total Sales by Location
query = '''
SELECT l.city, SUM(s.total_amount) AS total_sales_amount
FROM sales_fact s
JOIN locations_dim l ON s.location_id = l.location_id
GROUP BY l.city;
'''
df = pd.read_sql(query, conn)
print(df)

# Sales Amount by Month
query = '''
SELECT d.month, SUM(s.total_amount) AS total_sales_amount
FROM sales_fact s
JOIN dates_dim d ON s.date_id = d.date_id
GROUP BY d.month;
'''
df = pd.read_sql(query, conn)
print(df)

# Average Sales Amount by Customer Age Group
query = '''
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
'''
df = pd.read_sql(query, conn)
print(df)

# Close the connection
cursor.close()
conn.close()
```

