---
marp: true
title: Week 3 — ETL for Data Warehousing
paginate: true
theme: default
class: lead
---

# Week 3, Session 2
## ETL for Data Warehousing

Extract → Transform → Load, then **prove** nothing was lost: one monthly load into the coffee-shop star schema, step by step

---

# 🎯 Learning Objectives

By the end of this session you can:

- explain **ETL** vs **ELT**, and where each one transforms the data
- extract a source **as text**, with lineage
- **profile** an extract and turn every problem into a **rule**: fix, default, or reject
- load **dimensions before facts**, and keep rejected rows in a **reject table**
- **reconcile**: rows in = loaded + rejected + duplicates removed

**Lab 3.2** applies the same steps to the messy book-seller sales.

---

# 🧠 What Is ETL?

**Extract** data from the sources → **Transform** it (clean, type, deduplicate, look up keys) → **Load** it into the warehouse.

```text
Source systems  →  ETL  →  Data warehouse (star schema)  →  Analytics / BI
```

![w:700](./images/etl_01.png)

- OLTP sources are **normalized**, **write-heavy**, and hold only the **current** state.
- The warehouse is **denormalized**, **read-heavy**, and keeps **history**: ETL is the bridge, run on a schedule (nightly, hourly).

---

# 🔁 ETL vs ELT

| | **ETL** | **ELT** |
|---|---|---|
| Transform | **before** loading, in a separate tool / program | **after** loading, **inside** the warehouse, in SQL |
| Raw data in the warehouse | no | yes (a staging / Bronze layer) |
| Typical | classic on-premise warehouses, Informatica, SSIS | cloud warehouses (Snowflake, BigQuery, Databricks), **DuckDB** |
| Re-run a transform | re-extract from the source | re-run SQL on the stored raw data |

![w:600](./images/ETL_vs_ELT.png)

👉 Today we work **ELT-style**: load the raw export as text, then transform with SQL. Weeks 5–9 call the raw layer **Bronze**.

---

# 🔧 Setup: the Coffee-Shop Star from Session 1

```sql
CREATE OR REPLACE TABLE dim_product AS
SELECT * FROM (VALUES (1, 10, 'Latte', 'Coffee'), (2, 11, 'Espresso', 'Coffee'), (3, 12, 'Green Tea', 'Tea'),
                      (4, 13, 'Croissant', 'Bakery'), (5, 14, 'Muffin', 'Bakery'))
     AS t(product_key, product_id, product_name, category);

CREATE OR REPLACE TABLE dim_customer AS
SELECT * FROM (VALUES (0, NULL, 'Unknown', 'Unknown'),          -- the "unknown member" row
                      (1, 1, 'Ana', 'San Jose'), (2, 2, 'Ben', 'Santa Clara'),
                      (3, 3, 'Chen', 'San Jose'), (4, 4, 'Dara', 'Palo Alto'))
     AS t(customer_key, customer_id, name, city);

CREATE OR REPLACE TABLE dim_date AS
SELECT strftime(d, '%Y%m%d')::INTEGER AS date_key, d AS full_date, year(d) AS year, month(d) AS month,
       strftime(d, '%Y-%m') AS year_month, dayname(d) AS weekday
FROM (SELECT unnest(['2026-01-05', '2026-01-21', '2026-02-02', '2026-02-20']::DATE[]) AS d);

CREATE OR REPLACE TABLE fact_sales AS
SELECT * FROM (VALUES (1001, 1, 20260105, 1, 1, 1, 4.50), (1001, 2, 20260105, 4, 1, 1, 3.25),
                      (1002, 1, 20260105, 2, 2, 2, 6.00), (1003, 1, 20260121, 1, 1, 1, 4.50),
                      (1003, 2, 20260121, 5, 1, 2, 5.50), (1004, 1, 20260202, 3, 3, 1, 3.50),
                      (1004, 2, 20260202, 4, 3, 2, 6.50), (1005, 1, 20260202, 1, 4, 2, 9.00),
                      (1006, 1, 20260220, 2, 2, 1, 3.00), (1006, 2, 20260220, 5, 2, 1, 2.75))
     AS t(order_id, line_no, date_key, product_key, customer_key, quantity, revenue);
```

January–February are loaded (10 fact rows, revenue 48.50). Now the **March** export arrives.

---

# 1️⃣ Extract: Land the Export As Text

```sql
CREATE OR REPLACE TABLE raw_pos AS
SELECT *, 'pos_export_2026_03.csv' AS _source_file, current_timestamp AS _loaded_at   -- lineage
FROM (VALUES
  ('1007', '1', '2026-03-02 08:15', 'Latte',       '1', '4.50',  '1'),
  ('1007', '2', '2026-03-02 08:15', ' croissant ', '1', '3.25',  '1'),
  ('1008', '1', '03/02/2026 12:40', 'ESPRESSO',    '2', '$3.00', '3'),
  ('1009', '1', '2026-03-04 09:05', 'Green Tea',   '1', '3.50',  '2'),
  ('1009', '1', '2026-03-04 09:05', 'Green Tea',   '1', '3.50',  '2'),
  ('1010', '1', '03/05/2026 07:55', 'Muffin',      ' ', '2.75',  '4'),
  ('1011', '1', '2026-03-06 10:30', 'Mocha',       '1', '4.75',  '1'),
  ('1012', '1', '2026-03-31 17:45', 'Latte',       '2', '4.50',  '9'),
  ('1013', '1', '2026-02-30 08:00', 'Latte',       '1', '4.50',  '2'),
  ('1014', '1', '2026-03-09 08:20', 'Latte',       '1', '4.50',  '3')
) AS t(order_id, line_no, sold_at, product, quantity, unit_price, customer_id);

SELECT COUNT(*) AS raw_rows FROM raw_pos;
```

<!-- RESULT -->

| raw_rows |
|---------:|
|       10 |

*(1 row)*

<!-- /RESULT -->

In a real pipeline: `read_csv('pos_export_*.csv', all_varchar = true, filename = true)`. **Text first**: the load never fails, Transform decides the types.

---

# 🔁 Extract: Only What Is New (Incremental)

A full reload copies **everything** again every night. An **incremental** load takes only the rows changed since the last run:

```sql no-run
SELECT *
FROM source.orders
WHERE updated_at > (SELECT MAX(loaded_until) FROM etl_log WHERE target = 'fact_sales');
```

- `etl_log` remembers how far each load got (the **watermark**).
- Week 9 builds this for the pizza shop, monthly file by monthly file.
- Today's March export is already "only March": one file per month.

---

# 2️⃣ Profile Before You Transform

```sql
SELECT COUNT(*)                                                                    AS n_rows,
       COUNT(*) - COUNT(DISTINCT (order_id, line_no))                              AS duplicate_rows,
       COUNT(*) FILTER (WHERE try_strptime(sold_at, ['%Y-%m-%d %H:%M', '%m/%d/%Y %H:%M']) IS NULL) AS bad_dates,
       COUNT(*) FILTER (WHERE TRY_CAST(NULLIF(TRIM(quantity), '') AS INTEGER) IS NULL) AS bad_quantity,
       COUNT(*) FILTER (WHERE unit_price LIKE '$%')                                AS dollar_prices,
       COUNT(*) FILTER (WHERE LOWER(TRIM(product)) NOT IN
                        (SELECT LOWER(product_name) FROM dim_product))             AS unknown_products,
       COUNT(*) FILTER (WHERE customer_id::INTEGER NOT IN
                        (SELECT customer_id FROM dim_customer WHERE customer_id IS NOT NULL)) AS unknown_customers
FROM raw_pos;
```

<!-- RESULT -->

| n_rows | duplicate_rows | bad_dates | bad_quantity | dollar_prices | unknown_products | unknown_customers |
|-------:|---------------:|----------:|-------------:|--------------:|-----------------:|------------------:|
|     10 |              1 |         1 |            1 |             1 |                1 |                 1 |

*(1 row)*

<!-- /RESULT -->

Every non-zero number needs a **rule**, agreed with the business **before** the load (next slide).

---

# 📋 From Problems to Rules

| Problem (rows) | Kind | Rule |
|---|---|---|
| `' croissant '`, `ESPRESSO` | fixable | `LOWER(TRIM(…))` before the product lookup |
| `03/02/2026 12:40` | fixable | `try_strptime` with both formats |
| `$3.00` | fixable | `REPLACE(…, '$', '')`, then `TRY_CAST` |
| 1009 line 1 sent twice | duplicate | keep **one** row per `(order_id, line_no)` |
| customer `9` not in `dim_customer` | **default** | load it with `customer_key = 0` ("Unknown"): the sale is real |
| blank quantity (1010) | **reject** | no quantity = no revenue: send to `etl_rejects` |
| product `Mocha` (1011) | **reject** | no product row yet: reject, and ask for the product master data |
| `2026-02-30` (1013) | **reject** | impossible date |

👉 Three kinds of rule: **fix** it, **default** it, **reject** it. Never **silently** drop a row.

---

# 3️⃣ Transform: Type, Look Up, Flag, Deduplicate

```sql
CREATE OR REPLACE TABLE stg_sales AS
WITH typed AS (
  SELECT r.order_id::INTEGER                                                     AS order_id,
         r.line_no::INTEGER                                                      AS line_no,
         try_strptime(r.sold_at, ['%Y-%m-%d %H:%M', '%m/%d/%Y %H:%M'])           AS sold_at,
         p.product_key,
         TRY_CAST(NULLIF(TRIM(r.quantity), '') AS INTEGER)                       AS quantity,
         TRY_CAST(REPLACE(TRIM(r.unit_price), '$', '') AS DECIMAL(6, 2))         AS unit_price,
         COALESCE(c.customer_key, 0)                                             AS customer_key
  FROM raw_pos AS r
  LEFT JOIN dim_product  AS p ON LOWER(p.product_name) = LOWER(TRIM(r.product))
  LEFT JOIN dim_customer AS c ON c.customer_id = r.customer_id::INTEGER
)
SELECT *,
       concat_ws(', ',
         CASE WHEN sold_at     IS NULL THEN 'bad date'        END,
         CASE WHEN product_key IS NULL THEN 'unknown product' END,
         CASE WHEN quantity    IS NULL THEN 'no quantity'     END) AS dq_issue
FROM typed
QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id, line_no ORDER BY sold_at) = 1;

SELECT order_id, line_no, sold_at, product_key, quantity, unit_price, customer_key, dq_issue
FROM stg_sales ORDER BY order_id, line_no;
```

<!-- RESULT -->

| order_id | line_no | sold_at             | product_key | quantity | unit_price | customer_key | dq_issue        |
|---------:|--------:|---------------------|------------:|---------:|-----------:|-------------:|-----------------|
|     1007 |       1 | 2026-03-02 08:15:00 |           1 |        1 |       4.50 |            1 |                 |
|     1007 |       2 | 2026-03-02 08:15:00 |           4 |        1 |       3.25 |            1 |                 |
|     1008 |       1 | 2026-03-02 12:40:00 |           2 |        2 |       3.00 |            3 |                 |
|     1009 |       1 | 2026-03-04 09:05:00 |           3 |        1 |       3.50 |            2 |                 |
|     1010 |       1 | 2026-03-05 07:55:00 |           5 |     NULL |       2.75 |            4 | no quantity     |
|     1011 |       1 | 2026-03-06 10:30:00 |        NULL |        1 |       4.75 |            1 | unknown product |
|     1012 |       1 | 2026-03-31 17:45:00 |           1 |        2 |       4.50 |            0 |                 |
|     1013 |       1 | NULL                |           1 |        1 |       4.50 |            2 | bad date        |
|     1014 |       1 | 2026-03-09 08:20:00 |           1 |        1 |       4.50 |            3 |                 |

*(9 rows)*

<!-- /RESULT -->

---

# 4️⃣ Load: Dimensions First, Then Facts

A fact row needs its `date_key` to exist in `dim_date`. So: **add the new dates first**.

```sql
INSERT INTO dim_date
SELECT DISTINCT strftime(sold_at, '%Y%m%d')::INTEGER, sold_at::DATE, year(sold_at), month(sold_at),
       strftime(sold_at, '%Y-%m'), dayname(sold_at)
FROM stg_sales
WHERE dq_issue = ''
  AND strftime(sold_at, '%Y%m%d')::INTEGER NOT IN (SELECT date_key FROM dim_date);

SELECT COUNT(*) AS dim_date_rows FROM dim_date;
```

<!-- RESULT -->

| dim_date_rows |
|--------------:|
|             8 |

*(1 row)*

<!-- /RESULT -->

The same order every time: **dimensions → facts**. A load that inserts facts first creates orphans, or drops rows at the next `JOIN`.

---

# 4️⃣ Load: Facts and Rejects

```sql
INSERT INTO fact_sales
SELECT order_id, line_no, strftime(sold_at, '%Y%m%d')::INTEGER, product_key, customer_key,
       quantity, quantity * unit_price
FROM stg_sales
WHERE dq_issue = '';

CREATE OR REPLACE TABLE etl_rejects AS
SELECT 'pos_export_2026_03.csv' AS source_file, order_id, line_no, dq_issue, current_timestamp AS rejected_at
FROM stg_sales
WHERE dq_issue <> '';

SELECT * EXCLUDE (rejected_at) FROM etl_rejects ORDER BY order_id;
```

<!-- RESULT -->

| source_file            | order_id | line_no | dq_issue        |
|------------------------|---------:|--------:|-----------------|
| pos_export_2026_03.csv |     1010 |       1 | no quantity     |
| pos_export_2026_03.csv |     1011 |       1 | unknown product |
| pos_export_2026_03.csv |     1013 |       1 | bad date        |

*(3 rows)*

<!-- /RESULT -->

Rejected rows are **kept**, with the reason: someone fixes them at the source, and the next load picks them up.

---

# 5️⃣ Reconcile: Prove Nothing Was Lost

```sql
SELECT (SELECT COUNT(*) FROM raw_pos)                                       AS raw_rows,
       (SELECT COUNT(*) FROM raw_pos) - (SELECT COUNT(*) FROM stg_sales)    AS duplicates_removed,
       (SELECT COUNT(*) FROM stg_sales WHERE dq_issue = '')                 AS loaded,
       (SELECT COUNT(*) FROM etl_rejects)                                   AS rejected,
       (SELECT COUNT(*) FROM fact_sales WHERE date_key >= 20260301)         AS march_fact_rows,
       (SELECT SUM(revenue) FROM fact_sales WHERE date_key >= 20260301)     AS march_revenue,
       (SELECT COUNT(*) FROM fact_sales WHERE customer_key = 0)             AS unknown_customer_rows;
```

<!-- RESULT -->

| raw_rows | duplicates_removed | loaded | rejected | march_fact_rows | march_revenue | unknown_customer_rows |
|---------:|-------------------:|-------:|---------:|----------------:|--------------:|----------------------:|
|       10 |                  1 |      6 |        3 |               6 |         30.75 |                     1 |

*(1 row)*

<!-- /RESULT -->

**10 raw = 6 loaded + 3 rejected + 1 duplicate.** If this equation fails, the load is **not** finished: find the missing rows first.

---

# 📝 Log Every Run

```sql
CREATE OR REPLACE TABLE etl_log AS
SELECT 'fact_sales'                                          AS target,
       'pos_export_2026_03.csv'                              AS source_file,
       (SELECT COUNT(*) FROM raw_pos)                        AS rows_read,
       (SELECT COUNT(*) FROM stg_sales WHERE dq_issue = '')  AS rows_loaded,
       (SELECT COUNT(*) FROM etl_rejects)                    AS rows_rejected,
       (SELECT MAX(sold_at) FROM stg_sales WHERE dq_issue = '') AS loaded_until;   -- next run's watermark

SELECT * FROM etl_log;
```

<!-- RESULT -->

| target     | source_file            | rows_read | rows_loaded | rows_rejected | loaded_until        |
|------------|------------------------|----------:|------------:|--------------:|---------------------|
| fact_sales | pos_export_2026_03.csv |        10 |           6 |             3 | 2026-03-31 17:45:00 |

*(1 row)*

<!-- /RESULT -->

The log answers "what ran, when, from which file, with how many rows": the first place to look when a number looks wrong.
Production tools add **retries**, **alerts**, and a scheduler (cron, Airflow).

---

# 🧰 Transform in SQL: Your Toolkit (Weeks 1–2)

The same Transform steps, with the functions from the SQL toolkit
([Part 1](../../week01-Foundations-SQL-for-Analytics/sql_toolkit_for_medallion/lecture_notes_03_cleaning_one_table.md) ·
[Part 2](../../week02-SQL-Analytical-Thinking-and-EDA/sql_toolkit_for_medallion/lecture_notes_03_combine_dedup_reconcile.md)):

| Step | SQL |
|---|---|
| Extract as text | `read_csv('…', all_varchar = true)` · many files: `'*.csv'`, `union_by_name = true`, `filename = true` |
| Profile | `COUNT(*) - COUNT(col)` · `COUNT(*) FILTER (WHERE …)` · `GROUP BY col` · `LIKE '__/__/____'` |
| Clean | `TRIM`, `UPPER`/`LOWER`, `REPLACE` · `COALESCE(NULLIF(TRIM(col), ''), 'Unknown')` · `CASE … ELSE 'Unknown'` |
| Type | `TRY_CAST(col AS DECIMAL(10, 2))` · `try_strptime(col, ['%Y-%m-%d', '%m/%d/%Y'])::DATE` |
| Validate | `ABS(a - b) > 0.01` · `CASE WHEN x BETWEEN lo AND hi THEN x END` · a `dq_issue` column |
| Deduplicate | `QUALIFY ROW_NUMBER() OVER (PARTITION BY key ORDER BY newest DESC) = 1` |
| Check references | `LEFT JOIN … WHERE right.key IS NULL` · `NOT EXISTS` |
| Load + reconcile | `CREATE OR REPLACE TABLE … AS` · `INSERT INTO` · rows in = loaded + rejected + duplicates · `EXCEPT` |

👉 Lab 3.2 uses these steps on messy book-seller sales.

---

# 🐍 The Same ETL in Python (pandas)

Many teams write ETL in Python. The steps do not change:

```python
import os
import pandas as pd

raw = pd.read_csv("pos_export_2026_03.csv", dtype=str)                  # Extract, as text
raw["quantity"] = pd.to_numeric(raw["quantity"].str.strip(), errors="coerce")   # Transform (like TRY_CAST)
raw["unit_price"] = pd.to_numeric(raw["unit_price"].str.replace("$", ""), errors="coerce")
raw = raw.drop_duplicates(subset=["order_id", "line_no"])                # Deduplicate
good, rejects = raw[raw["quantity"].notna()], raw[raw["quantity"].isna()]

# Load: with SQLAlchemy into MySQL/PostgreSQL. Never write a password in code:
# engine = create_engine(f"mysql+pymysql://dw_user:{os.environ['MYSQL_PASSWORD']}@localhost/dw")
# good.to_sql("fact_sales", engine, if_exists="append", index=False)
```

More examples (MySQL, PETL, Parquet): [`ETL/resources/`](resources/README.md) · the full story: [`ETL_movies_to_star_schema/`](resources/ETL_movies_to_star_schema/).

---

# 🏭 ETL in Production

| Concern | What it means | Example |
|---|---|---|
| Data-quality checks | NULL, range, format, referential checks **on every load** | today's profile query, saved as a test |
| Error handling | rejects kept with a reason; the run is logged | `etl_rejects`, `etl_log` |
| Re-runs | running a load twice must not double the data | delete-then-insert the month, or `MERGE` on the key |
| Performance | bulk loads, partitions (one per month), parallel files | `read_csv('*.csv')` reads files in parallel |
| Orchestration | run steps in order, on a schedule, with retries | cron, Airflow, Dagster, dbt |
| Tools | open source / commercial / cloud | Spark, dbt · Informatica, SSIS · AWS Glue, Azure Data Factory |

**Modern architecture:** sources → raw files in a **data lake** → ELT in SQL → **Bronze / Silver / Gold** → BI (weeks 5–9).

---

# ✅ Summary

| Step | Coffee-shop March load |
|---|---|
| Extract | 10 rows, as text, with `_source_file` |
| Profile | 1 duplicate, 1 bad date, 1 blank quantity, 1 unknown product, 1 unknown customer, 1 `$` price, 2 date formats |
| Transform | `LOWER(TRIM)`, `try_strptime`, `REPLACE` + `TRY_CAST`, lookups, `dq_issue`, `QUALIFY` |
| Load | dimensions first (`dim_date` +4 days), then 6 fact rows (30.75); 3 rows to `etl_rejects` |
| Reconcile | 10 = 6 + 3 + 1 ✅ |
| Log | `etl_log` with the watermark for the next run |

👉 Now: **Lab 3.2** (30 minutes): the same ETL on 21,000 messy book-seller sales.
