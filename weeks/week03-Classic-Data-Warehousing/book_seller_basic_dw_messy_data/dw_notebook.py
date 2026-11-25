import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Book Seller → Star Schema, with Messy Data
    ### Week 3, Session 2 demo · the same steps as Lab 3.2

    The same book seller as the clean demo, but now the sales export is **messy**: 21,000 rows from 2024, with missing ids, missing values,
    three date formats, duplicate transactions, duplicate books, and a `final_price` column that is wrong. This notebook cleans it step by step
    and builds a star schema, then answers 10 business questions.

    | Layer | Tables | Rows |
    |---|---|---|
    | 🟫 Bronze (raw, as received) | `bronze_books`, `bronze_sales` | 120 · 21,000 |
    | ⚪ Silver (cleaned, one row per entity / transaction) | `silver_books`, `silver_sales_step1` → `silver_sales` → `silver_sales_clean` | 100 · 20,900 → 20,900 → 20,000 |
    | 🟡 Gold (star schema) | `dim_book`, `dim_location`, `dim_date`, `fact_sales` | 100 · 20 · 366 · 20,000 |

    Every step has the same shape: **what** we do → the **SQL** → a **check** → the **result** in numbers.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Why three layers?

    - **Bronze** keeps the data **exactly as received**: if a rule turns out wrong, we re-run Silver from Bronze, without asking the source again.
    - **Silver** applies the cleaning rules, one step per table, so each rule can be checked on its own.
    - **Gold** is the star schema that BI queries use: no cleaning logic in reports.

    Weeks 5–9 build the same three layers for the pizza shop.
    """)
    return


@app.cell
def _():
    ## 📊 **Optional Code Cell (Visual Diagram)**

    import matplotlib.pyplot as plt

    layers = ["Bronze\n(Raw)", "Silver\n(Clean)", "Gold\n(Star Schema)", "BI\n(Insights)"]
    levels = [1, 2, 3, 4]

    plt.figure(figsize=(10,2))
    plt.barh(layers, levels)

    plt.title("Medallion Architecture Flow")
    plt.xlabel("Data Maturity Level")

    plt.show()
    return (plt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🟫 Cell 1 — Load the Raw Files (Bronze)

    Load `books.csv` and `sales.csv` as they are: no cleaning, no fixes. This is the copy we can always go back to.
    """)
    return


@app.cell
def _():
    #🧾 3. SQL + Python

    # 1. Import the Required Library
    import duckdb

    # 2. Create a DuckDB Connection Object
    con = duckdb.connect()

    # 3. Define file paths (outside SQL)
    books_path = "data/books.csv"
    sales_path = "data/sales.csv"

    # 4. Create Bronze table: `bronze_books`
    con.execute(f"""
    CREATE OR REPLACE TABLE bronze_books AS
    SELECT * FROM read_csv_auto('{books_path}')
    """).fetchall()

    # 5. Create Bronze table: `bronze_sales`
    con.execute(f"""
    CREATE OR REPLACE TABLE bronze_sales AS
    SELECT * FROM read_csv_auto('{sales_path}')
    """).fetchall()

    # 5. Validate load
    con.execute("""
    SELECT 'bronze_books' AS table_name, COUNT(*) AS row_count FROM bronze_books
    UNION ALL
    SELECT 'bronze_sales', COUNT(*) FROM bronze_sales
    """).df()
    return (con,)


@app.cell
def _(con):
    # 📊 4. Nice Plot (Row Count Overview)


    df_counts = con.execute("""
    SELECT 'bronze_books' AS table_name, COUNT(*) AS row_count FROM bronze_books
    UNION ALL
    SELECT 'bronze_sales', COUNT(*) FROM bronze_sales
    """).df()

    df_counts
    return (df_counts,)


@app.cell
def _(df_counts, plt):
    # Plot the Counts of Bronze Tables
    plt.figure(figsize=(6,4))
    plt.bar(df_counts["table_name"], df_counts["row_count"])
    plt.title("Bronze Layer Row Counts")
    plt.xlabel("Table")
    plt.ylabel("Rows")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Result:** `bronze_books` **120** rows, `bronze_sales` **21,000** rows. The shapes already tell the roles: `sales` = many events (→ fact table),
    `books` = a short descriptive list (→ dimension).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🟫 Cell 2 — Profile the Data Quality (before any cleaning)

    We **count** the problems first, then decide a rule for each one. Nothing is changed in this cell.
    """)
    return


@app.cell
def _(con):
    #🧾 3. SQL (Data Quality Checks)

    # ----------------------------------------
    # 1. Duplicate Books
    # ----------------------------------------
    dup_books = con.execute("""
    SELECT COUNT(*) AS duplicate_books
    FROM (
        SELECT book_id, book_title, book_genre,
               author_id, author_name,
               author_gender, author_web_site,
               published_date, publisher,
               COUNT(*) AS cnt
        FROM bronze_books
        GROUP BY ALL
        HAVING COUNT(*) > 1
    )
    """).df()

    dup_books
    return (dup_books,)


@app.cell
def _(con):
    # --------------------------------------------------
    # 2. NULL transaction_id (CRITICAL)
    #
    # If a sales transaction has a transaction_id of NULL
    # Then we will drop that record (business rule)
    # --------------------------------------------------
    null_tx = con.execute("""
    SELECT COUNT(*) AS null_transaction_id
    FROM bronze_sales
    WHERE transaction_id IS NULL
    """).df()

    null_tx
    return (null_tx,)


@app.cell
def _(con):
    # ----------------------------------------
    # 3. NULL book_format
    # ----------------------------------------
    null_format = con.execute("""
    SELECT COUNT(*) AS null_book_format
    FROM bronze_sales
    WHERE book_format IS NULL
    """).df()

    null_format
    return (null_format,)


@app.cell
def _(con):
    # ----------------------------------------
    # 4. NULL discount
    # ----------------------------------------
    null_discount = con.execute("""
    SELECT COUNT(*) AS null_discount
    FROM bronze_sales
    WHERE discount IS NULL
    """).df()

    null_discount
    return (null_discount,)


@app.cell
def _(con):
    # ----------------------------------------
    # 5. Mixed Date Formats
    # ----------------------------------------
    mixed_dates = con.execute("""
    SELECT COUNT(*) AS non_standard_dates
    FROM bronze_sales
    WHERE date_sold LIKE '%/%'
    """).df()

    mixed_dates
    return (mixed_dates,)


@app.cell
def _(dup_books, mixed_dates, null_discount, null_format, null_tx):
    dup_books, null_tx, null_format, null_discount, mixed_dates
    return


@app.cell
def _(dup_books, mixed_dates, null_discount, null_format, null_tx, plt):
    ## 📊 4. Nice Plot (Data Quality Dashboard)


    issues = [
        ("Duplicate Books", dup_books.iloc[0,0]),
        ("NULL Tx ID", null_tx.iloc[0,0]),
        ("NULL Format", null_format.iloc[0,0]),
        ("NULL Discount", null_discount.iloc[0,0]),
        ("Mixed Dates", mixed_dates.iloc[0,0]),
    ]

    labels = [i[0] for i in issues]
    values = [i[1] for i in issues]

    plt.figure(figsize=(10,5))
    plt.bar(labels, values)
    plt.title("Data Quality Issues in Bronze Layer")
    plt.ylabel("Count of Problematic Rows")
    plt.xticks(rotation=30)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Findings and rules

    | Problem (count) | Rule | Kind |
    |---|---|---|
    | 20 duplicate rows in `books` (120 rows, 100 ids, exact copies) | `SELECT DISTINCT` | fix |
    | 100 sales with no `transaction_id` | drop, and count them in the reconciliation | **reject** |
    | 900 `transaction_id`s that appear twice (415 exact copies, 485 copies with a NULL `discount` or `book_format`) | keep **one** row per id: the most complete copy | fix |
    | 300 NULL `discount`, 200 NULL `book_format` (all in second copies, see above) | after deduplication: discount → 0.00, format → `hard_copy` | default |
    | 14,046 dates not in `YYYY-MM-DD` (7,164 `YYYY/MM/DD`, 6,882 `MM/DD/YYYY`) | parse all three formats | fix |
    | `final_price ≠ sale_price - discount` in 20,692 rows (the source value is wrong) | recompute it | fix |

    The last row is not profiled in Cell 2: check it yourself with `ABS(final_price - (sale_price - discount)) > 0.01` (Lab 3.2, Q4).
    **Order matters:** the defaults (row 4) must come **after** the deduplication (row 3), or the guessed 0.00 can win over a real discount.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ⚪ Cell 3 — Clean the Books (Silver)

    `bronze_books` has 120 rows for 100 books: 20 rows are **exact copies**. A dimension must have **one row per key**: if book 10 appeared twice,
    every sale of book 10 would join twice and its revenue would **double**. Here `SELECT DISTINCT` is enough, because the copies are identical.
    """)
    return


@app.cell
def _(con):
    # 🧾 3. SQL

    # ----------------------------------------
    # Remove duplicate books
    # bronze_books --> silver_books
    # ----------------------------------------

    _query = """
    CREATE OR REPLACE TABLE silver_books AS
    SELECT DISTINCT *
    FROM bronze_books
    """

    con.execute(_query).fetchall()


    # Validate result
    bronze_total_books = con.execute("""
    SELECT COUNT(*) AS bronze_total_books
    FROM bronze_books
    """).df()

    bronze_total_books

    silver_total_books = con.execute("""
    SELECT COUNT(*) AS silver_total_books
    FROM silver_books
    """).df()

    (bronze_total_books, silver_total_books)
    return


@app.cell
def _(con):
    # 🔍 Extra Validation (Very Important)
    # Check duplicates are gone

    remaining_duplicates = con.execute("""
    SELECT COUNT(*) AS remaining_duplicates
    FROM (
        SELECT *,
               COUNT(*) OVER (
                   PARTITION BY book_id, book_title, book_genre,
                                author_id, author_name,
                                author_gender, author_web_site,
                                published_date, publisher
               ) AS cnt
        FROM silver_books
    )
    WHERE cnt > 1
    """).df()

    # 👉 Expected result:
    # remaining_duplicates = 0

    remaining_duplicates
    return


@app.cell
def _(con, plt):
    # 📊 4. Nice Plot (Before vs After)


    df_compare = con.execute("""
    SELECT 'bronze_books' AS stage, COUNT(*) AS rows FROM bronze_books
    UNION ALL
    SELECT 'silver_books', COUNT(*) FROM silver_books
    """).df()

    plt.figure(figsize=(6,4))
    plt.bar(df_compare["stage"], df_compare["rows"])
    plt.title("Books: Before vs After Deduplication")
    plt.ylabel("Row Count")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Result:** 120 → **100** rows, 0 duplicate ids left.

    Why not `DISTINCT` on the sales too? Two sales can legitimately have the same values (same book, same day, same price): only the
    **transaction id** tells whether two rows are the same event. Cell 6 deduplicates sales **by id**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ⚪ Cell 4 — Clean the Sales, Step 1: Reject Rows Without an Id

    - **Reject** the 100 rows with no `transaction_id`: we cannot track, deduplicate or correct a sale without its id, and inventing one would be fake data.
    - Standardize the text columns (`UPPER(TRIM(…))`).
    - **Keep** the NULL `discount` and `book_format` values for now: Cell 6 decides which copy of a transaction survives, and the complete copy must win.
    """)
    return


@app.cell
def _(con):
    # 🧾 3. SQL

    # ----------------------------------------
    # Clean sales (Step 1)
    # ----------------------------------------

    _query = """
    CREATE OR REPLACE TABLE silver_sales_step1 AS
    SELECT
        transaction_id,
        book_id,
        UPPER(TRIM(sale_type)) AS sale_type,
        date_sold,
        year_sold,
        UPPER(TRIM(customer_gender)) AS customer_gender,
        sale_price,
        discount,        -- NULLs stay for now: every NULL row is a 2nd copy of a transaction (Cell 6)
        country_sold,
        city_sold,
        book_format      -- NULLs stay for now (same reason)

    FROM bronze_sales
    WHERE transaction_id IS NOT NULL      -- rule 1: no id → reject
    """

    con.execute(_query).fetchall()

    # Validate row count
    _cleaned_rows = con.execute("""
    SELECT COUNT(*) AS cleaned_rows
    FROM silver_sales_step1
    """).df()

    _cleaned_rows
    return


@app.cell
def _(con):
    # Validation: no NULL id is left; the NULL discounts / formats are still here on purpose
    # (Cell 6 keeps the complete copy of each transaction first, and only then fills the defaults)

    validation_checks = con.execute("""
    SELECT
        SUM(CASE WHEN transaction_id IS NULL THEN 1 ELSE 0 END) AS null_tx,
        SUM(CASE WHEN discount IS NULL THEN 1 ELSE 0 END) AS null_discount,
        SUM(CASE WHEN book_format IS NULL THEN 1 ELSE 0 END) AS null_format
    FROM silver_sales_step1
    """).df()

    validation_checks

    ### 👉 Expected: 0, 300, 200
    return


@app.cell
def _(con, plt):
    # 📊 4. Nice Plot (Data Reduction)


    _df_counts = con.execute("""
    SELECT 'bronze_sales' AS stage, COUNT(*) AS rows FROM bronze_sales
    UNION ALL
    SELECT 'silver_sales_step1', COUNT(*) FROM silver_sales_step1
    """).df()

    plt.figure(figsize=(6,4))
    plt.bar(_df_counts["stage"], _df_counts["rows"])
    plt.title("Sales: Before vs After Cleaning (Step 1)")
    plt.ylabel("Row Count")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Result:** 21,000 → **20,900** rows (100 rejected). Still NULL: 300 discounts and 200 formats, on purpose.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ⚪ Cell 5 — Parse the Dates (one DATE type)

    `date_sold` arrives in three formats: `2024-10-25` (6,954 rows), `2024/10/25` (7,164) and `10/25/2024` (6,882).
    As text, `GROUP BY date_sold` would treat them as three different days. `COALESCE(TRY_STRPTIME(…, fmt1), TRY_STRPTIME(…, fmt2), …)` tries each
    format in turn and keeps the first one that works.
    """)
    return


@app.cell
def _(con):
    # 🧾 3. SQL (Date Standardization)

    # ----------------------------------------
    # Fix date formats
    #
    #  silver_sales_step1 ---> silver_sales
    # ----------------------------------------

    _query = """
    CREATE OR REPLACE TABLE silver_sales AS
    SELECT
        transaction_id,
        book_id,
        sale_type,

        -- 🔥 CORE LOGIC: parse multiple formats
        COALESCE(
            TRY_STRPTIME(date_sold, '%m/%d/%Y'),
            TRY_STRPTIME(date_sold, '%Y-%m-%d'),
            TRY_STRPTIME(date_sold, '%Y/%m/%d')
        )::DATE AS date_sold,

        year_sold,
        customer_gender,
        sale_price,
        discount,
        country_sold,
        city_sold,
        book_format

    FROM silver_sales_step1
    """

    con.execute(_query).fetchall()

    # Validate
    silver_sales_total_rows = con.execute("""
    SELECT COUNT(*) AS total_rows
    FROM silver_sales
    """).df()

    silver_sales_total_rows
    return


@app.cell
def _(con):
    # 🔍 Validation (CRITICAL)

    # Check if any dates failed parsing
    bad_dates_count = con.execute("""
    SELECT COUNT(*) AS bad_dates
    FROM silver_sales
    WHERE date_sold IS NULL
    """).df()

    ### 👉 Expected:
    ### bad_dates = 0

    bad_dates_count
    return


@app.cell
def _(con, plt):
    # 📊 4. Nice Plot (Date Distribution)


    # Query
    df_dates = con.execute("""
    SELECT
        YEAR(date_sold) AS year,
        COUNT(*) AS cnt
    FROM silver_sales
    GROUP BY year
    ORDER BY year
    """).df()

    # Plot
    plt.figure(figsize=(8, 4))

    plt.bar(df_dates["year"], df_dates["cnt"])

    # Titles & labels
    plt.title("Transactions by Year (Cleaned Dates)", fontsize=14)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Number of Transactions", fontsize=12)

    # Improve readability
    plt.xticks(df_dates["year"], rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    # Tight layout for clean spacing
    plt.tight_layout()

    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Result:** **0** dates failed to parse; all 20,900 rows fall in 2024 (2024-01-01 → 2024-12-31).
    `TRY_STRPTIME` returns NULL instead of an error, so the check "0 failed" is what proves the rule covers every format.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ⚪ Cell 6 — One Row per Transaction, Then the Defaults

    900 `transaction_id`s appear twice. **415** are exact copies; the other **485** differ only because one copy has a NULL `discount` or `book_format`.
    So for each id we keep the **most complete** copy (`ORDER BY (discount IS NULL)::INT + (book_format IS NULL)::INT`), and only **then**:

    - NULL discount → 0.00, NULL format → `hard_copy` (business defaults; after this ordering, none are needed here),
    - `final_price` = `sale_price - discount`, recomputed (the source column is wrong in 20,692 rows).

    Fill the defaults **before** deduplicating and a copy with a guessed discount of 0.00 can win over the real one: a silent revenue error.
    """)
    return


@app.cell
def _(con):
    # 🧾 3. SQL

    # ----------------------------------------
    # One row per transaction_id: keep the MOST COMPLETE copy,
    # THEN fill the defaults and recompute final_price
    #
    # silver_sales ---> silver_sales_clean
    # ----------------------------------------

    _query = """
    CREATE OR REPLACE TABLE silver_sales_clean AS
    SELECT * EXCLUDE (discount, book_format, rn),
           COALESCE(discount, 0.00)                        AS discount,      -- rule: NULL discount → 0.00
           ROUND(sale_price - COALESCE(discount, 0.00), 2) AS final_price,   -- rule: recompute (the source value is wrong)
           COALESCE(book_format, 'hard_copy')              AS book_format    -- rule: NULL format → 'hard_copy'
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (
                   PARTITION BY transaction_id
                   ORDER BY (discount IS NULL)::INT + (book_format IS NULL)::INT,   -- complete copy first
                            date_sold
               ) AS rn
        FROM silver_sales
    )
    WHERE rn = 1
    """

    con.execute(_query).fetchall()

    # Validate
    _cleaned_rows = con.execute("""
    SELECT COUNT(*) AS cleaned_rows
    FROM silver_sales_clean
    """).df()

    _cleaned_rows
    return


@app.cell
def _(con):
    # 🔍 Validation (VERY IMPORTANT)
    # Check if duplicates still exist

    validation_rows = con.execute("""
    SELECT
        COUNT(*) AS total_rows,
        COUNT(DISTINCT transaction_id) AS unique_transactions,
        COUNT(*) - COUNT(discount)     AS null_discount,
        COUNT(*) - COUNT(book_format)  AS null_format,
        ROUND(SUM(final_price), 2)     AS revenue
    FROM silver_sales_clean
    """).df()

    validation_rows
    return


@app.cell
def _(con, plt):
    # 📊 4. Nice Plot (Before vs After)


    _df_counts = con.execute("""
    SELECT 'silver_sales' AS stage, COUNT(*) AS rows FROM silver_sales
    UNION ALL
    SELECT 'silver_sales_clean', COUNT(*) FROM silver_sales_clean
    """).df()

    plt.figure(figsize=(6,4))
    plt.bar(_df_counts["stage"], _df_counts["rows"])
    plt.title("Sales: Before vs After Deduplication")
    plt.ylabel("Row Count")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Result:** **20,000** rows = 20,000 distinct ids; 0 NULL discounts, 0 NULL formats; revenue **547,552.98**.

    **Reconciliation:** 21,000 raw = 20,000 loaded + 100 rejected (no id) + 900 duplicates removed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🟡 Cell 7 — `dim_book` (Gold)

    One row per book, keyed by `book_id` (the source's id: unique and stable, so we keep it as the key). Title, genre, author and publisher
    live **here**, once, instead of on 20,000 fact rows.
    """)
    return


@app.cell
def _(con):
    #🧾 3. SQL

    # ----------------------------------------
    # Create dim_book
    #
    # silver_books --> dim_book
    # ----------------------------------------

    _query = """
    CREATE OR REPLACE TABLE dim_book AS
    SELECT
        book_id,
        book_title,
        book_genre,
        author_id,
        author_name,
        author_gender,
        author_web_site,
        published_date,
        publisher
    FROM silver_books
    ORDER BY book_id
    """

    con.execute(_query).fetchall()

    # Validate
    dim_book_rows = con.execute("""
    SELECT COUNT(*) AS dim_book_rows
    FROM dim_book
    """).df()

    dim_book_rows
    return


@app.cell
def _(con):
    # 🔍 Validation (VERY IMPORTANT)

    # Ensure uniqueness of book_id
    con.execute("""
    SELECT COUNT(*) AS duplicate_books
    FROM (
        SELECT book_id, COUNT(*) AS cnt
        FROM dim_book
        GROUP BY book_id
        HAVING COUNT(*) > 1
    )
    """).df()

    ### 👉 Expected:
    ### duplicate_books = 0
    return


@app.cell
def _(con, plt):
    # 📊 4. Nice Plot (Books by Genre)


    _df_genre = con.execute("""
    SELECT
        book_genre,
        COUNT(*) AS num_books
    FROM dim_book
    GROUP BY book_genre
    ORDER BY num_books DESC
    """).df()

    plt.figure(figsize=(8,4))
    plt.bar(_df_genre["book_genre"], _df_genre["num_books"])
    plt.title("Number of Books by Genre")
    plt.xlabel("Genre")
    plt.ylabel("Number of Books")
    plt.xticks(rotation=30)
    plt.show()
    return


@app.cell
def _(con, plt):
    # ✅ Nice Pie Chart Version (Lecture-Quality)

    _df_genre = con.execute("""
    SELECT
        book_genre,
        COUNT(*) AS num_books
    FROM dim_book
    GROUP BY book_genre
    ORDER BY num_books DESC
    """).df()

    # Compact but readable
    plt.figure(figsize=(4, 4))

    plt.pie(
        _df_genre["num_books"],
        labels=_df_genre["book_genre"],   # 👈 bring labels back
        autopct='%1.0f%%',
        startangle=90,
        textprops={'fontsize': 8}        # 👈 smaller font to fit
    )

    plt.title("Books by Genre", fontsize=11)

    plt.tight_layout(pad=0.5)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Result:** **100** books, 0 duplicate ids. The catalog: Data Science 24 books, Fiction 21, Technology 21, History 20, Business 14.
    Keep these counts in mind: the revenue rankings later follow them closely.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🟡 Cell 8 — `dim_location` with a Surrogate Key

    Each distinct (`country`, `city`) pair gets a **surrogate key** `location_id` (1, 2, 3, …) made by the warehouse.
    The fact table then stores one small integer instead of two text columns, and a renamed city is changed in one row.
    """)
    return


@app.cell
def _(con):
    # 🧾 3. SQL

    # ----------------------------------------
    # Create dim_location
    #
    #  silver_sales_clean --> dim_location
    # ----------------------------------------

    _query = """
    CREATE OR REPLACE TABLE dim_location AS
    SELECT
        ROW_NUMBER() OVER (ORDER BY country_sold, city_sold) 
          AS location_id,
        country_sold AS country,
        city_sold AS city
    FROM (
        SELECT DISTINCT country_sold, city_sold
        FROM silver_sales_clean
    )
    ORDER BY country, city
    """

    con.execute(_query).fetchall()

    # Validate
    all_locations = con.execute("""
    SELECT location_id, country, city 
    FROM dim_location
    ORDER BY location_id
    """).df()

    all_locations
    return


@app.cell
def _(con):
    # 🔍 Validation (VERY IMPORTANT)

    # Ensure uniqueness of (country, city)
    con.execute("""
    SELECT COUNT(*) AS duplicates
    FROM (
        SELECT country, city, COUNT(*) AS cnt
        FROM dim_location
        GROUP BY country, city
        HAVING COUNT(*) > 1
    )
    """).df()

    ### 👉 Expected:
    ### duplicates = 0
    return


@app.cell
def _(con, plt):
    # 📊 4. Nice Plot (Transactions by Country)


    df_country = con.execute("""
    SELECT
        country_sold AS country,
        COUNT(*) AS transactions
    FROM silver_sales_clean
    GROUP BY country_sold
    ORDER BY transactions DESC
    """).df()

    plt.figure(figsize=(8,4))
    plt.bar(df_country["country"], df_country["transactions"])
    plt.title("Transactions by Country")
    plt.xlabel("Country")
    plt.ylabel("Transactions")
    plt.xticks(rotation=30)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Result:** **20** locations in 5 countries: USA **5** cities, UK, Germany and Canada 4 each, Australia **3**.
    The number of cities per country explains the country ranking in Cell 13.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Top-10 Cities
    """)
    return


@app.cell
def _(con, plt):
    df_city = con.execute("""
    SELECT
        city_sold AS city,
        COUNT(*) AS transactions
    FROM silver_sales_clean
    GROUP BY city_sold
    ORDER BY transactions DESC
    LIMIT 10
    """).df()

    plt.figure(figsize=(10,5))
    plt.barh(df_city["city"], df_city["transactions"])

    plt.title("Top 10 Cities by Transactions")
    plt.xlabel("Transactions")

    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🟡 Cell 9 — `dim_date`

    One row per day, with the parts that reports group by: year, month, day, weekday, quarter. Computed **once** here, so every report uses
    the same definition of "month" or "quarter".
    """)
    return


@app.cell
def _(con):
    # 🧾 3. SQL

    # ----------------------------------------
    # Create dim_date
    #
    # silver_sales_clean --> dim_date
    # ----------------------------------------

    _query = """
    CREATE OR REPLACE TABLE dim_date AS
    SELECT
        ROW_NUMBER() OVER (ORDER BY date_sold) AS date_id,
        date_sold,

        YEAR(date_sold)   AS year,
        MONTH(date_sold)  AS month,
        DAY(date_sold)    AS day,

        DAYNAME(date_sold) AS day_name,
        QUARTER(date_sold) AS quarter

    FROM (
        SELECT DISTINCT date_sold
        FROM silver_sales_clean
    )
    ORDER BY date_sold
    """

    con.execute(_query).fetchall()

    # Validate
    date_rows = con.execute("""
    SELECT COUNT(*) AS date_rows
    FROM dim_date
    """).df()

    date_rows
    return


@app.cell
def _(con):
    # 🔍 Validation (VERY IMPORTANT)
    # Ensure uniqueness of date

    dates_duplicates = con.execute("""
    SELECT COUNT(*) AS duplicates
    FROM (
        SELECT date_sold, COUNT(*) AS cnt
        FROM dim_date
        GROUP BY date_sold
        HAVING COUNT(*) > 1
    )
    """).df()

    ### 👉 Expected:
    ### dates_duplicates = 0


    dates_duplicates
    return


@app.cell
def _(con, plt):
    # 📊 4. Nice Plot (Transactions by Month)


    df_month = con.execute("""
    SELECT
        d.year,
        d.month,
        COUNT(*) AS transactions
    FROM silver_sales_clean s
    JOIN dim_date d
      ON s.date_sold = d.date_sold
    GROUP BY d.year, d.month
    ORDER BY d.year, d.month
    """).df()

    df_month["year_month"] = df_month["year"].astype(str) + "-" + df_month["month"].astype(str).str.zfill(2)

    plt.figure(figsize=(10,5))
    plt.plot(df_month["year_month"], df_month["transactions"], marker="o")

    plt.title("Transactions Over Time")
    plt.xlabel("Year-Month")
    plt.ylabel("Transactions")
    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Result:** **366** days (all of 2024, a leap year), 0 duplicates. A production `dim_date` would hold every day of the whole period,
    including days without sales.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🟡 Cell 10 — `fact_sales`: the Center of the Star

    **Grain: one row = one transaction.** Each row keeps the dimension keys (`date_id`, `book_id`, `location_id`), the attributes with only a few values
    (`sale_type`, `customer_gender`, `book_format`: kept in the fact as **degenerate dimensions**), and the measures (`quantity_sold`,
    `sale_price`, `discount`, `final_price`).
    """)
    return


@app.cell
def _(con):
    #🧾 3. SQL

    # ----------------------------------------
    # Create fact_sales
    #
    # { silver_sales_clean, dim_book, dim_location, dim_date } --> fact_sales
    # ----------------------------------------

    _query = """
    CREATE OR REPLACE TABLE fact_sales AS
    SELECT
        s.transaction_id,

        -- Foreign Keys
        d.date_id,
        b.book_id,
        l.location_id,

        -- Degenerate / attributes
        s.sale_type,
        s.customer_gender,
        s.book_format,

        -- Measures
        1 AS quantity_sold,
        s.sale_price,
        s.discount,
        s.final_price

    FROM silver_sales_clean s

    JOIN dim_book b
      ON s.book_id = b.book_id

    JOIN dim_location l
      ON s.country_sold = l.country
     AND s.city_sold = l.city

    JOIN dim_date d
      ON s.date_sold = d.date_sold

    ORDER BY s.transaction_id
    """

    con.execute(_query).fetchall()

    # Validate
    fact_rows_count = con.execute("""
    SELECT COUNT(*) AS fact_rows
    FROM fact_sales
    """).df()


    fact_rows_count
    return


@app.cell
def _(con):
    # 🔍 Validation (VERY IMPORTANT)
    # Check referential integrity

    total_rows = con.execute("""
    SELECT
        COUNT(*) AS total_rows,
        COUNT(DISTINCT transaction_id) AS unique_tx
    FROM fact_sales
    """).df()

    ### 👉 Expected:
    ### total_rows = unique_tx = 20000

    total_rows
    return


@app.cell
def _(con, plt):
    # 📊 4. Nice Plot (Revenue by Sale Type: INSTORE vs ONLINE)


    df_sales_type = con.execute("""
    SELECT
        sale_type,
        SUM(final_price) AS revenue
    FROM fact_sales
    GROUP BY sale_type
    """).df()

    plt.figure(figsize=(6,4))
    plt.bar(df_sales_type["sale_type"], df_sales_type["revenue"])

    plt.title("Revenue by Sale Type")
    plt.xlabel("Sale Type")
    plt.ylabel("Revenue")

    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Result:** **20,000** fact rows = 20,000 transactions, every one with its keys. Revenue by channel: ONLINE **290,288** (10,584 sales),
    INSTORE 257,265 (9,416 sales): ONLINE leads because it has more sales, not bigger ones.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 📊 Cell 11 — BI Query 1: Revenue by Genre

    Fact (measure) + dimension (grouping): the basic star-schema query.
    """)
    return


@app.cell
def _(con):
    #🧾 3. SQL: using "star schema tables"

    _query = """
    SELECT
        b.book_genre,
        ROUND(SUM(f.final_price), 2) AS total_revenue
    FROM fact_sales f
    JOIN dim_book b
      ON f.book_id = b.book_id
    GROUP BY b.book_genre
    ORDER BY total_revenue DESC
    """

    df_genre = con.execute(_query).df()
    df_genre
    return (df_genre,)


@app.cell
def _(df_genre, plt):
    #📊 4. Nice Plot (Revenue by Genre)


    plt.figure(figsize=(8,5))
    plt.bar(df_genre["book_genre"], df_genre["total_revenue"])

    plt.title("Revenue by Book Genre")
    plt.xlabel("Genre")
    plt.ylabel("Revenue")

    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Result:** Data Science **130,087**, Fiction 116,391, Technology 112,373, History 112,042, Business 76,659.

    **Why?** Divide by the number of books: every genre earns about **5,350–5,600 per book**. Data Science is first because it has the most books (24),
    Business last because it has the fewest (14). The ranking reflects the **catalog**, not demand per book. This is a **roll-up** (week 4).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 📊 Cell 12 — BI Query 2: Top 10 Books
    """)
    return


@app.cell
def _(con):
    # 🧾 3. SQL

    _query = """
    SELECT
        b.book_title,
        ROUND(SUM(f.final_price), 2) AS revenue
    FROM fact_sales f
    JOIN dim_book b
      ON f.book_id = b.book_id
    GROUP BY b.book_title
    ORDER BY revenue DESC
    LIMIT 10
    """

    df_top_books = con.execute(_query).df()
    df_top_books
    return (df_top_books,)


@app.cell
def _(df_top_books, plt):
    # 📊 4. Nice Plot (Top 10 Books)
    # 👉 Recommended: Horizontal Bar (cleaner)


    plt.figure(figsize=(10,6))
    plt.barh(df_top_books["book_title"], df_top_books["revenue"])

    plt.title("Top 10 Books by Revenue")
    plt.xlabel("Revenue")

    plt.gca().invert_yaxis()  # highest on top
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Result:** Book 98 (6,607) to Book 52 (5,989): the top 10 are within about 10% of each other, so no "bestseller" stands out.
    `SUM(final_price)` ranks by **revenue**; `COUNT(*)` would rank by **copies sold**: say which one you report.
    The cell below adds `RANK()` (week 2) to show ties.
    """)
    return


@app.cell
def _(con):
    _query = """
    SELECT
        b.book_title,
        ROUND(SUM(f.final_price), 2) AS revenue,
        RANK() OVER (ORDER BY SUM(f.final_price) DESC) AS rank
    FROM fact_sales f
    JOIN dim_book b
      ON f.book_id = b.book_id
    GROUP BY b.book_title
    ORDER BY revenue DESC
    LIMIT 10
    """

    con.execute(_query).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 📊 Cell 13 — BI Query 3: Revenue by Country
    """)
    return


@app.cell
def _(con):
    # 🧾 3. SQL

    _query = """
    SELECT
        l.country,
        ROUND(SUM(f.final_price), 2) AS revenue
    FROM fact_sales f
    JOIN dim_location l
      ON f.location_id = l.location_id
    GROUP BY l.country
    ORDER BY revenue DESC
    """

    df_country_rev = con.execute(_query).df()
    df_country_rev
    return (df_country_rev,)


@app.cell
def _(df_country_rev, plt):
    # 📊 4. Nice Plot (Revenue by Country)


    plt.figure(figsize=(8,5))
    plt.bar(df_country_rev["country"], df_country_rev["revenue"])

    plt.title("Revenue by Country")
    plt.xlabel("Country")
    plt.ylabel("Revenue")

    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The same result as a pie chart
    """)
    return


@app.cell
def _(df_country_rev, plt):
    plt.figure(figsize=(6,6))
    plt.pie(df_country_rev["revenue"],
            labels=df_country_rev["country"],
            autopct='%1.1f%%')

    plt.title("Revenue Share by Country")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Result:** USA **138,442**, UK 110,923, Germany 108,114, Canada 108,073, Australia 82,001.

    **Why?** Per city, every country earns about **27,000–27,700**. The USA is first because it has 5 cities, Australia last because it has 3.
    Before calling the USA "the strongest market", compare **per city** (or per customer).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 📊 Cell 14 — BI Query 4: Monthly Revenue
    """)
    return


@app.cell
def _(con):
    # 🧾 3. SQL

    _query = """
    SELECT
        d.year,
        d.month,
        ROUND(SUM(f.final_price), 2) AS revenue
    FROM fact_sales f
    JOIN dim_date d
      ON f.date_id = d.date_id
    GROUP BY d.year, d.month
    ORDER BY d.year, d.month
    """

    df_month_rev = con.execute(_query).df()

    # Create a proper label
    df_month_rev["year_month"] = (
        df_month_rev["year"].astype(str) + "-" +
        df_month_rev["month"].astype(str).str.zfill(2)
    )

    df_month_rev
    return (df_month_rev,)


@app.cell
def _(df_month_rev, plt):
    # 📊 4. Nice Plot (Line Chart — VERY IMPORTANT)


    plt.figure(figsize=(12,5))
    plt.plot(df_month_rev["year_month"],
             df_month_rev["revenue"],
             marker="o")

    plt.title("Monthly Revenue Trend")
    plt.xlabel("Year-Month")
    plt.ylabel("Revenue")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Result:** from 42,868 (February) to 49,951 (August); most months 44,000–47,000. February is the shortest month, so part of its dip is simply fewer days.
    The 3-month rolling average (next cell) stays between 44,000 and 47,200: no strong season in this one year.
    """)
    return


@app.cell
def _(df_month_rev, plt):
    # 🚀 Optional Upgrade (VERY NICE)

    # Add smoothing:

    df_month_rev["rolling_avg"] = df_month_rev["revenue"].rolling(3).mean()

    plt.figure(figsize=(12,5))
    plt.plot(df_month_rev["year_month"], df_month_rev["revenue"], label="Revenue")
    plt.plot(df_month_rev["year_month"], df_month_rev["rolling_avg"], label="3-Month Avg")

    plt.legend()
    plt.xticks(rotation=45)
    plt.title("Revenue Trend with Rolling Average")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 📊 Cell 15 — BI Query 5: Revenue by Format

    `book_format` lives in the fact table (a degenerate dimension): no join needed.
    """)
    return


@app.cell
def _(con):
    # 🧾 3. SQL

    _query = """
    SELECT
        f.book_format,
        ROUND(SUM(f.final_price), 2) AS revenue
    FROM fact_sales f
    GROUP BY f.book_format
    ORDER BY revenue DESC
    """

    df_format = con.execute(_query).df()
    df_format
    return (df_format,)


@app.cell
def _(df_format, plt):
    # 📊 4. Nice Plot (Pie Chart — very effective)


    plt.figure(figsize=(6,6))
    plt.pie(df_format["revenue"],
            labels=df_format["book_format"],
            autopct='%1.1f%%')

    plt.title("Revenue by Book Format")
    plt.show()
    return


@app.cell
def _(df_format, plt):
    # 🔥 Alternative (Bar Chart — more precise)

    plt.figure(figsize=(6,4))
    plt.bar(df_format["book_format"], df_format["revenue"])

    plt.title("Revenue by Book Format")
    plt.xlabel("Format")
    plt.ylabel("Revenue")

    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Result:** soft copy **199,099**, paperback 183,117, hard copy 165,338 (36% / 33% / 30%).
    """)
    return


@app.cell
def _():
    # blank
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 📊 Cell 16 — BI Query 6: Revenue by Customer Gender
    """)
    return


@app.cell
def _(con):
    # 🧾 3. SQL

    _query = """
    SELECT
        f.customer_gender,
        ROUND(SUM(f.final_price), 2) AS revenue
    FROM fact_sales f
    GROUP BY f.customer_gender
    ORDER BY revenue DESC
    """

    df_gender = con.execute(_query).df()
    df_gender
    return (df_gender,)


@app.cell
def _(df_gender, plt):
    # 📊 4. Nice Plot (Bar Chart)


    plt.figure(figsize=(6,4))
    plt.bar(df_gender["customer_gender"], df_gender["revenue"])

    plt.title("Revenue by Customer Gender")
    plt.xlabel("Customer Gender")
    plt.ylabel("Revenue")

    plt.show()
    return


@app.cell
def _(df_gender, plt):
    # 🔥 Optional Upgrade (Pie Chart)

    plt.figure(figsize=(6,6))
    plt.pie(df_gender["revenue"],
            labels=df_gender["customer_gender"],
            autopct='%1.1f%%')

    plt.title("Revenue Share by Gender")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Result:** FEMALE **292,885** (10,732 sales), MALE 254,668 (9,268 sales). The average sale is almost the same (27.29 vs 27.48):
    the difference is the **number** of sales, not what each customer spends.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 📊 Cell 17 — BI Query 7: Revenue by Publisher

    `publisher` is in `dim_book`, so this query joins the fact to that dimension.
    """)
    return


@app.cell
def _(con):
    #🧾 3. SQL

    _query = """
    SELECT
        b.publisher,
        ROUND(SUM(f.final_price), 2) AS revenue
    FROM fact_sales f
    JOIN dim_book b
      ON f.book_id = b.book_id
    GROUP BY b.publisher
    ORDER BY revenue DESC
    """

    df_publisher = con.execute(_query).df()
    df_publisher
    return (df_publisher,)


@app.cell
def _(df_publisher, plt):
    # 📊 4. Nice Plot (Bar Chart)


    plt.figure(figsize=(7,5))
    plt.bar(df_publisher["publisher"], df_publisher["revenue"])

    plt.title("Revenue by Publisher")
    plt.xlabel("Publisher")
    plt.ylabel("Revenue")

    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df_publisher, plt):
    # 🔥 Optional Upgrade (Pie Chart)

    plt.figure(figsize=(6,6))
    plt.pie(df_publisher["revenue"],
            labels=df_publisher["publisher"],
            autopct='%1.1f%%')

    plt.title("Revenue Share by Publisher")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Result:** Prentice Hall **233,115**, O'Reilly 158,207, Penguin 156,232. Prentice Hall publishes **42** of the 100 books (the others 29 each):
    per book, all three earn about 5,400–5,550. Same lesson as genres and countries: divide by the size of the group before you compare.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 📊 Cell 18 — BI Query 8: Genre × Channel

    Two dimensions at once: a **slice** of the OLAP cube (week 4).
    """)
    return


@app.cell
def _(con):
    #🧾 3. SQL

    _query = """
    SELECT
        b.book_genre,
        f.sale_type,
        ROUND(SUM(f.final_price), 2) AS revenue
    FROM fact_sales f
    JOIN dim_book b
      ON f.book_id = b.book_id
    GROUP BY b.book_genre, f.sale_type
    ORDER BY b.book_genre, f.sale_type
    """

    df_genre_channel = con.execute(_query).df()
    df_genre_channel
    return (df_genre_channel,)


@app.cell
def _(df_genre_channel, plt):
    # 📊 4. Nice Plot (Grouped Bar Chart)


    # Pivot for better plotting
    pivot_df = df_genre_channel.pivot(
        index="book_genre",
        columns="sale_type",
        values="revenue"
    )

    pivot_df.plot(kind="bar", figsize=(10,5))

    plt.title("Revenue by Genre and Sale Type")
    plt.xlabel("Genre")
    plt.ylabel("Revenue")

    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
    return (pivot_df,)


@app.cell
def _(pivot_df, plt):
    # 🔥 Optional Upgrade (Stacked Bar)

    pivot_df.plot(kind="bar", stacked=True, figsize=(10,5))

    plt.title("Revenue by Genre (Stacked by Sale Type)")
    plt.xlabel("Genre")
    plt.ylabel("Revenue")

    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Result:** **every** genre earns more ONLINE than INSTORE (for example Fiction 62,804 vs 53,586, Data Science 67,647 vs 62,441):
    the 53% / 47% channel split of Cell 10 holds in every genre. No genre needs a different channel strategy.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 📊 Cell 19 — BI Query 9: Top Country per Genre

    `RANK() OVER (PARTITION BY genre ORDER BY revenue DESC)` = 1: top-N **per group** (week 2).
    """)
    return


@app.cell
def _(con):
    # 🧾 3. SQL

    _query = """
    WITH genre_country AS (
        SELECT
            b.book_genre,
            l.country,
            ROUND(SUM(f.final_price), 2) AS revenue
        FROM fact_sales f
        JOIN dim_book b
          ON f.book_id = b.book_id
        JOIN dim_location l
          ON f.location_id = l.location_id
        GROUP BY b.book_genre, l.country
    ),

    ranked AS (
        SELECT
            *,
            RANK() OVER (
                PARTITION BY book_genre
                ORDER BY revenue DESC
            ) AS rnk
        FROM genre_country
    )

    SELECT
        book_genre,
        country,
        revenue
    FROM ranked
    WHERE rnk = 1
    ORDER BY revenue DESC
    """

    df_top_country_genre = con.execute(_query).df()
    df_top_country_genre
    return (df_top_country_genre,)


@app.cell
def _(df_top_country_genre, plt):
    # 📊 4. Nice Plot


    plt.figure(figsize=(10,5))
    plt.bar(df_top_country_genre["book_genre"],
            df_top_country_genre["revenue"])

    plt.title("Top Country per Genre (Revenue)")
    plt.xlabel("Genre")
    plt.ylabel("Revenue")

    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Result:** the USA is first in **all 5** genres (Data Science 33,329 … Business 19,461). Expected: the USA has the most cities (Cell 8).
    A "top per group" result is only interesting when the groups are comparable.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 📊 Cell 20 — BI Query 10: KPI Summary
    """)
    return


@app.cell
def _(con):
    # 🧾 3. SQL

    _query = """
    SELECT
        COUNT(*) AS total_transactions,
        ROUND(SUM(final_price), 2) AS total_revenue,
        ROUND(AVG(final_price), 2) AS avg_order_value,
        ROUND(SUM(discount), 2) AS total_discount
    FROM fact_sales
    """

    df_kpi = con.execute(_query).df()
    df_kpi
    return (df_kpi,)


@app.cell
def _(df_kpi, plt):
    # 📊 4. Nice Plot (KPI Visualization)


    # Convert to long format for plotting
    df_plot = df_kpi.melt(var_name="metric", value_name="value")

    plt.figure(figsize=(8,4))
    plt.bar(df_plot["metric"], df_plot["value"])

    plt.title("Executive KPI Dashboard")
    plt.ylabel("Value")

    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df_kpi):
    # 🔥 Optional Upgrade (Cleaner Dashboard Style)

    for col in df_kpi.columns:
        print(f"{col}: {df_kpi[col][0]:,.2f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Result:** **20,000** transactions, revenue **547,552.98**, average sale **27.38**, total discounts **50,105.65** (8.4% of the list price).
    One row from the fact table alone: no join, no grouping.

    ## What this notebook did

    | Step | Rows |
    |---|---|
    | Bronze: load as received | 21,000 sales · 120 books |
    | Silver: reject no-id rows | −100 |
    | Silver: parse 3 date formats | 0 failures |
    | Silver: one row per transaction (most complete copy), then defaults + recompute `final_price` | −900 → 20,000 |
    | Silver: deduplicate books | 120 → 100 |
    | Gold: star schema | `fact_sales` 20,000 · `dim_book` 100 · `dim_location` 20 · `dim_date` 366 |
    | BI | 10 questions: in this data, almost every difference comes from **group size** (books, cities, customers) |
    """)
    return


if __name__ == "__main__":
    app.run()
