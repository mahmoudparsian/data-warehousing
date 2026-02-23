
-- =============================================================
-- DuckDB Online Sales Star Schema: ONE-SHOT BUILD SCRIPT
-- =============================================================
-- Usage:
--   duckdb online_sales.duckdb < build_and_load_all.sql
-- OR
--   duckdb online_sales.duckdb
--   .read build_and_load_all.sql
--
-- Assumes CSV files are in: ./csv/
-- =============================================================

PRAGMA threads=8;
PRAGMA memory_limit='2GB';

-- -------------------------------------------------------------
-- DROP EXISTING OBJECTS
-- -------------------------------------------------------------
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS dates;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS stores;

DROP SEQUENCE IF EXISTS customer_key_seq;
DROP SEQUENCE IF EXISTS product_key_seq;
DROP SEQUENCE IF EXISTS store_key_seq;
DROP SEQUENCE IF EXISTS sales_key_seq;

-- -------------------------------------------------------------
-- CREATE DIMENSIONS
-- -------------------------------------------------------------

-- Dates
CREATE TABLE dates (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL,
    day_of_month INTEGER NOT NULL,
    day_of_week VARCHAR(10) NOT NULL,
    month_of_year INTEGER NOT NULL,
    month_name VARCHAR(10) NOT NULL,
    quarter INTEGER NOT NULL,
    year INTEGER NOT NULL,
    is_weekend BOOLEAN NOT NULL
);

-- Customers
CREATE SEQUENCE customer_key_seq START 1;

CREATE TABLE customers (
    customer_key INTEGER PRIMARY KEY DEFAULT nextval('customer_key_seq'),
    customer_id VARCHAR(50) UNIQUE,
    customer_name VARCHAR(255) NOT NULL,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('MALE','FEMALE')),
    email VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    segment VARCHAR(50)
);

-- Products
CREATE SEQUENCE product_key_seq START 1;

CREATE TABLE products (
    product_key INTEGER PRIMARY KEY DEFAULT nextval('product_key_seq'),
    product_id VARCHAR(50) UNIQUE,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    brand VARCHAR(100),
    color VARCHAR(50),
    cost DECIMAL(10, 2)
);

-- Stores
CREATE SEQUENCE store_key_seq START 1;

CREATE TABLE stores (
    store_key INTEGER PRIMARY KEY DEFAULT nextval('store_key_seq'),
    store_id VARCHAR(50) UNIQUE,
    store_name VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100)
);

-- -------------------------------------------------------------
-- CREATE FACT TABLE
-- -------------------------------------------------------------

CREATE SEQUENCE sales_key_seq START 1;

CREATE TABLE sales (
    sales_key BIGINT PRIMARY KEY DEFAULT nextval('sales_key_seq'),
    date_key INTEGER NOT NULL,
    customer_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    store_key INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_amount DECIMAL(12, 2) NOT NULL,

    FOREIGN KEY (date_key) REFERENCES dates(date_key),
    FOREIGN KEY (customer_key) REFERENCES customers(customer_key),
    FOREIGN KEY (product_key) REFERENCES products(product_key),
    FOREIGN KEY (store_key) REFERENCES stores(store_key)
);

-- -------------------------------------------------------------
-- LOAD CSV DATA
-- -------------------------------------------------------------

COPY customers FROM 'csv/customers.csv' (AUTO_DETECT TRUE);
COPY products  FROM 'csv/products.csv'  (AUTO_DETECT TRUE);
COPY stores    FROM 'csv/stores.csv'    (AUTO_DETECT TRUE);
COPY dates     FROM 'csv/dates.csv'     (AUTO_DETECT TRUE);
COPY sales     FROM 'csv/sales.csv'     (AUTO_DETECT TRUE);

-- -------------------------------------------------------------
-- BUILD STATISTICS
-- -------------------------------------------------------------

ANALYZE;

-- -------------------------------------------------------------
-- VALIDATION
-- -------------------------------------------------------------

SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'stores', COUNT(*) FROM stores
UNION ALL
SELECT 'dates', COUNT(*) FROM dates
UNION ALL
SELECT 'sales', COUNT(*) FROM sales;

-- Example sanity query
SELECT p.category, SUM(s.total_amount) AS total_sales_amount
FROM sales s
JOIN dates d    ON s.date_key = d.date_key
JOIN products p ON s.product_key = p.product_key
WHERE d.year = 2024 AND d.month_of_year = 1
GROUP BY p.category
ORDER BY total_sales_amount DESC;

-- =============================================================
-- END OF SCRIPT
-- =============================================================
