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
    # Medallion Architecture <br> for a Messy Retail Sales Dataset
    ## Raw → Bronze → Silver → Gold

    This revised notebook teaches the pipeline **one business rule at a time**.

    ## Business Rules
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

    We will show for each rule:
    - **why**
    - **how**
    - **SQL**
    - **layer-to-layer transformation**
    - **audit query / plot**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 01 — Import libraries and connect to DuckDB

    ### Why
    We need a small local analytics engine for classroom use.

    ### What
    Import libraries and open the DuckDB database.
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import matplotlib.pyplot as plt

    return duckdb, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Create a DuckDB Connection object:
    """)
    return


@app.cell
def _(duckdb):
    con = duckdb.connect("medallion_messy_sales.duckdb")
    print("Connected to DuckDB.")
    print("DuckDB version: ", duckdb.__version__)
    print("DuckDB Connection object: ", con)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 02 — Define the source CSV file

    ### Why
    A pipeline should be easy to rerun against a new batch.

    ### What
    Set the CSV file name in one place.
    """)
    return


@app.cell
def _():
    csv_file = "sale_records_1400_messy.csv"
    print("Source file:", csv_file)
    return (csv_file,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 03 — Preview the raw file

    ### Why
    Students should see the messy source before transformations.

    ### What
    Read the file as strings and inspect sample rows.
    """)
    return


@app.cell
def _(csv_file, pd):
    raw_preview = pd.read_csv(csv_file, dtype=str)
    raw_preview.head(12)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 04 — Create schemas

    ### Why
    Schemas separate the warehouse layers clearly.

    ### What
    Create `raw`, `bronze`, `silver`, and `gold`.
    """)
    return


@app.cell
def _(con):
    con.execute("CREATE SCHEMA IF NOT EXISTS raw;").fetchall()
    con.execute("CREATE SCHEMA IF NOT EXISTS bronze;").fetchall()
    con.execute("CREATE SCHEMA IF NOT EXISTS silver;").fetchall()
    con.execute("CREATE SCHEMA IF NOT EXISTS gold;").fetchall()


    con.execute("""
    SELECT schema_name
    FROM information_schema.schemata
    WHERE schema_name in ('raw', 'bronze', 'silver', 'gold')
    ORDER BY schema_name;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Raw and Bronze

    Bronze preserves the landed source before business cleanup.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 05 — Load the CSV into `raw.sales_file`

    ### Why
    We want a warehouse copy of the exact input.

    ### What
    Load the CSV as text using `all_varchar=true`.
    """)
    return


@app.cell
def _(con, csv_file):
    con.execute(f"""
    CREATE OR REPLACE TABLE raw.sales_file AS
    SELECT
        ROW_NUMBER() OVER () AS raw_row_num,
        *
    FROM read_csv_auto('{csv_file}', header=true, all_varchar=true);
    """).fetchall()

    con.execute("""
    SELECT COUNT(*) AS raw_rows 
    FROM raw.sales_file
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 06 — Create `bronze.sales_raw`

    ### Why
    Bronze is the warehouse landing layer.

    ### What
    Copy raw data into Bronze.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE bronze.sales_raw AS
    SELECT *
    FROM raw.sales_file;
    """).fetchall()

    con.execute("""
    SELECT COUNT(*) AS bronze_rows 
    FROM bronze.sales_raw
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 07 — Bronze profiling

    ### Why
    Measure the mess before cleanup.

    ### What
    Count missing IDs, missing products, missing names, missing dates, and duplicates.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT 'total_rows' AS metric, COUNT(*) AS value
    FROM bronze.sales_raw

    UNION ALL

    SELECT 'missing_sale_id_rows',
           SUM(CASE WHEN NULLIF(TRIM(sale_id), '') IS NULL THEN 1 ELSE 0 END)
    FROM bronze.sales_raw

    UNION ALL

    SELECT 'missing_product_rows',
           SUM(CASE WHEN NULLIF(TRIM(product), '') IS NULL THEN 1 ELSE 0 END)
    FROM bronze.sales_raw

    UNION ALL

    SELECT 'missing_customer_name_rows',
           SUM(CASE WHEN NULLIF(TRIM(customer_name), '') IS NULL THEN 1 ELSE 0 END)
    FROM bronze.sales_raw

    UNION ALL

    SELECT 'missing_sale_date_rows',
           SUM(CASE WHEN NULLIF(TRIM(sale_date), '') IS NULL THEN 1 ELSE 0 END)
    FROM bronze.sales_raw

    UNION ALL

    SELECT 'extra_duplicate_rows',
           COALESCE((
               SELECT SUM(cnt - 1)
               FROM (
                   SELECT
                       sale_id, sale_type, product, customer_name, customer_email,
                       customer_country, quantity, unit_price, discount, store_location, sale_date,
                       COUNT(*) AS cnt
                   FROM bronze.sales_raw
                   GROUP BY
                       sale_id, sale_type, product, customer_name, customer_email,
                       customer_country, quantity, unit_price, discount, store_location, sale_date
                   HAVING COUNT(*) > 1
               )
           ), 0);
    """).df()
    return


@app.cell
def _(con, plt):
    df_bronze = con.execute("""
    WITH dups AS (
        SELECT
            sale_id, sale_type, product, customer_name, customer_email,
            customer_country, quantity, unit_price, discount, store_location, sale_date,
            COUNT(*) AS cnt
        FROM bronze.sales_raw
        GROUP BY
            sale_id, sale_type, product, customer_name, customer_email,
            customer_country, quantity, unit_price, discount, store_location, sale_date
        HAVING COUNT(*) > 1
    )
    SELECT 'missing_sale_id' AS issue, SUM(CASE WHEN NULLIF(TRIM(sale_id), '') IS NULL THEN 1 ELSE 0 END) AS issue_count FROM bronze.sales_raw
    UNION ALL
    SELECT 'missing_product', SUM(CASE WHEN NULLIF(TRIM(product), '') IS NULL THEN 1 ELSE 0 END) FROM bronze.sales_raw
    UNION ALL
    SELECT 'missing_customer_name', SUM(CASE WHEN NULLIF(TRIM(customer_name), '') IS NULL THEN 1 ELSE 0 END) FROM bronze.sales_raw
    UNION ALL
    SELECT 'missing_sale_date', SUM(CASE WHEN NULLIF(TRIM(sale_date), '') IS NULL THEN 1 ELSE 0 END) FROM bronze.sales_raw
    UNION ALL
    SELECT 'extra_duplicate_rows', COALESCE((SELECT SUM(cnt - 1) FROM dups), 0);
    """).df()

    plt.figure(figsize=(9,4))
    plt.bar(df_bronze["issue"], df_bronze["issue_count"])
    plt.title("Bronze Data Quality Issues")
    plt.xlabel("Issue")
    plt.ylabel("Count")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Silver Layer: Business Rules One-by-One
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 08 — Rule 7: Deduplicate exact duplicate rows

    ### Why
    Duplicates inflate counts and revenue.

    ### How
    Use `SELECT DISTINCT` across all source columns.

    ### Transformation
    `bronze.sales_raw` → `silver.step01_dedup`
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.step01_dedup AS
    SELECT DISTINCT
        sale_id, sale_type, product, customer_name, customer_email,
        customer_country, quantity, unit_price, discount, store_location, sale_date
    FROM bronze.sales_raw;
    """).fetchall()

    con.execute("""
    SELECT
        (SELECT COUNT(*) FROM bronze.sales_raw) AS bronze_rows,
        (SELECT COUNT(*) FROM silver.step01_dedup) AS dedup_rows,
        (SELECT COUNT(*) FROM bronze.sales_raw) - (SELECT COUNT(*) FROM silver.step01_dedup) AS duplicates_removed;
    """).df()


    con.execute("""
    WITH counts AS (
       SELECT
        (SELECT COUNT(*) FROM bronze.sales_raw) AS bronze_rows,
        (SELECT COUNT(*) FROM silver.step01_dedup) AS dedup_rows
    )
    SELECT bronze_rows,
           dedup_rows,
           (bronze_rows - dedup_rows) AS duplicates_removed
    FROM counts
    """).df()
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT 'bronze_raw' AS stage, COUNT(*) AS row_count FROM bronze.sales_raw
    UNION ALL
    SELECT 'after_dedup', COUNT(*) FROM silver.step01_dedup;
    """).df()

    plt.figure(figsize=(6,4))
    plt.bar(_df["stage"], _df["row_count"])
    plt.title("Before and After Deduplication")
    plt.xlabel("Stage")
    plt.ylabel("Rows")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 09 — Standardize strings and safe casts

    ### Why
    We want consistent text and safe numeric parsing before enforcing more rules.

    ### Transformation
    `silver.step01_dedup` → `silver.step02_standardized`
    """)
    return


@app.cell
def _(con):
    ##----------------------------------------------------
    ## Function: NULLIF(expression1, expression2)
    ##
    ## Equivalent: CASE WHEN expression1 = expression2 
    ##                     THEN NULL 
    ##                     ELSE expression1 
    ##             END
    ##----------------------------------------------------

    con.execute("""
    CREATE OR REPLACE TABLE silver.step02_standardized AS
    SELECT
        -- Remove leading/trailing spaces from sale_id
        -- If the value becomes an empty string, 
        -- replace it with NULL
        NULLIF(TRIM(sale_id), '') AS sale_id_raw,

        -- Clean sale_type by removing extra spaces
        -- Convert values such as 'online' or 'InStore' 
        -- into a standard UPPERCASE format
        UPPER(NULLIF(TRIM(sale_type), '')) AS sale_type,

        -- Clean product names and standardize them to uppercase
        -- Example: 'laptop', ' Laptop ' → 'LAPTOP'
        UPPER(NULLIF(TRIM(product), '')) AS product,

        -- Remove unnecessary spaces from customer_name
        -- Keep the original letter casing for readability
        NULLIF(TRIM(customer_name), '') AS customer_name,

        -- Clean customer_email and convert to lowercase
        -- Emails are usually stored in lowercase for consistency
        LOWER(NULLIF(TRIM(customer_email), '')) AS customer_email,

        -- Clean customer_country and convert to uppercase
        -- Example: 'usa', 'UsA' → 'USA'
        UPPER(NULLIF(TRIM(customer_country), '')) AS customer_country,

        -- Remove spaces from quantity
        -- Convert the cleaned value into INTEGER safely using TRY_CAST
        -- Invalid numeric values will become NULL instead of causing an error
        TRY_CAST(NULLIF(TRIM(quantity), '') AS INTEGER) AS quantity,

        -- Remove spaces from unit_price
        -- Convert the cleaned value into DOUBLE safely using TRY_CAST
        -- Invalid prices will become NULL
        TRY_CAST(NULLIF(TRIM(unit_price), '') AS DOUBLE) AS unit_price,

        -- Remove extra spaces from discount field
        -- Keep original text format for later processing
        NULLIF(TRIM(discount), '') AS discount_raw,

        -- Clean store_location values and standardize to uppercase
        -- Example: 'new york', 'New York' → 'NEW YORK'
        UPPER(NULLIF(TRIM(store_location), '')) AS store_location,

        -- Remove extra spaces from sale_date
        -- Keep as raw text for now because dates may have mixed formats
        NULLIF(TRIM(sale_date), '') AS sale_date_raw

    FROM silver.step01_dedup;
    """).fetchall()

    con.execute("""
    SELECT * 
    FROM silver.step02_standardized 
    LIMIT 10
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 10 — Rule 4: Fix discount values

    ### Why
    Missing or negative discount should be treated as no discount.

    ### How
    Create a cleaned numeric `discount`.

    ### Transformation
    `silver.step02_standardized` → `silver.step03_discount_fixed`
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.step03_discount_fixed AS
    SELECT
        *,
        CASE
            WHEN TRY_CAST(discount_raw AS DOUBLE) IS NULL THEN 0.00
            WHEN TRY_CAST(discount_raw AS DOUBLE) < 0 THEN 0.00
            ELSE TRY_CAST(discount_raw AS DOUBLE)
        END AS discount
    FROM silver.step02_standardized;
    """).fetchall()

    ## Prfile the discount column
    con.execute("""
    SELECT
        SUM(CASE WHEN discount_raw IS NULL THEN 1 ELSE 0 END) AS missing_discount_rows,
        SUM(CASE WHEN TRY_CAST(discount_raw AS DOUBLE) < 0 THEN 1 ELSE 0 END) AS negative_discount_rows,
        SUM(CASE WHEN discount = 0.00 THEN 1 ELSE 0 END) AS final_zero_discount_rows
    FROM silver.step03_discount_fixed;
    """).df()
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT 'missing_discount' AS category, SUM(CASE WHEN discount_raw IS NULL THEN 1 ELSE 0 END) AS row_count
    FROM silver.step03_discount_fixed
    UNION ALL
    SELECT 'negative_discount', SUM(CASE WHEN TRY_CAST(discount_raw AS DOUBLE) < 0 THEN 1 ELSE 0 END)
    FROM silver.step03_discount_fixed
    UNION ALL
    SELECT 'zero_after_fix', SUM(CASE WHEN discount = 0.00 THEN 1 ELSE 0 END)
    FROM silver.step03_discount_fixed;
    """).df()

    plt.figure(figsize=(8,4))
    plt.bar(_df["category"], _df["row_count"])
    plt.title("Discount Cleanup")
    plt.xlabel("Category")
    plt.ylabel("Rows")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 11 — Rules 5 and 6: Parse allowed date formats

    ### Why
    Only two sale date formats are valid:
    - `MM/DD/YYYY`
    - `YYYY-MM-DD`

    Missing or invalid dates must be dropped later.

    ### How
    Use `TRY_STRPTIME` for both formats and `COALESCE`.

    ### Transformation
    `silver.step03_discount_fixed` → `silver.step04_date_parsed`
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.step04_date_parsed AS
    SELECT
        *,
        COALESCE(
            TRY_STRPTIME(sale_date_raw, '%m/%d/%Y')::DATE,
            TRY_STRPTIME(sale_date_raw, '%Y-%m-%d')::DATE
        ) AS sale_date
    FROM silver.step03_discount_fixed;
    """).fetchall()


    con.execute("""
    SELECT
        COUNT(*) AS rows_checked,
        SUM(CASE WHEN sale_date IS NULL THEN 1 ELSE 0 END) AS invalid_or_missing_sale_date_rows
    FROM silver.step04_date_parsed;
    """).df()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT sale_date_raw, 
           COUNT(*) AS row_count
    FROM silver.step04_date_parsed
    WHERE sale_date IS NULL
    GROUP BY sale_date_raw
    ORDER BY row_count DESC, sale_date_raw
    LIMIT 20;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 12 — Rules 2, 3, and 6: Build rejected records

    ### Why
    These rows are not valid for warehousing:
    - missing product
    - missing customer name
    - invalid/missing sale date

    ### Important
    Rejected rows are **not** cancelled.

    ### Transformation
    `silver.step04_date_parsed` → `silver.rejected_records`
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.rejected_records AS
    SELECT
        *,
        CASE
            WHEN product IS NULL THEN 'REJECT_MISSING_PRODUCT'
            WHEN customer_name IS NULL THEN 'REJECT_MISSING_CUSTOMER_NAME'
            WHEN sale_date IS NULL THEN 'REJECT_INVALID_OR_MISSING_SALE_DATE'
            ELSE 'REJECT_OTHER'
        END AS reject_reason
    FROM silver.step04_date_parsed
    WHERE product IS NULL OR customer_name IS NULL OR sale_date IS NULL;
    """).fetchall()

    con.execute("""
    SELECT reject_reason, COUNT(*) AS row_count
    FROM silver.rejected_records
    GROUP BY reject_reason
    ORDER BY row_count DESC;
    """).df()
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT reject_reason, COUNT(*) AS row_count
    FROM silver.rejected_records
    GROUP BY reject_reason
    ORDER BY row_count DESC;
    """).df()

    plt.figure(figsize=(9,4))
    plt.bar(_df["reject_reason"], _df["row_count"])
    plt.title("Rejected Records by Reason")
    plt.xlabel("Reject Reason")
    plt.ylabel("Rows")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 13 — Rule 1: Build cancelled transactions

    ### Why
    Business wants to know how many transactions were cancelled and for which products.

    ### Important
    A row counts as cancelled only if it is otherwise valid.
    Rejected rows do not become cancelled rows.

    ### Transformation
    `silver.step04_date_parsed` → `silver.cancelled_transactions`
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.cancelled_transactions AS
    SELECT
        sale_type, product, customer_name, customer_email, customer_country,
        quantity, unit_price, discount, store_location, sale_date
    FROM silver.step04_date_parsed
    WHERE sale_id_raw IS NULL
      AND product IS NOT NULL
      AND customer_name IS NOT NULL
      AND sale_date IS NOT NULL;
    """).fetchall()

    con.execute("""
    SELECT COUNT(*) AS cancelled_transaction_rows 
    FROM silver.cancelled_transactions
    """).df()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT product, 
           COUNT(*) AS cancelled_count
    FROM silver.cancelled_transactions
    GROUP BY product
    ORDER BY cancelled_count DESC;
    """).df()
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT product, COUNT(*) AS cancelled_count
    FROM silver.cancelled_transactions
    GROUP BY product
    ORDER BY cancelled_count DESC;
    """).df()

    plt.figure(figsize=(8,4))
    plt.bar(_df["product"], _df["cancelled_count"])
    plt.title("Cancelled Transactions by Product")
    plt.xlabel("Product")
    plt.ylabel("Cancelled Count")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 14 — Build valid non-cancelled rows

    ### Why
    Gold should use only trusted, valid, non-cancelled rows.

    ### Transformation
    `silver.step04_date_parsed` → `silver.step05_valid_non_cancelled`
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.step05_valid_non_cancelled AS
    SELECT *
    FROM silver.step04_date_parsed
    WHERE sale_id_raw IS NOT NULL
      AND product IS NOT NULL
      AND customer_name IS NOT NULL
      AND sale_date IS NOT NULL;
    """).fetchall()

    con.execute("""
    SELECT COUNT(*) AS valid_non_cancelled_rows 
    FROM silver.step05_valid_non_cancelled
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 15 — Rule 8: Compute final sale price

    ### Why
    This is the trusted monetary measure used in analytics.

    ### Transformation
    `silver.step05_valid_non_cancelled` → `silver.sales_clean`
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.sales_clean AS
    SELECT
        sale_id_raw AS sale_id,
        sale_type,
        product,
        customer_name,
        customer_email,
        customer_country,
        quantity,
        unit_price,
        discount,
        store_location,
        sale_date,
        (quantity * unit_price) - discount AS final_sale_price
    FROM silver.step05_valid_non_cancelled;
    """).fetchall()

    con.execute("SELECT * FROM silver.sales_clean LIMIT 10").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 16 — Audit all outcomes together

    ### Why
    Students need one summary of the full pipeline.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT 'bronze_raw_rows' AS category, COUNT(*) AS row_count FROM bronze.sales_raw
    UNION ALL
    SELECT 'after_dedup', COUNT(*) FROM silver.step01_dedup
    UNION ALL
    SELECT 'rejected_rows', COUNT(*) FROM silver.rejected_records
    UNION ALL
    SELECT 'cancelled_rows', COUNT(*) FROM silver.cancelled_transactions
    UNION ALL
    SELECT 'trusted_sales_clean', COUNT(*) FROM silver.sales_clean
    ORDER BY category;
    """).df()
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT 'bronze_raw_rows' AS category, COUNT(*) AS row_count FROM bronze.sales_raw
    UNION ALL
    SELECT 'after_dedup', COUNT(*) FROM silver.step01_dedup
    UNION ALL
    SELECT 'rejected_rows', COUNT(*) FROM silver.rejected_records
    UNION ALL
    SELECT 'cancelled_rows', COUNT(*) FROM silver.cancelled_transactions
    UNION ALL
    SELECT 'trusted_sales_clean', COUNT(*) FROM silver.sales_clean;
    """).df()

    plt.figure(figsize=(9,4))
    plt.bar(_df["category"], _df["row_count"])
    plt.title("Pipeline Audit Funnel")
    plt.xlabel("Stage")
    plt.ylabel("Rows")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Gold Layer

    ## Gold organizes trusted Silver data <br> into a star schema for OLAP.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 17 — Create Gold dimensions and fact table

    ### Why
    The Gold layer is optimized for analytics and reporting.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Build `gold.dim_customer`
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE gold.dim_customer AS
    SELECT
        ROW_NUMBER() OVER (ORDER BY customer_email) AS customer_key,
        customer_name,
        customer_email,
        customer_country
    FROM (
        SELECT DISTINCT customer_name, customer_email, customer_country
        FROM silver.sales_clean
    );
    """).fetchall()
    return


@app.cell
def _(con):
    con.sql("""
    SELECT COUNT(*) as number_of_customers 
    FROM gold.dim_customer
    """).show()
    return


@app.cell
def _(con):
    con.sql("""
    SELECT * 
    FROM gold.dim_customer
    LIMIT 5
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Build `gold.dim_product`
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE gold.dim_product AS
    SELECT
        ROW_NUMBER() OVER (ORDER BY product) AS product_key,
        product
    FROM (
        SELECT DISTINCT product
        FROM silver.sales_clean
    );
    """).fetchall()
    return


@app.cell
def _(con):
    con.sql("""
    SELECT COUNT(*) as number_of_products
    FROM gold.dim_product
    """).show()
    return


@app.cell
def _(con):
    con.sql("""
    SELECT * 
    FROM gold.dim_product
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Build `gold.dim_store`
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE gold.dim_store AS
    SELECT
        ROW_NUMBER() OVER (ORDER BY store_location) AS store_key,
        store_location
    FROM (
        SELECT DISTINCT store_location
        FROM silver.sales_clean
    );
    """).fetchall()
    return


@app.cell
def _(con):
    con.sql("""
    SELECT COUNT(*) as number_of_stores
    FROM gold.dim_store
    """).show()
    return


@app.cell
def _(con):
    con.sql("""
    SELECT * 
    FROM gold.dim_store
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Build `gold.dim_date`
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE gold.dim_date AS
    SELECT
        ROW_NUMBER() OVER (ORDER BY sale_date) AS date_key,
        sale_date AS full_date,
        EXTRACT(YEAR FROM sale_date) AS year_num,
        EXTRACT(QUARTER FROM sale_date) AS quarter_num,
        EXTRACT(MONTH FROM sale_date) AS month_num,
        STRFTIME(sale_date, '%B') AS month_name,
        EXTRACT(DAY FROM sale_date) AS day_num,
        STRFTIME(sale_date, '%A') AS day_name,
        STRFTIME(sale_date, '%Y-%m') AS year_month
    FROM (
        SELECT DISTINCT sale_date
        FROM silver.sales_clean
    );
    """).fetchall()
    return


@app.cell
def _(con):
    con.sql("""
    SELECT COUNT(*) as number_of_dates
    FROM gold.dim_date
    """).show()
    return


@app.cell
def _(con):
    con.sql("""
    SELECT * 
    FROM gold.dim_date
    LIMIT 5
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Build `gold.fact_sales`
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE gold.fact_sales AS
    SELECT
        s.sale_id,
        dc.customer_key,
        dp.product_key,
        ds.store_key,
        dd.date_key,
        s.sale_type,
        s.quantity,
        s.unit_price,
        s.discount,
        s.final_sale_price
    FROM silver.sales_clean s
    JOIN gold.dim_customer dc ON s.customer_email = dc.customer_email
    JOIN gold.dim_product dp ON s.product = dp.product
    JOIN gold.dim_store ds ON s.store_location = ds.store_location
    JOIN gold.dim_date dd ON s.sale_date = dd.full_date;
    """).fetchall()
    return


@app.cell
def _(con):
    con.sql("""
    SELECT COUNT(*) as number_of_sales_transaction
    FROM gold.fact_sales
    """).show()
    return


@app.cell
def _(con):
    con.sql("""
    SELECT * 
    FROM gold.fact_sales
    LIMIT 5
    """).show()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'gold'
    ORDER BY table_name;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Star Schema

    ```
                      dim_product
                           |
                           |
                           |
    dim_customer ----- fact_sales ----- dim_date
                           |
                           |
                           |
                        dim_store
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 18 — OLAP 1: Total final sales by product

    ### Why
    This query demonstrates a common OLAP-style business insight on the Gold layer.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT p.product, 
           ROUND(SUM(f.final_sale_price), 2) AS total_final_sales
    FROM gold.fact_sales f
    JOIN gold.dim_product p ON f.product_key = p.product_key
    GROUP BY p.product
    ORDER BY total_final_sales DESC;
    """).df()
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT p.product, 
           ROUND(SUM(f.final_sale_price), 2) AS total_final_sales
    FROM gold.fact_sales f
    JOIN gold.dim_product p ON f.product_key = p.product_key
    GROUP BY p.product
    ORDER BY total_final_sales DESC;
    """).df()

    plt.figure(figsize=(9,4))
    plt.bar(_df["product"], _df["total_final_sales"])
    plt.title("OLAP 1: Total final sales by product")
    plt.xlabel("product")
    plt.ylabel("total_final_sales")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 20 — OLAP 2: Monthly sales trend

    ### Why
    This query demonstrates a common OLAP-style business insight on the Gold layer.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT d.year_month, 
           ROUND(SUM(f.final_sale_price), 2) AS total_final_sales
    FROM gold.fact_sales f
    JOIN gold.dim_date d ON f.date_key = d.date_key
    GROUP BY d.year_month
    ORDER BY d.year_month;
    """).df()
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT d.year_month, ROUND(SUM(f.final_sale_price), 2) AS total_final_sales
    FROM gold.fact_sales f
    JOIN gold.dim_date d ON f.date_key = d.date_key
    GROUP BY d.year_month
    ORDER BY d.year_month;
    """).df()

    plt.figure(figsize=(9,4))
    plt.plot(_df["year_month"], _df["total_final_sales"])
    plt.title("OLAP 2: Monthly sales trend")
    plt.xlabel("year_month")
    plt.ylabel("total_final_sales")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 22 — OLAP 3: Sales by customer country

    ### Why
    This query demonstrates a common OLAP-style business insight on the Gold layer.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT c.customer_country, 
           ROUND(SUM(f.final_sale_price), 2) AS total_final_sales
    FROM gold.fact_sales f
    JOIN gold.dim_customer c ON f.customer_key = c.customer_key
    GROUP BY c.customer_country
    ORDER BY total_final_sales DESC;
    """).df()
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT c.customer_country, ROUND(SUM(f.final_sale_price), 2) AS total_final_sales
    FROM gold.fact_sales f
    JOIN gold.dim_customer c ON f.customer_key = c.customer_key
    GROUP BY c.customer_country
    ORDER BY total_final_sales DESC;
    """).df()

    plt.figure(figsize=(9,4))
    plt.bar(_df["customer_country"], _df["total_final_sales"])
    plt.title("OLAP 3: Sales by customer country")
    plt.xlabel("customer_country")
    plt.ylabel("total_final_sales")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 24 — OLAP 4: Sales by store location

    ### Why
    This query demonstrates a common OLAP-style business insight on the Gold layer.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT s.store_location, 
           ROUND(SUM(f.final_sale_price), 2) AS total_final_sales, 
           COUNT(*) AS transactions
    FROM gold.fact_sales f
    JOIN gold.dim_store s ON f.store_key = s.store_key
    GROUP BY s.store_location
    ORDER BY total_final_sales DESC;
    """).df()
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT s.store_location, ROUND(SUM(f.final_sale_price), 2) AS total_final_sales, COUNT(*) AS transactions
    FROM gold.fact_sales f
    JOIN gold.dim_store s ON f.store_key = s.store_key
    GROUP BY s.store_location
    ORDER BY total_final_sales DESC;
    """).df()

    plt.figure(figsize=(9,4))
    plt.bar(_df["store_location"], _df["total_final_sales"])
    plt.title("OLAP 4: Sales by store location")
    plt.xlabel("store_location")
    plt.ylabel("total_final_sales")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(con, plt):
    # sales by store location as a Pie Chart
    _df = con.execute("""
    SELECT 
        s.store_location, 
        ROUND(SUM(f.final_sale_price), 2) AS total_final_sales, 
        COUNT(*) AS transactions
    FROM gold.fact_sales f
    JOIN gold.dim_store s 
      ON f.store_key = s.store_key
    GROUP BY s.store_location
    ORDER BY total_final_sales DESC;
    """).df()

    plt.figure(figsize=(6, 6))

    plt.pie(
        _df["total_final_sales"],
        labels=_df["store_location"],
        autopct='%1.1f%%'
    )

    plt.title("OLAP 4: Sales Distribution by Store Location")

    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 26 — OLAP 5: Channel comparison

    ### Why
    This query demonstrates a common OLAP-style business insight on the Gold layer.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT sale_type, 
           COUNT(*) AS transactions, 
           ROUND(SUM(final_sale_price), 2) AS total_final_sales, 
           ROUND(AVG(final_sale_price), 2) AS avg_transaction_value
    FROM gold.fact_sales
    GROUP BY sale_type
    ORDER BY total_final_sales DESC;
    """).df()
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT sale_type, 
           COUNT(*) AS transactions, 
           ROUND(SUM(final_sale_price), 2) AS total_final_sales, 
           ROUND(AVG(final_sale_price), 2) AS avg_transaction_value
    FROM gold.fact_sales
    GROUP BY sale_type
    ORDER BY total_final_sales DESC;
    """).df()

    plt.figure(figsize=(9,4))
    plt.bar(_df["sale_type"], _df["total_final_sales"])
    plt.title("OLAP 5: Channel comparison")
    plt.xlabel("sale_type")
    plt.ylabel("total_final_sales")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 28 — OLAP 6: Top 10 customers by final sales

    ### Why
    This query demonstrates a common OLAP-style business insight on the Gold layer.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT c.customer_name, 
           c.customer_email, 
           ROUND(SUM(f.final_sale_price), 2) AS total_final_sales, 
           COUNT(*) AS transactions
    FROM gold.fact_sales f
    JOIN gold.dim_customer c ON f.customer_key = c.customer_key
    GROUP BY c.customer_name, c.customer_email
    ORDER BY total_final_sales DESC
    LIMIT 10;
    """).df()
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT c.customer_name, 
           c.customer_email, 
           ROUND(SUM(f.final_sale_price), 2) AS total_final_sales, 
           COUNT(*) AS transactions
    FROM gold.fact_sales f
    JOIN gold.dim_customer c ON f.customer_key = c.customer_key
    GROUP BY c.customer_name, c.customer_email
    ORDER BY total_final_sales DESC
    LIMIT 10;
    """).df()

    plt.figure(figsize=(9,4))
    plt.bar(_df["customer_name"], _df["total_final_sales"])
    plt.title("OLAP 6: Top 10 customers by final sales")
    plt.xlabel("customer_name")
    plt.ylabel("total_final_sales")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 30 — OLAP 7: Average discount by product

    ### Why
    This query demonstrates a common OLAP-style business insight on the Gold layer.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT p.product, 
           ROUND(AVG(f.discount), 2) AS avg_discount, 
           ROUND(SUM(f.discount), 2) AS total_discount_given
    FROM gold.fact_sales f
    JOIN gold.dim_product p ON f.product_key = p.product_key
    GROUP BY p.product
    ORDER BY avg_discount DESC;
    """).df()
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT p.product, 
           ROUND(AVG(f.discount), 2) AS avg_discount, 
           ROUND(SUM(f.discount), 2) AS total_discount_given
    FROM gold.fact_sales f
    JOIN gold.dim_product p ON f.product_key = p.product_key
    GROUP BY p.product
    ORDER BY avg_discount DESC;
    """).df()

    plt.figure(figsize=(9,4))
    plt.bar(_df["product"], _df["avg_discount"])
    plt.title("OLAP 7: Average discount by product")
    plt.xlabel("product")
    plt.ylabel("avg_discount")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 32 — OLAP 8: Product by country matrix

    ### Why
    This query demonstrates a common OLAP-style business insight on the Gold layer.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT c.customer_country, 
           p.product, 
           ROUND(SUM(f.final_sale_price), 2) AS total_final_sales
    FROM gold.fact_sales f
    JOIN gold.dim_customer c ON f.customer_key = c.customer_key
    JOIN gold.dim_product p ON f.product_key = p.product_key
    GROUP BY c.customer_country, p.product
    ORDER BY c.customer_country, total_final_sales DESC;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 33 — OLAP 9: Quarterly sales rollup

    ### Why
    This query demonstrates a common OLAP-style business insight on the Gold layer.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT d.year_num, 
           d.quarter_num, 
           ROUND(SUM(f.final_sale_price), 2) AS total_final_sales
    FROM gold.fact_sales f
    JOIN gold.dim_date d ON f.date_key = d.date_key
    GROUP BY d.year_num, d.quarter_num
    ORDER BY d.year_num, d.quarter_num;
    """).df()
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT d.year_num, 
           d.quarter_num, 
           ROUND(SUM(f.final_sale_price), 2) AS total_final_sales
    FROM gold.fact_sales f
    JOIN gold.dim_date d ON f.date_key = d.date_key
    GROUP BY d.year_num, d.quarter_num
    ORDER BY d.year_num, d.quarter_num;
    """).df()

    plt.figure(figsize=(9,4))
    plt.bar(_df["quarter_num"], _df["total_final_sales"])
    plt.title("OLAP 9: Quarterly sales rollup")
    plt.xlabel("quarter_num")
    plt.ylabel("total_final_sales")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 35 — OLAP 10: Month × channel analysis

    ### Why
    This query demonstrates a common OLAP-style business insight on the Gold layer.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT d.year_month, 
           f.sale_type, 
           ROUND(SUM(f.final_sale_price), 2) AS total_final_sales
    FROM gold.fact_sales f
    JOIN gold.dim_date d ON f.date_key = d.date_key
    GROUP BY d.year_month, f.sale_type
    ORDER BY d.year_month, f.sale_type;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Show schemas and tables
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
    SELECT 
        table_schema,
        table_name
    FROM information_schema.tables
    WHERE table_schema IN ('raw','bronze','silver','gold')
    ORDER BY table_schema, table_name;
    """).df()

    # Pretty display grouped by schema
    for schema, group in _df.groupby("table_schema"):
        print(f"\n📦 Schema: {schema.upper()}")
        print("-" * 40)
        print(group["table_name"].to_string(index=False))
    return


@app.cell
def _(con):
    ## Show schemas and tables

    con.execute("""

    SELECT 
        table_schema AS schema,
        table_name AS table
    FROM information_schema.tables
    WHERE table_schema IN ('raw','bronze','silver','gold')
    ORDER BY table_schema, table_name;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Final Notes

    This revised notebook now shows **exactly when and how** each business rule is implemented:

    - **Rule 7** in `silver.step01_dedup`
    - **Rule 4** in `silver.step03_discount_fixed`
    - **Rules 5 and 6** in `silver.step04_date_parsed`
    - **Rules 2, 3, and 6** in `silver.rejected_records`
    - **Rule 1** in `silver.cancelled_transactions`
    - **Rule 8** in `silver.sales_clean`

    This makes the pipeline much easier for students to follow.
    """)
    return


if __name__ == "__main__":
    app.run()
