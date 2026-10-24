-- ============================================================
-- Generate ~100,000 additional fact rows (MySQL 8.x)
-- Assumes:
--   1) ecommerce_dw database already exists
--   2) dim_date, dim_customer_scd2, dim_product, dim_store, dim_channel populated
--   3) Surrogate keys start at 1 and are reasonably contiguous
-- ============================================================

USE ecommerce_dw;

-- Increase recursion limit for large sequence
SET SESSION cte_max_recursion_depth = 200000;

-- Optional: check existing max surrogate values
-- SELECT MAX(customer_sk) FROM dim_customer_scd2;
-- SELECT MAX(product_sk)  FROM dim_product;
-- SELECT MAX(store_sk)    FROM dim_store;
-- SELECT MAX(channel_sk)  FROM dim_channel;

-- We dynamically fetch max surrogate keys for better distribution
SET @max_customer = (SELECT MAX(customer_sk) FROM dim_customer_scd2);
SET @max_product  = (SELECT MAX(product_sk)  FROM dim_product);
SET @max_store    = (SELECT MAX(store_sk)    FROM dim_store);
SET @max_channel  = (SELECT MAX(channel_sk)  FROM dim_channel);

-- Insert 100,000 synthetic fact rows
-- Grain: one row per synthetic order line
WITH RECURSIVE seq AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n+1 FROM seq WHERE n < 100000
)
INSERT INTO fact_sales
(order_id, customer_sk, product_sk, store_sk, channel_sk, date_id, quantity, sales_amount)
SELECT
    900000 + n AS order_id,
    1 + (n % @max_customer) AS customer_sk,
    1 + (n % @max_product)  AS product_sk,
    CASE 
        WHEN (n % 3)=0 THEN NULL
        ELSE 1 + (n % @max_store)
    END AS store_sk,
    1 + (n % @max_channel) AS channel_sk,
    CAST(DATE_FORMAT(
        DATE('2022-01-01') + INTERVAL (n % 1500) DAY,
        '%Y%m%d') AS UNSIGNED) AS date_id,
    1 + (n % 5) AS quantity,
    ROUND((1 + (n % 5)) * (50 + (n % 500) * 0.75), 2) AS sales_amount
FROM seq;

-- ============================================================
-- Suggested sanity checks after load
-- ============================================================

-- SELECT COUNT(*) FROM fact_sales;
-- SELECT MIN(date_id), MAX(date_id) FROM fact_sales;
-- SELECT channel_sk, COUNT(*) FROM fact_sales GROUP BY channel_sk;
-- SELECT store_sk, COUNT(*) FROM fact_sales GROUP BY store_sk;
-- SELECT SUM(sales_amount) FROM fact_sales;

-- ============================================================
-- This will significantly improve the usefulness of:
--   - Window functions
--   - YoY growth
--   - Ranking & percentile queries
--   - Revenue distribution analysis
-- ============================================================
