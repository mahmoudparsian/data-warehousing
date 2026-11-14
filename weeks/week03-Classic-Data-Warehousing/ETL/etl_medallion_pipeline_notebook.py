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
    # Week 4 — ETL, OLAP, Medallion (Advanced Notebook)

    ## 🔥 What You Will Learn
    This notebook is a **complete end-to-end data pipeline**:

    - Raw messy data (Bronze)
    - Cleaned data (Silver)
    - Business metrics (Gold)
    - OLAP queries
    - Visualization + business insight

    👉 Every section includes:
    - Explanation
    - SQL
    - Python
    - Business meaning
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 0 — Setup

    We use:
    - DuckDB (analytical database)
    - Pandas (inspection)
    - Matplotlib (visualization)

    👉 Why this matters:
    Modern analysts combine SQL + Python
    """)
    return


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import duckdb

    con = duckdb.connect("week04_pipeline_v2.duckdb")
    return con, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1 — Create Raw Data (Bronze Input)

    ### What we are doing
    We simulate messy real-world data:
    - inconsistent casing
    - bad values
    - mixed types

    ### Business Insight
    👉 Real data is NEVER clean
    👉 Pipelines exist because of this
    """)
    return


@app.cell
def _(pd):
    raw = pd.DataFrame({
        "order_id":[1,2,3,4,5,6],
        "region":["West ","west","EAST","East ","west","WEST"],
        "amount":["1000","2000","1500","ERROR","1800","1700"]
    })

    raw.to_csv("raw_sales.csv", index=False)
    raw
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2 — Bronze Layer

    ### What we are doing
    - Load raw data as-is
    - No cleaning

    ### Business Insight
    👉 Bronze = source of truth
    👉 Used for debugging + traceability
    """)
    return


@app.cell
def _(con, mo):
    _df = mo.sql(f"""DROP TABLE IF EXISTS bronze_sales;""", engine=con)
    _df = mo.sql(f"""CREATE OR REPLACE TABLE bronze_sales AS SELECT * FROM read_csv_auto('raw_sales.csv');""", engine=con)

    _df = mo.sql(f"""SELECT * FROM bronze_sales;""", engine=con)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 3 — Data Profiling

    ### What we are doing
    - Check nulls
    - Understand data issues

    ### Business Insight
    👉 Always profile BEFORE transforming
    👉 Prevents bad assumptions
    """)
    return


@app.cell
def _(bronze_sales, con, mo):
    res = mo.sql(f"""SELECT COUNT(*) total_rows, COUNT(amount) non_null_amount FROM bronze_sales""", engine=con)
    res
    return


@app.cell
def _(pd):
    df = pd.read_csv("raw_sales.csv")
    df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 4 — Silver Layer (Cleaning)

    ### What we are doing
    - Clean region values
    - Convert amount to numeric
    - Remove bad rows

    ### Business Insight
    👉 Silver = trusted data
    👉 This is where most logic lives
    """)
    return


@app.cell
def _(bronze_sales, con, mo):
    _df = mo.sql(f"""

    CREATE OR REPLACE TABLE silver_sales AS
    SELECT
        order_id,
        LOWER(TRIM(region)) AS region,
        TRY_CAST(amount AS DOUBLE) AS amount
    FROM bronze_sales
    WHERE TRY_CAST(amount AS DOUBLE) IS NOT NULL;

    SELECT * FROM silver_sales;
    """, engine=con)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 5 — Verify Silver (Python)

    ### What we are doing
    - Inspect cleaned dataset

    ### Business Insight
    👉 Always validate transformation
    👉 Never assume correctness
    """)
    return


@app.cell
def _(con):
    silver_df = con.execute("SELECT * FROM silver_sales").fetchdf()
    silver_df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 6 — Gold Layer (Business Metrics)

    ### What we are doing
    - Aggregate revenue by region

    ### Business Insight
    👉 Gold = decision layer
    👉 Executives care about THIS
    """)
    return


@app.cell
def _(con, mo, silver_sales):
    _df = mo.sql(f"""

    CREATE OR REPLACE TABLE gold_sales AS
    SELECT
        region,
        SUM(amount) AS total_revenue
    FROM silver_sales
    GROUP BY region;

    SELECT * FROM gold_sales;
    """, engine=con)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 7 — Visualization

    ### What we are doing
    - Plot revenue by region

    ### Business Insight
    👉 Visuals reveal patterns faster than tables
    """)
    return


@app.cell
def _(con, plt):
    gold_df = con.execute("SELECT * FROM gold_sales").fetchdf()

    plt.figure()
    plt.bar(gold_df["region"], gold_df["total_revenue"])
    plt.title("Revenue by Region")
    plt.xlabel("Region")
    plt.ylabel("Revenue")
    plt.grid(axis="y", alpha=0.3)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 8 — OLAP Query (Slice)

    ### What we are doing
    - Analyze one segment

    ### Business Insight
    👉 Slice = focused decision-making
    """)
    return


@app.cell
def _(con, mo, silver_sales):
    _df = mo.sql(f"""SELECT region, SUM(amount) FROM silver_sales GROUP BY region;""", engine=con)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 9 — Validation

    ### What we are doing
    - Check for anomalies

    ### Business Insight
    👉 Trust but verify
    """)
    return


@app.cell
def _(con, mo, silver_sales):
    _df = mo.sql(f"""SELECT * FROM silver_sales WHERE amount < 0;""", engine=con)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🎯 Final Summary

    - Bronze = raw data
    - Silver = cleaned data
    - Gold = business metrics
    - OLAP = insights

    👉 This is how real data systems work
    """)
    return


if __name__ == "__main__":
    app.run()
