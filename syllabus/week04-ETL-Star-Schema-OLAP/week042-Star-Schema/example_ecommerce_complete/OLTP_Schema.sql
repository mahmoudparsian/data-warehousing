-- ============================================================
-- Star Schema (E‑Commerce) — OLTP + DW + ETL (MySQL 8.x)
-- Expanded: customer country, stores, channel (ONLINE vs IN_STORE), Customer SCD Type 2
-- This script is designed to be run top-to-bottom.
-- ============================================================

-- =========================
-- A) OLTP SCHEMA + SEED DATA
-- =========================
DROP DATABASE IF EXISTS ecommerce_oltp;
CREATE DATABASE ecommerce_oltp;
USE ecommerce_oltp;

CREATE TABLE customers (
  customer_id INT PRIMARY KEY,
  first_name VARCHAR(100) NOT NULL,
  last_name  VARCHAR(100) NOT NULL,
  email      VARCHAR(200) NOT NULL,
  city       VARCHAR(100) NOT NULL,
  state      VARCHAR(100) NOT NULL,
  country    VARCHAR(100) NOT NULL,
  created_at DATETIME NOT NULL,
  UNIQUE KEY uk_customers_email (email)
);

CREATE TABLE stores (
  store_id INT PRIMARY KEY,
  store_name VARCHAR(200) NOT NULL,
  city    VARCHAR(100) NOT NULL,
  state   VARCHAR(100) NOT NULL,
  country VARCHAR(100) NOT NULL,
  opened_date DATE NOT NULL
);

CREATE TABLE products (
  product_id INT PRIMARY KEY,
  product_name VARCHAR(200) NOT NULL,
  category VARCHAR(100) NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  supplier VARCHAR(150) NOT NULL
);

CREATE TABLE orders (
  order_id BIGINT PRIMARY KEY,
  customer_id INT NOT NULL,
  store_id INT NULL, -- NULL means online order
  order_date DATETIME NOT NULL,
  channel ENUM('ONLINE','IN_STORE') NOT NULL,
  status VARCHAR(50) NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  FOREIGN KEY (store_id) REFERENCES stores(store_id)
);


CREATE TABLE order_items (
    order_item_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_id      BIGINT NOT NULL,
    product_id    INT NOT NULL,
    quantity      INT NOT NULL,
    unit_price    DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    INDEX(order_id),
    INDEX(product_id)
);

