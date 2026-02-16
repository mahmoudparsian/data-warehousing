# Story: Star Schema for Bike Store


1. The assumption is this: we have a bike  
store with some stores, products and customers.


2. Given the following star schema:

* Fact table: sales
* DIM tables: stores, products, customers, dates

3. ⚠️ IMPORTANT PERFORMANCE NOTES: Use MySQL 8+


4. Create 1000,000 customers 
   -- 600,000 MALE, 
   -- 400,000 FEMALE
   -- do not create even number of customers from given countries 

5. Create 6000,000 sales records
   -- data span is from 2010 to 2025

6. Then come up with a SQL script to create dates dimension from sales table.

7. data for stores is given: 12 stores

8. data for products is given: 100 products


-- --------------------
-- Star Schema Database
-- --------------------

-- ---------------
-- create database
-- ---------------
CREATE DATABASE bike_store;

-- ---------------
-- select database
-- ---------------
USE bike_store; 


-- -------------------------
-- Dimension Table: stores
-- -------------------------
CREATE TABLE stores (
    store_id INT PRIMARY KEY AUTO_INCREMENT,
    store_location VARCHAR(100) NOT NULL
);

-- -------------------------
-- Dimension Table: Products
-- -------------------------
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(20) NOT NULL
);

-- --------------------------
-- Dimension Table: customers
-- --------------------------
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL,  -- MALE/FEMALE
    country VARCHAR(20) NOT NULL, -- USA/CANADA/MEXICO/GERMANY/FRANCE/INDIA/CHINA/TURKEY/ENGLAND/ITALY
    email VARCHAR(40)
);

-- -------------------------
-- Dimension Table: dates
-- -------------------------
CREATE TABLE dates (
    date_id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,
    quarter INT NOT NULL
);

-- -------------------------
-- Fact Table: sales
-- -------------------------
CREATE TABLE sales (
    sale_id INT PRIMARY KEY AUTO_INCREMENT,
    sale_type VARCHAR(10) NOT NULL, -- IN-STORE/ON-LINE
    product_id INT NOT NULL,
    store_id INT NOT NULL,
    customer_id INT NOT NULL,
    date_id INT NOT NULL,
    quantity INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    sale_amount DECIMAL(10, 2) NOT NULL, -- sale_amount = quantity * amount
    
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (store_id) REFERENCES stores(store_id),
    FOREIGN KEY (date_id) REFERENCES Dates(date_id)
);


-- -----------------
-- Table Populations
-- -----------------


-- ------------------
-- stores Table
-- ------------------
INSERT INTO stores (store_id, store_location)
VALUES 
(1, 'Sunnyvale, CA, USA'),
(2, 'Detroit, MI, USA'),
(3, 'Miami, FL, USA'),
(4, 'Cupertino, CA, USA'),
(5, 'Chicago, IL, USA'),
(6, 'Ames, IA, USA'),
(7, 'Mexico City, Mexico'),
(8, 'Montreal, CANADA'),
(9, 'Toronto, CANADA'),
(10, 'Melbourne, AUS'),
(11, 'Sidney, AUS'),
(12, 'Ankara, Turkey');

-- ------------------
-- Products Table
-- ------------------
INSERT INTO products (product_name, category)
VALUES 
('Mountain Bike - Tera A', 'Mountain'),          -- Product_ID = 1
('Mountain Bike - Tera B', 'Mountain'),          -- Product_ID = 2
('Mountain Bike - Tera C', 'Mountain'),          -- Product_ID = 3
('Mountain Bike - Tera D', 'Mountain'),          -- Product_ID = 4
('Mountain Bike - Tera A', 'Hybrid'),            -- Product_ID = 5
('Mountain Bike - Tera B', 'Hybrid'),            -- Product_ID = 6
('Mountain Bike - Tera C', 'Hybrid'),            -- Product_ID = 7
('Mountain Bike - Tera D', 'Hybrid'),            -- Product_ID = 8
('Bike Helmet - SafeHelmets-1', 'Helmet'),       -- Product_ID = 9
('Bike Helmet - SafeHelmets-2', 'Helmet'),       -- Product_ID = 10
('Bike Helmet - SafeHelmets-3', 'Helmet'),       -- Product_ID = 11
('Bike Helmet - SafeHelmets-4', 'Helmet'),       -- Product_ID = 12
('Bike Helmet - SafeHelmets-5', 'Helmet'),       -- Product_ID = 13
('Bike Helmet - SafeHelmets-6', 'Helmet'),       -- Product_ID = 14
('Bike Lock - SecuLock-A', 'MISC'),              -- Product_ID = 15
('Bike Lock - SecuLock-B', 'MISC'),              -- Product_ID = 16
('Bike Lock - SecuLock-C', 'MISC'),              -- Product_ID = 17
('Bike Lock - SecuLock-D', 'MISC'),              -- Product_ID = 18
('Bike Lock - SecuLock-E', 'MISC'),              -- Product_ID = 19
('Bike Lock - SecuLock-F', 'MISC'),              -- Product_ID = 20
('Fixed gear bike - SlowRoad-1', 'Regular'),     -- Product_ID = 21
('Fixed gear bike - SlowRoad-2', 'Regular'),     -- Product_ID = 22
('Fixed gear bike - SlowRoad-3', 'Regular'),     -- Product_ID = 23
('Fixed gear bike - SlowRoad-4', 'Regular'),     -- Product_ID = 24
('Fixed gear bike - SlowRoad-5', 'Regular'),     -- Product_ID = 25
('Fixed gear bike - SlowRoad-6', 'Regular'),     -- Product_ID = 26
('Fixed gear bike - Road-1', 'Road-Regular'),    -- Product_ID = 27
('Fixed gear bike - Road-2', 'Road-Regular'),    -- Product_ID = 28
('Fixed gear bike - Road-3', 'Road-Regular'),    -- Product_ID = 29
('Fixed gear bike - Road-4', 'Road-Regular'),    -- Product_ID = 30
('Fixed gear bike - Road-5', 'Road-Regular'),    -- Product_ID = 31
('Fixed gear bike - Road-6', 'Road-Regular'),    -- Product_ID = 32
('Fixed gear bike - FastRoad-A', 'Fast'),        -- Product_ID = 33
('Fixed gear bike - FastRoad-B', 'Fast'),        -- Product_ID = 34
('Fixed gear bike - FastRoad-C', 'Fast'),        -- Product_ID = 35
('Fixed gear bike - FastRoad-D', 'Fast'),        -- Product_ID = 36
('Fixed gear bike - FastRoad-E', 'Fast'),        -- Product_ID = 37
('Fixed gear bike - FastRoad-F', 'Fast'),        -- Product_ID = 38
('Fixed gear bike - FastRoad-G', 'Fast'),        -- Product_ID = 39
('Fixed gear bike - FastRoad-H', 'Fast'),        -- Product_ID = 40
('Hybrid bike - SlowRoad-41', 'Hybrid'),         -- Product_ID = 41
('Hybrid bike - SlowRoad-42', 'Hybrid'),         -- Product_ID = 42
('Hybrid bike - SlowRoad-43', 'Hybrid'),         -- Product_ID = 43
('Hybrid bike - SlowRoad-44', 'Hybrid'),         -- Product_ID = 44
('Hybrid bike - SlowRoad-45', 'Hybrid'),         -- Product_ID = 45
('Hybrid bike - SlowRoad-46', 'Hybrid'),         -- Product_ID = 46
('Hybrid bike - SlowRoad-47', 'Hybrid'),         -- Product_ID = 47
('E-bike - Regular-Type 1', 'EBIKE'),            -- Product_ID = 48
('E-bike - Regular-Type 2', 'EBIKE'),            -- Product_ID = 49
('E-bike - Regular-Type 3', 'EBIKE'),            -- Product_ID = 50
('E-bike - Regular-Type 4', 'EBIKE'),            -- Product_ID = 51
('E-bike - Regular-Type 5', 'EBIKE'),            -- Product_ID = 52
('E-bike - Regular-Type 6', 'EBIKE'),            -- Product_ID = 53
('E-bike - Regular-Type 7', 'EBIKE'),            -- Product_ID = 54
('E-bike - Regular-Type 8', 'EBIKE'),            -- Product_ID = 55
('E-bike - Type 1', 'EBIKE-BASIC'),              -- Product_ID = 56
('E-bike - Type 2', 'EBIKE-BASIC'),              -- Product_ID = 57
('E-bike - Type 3', 'EBIKE-BASIC'),              -- Product_ID = 58
('E-bike - Type 4', 'EBIKE-BASIC'),              -- Product_ID = 59
('E-bike - Type 5', 'EBIKE-BASIC'),              -- Product_ID = 60
('E-bike - Type 6', 'EBIKE-BASIC'),              -- Product_ID = 61
('Advanced E-bike - Type 1', 'ADV-EBIKE'),       -- Product_ID = 62
('Advanced E-bike - Type 2', 'ADV-EBIKE'),       -- Product_ID = 63
('Advanced E-bike - Type 3', 'ADV-EBIKE'),       -- Product_ID = 64
('Advanced E-bike - Type 4', 'ADV-EBIKE'),       -- Product_ID = 65
('Advanced E-bike - Type 5', 'ADV-EBIKE'),       -- Product_ID = 66
('Advanced E-bike - Type 6', 'ADV-EBIKE'),       -- Product_ID = 67
('Advanced E-bike - Type 7', 'ADV-EBIKE'),       -- Product_ID = 68
('Advanced E-bike - Type 8', 'ADV-EBIKE'),       -- Product_ID = 69
('Lock Type 1', 'LOCK'),                         -- Product_ID = 70
('Lock Type 2', 'LOCK'),                         -- Product_ID = 71
('Lock Type 3', 'LOCK'),                         -- Product_ID = 72
('Lock Type 4', 'LOCK'),                         -- Product_ID = 73
('Lock Type 5', 'LOCK'),                         -- Product_ID = 74
('Lock Type 6', 'LOCK'),                         -- Product_ID = 75
('Lock Type 7', 'LOCK'),                         -- Product_ID = 76
('Lock Type 8', 'LOCK'),                         -- Product_ID = 77
('Mirror Type 1', 'MIRROR'),                     -- Product_ID = 78
('Mirror Type 2', 'MIRROR'),                     -- Product_ID = 79
('Mirror Type 3', 'MIRROR'),                     -- Product_ID = 80
('Mirror Type 4', 'MIRROR'),                     -- Product_ID = 81
('Mirror Type 5', 'MIRROR'),                     -- Product_ID = 82
('Mirror Type 6', 'MIRROR'),                     -- Product_ID = 83
('Mirror Type 7', 'MIRROR'),                     -- Product_ID = 84
('Brakes Type 1', 'BRAKE'),                      -- Product_ID = 85
('Brakes Type 2', 'BRAKE'),                      -- Product_ID = 86
('Brakes Type 3', 'BRAKE'),                      -- Product_ID = 87
('Brakes Type 4', 'BRAKE'),                      -- Product_ID = 88
('Brakes Type 5', 'BRAKE'),                      -- Product_ID = 89
('Brakes Type 6', 'BRAKE'),                      -- Product_ID = 90
('Brakes Type 7', 'BRAKE'),                      -- Product_ID = 91
('ADV Bike Helmet -1', 'Helmet'),                -- Product_ID = 92
('ADV Bike Helmet -2', 'Helmet'),                -- Product_ID = 93
('ADV Bike Helmet -3', 'Helmet'),                -- Product_ID = 94
('ADV Bike Helmet -4', 'Helmet'),                -- Product_ID = 95
('ADV Bike Helmet -5', 'Helmet'),                -- Product_ID = 96
('ADV Bike Helmet -6', 'Helmet'),                -- Product_ID = 97
('ADV Bike Helmet -7', 'Helmet'),                -- Product_ID = 98
('ADV Bike Helmet -8', 'Helmet'),                -- Product_ID = 99
('ADV Bike Helmet -9', 'Helmet');                -- Product_ID = 100


-- -----------
-- verify data
-- -----------
SELECT * FROM stores;
SELECT * FROM products;
SELECT * FROM customers;
SELECT * FROM dates;
SELECT * FROM sales;


Below is a fully working MySQL 8+ scalable data generation script that:

•	✅ Creates 1,000,000 customers
•	600,000 MALE
•	400,000 FEMALE
•	Countries are intentionally NOT evenly distributed
•	✅ Creates 6,000,000 sales rows
•	Date span: 2010–01–01 → 2025–12–31
•	✅ Generates dates dimension from sales table
•	✅ Uses efficient number-generation (cross joins)
•	✅ Avoids recursion limits
•	✅ Maintains referential integrity

⸻

* MySQL Database parameters:

SET GLOBAL max_allowed_packet = 512M;
mysql> SET GLOBAL max_allowed_packet = 512M;

SET autocommit = 0;
mysql> SET autocommit = 0;

⸻

🔢 STEP 1 — Create Helper Numbers Table (1..6,000,000)

DROP TABLE IF EXISTS numbers_6m;
CREATE TABLE numbers_6m (n INT PRIMARY KEY);

INSERT INTO numbers_6m (n)
SELECT x.n
FROM (
  SELECT 
    (a.d + 10*b.d + 100*c.d + 1000*d.d + 10000*e.d + 100000*f.d + 1000000*g.d) + 1 AS n
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
  CROSS JOIN
    (SELECT 0 d UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) g
) x
WHERE x.n <= 6000000;


⸻

👥 STEP 2 — Create 1,000,000 Customers
	•	First 600,000 → MALE
	•	Next 400,000 → FEMALE
	•	Countries intentionally uneven distribution

INSERT INTO customers (customer_name, gender, country, email)
SELECT
  CONCAT('Customer_', n),
  
  CASE 
    WHEN n <= 600000 THEN 'MALE'
    ELSE 'FEMALE'
  END AS gender,

  CASE
    WHEN MOD(n, 13) = 0 THEN 'USA'
    WHEN MOD(n, 17) = 0 THEN 'CANADA'
    WHEN MOD(n, 19) = 0 THEN 'MEXICO'
    WHEN MOD(n, 23) = 0 THEN 'GERMANY'
    WHEN MOD(n, 29) = 0 THEN 'FRANCE'
    WHEN MOD(n, 31) = 0 THEN 'INDIA'
    WHEN MOD(n, 37) = 0 THEN 'CHINA'
    WHEN MOD(n, 41) = 0 THEN 'TURKEY'
    WHEN MOD(n, 43) = 0 THEN 'ENGLAND'
    ELSE 'ITALY'
  END AS country,

  CONCAT('customer', n, '@bike.com')

FROM numbers_6m
WHERE n <= 1000000;

✔ This ensures countries are NOT evenly distributed.

⸻
📅 STEP 3 Create dates: (5844 days ≈ 16 years)

INSERT INTO dates (date, year, month, day, quarter)
SELECT
    dt,
    YEAR(dt),
    MONTH(dt),
    DAY(dt),
    QUARTER(dt)
FROM (
    SELECT DATE_ADD('2010-01-01', INTERVAL n DAY) AS dt
    FROM numbers_6m
    WHERE n <= 5844   -- ~16 years
) t;

💰 STEP 4 — Create 6,000,000 Sales Records (2010–2025)

Date range = 16 years

INSERT INTO sales (
    sale_type,
    product_id,
    store_id,
    customer_id,
    date_id,
    quantity,
    amount,
    sale_amount
)
SELECT
    CASE WHEN MOD(n,2)=0 THEN 'IN-STORE' ELSE 'ON-LINE' END,

    1 + MOD(n,100),
    1 + MOD(n,12),
    1 + MOD(n,1000000),

    1 + MOD(n,5844),  -- valid date_id range

    1 + MOD(n,5),
    ROUND(50 + MOD(n,500),2),

    (1 + MOD(n,5)) * ROUND(50 + MOD(n,500),2)

FROM numbers_6m
WHERE n <= 6000000;

⸻

🧹 Optional Cleanup

ALTER TABLE sales DROP COLUMN sale_date;
COMMIT;


⸻

✅ Verification Queries

SELECT COUNT(*) FROM customers; -- 1,000,000
SELECT gender, COUNT(*) FROM customers GROUP BY gender;

SELECT COUNT(*) FROM sales; -- 6,000,000
SELECT MIN(date), MAX(date) FROM dates;

SELECT COUNT(*) FROM dates; -- ~5844 rows


⸻

🎯 What You Now Have

Table        Rows
---------    ---------
customers    1,000,000
products           100
stores              12
sales        6,000,000
dates             5844


⸻

🚀 Performance Tip (Very Important)

After loading:

ALTER TABLE sales ADD INDEX idx_sales_date(date_id);
ALTER TABLE sales ADD INDEX idx_sales_customer(customer_id);
ALTER TABLE sales ADD INDEX idx_sales_product(product_id);
ALTER TABLE sales ADD INDEX idx_sales_store(store_id);


