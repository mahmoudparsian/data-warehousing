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
    # 🍕 Pizza Shop Data Warehouse

    ## 1. Notebook:

    This notebook is a **teaching-first template** <br>
    for a full modern data warehousing pipeline:

    **Raw → Bronze → Silver → Gold → OLAP**

    We will keep the notebook **DuckDB-centric**, <br>
    use Python mainly as a driver, and only use   <br>
    small DataFrames at the plotting step.

    ## 2. Business Rules
    [Business Rules are defined here.](./pizza_dw_story.md)

    ## 3. DuckDB Tables Created

    This notebook will generate the following tables:

    ```sql
    CREATE TABLE bronze.orders_2015_raw(order_id VARCHAR, date VARCHAR, "time" VARCHAR);
    CREATE TABLE bronze.orders_2016_raw(order_id VARCHAR, date VARCHAR, "time" VARCHAR);
    CREATE TABLE bronze.orders_raw(source_year INTEGER, order_id VARCHAR, date VARCHAR, "time" VARCHAR);
    CREATE TABLE bronze.order_details_2015_raw(order_details_id VARCHAR, order_id VARCHAR, pizza_id VARCHAR, quantity VARCHAR);
    CREATE TABLE bronze.order_details_2016_raw(order_details_id VARCHAR, order_id VARCHAR, pizza_id VARCHAR, quantity VARCHAR);
    CREATE TABLE bronze.order_details_raw(source_year INTEGER, order_details_id VARCHAR, order_id VARCHAR, pizza_id VARCHAR, quantity VARCHAR);
    CREATE TABLE bronze.pizzas_raw(pizza_id VARCHAR, pizza_type_id VARCHAR, size VARCHAR, price VARCHAR);
    CREATE TABLE bronze.pizza_types_raw(pizza_type_id VARCHAR, "name" VARCHAR, category VARCHAR, ingredients VARCHAR);

    CREATE TABLE silver.orders_clean(source_year INTEGER, order_id BIGINT, order_date DATE, order_time VARCHAR);
    CREATE TABLE silver.order_details_clean(order_details_id BIGINT, order_id BIGINT, pizza_id VARCHAR, quantity BIGINT);
    CREATE TABLE silver.pizzas_clean(pizza_id VARCHAR, pizza_type_id VARCHAR, size VARCHAR, price DOUBLE);
    CREATE TABLE silver.pizza_types_clean(pizza_type_id VARCHAR, pizza_name VARCHAR, category VARCHAR, ingredients VARCHAR);

    CREATE TABLE gold.dim_date(date_key DATE, year_num BIGINT, month_num BIGINT, month_name VARCHAR, day_num BIGINT, day_name VARCHAR, quarter_num BIGINT, weekday_num BIGINT);
    CREATE TABLE gold.dim_pizza(pizza_id VARCHAR, pizza_type_id VARCHAR, pizza_name VARCHAR, category VARCHAR, size VARCHAR, price DOUBLE, ingredients VARCHAR);
    CREATE TABLE gold.fact_sales(order_details_id BIGINT, order_id BIGINT, date_key DATE, order_time VARCHAR, pizza_id VARCHAR, pizza_type_id VARCHAR, category VARCHAR, size VARCHAR, quantity BIGINT, unit_price DOUBLE, sales_amount DOUBLE);
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 1 — Medallion Architecture (Very Short)

    **Why are we doing this step?**
    A data warehouse should not jump directly from raw CSV files to business dashboards.
    We want a layered design:

    - **Raw**: original source files as-is
    - **Bronze**: ingested data with minimal interpretation
    - **Silver**: cleaned, validated, standardized data
    - **Gold**: business-friendly fact and dimension tables
    - **OLAP / BI**: analytical queries and plots

    This makes the project easier to explain, validate, and maintain.
    """)
    return


@app.cell
def _():
    import duckdb
    import matplotlib.pyplot as plt
    from pathlib import Path

    #----------------------------------------
    # Option-1: Create a persistent database
    #----------------------------------------
    DB_PATH = "pizza_shop_dw.duckdb"
    con = duckdb.connect(DB_PATH)
    # con.execute("PRAGMA enable_progress_bar;")  # needs the ipywidgets package in Jupyter; not required

    #-----------------------------------
    # Option-2: Create a memory database
    #----------------------------====---
    # con = duckdb.connect()

    print("Connected to:", DB_PATH)
    return Path, con, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 2 — Project Files and Paths

    **Why are we doing this step?**
    A good notebook should make file locations explicit and easy to change.
    This also helps students understand which files belong to which layer.

    **Implementation in Python + DuckDB**
    We define file paths once and reuse them throughout the notebook.

    **Plotting**
    No plot here. This is a setup cell.

    **Business analysis**
    No business insight yet. This is technical setup.
    """)
    return


@app.cell
def _(Path):
    DATA_DIR = Path("./data")

    ORDERS_2015 = DATA_DIR / "orders_2015.csv"
    ORDERS_2016 = DATA_DIR / "orders_2016.csv"
    ORDER_DETAILS_2015 = DATA_DIR / "order_details_2015.csv"
    ORDER_DETAILS_2016 = DATA_DIR / "order_details_2016.csv"
    PIZZAS = DATA_DIR / "pizzas.csv"
    PIZZA_TYPES = DATA_DIR / "pizza_types.csv"

    for p in [ORDERS_2015, ORDERS_2016, ORDER_DETAILS_2015, ORDER_DETAILS_2016, PIZZAS, PIZZA_TYPES]:
        print(p, "->", p.exists())
    return (
        ORDERS_2015,
        ORDERS_2016,
        ORDER_DETAILS_2015,
        ORDER_DETAILS_2016,
        PIZZAS,
        PIZZA_TYPES,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 3 — Helper Function for Query Preview

    **Why are we doing this step?**
    Students need a convenient way to run SQL and inspect small result sets without writing repetitive code.

    **Implementation in Python + DuckDB**
    A tiny helper prints a SQL query result.

    **Plotting**
    No plot yet.

    **Business analysis**
    Still setup.
    """)
    return


@app.cell
def _(con):
    def _q(sql, limit=10):
        return con.execute(sql).fetchdf().head(limit)

    def show(sql, limit=10):
        df = con.execute(sql).fetchdf().head(limit)
        print(sql)
        return df

    return (show,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Raw Layer

    ## Cell 4 — Quick Raw File Inspection

    **Why are we doing this step?**
    Before ingesting anything, we want students to see the source files and their rough sizes.
    This frames the warehouse as a response to messy operational data.

    **Implementation in Python + DuckDB**
    We inspect row counts directly from the CSV files.

    **Very nice plotting**
    We will create a simple bar chart for raw file row counts.

    **Business analysis**
    At this stage, we are not making business claims.
    We are only understanding the incoming data volume.
    """)
    return


@app.cell
def _(
    ORDERS_2015,
    ORDERS_2016,
    ORDER_DETAILS_2015,
    ORDER_DETAILS_2016,
    PIZZAS,
    PIZZA_TYPES,
    con,
):
    raw_counts_sql = f"""
    WITH counts AS (
        SELECT 'orders_2015' AS file_name, COUNT(*) AS row_count 
        FROM read_csv_auto('{ORDERS_2015}', header=True, encoding = 'IBM_1252', all_varchar = true)
        UNION ALL
        SELECT 'orders_2016', COUNT(*) 
        FROM read_csv_auto('{ORDERS_2016}', header=True, encoding = 'IBM_1252', all_varchar = true)
        UNION ALL
        SELECT 'order_details_2015', COUNT(*) 
        FROM read_csv_auto('{ORDER_DETAILS_2015}', header=True, encoding = 'IBM_1252', all_varchar = true)
        UNION ALL
        SELECT 'order_details_2016', COUNT(*) 
        FROM read_csv_auto('{ORDER_DETAILS_2016}', header=True, encoding = 'IBM_1252', all_varchar = true)
        UNION ALL
        SELECT 'pizzas', COUNT(*) 
        FROM read_csv_auto('{PIZZAS}', header=True, encoding = 'IBM_1252', all_varchar = true)
        UNION ALL
        SELECT 'pizza_types', COUNT(*) 
        FROM read_csv_auto('{PIZZA_TYPES}', header=True, encoding = 'IBM_1252', all_varchar = true)
    )
    SELECT * FROM counts
    ORDER BY row_count DESC;
    """

    raw_counts = con.execute(raw_counts_sql).fetchdf()
    raw_counts

    # % wc -l *csv
    #      16 data_dictionary.csv
    #   48663 order_details_2015.csv
    #   58860 order_details_2016.csv
    #   21390 orders_2015.csv
    #   24992 orders_2016.csv
    #      36 pizza_types.csv
    #     106 pizzas.csv
    return (raw_counts,)


@app.cell
def _(plt, raw_counts):
    plt.figure(figsize=(10, 5))
    plt.bar(raw_counts["file_name"], raw_counts["row_count"])
    plt.title("Raw File Row Counts")
    plt.xlabel("File")
    plt.ylabel("Rows")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # ✅ Cell: Validate line counts vs DuckDB counts
    """)
    return


@app.cell
def _(
    ORDERS_2015,
    ORDERS_2016,
    ORDER_DETAILS_2015,
    ORDER_DETAILS_2016,
    PIZZAS,
    PIZZA_TYPES,
    con,
):
    # ✅ Cell: Validate line counts vs DuckDB counts

    # import duckdb
    # con = duckdb.connect()

    FILES = {
        "order_details_2015": ORDER_DETAILS_2015,
        "order_details_2016": ORDER_DETAILS_2016,
        "orders_2015": ORDERS_2015,
        "orders_2016": ORDERS_2016,
        "pizzas": PIZZAS,
        "pizza_types": PIZZA_TYPES,
    }

    # Compute DuckDB counts
    duck_counts = {}
    for _name, path in FILES.items():
        enc = "IBM_1252" if _name == "pizza_types" else None
        if enc:
            _q = f"SELECT COUNT(*) FROM read_csv_auto('{path}', header=True, encoding='{enc}')"
        else:
            _q = f"SELECT COUNT(*) FROM read_csv_auto('{path}', header=True)"
        duck_counts[_name] = con.execute(_q).fetchall()[0][0]

    # Compute wc -l counts (header + data)
    import subprocess

    wc_counts = {}
    for _name, path in FILES.items():
        out = subprocess.check_output(["wc", "-l", path]).decode().strip()
        wc_counts[_name] = int(out.split()[0])

    # Build comparison table
    rows = []
    for _name in FILES:
        rows.append({
            "file": _name,
            "wc_lines": wc_counts[_name],
            "duckdb_rows": duck_counts[_name],
            "difference": wc_counts[_name] - duck_counts[_name]
        })

    import pandas as pd
    df_check = pd.DataFrame(rows).sort_values("file")
    df_check
    return (df_check,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ✅ What this confirms

    ```
    For every file:

    difference = 1

    👉 Meaning:
    	•	wc -l = header + data
    	•	DuckDB = data only
    	•	✔ No corrupted rows
    	•	✔ No ingestion loss
    	•	✔ Encoding handled correctly
    ```
    """)
    return


@app.cell
def _(df_check, plt):
    # 📊 Optional plot (nice for class)

    plt.figure(figsize=(8,4))
    plt.bar(df_check["file"], df_check["difference"])
    plt.title("Difference: wc -l vs DuckDB COUNT(*)")
    plt.ylabel("Line Difference")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 5 — Peek at Raw Orders and Order Details

    **Why are we doing this step?**
    Students should see the original structure before any cleaning.
    This makes later transformations more meaningful.

    **Implementation in Python + DuckDB**
    We read the first few rows directly from the CSV files.

    **Very nice plotting**
    No plot here.

    **Business analysis**
    Still descriptive only.
    We are understanding operational data capture.
    """)
    return


@app.cell
def _(ORDERS_2015, show):
    show(f"""
    SELECT * 
    FROM read_csv_auto('{ORDERS_2015}', header=True) 
    LIMIT 10""")
    return


@app.cell
def _(ORDER_DETAILS_2015, show):
    show(f"""
    SELECT * 
    FROM read_csv_auto('{ORDER_DETAILS_2015}', header=True) 
    LIMIT 10""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Bronze Layer

    ## Cell 6 — Create Warehouse Schemas

    **Why are we doing this step?**
    The Bronze, Silver, and Gold schemas organize the warehouse by trust level and business readiness.

    **Implementation in Python + DuckDB**
    We create one schema per layer.

    **Very nice plotting**
    No plot here.

    **Business analysis**
    No business insight yet. This is structural setup.
    """)
    return


@app.cell
def _(con):
    con.execute("CREATE SCHEMA IF NOT EXISTS bronze;").fetchall()
    con.execute("CREATE SCHEMA IF NOT EXISTS silver;").fetchall()
    con.execute("CREATE SCHEMA IF NOT EXISTS gold;").fetchall()
    print("Schemas ready: bronze, silver, gold")
    return


@app.cell
def _(con):
    # check schemas:
    con.execute("""
    SELECT distinct schema_name
    FROM information_schema.schemata
    ORDER BY schema_name;
    """).fetchdf()
    return


@app.cell
def _(con):
    # Show schemas + tables together:
    con.execute("""
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE table_schema IN ('bronze', 'silver', 'gold')
    ORDER BY table_schema, table_name;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 7 — Ingest Bronze Orders as Text-First Tables

    **Why are we doing this step?**
    Because the orders files contain mixed date formats and possible messy values, it is safer to ingest them initially as text-like values.

    **Implementation in Python + DuckDB**
    We use `read_csv_auto` for fast CSV ingestion, then store the raw results in Bronze tables.
    Later, Silver will apply type validation and business rules.

    **Very nice plotting**
    No plot here.

    **Business analysis**
    No business insight yet. We are preserving source fidelity.
    """)
    return


@app.cell
def _(ORDERS_2015, ORDERS_2016, con):
    con.execute(f"""
    CREATE OR REPLACE TABLE bronze.orders_2015_raw AS
    SELECT * FROM read_csv_auto('{ORDERS_2015}', header=True, all_varchar=True)
    """).fetchall()

    con.execute(f"""
    CREATE OR REPLACE TABLE bronze.orders_2016_raw AS
    SELECT * FROM read_csv_auto('{ORDERS_2016}', header=True, all_varchar=True)
    """).fetchall()

    con.execute("""
    CREATE OR REPLACE TABLE bronze.orders_raw AS
    SELECT 2015 AS source_year, * FROM bronze.orders_2015_raw
    UNION ALL
    SELECT 2016 AS source_year, * FROM bronze.orders_2016_raw
    """).fetchall()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 🧰 ✅ Cell: Inspect bronze.orders_raw

    ```
    📌 1. Why we are doing this

    We just combined 2015 and 2016 raw orders into a single Bronze table.
    Now we need to:
    	•	Verify the data loaded correctly
    	•	Inspect structure and sample rows
    	•	Validate row counts
    ```
    """)
    return


@app.cell
def _(con):
    # 🧪 2. Implementation (DuckDB) 🔹 Sample rows
    print("📄 Sample rows from bronze.orders_raw")
    con.execute("""
    SELECT *
    FROM bronze.orders_raw
    LIMIT 10
    """).fetchdf()
    return


@app.cell
def _(con):
    # 🔹 Row count (total)

    print("📊 Total row count")
    con.execute("""
    SELECT COUNT(*) AS total_rows
    FROM bronze.orders_raw
    """).fetchdf()
    return


@app.cell
def _(con):
    # 🔹 Row count by year (VERY IMPORTANT)

    print("📊 Row count by source_year")
    df_orders_counts = con.execute("""
    SELECT source_year, COUNT(*) AS row_count
    FROM bronze.orders_raw
    GROUP BY source_year
    ORDER BY source_year
    """).fetchdf()

    df_orders_counts
    return (df_orders_counts,)


@app.cell
def _(df_orders_counts, plt):
    # 📊 3. Nice Plot


    plt.figure(figsize=(5,3))
    plt.bar(df_orders_counts["source_year"].astype(str),
            df_orders_counts["row_count"])
    plt.title("Orders Count by Year (Bronze)")
    plt.xlabel("Year")
    plt.ylabel("Number of Orders")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧠 4. Business Analysis

    ```
    - Orders from both 2015 and 2016 are successfully combined
    - Row counts per year match expected ingestion values
    - 2016 has more orders → consistent with simulated growth
    - Data is still raw (strings, mixed formats, possible duplicates)

    Next:
    👉 Move to Silver layer to clean:
    - Date formats
    - Missing order_id
    - Duplicate records
    ```
    """)
    return


@app.cell
def _(con):
    # 🔥 Optional (VERY STRONG ADDITION)
    # 🔍 Check for NULL order_id (preview Silver issue)

    con.execute("""
    SELECT COUNT(*) AS null_order_id
    FROM bronze.orders_raw
    WHERE order_id IS NULL OR order_id = ''
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Some Notes:

    ```
    🎯 Why this is excellent
    	•	✔ Validates your UNION logic
    	•	✔ Introduces source_year concept
    	•	✔ Sets up Silver cleaning naturally
    	•	✔ Shows growth (2015 → 2016)

    ⸻

    🚀 Next Step

    We continue the same pattern for:

    👉 bronze.order_details_raw

    Then:

    👉 Move to Silver layer cleaning (your business rules in SQL)

    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 8 — Ingest Bronze Order Details Carefully

    **Why are we doing this step?**
    The order details files may contain structural problems.
    We want a Bronze strategy that is flexible enough to load what it can, while postponing strict validation to Silver.

    **Implementation in Python + DuckDB**
    We ingest the files with text-first handling.
    If your local messy files require additional CSV options, this is the cell to adjust.

    **Very nice plotting**
    No plot here.

    **Business analysis**
    Still technical ingestion only.
    """)
    return


@app.cell
def _(ORDER_DETAILS_2015, ORDER_DETAILS_2016, con):
    con.execute(f"""
    CREATE OR REPLACE TABLE bronze.order_details_2015_raw AS
    SELECT * FROM read_csv_auto('{ORDER_DETAILS_2015}', header=True, all_varchar=True)
    """).fetchall()

    con.execute(f"""
    CREATE OR REPLACE TABLE bronze.order_details_2016_raw AS
    SELECT * FROM read_csv_auto('{ORDER_DETAILS_2016}', header=True, all_varchar=True)
    """).fetchall()

    con.execute("""
    CREATE OR REPLACE TABLE bronze.order_details_raw AS
    SELECT 2015 AS source_year, * FROM bronze.order_details_2015_raw
    UNION ALL
    SELECT 2016 AS source_year, * FROM bronze.order_details_2016_raw
    """).fetchall()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Inspect `bronze.order_details_raw`

    ```
    1. Why we are doing this

    We combined 2015 and 2016 order-detail
    rows into one Bronze table.

        Now we want to verify:
    	•	the union worked correctly
    	•	the table shape looks right
    	•	row counts by year match expectations
    	•	the table is ready for Silver cleaning

    This is important because order_details_raw is the
    future fact-like source for the warehouse.
    ```
    """)
    return


@app.cell
def _(con):
    # 2. Implementation in Python + DuckDB
    #
    # Created the combined Bronze table: bronze.order_details_raw
    # 
    # Sample rows

    print("📄 Sample rows from bronze.order_details_raw")
    con.execute("""
    SELECT *
    FROM bronze.order_details_raw
    LIMIT 10
    """).fetchdf()
    return


@app.cell
def _(con):
    # Total row count

    print("📊 Total row count")
    con.execute("""
    SELECT COUNT(*) AS total_rows
    FROM bronze.order_details_raw
    """).fetchdf()
    return


@app.cell
def _(con):
    # Row count by year

    print("📊 Row count by source_year")
    df_od_counts = con.execute("""
    SELECT source_year, COUNT(*) AS row_count
    FROM bronze.order_details_raw
    GROUP BY source_year
    ORDER BY source_year
    """).fetchdf()

    df_od_counts
    return (df_od_counts,)


@app.cell
def _(con):
    # Quick structure check

    print("🧱 Schema of bronze.order_details_raw")
    con.execute("""
    DESCRIBE bronze.order_details_raw
    """).fetchdf()
    return


@app.cell
def _(df_od_counts, plt):
    # 3. Very Nice Plotting


    plt.figure(figsize=(5, 3))
    plt.bar(df_od_counts["source_year"].astype(str), df_od_counts["row_count"])
    plt.title("Order Details Count by Year (Bronze)")
    plt.xlabel("Year")
    plt.ylabel("Number of Rows")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Business Analysis

    ```
    - order_details_raw contains many more rows than
      orders_raw, which is expected

    - one order may contain multiple pizza lines

    - 2016 has more detail rows than 2015,
      which matches the additional synthetic growth

    - this table is the strongest candidate for
      the future fact table source

    - at Bronze level, all values are still raw strings
      and have not been validated yet

    Next:
    👉 inspect pizzas and pizza_types, then move to Silver cleaning
    ```
    """)
    return


@app.cell
def _(con):
    # Strong optional checks
    # These are very useful before Silver.
    #
    # Check for missing fields

    con.execute("""
    SELECT
        SUM(CASE WHEN order_details_id IS NULL OR trim(order_details_id) = '' THEN 1 ELSE 0 END) AS missing_order_details_id,
        SUM(CASE WHEN order_id IS NULL OR trim(order_id) = '' THEN 1 ELSE 0 END) AS missing_order_id,
        SUM(CASE WHEN pizza_id IS NULL OR trim(pizza_id) = '' THEN 1 ELSE 0 END) AS missing_pizza_id,
        SUM(CASE WHEN quantity IS NULL OR trim(quantity) = '' THEN 1 ELSE 0 END) AS missing_quantity
    FROM bronze.order_details_raw
    """).fetchdf()
    return


@app.cell
def _(con):
    # Check for exact duplicates

    con.execute("""
    SELECT COUNT(*) AS duplicate_rows
    FROM (
        SELECT
            source_year,
            order_details_id,
            order_id,
            pizza_id,
            quantity,
            COUNT(*) AS cnt
        FROM bronze.order_details_raw
        GROUP BY
            source_year,
            order_details_id,
            order_id,
            pizza_id,
            quantity
        HAVING COUNT(*) > 1
    ) d
    """).fetchdf()
    return


@app.cell
def _(con):
    # Check row counts relative to orders

    con.execute("""
    SELECT
        o.source_year,
        COUNT(DISTINCT o.order_id) AS num_orders,
        COUNT(d.order_details_id) AS num_order_detail_rows,
        ROUND(COUNT(d.order_details_id) * 1.0 / COUNT(DISTINCT o.order_id), 2) AS avg_detail_rows_per_order
    FROM bronze.orders_raw o
    LEFT JOIN bronze.order_details_raw d
        ON o.source_year = d.source_year
       AND o.order_id = d.order_id
    GROUP BY o.source_year
    ORDER BY o.source_year
    """).fetchdf()
    return


@app.cell
def _(con):
    # Show schemas + tables together:
    con.execute("""
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE table_schema IN ('bronze', 'silver', 'gold')
    ORDER BY table_schema, table_name;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Next...

    ```
    That last one is especially nice because
    it starts connecting the business idea:
    an order can contain multiple pizzas.

    Next after this should be bronze.pizzas_raw
    and bronze.pizza_types_raw, then we move into Silver.
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 9 — Ingest Reference Tables into Bronze

    **Why are we doing this step?**
    `pizzas.csv` and `pizza_types.csv` are reference/master data that will feed the Gold dimensions later.

    **Implementation in Python + DuckDB**
    We ingest them into Bronze as well, so every source is represented in the warehouse pipeline.

    **Very nice plotting**
    No plot here.

    **Business analysis**
    No insight yet. This is foundational modeling work.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Create `bronze.pizzas_raw`
    """)
    return


@app.cell
def _(PIZZAS, con):
    con.execute(f"""
    CREATE OR REPLACE TABLE bronze.pizzas_raw AS
    SELECT * FROM read_csv_auto('{PIZZAS}', header=True, all_varchar=True)
    """).fetchall()
    return


@app.cell
def _(con):
    # Inspect count of rows: for bronze.pizzas_raw

    con.execute("""
    SELECT COUNT(*) 
    FROM bronze.pizzas_raw
    """).fetchdf()
    return


@app.cell
def _(con):
    # View Rows for bronze.pizzas_raw

    con.execute("""
    SELECT * 
    FROM bronze.pizzas_raw
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Create `bronze.pizza_types_raw`
    """)
    return


@app.cell
def _(PIZZA_TYPES, con):
    con.execute(f"""
    CREATE OR REPLACE TABLE bronze.pizza_types_raw AS
    SELECT *
    FROM read_csv_auto(
        '{PIZZA_TYPES}',
        header = TRUE,
        all_varchar = TRUE,
        encoding = 'IBM_1252',
        ignore_errors = FALSE
    )
    """).fetchall()

    con.execute(f"""
    DESCRIBE bronze.pizza_types_raw
    """).fetchdf()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT COUNT(*) 
    FROM bronze.pizza_types_raw
    """).fetchdf()
    return


@app.cell
def _(con):
    # Check the rows for bronze.pizza_types_raw
    con.execute("""
    SELECT * 
    FROM bronze.pizza_types_raw 
    LIMIT 5
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # VERIFY bronze.pizza_types_raw
    """)
    return


@app.cell
def _(con):
    _df = con.execute("SELECT * FROM bronze.pizza_types_raw").fetchdf()

    print(_df.shape)

    print(_df.columns)

    print(_df.head)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## BIG PROBLEM:
    ## we have 1 column instead of 4 columns in `bronze.pizza_types_raw`

    ## FIX the PROBLEM
    """)
    return


@app.cell
def _(con):
    # Fix 1: normalize text
    # Python normalization

    import unicodedata

    def normalize_text(s):
        if s is None:
            return s

        return unicodedata.normalize('NFKC', s)
    #end-def

    df = con.execute("""
    SELECT * 
    FROM bronze.pizza_types_raw
    """).fetchdf()

    df = df.map(normalize_text)
    return (df,)


@app.cell
def _(df):
    df.shape

    ### 35 rows
    ### 1 column ==> PROBLEM: there must be 4 columns
    return


@app.cell
def _():
    ## PROBLEM: 1 column instead of 4 columns in bronze.pizza_types_raw
    ## FIX the PROBLEM
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### PROBLEM:
    ```
    it seems that we did not read the pizza_types.csv
    file properly: we are supposed to have 4 columns,
    but we got ONE (1) column.
    ```
    """)
    return


@app.cell
def _(df):
    df.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### FIX The PROBLEM
    ### FIX the `pizza_types.csv` File -> `pizza_types_fixed.csv`
    """)
    return


@app.cell
def _(PIZZA_TYPES):
    # FIX the pizza_types.csv File => "pizza_types_fixed.csv"

    fixed_file = "./data/pizza_types_fixed.csv"

    with open(PIZZA_TYPES, "r", encoding="cp1252") as f:
        content = f.read()

    # Replace full-width commas with normal commas
    content = content.replace("，", ",")

    with open(fixed_file, "w", encoding="utf-8") as f:
        f.write(content)
    return (fixed_file,)


@app.cell
def _(con, fixed_file):
    # Reload in DuckDB
    con.execute(f"""
    CREATE OR REPLACE TABLE bronze.pizza_types_raw AS
    SELECT *
    FROM read_csv_auto(
        '{fixed_file}',
        header = TRUE,
        all_varchar = TRUE
    )
    """).fetchall()
    return


@app.cell
def _(con):
    # VERIFY bronze.pizza_types_raw

    _df = con.execute("SELECT * FROM bronze.pizza_types_raw").fetchdf()

    print(_df.shape)

    print(_df.columns)

    print(_df.head)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 10 — Bronze Data Quality Profile for Orders

    **Why are we doing this step?**
    Before cleaning, students should **measure the mess**.
    This makes Silver transformations evidence-based instead of arbitrary.

    **Implementation in Python + DuckDB**
    We profile the Bronze orders for:
    - missing order IDs
    - mixed date formats
    - exact duplicate rows

    **Very nice plotting**
    We produce a compact data-quality bar chart.

    **Business analysis**
    The business cannot trust revenue, order counts, or peak-hour trends until these issues are controlled.
    """)
    return


@app.cell
def _(con):
    bronze_orders_profile_sql = """
    WITH base AS (
        SELECT * FROM bronze.orders_raw
    ),
    metrics AS (
        SELECT 'missing_order_id' AS metric, COUNT(*)::BIGINT AS cnt
        FROM base
        WHERE order_id IS NULL OR trim(order_id) = ''

        UNION ALL

        SELECT 'yyyy_mm_dd_dates', COUNT(*)::BIGINT
        FROM base
        WHERE try_strptime(date, '%Y-%m-%d') IS NOT NULL

        UNION ALL

        SELECT 'mm_dd_yyyy_dates', COUNT(*)::BIGINT
        FROM base
        WHERE try_strptime(date, '%m/%d/%Y') IS NOT NULL

        UNION ALL

        SELECT 'unparseable_dates', COUNT(*)::BIGINT
        FROM base
        WHERE try_strptime(date, '%Y-%m-%d') IS NULL
          AND try_strptime(date, '%m/%d/%Y') IS NULL

        UNION ALL

        SELECT 'exact_duplicate_rows', COUNT(*)::BIGINT
        FROM (
            SELECT source_year, order_id, date, time, COUNT(*) AS n
            FROM base
            GROUP BY ALL
            HAVING COUNT(*) > 1
        )
    )
    SELECT * FROM metrics;
    """
    bronze_orders_profile = con.execute(bronze_orders_profile_sql).fetchdf()
    bronze_orders_profile
    return (bronze_orders_profile,)


@app.cell
def _(bronze_orders_profile, plt):
    plt.figure(figsize=(9, 4))
    plt.bar(bronze_orders_profile["metric"], bronze_orders_profile["cnt"])
    plt.title("Bronze Orders Data Quality Profile")
    plt.xlabel("Metric")
    plt.ylabel("Count")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 11 — Bronze Data Quality Profile for Order Details

    **Why are we doing this step?**
    The order details table is the future fact table driver.
    If it is broken, sales analysis will be wrong.

    **Implementation in Python + DuckDB**
    We profile:
    - missing IDs
    - missing order references
    - missing pizza references
    - missing quantity
    - duplicate detail IDs

    **Very nice plotting**
    We create a second quality chart.

    **Business analysis**
    If order detail quality is weak, measures such as quantity sold and revenue become unreliable.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT 
        COUNT(*) AS total_rows,
        SUM(CASE WHEN order_details_id IS NULL OR trim(order_details_id) = '' THEN 1 ELSE 0 END) AS empty_ids
    FROM bronze.order_details_raw
    """).fetchdf()
    return


@app.cell
def _(con):
    # ✅ Fix: detect true duplicate rows in bronze.order_details_raw
    con.execute("""
    SELECT 
        'duplicate_full_rows' AS metric,
        COALESCE(SUM(cnt - 1), 0) AS cnt
    FROM (
        SELECT 
            order_details_id,
            order_id,
            pizza_id,
            quantity,
            COUNT(*) AS cnt
        FROM bronze.order_details_raw
        GROUP BY 
            order_details_id,
            order_id,
            pizza_id,
            quantity
        HAVING COUNT(*) > 1
    ) t
    """).fetchdf()

    # 🎯 What this means (important)
    # 👉 Your order_details_raw table:
    #	•	✔ Has no exact duplicate rows
    #	•	✔ Each row is unique at the full-record level
    #	•	✔ Data is cleaner than expected (good!)
    return


@app.cell
def _(con):
    #👉 This shows:
    #	•	repeated IDs
    #	•	but not identical rows
    con.execute("""
    SELECT order_details_id, 
           COUNT(*) AS cnt
    FROM bronze.order_details_raw
    GROUP BY order_details_id
    HAVING COUNT(*) > 1
    ORDER BY cnt DESC
    LIMIT 10
    """).fetchdf()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT 
        COUNT(*) AS total_rows,
        COUNT(DISTINCT order_details_id) AS distinct_ids
    FROM bronze.order_details_raw
    """).fetchdf()

    # NOTE ------------------------------------------------
    #      🧠 The real issue is conceptual
    #.     ❗ order_details_id is NOT a unique identifier
    #-------------------------------------------------------
    return


@app.cell
def _(con):
    bronze_details_profile_sql = """
    WITH base AS (
        SELECT * FROM bronze.order_details_raw
    ),

    -- normalize fields
    normalized AS (
        SELECT
            TRIM(order_details_id) AS order_details_id,
            TRIM(order_id) AS order_id,
            TRIM(pizza_id) AS pizza_id,
            TRIM(quantity) AS quantity
        FROM base
    ),

    -- valid IDs only
    valid_ids AS (
        SELECT *
        FROM normalized
        WHERE order_details_id IS NOT NULL
          AND order_details_id <> ''
    ),

    -- ID reuse (NOT duplicates)
    id_stats AS (
        SELECT 
            order_details_id,
            COUNT(*) AS cnt
        FROM valid_ids
        GROUP BY order_details_id
        HAVING COUNT(*) > 1
    ),

    -- true duplicate rows
    dup_rows AS (
        SELECT 
            order_details_id,
            order_id,
            pizza_id,
            quantity,
            COUNT(*) AS cnt
        FROM normalized
        GROUP BY 
            order_details_id,
            order_id,
            pizza_id,
            quantity
        HAVING COUNT(*) > 1
    ),

    metrics AS (

        -- total rows
        SELECT 'total_rows' AS metric, COUNT(*)::BIGINT AS cnt
        FROM normalized

        UNION ALL

        -- unique full rows (NEW METRIC)
        SELECT 'unique_order_details_rows', COUNT(*)::BIGINT
        FROM (
            SELECT DISTINCT
                order_details_id,
                order_id,
                pizza_id,
                quantity
            FROM normalized
        )

        UNION ALL

        -- missing fields
        SELECT 'missing_order_details_id', COUNT(*)::BIGINT
        FROM normalized
        WHERE order_details_id IS NULL OR order_details_id = ''

        UNION ALL

        SELECT 'missing_order_id', COUNT(*)::BIGINT
        FROM normalized
        WHERE order_id IS NULL OR order_id = ''

        UNION ALL

        SELECT 'missing_pizza_id', COUNT(*)::BIGINT
        FROM normalized
        WHERE pizza_id IS NULL OR pizza_id = ''

        UNION ALL

        SELECT 'missing_quantity', COUNT(*)::BIGINT
        FROM normalized
        WHERE quantity IS NULL OR quantity = ''

        -- TRUE duplicates
        UNION ALL

        SELECT 'duplicate_full_rows', COALESCE(SUM(cnt - 1), 0)::BIGINT
        FROM dup_rows

        -- key integrity
        UNION ALL

        SELECT 'non_unique_order_details_id_groups', COUNT(*)::BIGINT
        FROM id_stats

        UNION ALL

        SELECT 'non_unique_order_details_id_extra_rows', COALESCE(SUM(cnt - 1), 0)::BIGINT
        FROM id_stats
    )

    SELECT * FROM metrics
    ORDER BY metric;
    """

    bronze_details_profile = con.execute(bronze_details_profile_sql).fetchdf()
    bronze_details_profile
    return (bronze_details_profile,)


@app.cell
def _(bronze_details_profile, plt):
    plt.figure(figsize=(10, 4))
    plt.bar(bronze_details_profile["metric"], bronze_details_profile["cnt"])
    plt.title("Bronze Order Details Data Quality Profile")
    plt.xlabel("Metric")
    plt.ylabel("Count")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Silver Layer

    ## Cell 12 — Clean and Standardize Orders

    **Why are we doing this step?**
    This is the first true business-trust layer.
    We standardize dates, remove unusable rows, and de-duplicate exact copies.

    **Implementation in Python + DuckDB**
    Business rules applied here:
    - mixed date formats consolidated to one valid date
    - rows with NULL order_id removed
    - rows with unparseable dates removed
    - exact duplicate rows removed

    **Very nice plotting**
    No plot in the build step. We will profile results in the next cell.

    **Business analysis**
    After this step, order counts become much more credible.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```
    Now we’re moving into the heart of the course.
    Silver Layer, in the correct order, with:
    	•	✔ clear reasoning (why)
    	•	✔ DuckDB-first SQL
    	•	✔ minimal Python (only where needed)
    	•	✔ validation + plots
    	•	✔ strong teaching narrative

    ⸻

    ⚪ CELL 8 — SILVER LAYER (FULL PIPELINE)

    ⸻

    🧠 1. What is Silver Layer (very short)

    Bronze = raw data
    Silver = cleaned, validated, standardized data

    👉 In Silver, we enforce:
    	•	data types
    	•	NULL rules
    	•	referential integrity
    	•	consistent formats
    	•	reliable keys

    ⸻

    🚨 IMPORTANT ORDER (DO NOT CHANGE)

    We must build in this order:

    1. pizzas_clean
    2. pizza_types_clean
    3. orders_clean
    4. order_details_clean   (depends on all above)
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ⚪ STEP 1 — silver.pizzas_clean
    ```

    📌 Why
    	•	Validate product catalog
    	•	Enforce correct price + size
    	•	Remove bad rows
    ```
    """)
    return


@app.cell
def _(con):
    # 🧪 Implementation: CREATE silver.pizzas_clean

    con.execute("""
    CREATE OR REPLACE TABLE silver.pizzas_clean AS
    WITH base AS (
        SELECT
            TRIM(pizza_id) AS pizza_id,
            TRIM(pizza_type_id) AS pizza_type_id,
            UPPER(TRIM(size)) AS size,
            TRIM(price) AS raw_price
        FROM bronze.pizzas_raw
    ),

    typed AS (
        SELECT
            pizza_id,
            pizza_type_id,
            size,
            TRY_CAST(raw_price AS DOUBLE) AS price
        FROM base
    ),

    filtered AS (
        SELECT DISTINCT *
        FROM typed
        WHERE pizza_id IS NOT NULL 
          AND pizza_id <> ''
          AND pizza_type_id IS NOT NULL 
          AND pizza_type_id <> ''
          AND size IN ('S','M','L','XL','XXL')
          AND price IS NOT NULL
          AND price > 0
    )

    SELECT * FROM filtered;
    """).fetchall()

    pizzas_clean_5_rows = con.execute("""
    SELECT *
    FROM silver.pizzas_clean
    LIMIT 5
    """).fetchdf()

    pizzas_clean_5_rows
    return


@app.cell
def _(con):
    #----------------
    # 📊 Count & Plot
    #----------------

    df_2 = con.execute("""
    SELECT size, 
           COUNT(*) AS cnt
    FROM silver.pizzas_clean
    GROUP BY size
    """).fetchdf()
    df_2
    return (df_2,)


@app.cell
def _(df_2, plt):
    plt.bar(df_2["size"], df_2["cnt"])
    plt.title("Pizza Distribution by Size")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧠 Business Insight
    ```
    	•	Menu coverage across sizes
    	•	Helps pricing + demand analysis

    ⸻

    🟡 STEP 2 — silver.pizza_types_clean

    ⸻

    📌 Why
    	•	Fix Unicode issues
    	•	Clean product descriptions
    	•	Ensure joinable dimension

    ⸻
    ```
    """)
    return


@app.cell
def _(con):
    # CREATE silver.pizza_types_clean

    con.execute("""
    CREATE OR REPLACE TABLE silver.pizza_types_clean AS
    SELECT DISTINCT *
    FROM bronze.pizza_types_raw
    WHERE pizza_type_id IS NOT NULL
      AND pizza_type_id <> ''
    """).fetchall()

    all_rows = con.execute("""
    SELECT * 
    FROM silver.pizza_types_clean 
    """).fetchdf()

    all_rows
    return


@app.cell
def _(con, plt):
    # 📊 Plot

    _df = con.execute("""
    SELECT category, COUNT(*) AS cnt
    FROM silver.pizza_types_clean
    GROUP BY category
    """).fetchdf()

    plt.bar(_df["category"], _df["cnt"])
    plt.title("Pizza Types by Category")
    plt.xticks(rotation=30)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧠 Business Insight
    ```
    	•	Category mix (Chicken, Veggie, etc.)
    	•	Important for promotions

    ⸻

    🟡 STEP 3 — silver.orders_clean

    ⸻

    📌 Why
    	•	Fix mixed date formats
    	•	Remove invalid orders
    	•	Create reliable time dimension

    ⸻
    ```
    """)
    return


@app.cell
def _(con):
    # 🧪 Implementation: CREATE silver.orders_clean

    con.execute("""
    CREATE OR REPLACE TABLE silver.orders_clean AS
    WITH base AS (
        SELECT
            CAST(source_year AS INTEGER) AS source_year,
            TRIM(order_id) AS order_id,
            TRIM(date) AS raw_date,
            TRIM(time) AS raw_time
        FROM bronze.orders_raw
    ),

    parsed AS (
        SELECT
            source_year,
            order_id,
            COALESCE(
                TRY_STRPTIME(raw_date, '%Y-%m-%d'),
                TRY_STRPTIME(raw_date, '%m/%d/%Y')
            ) AS order_date,
            TRY_STRPTIME(raw_time, '%H:%M:%S') AS order_time
        FROM base
    ),

    filtered AS (
        SELECT DISTINCT
            source_year,
            CAST(order_id AS BIGINT) AS order_id,
            CAST(order_date AS DATE) AS order_date,
            CAST(order_time AS TIME) AS order_time
        FROM parsed
        WHERE order_id IS NOT NULL
          AND order_id <> ''
          AND TRY_CAST(order_id AS BIGINT) IS NOT NULL
          AND order_date IS NOT NULL
          AND order_time IS NOT NULL
    )

    SELECT * FROM filtered;
    """).fetchall()
    return


@app.cell
def _(con, plt):
    # 📊 Plot

    _df = con.execute("""
    SELECT EXTRACT(HOUR FROM order_time) AS hour, 
           COUNT(*) AS cnt
    FROM silver.orders_clean
    GROUP BY hour
    ORDER BY hour
    """).fetchdf()

    plt.plot(_df["hour"], _df["cnt"])
    plt.title("Orders by Hour")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧠 Business Insight
    ```
    	•	Identify peak hours
    	•	Staffing optimization

    ⸻

    🟡 STEP 4 — silver.order_details_clean

    ⸻

    📌 Why (CRITICAL)

    This is your future FACT table

    We must:
    	•	remove bad rows
    	•	enforce referential integrity
    	•	fix types
    	•	create surrogate key

    ⸻
    ```
    """)
    return


@app.cell
def _(con):
    # 🧪 Implementation: CREATE silver.order_details_clean

    con.execute("""
    CREATE OR REPLACE TABLE silver.order_details_clean AS
    WITH base AS (
        SELECT
            CAST(source_year AS INTEGER) AS source_year,
            TRIM(order_details_id) AS raw_id,
            TRIM(order_id) AS raw_order_id,
            TRIM(pizza_id) AS pizza_id,
            TRIM(quantity) AS raw_quantity
        FROM bronze.order_details_raw
    ),

    typed AS (
        SELECT
            source_year,
            TRY_CAST(raw_id AS BIGINT) AS raw_id,
            TRY_CAST(raw_order_id AS BIGINT) AS order_id,
            pizza_id,
            TRY_CAST(raw_quantity AS INTEGER) AS quantity
        FROM base
    ),

    filtered AS (
        SELECT DISTINCT *
        FROM typed
        WHERE raw_id IS NOT NULL
          AND order_id IS NOT NULL
          AND pizza_id IS NOT NULL
          AND pizza_id <> ''
          AND quantity IS NOT NULL
          AND quantity > 0
    ),

    joined AS (
        SELECT f.*
        FROM filtered f
        JOIN silver.orders_clean o
          ON f.source_year = o.source_year
         AND f.order_id = o.order_id
        JOIN silver.pizzas_clean p
          ON f.pizza_id = p.pizza_id
    ),

    finalized AS (
        SELECT
            ROW_NUMBER() OVER (
                ORDER BY source_year, order_id, pizza_id
            ) AS order_details_sk,
            *
        FROM joined
    )

    SELECT * FROM finalized;
    """).fetchall()
    return


@app.cell
def _(con, plt):
    # 📊 Plot silver.order_details_clean

    _df = con.execute("""
    SELECT source_year, 
           COUNT(*) AS cnt
    FROM silver.order_details_clean
    GROUP BY source_year
    """).fetchdf()

    plt.bar(_df["source_year"], _df["cnt"])
    plt.title("Order Details by Year")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧠 Business Insight
    ```
    	•	Growth from 2015 → 2016
    	•	More granular than orders

    ⸻

    🔍 FINAL VALIDATION (VERY IMPORTANT)

    ⸻

    ✔ Surrogate key uniqueness
    ```
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT COUNT(*) AS total,
           COUNT(DISTINCT order_details_sk) AS unique_sk
    FROM silver.order_details_clean
    """).fetchdf()
    return


@app.cell
def _(con):
    # CHECK ✔ Referential integrity

    con.execute("""
    SELECT COUNT(*) AS bad_rows
    FROM silver.order_details_clean d
    LEFT JOIN silver.orders_clean o
    ON d.order_id = o.order_id
    WHERE o.order_id IS NULL
    """).fetchdf()
    return


@app.cell
def _(con):
    # CHECK ✔ NULL checks

    con.execute("""
    SELECT 
        SUM(order_id IS NULL) AS null_order_id,
        SUM(pizza_id IS NULL) AS null_pizza_id
    FROM silver.order_details_clean
    """).fetchdf()
    return


@app.cell
def _(con):
    # 📊 FINAL PLOT — Bronze vs Silver

    df_3 = con.execute("""
    SELECT 'bronze' AS layer, COUNT(*) AS cnt FROM bronze.order_details_raw
    UNION ALL
    SELECT 'silver', COUNT(*) FROM silver.order_details_clean
    """).fetchdf()

    df_3
    return (df_3,)


@app.cell
def _(df_3, plt):
    plt.bar(df_3["layer"], df_3["cnt"])
    plt.title("Bronze vs Silver Row Count")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 🎓 FINAL BUSINESS SUMMARY

    ```
    Silver layer transforms messy operational data
    into reliable analytical data.

    Key improvements:
    - dates standardized
    - invalid rows removed
    - referential integrity enforced
    - unreliable keys replaced with surrogate key
    - data now consistent and queryable

    This layer is now ready for:
    👉 Gold star schema modeling
    👉 OLAP queries
    👉 BI dashboards

    ⸻

    🚀 NEXT STEP

    You are now ready for:

    🟡 Cell 9 — GOLD LAYER

    We will build:
    	•	fact table
    	•	dimension tables
    	•	star schema
    	•	OLAP queries

    ⸻

    👉 Cell 9: Gold Layer (star schema + OLAP + plots)
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## CREATE  silver.orders_clean
    """)
    return


@app.cell
def _(con):
    # CREATE  silver.orders_clean

    con.execute("""
    CREATE OR REPLACE TABLE silver.orders_clean AS
    WITH standardized AS (
        SELECT
            source_year,
            trim(order_id) AS order_id_raw,
            COALESCE(
                try_strptime(trim(date), '%Y-%m-%d'),
                try_strptime(trim(date), '%m/%d/%Y')
            )::DATE AS order_date,
            trim(time) AS order_time
        FROM bronze.orders_raw
    ),
    filtered AS (
        SELECT *
        FROM standardized
        WHERE order_id_raw IS NOT NULL
          AND order_id_raw <> ''
          AND order_date IS NOT NULL
          AND order_time IS NOT NULL
          AND order_time <> ''
    ),
    deduped AS (
        SELECT DISTINCT
            source_year,
            CAST(order_id_raw AS BIGINT) AS order_id,
            order_date,
            order_time
        FROM filtered
    )
    SELECT * FROM deduped
    """).fetchall()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 13 — Validate Silver Orders Outcome

    **Why are we doing this step?**
    Students should see how many rows survived cleaning and how many were rejected.

    **Implementation in Python + DuckDB**
    We compare Bronze counts versus Silver counts.

    **Very nice plotting**
    A before-vs-after chart helps students visualize the cost of quality rules.

    **Business analysis**
    A small drop may be healthy.
    A large drop signals source-system problems that management should know about.
    """)
    return


@app.cell
def _(con):
    silver_orders_audit_sql = """
    SELECT 'bronze_orders_raw' AS stage, COUNT(*) AS row_count FROM bronze.orders_raw
    UNION ALL
    SELECT 'silver_orders_clean', COUNT(*) FROM silver.orders_clean
    """
    silver_orders_audit = con.execute(silver_orders_audit_sql).fetchdf()
    silver_orders_audit
    return (silver_orders_audit,)


@app.cell
def _(plt, silver_orders_audit):
    plt.figure(figsize=(7, 4))
    plt.bar(silver_orders_audit["stage"], silver_orders_audit["row_count"])
    plt.title("Orders: Bronze vs Silver")
    plt.xlabel("Stage")
    plt.ylabel("Rows")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 14 — Clean and Validate Order Details

    **Why are we doing this step?**
    This is the heart of the Silver layer because `order_details` will become the transaction-level sales table.

    **Implementation in Python + DuckDB**
    Business rules applied here:
    - required fields present
    - no missing values
    - positive quantity only
    - valid order reference
    - valid pizza reference
    - de-duplicate by exact row and detail ID

    **Very nice plotting**
    No plot in the build step.

    **Business analysis**
    Only after this step can we trust quantity and revenue measures.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.order_details_clean AS
    WITH base AS (
        SELECT
            source_year,
            trim(order_details_id) AS order_details_id_raw,
            trim(order_id) AS order_id_raw,
            trim(pizza_id) AS pizza_id,
            trim(quantity) AS quantity_raw
        FROM bronze.order_details_raw
    ),
    filtered AS (
        SELECT *
        FROM base
        WHERE order_details_id_raw IS NOT NULL 
          AND order_details_id_raw <> ''
          AND order_id_raw IS NOT NULL AND order_id_raw <> ''
          AND pizza_id IS NOT NULL 
          AND pizza_id <> ''
          AND quantity_raw IS NOT NULL AND quantity_raw <> ''
          AND try_cast(quantity_raw AS BIGINT) IS NOT NULL
          AND try_cast(quantity_raw AS BIGINT) > 0
    ),
    deduped AS (
        SELECT DISTINCT
            CAST(order_details_id_raw AS BIGINT) AS order_details_id,
            CAST(order_id_raw AS BIGINT) AS order_id,
            pizza_id,
            CAST(quantity_raw AS BIGINT) AS quantity
        FROM filtered
    ),
    valid_orders AS (
        SELECT d.*
        FROM deduped d
        INNER JOIN silver.orders_clean o
            ON d.order_id = o.order_id
    ),
    valid_pizzas AS (
        SELECT v.*
        FROM valid_orders v
        INNER JOIN bronze.pizzas_raw p
            ON v.pizza_id = p.pizza_id
    ),
    unique_detail_id AS (
        SELECT *
        FROM (
            SELECT *,
                   ROW_NUMBER() OVER (PARTITION BY order_details_id ORDER BY order_id) AS rn
            FROM valid_pizzas
        )
        WHERE rn = 1
    )
    SELECT
        order_details_id,
        order_id,
        pizza_id,
        quantity
    FROM unique_detail_id
    """).fetchall()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 15 — Validate Silver Order Details Outcome

    **Why are we doing this step?**
    Every cleaning phase should be measurable.
    We do not want Silver rules to feel magical or hidden.

    **Implementation in Python + DuckDB**
    We compare Bronze and Silver row counts for order details.

    **Very nice plotting**
    A bar chart makes the reduction easy to discuss in class.

    **Business analysis**
    A sizable reduction may reveal source problems such as invalid pizza IDs or broken joins.
    """)
    return


@app.cell
def _(con):
    silver_details_audit_sql = """

    WITH base AS (

        SELECT
            CAST(source_year AS INTEGER) AS source_year,
            TRIM(order_details_id) AS raw_order_details_id,
            TRIM(order_id) AS raw_order_id,
            TRIM(pizza_id) AS pizza_id,
            TRIM(quantity) AS raw_quantity
        FROM bronze.order_details_raw
    ),

    typed AS (
        SELECT
            source_year,
            TRY_CAST(raw_order_details_id AS BIGINT) AS raw_order_details_id,
            TRY_CAST(raw_order_id AS BIGINT) AS order_id,
            pizza_id,
            TRY_CAST(raw_quantity AS INTEGER) AS quantity
        FROM base
    ),

    filtered_missing_invalid AS (
        SELECT *
        FROM typed
        WHERE raw_order_details_id IS NOT NULL
          AND order_id IS NOT NULL
          AND pizza_id IS NOT NULL
          AND pizza_id <> ''
          AND quantity IS NOT NULL
          AND quantity > 0
    ),

    dedup_full_rows AS (
        SELECT DISTINCT *
        FROM filtered_missing_invalid
    ),

    after_orders_join AS (
        SELECT d.*
        FROM dedup_full_rows d
        JOIN silver.orders_clean o
          ON d.source_year = o.source_year
         AND d.order_id = o.order_id
    ),

    after_pizzas_join AS (
        SELECT d.*
        FROM after_orders_join d
        JOIN silver.pizzas_clean p
          ON d.pizza_id = p.pizza_id
    )

    SELECT 'bronze_raw' AS stage, COUNT(*) FROM bronze.order_details_raw

    UNION ALL

    SELECT 'typed_cast', COUNT(*) FROM typed

    UNION ALL

    SELECT 'after_filter', COUNT(*) FROM filtered_missing_invalid

    UNION ALL

    SELECT 'after_dedup_full_rows', COUNT(*) FROM dedup_full_rows

    UNION ALL

    SELECT 'after_orders_join', COUNT(*) FROM after_orders_join

    UNION ALL

    SELECT 'after_pizzas_join (EXPECTED FINAL)', COUNT(*) FROM after_pizzas_join

    UNION ALL

    SELECT 'silver_order_details_clean (ACTUAL FINAL)', COUNT(*) FROM silver.order_details_clean

    ORDER BY stage;

    """

    silver_details_audit = con.execute(silver_details_audit_sql).fetchdf()

    silver_details_audit

    # Interpretation (clean + final)
    # ✔ Data loss is minimal and controlled
    # 107,521 → 107,429  (loss = 92 rows)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 16 — Clean Reference Tables

    **Why are we doing this step?**
    Gold dimensions depend on trusted reference data.
    We standardize the pizza and pizza type tables before dimensional modeling.

    **Implementation in Python + DuckDB**
    We trim text, cast price, and preserve pizza hierarchy.

    **Very nice plotting**
    No plot here.

    **Business analysis**
    Reliable reference data is required for category-level and product-level reporting.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.pizzas_clean AS
    SELECT DISTINCT
        trim(pizza_id) AS pizza_id,
        trim(pizza_type_id) AS pizza_type_id,
        trim(size) AS size,
        try_cast(price AS DOUBLE) AS price
    FROM bronze.pizzas_raw
    WHERE pizza_id IS NOT NULL
      AND pizza_type_id IS NOT NULL
      AND size IS NOT NULL
      AND try_cast(price AS DOUBLE) IS NOT NULL
    """).fetchall()

    silver_pizzas_clean_rows = con.execute("SELECT * from silver.pizzas_clean").fetchdf()
    silver_pizzas_clean_rows
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.pizza_types_clean AS
    SELECT DISTINCT
        trim(pizza_type_id) AS pizza_type_id,
        trim(name) AS pizza_name,
        trim(category) AS category,
        trim(ingredients) AS ingredients
    FROM bronze.pizza_types_raw
    WHERE pizza_type_id IS NOT NULL
      AND name IS NOT NULL
      AND category IS NOT NULL
    """).fetchall()

    silver_pizza_types_clean_rows = con.execute("SELECT * from silver.pizza_types_clean").fetchdf()
    silver_pizza_types_clean_rows
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Gold Layer

    ## Cell 17 — Define the Star Schema

    **Why are we doing this step?**
    This is where technical cleanup becomes business modeling.
    We define:
    - one sales fact table
    - several dimensions

    **Implementation in Python + DuckDB**
    We create:
    - `gold.dim_date`
    - `gold.dim_pizza`
    - `gold.fact_sales`

    **Very nice plotting**
    No plot yet.

    **Business analysis**
    The Gold layer is what analysts and BI tools should use.
    """)
    return


@app.cell
def _(con, show):
    con.execute("""
    CREATE OR REPLACE TABLE gold.dim_date AS
    SELECT DISTINCT
        order_date AS date_key,
        EXTRACT(YEAR FROM order_date) AS year_num,
        EXTRACT(MONTH FROM order_date) AS month_num,
        STRFTIME(order_date, '%B') AS month_name,
        EXTRACT(DAY FROM order_date) AS day_num,
        STRFTIME(order_date, '%A') AS day_name,
        EXTRACT(QUARTER FROM order_date) AS quarter_num,
        WEEKDAY(order_date) AS weekday_num
    FROM silver.orders_clean
    """).fetchall()

    show("SELECT * FROM gold.dim_date ORDER BY date_key LIMIT 10")
    return


@app.cell
def _(con, show):
    con.execute("""
    CREATE OR REPLACE TABLE gold.dim_pizza AS
    SELECT
        p.pizza_id,
        p.pizza_type_id,
        pt.pizza_name,
        pt.category,
        p.size,
        p.price,
        pt.ingredients
    FROM silver.pizzas_clean p
    JOIN silver.pizza_types_clean pt
      ON p.pizza_type_id = pt.pizza_type_id
    """).fetchall()

    show("SELECT * FROM gold.dim_pizza ORDER BY pizza_id LIMIT 10")
    return


@app.cell
def _(show):
    # 🧠 check rows of silver.order_details_clean

    show("SELECT * FROM silver.order_details_clean  LIMIT 5")
    return


@app.cell
def _(con, show):
    # 🧠 Why this is actually GOOD
    # This confirms your pipeline is correctly designed:
    # * Bronze → messy order_details_id
    # * Silver → clean order_details_sk (surrogate key: sk)
    # * Gold → should ONLY use the clean key

    con.execute("""
    CREATE OR REPLACE TABLE gold.fact_sales AS
    SELECT
        od.order_details_id,
        o.order_id,
        o.order_date AS date_key,
        o.order_time,
        od.pizza_id,
        dp.pizza_type_id,
        dp.category,
        dp.size,
        od.quantity,
        dp.price AS unit_price,
        od.quantity * dp.price AS sales_amount
    FROM silver.order_details_clean od
    JOIN silver.orders_clean o
      ON od.order_id = o.order_id
    JOIN gold.dim_pizza dp
      ON od.pizza_id = dp.pizza_id
    """).fetchall()

    show("SELECT * FROM gold.fact_sales ORDER BY order_details_id LIMIT 10")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 18 — Inspect Gold Tables

    **Why are we doing this step?**
    Students should verify that the star schema looks clean and business-friendly.

    **Implementation in Python + DuckDB**
    We preview the dimensions and fact table.

    **Very nice plotting**
    No plot here.

    **Business analysis**
    At this point, the warehouse is ready for OLAP.
    """)
    return


@app.cell
def _(show):
    show("SELECT * FROM gold.dim_date ORDER BY date_key LIMIT 10")
    return


@app.cell
def _(show):
    show("SELECT * FROM gold.dim_pizza ORDER BY pizza_id LIMIT 10")
    return


@app.cell
def _(show):
    show("SELECT * FROM gold.fact_sales ORDER BY order_details_id LIMIT 10")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # OLAP / BI Layer

    ## Cell 19 — KPI Summary

    **Why are we doing this step?**
    Before diving into charts, we want a one-row summary of key measures.

    **Implementation in Python + DuckDB**
    We compute:
    - total orders
    - total line items
    - total pizzas sold
    - total revenue

    **Very nice plotting**
    No plot here; this is a KPI table.

    **Business analysis**
    This gives management a quick operational snapshot of the pizza shop across both years.
    """)
    return


@app.cell
def _(con):
    kpi_sql = """
    SELECT
        COUNT(DISTINCT order_id) AS total_orders,
        COUNT(*) AS total_line_items,
        SUM(quantity) AS total_pizzas_sold,
        ROUND(SUM(sales_amount), 2) AS total_revenue
    FROM gold.fact_sales
    """
    con.execute(kpi_sql).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 20 — Revenue by Month

    **Why are we doing this step?**
    Monthly revenue is one of the most common business trend analyses.

    **Implementation in Python + DuckDB**
    We aggregate sales by month.

    **Very nice plotting**
    Line chart for trend over time.

    **Business analysis**
    This chart can reveal growth, seasonality, and the commercial effect of new products introduced in 2016.
    """)
    return


@app.cell
def _(con):
    monthly_revenue_sql = """
    SELECT
        DATE_TRUNC('month', date_key) AS month_start,
        ROUND(SUM(sales_amount), 2) AS revenue
    FROM gold.fact_sales
    GROUP BY 1
    ORDER BY 1
    """
    monthly_revenue = con.execute(monthly_revenue_sql).fetchdf()
    monthly_revenue.head()
    return (monthly_revenue,)


@app.cell
def _(monthly_revenue, plt):
    plt.figure(figsize=(10, 5))
    plt.plot(monthly_revenue["month_start"], monthly_revenue["revenue"], marker="o")
    plt.title("Monthly Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 21 — Orders by Hour (Peak Hours)

    **Why are we doing this step?**
    Management wants to know when demand is strongest.

    **Implementation in Python + DuckDB**
    We derive the order hour from the order time and count distinct orders.

    **Very nice plotting**
    Bar chart by hour.

    **Business analysis**
    This helps staffing, kitchen scheduling, and promotion timing.
    """)
    return


@app.cell
def _(con):
    hourly_orders_sql = """
    SELECT
        EXTRACT(HOUR FROM CAST(order_time AS TIME)) AS order_hour,
        COUNT(DISTINCT order_id) AS order_count
    FROM gold.fact_sales
    GROUP BY 1
    ORDER BY 1
    """
    hourly_orders = con.execute(hourly_orders_sql).fetchdf()
    hourly_orders
    return (hourly_orders,)


@app.cell
def _(hourly_orders, plt):
    plt.figure(figsize=(9, 4))
    plt.bar(hourly_orders["order_hour"], hourly_orders["order_count"])
    plt.title("Distinct Orders by Hour")
    plt.xlabel("Hour of Day")
    plt.ylabel("Orders")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 22 — Top 10 Pizzas by Revenue

    **Why are we doing this step?**
    The business wants to know which menu items generate the most money.

    **Implementation in Python + DuckDB**
    We aggregate revenue by pizza name.

    **Very nice plotting**
    Horizontal bar chart for readability.

    **Business analysis**
    This supports menu design, promotion decisions, and premium-item strategy.
    """)
    return


@app.cell
def _(con):
    top_pizzas_sql = """
    SELECT
        dp.pizza_name,
        ROUND(SUM(fs.sales_amount), 2) AS revenue
    FROM gold.fact_sales fs
    JOIN gold.dim_pizza dp
      ON fs.pizza_id = dp.pizza_id
    GROUP BY 1
    ORDER BY revenue DESC
    LIMIT 10
    """
    top_pizzas = con.execute(top_pizzas_sql).fetchdf()
    top_pizzas
    return (top_pizzas,)


@app.cell
def _(plt, top_pizzas):
    plt.figure(figsize=(10, 5))
    plt.barh(top_pizzas["pizza_name"], top_pizzas["revenue"])
    plt.title("Top 10 Pizzas by Revenue")
    plt.xlabel("Revenue")
    plt.ylabel("Pizza")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 23 — Category Mix

    **Why are we doing this step?**
    A category view summarizes demand at a higher business level.

    **Implementation in Python + DuckDB**
    We roll up revenue by pizza category.

    **Very nice plotting**
    A pie chart works nicely here because the number of categories is small.

    **Business analysis**
    This helps evaluate whether the menu is balanced or overly dependent on one category.
    """)
    return


@app.cell
def _(con):
    category_mix_sql = """
    SELECT
        category,
        ROUND(SUM(sales_amount), 2) AS revenue
    FROM gold.fact_sales
    GROUP BY 1
    ORDER BY revenue DESC
    """
    category_mix = con.execute(category_mix_sql).fetchdf()
    category_mix
    return (category_mix,)


@app.cell
def _(category_mix, plt):
    plt.figure(figsize=(6, 6))
    plt.pie(category_mix["revenue"], labels=category_mix["category"], autopct="%1.1f%%")
    plt.title("Revenue Share by Category")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 24 — New 2016 Pizza Adoption

    **Why are we doing this step?**
    You added new menu items in 2016.
    This is a perfect business question: are the new products gaining traction?

    **Implementation in Python + DuckDB**
    We isolate the new pizzas and show monthly revenue.

    **Very nice plotting**
    Multi-line chart by pizza name.

    **Business analysis**
    This directly measures product launch success.
    """)
    return


@app.cell
def _(con):
    new_product_sql = """
    SELECT
        DATE_TRUNC('month', fs.date_key) AS month_start,
        dp.pizza_name,
        ROUND(SUM(fs.sales_amount), 2) AS revenue
    FROM gold.fact_sales fs
    JOIN gold.dim_pizza dp
      ON fs.pizza_id = dp.pizza_id
    WHERE dp.pizza_type_id IN ('deep_dish', 'detroit_style', 'margherita')
    GROUP BY 1, 2
    ORDER BY 1, 2
    """
    new_product = con.execute(new_product_sql).fetchdf()
    new_product.head(20)
    return (new_product,)


@app.cell
def _(new_product, plt):
    plt.figure(figsize=(10, 5))
    for _name in new_product["pizza_name"].unique():
        temp = new_product[new_product["pizza_name"] == _name]
        plt.plot(temp["month_start"], temp["revenue"], marker="o", label=_name)

    plt.title("Monthly Revenue for New 2016 Pizza Lines")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 25 — Final Business Summary

    **Why are we doing this step?**
    A notebook should end by translating technical work into business language.

    **Implementation in Python + DuckDB**
    No new SQL is required here unless you want to add final summary queries.

    **Very nice plotting**
    No new plot required.

    **Business analysis**
    Use this markdown cell to summarize:
    - data quality improvements from Bronze to Silver
    - total revenue and order volume
    - peak hours
    - top pizzas
    - category mix
    - performance of new 2016 menu items

    This is the bridge from engineering to decision-making.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 🧠 Clean mental model

    | Layer | Key used
    |-------|---------|
    |Bronze | `raw_order_details_id` (messy) |
    |Silver | `order_details_sk` (clean)|
    |Gold   | `order_details_id` (ONLY)|
    """)
    return


@app.cell
def _():
    # 🎯 Proper way to close DuckDB in Jupyter
    #
    # ✅ 1. The correct (graceful) way
    # =========================================
    # Clean shutdown
    # =========================================

    # try:
    #    con.close()
    #    print("DuckDB connection closed.")
    # except Exception as e:
    #    print("Connection already closed or not defined.")
    return


if __name__ == "__main__":
    app.run()
