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
    # Vehicles.csv — Exploratory Data Analysis (DuckDB-first)

    Dataset: **Craigslist Cars & Trucks (USA)**
    File: `vehicles.csv` (~426,881 rows; wide schema; heavy text columns like `description`)

    **Design principle:** Use DuckDB for scanning and aggregation. Only pull small aggregated result sets into pandas for charts.

    ![ETL Diagram](vehicles_lakehouse_etl_diagram.png)

    ---

    ## What you will do

    1) Load `vehicles.csv` into a **Bronze view** (raw)
    2) Inspect schema + missingness + basic distributions
    3) Validate key columns (price, year, odometer, posting_date)
    4) Produce EDA charts from aggregated queries
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import matplotlib.pyplot as plt
    from pathlib import Path

    DATA_PATH = Path("vehicles.csv")   # Put vehicles.csv in the same folder as this notebook (or change this path)
    DB_PATH = Path("vehicles_eda.duckdb")

    con = duckdb.connect(str(DB_PATH))
    print("DuckDB:", duckdb.__version__)
    print("Data path:", DATA_PATH.resolve())
    return con, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1) Bronze view: read_csv_auto (raw)
    """)
    return


@app.cell
def _(con):
    con.execute("""

    CREATE OR REPLACE VIEW bronze_vehicles AS
    SELECT *
    FROM read_csv_auto(
      'vehicles.csv',
      header=true,
      sample_size=50000,
      ignore_errors=true
    );
    """).fetchall()

    con.execute("SELECT COUNT(*) AS rows FROM bronze_vehicles;").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2) Schema discovery
    """)
    return


@app.cell
def _(con):
    con.execute("DESCRIBE bronze_vehicles").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3) Column completeness (missingness)
    """)
    return


@app.cell
def _(con):
    cols = [
      'price','year','manufacturer','model','condition','cylinders','fuel',
      'odometer','title_status','transmission','drive','size','type','paint_color',
      'state','lat','long','posting_date'
    ]

    missing_sql = "SELECT\n" + ",\n".join([
        f"  SUM(CASE WHEN {c} IS NULL OR CAST({c} AS VARCHAR)='' THEN 1 ELSE 0 END) AS missing_{c}"
        for c in cols
    ]) + "\nFROM bronze_vehicles;"

    miss = con.execute(missing_sql).df().T.reset_index()
    miss.columns = ["metric","missing_count"]
    miss["column"] = miss["metric"].str.replace("missing_","", regex=False)
    miss = miss[["column","missing_count"]].sort_values("missing_count", ascending=False)
    miss
    return (miss,)


@app.cell
def _(miss, plt):
    top = miss.head(12)
    plt.figure(figsize=(10,4))
    plt.bar(top["column"], top["missing_count"])
    plt.xticks(rotation=45, ha="right")
    plt.title("Missing values (top 12 columns)")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4) Price distribution (robust bins)
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT price
    FROM bronze_vehicles
    WHERE price IS NOT NULL AND price BETWEEN 500 AND 200000
    """).df()

    plt.figure(figsize=(9,4))
    plt.hist(_df["price"], bins=60)
    plt.title("Price distribution (filtered to $500–$200k for visualization)")
    plt.xlabel("price"); plt.ylabel("count")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5) Posting date coverage
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
    SELECT
      posting_date::DATE AS post_date
    FROM bronze_vehicles
    WHERE posting_date IS NOT NULL
    """).df()

    _df["post_date"].describe()
    return


@app.cell
def _(con, plt):
    dfm = con.execute("""
    WITH d AS (
      SELECT posting_date::DATE AS post_date
      FROM bronze_vehicles
      WHERE posting_date IS NOT NULL
    )
    SELECT
      date_trunc('month', post_date) AS month,
      COUNT(*) AS listings
    FROM d
    GROUP BY 1
    ORDER BY 1;
    """).df()

    plt.figure(figsize=(10,4))
    plt.plot(dfm["month"], dfm["listings"])
    plt.title("Listings over time (monthly)")
    plt.xlabel("month")
    plt.ylabel("listings")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6) Top states by listing count
    """)
    return


@app.cell
def _(con):
    dft = con.execute("""
    SELECT state, COUNT(*) AS listings
    FROM bronze_vehicles
    WHERE state IS NOT NULL AND state != ''
    GROUP BY state
    ORDER BY listings DESC
    LIMIT 20;
    """).df()

    dft
    return (dft,)


@app.cell
def _(dft, plt):
    plt.figure(figsize=(10,4))
    plt.bar(dft["state"], dft["listings"])
    plt.title("Top 20 states by listing count")
    plt.xlabel("state"); plt.ylabel("listings")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7) Manufacturers: coverage + typical prices
    """)
    return


@app.cell
def _(con):
    dfmfg = con.execute("""
    SELECT
      lower(trim(manufacturer)) AS manufacturer,
      COUNT(*) AS listings,
      median(price) AS median_price
    FROM bronze_vehicles
    WHERE manufacturer IS NOT NULL AND manufacturer != ''
      AND price IS NOT NULL AND price BETWEEN 500 AND 200000
    GROUP BY 1
    HAVING COUNT(*) >= 1000
    ORDER BY listings DESC
    LIMIT 20;
    """).df()

    dfmfg
    return (dfmfg,)


@app.cell
def _(dfmfg, plt):
    plt.figure(figsize=(10,4))
    plt.bar(dfmfg["manufacturer"], dfmfg["median_price"])
    plt.xticks(rotation=45, ha="right")
    plt.title("Median price by manufacturer (top 20 by listings; min 1000 listings)")
    plt.xlabel("manufacturer"); plt.ylabel("median price")
    plt.tight_layout()
    plt.show()
    return


if __name__ == "__main__":
    app.run()
