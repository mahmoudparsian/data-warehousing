
-- ============================================================
-- Data Warehouse Star Schema (MySQL) + Indexes
-- ============================================================

CREATE DATABASE IF NOT EXISTS dw_demo;
USE dw_demo;

SET sql_safe_updates = 0;

DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_store;
DROP TABLE IF EXISTS dim_date;

-- DIMENSIONS
CREATE TABLE dim_date (
  date_key INT PRIMARY KEY,
  full_date DATE NOT NULL,
  year SMALLINT NOT NULL,
  quarter TINYINT NOT NULL,
  month TINYINT NOT NULL,
  month_name VARCHAR(12) NOT NULL,
  day TINYINT NOT NULL,
  weekday_name VARCHAR(12) NOT NULL
);

CREATE TABLE dim_store (
  store_key INT PRIMARY KEY AUTO_INCREMENT,
  store_id INT NOT NULL,
  store_name VARCHAR(120) NOT NULL,
  region VARCHAR(60) NOT NULL,
  UNIQUE KEY uk_dim_store_store_id (store_id)
);

CREATE TABLE dim_product (
  product_key INT PRIMARY KEY AUTO_INCREMENT,
  product_id INT NOT NULL,
  product_name VARCHAR(120) NOT NULL,
  category VARCHAR(60) NOT NULL,
  brand VARCHAR(60) NOT NULL,
  UNIQUE KEY uk_dim_product_product_id (product_id)
);

-- SCD Type 2 dimension for customer
CREATE TABLE dim_customer (
  customer_key INT PRIMARY KEY AUTO_INCREMENT,
  customer_id INT NOT NULL,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(120) NOT NULL,
  country VARCHAR(50) NOT NULL,
  effective_date DATE NOT NULL,
  expiry_date DATE NOT NULL,
  is_current BOOLEAN NOT NULL,
  KEY idx_dim_customer_nk_current (customer_id, is_current),
  KEY idx_dim_customer_effective (effective_date),
  KEY idx_dim_customer_expiry (expiry_date)
);

-- FACT (grain = order_item)
CREATE TABLE fact_sales (
  sales_key BIGINT PRIMARY KEY AUTO_INCREMENT,
  date_key INT NOT NULL,
  customer_key INT NOT NULL,
  product_key INT NOT NULL,
  store_key INT NOT NULL,
  order_id BIGINT NOT NULL,
  order_item_id BIGINT NOT NULL,
  quantity INT NOT NULL,
  unit_price DECIMAL(10,2) NOT NULL,
  sales_amount DECIMAL(12,2) NOT NULL,

  KEY idx_fact_date (date_key),
  KEY idx_fact_customer (customer_key),
  KEY idx_fact_product (product_key),
  KEY idx_fact_store (store_key),
  KEY idx_fact_order (order_id),
  KEY idx_fact_order_item (order_item_id)
);
