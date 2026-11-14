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
    # Medallion Architecture in 1200 Records
    ## Bronze → Silver → Gold with DuckDB

    This notebook teaches **Medallion Architecture** step by step using a small retail sales dataset with **1200 clean records**.

    We will use three logical layers:

    - **Bronze**: raw ingested data
    - **Silver**: cleaned, standardized, typed data
    - **Gold**: analytical model for reporting and BI

    The source CSV contains the following columns:

    - `sale_id`
    - `sale_type`
    - `product`
    - `customer_name`
    - `customer_email`
    - `customer_country`
    - `quantity`
    - `unit_price`
    - `discount`
    - `store_location`
    - `sale_date`

    ---

    ## Teaching Goal

    By the end of this notebook, you will understand:

    1. how raw data lands in Bronze
    2. how Silver improves quality and consistency
    3. how Gold prepares the data for analytics
    4. how to write analytical SQL on top of Gold tables
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 1 — Import libraries and create a DuckDB connection

    ### What are we doing?
    We import Python libraries and create a local DuckDB database connection.

    ### Why are we doing this?
    DuckDB lets us build a small data warehouse directly inside a notebook.
    This is excellent for teaching because students can run SQL immediately without installing a separate database server.
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd

    con = duckdb.connect("medallion_1200.duckdb")
    print("Connected to DuckDB.")
    return con, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 2 — Define the source file

    ### What are we doing?
    We define the CSV file name that contains the 1200 sales records.

    ### Why are we doing this?
    Keeping the file name in one variable makes the notebook easier to maintain.
    If the file changes later, students only need to update one place.
    """)
    return


@app.cell
def _():
    csv_file = "medallion_sales_1200.csv"
    print("Using source file:", csv_file)
    return (csv_file,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 3 — Preview the raw CSV with pandas

    ### What are we doing?
    We load a small preview of the CSV file using pandas.

    ### Why are we doing this?
    Before building Bronze, we should inspect the incoming data:
    - column names
    - sample values
    - business meaning of the fields

    This is the first step in understanding the raw source.
    """)
    return


@app.cell
def _(csv_file, pd):
    df_preview = pd.read_csv(csv_file)
    df_preview.head(10)
    return (df_preview,)


@app.cell
def _(df_preview):
    df_preview.shape
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 4 — Create logical schemas: Bronze, Silver, Gold

    ### What are we doing?
    We create three schemas inside DuckDB.

    ### Why are we doing this?
    Schemas help us separate layers clearly:

    - `bronze` = ingestion layer
    - `silver` = cleaned layer
    - `gold` = reporting / analytics layer

    Even in a small classroom example, this separation teaches a very important real-world habit.
    """)
    return


@app.cell
def _(con):
    con.execute("CREATE SCHEMA IF NOT EXISTS bronze;").fetchall()
    con.execute("CREATE SCHEMA IF NOT EXISTS silver;").fetchall()
    con.execute("CREATE SCHEMA IF NOT EXISTS gold;").fetchall()

    con.execute("SELECT schema_name FROM information_schema.schemata ORDER BY schema_name").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Bronze Layer

    The Bronze layer stores data as it arrives from the source.

    In real systems, Bronze may contain:
    - raw text
    - inconsistent formatting
    - duplicate rows
    - missing values
    - late-arriving data

    In this notebook, the dataset is already clean, but we still use Bronze to teach the architecture correctly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 5 — Create the Bronze table from the CSV file

    ### What are we doing?
    We load the CSV file into `bronze.sales_raw`.

    ### Why are we doing this?
    Bronze is the **landing zone**.
    It preserves the source data in its original form so that:
    - we can trace where data came from
    - we can reload Silver later
    - we keep a reproducible ingestion step
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE bronze.sales_raw AS
    SELECT *
    FROM read_csv_auto('medallion_sales_1200.csv');
    """).fetchall()

    con.execute("SELECT COUNT(*) AS bronze_row_count FROM bronze.sales_raw").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 6 — Inspect Bronze structure

    ### What are we doing?
    We list the columns and data types in the Bronze table.

    ### Why are we doing this?
    Bronze often reflects the source file more than the business model.
    We inspect structure before deciding what needs improvement in Silver.
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


@app.cell
def _(con):
    # INSPECT metadata

    con.execute("""
    DESC TABLE bronze.sales_raw;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 7 — Look at sample Bronze rows

    ### What are we doing?
    We display sample rows from Bronze.

    ### Why are we doing this?
    Students should connect SQL structure to actual business records:
    - a customer
    - a product
    - a quantity
    - a discount
    - a sale date
    """)
    return


@app.cell
def _(con):
    con.execute("SELECT * FROM bronze.sales_raw LIMIT 10").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 8 — Profile the Bronze data

    ### What are we doing?
    We calculate basic profiling metrics.

    ### Why are we doing this?
    Data engineers always ask:
    - How many rows do we have?
    - Are IDs unique?
    - How many customers and products exist?
    - Are there obvious null issues?

    This gives us a quick health check before Silver.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        COUNT(*) AS total_rows,
        COUNT(DISTINCT sale_id) AS distinct_sale_ids,
        COUNT(DISTINCT customer_email) AS distinct_customers,
        COUNT(DISTINCT product) AS distinct_products,
        COUNT(DISTINCT sale_type) AS distinct_sale_types,
        COUNT(DISTINCT store_location) AS distinct_store_locations
    FROM bronze.sales_raw;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Silver Layer

    The Silver layer improves the Bronze data.

    Typical Silver tasks include:
    - standardizing text
    - converting data types
    - validating business rules
    - removing duplicates
    - deriving useful columns

    Even though this dataset is already valid, we still create Silver because it represents the **trusted and standardized** version of the data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 9 — Create a cleaned and typed Silver table

    ### What are we doing?
    We create `silver.sales_clean` by:
    - uppercasing category-like fields
    - trimming text fields
    - converting `sale_date` to a real `DATE`
    - keeping numeric fields in proper numeric types

    ### Why are we doing this?
    Silver should be the reliable working layer for analysts and downstream transformations.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.sales_clean AS

    SELECT

        CAST(sale_id AS INTEGER) AS sale_id,
        UPPER(TRIM(sale_type)) AS sale_type,
        UPPER(TRIM(product)) AS product,
        TRIM(customer_name) AS customer_name,
        LOWER(TRIM(customer_email)) AS customer_email,
        UPPER(TRIM(customer_country)) AS customer_country,
        CAST(quantity AS INTEGER) AS quantity,
        CAST(unit_price AS DOUBLE) AS unit_price,
        CAST(discount AS DOUBLE) AS discount,
        UPPER(TRIM(store_location)) AS store_location,
        CAST(sale_date AS DATE) AS sale_date

    FROM bronze.sales_raw;
    """).fetchall()

    con.execute("SELECT COUNT(*) AS silver_row_count FROM silver.sales_clean").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 10 — Validate Silver data types

    ### What are we doing?
    We inspect the schema of `silver.sales_clean`.

    ### Why are we doing this?
    We want to verify that the transformations worked:
    - `sale_date` should be a `DATE`
    - quantity should be numeric
    - price and discount should be numeric
    """)
    return


@app.cell
def _(con):
    # show me the metadata for silver.sales_clean table
    con.execute("""
    SELECT
        column_name,
        data_type
    FROM information_schema.columns
    WHERE table_schema = 'silver'
      AND table_name = 'sales_clean'
    ORDER BY ordinal_position;
    """).df()
    return


@app.cell
def _(con):
    # OR show me the metadata for silver.sales_clean table
    con.execute("""
    DESC TABLE silver.sales_clean;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 11 — Add derived business columns in Silver

    ### What are we doing?
    We create a richer Silver table with derived measures:
    - `gross_amount = quantity * unit_price`
    - `net_amount = gross_amount - discount`
    - year / month fields for time analysis

    ### Why are we doing this?
    Derived fields reduce repeated SQL later and make Gold construction easier.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.sales_enriched AS
    SELECT
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
        sale_date,
        quantity * unit_price AS gross_amount,
        quantity * unit_price - discount AS net_amount,
        EXTRACT(YEAR FROM sale_date) AS sale_year,
        EXTRACT(MONTH FROM sale_date) AS sale_month,
        STRFTIME(sale_date, '%Y-%m') AS year_month
    FROM silver.sales_clean;
    """).fetchall()

    con.execute("SELECT * FROM silver.sales_enriched LIMIT 10").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 12 — Run Silver validation checks

    ### What are we doing?
    We check a few business rules:
    - no null primary sale IDs
    - no duplicated sale IDs
    - no negative quantity
    - no negative unit price
    - no negative discount
    - no negative net amount

    ### Why are we doing this?
    Silver is where we begin to trust the data.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        SUM(CASE WHEN sale_id IS NULL THEN 1 ELSE 0 END) AS null_sale_id,
        COUNT(*) - COUNT(DISTINCT sale_id) AS duplicate_sale_id_count,
        SUM(CASE WHEN quantity <= 0 THEN 1 ELSE 0 END) AS bad_quantity_count,
        SUM(CASE WHEN unit_price < 0 THEN 1 ELSE 0 END) AS bad_unit_price_count,
        SUM(CASE WHEN discount < 0 THEN 1 ELSE 0 END) AS bad_discount_count,
        SUM(CASE WHEN net_amount < 0 THEN 1 ELSE 0 END) AS bad_net_amount_count
    FROM silver.sales_enriched;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 13 — Understand customer concentration in Silver

    ### What are we doing?
    We identify the most active customers by transaction count.

    ### Why are we doing this?
    The dataset was intentionally created so that some customers dominate.
    This confirms that the data is **not balanced**, which is useful for analytical practice.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        customer_name,
        customer_email,
        COUNT(*) AS purchase_count,
        ROUND(SUM(net_amount), 2) AS total_net_sales
    FROM silver.sales_enriched
    GROUP BY customer_name, customer_email
    ORDER BY purchase_count DESC, total_net_sales DESC
    LIMIT 10;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Gold Layer

    The Gold layer is built for analytics, reporting, dashboards, and business questions.

    In this notebook, we will build a small star schema:
    - one fact table
    - several dimension tables

    This makes analytical SQL easier, cleaner, and more reusable.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 14 — Create `gold.dim_customer`

    ### What are we doing?
    We create a customer dimension with one row per customer.

    ### Why are we doing this?
    Dimensions store descriptive business entities.
    The customer dimension allows us to analyze sales by customer and country.

    #### Now, we create `customer_key` to represent the following 3 columns:

    * `customer_name`,
    * `customer_email`,
    * `customer_country`

    Anytime we need a customer information, we use `customer_key`
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
        SELECT DISTINCT
            customer_name,
            customer_email,
            customer_country
        FROM silver.sales_enriched
    );
    """).fetchall()

    con.execute("SELECT * FROM gold.dim_customer LIMIT 10").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 15 — Create `gold.dim_product`

    ### What are we doing?
    We create a product dimension with one row per product.

    ### Why are we doing this?
    A dimension table should contain descriptive attributes about the business entity.
    For now, the dataset only gives us the product name, so the dimension is simple.

    #### `product_key` becomes the PK for `gold.dim_product` table
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
        FROM silver.sales_enriched
    );
    """).fetchall()

    con.execute("SELECT * FROM gold.dim_product ORDER BY product_key").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 16 — Create `gold.dim_store`

    ### What are we doing?
    We create a store/location dimension from `store_location`.

    ### Why are we doing this?
    Store location is a descriptive attribute often used for slicing sales results.

    #### `store_key` becomes the PK for `gold.dim_store` table
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
        FROM silver.sales_enriched
    );
    """).fetchall()

    con.execute("SELECT * FROM gold.dim_store ORDER BY store_key").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 17 — Create `gold.dim_date`

    ### What are we doing?
    We create a date dimension from all distinct sale dates.

    ### Why are we doing this?
    The date dimension supports time-based analytics such as:
    - year
    - month
    - quarter
    - weekday
    - month name

    #### `date_key` becomes the PK for `gold.dim_date` table

    #### In our analytics, `date_key` will be used for all dates informations.
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
        FROM silver.sales_enriched
    );
    """).fetchall()

    con.execute("SELECT * FROM gold.dim_date LIMIT 10").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 18 — Create `gold.fact_sales`

    ### What are we doing?
    We create the fact table and connect each sale to the dimensions.

    ### Why are we doing this?
    The fact table stores measurable business events:
    - quantity
    - unit price
    - discount
    - gross amount
    - net amount

    This is the center of the star schema.
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
        s.gross_amount,
        s.net_amount
    FROM silver.sales_enriched s
    JOIN gold.dim_customer dc
      ON s.customer_email = dc.customer_email
    JOIN gold.dim_product dp
      ON s.product = dp.product
    JOIN gold.dim_store ds
      ON s.store_location = ds.store_location
    JOIN gold.dim_date dd
      ON s.sale_date = dd.full_date;
    """).fetchall()

    con.execute("SELECT COUNT(*) AS fact_row_count FROM gold.fact_sales").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 19 — Inspect the final Gold model

    ### What are we doing?
    We list all Gold tables.

    ### Why are we doing this?
    Students should clearly see the final analytical structure:
    - dimensions
    - fact table
    - schema organization
    """)
    return


@app.cell
def _(con):
    # show me the tables in gold schema
    con.execute("""
    SELECT
        table_schema,
        table_name
    FROM information_schema.tables
    WHERE table_schema = 'gold'
    ORDER BY table_name;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 20 — Join the Gold star schema for a readable analytical view

    ### What are we doing?
    We join the fact and dimension tables into a business-friendly result.

    ### Why are we doing this?
    This helps students see how the star schema works in practice.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        f.sale_id,
        d.full_date,
        d.year_month,
        c.customer_name,
        c.customer_country,
        p.product,
        s.store_location,
        f.sale_type,
        f.quantity,
        f.unit_price,
        f.discount,
        f.net_amount
    FROM gold.fact_sales f
    JOIN gold.dim_customer c ON f.customer_key = c.customer_key
    JOIN gold.dim_product p  ON f.product_key = p.product_key
    JOIN gold.dim_store s    ON f.store_key = s.store_key
    JOIN gold.dim_date d     ON f.date_key = d.date_key
    LIMIT 15;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Analytical SQL on Gold

    Now that Gold is ready, we can answer business questions more easily.
    These examples are intentionally practical and classroom-friendly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 21 — Total net sales by product

    ### What are we doing?
    We compute total net sales by product.

    ### Why are we doing this?
    This is a classic dimensional query:
    **Which products generate the most revenue?**
    """)
    return


@app.cell
def _(con):
    import matplotlib.pyplot as plt
    _df = con.execute("""
    SELECT p.product, SUM(f.net_amount) AS total_net_sales
    FROM gold.fact_sales f
    JOIN gold.dim_product p ON f.product_key = p.product_key
    GROUP BY p.product
    ORDER BY total_net_sales DESC
    """).df()
    plt.figure()
    plt.bar(_df.iloc[:,0], _df.iloc[:,1])
    plt.xticks(rotation=45, ha='right')
    plt.xlabel(_df.columns[0])
    plt.ylabel(_df.columns[1])
    plt.title("Bar Chart")
    plt.tight_layout()
    plt.show()
    return (plt,)


@app.cell
def _(con):
    con.execute("""
    SELECT
        p.product,
        ROUND(SUM(f.net_amount), 2) AS total_net_sales
    FROM gold.fact_sales f
    JOIN gold.dim_product p
      ON f.product_key = p.product_key
    GROUP BY p.product
    ORDER BY total_net_sales DESC;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 22 — Monthly sales trend

    ### What are we doing?
    We aggregate net sales by month.

    ### Why are we doing this?
    This helps us confirm the designed seasonality in the dataset, especially the stronger sales in November and December 2025.
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT d.year_month, SUM(f.net_amount) AS total_net_sales
    FROM gold.fact_sales f
    JOIN gold.dim_date d ON f.date_key = d.date_key
    GROUP BY d.year_month
    ORDER BY d.year_month
    """).df()
    plt.figure()
    plt.plot(_df.iloc[:,0], _df.iloc[:,1])
    plt.xticks(rotation=45, ha='right')
    plt.xlabel(_df.columns[0])
    plt.ylabel(_df.columns[1])
    plt.title("Line Chart")
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        d.year_month,
        ROUND(SUM(f.net_amount), 2) AS total_net_sales,
        COUNT(*) AS transaction_count
    FROM gold.fact_sales f
    JOIN gold.dim_date d
      ON f.date_key = d.date_key
    GROUP BY d.year_month
    ORDER BY d.year_month;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 23 — Sales by country

    ### What are we doing?
    We calculate sales by customer country.

    ### Why are we doing this?
    This shows how a dimension can be used to slice the fact table by geography.
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT c.customer_country, SUM(f.net_amount) AS total_net_sales
    FROM gold.fact_sales f
    JOIN gold.dim_customer c ON f.customer_key = c.customer_key
    GROUP BY c.customer_country
    ORDER BY total_net_sales DESC
    """).df()
    plt.figure()
    plt.bar(_df.iloc[:,0], _df.iloc[:,1])
    plt.xticks(rotation=45, ha='right')
    plt.xlabel(_df.columns[0])
    plt.ylabel(_df.columns[1])
    plt.title("Bar Chart")
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        c.customer_country,
        ROUND(SUM(f.net_amount), 2) AS total_net_sales,
        COUNT(*) AS transactions
    FROM gold.fact_sales f
    JOIN gold.dim_customer c
      ON f.customer_key = c.customer_key
    GROUP BY c.customer_country
    ORDER BY total_net_sales DESC;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 24 — Top 10 customers by total sales

    ### What are we doing?
    We rank customers by total net sales.

    ### Why are we doing this?
    This query demonstrates customer concentration and helps explain why skewed data matters in analytics.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        c.customer_name,
        c.customer_email,
        ROUND(SUM(f.net_amount), 2) AS total_net_sales,
        COUNT(*) AS transaction_count
    FROM gold.fact_sales f
    JOIN gold.dim_customer c
      ON f.customer_key = c.customer_key
    GROUP BY c.customer_name, c.customer_email
    ORDER BY total_net_sales DESC
    LIMIT 10;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 25 — Compare IN-STORE vs ON-LINE sales

    ### What are we doing?
    We compare the two sales channels.

    ### Why are we doing this?
    `sale_type` is a useful business attribute even though it is stored in the fact table rather than a separate dimension in this small example.
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT sale_type, SUM(net_amount) AS total_net_sales
    FROM gold.fact_sales
    GROUP BY sale_type
    """).df()
    plt.figure()
    plt.bar(_df.iloc[:,0], _df.iloc[:,1])
    plt.xticks(rotation=45, ha='right')
    plt.xlabel(_df.columns[0])
    plt.ylabel(_df.columns[1])
    plt.title("Bar Chart")
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        sale_type,
        COUNT(*) AS transactions,
        ROUND(SUM(net_amount), 2) AS total_net_sales,
        ROUND(AVG(net_amount), 2) AS avg_net_sale
    FROM gold.fact_sales
    GROUP BY sale_type
    ORDER BY total_net_sales DESC;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 26 — Average discount by product

    ### What are we doing?
    We analyze average discount by product.

    ### Why are we doing this?
    This shows how measures in the fact table can be studied across dimensions.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        p.product,
        ROUND(AVG(f.discount), 2) AS avg_discount,
        ROUND(SUM(f.discount), 2) AS total_discount_given
    FROM gold.fact_sales f
    JOIN gold.dim_product p
      ON f.product_key = p.product_key
    GROUP BY p.product
    ORDER BY avg_discount DESC;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 27 — Find the busiest store location

    ### What are we doing?
    We calculate transaction count and sales by store location.

    ### Why are we doing this?
    This is another example of slicing the fact table with a dimension.
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT s.store_location, COUNT(*) AS transactions
    FROM gold.fact_sales f
    JOIN gold.dim_store s ON f.store_key = s.store_key
    GROUP BY s.store_location
    ORDER BY transactions DESC
    """).df()
    plt.figure()
    plt.bar(_df.iloc[:,0], _df.iloc[:,1])
    plt.xticks(rotation=45, ha='right')
    plt.xlabel(_df.columns[0])
    plt.ylabel(_df.columns[1])
    plt.title("Bar Chart")
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        s.store_location,
        COUNT(*) AS transactions,
        ROUND(SUM(f.net_amount), 2) AS total_net_sales
    FROM gold.fact_sales f
    JOIN gold.dim_store s
      ON f.store_key = s.store_key
    GROUP BY s.store_location
    ORDER BY transactions DESC;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 28 — Final explanation

    ### What did we learn?

    We built a full teaching example of Medallion Architecture:

    ### Bronze
    - landed raw source data
    - preserved the ingestion step

    ### Silver
    - standardized text
    - typed columns
    - added derived business measures
    - ran validation checks

    ### Gold
    - created dimensions
    - created a fact table
    - ran analytical SQL

    This pattern scales from classroom notebooks to real modern data platforms.
    """)
    return


if __name__ == "__main__":
    app.run()
