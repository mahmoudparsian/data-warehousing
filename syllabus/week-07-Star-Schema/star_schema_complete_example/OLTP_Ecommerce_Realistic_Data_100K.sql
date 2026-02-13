-- ============================================================
-- Realistic OLTP Data Generator (MySQL 8.x)
-- Targets:
--   customers:    1,000
--   stores:          50
--   products:     2,000
--   orders:     100,000
--   order_items: 300,000
-- ============================================================

USE ecommerce_oltp;

-- Optional but recommended for reloads
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE order_items;
TRUNCATE TABLE orders;
TRUNCATE TABLE products;
TRUNCATE TABLE stores;
TRUNCATE TABLE customers;
SET FOREIGN_KEY_CHECKS = 1;

-- ------------------------------------------------------------
-- Helper inline digits (0..9) used via CROSS JOIN
-- We'll generate n = 1..N using base-10 expansion
-- ------------------------------------------------------------

-- ============================================================
-- 1) CUSTOMERS (1,000)
-- ============================================================
INSERT INTO customers
(customer_id, first_name, last_name, email, city, state, country, created_at)
SELECT
  n,
  CONCAT('First', n),
  CONCAT('Last', n),
  CONCAT('customer', n, '@example.com'),
  ELT(1 + (n % 10),
      'San Jose','Austin','New York','Seattle','Chicago',
      'Boston','Denver','Atlanta','Miami','Dallas'),
  ELT(1 + (n % 8),'CA','TX','NY','WA','IL','MA','CO','GA'),
  'USA',
  TIMESTAMP('2021-01-01') + INTERVAL (n % 900) DAY
FROM (
  SELECT
    (d0.i + d1.i*10 + d2.i*100) + 1 AS n
  FROM
    (SELECT 0 i UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) d0
  CROSS JOIN
    (SELECT 0 i UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) d1
  CROSS JOIN
    (SELECT 0 i UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) d2
) seq
WHERE n <= 1000;

-- ============================================================
-- 2) STORES (50)
-- ============================================================
INSERT INTO stores
(store_id, store_name, city, state, country, opened_date)
SELECT
  n,
  CONCAT('Store_', n),
  ELT(1 + (n % 10),
      'San Jose','Austin','New York','Seattle','Chicago',
      'Boston','Denver','Atlanta','Miami','Dallas'),
  ELT(1 + (n % 8),'CA','TX','NY','WA','IL','MA','CO','GA'),
  'USA',
  DATE('2018-01-01') + INTERVAL (n % 1500) DAY
FROM (
  SELECT (d0.i + d1.i*10) + 1 AS n
  FROM
    (SELECT 0 i UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) d0
  CROSS JOIN
    (SELECT 0 i UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) d1
) seq
WHERE n <= 50;

-- ============================================================
-- 3) PRODUCTS (2,000)
-- ============================================================
INSERT INTO products
(product_id, product_name, category, price, supplier)
SELECT
  n,
  CONCAT('Product_', n),
  ELT(1 + (n % 8),
      'Electronics','Furniture','Office','Kitchen',
      'Sports','Clothing','Toys','Accessories'),
  ROUND(10 + (n % 1000) * 0.75, 2),
  ELT(1 + (n % 6),
      'SupplierA','SupplierB','SupplierC',
      'SupplierD','SupplierE','SupplierF')
FROM (
  SELECT
    (d0.i + d1.i*10 + d2.i*100 + d3.i*1000) + 1 AS n
  FROM
    (SELECT 0 i UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) d0
  CROSS JOIN
    (SELECT 0 i UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) d1
  CROSS JOIN
    (SELECT 0 i UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) d2
  CROSS JOIN
    (SELECT 0 i UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) d3
) seq
WHERE n <= 2000;

-- ============================================================
-- 4) ORDERS (100,000)
-- ============================================================
INSERT INTO orders
(order_id, customer_id, store_id, order_date, channel, status)
SELECT
  1000000 + n,
  1 + (n % 1000),
  CASE WHEN (n % 3)=0 THEN NULL ELSE 1 + (n % 50) END,
  TIMESTAMP('2022-01-01') + INTERVAL (n % 1400) DAY,
  CASE WHEN (n % 3)=0 THEN 'ONLINE' ELSE 'IN_STORE' END,
  ELT(1 + (n % 4),'Placed','Shipped','Delivered','Cancelled')
FROM (
  SELECT
    (d0.i + d1.i*10 + d2.i*100 + d3.i*1000 + d4.i*10000) + 1 AS n
  FROM
    (SELECT 0 i UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) d0
  CROSS JOIN
    (SELECT 0 i UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) d1
  CROSS JOIN
    (SELECT 0 i UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) d2
  CROSS JOIN
    (SELECT 0 i UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) d3
  CROSS JOIN
    (SELECT 0 i UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) d4
) seq
WHERE n <= 100000;

-- ============================================================
-- 5) ORDER_ITEMS (300,000)
-- ============================================================
INSERT INTO order_items
(order_id, product_id, quantity, unit_price)
SELECT
    o.order_id,
    1 + FLOOR(RAND(o.order_id * s.i) * 2000),
    1 + FLOOR(RAND(o.order_id * s.i * 7) * 5),
    ROUND(10 + FLOOR(RAND(o.order_id * s.i * 13) * 1000) * 0.75, 2)
FROM orders o
JOIN (
    SELECT 1 i UNION ALL SELECT 2 UNION ALL SELECT 3
) s;
-- ============================================================
-- Sanity checks
-- ============================================================
SELECT COUNT(*) AS customers_cnt   FROM customers;
SELECT COUNT(*) AS stores_cnt      FROM stores;
SELECT COUNT(*) AS products_cnt    FROM products;
SELECT COUNT(*) AS orders_cnt      FROM orders;
SELECT COUNT(*) AS order_items_cnt FROM order_items;