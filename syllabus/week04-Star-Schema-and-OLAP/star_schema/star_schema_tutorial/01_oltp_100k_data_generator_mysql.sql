
-- ============================================================
-- Star Schema Tutorial: 100K+ Realistic OLTP Data Generator (MySQL 8+)
-- Creates: customers (1,000), products (2,000), stores (50),
--          orders (100,000), order_items (300,000)
-- Notes:
-- 1) Uses a numbers table generated via CROSS JOIN (no recursion limits).
-- 2) Uses a deterministic pseudo-random pattern based on CRC32 for repeatability.
-- 3) Run in a dedicated schema/database for best results.
-- ============================================================

-- Optional: create & use a sandbox database
CREATE DATABASE IF NOT EXISTS oltp_demo;
USE oltp_demo;

SET sql_safe_updates = 0;

-- ------------------------------------------------------------
-- DROP (optional)
-- ------------------------------------------------------------
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS stores;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS numbers_300k;

-- ------------------------------------------------------------
-- OLTP TABLES
-- ------------------------------------------------------------
CREATE TABLE customers (
  customer_id INT PRIMARY KEY AUTO_INCREMENT,
  first_name VARCHAR(50) NOT NULL,
  last_name  VARCHAR(50) NOT NULL,
  email      VARCHAR(120) NOT NULL,
  country    VARCHAR(50) NOT NULL,
  created_at DATETIME NOT NULL
);

CREATE TABLE products (
  product_id INT PRIMARY KEY AUTO_INCREMENT,
  product_name VARCHAR(120) NOT NULL,
  category     VARCHAR(60) NOT NULL,
  brand        VARCHAR(60) NOT NULL,
  price        DECIMAL(10,2) NOT NULL
);

CREATE TABLE stores (
  store_id INT PRIMARY KEY AUTO_INCREMENT,
  store_name VARCHAR(120) NOT NULL,
  region     VARCHAR(60) NOT NULL
);

CREATE TABLE orders (
  order_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  customer_id INT NOT NULL,
  store_id INT NOT NULL,
  order_date DATE NOT NULL,
  KEY idx_orders_customer (customer_id),
  KEY idx_orders_date (order_date)
);

CREATE TABLE order_items (
  order_item_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  order_id BIGINT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL,
  unit_price DECIMAL(10,2) NOT NULL,
  KEY idx_items_order (order_id),
  KEY idx_items_product (product_id)
);

-- ------------------------------------------------------------
-- NUMBERS TABLE (1..300,000)
-- ------------------------------------------------------------
CREATE TABLE numbers_300k (n INT PRIMARY KEY);

INSERT INTO numbers_300k (n)
SELECT x.n
FROM (
  SELECT (a.d + 10*b.d + 100*c.d + 1000*d.d + 10000*e.d + 100000*f.d) + 1 AS n
  FROM
    (SELECT 0 d UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) a
  CROSS JOIN
    (SELECT 0 d UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) b
  CROSS JOIN
    (SELECT 0 d UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) c
  CROSS JOIN
    (SELECT 0 d UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) d
  CROSS JOIN
    (SELECT 0 d UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) e
  CROSS JOIN
    (SELECT 0 d UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) f
) x
WHERE x.n <= 300000
ORDER BY x.n;

-- ------------------------------------------------------------
-- POPULATE STORES (50)
-- ------------------------------------------------------------
INSERT INTO stores (store_name, region)
SELECT
  CONCAT('Store ', LPAD(n, 3, '0')),
  CASE MOD(n, 5)
    WHEN 0 THEN 'North'
    WHEN 1 THEN 'South'
    WHEN 2 THEN 'East'
    WHEN 3 THEN 'West'
    ELSE 'Central'
  END
FROM numbers_300k
WHERE n <= 50;

-- ------------------------------------------------------------
-- POPULATE CUSTOMERS (1,000)
-- ------------------------------------------------------------
INSERT INTO customers (first_name, last_name, email, country, created_at)
SELECT
  CASE MOD(n, 12)
    WHEN 0 THEN 'Alex' WHEN 1 THEN 'Sam' WHEN 2 THEN 'Taylor' WHEN 3 THEN 'Jordan'
    WHEN 4 THEN 'Casey' WHEN 5 THEN 'Riley' WHEN 6 THEN 'Morgan' WHEN 7 THEN 'Jamie'
    WHEN 8 THEN 'Cameron' WHEN 9 THEN 'Avery' WHEN 10 THEN 'Quinn' ELSE 'Drew'
  END AS first_name,
  CASE MOD(n, 12)
    WHEN 0 THEN 'Smith' WHEN 1 THEN 'Johnson' WHEN 2 THEN 'Brown' WHEN 3 THEN 'Garcia'
    WHEN 4 THEN 'Miller' WHEN 5 THEN 'Davis' WHEN 6 THEN 'Rodriguez' WHEN 7 THEN 'Martinez'
    WHEN 8 THEN 'Hernandez' WHEN 9 THEN 'Lopez' WHEN 10 THEN 'Gonzalez' ELSE 'Wilson'
  END AS last_name,
  CONCAT('customer', n, '@example.com') AS email,
  CASE MOD(n, 10)
    WHEN 0 THEN 'United States'
    WHEN 1 THEN 'Canada'
    WHEN 2 THEN 'United Kingdom'
    WHEN 3 THEN 'Germany'
    WHEN 4 THEN 'France'
    WHEN 5 THEN 'India'
    WHEN 6 THEN 'Brazil'
    WHEN 7 THEN 'Australia'
    WHEN 8 THEN 'Japan'
    ELSE 'Mexico'
  END AS country,
  DATE_SUB(NOW(), INTERVAL MOD(n, 365) DAY) AS created_at
FROM numbers_300k
WHERE n <= 1000;

-- ------------------------------------------------------------
-- POPULATE PRODUCTS (2,000)
-- ------------------------------------------------------------
INSERT INTO products (product_name, category, brand, price)
SELECT
  CONCAT(
    CASE MOD(n, 8)
      WHEN 0 THEN 'Wireless '
      WHEN 1 THEN 'Smart '
      WHEN 2 THEN 'Eco '
      WHEN 3 THEN 'Premium '
      WHEN 4 THEN 'Compact '
      WHEN 5 THEN 'Ultra '
      WHEN 6 THEN 'Pro '
      ELSE 'Basic '
    END,
    CASE MOD(n, 10)
      WHEN 0 THEN 'Headphones'
      WHEN 1 THEN 'Speaker'
      WHEN 2 THEN 'Laptop'
      WHEN 3 THEN 'Mouse'
      WHEN 4 THEN 'Keyboard'
      WHEN 5 THEN 'Monitor'
      WHEN 6 THEN 'Backpack'
      WHEN 7 THEN 'Bottle'
      WHEN 8 THEN 'Lamp'
      ELSE 'Camera'
    END,
    ' #', n
  ) AS product_name,
  CASE MOD(n, 6)
    WHEN 0 THEN 'Electronics'
    WHEN 1 THEN 'Accessories'
    WHEN 2 THEN 'Home'
    WHEN 3 THEN 'Outdoors'
    WHEN 4 THEN 'Office'
    ELSE 'Lifestyle'
  END AS category,
  CASE MOD(n, 7)
    WHEN 0 THEN 'Acme'
    WHEN 1 THEN 'Nova'
    WHEN 2 THEN 'Zenith'
    WHEN 3 THEN 'Orbit'
    WHEN 4 THEN 'Pulse'
    WHEN 5 THEN 'Vertex'
    ELSE 'Nimbus'
  END AS brand,
  ROUND(5 + (CRC32(CONCAT('price', n)) % 50000) / 100, 2) AS price
FROM numbers_300k
WHERE n <= 2000;

-- ------------------------------------------------------------
-- POPULATE ORDERS (100,000)
-- ------------------------------------------------------------
INSERT INTO orders (customer_id, store_id, order_date)
SELECT
  1 + (CRC32(CONCAT('cust', n)) % 1000) AS customer_id,
  1 + (CRC32(CONCAT('store', n)) % 50) AS store_id,
  DATE_SUB(CURDATE(), INTERVAL (CRC32(CONCAT('date', n)) % 365) DAY) AS order_date
FROM numbers_300k
WHERE n <= 100000;

-- ------------------------------------------------------------
-- POPULATE ORDER ITEMS (300,000)
-- 3 line items per order (100k orders)
-- ------------------------------------------------------------
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
SELECT
  1 + FLOOR((n - 1)/3) AS order_id,
  1 + (CRC32(CONCAT('prod', n)) % 2000) AS product_id,
  1 + (CRC32(CONCAT('qty', n)) % 5) AS quantity,
  ROUND(
    (SELECT p.price FROM products p WHERE p.product_id = (1 + (CRC32(CONCAT('prod', n)) % 2000)))
    * (0.90 + (CRC32(CONCAT('disc', n)) % 21) / 100.0),
    2
  ) AS unit_price
FROM numbers_300k
WHERE n <= 300000;

-- ------------------------------------------------------------
-- QUICK SANITY CHECKS
-- ------------------------------------------------------------
SELECT 'customers' AS table_name, COUNT(*) AS rows_cnt FROM customers
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'stores', COUNT(*) FROM stores
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'order_items', COUNT(*) FROM order_items;

-- Done.
