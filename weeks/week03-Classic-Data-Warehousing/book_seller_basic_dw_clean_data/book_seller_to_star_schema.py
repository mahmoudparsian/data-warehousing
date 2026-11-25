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
    # Book Seller to Star Schema
    ## First POC on Data Warehousing

    ```
    This notebook demonstrates a simple
    end-to-end data warehousing proof of
    concept using a fictional "book seller".
    ```

    ### Goals

    1. Load two operational tables: `sales` and `books`

    2. Understand the transactional design

    3. Design and build a star schema (a fact table and dimension tables)

    4. Perform ETL from operational tables into dimensional tables and a fact table

    5. Run business intelligence queries on the star schema

    ### Tools
    - Python
    - Pandas
    - DuckDB

    ### Input files

    The following files are generated from a transactional databases:

    - `sales.csv` with 10,000 rows
    - `books.csv` with 100 rows
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    #  What is a Star Schema?
    # ⭐ Star Schema (Core Concept in Data Warehousing)

    A **Star Schema** is a data model designed for **analytical queries (OLAP)**.

    It consists of:

    - **1 central FACT table** (measurable events)
    - **Multiple DIMENSION tables** (descriptive context)

    ```
                        dim_location
                              |
                              |
        dim_book   ------ fact_sales  ------- dim_date
                              |
                              |
                        dim_book_format
    ```

    ---

    ## Key Characteristics of a Star Schema

    - Simple and intuitive structure
    - Optimized for **fast queries**
    - Uses **joins between fact and dimensions**
    - Supports **aggregation and reporting**

    ---

    ## Why use Star Schema?

    - Faster analytics
    - Cleaner queries
    - Better organization of data
    - Scales for large datasets

    ---

    ## Example in this project

    - **fact_sales** → transactions
    - **dim_book** → book details
    - **dim_location** → geography
    - **dim_date** → time
    - **dim_book_format** → format of book

    ---
    # 📄 Slide 2 — Fact Table vs Dimension Tables

    ## 🟡 Fact Table (fact_sales)

    ### What is it?

    Stores **business events** (transactions)

    ### Contains:

    - **Foreign Keys**
      - book_id
      - date_id
      - location_id

    - **Measures (numeric values)**
      - sale_price
      - discount
      - final_price

    ---

    ### Example:

    | transaction_id | book_id | date_id | revenue |
    |----------------|--------|--------|---------|
    | 1001           | 10     | 25     | 20.00   |

    ---

    ## 🟢 Dimension Tables

    ### What are they?

    Store **descriptive attributes**

    ---

    ### Examples:

    #### dim_book
    - book_title
    - genre
    - publisher

    #### dim_location
    - country
    - city

    #### dim_date
    - year
    - month
    - day

    ---

    ## 🔥 Key Differences

    | Feature | Fact Table | Dimension Table |
    |--------|-----------|----------------|
    | Purpose | Store events | Describe data |
    | Size | Large | Small |
    | Data | Numeric | Text / attributes |
    | Updates | Frequent | Rare |

    ---

    ## 🧠 Key Insight

    * Fact table = “What happened?”

    * Dimension tables = “Context of what happened”
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Data Quality

    #### NOTE-1: For this notebook, all of data is clean
    #### NOTE-2: In the next iterations, we will deal with "messy" data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Cell Description
    ### 1. Import required libraries
    ### 2. Define Data location
    """)
    return


@app.cell
def _():
    import pandas as pd
    from pathlib import Path

    # define the folder where data files are
    DATA_DIR = Path("./data")

    sales_file = DATA_DIR / "sales.csv"
    # sales_file = "./data/sales.csv"

    books_file = DATA_DIR / "books.csv"
    # books_file = "./data/books.csv"

    print("sales.csv file exists:", sales_file.exists())
    print("books.csv file exists:", books_file.exists())
    return books_file, pd, sales_file


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Create a DuckDB Connection object as con
    """)
    return


@app.cell
def _():
    import duckdb

    # create a DuckDB Connection Object as con:
    con = duckdb.connect()

    # print for debugging purposes
    print("DuckDB version: ", duckdb.__version__)
    print("DuckDB conection object:", con)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Load the operational tables

    These are the original transactional tables. In a real system, they might come from an OLTP database, application exports, or APIs.

    For this first POC, the data is clean on purpose so we can focus on dimensional modeling and ETL.
    """)
    return


@app.cell
def _(books_file, pd, sales_file):
    sales_df = pd.read_csv(sales_file, parse_dates=["date_sold"])
    books_df = pd.read_csv(books_file, parse_dates=["published_date"])

    print("sales_df shape:", sales_df.shape)
    print("books_df shape:", books_df.shape)
    return books_df, sales_df


@app.cell
def _(sales_df):
    sales_df.head()
    return


@app.cell
def _(books_df):
    books_df.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Create DuckDB tables for the operational model

    We now load the CSV files into DuckDB so we can use SQL for transformation and analytics.
    """)
    return


@app.cell
def _(books_df, con, sales_df):
    con.execute("DROP TABLE IF EXISTS sales").fetchall()
    con.execute("DROP TABLE IF EXISTS books").fetchall()

    con.from_df(sales_df).create("sales")
    con.from_df(books_df).create("books")

    con.execute("SHOW TABLES").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Understand the transactional schema

    The `sales` table mixes several concerns:
    - transaction information
    - date information
    - location information
    - book format information

    The `books` table contains book and author attributes.

    This is acceptable for transactions, but it is not ideal for analytics at scale. A star schema makes reporting easier and faster.
    """)
    return


@app.cell
def _(con):
    print("Sales schema:")
    print(con.execute("DESCRIBE sales").df().to_string(index=False))
    return


@app.cell
def _(con):
    print("\nBooks schema:")
    print(con.execute("DESCRIBE books").df().to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Proposed star schema

    We will create the following dimensional model:

    ### Dimension tables
    1. `dim_book`
       - book information and author attributes
    2. `dim_location`
       - country and city where the book was sold
    3. `dim_date`
       - one row per sold date
    4. `dim_book_format`
       - hard copy / paperback / soft copy

    ### Fact table
    5. `fact_sales`
       - one row per transaction
       - foreign keys to dimensions
       - measures such as `sale_price`, `discount`, and `final_price`

    This is a simple, practical star schema for teaching and BI work.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. ETL Step A: Create dimension tables

    We start by extracting unique descriptive entities from the operational tables.
    """)
    return


@app.cell
def _(con):
    con.execute("DROP TABLE IF EXISTS dim_book").fetchall()
    con.execute("""
    CREATE OR REPLACE TABLE dim_book AS
    SELECT
        book_id,
        book_title,
        book_genre,
        author_id,
        author_name,
        author_web_site,
        published_date
    FROM books
    ORDER BY book_id
    """).fetchall()

    con.execute("SELECT COUNT(*) AS dim_book_rows FROM dim_book").df()
    return


@app.cell
def _(con):
    five_rows = con.execute("SELECT * FROM dim_book LIMIT 5").df()
    five_rows
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Create Location Dimension Table as `dim_location` table.

    ### Note that `location_id` is a "surrogate key"

    ### What is a surrogate key?

    ```
        A surrogate key is a unique, system-generated,
        and business-meaningless value (often an integer
        or UUID) used as a database table's primary key.
        Unlike natural keys, they have no intrinsic meaning,
        ensuring consistent identification regardless of data
        changes. Common examples include AUTO_INCREMENT,
        IDENTITY columns, or sequences.
    ```

    #### Here, a pair of `(country, city)` is represented by a `location_id`.
    """)
    return


@app.cell
def _(con):
    con.execute("DROP TABLE IF EXISTS dim_location").fetchall()
    con.execute("""
    CREATE OR REPLACE TABLE dim_location AS
    SELECT
        ROW_NUMBER() OVER (ORDER BY country_sold, city_sold) AS location_id,
        country_sold AS country,
        city_sold AS city
    FROM (
        SELECT DISTINCT country_sold, city_sold
        FROM sales
    )
    ORDER BY country, city
    """).fetchall()

    con.execute("SELECT * FROM dim_location ORDER BY location_id").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Create Date Dimension table as `dim_date`

    ```
       date_id is a "surrogate key" and acts
       as a PK for the `dim_date` table
    ```
    """)
    return


@app.cell
def _(con):
    con.execute("DROP TABLE IF EXISTS dim_date").fetchall()
    con.execute("""
    CREATE OR REPLACE TABLE dim_date AS
    SELECT
        ROW_NUMBER() OVER (ORDER BY date_sold) AS date_id,
        date_sold,
        year(date_sold) AS year_sold,
        month(date_sold) AS month_sold,
        day(date_sold) AS day_sold,
        dayname(date_sold) AS day_name,
        quarter(date_sold) AS quarter_num
    FROM (
        SELECT DISTINCT date_sold
        FROM sales
    )
    ORDER BY date_sold
    """).fetchall()

    con.execute("SELECT * FROM dim_date ORDER BY date_id LIMIT 10").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Create Book Format Dimension table as `dim_book_format`

    * NOTE-1:

    ```
       format_id is a "surrogate key" and acts
       as a PK for the `dim_book_format` table
    ```

    * NOTE-2:

    ```
        These 3 columns (`hard_copy`, `paperback`, and `soft_copy`)
        in sales table are replaced by a `format_id`.
    ```
    """)
    return


@app.cell
def _(con):
    con.execute("DROP TABLE IF EXISTS dim_book_format").fetchall()
    con.execute("""
    CREATE OR REPLACE TABLE dim_book_format AS
    SELECT 1 AS format_id, 'HARDCOPY' AS format_name
    UNION ALL
    SELECT 2 AS format_id, 'PAPERBACK' AS format_name
    UNION ALL
    SELECT 3 AS format_id, 'SOFTCOPY' AS format_name
    ORDER BY format_id
    """).fetchall()

    con.execute("SELECT * FROM dim_book_format").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. ETL Step B: Create the fact table as `fact_sales`

    ```
    Now we map each transaction to its dimension keys
    and keep the measurable attributes (sale_price,
    discount, final_price, ...) in the fact table.
    ```

    #### What is a Fact Table in Star Schema?
    ```
    A fact table is the central hub of a star schema in a
    data warehouse, storing quantitative metrics (measures)
    such as sales amounts, quantities, or prices. It connects
    to surrounding dimension tables via foreign keys to enable
    analysis of business events. Fact tables are typically very
    large, containing millions of rows, and are optimized for
    fast aggregation.
    ```

    #### Observations:

    ```
    1. These 3 columns (`hard_copy`, `paperback`, `soft_copy`)
        in sales table are replaced by a `format_id`.

    2. These 4 columns (`date_sold`, `year_sold`, `month_sold`, `day_sold`)
       in sales table are replaced by a `date_id`.

    3. These 2 columns (`country`, `city`) is replaced
       and represented by a `location_id`.
    ```

    #### Measureable fields/columns in `fact_sales` table:
    * `sale_type`
    * `quantity_sold`
    * `sale_price`
    * `discount`
    * `final_price`
    """)
    return


@app.cell
def _(con):
    con.execute("DROP TABLE IF EXISTS fact_sales").fetchall()
    con.execute("""
    CREATE OR REPLACE TABLE fact_sales AS
    WITH sales_enriched AS (
        SELECT
            s.transaction_id,
            s.book_id,
            s.sale_type,
            s.date_sold,
            s.sale_price,
            s.discount,
            s.final_price,
            s.country_sold,
            s.city_sold,
            CASE
                WHEN s.hard_copy THEN 'HARDCOPY'
                WHEN s.paperback THEN 'PAPERBACK'
                WHEN s.soft_copy THEN 'SOFTCOPY'
            END AS format_name
        FROM sales s
    )
    SELECT
        se.transaction_id,
        d.date_id,
        b.book_id,
        l.location_id,
        f.format_id,
        se.sale_type,
        1 AS quantity_sold,
        se.sale_price,
        se.discount,
        se.final_price
    FROM sales_enriched se
    JOIN dim_book b
        ON se.book_id = b.book_id
    JOIN dim_location l
        ON se.country_sold = l.country
       AND se.city_sold = l.city
    JOIN dim_date d
        ON se.date_sold = d.date_sold
    JOIN dim_book_format f
        ON se.format_name = f.format_name
    ORDER BY se.transaction_id
    """).fetchall()

    con.execute("SELECT COUNT(*) AS fact_rows FROM fact_sales").df()
    return


@app.cell
def _(con):
    con.execute("SELECT * FROM fact_sales LIMIT 10").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 7. Validate the star schema

    Three checks, every time:
    - **rows:** `fact_sales` has as many rows as `sales` (10,000); `dim_book` 100, `dim_location` 15 (5 countries × 3 cities), `dim_date` 731 (every day of 2024–2025)
    - **totals:** `SUM(final_price)` is the same in `sales` and `fact_sales` (255,735.44)
    - **keys:** no fact row without its dimension keys (0)
    """)
    return


@app.cell
def _(con):
    validation_sql = '''
    SELECT 'sales' AS table_name, COUNT(*) AS row_count FROM sales
    UNION ALL
    SELECT 'fact_sales' AS table_name, COUNT(*) AS row_count FROM fact_sales
    UNION ALL
    SELECT 'dim_book' AS table_name, COUNT(*) AS row_count FROM dim_book
    UNION ALL
    SELECT 'dim_location' AS table_name, COUNT(*) AS row_count FROM dim_location
    UNION ALL
    SELECT 'dim_date' AS table_name, COUNT(*) AS row_count FROM dim_date
    UNION ALL
    SELECT 'dim_book_format' AS table_name, COUNT(*) AS row_count FROM dim_book_format
    '''
    con.execute(validation_sql).df()
    return


@app.cell
def _(con):
    # Totals must match too: rows in = rows out is not enough
    con.execute("""
    SELECT ROUND((SELECT SUM(final_price) FROM sales), 2)      AS sales_revenue,
           ROUND((SELECT SUM(final_price) FROM fact_sales), 2) AS fact_revenue,
           (SELECT COUNT(*) FROM fact_sales
            WHERE date_id IS NULL OR location_id IS NULL OR format_id IS NULL) AS missing_keys
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 8. Star schema diagram

    Conceptually:

    - `fact_sales` links to:
      - `dim_book`
      - `dim_location`
      - `dim_date`
      - `dim_book_format`

    This is the central idea of the star schema:
    a **fact table** in the middle, and **dimension tables** around it.

    ```
                        dim_location
                              |
                              |
        dim_book   ------ fact_sales  ------- dim_date
                              |
                              |
                        dim_book_format
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 9. Business Intelligence questions

    Ten BI questions follow (Cells 1–10), each with its SQL, a chart and the result in numbers. The three classic ones:

    1. Which book genres generate the highest revenue?
    2. Which countries and cities generate the most sales?
    3. How do sales vary by month and sale type?

    We now answer them in SQL using the star schema
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # ✅ Cell 1 — Revenue by Book Genre

    ## Question

    Which genres earn the most?

    **Result:** Fantasy is first (**46,454**), then Data Science (39,129); Biography is last (12,846).

    **Why?** Look at *count* and *price* separately (Cell 11 below): Fantasy has **20 of the 100 books** and 2,080 sales, but a low average sale (22.33).
    Data Science has only 9 books, but the highest average sale (**41.72**). (Counts per genre: the extra tables at the end.) Revenue = volume × price: always check which one drives it.

    """)
    return


@app.cell
def _(con):
    # ----------------------------------------
    # Objective: Revenue by Book Genre
    # ----------------------------------------

    _query = """
    SELECT
        b.book_genre,
        SUM(f.final_price) AS total_revenue
    FROM fact_sales f
    JOIN dim_book b
      ON f.book_id = b.book_id
    GROUP BY b.book_genre
    ORDER BY total_revenue DESC
    """

    df = con.execute(_query).df()
    df
    return (df,)


@app.cell
def _(df):
    # Plot
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10,5))
    plt.bar(df["book_genre"], df["total_revenue"])
    plt.title("Revenue by Genre")
    plt.xlabel("Genre")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.show()
    return (plt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ✅ Cell 2 — Top 10 Books by Revenue

    ## Question

    Which books earn the most?

    **Result:** the top book ("Practical Machine Learning 84") earns 4,808, the 10th 3,919: no single book dominates.
    For promotions, compare this list with the **count** of sales per book: a top-revenue book may simply be expensive.

    """)
    return


@app.cell
def _(con):
    _query = """
    SELECT
        b.book_title,
        SUM(f.final_price) AS revenue
    FROM fact_sales f
    JOIN dim_book b
      ON f.book_id = b.book_id
    GROUP BY b.book_title
    ORDER BY revenue DESC
    LIMIT 10
    """

    df_2 = con.execute(_query).df()
    df_2
    return (df_2,)


@app.cell
def _(df_2, plt):
    plt.figure(figsize=(10,5))
    plt.barh(df_2["book_title"], df_2["revenue"])
    plt.title("Top 10 Books by Revenue")
    plt.xlabel("Revenue")
    plt.gca().invert_yaxis()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # ✅ Cell 3 — Revenue by Country

    ## Question

    Which countries earn the most?

    **Result:** all 5 countries are within 4%: Germany 52,090 · USA 51,436 · Canada 51,287 · UK 50,990 · Australia 49,933.
    No country stands out, so a country-specific strategy is not supported by this data.

    """)
    return


@app.cell
def _(con):
    _query = """
    SELECT
        l.country,
        SUM(f.final_price) AS revenue
    FROM fact_sales f
    JOIN dim_location l
      ON f.location_id = l.location_id
    GROUP BY l.country
    ORDER BY revenue DESC
    """

    df_3 = con.execute(_query).df()
    df_3
    return (df_3,)


@app.cell
def _(df_3, plt):
    plt.figure(figsize=(8,5))
    plt.bar(df_3["country"], df_3["revenue"])
    plt.title("Revenue by Country")
    plt.xlabel("Country")
    plt.ylabel("Revenue")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # ✅ Cell 4 — Top Cities by Sales Volume

    ## Question

    Which cities have the most transactions?

    **Result:** Munich (706), San Francisco (697), London and Vancouver (686): the 15 cities range only from 627 to 706 transactions.
    `COUNT(*)` measures **volume**; `SUM(final_price)` would measure **revenue**: name which one you report.

    """)
    return


@app.cell
def _(con):
    _query = """
    SELECT
        l.city,
        COUNT(*) AS transactions
    FROM fact_sales f
    JOIN dim_location l
      ON f.location_id = l.location_id
    GROUP BY l.city
    ORDER BY transactions DESC
    LIMIT 10
    """

    df_4 = con.execute(_query).df()
    df_4
    return (df_4,)


@app.cell
def _(df_4, plt):
    plt.figure(figsize=(10,5))
    plt.bar(df_4["city"], df_4["transactions"])
    plt.title("Top Cities by Transactions")
    plt.xticks(rotation=45)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # ✅ Cell 5 — Monthly Revenue Trend

    ## Question

    Is there seasonality?

    **Result:** months range from 9,169 (June 2024, the lowest) to about 11,250; 2025 (129,838) is **3.1%** above 2024 (125,898).
    The line is flat with noise: no clear season. One `dim_date` join gives year and month without any date functions in the query.

    """)
    return


@app.cell
def _(con):
    _query = """
    SELECT
        d.year_sold,
        d.month_sold,
        SUM(f.final_price) AS revenue
    FROM fact_sales f
    JOIN dim_date d
      ON f.date_id = d.date_id
    GROUP BY d.year_sold, d.month_sold
    ORDER BY d.year_sold, d.month_sold
    """

    df_5 = con.execute(_query).df()
    df_5["year_month"] = df_5["year_sold"].astype(str) + "-" + df_5["month_sold"].astype(str)
    df_5
    return (df_5,)


@app.cell
def _(df_5, plt):
    plt.figure(figsize=(12,5))
    plt.plot(df_5["year_month"], df_5["revenue"], marker='o')
    plt.xticks(rotation=45)
    plt.title("Monthly Revenue Trend")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # ✅ Cell 6 — ONLINE vs INSTORE Revenue

    ## Question

    Which channel earns more?

    **Result:** INSTORE **131,214**, ONLINE 124,521 (51% vs 49%): the two channels are almost equal.

    """)
    return


@app.cell
def _(con):
    _query = """
    SELECT
        sale_type,
        SUM(final_price) AS revenue
    FROM fact_sales
    GROUP BY sale_type
    """

    df_6 = con.execute(_query).df()
    df_6
    return (df_6,)


@app.cell
def _(df_6, plt):
    plt.figure(figsize=(6,4))
    plt.bar(df_6["sale_type"], df_6["revenue"])
    plt.title("Revenue by Channel")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # ✅ Cell 7 — Book Format Performance

    ## Question

    Which format earns the most?

    **Result:** hard copy **112,397** (44%), paperback 78,126, soft copy 65,213.
    But the formats sell almost the **same number** of copies (3,417 / 3,299 / 3,284): hard copy earns more only because its average sale is higher
    (32.89 vs 23.68 vs 19.86). Soft copies are **not** growing here; a pie chart of revenue hides that.

    """)
    return


@app.cell
def _(con):
    _query = """
    SELECT
        f2.format_name,
        SUM(f.final_price) AS revenue
    FROM fact_sales f
    JOIN dim_book_format f2
      ON f.format_id = f2.format_id
    GROUP BY f2.format_name
    ORDER BY revenue DESC
    """

    df_7 = con.execute(_query).df()
    df_7
    return (df_7,)


@app.cell
def _(df_7, plt):
    plt.figure(figsize=(6,4))
    plt.pie(df_7["revenue"], labels=df_7["format_name"], autopct='%1.1f%%')
    plt.title("Revenue by Format")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # ✅ Cell 8 — Discount Impact Analysis

    ## Question

    What do discounts do?

    **Result:** 57.2% of sales have a discount (average 3.44). Average revenue: 27.62 without, 24.04 with a discount.
    The list prices are the same in both groups (27.62 vs 27.48), so the 3.58 gap **is** the discount itself.
    Whether discounts bring **more** sales cannot be answered here: we have no comparison of the same books with and without a discount.

    """)
    return


@app.cell
def _(con):
    _query = """
    SELECT
        CASE 
            WHEN discount = 0 THEN 'No Discount'
            ELSE 'Discount Applied'
        END AS discount_flag,
        AVG(final_price) AS avg_revenue
    FROM fact_sales
    GROUP BY discount_flag
    """

    df_8 = con.execute(_query).df()
    df_8
    return (df_8,)


@app.cell
def _(df_8, plt):
    plt.figure(figsize=(6,4))
    plt.bar(df_8["discount_flag"], df_8["avg_revenue"])
    plt.title("Discount Impact")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # ✅ Cell 9 — Revenue by Day of Week

    ## Question

    Do weekdays differ?

    **Result:** from Monday (34,243, the lowest) to Wednesday (37,949, the highest): about 10% apart, with no weekend pattern.
    The query orders the days Monday → Sunday with `dayofweek` (alphabetical order would put Friday first).

    """)
    return


@app.cell
def _(con):
    _query = """
    SELECT
        d.day_name,
        SUM(f.final_price) AS revenue
    FROM fact_sales f
    JOIN dim_date d
      ON f.date_id = d.date_id
    GROUP BY d.day_name
    ORDER BY MIN(dayofweek(d.date_sold) + 6) % 7      -- Monday first
    """

    df_9 = con.execute(_query).df()
    df_9
    return (df_9,)


@app.cell
def _(df_9, plt):
    plt.figure(figsize=(8,4))
    plt.bar(df_9["day_name"], df_9["revenue"])
    plt.xticks(rotation=45)
    plt.title("Revenue by Day")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # ✅ Cell 10 — Genre vs Channel Analysis (OLAP Cube Slice)

    ## Question

    Do genres sell differently online and in store?

    **Result:** no: every genre splits about 50/50 between the channels (the largest relative gap is Mystery: 10,085 in store vs 9,075 online, 11%).
    Two dimensions at once (genre × channel) is a **slice of the OLAP cube** (week 4).

    """)
    return


@app.cell
def _(con):
    _query = """
    SELECT
        b.book_genre,
        f.sale_type,
        SUM(f.final_price) AS revenue
    FROM fact_sales f
    JOIN dim_book b
      ON f.book_id = b.book_id
    GROUP BY b.book_genre, f.sale_type
    ORDER BY b.book_genre
    """

    df_10 = con.execute(_query).df()
    df_10
    return (df_10,)


@app.cell
def _(df_10, plt):
    pivot_df = df_10.pivot(index="book_genre", columns="sale_type", values="revenue")

    pivot_df.plot(kind="bar", figsize=(10,5))
    plt.title("Genre vs Channel Revenue")
    plt.xticks(rotation=45)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Extra tables: the same questions with counts

    Revenue alone hides **why** a group is big. These three tables add `COUNT(*)` (transactions) next to `SUM(final_price)`:
    by genre, by country and city, and by month and channel. The charts in section 10 use them.
    """)
    return


@app.cell
def _(con):
    # Books Sales by Genre

    q1 = '''
    SELECT
        b.book_genre,
        COUNT(*) AS transactions,
        ROUND(SUM(f.final_price), 2) AS total_revenue
    FROM fact_sales f
    JOIN dim_book b
      ON f.book_id = b.book_id
    GROUP BY b.book_genre
    ORDER BY total_revenue DESC
    '''
    genre_revenue = con.execute(q1).df()
    genre_revenue
    return (genre_revenue,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Book Sales by Country and City
    """)
    return


@app.cell
def _(con):
    q2 = '''
    SELECT
        l.country,
        l.city,
        COUNT(*) AS transactions,
        ROUND(SUM(f.final_price), 2) AS total_revenue
    FROM fact_sales f
    JOIN dim_location l
      ON f.location_id = l.location_id
    GROUP BY l.country, l.city
    ORDER BY total_revenue DESC
    LIMIT 15
    '''
    location_revenue = con.execute(q2).df()
    location_revenue
    return (location_revenue,)


@app.cell
def _(con):
    # Book sales by Year, Month, and Sale_Type

    q3 = '''
    SELECT
        d.year_sold,
        d.month_sold,
        f.sale_type,
        COUNT(*) AS transactions,
        ROUND(SUM(f.final_price), 2) AS total_revenue
    FROM fact_sales f
    JOIN dim_date d
      ON f.date_id = d.date_id
    GROUP BY d.year_sold, d.month_sold, f.sale_type
    ORDER BY d.year_sold, d.month_sold, f.sale_type
    '''
    monthly_trend = con.execute(q3).df()
    monthly_trend.head(20)
    return (monthly_trend,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Optional visualization

    For a first demo, a few simple plots help students see the value of the star schema quickly.
    """)
    return


@app.cell
def _(genre_revenue, plt):
    plt.figure(figsize=(10, 5))
    plt.bar(genre_revenue["book_genre"], genre_revenue["total_revenue"])
    plt.title("Revenue by Book Genre")
    plt.xlabel("Genre")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(location_revenue, plt):
    top_cities = location_revenue.head(10)

    plt.figure(figsize=(10, 5))
    plt.bar(top_cities["city"], top_cities["total_revenue"])
    plt.title("Top Cities by Revenue")
    plt.xlabel("City")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(monthly_trend, plt):
    monthly_online = monthly_trend[monthly_trend["sale_type"] == "ONLINE"].copy()
    monthly_online["year_month"] = (
        monthly_online["year_sold"].astype(str) + "-" +
        monthly_online["month_sold"].astype(str).str.zfill(2)
    )

    plt.figure(figsize=(12, 5))
    plt.plot(monthly_online["year_month"], monthly_online["total_revenue"], marker="o")
    plt.title("Monthly ONLINE Revenue")
    plt.xlabel("Year-Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 11. What we learned

    This POC shows the core data warehousing flow:

    1. Start with operational data
    2. Identify descriptive entities for dimensions
    3. Identify measurable events for the fact table
    4. Build ETL to transform transactional data into a star schema
    5. Use the star schema for reporting and BI SQL

    This is a strong first demo for teaching dimensional modeling.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 12. Suggested next steps

    To extend this demo, you could add:

    - `dim_sale_type` as a separate dimension
    - `quantity_sold` values greater than 1
    - inventory and publisher tables
    - slowly changing dimensions
    - a gold reporting layer with pre-aggregated marts
    - dashboarding in Power BI, Tableau, or Streamlit
    """)
    return


if __name__ == "__main__":
    app.run()
