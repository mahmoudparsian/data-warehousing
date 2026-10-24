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
    # Medallion Architecture Walkthrough
    ## Cleaning the Messy v2 Dataset Step-by-Step

    This notebook teaches how to clean a messy retail sales dataset using a **Medallion Architecture** approach:

    - **Bronze** → landed raw data
    - **Silver** → cleaned, validated, business-rule compliant data
    - **Gold** → analytics-ready data

    The source file used in this lab is:

    ```text
    dataset_messy.csv
    ```

    ---

    ## What this notebook emphasizes

    For every major transformation, we explain:

    - **Why** the rule matters
    - **Business value**
    - **How** the SQL works
    - **What** the plot means

    ---

    ## Core Business Rules Applied

    1. exact duplicates are dropped
    2. invalid or missing `sale_id` → cancelled
    3. missing `sale_type` → reject
    4. missing `sales_channel` → impute `UNKNOWN`
    5. missing `product_name` → reject
    6. invalid or missing `customer_email` → reject
    7. invalid `customer_gender` → impute `UNKNOWN` *(if present in future datasets)*
    8. `quantity` must be integer > 0
    9. `unit_price` must be > 0
    10. invalid / missing `discount` → impute `0.00`
    11. invalid / missing `store_location` → reject
    12. invalid / missing `sale_date` → reject

    This notebook is designed for teaching and discussion, not just execution.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 01 — Import libraries and connect to DuckDB

    ### Why
    We need:
    - SQL execution with DuckDB
    - table inspection with pandas
    - plotting with matplotlib

    ### Business value
    A lightweight warehouse environment lets students focus on **data quality logic** instead of infrastructure.
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import matplotlib.pyplot as plt

    con = duckdb.connect("medallion_v2.duckdb")
    print("Connected to DuckDB.")
    return con, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 02 — Define the source file

    ### Why
    Keeping the CSV path in one variable makes the notebook easier to rerun and modify.

    ### Business value
    In real pipelines, the source file changes by batch or date, so parameterizing the file name is a standard practice.
    """)
    return


@app.cell
def _():
    csv_file = "dataset_messy.csv"
    print("Using source file:", csv_file)
    return (csv_file,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 03 — Preview the raw file with pandas

    ### Why
    Before we apply rules, we need to see the mess.

    ### Business value
    Data profiling starts with inspection. Students should recognize:
    - missing values
    - malformed values
    - suspicious records
    """)
    return


@app.cell
def _(csv_file, pd):
    df_preview = pd.read_csv(csv_file, dtype=str)
    df_preview.head(10)
    return (df_preview,)


@app.cell
def _(df_preview):
    df_preview.shape
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 04 — Create schemas and load Raw/Bronze

    ### Why
    Schemas make the medallion layers visible:
    - `raw`
    - `bronze`
    - `silver`
    - `gold`

    ### Business value
    Schema separation is a design habit that improves maintainability and auditability.
    """)
    return


@app.cell
def _(con, csv_file):
    con.execute("CREATE SCHEMA IF NOT EXISTS raw;").fetchall()
    con.execute("CREATE SCHEMA IF NOT EXISTS bronze;").fetchall()
    con.execute("CREATE SCHEMA IF NOT EXISTS silver;").fetchall()
    con.execute("CREATE SCHEMA IF NOT EXISTS gold;").fetchall()

    con.execute(f"""
    CREATE OR REPLACE TABLE raw.sales_file AS
    SELECT
        ROW_NUMBER() OVER () AS raw_row_num,
        *
    FROM read_csv_auto('{csv_file}', header=true, all_varchar=true);
    """).fetchall()

    con.execute("""
    CREATE OR REPLACE TABLE bronze.sales_raw AS
    SELECT *
    FROM read_csv_auto('dataset_messy.csv');
    """).fetchall()

    con.execute("""
    SELECT COUNT(*) AS bronze_rows 
    FROM bronze.sales_raw
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 05 — Inspect Bronze structure

    ### Why
    We need to know the landed columns and types before cleaning.

    ### Business value
    This is the warehouse equivalent of understanding the source system contract.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        column_name,
        data_type
    FROM information_schema.columns
    WHERE table_schema = 'bronze'
      AND table_name = 'sales_raw'
    ORDER BY ordinal_position;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 06 — Bronze quality profile

    ### Why
    We establish a baseline before transforming anything.

    ### Business value
    This gives stakeholders a quick summary of how messy the incoming batch is.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    WITH dups AS (
        SELECT
            sale_id,
            sale_type,
            sales_channel,
            product_name,
            customer_email,
            customer_country,
            quantity,
            unit_price,
            cost_price,
            discount,
            store_location,
            sale_date,
            COUNT(*) AS cnt
        FROM bronze.sales_raw
        GROUP BY
            sale_id,
            sale_type,
            sales_channel,
            product_name,
            customer_email,
            customer_country,
            quantity,
            unit_price,
            cost_price,
            discount,
            store_location,
            sale_date
        HAVING COUNT(*) > 1
    ),

    metrics AS (
        SELECT
            COUNT(*) AS total_rows,

            SUM(CASE 
                WHEN NULLIF(TRIM(sale_id), '') IS NULL THEN 1 
                ELSE 0 
            END) AS missing_sale_id_rows,

            SUM(CASE 
                WHEN NULLIF(TRIM(product_name), '') IS NULL THEN 1 
                ELSE 0 
            END) AS missing_product_rows,

            SUM(CASE 
                WHEN NULLIF(TRIM(customer_email), '') IS NULL THEN 1 
                ELSE 0 
            END) AS missing_customer_email_rows,

            SUM(CASE 
                WHEN NULLIF(TRIM(store_location), '') IS NULL THEN 1 
                ELSE 0 
            END) AS missing_store_location_rows,

            SUM(CASE 
                WHEN NULLIF(TRIM(sale_date), '') IS NULL THEN 1 
                ELSE 0 
            END) AS missing_sale_date_rows,

            COALESCE(
                (SELECT SUM(cnt - 1) FROM dups),
                0
            ) AS extra_duplicate_rows

        FROM bronze.sales_raw
    )

    SELECT 'total_rows' AS metric, total_rows AS value FROM metrics
    UNION ALL
    SELECT 'missing_sale_id_rows', missing_sale_id_rows FROM metrics
    UNION ALL
    SELECT 'missing_product_rows', missing_product_rows FROM metrics
    UNION ALL
    SELECT 'missing_customer_email_rows', missing_customer_email_rows FROM metrics
    UNION ALL
    SELECT 'missing_store_location_rows', missing_store_location_rows FROM metrics
    UNION ALL
    SELECT 'missing_sale_date_rows', missing_sale_date_rows FROM metrics
    UNION ALL
    SELECT 'extra_duplicate_rows', extra_duplicate_rows FROM metrics;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 07 — Plot Bronze issue counts

    ### Why
    A visual summary makes data quality discussions more concrete.

    ### How to read the plot
    Higher bars indicate where the dataset is dirtiest.

    ### Business value
    The plot helps answer: *Where should the cleaning effort focus first?*
    """)
    return


@app.cell
def _(con, plt):
    df_bronze_issues = con.execute("""
    WITH dups AS (
        SELECT
            sale_id, sale_type, sales_channel, product_name, customer_email,
            customer_country, quantity, unit_price, cost_price, discount, store_location, sale_date,
            COUNT(*) AS cnt
        FROM bronze.sales_raw
        GROUP BY
            sale_id, sale_type, sales_channel, product_name, customer_email,
            customer_country, quantity, unit_price, cost_price, discount, store_location, sale_date
        HAVING COUNT(*) > 1
    )
    SELECT 'missing_sale_id' AS issue, SUM(CASE WHEN NULLIF(TRIM(sale_id), '') IS NULL THEN 1 ELSE 0 END) AS issue_count FROM bronze.sales_raw
    UNION ALL
    SELECT 'missing_product', SUM(CASE WHEN NULLIF(TRIM(product_name), '') IS NULL THEN 1 ELSE 0 END) FROM bronze.sales_raw
    UNION ALL
    SELECT 'missing_customer_email', SUM(CASE WHEN NULLIF(TRIM(customer_email), '') IS NULL THEN 1 ELSE 0 END) FROM bronze.sales_raw
    UNION ALL
    SELECT 'missing_store_location', SUM(CASE WHEN NULLIF(TRIM(store_location), '') IS NULL THEN 1 ELSE 0 END) FROM bronze.sales_raw
    UNION ALL
    SELECT 'missing_sale_date', SUM(CASE WHEN NULLIF(TRIM(sale_date), '') IS NULL THEN 1 ELSE 0 END) FROM bronze.sales_raw
    UNION ALL
    SELECT 'extra_duplicates', COALESCE((SELECT SUM(cnt - 1) FROM dups), 0);
    """).df()

    plt.figure(figsize=(9,4))
    plt.bar(df_bronze_issues["issue"], df_bronze_issues["issue_count"])
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
    ### Plot interpretation

    This plot shows the main quality issues before any Silver cleaning.

    A larger bar means that issue affects more rows. In real data engineering work, this helps prioritize transformations and stakeholder communication.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Silver Layer — Step-by-Step Cleaning

    Silver is where we apply business rules one by one and make every decision auditable.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 08 — Step 1: Deduplicate exact duplicate rows

    ### Why
    Duplicate rows inflate revenue, transactions, and counts.

    ### Business value
    Without deduplication, business dashboards become misleading.

    ### How
    We use `SELECT DISTINCT` across all business columns.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.step01_dedup AS
    SELECT DISTINCT
        -- =========================
        -- CORE
        -- =========================
        sale_id,
        sale_type,
        sales_channel,

        -- =========================
        -- PRODUCT
        -- =========================
        product_name,
        product_category,
        product_brand,

        -- =========================
        -- CUSTOMER
        -- =========================
        customer_name,
        customer_email,
        customer_country,
        customer_city,
        customer_gender,
        customer_segment,

        -- =========================
        -- MEASURES
        -- =========================
        quantity,
        unit_price,
        cost_price,
        discount,

        -- =========================
        -- STORE
        -- =========================
        store_location,
        store_region,
        store_manager,

        -- =========================
        -- DATE / TIME
        -- =========================
        sale_date,
        order_timestamp,
        delivery_date,
        order_status

    FROM bronze.sales_raw;
    """).fetchall()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT COUNT(*) AS num_of_rows_silver_step01_dedup
    FROM silver.step01_dedup 
    """).df()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT * 
    FROM silver.step01_dedup 
    LIMIT 5;
    """).df()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        (SELECT COUNT(*) FROM bronze.sales_raw) AS bronze_rows,
        (SELECT COUNT(*) FROM silver.step01_dedup) AS dedup_rows,
        (SELECT COUNT(*) FROM bronze.sales_raw) - (SELECT COUNT(*) FROM silver.step01_dedup) AS duplicates_removed;
    """).df()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT *
    FROM silver.step01_dedup
    LIMIT 3;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 09 — Step 2: Standardize strings and preserve raw fields

    ### Why
    Before applying rules, we normalize text and create raw helper columns.

    ### Business value
    This makes later transformations safer and easier to audit.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.step02_standardized AS
    SELECT
        -- =========================
        -- RAW KEYS (safe casting)
        -- =========================
        NULLIF(TRIM(CAST(sale_id AS VARCHAR)), '') AS sale_id_raw,

        -- =========================
        -- CORE
        -- =========================
        UPPER(NULLIF(TRIM(CAST(sale_type AS VARCHAR)), '')) AS sale_type,
        UPPER(NULLIF(TRIM(CAST(sales_channel AS VARCHAR)), '')) AS sales_channel,

        -- =========================
        -- PRODUCT
        -- =========================
        UPPER(NULLIF(TRIM(CAST(product_name AS VARCHAR)), '')) AS product_name,
        UPPER(NULLIF(TRIM(CAST(product_category AS VARCHAR)), '')) AS product_category,
        UPPER(NULLIF(TRIM(CAST(product_brand AS VARCHAR)), '')) AS product_brand,

        -- =========================
        -- CUSTOMER
        -- =========================
        TRIM(CAST(customer_name AS VARCHAR)) AS customer_name,
        LOWER(NULLIF(TRIM(CAST(customer_email AS VARCHAR)), '')) AS customer_email,
        UPPER(NULLIF(TRIM(CAST(customer_country AS VARCHAR)), '')) AS customer_country,
        UPPER(NULLIF(TRIM(CAST(customer_city AS VARCHAR)), '')) AS customer_city,
        UPPER(NULLIF(TRIM(CAST(customer_gender AS VARCHAR)), '')) AS customer_gender,
        UPPER(NULLIF(TRIM(CAST(customer_segment AS VARCHAR)), '')) AS customer_segment,

        -- =========================
        -- MEASURES (safe numeric parsing)
        -- =========================
        TRY_CAST(TRIM(CAST(quantity AS VARCHAR)) AS INTEGER) AS quantity,
        TRY_CAST(TRIM(CAST(unit_price AS VARCHAR)) AS DOUBLE) AS unit_price,
        TRY_CAST(TRIM(CAST(cost_price AS VARCHAR)) AS DOUBLE) AS cost_price,

        NULLIF(TRIM(CAST(discount AS VARCHAR)), '') AS discount_raw,

        -- =========================
        -- STORE
        -- =========================
        UPPER(NULLIF(TRIM(CAST(store_location AS VARCHAR)), '')) AS store_location,
        UPPER(NULLIF(TRIM(CAST(store_region AS VARCHAR)), '')) AS store_region,
        TRIM(CAST(store_manager AS VARCHAR)) AS store_manager,

        -- =========================
        -- DATE (keep raw for parsing later)
        -- =========================
        NULLIF(TRIM(CAST(sale_date AS VARCHAR)), '') AS sale_date_raw,

        -- =========================
        -- PASS-THROUGH (no transformation)
        -- =========================
        order_timestamp,
        delivery_date,

        UPPER(NULLIF(TRIM(CAST(order_status AS VARCHAR)), '')) AS order_status

    FROM silver.step01_dedup;
    """).fetchall()

    con.execute("SELECT * FROM silver.step02_standardized LIMIT 12").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 10 — Step 3: Fix discount values

    ### Rule
    Invalid, missing, or negative discount becomes `0.00`.

    ### Business value
    This prevents nonsensical pricing calculations and keeps revenue metrics stable.

    ### How
    We use `CASE` with `TRY_CAST`.
    """)
    return


@app.cell
def _(con):
    con.execute("""

    CREATE OR REPLACE TABLE silver.step03_discount_fixed AS

    SELECT
        *,

        -- =========================
        -- DISCOUNT (CLEANED)
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
        FROM silver.step02_standardized
    );
    """).fetchall()

    con.execute("""
    SELECT
        SUM(CASE WHEN discount_raw IS NULL THEN 1 ELSE 0 END) AS missing_discount_rows,
        SUM(CASE WHEN TRY_CAST(discount_raw AS DOUBLE) < 0 THEN 1 ELSE 0 END) AS negative_discount_rows,
        SUM(CASE WHEN discount = 0.00 THEN 1 ELSE 0 END) AS final_zero_discount_rows
    FROM silver.step03_discount_fixed;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 11 — Plot discount cleanup results

    ### Why
    This shows how often discount imputation happened.

    ### Plot meaning
    - `missing_discount` = blank discount values
    - `negative_discount` = discount below zero
    - `zero_after_fix` = final number of rows with discount set to zero
    """)
    return


@app.cell
def _(con, plt):
    df_discount = con.execute("""
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
    plt.bar(df_discount["category"], df_discount["row_count"])
    plt.title("Discount Cleanup Summary")
    plt.xlabel("Category")
    plt.ylabel("Rows")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot interpretation

    This plot shows how often discount values required correction.

    If the `negative_discount` bar is high, the source system may have a pricing logic problem. If `missing_discount` is high, the issue is more likely data completeness.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 12 — Step 4: Parse valid sale dates

    ### Rule
    Accepted formats:
    - `MM/DD/YYYY`
    - `YYYY-MM-DD`

    ### Business value
    Time analysis is impossible without clean dates. Invalid dates must be identified before Gold analytics.

    ### How
    We parse both allowed formats with `TRY_STRPTIME` and combine them with `COALESCE`.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.step04_date_parsed AS
    SELECT
        *,

        -- =========================
        -- DATE PARSING (STEP A)
        -- =========================
        TRY_STRPTIME(sale_date_raw, '%m/%d/%Y')::DATE AS sale_date_us,

        TRY_STRPTIME(sale_date_raw, '%Y-%m-%d')::DATE AS sale_date_iso,

        -- =========================
        -- FINAL DATE (STEP B)
        -- =========================
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 13 — Show examples of bad dates

    ### Why
    Bad examples help students understand what the parser rejects.

    ### Business value
    This is a practical data quality audit that can be shared with upstream teams.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        sale_date_raw,
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
    ## Cell 14 — Step 5: Build rejected records

    ### Rejection logic
    A row is rejected if:
    - `sale_type` is missing
    - `product_name` is missing
    - `customer_email` is missing or invalid
    - `quantity` is invalid or <= 0
    - `unit_price` is missing or <= 0
    - `cost_price` is missing or <= 0
    - `store_location` is missing or invalid
    - `sale_date` is invalid or missing

    ### Business value
    Rejected rows do not represent trustworthy business events and should not reach Gold.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.rejected_records AS
    SELECT
        *,
        -- =========================
        -- REJECTION REASON
        -- =========================
        CASE
            WHEN sale_type IS NULL THEN 'REJECT_MISSING_SALE_TYPE'
            WHEN product_name IS NULL THEN 'REJECT_MISSING_PRODUCT'      
            WHEN customer_name IS NULL THEN 'REJECT_MISSING_CUSTOMER_NAME'     
            WHEN customer_email IS NULL THEN 'REJECT_MISSING_EMAIL'
            WHEN POSITION('@' IN customer_email) = 0 THEN 'REJECT_INVALID_EMAIL'      
            WHEN quantity IS NULL OR quantity <= 0 THEN 'REJECT_INVALID_QUANTITY'     
            WHEN unit_price IS NULL OR unit_price <= 0 THEN 'REJECT_INVALID_UNIT_PRICE'    
            WHEN cost_price IS NULL OR cost_price <= 0 THEN 'REJECT_INVALID_COST_PRICE'    
            WHEN store_location IS NULL THEN 'REJECT_MISSING_STORE_LOCATION'
            WHEN store_location NOT IN ('USA','CANADA','ENGLAND','CHINA') THEN 'REJECT_INVALID_STORE_LOCATION'      
            WHEN sale_date IS NULL THEN 'REJECT_INVALID_OR_MISSING_SALE_DATE' 
            ELSE 'REJECT_OTHER'
        END AS reject_reason

    FROM silver.step04_date_parsed

    -- =========================
    -- FILTER: ONLY BAD RECORDS
    -- =========================
    WHERE
        sale_type IS NULL
        OR product_name IS NULL
        OR customer_name IS NULL
        OR customer_email IS NULL
        OR POSITION('@' IN customer_email) = 0
        OR quantity IS NULL OR quantity <= 0
        OR unit_price IS NULL OR unit_price <= 0
        OR cost_price IS NULL OR cost_price <= 0
        OR store_location IS NULL
        OR store_location NOT IN ('USA','CANADA','ENGLAND','CHINA')
        OR sale_date IS NULL;
    """).fetchall()

    con.execute("""
    SELECT reject_reason, COUNT(*) AS row_count
    FROM silver.rejected_records
    GROUP BY reject_reason
    ORDER BY row_count DESC;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 15 — Plot rejected records by reason

    ### Why
    This shows which rule causes the most rejection.

    ### Business value
    The dominant rejection reason often points to the most important upstream system problem.
    """)
    return


@app.cell
def _(con, plt):
    df_rejects = con.execute("""
    SELECT reject_reason, COUNT(*) AS row_count
    FROM silver.rejected_records
    GROUP BY reject_reason
    ORDER BY row_count DESC;
    """).df()

    plt.figure(figsize=(10,4))
    plt.bar(df_rejects["reject_reason"], df_rejects["row_count"])
    plt.title("Rejected Records by Reason")
    plt.xlabel("Reject Reason")
    plt.ylabel("Rows")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot interpretation

    This plot explains *why* rows are lost in Silver. A dominant reason suggests where the source data contract is weakest.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 16 — Step 6: Build cancelled transactions

    ### Cancellation logic
    If `sale_id` is missing or not an integer, the row is classified as **cancelled**, but only if the rest of the row is otherwise valid.

    ### Business value
    Cancelled transactions still contain business signal:
    - customer intent existed
    - product demand existed
    - revenue opportunity was lost
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.cancelled_transactions AS
    SELECT
        *
    FROM silver.step04_date_parsed
    WHERE
        -- =========================
        -- CANCELLED CONDITION
        -- =========================
        (sale_id_raw IS NULL OR TRY_CAST(sale_id_raw AS INTEGER) IS NULL)

        -- =========================
        -- MUST BE OTHERWISE VALID
        -- =========================
        AND sale_type IS NOT NULL
        AND product_name IS NOT NULL    
        AND customer_name IS NOT NULL    
        AND customer_email IS NOT NULL
        AND POSITION('@' IN customer_email) > 0    
        AND quantity IS NOT NULL AND quantity > 0    
        AND unit_price IS NOT NULL AND unit_price > 0   
        AND cost_price IS NOT NULL AND cost_price > 0   
        AND store_location IS NOT NULL
        AND store_location IN ('USA','CANADA','ENGLAND','CHINA')   
        AND sale_date IS NOT NULL;
    """).fetchall()

    con.execute("SELECT COUNT(*) AS cancelled_rows FROM silver.cancelled_transactions").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 17 — Analyze cancelled transactions by product

    ### Why
    This reveals which products are most affected by cancellations.

    ### Business value
    A high cancellation count for a product can suggest inventory, payment, or customer experience issues.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        product_name,
        COUNT(*) AS cancelled_count,
        ROUND(SUM((quantity * unit_price) - discount), 2) AS cancelled_value
    FROM silver.cancelled_transactions
    GROUP BY product_name
    ORDER BY cancelled_count DESC, cancelled_value DESC;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 18 — Plot cancelled transactions by product

    ### Plot meaning
    This chart compares cancellation volume across products.

    ### Business value
    It helps business teams focus on which product lines lose the most potential sales.
    """)
    return


@app.cell
def _(con, plt):
    df_cancelled = con.execute("""
    SELECT
        product_name,
        COUNT(*) AS cancelled_count
    FROM silver.cancelled_transactions
    GROUP BY product_name
    ORDER BY cancelled_count DESC;
    """).df()

    plt.figure(figsize=(9,4))
    plt.bar(df_cancelled["product_name"], df_cancelled["cancelled_count"])
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
    ### Plot interpretation

    Tall bars indicate products with more cancelled transactions. This does not automatically mean they are problematic; it may also reflect higher sales volume. The next step is to compare cancellation rate, not just count.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 19 — Step 7: Build trusted Silver records

    ### Why
    Gold should be built only from rows that are:
    - not rejected
    - not cancelled
    - consistent enough for analytics

    ### Business value
    This creates the warehouse-ready operational truth.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.sales_clean AS
    SELECT
        -- =========================
        -- CORE IDENTIFIERS
        -- =========================
        TRY_CAST(sale_id_raw AS INTEGER) AS sale_id,

        sale_type,
        COALESCE(sales_channel, 'UNKNOWN') AS sales_channel,

        -- =========================
        -- PRODUCT
        -- =========================
        product_name,
        product_category,
        product_brand,

        -- =========================
        -- CUSTOMER
        -- =========================
        customer_name,
        customer_email,
        customer_country,
        customer_city,
        customer_gender,
        customer_segment,

        -- =========================
        -- MEASURES
        -- =========================
        quantity,
        unit_price,
        cost_price,
        discount,   -- ✅ use from step03

        -- =========================
        -- STORE
        -- =========================
        store_location,
        store_region,
        store_manager,

        -- =========================
        -- DATE
        -- =========================
        sale_date,  -- ✅ use from step04

        order_timestamp,
        delivery_date,
        order_status,

        -- =========================
        -- DERIVED METRICS
        -- =========================
        (quantity * unit_price) - discount AS final_sale_price,

        (quantity * cost_price) AS total_cost,

        ((quantity * unit_price) - discount) - (quantity * cost_price) AS profit

    FROM silver.step04_date_parsed

    -- =========================
    -- 🔥 KEEP ONLY VALID (NON-REJECTED, NON-CANCELLED)
    -- =========================
    WHERE
        -- must have valid sale_id (exclude cancelled)
        TRY_CAST(sale_id_raw AS INTEGER) IS NOT NULL

        -- basic validity
        AND sale_type IS NOT NULL
        AND product_name IS NOT NULL
        AND customer_name IS NOT NULL

        AND customer_email IS NOT NULL
        AND POSITION('@' IN customer_email) > 0

        AND quantity IS NOT NULL AND quantity > 0
        AND unit_price IS NOT NULL AND unit_price > 0
        AND cost_price IS NOT NULL AND cost_price > 0

        AND store_location IS NOT NULL
        AND store_location IN ('USA','CANADA','ENGLAND','CHINA')

        AND sale_date IS NOT NULL;
    """).fetchall()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT count(*) AS num_of_silver_sales_clean 
    FROM silver.sales_clean
    """).df()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT * 
    FROM silver.sales_clean 
    LIMIT 12""").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 20 — Build the pipeline funnel

    ### Why
    A funnel summarizes how the dataset shrinks from messy input to trusted output.

    ### Business value
    This is a high-value governance and teaching artifact.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT 'bronze.sales_raw' AS stage, COUNT(*) AS row_count FROM bronze.sales_raw
    UNION ALL
    SELECT 'silver.step01_dedup', COUNT(*) FROM silver.step01_dedup
    UNION ALL
    SELECT 'silver.rejected_records', COUNT(*) FROM silver.rejected_records
    UNION ALL
    SELECT 'silver.cancelled_transactions', COUNT(*) FROM silver.cancelled_transactions
    UNION ALL
    SELECT 'silver.sales_clean', COUNT(*) FROM silver.sales_clean;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 21 — Plot the funnel

    ### Plot meaning
    This chart shows how many rows survive each major stage.

    ### Business value
    It turns a complex cleaning pipeline into an easily explainable picture for stakeholders.
    """)
    return


@app.cell
def _(con, plt):
    _df_funnel = con.execute("""
    SELECT 'bronze.sales_raw' AS stage, COUNT(*) AS row_count FROM bronze.sales_raw
    UNION ALL
    SELECT 'silver.step01_dedup', COUNT(*) FROM silver.step01_dedup
    UNION ALL
    SELECT 'silver.rejected_records', COUNT(*) FROM silver.rejected_records
    UNION ALL
    SELECT 'silver.cancelled_transactions', COUNT(*) FROM silver.cancelled_transactions
    UNION ALL
    SELECT 'silver.sales_clean', COUNT(*) FROM silver.sales_clean;
    """).df()

    plt.figure(figsize=(10,4))
    plt.bar(_df_funnel["stage"], _df_funnel["row_count"])
    plt.title("Medallion Cleaning Funnel")
    plt.xlabel("Stage")
    plt.ylabel("Rows")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot interpretation

    The funnel shows the cumulative effect of rule enforcement. If too many rows are lost, the upstream system may be unstable. If very few rows are lost, the source data is relatively healthy.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Gold Layer

    Gold converts trusted Silver data into analytics-ready structures.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 22 — Create Gold dimensions

    ### Why
    Dimension tables store reusable business entities and descriptive attributes.

    ### Business value
    They support slicing, grouping, and drill-down analytics.
    """)
    return


@app.cell
def _(con):
    con.execute("""

    CREATE OR REPLACE TABLE gold.dim_customer AS
    SELECT
        ROW_NUMBER() OVER (ORDER BY customer_email) AS customer_key,
        customer_email,
        -- =========================
        -- CUSTOMER ATTRIBUTES
        -- =========================
        MIN(customer_name) AS customer_name,
        MIN(customer_country) AS customer_country,
        MIN(customer_city) AS customer_city,
        MIN(customer_gender) AS customer_gender,
        MIN(customer_segment) AS customer_segment
    FROM silver.sales_clean
    GROUP BY customer_email;
    """).fetchall()
    return


@app.cell
def _(con):
    _df_funnel = con.execute("""
    SELECT * 
    FROM gold.dim_customer
    LIMIT 5;
    """).df()

    _df_funnel
    return


@app.cell
def _(con):
    con.execute("""

    CREATE OR REPLACE TABLE gold.dim_product AS
    SELECT
        ROW_NUMBER() OVER (ORDER BY product_name, product_category, product_brand) AS product_key,
        product_name,
        product_category,
        product_brand
    FROM (
        SELECT DISTINCT
            product_name,
            product_category,
            product_brand
        FROM silver.sales_clean
    );
    """).fetchall()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT * 
    FROM gold.dim_product;
    """).df()
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE gold.dim_store AS
    SELECT
        ROW_NUMBER() OVER (ORDER BY store_location, store_region, store_manager) AS store_key,
        store_location,
        store_region,
        store_manager
    FROM (
        SELECT DISTINCT
            store_location,
            store_region,
            store_manager
        FROM silver.sales_clean
    );
    """).fetchall()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT * 
    FROM gold.dim_store;
    """).df()
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE gold.dim_date AS
    SELECT
        ROW_NUMBER() OVER (ORDER BY sale_date) AS date_key,

        -- =========================
        -- CORE
        -- =========================
        sale_date AS full_date,

        -- =========================
        -- YEAR / QUARTER / MONTH
        -- =========================
        EXTRACT(YEAR FROM sale_date) AS year_num,
        EXTRACT(QUARTER FROM sale_date) AS quarter_num,
        EXTRACT(MONTH FROM sale_date) AS month_num,

        STRFTIME(sale_date, '%B') AS month_name,
        STRFTIME(sale_date, '%Y-%m') AS year_month,

        -- =========================
        -- DAY FEATURES (VERY USEFUL)
        -- =========================
        EXTRACT(DAY FROM sale_date) AS day_of_month,

        EXTRACT(DOW FROM sale_date) AS day_of_week_num,
        STRFTIME(sale_date, '%A') AS day_of_week_name,

        CASE 
            WHEN EXTRACT(DOW FROM sale_date) IN (0, 6) THEN 'WEEKEND'
            ELSE 'WEEKDAY'
        END AS day_type,

        -- =========================
        -- WEEK FEATURES
        -- =========================
        EXTRACT(WEEK FROM sale_date) AS week_of_year,

        -- =========================
        -- SORT KEYS (VERY IMPORTANT)
        -- =========================
        CAST(STRFTIME(sale_date, '%Y%m%d') AS INTEGER) AS date_int_key

    FROM (
        SELECT DISTINCT sale_date
        FROM silver.sales_clean
    );
    """).fetchall()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT COUNT(*) AS num_of_dates 
    FROM gold.dim_date;
    """).df()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT * 
    FROM gold.dim_date
    LIMIT 10;
    """).df()
    return


@app.cell
def _(con):
    # List of Tables in GOLD Schema:

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
    ## Cell 23 — Create the Gold fact table

    ### Why
    The fact table stores measurable business events and connects to dimensions.

    ### Business value
    This is the center of OLAP analysis.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE gold.fact_sales AS
    SELECT
        s.sale_id,

        -- =========================
        -- DIMENSION KEYS
        -- =========================
        dc.customer_key,
        dp.product_key,
        ds.store_key,
        dd.date_key,

        -- =========================
        -- DEGENERATE DIMENSIONS
        -- =========================
        s.sale_type,
        s.sales_channel,

        -- =========================
        -- MEASURES
        -- =========================
        s.quantity,
        s.unit_price,
        s.cost_price,
        s.discount,
        s.final_sale_price,
        s.total_cost,
        s.profit

    FROM silver.sales_clean s

    -- =========================
    -- CORRECT JOINS
    -- =========================
    JOIN gold.dim_customer dc 
        ON s.customer_email = dc.customer_email

    JOIN gold.dim_product dp 
        ON s.product_name = dp.product_name
       AND s.product_category = dp.product_category
       AND s.product_brand = dp.product_brand

    JOIN gold.dim_store ds 
        ON s.store_location = ds.store_location
       AND s.store_region = ds.store_region
       AND s.store_manager = ds.store_manager

    JOIN gold.dim_date dd 
        ON s.sale_date = dd.full_date;
    """).fetchall()

    con.execute("SELECT COUNT(*) AS num_of_fact_rows FROM gold.fact_sales").df()
    return


@app.cell
def _(con):
    con.execute("SELECT * FROM gold.fact_sales LIMIT 5").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 24 — Show tables by schema

    ### Why
    This gives a compact structural view of the full medallion pipeline.
    """)
    return


@app.cell
def _(con):
    df_tables = con.execute("""
    SELECT
        table_schema,
        table_name
    FROM information_schema.tables
    WHERE table_schema IN ('raw','bronze','silver','gold')
    ORDER BY table_schema, table_name;
    """).df()

    for schema, group in df_tables.groupby("table_schema"):
        print(f"\n📦 Schema: {schema.upper()}")
        print("-" * 40)
        print(group["table_name"].to_string(index=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Analytics on Gold

    These queries demonstrate why Gold exists: reliable business insight.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 25 — OLAP 1: Final sales by product

    ### Why
    This shows which products generate the most trusted revenue.

    ### Plot interpretation
    A taller bar means that product contributes more final sales. This helps identify top-performing product lines.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        p.product_name,
        ROUND(SUM(f.final_sale_price), 2) AS total_final_sales
    FROM gold.fact_sales f
    JOIN gold.dim_product p ON f.product_key = p.product_key
    GROUP BY p.product_name
    ORDER BY total_final_sales DESC;
    """).df()
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT
        p.product_name,
        SUM(f.final_sale_price) AS total_final_sales
    FROM gold.fact_sales f
    JOIN gold.dim_product p ON f.product_key = p.product_key
    GROUP BY p.product_name
    ORDER BY total_final_sales DESC;
    """).df()

    plt.figure(figsize=(9,4))
    plt.bar(_df["product_name"], _df["total_final_sales"])
    plt.title("Final Sales by Product")
    plt.xlabel("Product")
    plt.ylabel("Final Sales")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 26 — OLAP 2: Monthly sales trend

    ### Why
    This reveals seasonality and trend patterns in trusted sales.

    ### Plot interpretation
    The line helps detect high and low periods. Peaks may correspond to demand spikes or seasonal effects.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        d.year_month,
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
    SELECT
        d.year_month,
        SUM(f.final_sale_price) AS total_final_sales
    FROM gold.fact_sales f
    JOIN gold.dim_date d ON f.date_key = d.date_key
    GROUP BY d.year_month
    ORDER BY d.year_month;
    """).df()

    plt.figure(figsize=(10,4))
    plt.plot(_df["year_month"], _df["total_final_sales"])
    plt.title("Monthly Sales Trend")
    plt.xlabel("Year-Month")
    plt.ylabel("Final Sales")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 27 — OLAP 3: Profit by store location

    ### Why
    This compares profitability across store locations.

    ### Plot interpretation
    A larger slice or bar indicates a stronger profit contribution from that store location.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        s.store_location,
        ROUND(SUM(f.profit), 2) AS total_profit
    FROM gold.fact_sales f
    JOIN gold.dim_store s ON f.store_key = s.store_key
    GROUP BY s.store_location
    ORDER BY total_profit DESC;
    """).df()
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT
        s.store_location,
        SUM(f.profit) AS total_profit
    FROM gold.fact_sales f
    JOIN gold.dim_store s ON f.store_key = s.store_key
    GROUP BY s.store_location
    ORDER BY total_profit DESC;
    """).df()

    plt.figure(figsize=(6,6))
    plt.pie(_df["total_profit"], labels=_df["store_location"], autopct='%1.1f%%')
    plt.title("Profit Distribution by Store Location")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 28 — OLAP 4: Sales by customer country

    ### Why
    This shows geographic contribution to revenue.

    ### Plot interpretation
    Taller bars indicate countries generating more sales. This can support localization or expansion decisions.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        c.customer_country,
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
    SELECT
        c.customer_country,
        SUM(f.final_sale_price) AS total_final_sales
    FROM gold.fact_sales f
    JOIN gold.dim_customer c ON f.customer_key = c.customer_key
    GROUP BY c.customer_country
    ORDER BY total_final_sales DESC;
    """).df()

    plt.figure(figsize=(9,4))
    plt.bar(_df["customer_country"], _df["total_final_sales"])
    plt.title("Final Sales by Customer Country")
    plt.xlabel("Customer Country")
    plt.ylabel("Final Sales")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 29 — OLAP 5: Channel comparison

    ### Why
    This compares revenue across sales channels.

    ### Plot interpretation
    The plot reveals which customer interaction channel contributes most to revenue.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        sales_channel,
        COUNT(*) AS transactions,
        ROUND(SUM(final_sale_price), 2) AS total_final_sales,
        ROUND(AVG(final_sale_price), 2) AS avg_transaction_value
    FROM gold.fact_sales
    GROUP BY sales_channel
    ORDER BY total_final_sales DESC;
    """).df()
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT
        sales_channel,
        SUM(final_sale_price) AS total_final_sales
    FROM gold.fact_sales
    GROUP BY sales_channel
    ORDER BY total_final_sales DESC;
    """).df()

    plt.figure(figsize=(7,4))
    plt.bar(_df["sales_channel"], _df["total_final_sales"])
    plt.title("Final Sales by Sales Channel")
    plt.xlabel("Sales Channel")
    plt.ylabel("Final Sales")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Final Reflection

    This notebook demonstrated how to clean a messy dataset using a medallion pattern:

    - Bronze preserved the raw source
    - Silver applied business rules step-by-step
    - Gold enabled trustworthy analytics

    ### Most important lesson
    Good analytics depend on good data quality design. Cleaning is not just technical work — it protects business decisions.
    """)
    return


if __name__ == "__main__":
    app.run()
