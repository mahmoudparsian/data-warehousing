# Sales Data Analysis Project with SQL

## 1. Prepare Metadata Original 

~~~sql
-- -----------------------------
-- Create a table for sales data
-- -----------------------------
CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    sale_date DATE,
    product_id INT,
    quantity INT,
    price DECIMAL(10, 2)
);
~~~

## 2. Prepare Derived Metadata from Original 

### 2.1 Derived Data

* `year` is derived from `sale_date`
* `quarter` is derived from `sale_date`

### 2.2 Quarter Definition

There are 4 quarters per year:

~~~
-- -----------------------------------
-- Note that each year has 4 quarters:
-- -----------------------------------
Quarter 1: January (1), February (2), March (3)
Quarter 2: April (4), May (5), June (6)
Quarter 3: July (7), August (8), September (9)
Quarter 4: October (10), November (11), December (12)

~~~

### 2.3 Prepare Derived Metadata & Apply Transformations

~~~sql
-- -----------------------------
-- Create a table for sales data
-- -----------------------------
CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    sale_date DATE,
    sale_year INT,         -- DERIVED
    sale_quarter INT,      -- DERIVED
    product_id INT,
    quantity INT,
    price DECIMAL(10, 2)
);
~~~



## 3. Populate Data

~~~sql

-- --------------------------------------------
-- Insert some sample data into the sales table
-- --------------------------------------------
INSERT INTO sales 
(sale_id, sale_date, sale_year, sale_quarter, product_id, quantity, price) 
VALUES
(1, '2024-01-01', 2024, 1, 101, 2, 19.99),
(2, '2024-01-02', 2024, 1, 102, 1, 29.99),
(3, '2024-01-02', 2024, 1, 101, 1, 19.99),
(4, '2024-01-03', 2024, 1, 103, 3, 9.99),
(5, '2024-11-07', 2024, 4, 104, 1, 39.99),
(6, '2024-12-05', 2024, 4, 104, 3, 3.99),
(7, '2024-04-05', 2024, 2, 105, 2, 23.99);
~~~


## 4. Query Data

### Query-1: Calculate total sales

~~~sql
-- ---------------------
-- Calculate total sales
-- ---------------------
SELECT SUM(quantity * price) AS total_sales
FROM sales;
~~~

### Query-2: Calculate total sales per year

~~~sql
-- ---------------------
-- Calculate total sales
-- ---------------------
SELECT year, SUM(quantity * price) AS total_sales
FROM sales
GROUP BY year;
~~~

### Query-3: Calculate average sales per day

~~~sql
-- -------------------------------
-- Calculate average sales per day
-- -------------------------------
SELECT sale_date, AVG(quantity * price) AS average_sales
FROM sales
GROUP BY sale_date;
~~~

### Query-4: Identify top-selling products

~~~sql
-- -----------------------------
-- Identify top-selling products
-- ------------------------------
SELECT product_id, SUM(quantity) AS total_quantity_sold
FROM sales
GROUP BY product_id
ORDER BY total_quantity_sold DESC;
~~~

### Query-5: Calculate total sales per year and quarter

~~~sql
-- -------------------------------------------
-- Calculate total sales per year and quarter
-- -------------------------------------------
SELECT year, quarter, SUM(quantity * price) AS total_sales
FROM sales
GROUP BY year, quarter;
~~~

### Query-6: Find the best year and quarter of total sales

~~~sql
-- ---------------------------------------------
-- Find the best year and quarter of total sales
-- ---------------------------------------------
SELECT year, quarter, SUM(quantity * price) AS total_sales
FROM sales
GROUP BY year, quarter;
ORDER by total_sales DESC
LIMIT 1;
~~~

## 5. Homework

### Query-7: Find the best quarter per year of total sales

### Query-8: Find the worst quarter per year of total sales

### Query-9: Find the best and worst quarter per year of total sales