-- =========================
-- B) DATA WAREHOUSE SCHEMA
-- =========================
DROP DATABASE IF EXISTS ecommerce_dw;
CREATE DATABASE ecommerce_dw;
USE ecommerce_dw;

-- ---- Staging (daily extracts) ----
CREATE TABLE stg_customers (
  extract_date DATE NOT NULL,
  customer_id INT NOT NULL,
  first_name VARCHAR(100) NOT NULL,
  last_name  VARCHAR(100) NOT NULL,
  email VARCHAR(200) NOT NULL,
  city VARCHAR(100) NOT NULL,
  state VARCHAR(100) NOT NULL,
  country VARCHAR(100) NOT NULL,
  PRIMARY KEY (extract_date, customer_id)
);

CREATE TABLE stg_products (
  extract_date DATE NOT NULL,
  product_id INT NOT NULL,
  product_name VARCHAR(200) NOT NULL,
  category VARCHAR(100) NOT NULL,
  supplier VARCHAR(150) NOT NULL,
  PRIMARY KEY (extract_date, product_id)
);

CREATE TABLE stg_stores (
  extract_date DATE NOT NULL,
  store_id INT NOT NULL,
  store_name VARCHAR(200) NOT NULL,
  city VARCHAR(100) NOT NULL,
  state VARCHAR(100) NOT NULL,
  country VARCHAR(100) NOT NULL,
  opened_date DATE NOT NULL,
  PRIMARY KEY (extract_date, store_id)
);

CREATE TABLE stg_orders (
  extract_date DATE NOT NULL,
  order_id BIGINT NOT NULL,
  customer_id INT NOT NULL,
  store_id INT NULL,
  order_date DATETIME NOT NULL,
  channel VARCHAR(20) NOT NULL,
  status VARCHAR(50) NOT NULL,
  PRIMARY KEY (extract_date, order_id)
);

CREATE TABLE stg_order_items (
  extract_date DATE NOT NULL,
  order_id BIGINT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL,
  unit_price DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (extract_date, order_id, product_id)
);

-- ---- Dimensions (surrogate keys) ----
CREATE TABLE dim_channel (
  channel_sk INT AUTO_INCREMENT PRIMARY KEY,
  channel_name VARCHAR(20) NOT NULL,
  UNIQUE KEY uk_channel_name (channel_name)
);

CREATE TABLE dim_product (
  product_sk BIGINT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL,
  product_name VARCHAR(200) NOT NULL,
  category VARCHAR(100) NOT NULL,
  supplier VARCHAR(150) NOT NULL,
  UNIQUE KEY uk_product_nk (product_id)
);

CREATE TABLE dim_store (
  store_sk BIGINT AUTO_INCREMENT PRIMARY KEY,
  store_id INT NOT NULL,
  store_name VARCHAR(200) NOT NULL,
  city VARCHAR(100) NOT NULL,
  state VARCHAR(100) NOT NULL,
  country VARCHAR(100) NOT NULL,
  opened_date DATE NOT NULL,
  UNIQUE KEY uk_store_nk (store_id)
);

-- Customer as SCD Type 2
CREATE TABLE dim_customer_scd2 (
  customer_sk BIGINT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL, -- natural key
  full_name VARCHAR(220) NOT NULL,
  email VARCHAR(200) NOT NULL,
  city VARCHAR(100) NOT NULL,
  state VARCHAR(100) NOT NULL,
  country VARCHAR(100) NOT NULL,
  effective_start DATE NOT NULL,
  effective_end DATE NULL,
  is_current CHAR(1) NOT NULL DEFAULT 'Y',
  UNIQUE KEY uk_customer_current (customer_id, is_current),
  INDEX ix_customer_nk (customer_id),
  INDEX ix_customer_dates (effective_start, effective_end)
);

-- Date dimension
CREATE TABLE dim_date (
  date_id INT PRIMARY KEY,      -- yyyymmdd
  full_date DATE NOT NULL,
  year INT NOT NULL,
  month INT NOT NULL,
  day INT NOT NULL,
  quarter INT NOT NULL
);

-- ---- Fact ----
CREATE TABLE fact_sales (
  sales_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  order_id BIGINT NOT NULL,
  customer_sk BIGINT NOT NULL,
  product_sk BIGINT NOT NULL,
  store_sk BIGINT NULL,    -- NULL for online
  channel_sk INT NOT NULL,
  date_id INT NOT NULL,
  quantity INT NOT NULL,
  sales_amount DECIMAL(12,2) NOT NULL,
  UNIQUE KEY uk_fact_order_line (order_id, product_sk),
  INDEX ix_fact_date (date_id),
  INDEX ix_fact_customer (customer_sk),
  INDEX ix_fact_product (product_sk),
  INDEX ix_fact_store (store_sk),
  CONSTRAINT fk_fact_customer FOREIGN KEY (customer_sk) REFERENCES dim_customer_scd2(customer_sk),
  CONSTRAINT fk_fact_product  FOREIGN KEY (product_sk)  REFERENCES dim_product(product_sk),
  CONSTRAINT fk_fact_store    FOREIGN KEY (store_sk)    REFERENCES dim_store(store_sk),
  CONSTRAINT fk_fact_channel  FOREIGN KEY (channel_sk)  REFERENCES dim_channel(channel_sk),
  CONSTRAINT fk_fact_date     FOREIGN KEY (date_id)     REFERENCES dim_date(date_id)
);

-- =========================
-- C) dim_date auto-population
-- =========================
-- MySQL's default recursion limit is 1000; we raise it for a multi-year date range.
SET SESSION cte_max_recursion_depth = 10000;

-- ----------------------------------------------
-- Populate dim_date for 2022-01-01 .. 2026-12-31
-- ----------------------------------------------
WITH RECURSIVE d AS (
  SELECT DATE('2022-01-01') AS dt
  UNION ALL
  SELECT dt + INTERVAL 1 DAY FROM d WHERE dt < '2026-12-31'
)
INSERT INTO dim_date (date_id, full_date, year, month, day, quarter)
SELECT
  CAST(DATE_FORMAT(dt, '%Y%m%d') AS UNSIGNED) AS date_id,
  dt AS full_date,
  YEAR(dt) AS year,
  MONTH(dt) AS month,
  DAY(dt) AS day,
  QUARTER(dt) AS quarter
FROM d;

-- =========================
-- D) Seed dim_channel (static)
-- =========================
INSERT INTO dim_channel (channel_name) VALUES ('ONLINE'), ('IN_STORE')
ON DUPLICATE KEY UPDATE channel_name=VALUES(channel_name);

-- ============================================================
-- E) ETL RUN #1 (initial load) — snapshot date 2023-03-25
-- ============================================================
SET @extract_date = '2023-03-25';

-- 1) Extract OLTP → staging (snapshot)
INSERT INTO stg_customers
(extract_date, customer_id, first_name, last_name, email, city, state, country)
SELECT @extract_date, c.customer_id, c.first_name, c.last_name, c.email, c.city, c.state, c.country
FROM ecommerce_oltp.customers c
ON DUPLICATE KEY UPDATE
  first_name=VALUES(first_name), last_name=VALUES(last_name), email=VALUES(email),
  city=VALUES(city), state=VALUES(state), country=VALUES(country);

INSERT INTO stg_products
(extract_date, product_id, product_name, category, supplier)
SELECT @extract_date, p.product_id, p.product_name, p.category, p.supplier
FROM ecommerce_oltp.products p
ON DUPLICATE KEY UPDATE
  product_name=VALUES(product_name), category=VALUES(category), supplier=VALUES(supplier);

INSERT INTO stg_stores
(extract_date, store_id, store_name, city, state, country, opened_date)
SELECT @extract_date, s.store_id, s.store_name, s.city, s.state, s.country, s.opened_date
FROM ecommerce_oltp.stores s
ON DUPLICATE KEY UPDATE
  store_name=VALUES(store_name), city=VALUES(city), state=VALUES(state),
  country=VALUES(country), opened_date=VALUES(opened_date);

INSERT INTO stg_orders
(extract_date, order_id, customer_id, store_id, order_date, channel, status)
SELECT @extract_date, o.order_id, o.customer_id, o.store_id, o.order_date, o.channel, o.status
FROM ecommerce_oltp.orders o
ON DUPLICATE KEY UPDATE
  customer_id=VALUES(customer_id), store_id=VALUES(store_id),
  order_date=VALUES(order_date), channel=VALUES(channel), status=VALUES(status);

INSERT INTO stg_order_items
(extract_date, order_id, product_id, quantity, unit_price)
SELECT @extract_date, i.order_id, i.product_id, i.quantity, i.unit_price
FROM ecommerce_oltp.order_items i
ON DUPLICATE KEY UPDATE
  quantity=VALUES(quantity), unit_price=VALUES(unit_price);

-- 2) Load Type 1 dims (product, store)
INSERT INTO dim_product (product_id, product_name, category, supplier)
SELECT s.product_id, s.product_name, s.category, s.supplier
FROM stg_products s
WHERE s.extract_date=@extract_date
ON DUPLICATE KEY UPDATE
  product_name=VALUES(product_name),
  category=VALUES(category),
  supplier=VALUES(supplier);

INSERT INTO dim_store (store_id, store_name, city, state, country, opened_date)
SELECT s.store_id, s.store_name, s.city, s.state, s.country, s.opened_date
FROM stg_stores s
WHERE s.extract_date=@extract_date
ON DUPLICATE KEY UPDATE
  store_name=VALUES(store_name),
  city=VALUES(city),
  state=VALUES(state),
  country=VALUES(country),
  opened_date=VALUES(opened_date);

-- 3) Customer SCD2 — initial insert (effective_start backfilled to cover older facts)
INSERT INTO dim_customer_scd2
(customer_id, full_name, email, city, state, country, effective_start, effective_end, is_current)
SELECT
  s.customer_id,
  CONCAT(s.first_name, ' ', s.last_name) AS full_name,
  s.email, s.city, s.state, s.country,
  '1900-01-01' AS effective_start,
  NULL AS effective_end,
  'Y' AS is_current
FROM stg_customers s
LEFT JOIN dim_customer_scd2 d
  ON d.customer_id = s.customer_id
WHERE s.extract_date=@extract_date
  AND d.customer_id IS NULL;

-- 4) Fact load (order-line grain) for this extract run
INSERT IGNORE INTO fact_sales
(order_id, customer_sk, product_sk, store_sk, channel_sk, date_id, quantity, sales_amount)
SELECT
  o.order_id,
  c.customer_sk,
  p.product_sk,
  st.store_sk,
  ch.channel_sk,
  d.date_id,
  i.quantity,
  ROUND(i.quantity * i.unit_price, 2) AS sales_amount
FROM stg_orders o
JOIN stg_order_items i
  ON i.extract_date=o.extract_date AND i.order_id=o.order_id
JOIN dim_product p
  ON p.product_id = i.product_id
LEFT JOIN dim_store st
  ON st.store_id = o.store_id
JOIN dim_channel ch
  ON ch.channel_name = o.channel
JOIN dim_date d
  ON d.full_date = DATE(o.order_date)
JOIN dim_customer_scd2 c
  ON c.customer_id = o.customer_id
 AND DATE(o.order_date) >= c.effective_start
 AND (c.effective_end IS NULL OR DATE(o.order_date) <= c.effective_end)
WHERE o.extract_date=@extract_date;

-- ============================================================
-- F) Simulate a real-world change in OLTP (customer move + new order)
-- ============================================================
-- Alice moves: San Jose -> San Francisco (same country)
UPDATE ecommerce_oltp.customers
SET city='San Francisco', state='CA', country='USA'
WHERE customer_id=1;

-- New order after the move (online)
INSERT INTO ecommerce_oltp.orders VALUES
(20001,1,NULL,'2024-06-10 10:30:00','ONLINE','Shipped');

INSERT INTO ecommerce_oltp.order_items VALUES
(20001,103,1,90),
(20001,101,1,25);

-- ============================================================
-- G) ETL RUN #2 (incremental) — snapshot date 2024-06-15
-- ============================================================
SET @extract_date = '2024-06-15';

-- 1) Extract OLTP → staging (snapshot)
INSERT INTO stg_customers
(extract_date, customer_id, first_name, last_name, email, city, state, country)
SELECT @extract_date, c.customer_id, c.first_name, c.last_name, c.email, c.city, c.state, c.country
FROM ecommerce_oltp.customers c
ON DUPLICATE KEY UPDATE
  first_name=VALUES(first_name), last_name=VALUES(last_name), email=VALUES(email),
  city=VALUES(city), state=VALUES(state), country=VALUES(country);

INSERT INTO stg_orders
(extract_date, order_id, customer_id, store_id, order_date, channel, status)
SELECT @extract_date, o.order_id, o.customer_id, o.store_id, o.order_date, o.channel, o.status
FROM ecommerce_oltp.orders o
ON DUPLICATE KEY UPDATE
  customer_id=VALUES(customer_id), store_id=VALUES(store_id),
  order_date=VALUES(order_date), channel=VALUES(channel), status=VALUES(status);

INSERT INTO stg_order_items
(extract_date, order_id, product_id, quantity, unit_price)
SELECT @extract_date, i.order_id, i.product_id, i.quantity, i.unit_price
FROM ecommerce_oltp.order_items i
ON DUPLICATE KEY UPDATE
  quantity=VALUES(quantity), unit_price=VALUES(unit_price);

-- 2) Customer SCD2 change detection (expire + insert new current row)
DROP TEMPORARY TABLE IF EXISTS tmp_customer_changed;
CREATE TEMPORARY TABLE tmp_customer_changed AS
SELECT
  s.customer_id,
  CONCAT(s.first_name, ' ', s.last_name) AS full_name,
  s.email, s.city, s.state, s.country,
  d.customer_sk AS current_customer_sk
FROM stg_customers s
JOIN dim_customer_scd2 d
  ON d.customer_id = s.customer_id
 AND d.is_current='Y'
WHERE s.extract_date=@extract_date
  AND (
       d.full_name <> CONCAT(s.first_name, ' ', s.last_name)
    OR d.email     <> s.email
    OR d.city      <> s.city
    OR d.state     <> s.state
    OR d.country   <> s.country
  );

-- Expire old current row(s)
UPDATE dim_customer_scd2 d
JOIN tmp_customer_changed c
  ON c.current_customer_sk = d.customer_sk
SET
  d.effective_end = DATE_SUB(@extract_date, INTERVAL 1 DAY),
  d.is_current = 'N'
WHERE d.is_current='Y';

-- Insert new current row(s)
INSERT INTO dim_customer_scd2
(customer_id, full_name, email, city, state, country, effective_start, effective_end, is_current)
SELECT
  c.customer_id, c.full_name, c.email, c.city, c.state, c.country,
  @extract_date AS effective_start,
  NULL AS effective_end,
  'Y' AS is_current
FROM tmp_customer_changed c;

-- 3) Fact load for this extract run (INSERT IGNORE prevents duplicates)
INSERT IGNORE INTO fact_sales
(order_id, customer_sk, product_sk, store_sk, channel_sk, date_id, quantity, sales_amount)
SELECT
  o.order_id,
  c.customer_sk,
  p.product_sk,
  st.store_sk,
  ch.channel_sk,
  d.date_id,
  i.quantity,
  ROUND(i.quantity * i.unit_price, 2) AS sales_amount
FROM stg_orders o
JOIN stg_order_items i
  ON i.extract_date=o.extract_date AND i.order_id=o.order_id
JOIN dim_product p
  ON p.product_id = i.product_id
LEFT JOIN dim_store st
  ON st.store_id = o.store_id
JOIN dim_channel ch
  ON ch.channel_name = o.channel
JOIN dim_date d
  ON d.full_date = DATE(o.order_date)
JOIN dim_customer_scd2 c
  ON c.customer_id = o.customer_id
 AND DATE(o.order_date) >= c.effective_start
 AND (c.effective_end IS NULL OR DATE(o.order_date) <= c.effective_end)
WHERE o.extract_date=@extract_date;

-- ============================================================
-- H) Quick sanity checks (optional)
-- ============================================================
-- Customer history for Alice:
-- SELECT customer_id, city, effective_start, effective_end, is_current
-- FROM dim_customer_scd2 WHERE customer_id=1 ORDER BY effective_start;
--
-- Revenue by channel:
-- SELECT ch.channel_name, SUM(f.sales_amount) revenue
-- FROM fact_sales f JOIN dim_channel ch ON ch.channel_sk=f.channel_sk
-- GROUP BY ch.channel_name;
