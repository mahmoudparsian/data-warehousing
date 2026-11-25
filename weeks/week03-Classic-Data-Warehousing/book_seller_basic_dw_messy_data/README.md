# Book Seller → Star Schema (Messy Data)
### Week 3, Session 2 demo · the same steps as [Lab 3.2](../labs/week_03_lab_02_student.md)

The same book seller as the [clean-data demo](../book_seller_basic_dw_clean_data/), one year later, but this time the export is **messy**.
The demo notebook cleans it in clear steps (**Bronze → Silver → Gold**), builds a star schema, proves that no row was lost, and answers
10 business questions.

## What you learn

1. **profile** raw data before changing it, and turn each problem into a rule: **fix**, **default** or **reject**
2. apply the rules in the **right order** (deduplicate before filling defaults)
3. deduplicate a **dimension** (exact copies) differently from a **fact table** (one row per transaction id)
4. build a star schema with a surrogate key (`location_id`) and validate it
5. **reconcile**: raw rows = loaded + rejected + duplicates removed

## The operational tables (`data/`)

| File | Rows | One row = | Columns |
|---|---:|---|---|
| `sales.csv` | 21,000 | one transaction (2024) | `transaction_id`, `book_id`, `sale_type` (ONLINE / INSTORE), `date_sold`, `year_sold`, `customer_gender` (MALE / FEMALE), `sale_price`, `discount`, `final_price` (should be `sale_price - discount`), `country_sold` (5 countries), `city_sold` (20 cities), `book_format` (`hard_copy` / `paperback` / `soft_copy`) |
| `books.csv` | 120 | one book (in theory) | `book_id`, `book_title`, `book_genre` (5 genres), `author_id`, `author_name`, `author_gender`, `author_web_site`, `published_date`, `publisher` (Penguin, Prentice Hall, O'Reilly) |

## The pipeline in the notebook

| Layer | Tables |
|---|---|
| 🟫 Bronze (as received) | `bronze_books`, `bronze_sales` |
| ⚪ Silver (cleaned) | `silver_books` · `silver_sales_step1` (reject) → `silver_sales` (dates) → `silver_sales_clean` (one row per transaction, defaults, recomputed `final_price`) |
| 🟡 Gold (star schema) | `fact_sales` (grain: one transaction) + `dim_book`, `dim_location` (surrogate key), `dim_date` |

## Files

| File | What it is |
|---|---|
| `data/books.csv`, `data/sales.csv` | the 2 messy operational tables |
| `dw_notebook.py` | the demo (Marimo). Run `marimo edit dw_notebook.py` from this folder |

What exactly is wrong with the data? Try to find out yourself first: that is [Lab 3.2](../labs/week_03_lab_02_student.md). The notebook's Cell 2 shows the answer.
