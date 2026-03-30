
-- ============================================================
-- ETL: OLTP (oltp_demo) -> DW (dw_demo) Star Schema (MySQL)
-- Run while connected to dw_demo
-- ============================================================

USE dw_demo;
SET sql_safe_updates = 0;

-- 1) dim_date for last 400 days
WITH RECURSIVE seq(n) AS (
  SELECT 0
  UNION ALL SELECT n+1 FROM seq WHERE n < 400
),
dates AS (
  SELECT DATE_SUB(CURDATE(), INTERVAL n DAY) AS d
  FROM seq
)
INSERT IGNORE INTO dim_date (date_key, full_date, year, quarter, month, month_name, day, weekday_name)
SELECT
  DATE_FORMAT(d, '%Y%m%d') + 0 AS date_key,
  d AS full_date,
  YEAR(d) AS year,
  QUARTER(d) AS quarter,
  MONTH(d) AS month,
  DATE_FORMAT(d, '%M') AS month_name,
  DAY(d) AS day,
  DATE_FORMAT(d, '%W') AS weekday_name
FROM dates;

-- 2) Type 1 dims
INSERT INTO dim_store (store_id, store_name, region)
SELECT s.store_id, s.store_name, s.region
FROM oltp_demo.stores s
ON DUPLICATE KEY UPDATE
  store_name = VALUES(store_name),
  region = VALUES(region);

INSERT INTO dim_product (product_id, product_name, category, brand)
SELECT p.product_id, p.product_name, p.category, p.brand
FROM oltp_demo.products p
ON DUPLICATE KEY UPDATE
  product_name = VALUES(product_name),
  category = VALUES(category),
  brand = VALUES(brand);

-- 3) dim_customer initial SCD2 load (insert only missing current rows)
INSERT INTO dim_customer (
  customer_id, first_name, last_name, email, country,
  effective_date, expiry_date, is_current
)
SELECT
  c.customer_id, c.first_name, c.last_name, c.email, c.country,
  CURDATE(), '9999-12-31', TRUE
FROM oltp_demo.customers c
LEFT JOIN dim_customer dc
  ON dc.customer_id = c.customer_id AND dc.is_current = TRUE
WHERE dc.customer_id IS NULL;

-- 4) fact load (maps to current customer version)
INSERT INTO fact_sales (
  date_key, customer_key, product_key, store_key,
  order_id, order_item_id,
  quantity, unit_price, sales_amount
)
SELECT
  DATE_FORMAT(o.order_date, '%Y%m%d') + 0 AS date_key,
  dc.customer_key,
  dp.product_key,
  ds.store_key,
  o.order_id,
  oi.order_item_id,
  oi.quantity,
  oi.unit_price,
  (oi.quantity * oi.unit_price) AS sales_amount
FROM oltp_demo.orders o
JOIN oltp_demo.order_items oi ON oi.order_id = o.order_id
JOIN dim_customer dc ON dc.customer_id = o.customer_id AND dc.is_current = TRUE
JOIN dim_product dp ON dp.product_id = oi.product_id
JOIN dim_store ds ON ds.store_id = o.store_id;
