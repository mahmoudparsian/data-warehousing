# Book Seller → Star Schema (Clean Data)
### First data-warehousing demo · Week 3, Session 1 · used in [Lab 3.1](../labs/week_03_lab_01_student.md)

A book seller sells books in 5 countries, online and in store. Its operational (OLTP) system has **2 tables**.
This demo turns them into a **star schema** and answers **10 business questions** on it.
The data is **clean on purpose**, so we can focus on modeling; the [messy-data demo](../book_seller_basic_dw_messy_data/) adds the cleaning.

## What you learn

1. read an operational schema and find its **grain** (one row of `sales` = **one transaction** = one book sold)
2. split it into **dimensions** (who / what / where / when / how) and a **fact table** (the measures)
3. give dimensions **surrogate keys** (`location_id`, `date_id`, `format_id`)
4. **validate** the star against the source: rows, totals, keys
5. answer business questions with `SUM(measure)` + `GROUP BY` dimension columns

## The operational tables (`data/`)

| File | Rows | One row = | Columns |
|---|---:|---|---|
| `sales.csv` | 10,000 | one transaction (2024-01-01 → 2025-12-31) | `transaction_id`, `book_id`, `sale_type` (ONLINE / INSTORE), `date_sold`, `year_sold`, `month_sold`, `day_sold`, `sale_price`, `discount`, `final_price` (= `sale_price - discount`), `country_sold` (5), `city_sold` (15), `hard_copy`, `paperback`, `soft_copy` (BOOLEAN, exactly one is true) |
| `books.csv` | 100 | one book | `book_id`, `book_title`, `book_genre` (10 genres), `author_id`, `author_name`, `author_web_site`, `published_date` |

## The star schema

```text
                 dim_location (15)
                        |
   dim_book (100) — fact_sales (10,000) — dim_date (731)
                        |
                 dim_book_format (3)
```

| Table | Key | Built from | Contents |
|---|---|---|---|
| `fact_sales` | `transaction_id` | `sales` | keys `book_id`, `location_id`, `date_id`, `format_id`; `sale_type`; measures `quantity_sold` (always 1), `sale_price`, `discount`, `final_price` |
| `dim_book` | `book_id` (natural key) | `books` | title, genre, author |
| `dim_location` | `location_id` (surrogate) | distinct (`country_sold`, `city_sold`) | country, city |
| `dim_date` | `date_id` (surrogate) | distinct `date_sold` | date, year, month, day, weekday, quarter |
| `dim_book_format` | `format_id` (surrogate) | the 3 BOOLEAN columns | HARDCOPY / PAPERBACK / SOFTCOPY |

**Validation:** 10,000 rows in `sales` = 10,000 in `fact_sales`; revenue 255,735.44 in both; 0 fact rows without dimension keys.

## Highlights of the 10 business questions

- **Genre:** Fantasy earns the most (46,454) because it has 20 of the 100 books; Data Science has the highest average sale (41.72).
- **Format:** hard copy earns 44% of revenue, but the 3 formats sell almost the same number of copies; hard copies are simply more expensive.
- **Countries, channels, weekdays, months:** all close to equal (countries within 4%, ONLINE 49% / INSTORE 51%). In this data, *what* is sold matters more than *where* or *when*.

## Files

| File | What it is |
|---|---|
| `data/books.csv`, `data/sales.csv` | the 2 operational tables |
| `book_seller_to_star_schema.py` | the demo (Marimo): load → star schema → validation → 10 BI questions with charts. Run `marimo edit book_seller_to_star_schema.py` from this folder |
