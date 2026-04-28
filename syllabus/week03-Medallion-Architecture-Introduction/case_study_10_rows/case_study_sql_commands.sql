-- create bronze, silver, and gold schemas
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

-- create bronze.sales_raw from sales_data_10_rows.csv
CREATE OR REPLACE TABLE bronze.sales_raw AS
SELECT
    ROW_NUMBER() OVER () AS row_id,   --  add row_id
    *
FROM read_csv_auto(
    'sales_data_10_rows.csv',
    header = true,
    all_varchar = true
);


-- View `bronze.sales_raw`
SELECT COUNT(*) 
FROM bronze.sales_raw;

SELECT * 
FROM bronze.sales_raw;




-- This SQL query ignores `row_id` 
-- when detecting duplicates:
CREATE OR REPLACE TABLE silver.step01_dedup AS
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY 
                   sale_id, 
                   sale_type, 
                   product, 
                   customer_name,
                   customer_email, 
                   customer_country, 
                   quantity,
                   unit_price, 
                   discount, 
                   store_location, 
                   sale_date
               ORDER BY row_id
           ) AS rn
    FROM bronze.sales_raw
)
WHERE rn = 1;


-- View `silver.step01_dedup`
--
SELECT COUNT(*) 
FROM silver.step01_dedup;

SELECT * 
FROM  silver.step01_dedup 
ORDER by row_id;



-- Silver Step 2 — Standardize strings and prepare fields
-- Before applying business rules, we normalize text and 
-- preserve raw values for safe parsing.
CREATE OR REPLACE TABLE silver.step02_standardized AS
SELECT
    -- =========================
    -- TECHNICAL COLUMN
    -- =========================
    row_id,

    -- Preserve row identifier for debugging and lineage

    -- =========================
    -- CORE IDENTIFIER
    -- =========================

    NULLIF(TRIM(sale_id), '') AS sale_id_raw,
    -- Remove whitespace and convert empty sale_id to NULL

    -- =========================
    -- TRANSACTION ATTRIBUTES
    -- =========================

    UPPER(NULLIF(TRIM(sale_type), '')) AS sale_type,
    -- Standardize sale type (ON-LINE, IN-STORE)

    UPPER(NULLIF(TRIM(product), '')) AS product,
    -- Normalize product names to uppercase

    -- =========================
    -- CUSTOMER
    -- =========================

    NULLIF(TRIM(customer_name), '') AS customer_name,
    -- Clean customer name and convert empty to NULL

    LOWER(NULLIF(TRIM(customer_email), '')) AS customer_email,
    -- Normalize email to lowercase

    UPPER(NULLIF(TRIM(customer_country), '')) AS customer_country,
    -- Standardize country names

    -- =========================
    -- MEASURES
    -- =========================

    TRY_CAST(NULLIF(TRIM(quantity), '') AS INTEGER) AS quantity,
    -- Convert quantity to integer

    TRY_CAST(NULLIF(TRIM(unit_price), '') AS DOUBLE) AS unit_price,
    -- Convert unit price to numeric

    NULLIF(TRIM(discount), '') AS discount_raw,
    -- Preserve discount for later business rules

    -- =========================
    -- STORE
    -- =========================

    UPPER(NULLIF(TRIM(store_location), '')) AS store_location,
    -- Standardize store location

    -- =========================
    -- DATE (RAW)
    -- =========================

    NULLIF(TRIM(sale_date), '') AS sale_date_raw
    -- Keep raw date for parsing in next step

FROM silver.step01_dedup;



-- View `silver.step02_standardized`
--
SELECT COUNT(*) 
FROM silver.step02_standardized;

SELECT * 
FROM silver.step02_standardized 
ORDER BY row_id;


-- Silver Step 3 — Rule 4: Fix discount values
-- Business rule
-- Null, missing, or negative discount becomes `0.00`.
--
-- Create `silver.step03_discount_fixed`
--
CREATE OR REPLACE TABLE silver.step03_discount_fixed AS
SELECT
    *,
    -- =========================
    -- DISCOUNT CLEANING
    -- =========================

    CASE
        WHEN discount_num IS NULL THEN 0.00
        WHEN discount_num < 0 THEN 0.00
        ELSE discount_num
    END AS discount

FROM (
    SELECT
        *,
        TRY_CAST(discount_raw AS DOUBLE) AS discount_num
        -- Convert raw discount once for reuse

    FROM silver.step02_standardized
);


-- View `silver.step03_discount_fixed`
--
SELECT COUNT(*) 
FROM silver.step03_discount_fixed;

SELECT * 
FROM silver.step03_discount_fixed 
ORDER BY row_id;




-- Silver Step 4 — Rules 5 and 6: Parse sale_date
-- Business rule
-- Only these formats are valid:
--
--   `MM/DD/YYYY`
--   `YYYY-MM-DD`
--
-- Create `silver.step04_date_parsed`
--
CREATE OR REPLACE TABLE silver.step04_date_parsed AS
SELECT
    *,

    -- Only accept VALID formats explicitly
    CASE
        WHEN sale_date_raw LIKE '__/__/____' THEN
            TRY_STRPTIME(sale_date_raw, '%m/%d/%Y')::DATE

        WHEN sale_date_raw LIKE '____-__-__' THEN
            TRY_STRPTIME(sale_date_raw, '%Y-%m-%d')::DATE

        ELSE NULL
    END AS sale_date

FROM silver.step03_discount_fixed;


-- View `silver.step04_date_parsed`
--
SELECT COUNT(*) 
FROM silver.step04_date_parsed;

SELECT * 
FROM silver.step04_date_parsed 
ORDER BY row_id;

-- Debuggable (VERY IMPORTANT)
SELECT sale_date_raw, 
       sale_date
FROM silver.step04_date_parsed
WHERE sale_date IS NULL;


-- What the result proves:
-- 
-- sale_date_raw        → sale_date
-- --------------------------------
-- 2025-02-29           → NULL ✔ (invalid date)
-- 31-12-25             → NULL ✔ (invalid format)
-- NULL                 → NULL ✔ (missing)


-- Silver Step 5 — Rules 2, 3, and 6: Reject invalid rows
-- Business rule
-- Reject rows where:
-- - `product` is missing
-- - `customer_name` is missing/empty
-- - `sale_date` is missing or invalid
--
-- Important: Rejected rows are **not cancelled**.

-- Create `silver.rejected_records`
--
CREATE OR REPLACE TABLE silver.rejected_records AS
SELECT
    *,

    -- =========================
    -- REJECTION REASON
    -- =========================
    CASE
        WHEN product IS NULL THEN 'REJECT_MISSING_PRODUCT'

        WHEN customer_name IS NULL THEN 'REJECT_MISSING_CUSTOMER_NAME'

        WHEN customer_email IS NULL THEN 'REJECT_MISSING_EMAIL'
        
        WHEN POSITION('@' IN customer_email) = 0 THEN 'REJECT_INVALID_EMAIL'

        WHEN quantity IS NULL OR quantity <= 0 THEN 'REJECT_INVALID_QUANTITY'

        WHEN unit_price IS NULL OR unit_price <= 0 THEN 'REJECT_INVALID_UNIT_PRICE'

        WHEN store_location IS NULL THEN 'REJECT_MISSING_STORE_LOCATION'

        WHEN sale_date IS NULL THEN 'REJECT_INVALID_OR_MISSING_SALE_DATE'

        ELSE 'REJECT_OTHER'
    END AS reject_reason

FROM silver.step04_date_parsed

-- =========================
-- FILTER: ONLY BAD RECORDS
-- =========================
WHERE
    product IS NULL
    OR customer_name IS NULL
    OR customer_email IS NULL
    OR POSITION('@' IN customer_email) = 0
    OR quantity IS NULL OR quantity <= 0
    OR unit_price IS NULL OR unit_price <= 0
    OR store_location IS NULL
    OR sale_date IS NULL;


-- View `silver.rejected_records`
--
SELECT COUNT(*) 
FROM silver.rejected_records;

SELECT * 
FROM silver.rejected_records 
ORDER BY row_id;

-- Rejected Rows
-- 
-- | row_id | reason |
-- |-------:|--------|
-- | 4      | `REJECT_MISSING_PRODUCT` |
-- | 5      | `REJECT_MISSING_CUSTOMER_NAME` |
-- | 6      | `REJECT_INVALID_OR_MISSING_SALE_DATE` |
-- | 7      | `REJECT_INVALID_OR_MISSING_SALE_DATE` |
-- | 10.    | `REJECT_INVALID_OR_MISSING_SALE_DATE` |

-- ### Rejected count = 5


-- Silver Step 6 — Rule 1: Capture cancelled transactions
-- Business rule
-- Missing `sale_id` means **cancelled transaction**.
-- Important: A row counts as cancelled only if it is otherwise valid.

-- That means row 3 is cancelled because:
--  - `sale_id` is missing
--  - product exists
--  - customer_name exists
--  - sale_date is valid


-- Create `silver.cancelled_transactions`
--
CREATE OR REPLACE TABLE silver.cancelled_transactions AS
SELECT
    *
    -- Keep full schema for traceability and debugging

FROM silver.step04_date_parsed
WHERE
    -- =========================
    -- CANCELLED CONDITION
    -- =========================
    sale_id_raw IS NULL

    -- =========================
    -- MUST BE OTHERWISE VALID
    -- =========================
    AND product IS NOT NULL
    AND customer_name IS NOT NULL

    AND customer_email IS NOT NULL
    AND POSITION('@' IN customer_email) > 0

    AND quantity IS NOT NULL AND quantity > 0
    AND unit_price IS NOT NULL AND unit_price > 0

    AND store_location IS NOT NULL

    AND sale_date IS NOT NULL;


-- View `silver.cancelled_transactions`
--
SELECT COUNT(*) 
FROM silver.cancelled_transactions;

SELECT * 
FROM silver.cancelled_transactions 
ORDER BY row_id;
                                      
-- Silver Step 7 — Rule 8: Build trusted sales and compute final price
-- ## Business rule
--   `final_sale_price = (quantity * unit_price) - discount`
--
-- Create `silver.sales_clean`
--
CREATE OR REPLACE TABLE silver.sales_clean AS
SELECT
    -- =========================
    -- CORE IDENTIFIER
    -- =========================
    TRY_CAST(sale_id_raw AS INTEGER) AS sale_id,

    -- =========================
    -- DIMENSIONS
    -- =========================
    sale_type,
    product,
    customer_name,
    customer_email,
    customer_country,
    store_location,
    sale_date,

    -- =========================
    -- MEASURES
    -- =========================
    quantity,
    unit_price,
    discount,

    -- =========================
    -- DERIVED METRIC
    -- =========================
    (quantity * unit_price) - discount AS final_sale_price

FROM silver.step04_date_parsed

WHERE
    -- =========================
    -- VALID TRANSACTION (NOT CANCELLED)
    -- =========================
    TRY_CAST(sale_id_raw AS INTEGER) IS NOT NULL

    -- =========================
    -- DATA QUALITY RULES
    -- =========================
    AND product IS NOT NULL
    AND customer_name IS NOT NULL

    AND customer_email IS NOT NULL
    AND POSITION('@' IN customer_email) > 0

    AND quantity IS NOT NULL AND quantity > 0
    AND unit_price IS NOT NULL AND unit_price > 0

    AND store_location IS NOT NULL

    AND sale_date IS NOT NULL;


-- View `silver.sales_clean`
-- Trusted Silver Rows
--
SELECT COUNT(*) 
FROM silver.sales_clean; 

SELECT * 
FROM silver.sales_clean 
ORDER BY sale_id;


-- Funnel SQL
SELECT 'bronze.sales_raw' AS stage, 
       COUNT(*) AS row_count 
FROM bronze.sales_raw
UNION ALL
SELECT 'after_dedup', 
       COUNT(*) 
FROM silver.step01_dedup
UNION ALL
SELECT 'rejected_records', 
       COUNT(*) 
FROM silver.rejected_records
UNION ALL
SELECT 'cancelled_transactions', 
       COUNT(*) 
FROM silver.cancelled_transactions
UNION ALL
SELECT 'trusted_sales_clean', 
       COUNT(*) 
FROM silver.sales_clean;

-- This funnel is one of the best teaching visuals 
-- in a medallion pipeline.
--
-- # End-to-End Funnel
-- | `stage`                 | `row_count` |
-- |-------------------------|------------:|
-- | `bronze.sales_raw`      | 10          |
-- | `after_dedup`           |  9          |
-- | `rejected_records`      |  5          |
-- | `cancelled_transactions`|  1          |
-- | `trusted_sales_clean`   |  3          |


---

-- # Gold Layer — Why only trusted rows?
-- Gold is for:
--
--   - analytics
--   - BI dashboards
--   - business decisions
--
-- Next, we build a "Star Schema"
--
--
--
--              dim_customer
--                    │
--                    │       
--  dim_product ───  fact_sales  ─── dim_date


-- 🟡 Gold Example — Customer Dimension
--
CREATE OR REPLACE TABLE gold.dim_customer AS
SELECT
    -- =========================
    -- SURROGATE KEY
    -- =========================
    ROW_NUMBER() OVER (ORDER BY customer_email) AS customer_key,

    -- =========================
    -- BUSINESS KEYS / ATTRIBUTES
    -- =========================
    customer_name,
    customer_email,
    customer_country

FROM (
    SELECT DISTINCT
        customer_name,
        customer_email,
        customer_country
    FROM silver.sales_clean
);


-- View `gold.dim_customer`
SELECT COUNT(*) 
FROM gold.dim_customer;

SELECT * 
FROM gold.dim_customer
ORDER BY customer_key;



-- 🟡 Gold Example — Product Dimension
--
CREATE OR REPLACE TABLE gold.dim_product AS
SELECT
    -- =========================
    -- SURROGATE KEY
    -- =========================
    ROW_NUMBER() OVER (ORDER BY product) AS product_key,

    -- =========================
    -- PRODUCT ATTRIBUTE
    -- =========================
    product

FROM (
    SELECT DISTINCT product
    FROM silver.sales_clean
);


-- View `gold.dim_product`
SELECT COUNT(*)
FROM gold.dim_product;

SELECT * 
FROM gold.dim_product;



-- 🟡 Gold Example: Date Dimension
-- Build a Date Dimension
-- Date Dimension = the most powerful dimension in analytics
--
CREATE OR REPLACE TABLE gold.dim_date AS
SELECT
    -- =========================
    -- SURROGATE KEY
    -- =========================
    ROW_NUMBER() OVER (ORDER BY sale_date) AS date_key,

    -- =========================
    -- CORE DATE
    -- =========================
    sale_date AS full_date,

    -- =========================
    -- DATE ATTRIBUTES
    -- =========================
    EXTRACT(YEAR FROM sale_date) AS year_num,
    EXTRACT(MONTH FROM sale_date) AS month_num,
    EXTRACT(DAY FROM sale_date) AS day_num,

    STRFTIME(sale_date, '%Y-%m') AS year_month,
    STRFTIME(sale_date, '%B') AS month_name,
    STRFTIME(sale_date, '%A') AS day_name,

    -- =========================
    -- BUSINESS FLAGS
    -- =========================
    CASE 
        WHEN STRFTIME(sale_date, '%w') IN ('0','6') THEN 'WEEKEND'
        ELSE 'WEEKDAY'
    END AS day_type

FROM (
    SELECT DISTINCT sale_date
    FROM silver.sales_clean
);

-- Verify Date Dimension
SELECT COUNT(*)
FROM gold.dim_date;

SELECT *
FROM gold.dim_date
ORDER BY date_key;


-- 🟡 Gold Example — Fact Table
--
CREATE OR REPLACE TABLE gold.fact_sales AS
SELECT
    -- =========================
    -- FACT KEY (BUSINESS KEY)
    -- =========================
    s.sale_id,

    -- =========================
    -- FOREIGN KEYS
    -- =========================
    c.customer_key,
    p.product_key,
    d.date_key,

    -- =========================
    -- MEASURES
    -- =========================
    s.quantity,
    s.unit_price,
    s.discount,
    s.final_sale_price

FROM silver.sales_clean s

-- =========================
-- DIMENSION JOINS
-- =========================
JOIN gold.dim_customer c
    ON s.customer_email = c.customer_email

JOIN gold.dim_product p
    ON s.product = p.product

JOIN gold.dim_date d
    ON s.sale_date = d.full_date;


-- View `gold.fact_sales`
SELECT COUNT(*) 
FROM gold.fact_sales;

SELECT * 
FROM gold.fact_sales
ORDER BY sale_id;
