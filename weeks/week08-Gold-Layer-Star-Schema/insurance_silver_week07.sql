-- Week 8 setup for the insurance examples: rebuild week 7's Silver table silver.insurance
-- (same rules as week 7, slides 1: conform → deduplicate → reject / flag).
-- Run from this week08 folder:   duckdb insurance.duckdb < insurance_silver_week07.sql
-- Result: 5,197 rows (4,160 valid + 1,037 flagged); 974 rejected; 296 duplicates; Bronze 6,467.

CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;

CREATE OR REPLACE TABLE bronze.insurance AS
SELECT * EXCLUDE (filename),
       regexp_extract(filename, '[^/]+$')                  AS _source_file,
       CAST(regexp_extract(filename, '(\d{4})', 1) AS INT) AS _batch_id,
       current_timestamp                                   AS _ingested_at
FROM read_csv('../week07-Silver-Layer-Cleaning-and-Conforming/data_messy/insurance.*.messy.csv', all_varchar = true, filename = true);

CREATE OR REPLACE MACRO norm_region(r) AS regexp_replace(lower(trim(r)), '[ -]', '', 'g');
CREATE OR REPLACE TABLE silver.map_region AS SELECT * FROM (VALUES
    ('northeast', 'northeast'), ('northwest', 'northwest'),
    ('southeast', 'southeast'), ('southwest', 'southwest')) t(region_key, region);
CREATE OR REPLACE TABLE silver.map_smoker AS SELECT * FROM (VALUES ('yes', 'yes'), ('no', 'no')) t(smoker_key, smoker);
CREATE OR REPLACE TABLE silver.map_gender AS SELECT * FROM (VALUES ('female', 'female'), ('male', 'male'), ('m', 'male')) t(gender_key, gender);

CREATE OR REPLACE TABLE silver.step1_standardized AS
SELECT b._batch_id,
       TRY_CAST(TRY_CAST(b.age AS DOUBLE) AS INTEGER)      AS age,
       COALESCE(g.gender, 'unknown')                       AS gender,
       TRY_CAST(b.bmi AS DECIMAL(5, 2))                    AS bmi,
       TRY_CAST(TRY_CAST(b.children AS DOUBLE) AS INTEGER) AS children,
       COALESCE(s.smoker, 'unknown')                       AS smoker,
       COALESCE(r.region, 'unknown')                       AS region,
       TRY_CAST(b.charges AS DECIMAL(10, 2))               AS charges,
       b.region                                            AS region_raw
FROM bronze.insurance b
LEFT JOIN silver.map_region r ON r.region_key = norm_region(b.region)
LEFT JOIN silver.map_smoker s ON s.smoker_key = lower(trim(b.smoker))
LEFT JOIN silver.map_gender g ON g.gender_key = lower(trim(b.gender));

CREATE OR REPLACE TABLE silver.step2_dedup AS
SELECT * FROM silver.step1_standardized
QUALIFY ROW_NUMBER() OVER (PARTITION BY _batch_id, age, gender, bmi, children, smoker, region, charges ORDER BY region_raw) = 1;

CREATE OR REPLACE TABLE silver.insurance_rejected AS
SELECT *,
       CASE WHEN age IS NULL OR bmi IS NULL OR children IS NULL OR charges IS NULL THEN 'missing value'
            WHEN age NOT BETWEEN 18 AND 100     THEN 'age outside 18-100'
            WHEN bmi NOT BETWEEN 12 AND 70      THEN 'bmi outside 12-70'
            WHEN children NOT BETWEEN 0 AND 10  THEN 'children outside 0-10'
            ELSE 'charges <= 0' END AS reject_reason
FROM silver.step2_dedup
WHERE age IS NULL OR bmi IS NULL OR children IS NULL OR charges IS NULL
   OR age NOT BETWEEN 18 AND 100 OR bmi NOT BETWEEN 12 AND 70
   OR children NOT BETWEEN 0 AND 10 OR charges <= 0;

CREATE OR REPLACE TABLE silver.insurance AS
SELECT _batch_id AS year, age, gender, bmi, children, smoker, region, charges, region_raw,
       gender = 'unknown' AS is_gender_unknown,
       smoker = 'unknown' AS is_smoker_unknown,
       region = 'unknown' AS is_region_unknown
FROM silver.step2_dedup
WHERE NOT (age IS NULL OR bmi IS NULL OR children IS NULL OR charges IS NULL
           OR age NOT BETWEEN 18 AND 100 OR bmi NOT BETWEEN 12 AND 70
           OR children NOT BETWEEN 0 AND 10 OR charges <= 0);

SELECT COUNT(*) AS silver_rows FROM silver.insurance;   -- 5,197
