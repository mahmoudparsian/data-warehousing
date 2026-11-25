---
title: Medallion Architecture at Scale — 21,000 Messy Book Sales
marp: true
paginate: true
theme: gaia
class: lead
style: |
  section {
    justify-content: flex-start;
    font-size: 22px;
    line-height: 1.3;
  }
  pre code {
    font-size: 16px;
    line-height: 1.2;
  }
---

# 🧠 Medallion Architecture at Scale
## The same three layers on 21,000 messy book sales

Worked example 2 (after the [10-row case study](case_study_10_rows/)). Data: the week 3 [messy book seller](../week03-Classic-Data-Warehousing/book_seller_basic_dw_messy_data/).
Week 3 cleaned it with classic ETL; now every step is a **layer**, every row has a **fate**, and the result **reconciles**.

---

# 🥉🥈🥇 Three Layers (Reminder)

| Layer | Holds | Here |
|---|---|---|
| 🟫 Bronze | the files **as received** (all text) + lineage | `bronze.sales_raw`, `bronze.books_raw` |
| ⚪ Silver | typed, standardized, **rules applied**; every row valid, flagged, rejected or duplicate | `silver.sales`, `silver.rejected`, `silver.books` |
| 🟡 Gold | shaped for business questions | `gold.fact_sales`, `gold.dim_book`, `gold.dim_location`, `gold.dim_date`, `gold.revenue_by_genre` |

**Three** layers; dashboards and BI tools are **consumers** of Gold. Definitions: [Medallion in a nutshell](Medallion_Architecture_in_a_Nutshell.md).

---

# 🟫 Bronze: Land Both Files As Received

```sql
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

CREATE OR REPLACE TABLE bronze.sales_raw AS
SELECT *, 'sales.csv' AS _source_file, current_timestamp AS _ingested_at
FROM read_csv('../week03-Classic-Data-Warehousing/book_seller_basic_dw_messy_data/data/sales.csv', all_varchar = true);

CREATE OR REPLACE TABLE bronze.books_raw AS
SELECT *, 'books.csv' AS _source_file, current_timestamp AS _ingested_at
FROM read_csv('../week03-Classic-Data-Warehousing/book_seller_basic_dw_messy_data/data/books.csv', all_varchar = true);

SELECT 'bronze.sales_raw' AS table_name, COUNT(*) AS n_rows FROM bronze.sales_raw
UNION ALL SELECT 'bronze.books_raw', COUNT(*) FROM bronze.books_raw;
```

<!-- RESULT -->

| table_name       | n_rows |
|------------------|-------:|
| bronze.sales_raw |  21000 |
| bronze.books_raw |    120 |

*(2 rows)*

<!-- /RESULT -->

All text, nothing converted, nothing removed: this is the copy we can always replay from.

---

# 🔍 Profile Bronze (Look, Don't Touch)

```sql
SELECT COUNT(*)                                                         AS n_rows,
       COUNT(*) FILTER (WHERE transaction_id IS NULL)                   AS no_id,
       COUNT(transaction_id) - COUNT(DISTINCT transaction_id)           AS repeated_ids,
       COUNT(*) FILTER (WHERE discount IS NULL)                         AS null_discount,
       COUNT(*) FILTER (WHERE book_format IS NULL)                      AS null_format,
       COUNT(*) FILTER (WHERE date_sold NOT LIKE '____-__-__')          AS non_iso_dates,
       COUNT(*) FILTER (WHERE ABS(final_price::DOUBLE
                 - (sale_price::DOUBLE - discount::DOUBLE)) > 0.01)     AS wrong_final_price
FROM bronze.sales_raw;
```

<!-- RESULT -->

| n_rows | no_id | repeated_ids | null_discount | null_format | non_iso_dates | wrong_final_price |
|-------:|------:|-------------:|--------------:|------------:|--------------:|------------------:|
|  21000 |   100 |          900 |           300 |         200 |         14046 |             20692 |

*(1 row)*

<!-- /RESULT -->

Profiling **reads** Bronze. Each number becomes a business rule (next slide), applied in Silver.

---

# 📋 Business Rules → Fates

| # | Rule | Fate |
|---|---|---|
| S1 | no `transaction_id` → cannot be tracked | **rejected** → `silver.rejected` |
| S2 | the same `transaction_id` more than once → keep the **most complete** copy | **duplicate** (removed, counted) |
| S3 | `date_sold` in 3 formats (`YYYY-MM-DD`, `YYYY/MM/DD`, `MM/DD/YYYY`) → one `DATE` | fixed |
| S4 | NULL `discount` → 0.00; NULL `book_format` → `hard_copy` (**after** S2) | fixed |
| S5 | `final_price` from the source is wrong → recompute `sale_price - discount` | fixed |
| B1 | the same book row more than once | **duplicate** |

No rule flags anything in this data (no "cancelled" status here): **flagged = 0**. The rule order matters: S2 before S4,
or a guessed 0.00 discount can win over the real one (week 3).

---

# ⚪ Silver: Quarantine Rows Without an Id (S1)

```sql
CREATE OR REPLACE TABLE silver.rejected AS
SELECT *, 'S1 missing transaction_id' AS reject_reason
FROM bronze.sales_raw
WHERE transaction_id IS NULL;

SELECT reject_reason, COUNT(*) AS n_rows FROM silver.rejected GROUP BY ALL;
```

<!-- RESULT -->

| reject_reason             | n_rows |
|---------------------------|-------:|
| S1 missing transaction_id |    100 |

*(1 row)*

<!-- /RESULT -->

Kept with the reason, not deleted: the source team gets the list, and the reconciliation counts them.

---

# ⚪ Silver: Type, Parse, One Row per Sale (S2–S5)

```sql
CREATE OR REPLACE TABLE silver.sales AS
WITH typed AS (
  SELECT CAST(transaction_id::DOUBLE AS INTEGER)        AS transaction_id,
         book_id::INTEGER                               AS book_id,
         UPPER(TRIM(sale_type))                         AS sale_type,
         CASE WHEN date_sold LIKE '____-__-__' THEN try_strptime(date_sold, '%Y-%m-%d')
              WHEN date_sold LIKE '____/__/__' THEN try_strptime(date_sold, '%Y/%m/%d')
              WHEN date_sold LIKE '__/__/____' THEN try_strptime(date_sold, '%m/%d/%Y')
         END::DATE                                      AS date_sold,                     -- S3
         UPPER(TRIM(customer_gender))                   AS customer_gender,
         sale_price::DECIMAL(10, 2)                     AS sale_price,
         discount::DECIMAL(10, 2)                       AS discount,
         country_sold, city_sold, book_format, _source_file
  FROM bronze.sales_raw
  WHERE transaction_id IS NOT NULL                                                         -- S1 rows are in silver.rejected
),
one_per_sale AS (
  SELECT * FROM typed
  QUALIFY ROW_NUMBER() OVER (PARTITION BY transaction_id
                             ORDER BY (discount IS NULL)::INT + (book_format IS NULL)::INT) = 1   -- S2
)
SELECT * EXCLUDE (discount, book_format),
       COALESCE(discount, 0.00)                        AS discount,                         -- S4
       COALESCE(book_format, 'hard_copy')              AS book_format,                      -- S4
       sale_price - COALESCE(discount, 0.00)           AS final_price                       -- S5
FROM one_per_sale;

SELECT COUNT(*) AS n_rows, COUNT(DISTINCT transaction_id) AS n_ids,
       COUNT(*) FILTER (WHERE date_sold IS NULL) AS unparsed_dates, SUM(final_price) AS revenue
FROM silver.sales;
```

<!-- RESULT -->

| n_rows | n_ids | unparsed_dates |   revenue |
|-------:|------:|---------------:|----------:|
|  20000 | 20000 |              0 | 547552.98 |

*(1 row)*

<!-- /RESULT -->

---

# ⚪ Silver: The Books (B1)

```sql
CREATE OR REPLACE TABLE silver.books AS
SELECT DISTINCT book_id::INTEGER AS book_id, book_title, book_genre, author_id::INTEGER AS author_id,
       author_name, author_gender, author_web_site, published_date::DATE AS published_date, publisher
FROM bronze.books_raw;

SELECT (SELECT COUNT(*) FROM bronze.books_raw) AS bronze_rows,
       COUNT(*)                                AS silver_rows,
       COUNT(DISTINCT book_id)                 AS distinct_ids
FROM silver.books;
```

<!-- RESULT -->

| bronze_rows | silver_rows | distinct_ids |
|------------:|------------:|-------------:|
|         120 |         100 |          100 |

*(1 row)*

<!-- /RESULT -->

The 20 extra book rows were **exact** copies, so `DISTINCT` is enough here; the sales needed the "most complete copy" rule.

---

# ⚖️ Reconcile Both Tables

```sql
SELECT 'sales' AS source,
       (SELECT COUNT(*) FROM bronze.sales_raw)     AS bronze_rows,
       (SELECT COUNT(*) FROM silver.sales)         AS valid,
       0                                           AS flagged,
       (SELECT COUNT(*) FROM silver.rejected)      AS rejected,
       (SELECT COUNT(*) FROM bronze.sales_raw) - (SELECT COUNT(*) FROM silver.sales)
         - (SELECT COUNT(*) FROM silver.rejected)  AS duplicates
UNION ALL
SELECT 'books', (SELECT COUNT(*) FROM bronze.books_raw), (SELECT COUNT(*) FROM silver.books), 0, 0,
       (SELECT COUNT(*) FROM bronze.books_raw) - (SELECT COUNT(*) FROM silver.books);
```

<!-- RESULT -->

| source | bronze_rows | valid | flagged | rejected | duplicates |
|--------|------------:|------:|--------:|---------:|-----------:|
| sales  |       21000 | 20000 |       0 |      100 |        900 |
| books  |         120 |   100 |       0 |        0 |         20 |

*(2 rows)*

<!-- /RESULT -->

**Sales: 21,000 = 20,000 valid + 0 flagged + 100 rejected + 900 duplicates.** Books: 120 = 100 + 20 duplicates.
Check: the 900 duplicates match the 900 repeated ids found by the Bronze profile.

---

# 🟡 Gold: the Star Schema (Built Only from Silver)

```sql
CREATE OR REPLACE TABLE gold.dim_book AS
SELECT book_id, book_title, book_genre, author_name, publisher FROM silver.books;

CREATE OR REPLACE TABLE gold.dim_location AS
SELECT ROW_NUMBER() OVER (ORDER BY country_sold, city_sold) AS location_key, country_sold AS country, city_sold AS city
FROM (SELECT DISTINCT country_sold, city_sold FROM silver.sales);

CREATE OR REPLACE TABLE gold.dim_date AS
SELECT strftime(d, '%Y%m%d')::INTEGER AS date_key, d AS full_date, month(d) AS month, monthname(d) AS month_name
FROM (SELECT DISTINCT date_sold AS d FROM silver.sales);

CREATE OR REPLACE TABLE gold.fact_sales AS
SELECT s.transaction_id, s.book_id, l.location_key, strftime(s.date_sold, '%Y%m%d')::INTEGER AS date_key,
       s.sale_type, s.book_format, s.sale_price, s.discount, s.final_price
FROM silver.sales AS s
JOIN gold.dim_location AS l ON l.country = s.country_sold AND l.city = s.city_sold;

SELECT (SELECT COUNT(*) FROM gold.fact_sales)       AS fact_rows,
       (SELECT SUM(final_price) FROM gold.fact_sales) AS fact_revenue,
       (SELECT SUM(final_price) FROM silver.sales)  AS silver_revenue,
       (SELECT COUNT(*) FROM gold.dim_book)          AS books,
       (SELECT COUNT(*) FROM gold.dim_location)      AS locations,
       (SELECT COUNT(*) FROM gold.dim_date)          AS dates;
```

<!-- RESULT -->

| fact_rows | fact_revenue | silver_revenue | books | locations | dates |
|----------:|-------------:|---------------:|------:|----------:|------:|
|     20000 |    547552.98 |      547552.98 |   100 |        20 |   366 |

*(1 row)*

<!-- /RESULT -->

---

# 🟡 Gold: a Business Table

```sql
CREATE OR REPLACE TABLE gold.revenue_by_genre AS
SELECT b.book_genre,
       COUNT(DISTINCT b.book_id)                            AS books,
       COUNT(*)                                             AS sales,
       SUM(f.final_price)                                   AS revenue,
       ROUND(SUM(f.final_price) / COUNT(DISTINCT b.book_id)) AS revenue_per_book
FROM gold.fact_sales AS f
JOIN gold.dim_book  AS b USING (book_id)
GROUP BY b.book_genre
ORDER BY revenue DESC;

SELECT * FROM gold.revenue_by_genre;
```

<!-- RESULT -->

| book_genre   | books | sales |   revenue | revenue_per_book |
|--------------|------:|------:|----------:|-----------------:|
| Data Science |    24 |  4735 | 130087.49 |           5420.0 |
| Fiction      |    21 |  4213 | 116390.68 |           5542.0 |
| Technology   |    21 |  4121 | 112373.09 |           5351.0 |
| History      |    20 |  4124 | 112042.37 |           5602.0 |
| Business     |    14 |  2807 |  76659.35 |           5476.0 |

*(5 rows)*

<!-- /RESULT -->

Data Science earns the most because it has the most books (24): per book, every genre earns about the same.
A Gold table that answers the question **and** shows why.

---

# ⚖️ Week 3 (Classic ETL) vs Today (Medallion)

| | Week 3 demo | Today |
|---|---|---|
| Raw files | read, then cleaned in place | `bronze.*_raw`: kept, all text, with lineage |
| Rows without an id | dropped (and counted in the lab) | `silver.rejected`, with `reject_reason` |
| Rules | spread over 6 cells | one Silver step per rule, named S1–S5, B1 |
| Proof | counts in separate cells | one reconciliation per table: 21,000 = 20,000 + 0 + 100 + 900 |
| A rule changes | re-run the whole notebook from the files | re-run Silver and Gold from Bronze |
| Result | the same star schema, revenue 547,552.98 | the same star schema, revenue 547,552.98 |

**Same answer, but now every number can be explained back to a source row.**

---

# ✅ Takeaway

- Bronze: 21,000 + 120 rows, **as received**, with lineage.
- Silver: every rule a named step; every row **valid**, **flagged**, **rejected** (with a reason) or a **duplicate** (counted).
- Gold: a star schema + business tables, built only from Silver.
- **Reconcile** every table, every load.

The pizza shop (weeks 6–9) builds the same layers step by step, with new sources every week.
