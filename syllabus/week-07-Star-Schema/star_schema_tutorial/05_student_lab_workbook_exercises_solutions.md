
# MASTER TUTORIAL: STAR SCHEMA (Complete A–Z with Advanced Modules)

Audience: Data Warehousing / BI / Analytics Students  
Level: Beginner → Advanced  
Environment: MySQL (OLTP + DW)

============================================================
SECTION 1 — FOUNDATIONS
============================================================

1.1 What is a Star Schema?

A Star Schema is a dimensional model composed of:

• One central FACT table  
• Multiple surrounding DIMENSION tables  

Purpose:
- Simplify analytics
- Improve aggregation performance
- Make BI reporting intuitive

============================================================
SECTION 2 — FULL REALISTIC 100K+ DATASET DESIGN
============================================================

OLTP Tables:
- customers (1,000 rows)
- products (2,000 rows)
- stores (50 rows)
- orders (100,000 rows)
- order_items (300,000 rows)

------------------------------------------------------------
OLTP TABLE DEFINITIONS
------------------------------------------------------------

CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    country VARCHAR(50),
    created_at DATETIME
);

CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100),
    category VARCHAR(50),
    brand VARCHAR(50),
    price DECIMAL(10,2)
);

CREATE TABLE stores (
    store_id INT PRIMARY KEY AUTO_INCREMENT,
    store_name VARCHAR(100),
    region VARCHAR(50)
);

CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    store_id INT,
    order_date DATE
);

CREATE TABLE order_items (
    order_item_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    order_id BIGINT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2)
);

------------------------------------------------------------
DATA GENERATION (100K+ EXAMPLE)
------------------------------------------------------------

Example using helper numbers table:

INSERT INTO orders (customer_id, store_id, order_date)
SELECT 
    FLOOR(1 + RAND()*1000),
    FLOOR(1 + RAND()*50),
    DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*365) DAY)
FROM seq_1_to_100000;

============================================================
SECTION 3 — STAR SCHEMA DESIGN
============================================================

Grain: One row per product per order.

------------------------------------------------------------
DIMENSION TABLES
------------------------------------------------------------

CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    full_date DATE,
    year INT,
    quarter INT,
    month INT,
    month_name VARCHAR(20),
    day INT,
    weekday VARCHAR(20)
);

CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    country VARCHAR(50),
    effective_date DATE,
    expiry_date DATE,
    is_current BOOLEAN
);

CREATE TABLE dim_product (
    product_key INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT,
    product_name VARCHAR(100),
    category VARCHAR(50),
    brand VARCHAR(50)
);

------------------------------------------------------------
FACT TABLE
------------------------------------------------------------

CREATE TABLE fact_sales (
    sales_key BIGINT PRIMARY KEY AUTO_INCREMENT,
    date_id INT,
    customer_key INT,
    product_key INT,
    store_id INT,
    quantity INT,
    sales_amount DECIMAL(12,2)
);

============================================================
SECTION 4 — ETL PROCESS (OLTP → STAR)
============================================================

Load Dimensions:

INSERT INTO dim_product (product_id, product_name, category, brand)
SELECT product_id, product_name, category, brand
FROM products;

Load Fact Table:

INSERT INTO fact_sales (
    date_id, customer_key, product_key, store_id,
    quantity, sales_amount
)
SELECT
    DATE_FORMAT(o.order_date, '%Y%m%d'),
    dc.customer_key,
    dp.product_key,
    o.store_id,
    oi.quantity,
    oi.quantity * oi.unit_price
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN dim_customer dc ON o.customer_id = dc.customer_id
JOIN dim_product dp ON oi.product_id = dp.product_id;

============================================================
SECTION 5 — SCD TYPE 2 WALKTHROUGH
============================================================

Purpose: Preserve history when attributes change.

Expire old row:

UPDATE dim_customer
SET expiry_date = CURDATE() - INTERVAL 1 DAY,
    is_current = FALSE
WHERE customer_id = 101
AND is_current = TRUE;

Insert new row:

INSERT INTO dim_customer (
    customer_id, first_name, last_name, country,
    effective_date, expiry_date, is_current
)
VALUES (
    101, 'John', 'Smith', 'Canada',
    CURDATE(), '9999-12-31', TRUE
);

============================================================
SECTION 6 — SNOWFLAKE vs STAR
============================================================

Feature Comparison:

Star Schema:
- Denormalized
- Fewer joins
- Faster queries
- Simpler design

Snowflake Schema:
- Normalized dimensions
- More joins
- Saves space
- More complex

============================================================
SECTION 7 — ADVANCED OLAP QUERIES
============================================================

Revenue by Year:

SELECT d.year, SUM(f.sales_amount)
FROM fact_sales f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year;

Top 10 Customers:

WITH customer_sales AS (
    SELECT customer_key,
           SUM(sales_amount) AS total_sales
    FROM fact_sales
    GROUP BY customer_key
)
SELECT *
FROM customer_sales
ORDER BY total_sales DESC
LIMIT 10;

============================================================
SECTION 8 — COMPLETE LAB MODULE
============================================================

Lab 1: Build OLTP (100K rows)
Lab 2: Design Star Schema
Lab 3: Write ETL SQL
Lab 4: Implement SCD Type 2
Lab 5: Write 10 OLAP queries
Lab 6: Performance comparison

============================================================
SECTION 9 — TEACHING SLIDES CONTENT
============================================================

Slide 1: What is Dimensional Modeling?
Slide 2: Fact vs Dimension
Slide 3: Defining Grain
Slide 4: Star Architecture Diagram
Slide 5: ETL Flow
Slide 6: SCD Types (1,2,3)
Slide 7: Snowflake Comparison
Slide 8: OLAP Examples
Slide 9: Performance Impact
Slide 10: Summary

============================================================
FINAL TAKEAWAY
============================================================

Star Schema:

• Separates metrics from descriptive data  
• Optimizes aggregation workloads  
• Simplifies BI development  
• Supports historical tracking  

It is the backbone of enterprise analytics systems.


---

## Appendix: Student Lab Workbook

The dedicated workbook is included in this bundle as well.

Use `README.md` for run order and the separate lab module file below.
