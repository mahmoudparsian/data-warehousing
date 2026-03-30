# Retail Star Schema – SQL Demo (Star Schema)

```sql
-- =========================================
-- DATABASE
-- =========================================
CREATE DATABASE retail_dw;
USE retail_dw;

-- =========================================
-- DATE DIMENSION
-- =========================================
CREATE TABLE dim_dates (
  date_id INT PRIMARY KEY,
  full_date DATE,
  year INT,
  quarter INT,
  month INT,
  month_name VARCHAR(15),
  day INT
);

INSERT INTO dim_dates VALUES
(20230101,'2023-01-01',2023,1,1,'January',1),
(20230315,'2023-03-15',2023,1,3,'March',15),
(20230710,'2023-07-10',2023,3,7,'July',10),
(20240105,'2024-01-05',2024,1,1,'January',5),
(20240420,'2024-04-20',2024,2,4,'April',20);

-- =========================================
-- CUSTOMER DIMENSION
-- =========================================
CREATE TABLE dim_customers (
  customer_id INT PRIMARY KEY,
  name VARCHAR(50),
  gender VARCHAR(10),
  country VARCHAR(30)
);

INSERT INTO dim_customers VALUES
(1,'Alice','FEMALE','USA'),
(2,'Bob','MALE','USA'),
(3,'Carlos','MALE','MEXICO'),
(4,'Diana','FEMALE','CANADA'),
(5,'Eva','FEMALE','GERMANY');

-- =========================================
-- PRODUCT DIMENSION
-- =========================================
CREATE TABLE dim_products (
  product_id INT PRIMARY KEY,
  product_name VARCHAR(50),
  category VARCHAR(30),
  brand VARCHAR(30)
);

INSERT INTO dim_products VALUES
(101,'Laptop','Electronics','Dell'),
(102,'Phone','Electronics','Apple'),
(103,'Headphones','Accessories','Sony'),
(104,'Desk','Furniture','Ikea'),
(105,'Chair','Furniture','Ikea');

-- =========================================
-- STORE DIMENSION
-- =========================================
CREATE TABLE dim_stores (
  store_id INT PRIMARY KEY,
  store_name VARCHAR(50),
  country VARCHAR(30),
  store_type VARCHAR(20)
);

INSERT INTO dim_stores VALUES
(1,'NY Downtown','USA','PHYSICAL'),
(2,'LA Mall','USA','PHYSICAL'),
(3,'Toronto Central','CANADA','PHYSICAL'),
(4,'Online Store','USA','ONLINE');

-- =========================================
-- FACT TABLE: SALES
-- =========================================
CREATE TABLE fact_sales (
  sales_id INT PRIMARY KEY AUTO_INCREMENT,
  date_id INT,
  customer_id INT,
  product_id INT,
  store_id INT,
  quantity INT,
  unit_price DECIMAL(10,2),
  total_amount DECIMAL(10,2),
  FOREIGN KEY (date_id) REFERENCES dim_dates(date_id),
  FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
  FOREIGN KEY (product_id) REFERENCES dim_products(product_id),
  FOREIGN KEY (store_id) REFERENCES dim_stores(store_id)
);

INSERT INTO fact_sales
(date_id, customer_id, product_id, store_id, quantity, unit_price, total_amount)
VALUES
(20230101,1,101,1,1,1200,1200),
(20230315,2,102,2,2,900,1800),
(20230710,3,103,4,3,150,450),
(20240105,4,104,3,1,400,400),
(20240420,5,105,4,4,100,400),
(20240420,1,102,4,1,950,950),
(20230315,2,103,1,2,140,280),
(20240105,3,101,4,1,1250,1250);

-- =========================================
-- OLAP QUERY 1: Total revenue by year
-- =========================================
SELECT d.year, SUM(f.total_amount) AS total_revenue
FROM fact_sales f
JOIN dim_dates d ON f.date_id = d.date_id
GROUP BY d.year;

-- =========================================
-- OLAP QUERY 2: Revenue by product category
-- =========================================
SELECT p.category, SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.category;

-- =========================================
-- OLAP QUERY 3: Top 3 products by revenue
-- =========================================
SELECT p.product_name, SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 3;

-- =========================================
-- OLAP QUERY 4: Revenue by customer country
-- =========================================
SELECT c.country, SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.country;

-- =========================================
-- OLAP QUERY 5: Online vs Physical store revenue
-- =========================================
SELECT s.store_type, SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_stores s ON f.store_id = s.store_id
GROUP BY s.store_type;

-- =========================================
-- OLAP QUERY 6: Average order value per store
-- =========================================
SELECT s.store_name, AVG(f.total_amount) AS avg_order_value
FROM fact_sales f
JOIN dim_stores s ON f.store_id = s.store_id
GROUP BY s.store_name;

-- =========================================
-- OLAP QUERY 7: Monthly revenue trend
-- =========================================
SELECT d.year, d.month_name, SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_dates d ON f.date_id = d.date_id
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;

-- =========================================
-- OLAP QUERY 8: Best-selling products per year
-- =========================================
SELECT d.year, p.product_name, SUM(f.quantity) AS units_sold
FROM fact_sales f
JOIN dim_dates d ON f.date_id = d.date_id
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY d.year, p.product_name
ORDER BY d.year, units_sold DESC;

-- =========================================
-- OLAP QUERY 9: Customer lifetime value (CLV)
-- =========================================
SELECT c.name, SUM(f.total_amount) AS lifetime_value
FROM fact_sales f
JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.name
ORDER BY lifetime_value DESC;

-- =========================================
-- OLAP QUERY 10: Revenue by category over years
-- =========================================
SELECT d.year, p.category, SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_dates d ON f.date_id = d.date_id
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY d.year, p.category
ORDER BY d.year, p.category;

-- =========================================
-- OLAP QUERY 11: Customers who have never purchased any products
-- =========================================
SELECT c.customer_id, c.name, c.country
FROM dim_customers c
LEFT JOIN fact_sales f
  ON c.customer_id = f.customer_id
WHERE f.customer_id IS NULL;

-- =========================================
-- OLAP QUERY 12: Products that have never been sold
-- =========================================
SELECT p.product_id, p.product_name, p.category
FROM dim_products p
LEFT JOIN fact_sales f
  ON p.product_id = f.product_id
WHERE f.product_id IS NULL;


```

