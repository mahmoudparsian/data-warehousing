---
marp: true

theme: default

paginate: true

title: Medallion Architecture Running Case Study

author: Mahmoud Parsian

---

# Medallion Architecture Running Case Study

### One dataset flowing through Bronze → Silver → Gold

---

## Database 

```
% duckdb --version
v1.5.2 (Variegata) 8a5851971f
```

---

## Scenario

This document follows the **same 10 messy sales rows** through a medallion pipeline.

It is designed for teaching:

- how each business rule changes the data
- why order matters
- how rejected rows differ from cancelled rows
- how trusted Gold data emerges from messy Bronze data

---

# Business Rules

1. Missing `sale_id` → **cancelled transaction**
2. Missing `product` → **drop record**
3. Missing/empty `customer_name` → **drop record**
4. Null/missing/negative `discount` → **0.00**
5. Valid `sale_date` formats only:
   - `MM/DD/YYYY`
   - `YYYY-MM-DD`
6. Missing/malformed/invalid `sale_date` → **drop record**
7. Drop exact duplicate rows
8. `final_sale_price = (quantity * unit_price) - discount`

---

# The 10 Raw Rows

| `row_id` | `sale_id` | `sale_type` | `product`  | `customer_name` | `customer_email`         | `customer_country` | `quantity` | `unit_price` | `discount` | `store_location` | `sale_date`   |
|-------:|--------:|-----------|----------|---------------|------------------------|------------------|---------:|-----------:|---------:|----------------|-------------|
| 1 | 1001 | ON-LINE  | TV       | John Smith    | john@a.com            | USA     | 1 | 900  | 50   | USA     | 12/31/2025 |
| 2 | 1002 | IN-STORE | IPHONE   | Mary Jones    | mary@a.com            | CANADA  | 2 | 1100 | -20  | CANADA  | 2025-12-30 |
| 3 |      | ON-LINE  | WATCH    | Bob Lee       | bob@a.com             | USA     | 3 | 200  | 10   | USA     | 12/29/2025 |
| 4 | 1004 | ON-LINE  |          | Alice Brown   | alice@a.com           | ENGLAND | 1 | 700  | 0    | ENGLAND | 12/28/2025 |
| 5 | 1005 | IN-STORE | EBIKE    |               | no_name@a.com         | USA     | 1 | 2200 | 100  | USA     | 2025-12-27 |
| 6 | 1006 | ON-LINE  | COMPUTER | David Kim     | david@a.com           | USA     | 1 | 1500 |      | USA     | 31-12-25   |
| 7 | 1007 | IN-STORE | IPAD     | Susan Clark   | susan@a.com           | FRANCE  | 2 | 700  | 20   | CANADA  |             |
| 8 | 1001 | ON-LINE  | TV       | John Smith    | john@a.com            | USA     | 1 | 900  | 50   | USA     | 12/31/2025 |
| 9 | 1009 | ON-LINE  | WATCH    | Rita Patel    | rita@a.com            | GERMANY | 4 | 250  | 30   | ENGLAND | 2025-12-26 |
| 10| 1010 | IN-STORE | COMPUTER | Omar Khan     | omar@a.com            | MEXICO  | 1 | 1400 | 0    | USA     | 2025-02-29 |

---

# Why these 10 rows are good for teaching

They include:

- a valid record
- a negative discount
- a cancelled transaction
- a missing product
- a missing customer name
- a malformed date
- a missing date
- an exact duplicate
- another valid record
- an invalid calendar date

This gives students one compact but realistic end-to-end case.

---

# Bronze Layer

## Goal

* Preserve the landed source as-is.

* In Bronze, we do **not** apply business rules yet.

* In Bronze, we keep the raw values for traceability and auditability.

---
# 10 Rows Dataset

```
% cat sales_data_10_rows.csv
sale_id,sale_type,product,customer_name,customer_email,customer_country,quantity,unit_price,discount,store_location,sale_date
1001,ON-LINE,TV,John Smith,john@a.com,USA,1,900,50,USA,12/31/2025
1002,IN-STORE,IPHONE,Mary Jones,mary@a.com,CANADA,2,1100,-20,CANADA,2025-12-30
,ON-LINE,WATCH,Bob Lee,bob@a.com,USA,3,200,10,USA,12/29/2025
1004,ON-LINE,,Alice Brown,alice@a.com,ENGLAND,1,700,0,ENGLAND,12/28/2025
1005,IN-STORE,EBIKE,,no_name@a.com,USA,1,2200,100,USA,2025-12-27
1006,ON-LINE,COMPUTER,David Kim,david@a.com,USA,1,1500,,USA,31-12-25
1007,IN-STORE,IPAD,Susan Clark,susan@a.com,FRANCE,2,700,20,CANADA,
1001,ON-LINE,TV,John Smith,john@a.com,USA,1,900,50,USA,12/31/2025
1009,ON-LINE,WATCH,Rita Patel,rita@a.com,GERMANY,4,250,30,ENGLAND,2025-12-26
1010,IN-STORE,COMPUTER,Omar Khan,omar@a.com,MEXICO,1,1400,0,USA,2025-02-29
```

# Bronze SQL

```sql
CREATE SCHEMA IF NOT EXISTS bronze;

CREATE OR REPLACE TABLE bronze.sales_raw AS

SELECT
    ROW_NUMBER() OVER () AS row_id,   -- 👈 add row_id
    *
FROM read_csv_auto(
    'sales_data_10_rows.csv',
    header = true,
    all_varchar = true
);
```

## View `bronze.sales_raw`

```sql
SELECT * 
FROM bronze.sales_raw;

┌────────┬─────────┬───────────┬──────────┬───────────────┬────────────────┬───┬──────────┬────────────┬──────────┬────────────────┬────────────┐
│ row_id │ sale_id │ sale_type │ product  │ customer_name │ customer_email │ … │ quantity │ unit_price │ discount │ store_location │ sale_date  │
│ int64  │ varchar │  varchar  │ varchar  │    varchar    │    varchar     │ … │ varchar  │  varchar   │ varchar  │    varchar     │  varchar   │
├────────┼─────────┼───────────┼──────────┼───────────────┼────────────────┼───┼──────────┼────────────┼──────────┼────────────────┼────────────┤
│      1 │ 1001    │ ON-LINE   │ TV       │ John Smith    │ john@a.com     │ … │ 1        │ 900        │ 50       │ USA            │ 12/31/2025 │
│      2 │ 1002    │ IN-STORE  │ IPHONE   │ Mary Jones    │ mary@a.com     │ … │ 2        │ 1100       │ -20      │ CANADA         │ 2025-12-30 │
│      3 │ NULL    │ ON-LINE   │ WATCH    │ Bob Lee       │ bob@a.com      │ … │ 3        │ 200        │ 10       │ USA            │ 12/29/2025 │
│      4 │ 1004    │ ON-LINE   │ NULL     │ Alice Brown   │ alice@a.com    │ … │ 1        │ 700        │ 0        │ ENGLAND        │ 12/28/2025 │
│      5 │ 1005    │ IN-STORE  │ EBIKE    │ NULL          │ no_name@a.com  │ … │ 1        │ 2200       │ 100      │ USA            │ 2025-12-27 │
│      6 │ 1006    │ ON-LINE   │ COMPUTER │ David Kim     │ david@a.com    │ … │ 1        │ 1500       │ NULL     │ USA            │ 31-12-25   │
│      7 │ 1007    │ IN-STORE  │ IPAD     │ Susan Clark   │ susan@a.com    │ … │ 2        │ 700        │ 20       │ CANADA         │ NULL       │
│      8 │ 1001    │ ON-LINE   │ TV       │ John Smith    │ john@a.com     │ … │ 1        │ 900        │ 50       │ USA            │ 12/31/2025 │
│      9 │ 1009    │ ON-LINE   │ WATCH    │ Rita Patel    │ rita@a.com     │ … │ 4        │ 250        │ 30       │ ENGLAND        │ 2025-12-26 │
│     10 │ 1010    │ IN-STORE  │ COMPUTER │ Omar Khan     │ omar@a.com     │ … │ 1        │ 1400       │ 0        │ USA            │ 2025-02-29 │
└────────┴─────────┴───────────┴──────────┴───────────────┴────────────────┴───┴──────────┴────────────┴──────────┴────────────────┴────────────┘
10 rows 
```

---

# Bronze Snapshot

The Bronze table still contains all 10 rows exactly as landed.

| stage              | `row_count` |
|--------------------|------------:|
| `bronze.sales_raw` | 10          |

---

# Silver Step 1 <br> Rule 7: Deduplicate exact duplicate rows

## Why first?

* If we delay deduplication, later counts can be inflated.

* Rows 1 and 8 are exact duplicates.



```sql
CREATE SCHEMA IF NOT EXISTS silver;


-- 👉 This SQL query ignores `row_id` 
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
```

## View `silver.step01_dedup`

```sql
SELECT * 
FROM  silver.step01_dedup 
ORDER by row_id;

┌────────┬─────────┬───────────┬──────────┬───────────────┬────────────────┬──────────────────┬──────────┬────────────┬──────────┬───────────────>
│ row_id │ sale_id │ sale_type │ product  │ customer_name │ customer_email │ customer_country │ quantity │ unit_price │ discount │ store_location>
│ int64  │ varchar │  varchar  │ varchar  │    varchar    │    varchar     │     varchar      │ varchar  │  varchar   │ varchar  │    varchar    >
├────────┼─────────┼───────────┼──────────┼───────────────┼────────────────┼──────────────────┼──────────┼────────────┼──────────┼───────────────>
│      1 │ 1001    │ ON-LINE   │ TV       │ John Smith    │ john@a.com     │ USA              │ 1        │ 900        │ 50       │ USA           >
│      2 │ 1002    │ IN-STORE  │ IPHONE   │ Mary Jones    │ mary@a.com     │ CANADA           │ 2        │ 1100       │ -20      │ CANADA        >
│      3 │ NULL    │ ON-LINE   │ WATCH    │ Bob Lee       │ bob@a.com      │ USA              │ 3        │ 200        │ 10       │ USA           >
│      4 │ 1004    │ ON-LINE   │ NULL     │ Alice Brown   │ alice@a.com    │ ENGLAND          │ 1        │ 700        │ 0        │ ENGLAND       >
│      5 │ 1005    │ IN-STORE  │ EBIKE    │ NULL          │ no_name@a.com  │ USA              │ 1        │ 2200       │ 100      │ USA           >
│      6 │ 1006    │ ON-LINE   │ COMPUTER │ David Kim     │ david@a.com    │ USA              │ 1        │ 1500       │ NULL     │ USA           >
│      7 │ 1007    │ IN-STORE  │ IPAD     │ Susan Clark   │ susan@a.com    │ FRANCE           │ 2        │ 700        │ 20       │ CANADA        >
│      9 │ 1009    │ ON-LINE   │ WATCH    │ Rita Patel    │ rita@a.com     │ GERMANY          │ 4        │ 250        │ 30       │ ENGLAND       >
│     10 │ 1010    │ IN-STORE  │ COMPUTER │ Omar Khan     │ omar@a.com     │ MEXICO           │ 1        │ 1400       │ 0        │ USA           >
└────────┴─────────┴───────────┴──────────┴───────────────┴────────────────┴──────────────────┴──────────┴────────────┴──────────┴───────────────>
```

---

# After Deduplication

Row 8 is removed.

| stage | row_count |
|-------|----------:|
| `bronze.sales_raw` | 10 |
| `silver.step01_dedup` | 9 |

### Rows removed
- row 8 (duplicate of row 1)

---

# Silver Step 2 — Standardize strings and prepare fields

## Why?
Before applying business rules, we normalize text and preserve raw values for safe parsing.

## Create `silver.step02_standardized`

```sql
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
```

## View `silver.step02_standardized`

```
SELECT * 
FROM silver.step02_standardized 
ORDER BY row_id;

┌────────┬─────────────┬───────────┬──────────┬───────────────┬───┬──────────┬────────────┬──────────────┬────────────────┬───────────────┐
│ row_id │ sale_id_raw │ sale_type │ product  │ customer_name │ … │ quantity │ unit_price │ discount_raw │ store_location │ sale_date_raw │
│ int64  │   varchar   │  varchar  │ varchar  │    varchar    │ … │  int32   │   double   │   varchar    │    varchar     │    varchar    │
├────────┼─────────────┼───────────┼──────────┼───────────────┼───┼──────────┼────────────┼──────────────┼────────────────┼───────────────┤
│      1 │ 1001        │ ON-LINE   │ TV       │ John Smith    │ … │        1 │      900.0 │ 50           │ USA            │ 12/31/2025    │
│      2 │ 1002        │ IN-STORE  │ IPHONE   │ Mary Jones    │ … │        2 │     1100.0 │ -20          │ CANADA         │ 2025-12-30    │
│      3 │ NULL        │ ON-LINE   │ WATCH    │ Bob Lee       │ … │        3 │      200.0 │ 10           │ USA            │ 12/29/2025    │
│      4 │ 1004        │ ON-LINE   │ NULL     │ Alice Brown   │ … │        1 │      700.0 │ 0            │ ENGLAND        │ 12/28/2025    │
│      5 │ 1005        │ IN-STORE  │ EBIKE    │ NULL          │ … │        1 │     2200.0 │ 100          │ USA            │ 2025-12-27    │
│      6 │ 1006        │ ON-LINE   │ COMPUTER │ David Kim     │ … │        1 │     1500.0 │ NULL         │ USA            │ 31-12-25      │
│      7 │ 1007        │ IN-STORE  │ IPAD     │ Susan Clark   │ … │        2 │      700.0 │ 20           │ CANADA         │ NULL          │
│      9 │ 1009        │ ON-LINE   │ WATCH    │ Rita Patel    │ … │        4 │      250.0 │ 30           │ ENGLAND        │ 2025-12-26    │
│     10 │ 1010        │ IN-STORE  │ COMPUTER │ Omar Khan     │ … │        1 │     1400.0 │ 0            │ USA            │ 2025-02-29    │
└────────┴─────────────┴───────────┴──────────┴───────────────┴───┴──────────┴────────────┴──────────────┴────────────────┴───────────────┘
  9 rows     
```


# Silver Step 3 — Rule 4: Fix discount values

## Business rule

* Null, missing, or negative discount becomes `0.00`.

## Affected rows
- row 2: discount = `-20`
- row 6: discount = missing


## Create `silver.step03_discount_fixed`

```sql
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
```

## View `silver.step03_discount_fixed`

```sql
SELECT * 
FROM silver.step03_discount_fixed 
ORDER BY row_id;

┌────────┬─────────────┬───────────┬──────────┬───────────────┬───┬──────────────┬────────────────┬───────────────┬──────────────┬──────────┐
│ row_id │ sale_id_raw │ sale_type │ product  │ customer_name │ … │ discount_raw │ store_location │ sale_date_raw │ discount_num │ discount │
│ int64  │   varchar   │  varchar  │ varchar  │    varchar    │ … │   varchar    │    varchar     │    varchar    │    double    │  double  │
├────────┼─────────────┼───────────┼──────────┼───────────────┼───┼──────────────┼────────────────┼───────────────┼──────────────┼──────────┤
│      1 │ 1001        │ ON-LINE   │ TV       │ John Smith    │ … │ 50           │ USA            │ 12/31/2025    │         50.0 │     50.0 │
│      2 │ 1002        │ IN-STORE  │ IPHONE   │ Mary Jones    │ … │ -20          │ CANADA         │ 2025-12-30    │        -20.0 │      0.0 │
│      3 │ NULL        │ ON-LINE   │ WATCH    │ Bob Lee       │ … │ 10           │ USA            │ 12/29/2025    │         10.0 │     10.0 │
│      4 │ 1004        │ ON-LINE   │ NULL     │ Alice Brown   │ … │ 0            │ ENGLAND        │ 12/28/2025    │          0.0 │      0.0 │
│      5 │ 1005        │ IN-STORE  │ EBIKE    │ NULL          │ … │ 100          │ USA            │ 2025-12-27    │        100.0 │    100.0 │
│      6 │ 1006        │ ON-LINE   │ COMPUTER │ David Kim     │ … │ NULL         │ USA            │ 31-12-25      │         NULL │      0.0 │
│      7 │ 1007        │ IN-STORE  │ IPAD     │ Susan Clark   │ … │ 20           │ CANADA         │ NULL          │         20.0 │     20.0 │
│      9 │ 1009        │ ON-LINE   │ WATCH    │ Rita Patel    │ … │ 30           │ ENGLAND        │ 2025-12-26    │         30.0 │     30.0 │
│     10 │ 1010        │ IN-STORE  │ COMPUTER │ Omar Khan     │ … │ 0            │ USA            │ 2025-02-29    │          0.0 │      0.0 │
└────────┴─────────────┴───────────┴──────────┴───────────────┴───┴──────────────┴────────────────┴───────────────┴──────────────┴──────────┘
  9 rows 
```

---

# Discount Before → After

| row_id | discount_raw | discount |
|-------:|--------------|---------:|
| 1      | 50           | 50       |
| 2      | -20          | 0        |
| 3      | 10           | 10       |
| 4      | 0            | 0        |
| 5      | 100          | 100      |
| 6      | NULL         | 0        |
| 7      | 20           | 20       |
| 9      | 30           | 30       |
| 10     | 0            | 0        |

---

# Silver Step 4 — Rules 5 and 6: Parse sale_date

## Business rule
Only these formats are valid:

- `MM/DD/YYYY`
- `YYYY-MM-DD`

## Affected rows
- row 6: `31-12-25` → invalid format
- row 7: missing date
- row 10: `2025-02-29` → invalid calendar date

---

## Create `silver.step04_date_parsed`

```sql
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
```

## View `silver.step04_date_parsed`

```sql
SELECT * 
FROM silver.step04_date_parsed 
ORDER BY row_id;

┌────────┬─────────────┬───────────┬──────────┬───────────────┬───┬────────────────┬───────────────┬──────────────┬──────────┬────────────┐
│ row_id │ sale_id_raw │ sale_type │ product  │ customer_name │ … │ store_location │ sale_date_raw │ discount_num │ discount │ sale_date  │
│ int64  │   varchar   │  varchar  │ varchar  │    varchar    │ … │    varchar     │    varchar    │    double    │  double  │    date    │
├────────┼─────────────┼───────────┼──────────┼───────────────┼───┼────────────────┼───────────────┼──────────────┼──────────┼────────────┤
│      1 │ 1001        │ ON-LINE   │ TV       │ John Smith    │ … │ USA            │ 12/31/2025    │         50.0 │     50.0 │ 2025-12-31 │
│      2 │ 1002        │ IN-STORE  │ IPHONE   │ Mary Jones    │ … │ CANADA         │ 2025-12-30    │        -20.0 │      0.0 │ 2025-12-30 │
│      3 │ NULL        │ ON-LINE   │ WATCH    │ Bob Lee       │ … │ USA            │ 12/29/2025    │         10.0 │     10.0 │ 2025-12-29 │
│      4 │ 1004        │ ON-LINE   │ NULL     │ Alice Brown   │ … │ ENGLAND        │ 12/28/2025    │          0.0 │      0.0 │ 2025-12-28 │
│      5 │ 1005        │ IN-STORE  │ EBIKE    │ NULL          │ … │ USA            │ 2025-12-27    │        100.0 │    100.0 │ 2025-12-27 │
│      6 │ 1006        │ ON-LINE   │ COMPUTER │ David Kim     │ … │ USA            │ 31-12-25      │         NULL │      0.0 │ NULL       │
│      7 │ 1007        │ IN-STORE  │ IPAD     │ Susan Clark   │ … │ CANADA         │ NULL          │         20.0 │     20.0 │ NULL       │
│      9 │ 1009        │ ON-LINE   │ WATCH    │ Rita Patel    │ … │ ENGLAND        │ 2025-12-26    │         30.0 │     30.0 │ 2025-12-26 │
│     10 │ 1010        │ IN-STORE  │ COMPUTER │ Omar Khan     │ … │ USA            │ 2025-02-29    │          0.0 │      0.0 │ NULL       │
└────────┴─────────────┴───────────┴──────────┴───────────────┴───┴────────────────┴───────────────┴──────────────┴──────────┴────────────┘
  9 rows    15 columns (10 shown)
```

## ✅ 1. Debuggable (VERY IMPORTANT)

```
SELECT sale_date_raw, 
       sale_date
FROM silver.step04_date_parsed
WHERE sale_date IS NULL;

┌───────────────┬───────────┐
│ sale_date_raw │ sale_date │
│    varchar    │   date    │
├───────────────┼───────────┤
│ 2025-02-29    │ NULL      │
│ 31-12-25      │ NULL      │
│ NULL          │ NULL      │
└───────────────┴───────────┘
```

✅ What the result proves:

```
sale_date_raw        → sale_date
--------------------------------
2025-02-29           → NULL ✔ (invalid date)
31-12-25             → NULL ✔ (invalid format)
NULL                 → NULL ✔ (missing)
```

---

# Date Parsing Before → After

| `row_id` | `sale_date_raw` | `sale_date`  |
|---------:|-----------------|--------------|
| 1        | `12/31/2025`    | `2025-12-31` |
| 2        | `2025-12-30`    | `2025-12-30` |
| 3        | `12/29/2025`    | `2025-12-29` |
| 4        | `12/28/2025`    | `2025-12-28` |
| 5        | `2025-12-27`    | `2025-12-27` |
| 6        | `31-12-25`      | `NULL`       |
| 7        | `NULL`          | `NULL`       |
| 9        | `2025-12-26`    | `2025-12-26` |
| 10       | `2025-02-29`    | `NULL`       |

---

# Silver Step 5 — Rules 2, 3, and 6: Reject invalid rows

## Business rule
Reject rows where:

- `product` is missing
- `customer_name` is missing/empty
- `sale_date` is missing or invalid

## Important
Rejected rows are **not cancelled**.

---

## Create `silver.rejected_records`

```sql
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
```

## View `silver.rejected_records`

```
SELECT * 
FROM silver.rejected_records 
ORDER BY row_id;

┌────────┬─────────────┬───────────┬──────────┬───────────────┬───┬───────────────┬──────────────┬──────────┬────────────┬───────────────────────┐
│ row_id │ sale_id_raw │ sale_type │ product  │ customer_name │ … │ sale_date_raw │ discount_num │ discount │ sale_date  │     reject_reason     │
│ int64  │   varchar   │  varchar  │ varchar  │    varchar    │ … │    varchar    │    double    │  double  │    date    │        varchar        │
├────────┼─────────────┼───────────┼──────────┼───────────────┼───┼───────────────┼──────────────┼──────────┼────────────┼───────────────────────┤
│      4 │ 1004        │ ON-LINE   │ NULL     │ Alice Brown   │ … │ 12/28/2025    │          0.0 │      0.0 │ 2025-12-28 │ REJECT_MISSING_PRODU… │
│      5 │ 1005        │ IN-STORE  │ EBIKE    │ NULL          │ … │ 2025-12-27    │        100.0 │    100.0 │ 2025-12-27 │ REJECT_MISSING_CUSTO… │
│      6 │ 1006        │ ON-LINE   │ COMPUTER │ David Kim     │ … │ 31-12-25      │         NULL │      0.0 │ NULL       │ REJECT_INVALID_OR_MI… │
│      7 │ 1007        │ IN-STORE  │ IPAD     │ Susan Clark   │ … │ NULL          │         20.0 │     20.0 │ NULL       │ REJECT_INVALID_OR_MI… │
│     10 │ 1010        │ IN-STORE  │ COMPUTER │ Omar Khan     │ … │ 2025-02-29    │          0.0 │      0.0 │ NULL       │ REJECT_INVALID_OR_MI… │
└────────┴─────────────┴───────────┴──────────┴───────────────┴───┴───────────────┴──────────────┴──────────┴────────────┴───────────────────────┘
  5 rows                                          use .last to show entire result                                          16 columns (10 shown)
sales_10_
```
---

# Rejected Rows

| row_id | reason |
|-------:|--------|
| 4      | `REJECT_MISSING_PRODUCT` |
| 5      | `REJECT_MISSING_CUSTOMER_NAME` |
| 6      | `REJECT_INVALID_OR_MISSING_SALE_DATE` |
| 7      | `REJECT_INVALID_OR_MISSING_SALE_DATE` |
| 10.    | `REJECT_INVALID_OR_MISSING_SALE_DATE` |

### Rejected count = 5

---

# Silver Step 6 — Rule 1: Capture cancelled transactions

## Business rule

* Missing `sale_id` means **cancelled transaction**.

## Important
A row counts as cancelled only if it is otherwise valid.

That means row 3 is cancelled because:

- `sale_id` is missing
- product exists
- customer_name exists
- sale_date is valid

## Create `silver.cancelled_transactions`

```sql
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
```

## View `silver.cancelled_transactions`

```
SELECT * 
FROM silver.cancelled_transactions 
ORDER BY row_id;

┌────────┬─────────────┬───────────┬─────────┬───────────────┬───┬────────────────┬───────────────┬──────────────┬──────────┬────────────┐
│ row_id │ sale_id_raw │ sale_type │ product │ customer_name │ … │ store_location │ sale_date_raw │ discount_num │ discount │ sale_date  │
│ int64  │   varchar   │  varchar  │ varchar │    varchar    │ … │    varchar     │    varchar    │    double    │  double  │    date    │
├────────┼─────────────┼───────────┼─────────┼───────────────┼───┼────────────────┼───────────────┼──────────────┼──────────┼────────────┤
│      3 │ NULL        │ ON-LINE   │ WATCH   │ Bob Lee       │ … │ USA            │ 12/29/2025    │         10.0 │     10.0 │ 2025-12-29 │
└────────┴─────────────┴───────────┴─────────┴───────────────┴───┴────────────────┴───────────────┴──────────────┴──────────┴────────────┘
  1 rows                                      use .last to show entire result                                      15 columns (10 shown)
```

# Cancelled Rows

| `row_id` | `product` | `quantity` | `unit_price` | `discount` | `sale_date` |
|---------:|-----------|-----------:|-------------:|-----------:|-------------|
| `3`      | `WATCH`   | `3`        | `200`        | `10`       | `2025-12-29`|

### Cancelled count = 1

---

# Silver Step 7 — Rule 8: Build trusted sales and compute final price

## Business rule

`final_sale_price = (quantity * unit_price) - discount`

## SQL

```sql
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
```

## View `silver.sales_clean`

```sql
SELECT * 
FROM silver.sales_clean 
ORDER BY sale_id;

┌─────────┬───────────┬─────────┬───────────────┬────────────────┬───┬────────────┬──────────┬────────────┬──────────┬──────────────────┐
│ sale_id │ sale_type │ product │ customer_name │ customer_email │ … │ sale_date  │ quantity │ unit_price │ discount │ final_sale_price │
│  int32  │  varchar  │ varchar │    varchar    │    varchar     │ … │    date    │  int32   │   double   │  double  │      double      │
├─────────┼───────────┼─────────┼───────────────┼────────────────┼───┼────────────┼──────────┼────────────┼──────────┼──────────────────┤
│    1001 │ ON-LINE   │ TV      │ John Smith    │ john@a.com     │ … │ 2025-12-31 │        1 │      900.0 │     50.0 │            850.0 │
│    1002 │ IN-STORE  │ IPHONE  │ Mary Jones    │ mary@a.com     │ … │ 2025-12-30 │        2 │     1100.0 │      0.0 │           2200.0 │
│    1009 │ ON-LINE   │ WATCH   │ Rita Patel    │ rita@a.com     │ … │ 2025-12-26 │        4 │      250.0 │     30.0 │            970.0 │
└─────────┴───────────┴─────────┴───────────────┴────────────────┴───┴────────────┴──────────┴────────────┴──────────┴──────────────────┘
  3 rows                                    
```


# Trusted Silver Rows

These rows survive all rules and are not cancelled:

| `sale_id` | `product`  | `quantity` | `unit_price` | `discount` | `final_sale_price` |
|-----------|------------|------------|--------------|------------|--------------------|
| 1001      | TV         | 1          | 900          | 50         | 850                |
| 1002      | IPHONE     | 2          | 1100         | 0          | 2200               |
| 1009      | WATCH      | 4          | 250          | 30         | 970                |

### Trusted count = 3

---

# Funnel SQL

```sql
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
       COUNT(*) FROM 
silver.sales_clean;
```


# End-to-End Funnel

| `stage` | `row_count` |
|-------|----------:|
| `bronze.sales_raw` | 10 |
| `after_dedup` | 9 |
| `rejected_records` | 5 |
| `cancelled_transactions` | 1 |
| `trusted_sales_clean` | 3 |

This funnel is one of the best teaching visuals in a medallion pipeline.

---

# Gold Layer — Why only trusted rows?

Gold is for:

- analytics
- BI dashboards
- business decisions

NOTES:

* If Gold included rejected or cancelled rows, reports would be misleading.

* So Gold is built only from `silver.sales_clean`.

---

# Gold Example — Customer Dimension

From the 3 trusted rows, we create a dimension:

```sql
CREATE SCHEMA IF NOT EXISTS gold;

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
```

## View `gold.dim_customer`

```sql
SELECT * 
FROM gold.dim_customer;

┌──────────────┬───────────────┬────────────────┬──────────────────┐
│ customer_key │ customer_name │ customer_email │ customer_country │
│    int64     │    varchar    │    varchar     │     varchar      │
├──────────────┼───────────────┼────────────────┼──────────────────┤
│            1 │ John Smith    │ john@a.com     │ USA              │
│            2 │ Mary Jones    │ mary@a.com     │ CANADA           │
│            3 │ Rita Patel    │ rita@a.com     │ GERMANY          │
└──────────────┴───────────────┴────────────────┴──────────────────┘
```

# Gold Example — Product Dimension

```sql
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
```

## View `gold.dim_product`

```sql
SELECT * 
FROM gold.dim_product;

┌─────────────┬─────────┐
│ product_key │ product │
│    int64    │ varchar │
├─────────────┼─────────┤
│           1 │ IPHONE  │
│           2 │ TV      │
│           3 │ WATCH   │
└─────────────┴─────────┘
```
---

# Gold Example — Fact Table

```
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
    ON s.product = p.product;
```

## View `gold.fact_sales`

```sql
SELECT * 
FROM gold.fact_sales;

┌─────────┬──────────────┬─────────────┬──────────┬────────────┬──────────┬──────────────────┐
│ sale_id │ customer_key │ product_key │ quantity │ unit_price │ discount │ final_sale_price │
│  int32  │    int64     │    int64    │  int32   │   double   │  double  │      double      │
├─────────┼──────────────┼─────────────┼──────────┼────────────┼──────────┼──────────────────┤
│    1001 │            1 │           2 │        1 │      900.0 │     50.0 │            850.0 │
│    1002 │            2 │           1 │        2 │     1100.0 │      0.0 │           2200.0 │
│    1009 │            3 │           3 │        4 │      250.0 │     30.0 │            970.0 │
└─────────┴──────────────┴─────────────┴──────────┴────────────┴──────────┴──────────────────┘
``` 

---

# What students should notice

1. Deduplication happens before analytics.
2. Rejected rows and cancelled rows are different categories.
3. Discount cleanup happens before final price calculation.
4. Date parsing must happen before rejecting bad dates.
5. Only trusted Silver rows become Gold rows.

This is the logic of a real data warehouse.

---

# Instructor Notes

## Ask students:
- Why is row 3 cancelled but row 4 rejected?
- Why is row 6 rejected even though discount was fixed successfully?
- Why should row 8 disappear before revenue analysis?
- Why does row 10 fail even though the format looks valid?

These are strong discussion questions.

---

# Final Takeaway

This 10-row case study shows the full medallion story:

- Bronze preserves the source
- Silver applies business rules step-by-step
- Gold contains only trusted analytics-ready data

This is exactly how messy business data becomes reliable business insight.
