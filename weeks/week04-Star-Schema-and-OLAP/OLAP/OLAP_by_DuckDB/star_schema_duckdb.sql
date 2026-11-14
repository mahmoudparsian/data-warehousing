-- DuckDB Online Sales Star Schema (Teaching)
-- Run in DuckDB CLI: duckdb online_sales.duckdb < star_schema_duckdb.sql

DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS dates;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS stores;

-- Dimension: Dates
CREATE TABLE dates (
    date_key INTEGER PRIMARY KEY, -- YYYYMMDD
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
DROP SEQUENCE IF EXISTS customer_key_seq;
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
DROP SEQUENCE IF EXISTS product_key_seq;
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
DROP SEQUENCE IF EXISTS store_key_seq;
CREATE SEQUENCE store_key_seq START 1;

CREATE TABLE stores (
    store_key INTEGER PRIMARY KEY DEFAULT nextval('store_key_seq'),
    store_id VARCHAR(50) UNIQUE,
    store_name VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100)
);

-- Fact: Sales
DROP SEQUENCE IF EXISTS sales_key_seq;
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

-- Note: DuckDB is columnar; indexes are usually unnecessary for OLAP workloads.
