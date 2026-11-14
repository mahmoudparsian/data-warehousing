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
    # Week 2 — Analytical Thinking + Window Functions (Advanced Notebook)
    ## Overview
    - This notebook demonstrates how analysts think using SQL
    - We combine row-level + aggregated insights using window functions
    - Each section includes: explanation → SQL → business insight → visualization
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup: Connect to DuckDB
    - We use DuckDB as analytical engine
    - JupySQL allows SQL inside notebook
    - This creates a local analytical environment
    """)
    return


@app.cell
def _():
    import duckdb as _duckdb
    _duckdb.execute("ATTACH IF NOT EXISTS 'week02_advanced.duckdb' AS week02_advanced; USE week02_advanced").fetchall()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Load Data
    - Load insurance dataset into DuckDB
    - This becomes our analytical table
    - We will query this table throughout
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql("""
    CREATE OR REPLACE TABLE insurance AS SELECT * FROM read_csv_auto('../week01-Foundations-SQL-for-Analytics/example_1_insurance/insurance.csv');
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Preview Data
    - Understand structure of dataset
    - Identify key variables
    - This is exploration, not analysis
    """)
    return


@app.cell
def _(insurance, mo):
    _res = mo.sql(f"""SELECT * FROM insurance LIMIT 5""")
    _df = _res
    _df
    return


@app.cell
def _():
    import matplotlib.pyplot as plt

    return (plt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Top-N per Region (Window Function)
    - Business Question: Who are top customers per region?
    - Use ROW_NUMBER with PARTITION
    - Keeps row-level detail while ranking
    """)
    return


@app.cell
def _(insurance, mo):
    res = mo.sql(f"""
    SELECT *
    FROM (
        SELECT *, 
               ROW_NUMBER() OVER (PARTITION BY region ORDER BY charges DESC) AS rn
        FROM insurance
    ) t
    WHERE rn <= 3
    """)
    return (res,)


@app.cell
def _(res):
    df = res
    df
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    - Identifies VIP customers in each region
    - Enables targeted marketing or pricing
    - Helps allocate resources effectively
    """)
    return


@app.cell
def _(df, plt):
    df_group = df.groupby("region")["charges"].mean()

    plt.figure()
    df_group.plot(kind="bar")
    plt.title("Top Customers Avg Charges by Region")
    plt.xlabel("Region")
    plt.ylabel("Charges")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Compare Customers to Regional Average
    - Add context to each row
    - Compare individual vs group
    - This is key analytical thinking
    """)
    return


@app.cell
def _(insurance, mo):
    res_2 = mo.sql(f"""
    SELECT *, 
           AVG(charges) OVER (PARTITION BY region) AS regional_avg
    FROM insurance
    """)
    return (res_2,)


@app.cell
def _(res_2):
    df_2 = res_2
    df_2.head()
    return (df_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    - Shows whether customer is above or below norm
    - Helps identify outliers
    - Useful for pricing strategies
    """)
    return


@app.cell
def _(df_2, plt):
    diff = df_2.groupby("region")["regional_avg"].mean()

    plt.figure()
    diff.plot(kind="bar")
    plt.title("Regional Average Charges")
    plt.xlabel("Region")
    plt.ylabel("Avg Charges")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Customers Above Regional Average
    - Identify high-value customers
    - Filter using window result
    - Common real-world pattern
    """)
    return


@app.cell
def _(insurance, mo):
    res_3 = mo.sql(f"""
    SELECT *
    FROM (
        SELECT *, AVG(charges) OVER (PARTITION BY region) AS regional_avg
        FROM insurance
    ) t
    WHERE charges > regional_avg
    """)
    return (res_3,)


@app.cell
def _(res_3):
    df_3 = res_3
    df_3.head()
    return (df_3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    - Focus on customers generating more revenue
    - Helps segmentation
    - Supports retention strategies
    """)
    return


@app.cell
def _(df_3, plt):
    count = df_3.groupby("region").size()

    plt.figure()
    count.plot(kind="bar")
    plt.title("Above Avg Customers by Region")
    plt.xlabel("Region")
    plt.ylabel("Count")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Contribution to Total Revenue
    - Measure importance of each customer
    - Use SUM window function
    - Enables Pareto analysis
    """)
    return


@app.cell
def _(insurance, mo):
    res_4 = mo.sql(f"""
    SELECT *, charges / SUM(charges) OVER () AS pct_total
    FROM insurance
    """)
    return (res_4,)


@app.cell
def _(res_4):
    df_4 = res_4
    df_4.head()
    return (df_4,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    - Identify customers driving most revenue
    - Supports prioritization
    - Helps focus on high-impact users
    """)
    return


@app.cell
def _(df_4, plt):
    top = df_4.sort_values("pct_total", ascending=False).head(10)

    plt.figure()
    plt.bar(range(len(top)), top["pct_total"])
    plt.title("Top Revenue Contributors")
    plt.xlabel("Top Customers")
    plt.ylabel("Contribution")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Running Total
    - Shows accumulation of values
    - Useful for trends
    - Demonstrates progression
    """)
    return


@app.cell
def _(insurance, mo):
    res_5 = mo.sql(f"""
    SELECT age, charges,
           SUM(charges) OVER (ORDER BY age) AS running_total
    FROM insurance
    """)
    return (res_5,)


@app.cell
def _(res_5):
    df_5 = res_5
    df_5.head()
    return (df_5,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    - Helps understand cumulative trends
    - Useful for forecasting
    - Shows how values build up
    """)
    return


@app.cell
def _(df_5, plt):
    plt.figure()
    plt.plot(df_5["age"], df_5["running_total"])
    plt.title("Running Total by Age")
    plt.xlabel("Age")
    plt.ylabel("Running Total")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. LAG / LEAD (Comparison)
    - Compare neighboring rows
    - Detect changes
    - Used in time-series
    """)
    return


@app.cell
def _(insurance, mo):
    res_6 = mo.sql(f"""
    SELECT age, charges,
           LAG(charges) OVER (ORDER BY age) AS prev,
           LEAD(charges) OVER (ORDER BY age) AS next
    FROM insurance
    """)
    return (res_6,)


@app.cell
def _(res_6):
    df_6 = res_6
    df_6.head()
    return (df_6,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    - Detect changes between observations
    - Useful for anomaly detection
    - Supports trend analysis
    """)
    return


@app.cell
def _(df_6, plt):
    plt.figure()
    plt.plot(df_6["age"], df_6["charges"])
    plt.title("Charges by Age")
    plt.xlabel("Age")
    plt.ylabel("Charges")
    plt.show()
    return


if __name__ == "__main__":
    app.run()
