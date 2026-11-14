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
    # Craigslist Vehicles Lakehouse (DuckDB)
    ## Bronze → Silver → Gold + 10 Insight Queries (with charts)

    This notebook builds a teaching-grade **Lakehouse** over `vehicles.csv` using DuckDB only (**no Parquet**).

    ![ETL Diagram](vehicles_lakehouse_etl_diagram.png)
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import matplotlib.pyplot as plt
    from pathlib import Path

    DATA_PATH = Path("vehicles.csv")
    DB_PATH = Path("vehicles_lakehouse.duckdb")

    con = duckdb.connect(str(DB_PATH))
    print("DuckDB:", duckdb.__version__)
    return con, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1) Bronze: raw view
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
    return


@app.cell
def _(con):
    con.execute("SELECT COUNT(*) AS row_count FROM bronze_vehicles;").df()
    return


@app.cell
def _(con):
    con.execute("SELECT * FROM bronze_vehicles limit 4;").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2) Silver: cleaned and standardized table
    """)
    return


@app.cell
def _(con):
    con.execute("""

    CREATE OR REPLACE TABLE silver_vehicles AS
    WITH base AS (
      SELECT
        id,
        url,
        region,
        region_url,
        TRY_CAST(price AS BIGINT) AS price,
        TRY_CAST(year AS INTEGER) AS vehicle_year,
        lower(trim(CAST(manufacturer AS VARCHAR))) AS manufacturer,
        lower(trim(CAST(model AS VARCHAR))) AS model,
        lower(trim(CAST(condition AS VARCHAR))) AS condition,
        lower(trim(CAST(cylinders AS VARCHAR))) AS cylinders,
        lower(trim(CAST(fuel AS VARCHAR))) AS fuel,
        TRY_CAST(odometer AS BIGINT) AS odometer,
        lower(trim(CAST(title_status AS VARCHAR))) AS title_status,
        lower(trim(CAST(transmission AS VARCHAR))) AS transmission,
        CAST(VIN AS VARCHAR) AS vin,
        lower(trim(CAST(drive AS VARCHAR))) AS drive,
        lower(trim(CAST(size AS VARCHAR))) AS size,
        lower(trim(CAST(type AS VARCHAR))) AS type,
        lower(trim(CAST(paint_color AS VARCHAR))) AS paint_color,
        image_url,
        description,
        county,
        lower(trim(CAST(state AS VARCHAR))) AS state,
        TRY_CAST(lat AS DOUBLE) AS lat,
        TRY_CAST(long AS DOUBLE) AS lon,

        -- IMPORTANT FIX
        posting_date AS posting_ts

      FROM bronze_vehicles
    ),
    enriched AS (
      SELECT
        *,
        posting_ts::DATE AS posting_date,
        EXTRACT(year FROM posting_ts) AS posting_year,
        EXTRACT(month FROM posting_ts) AS posting_month,

        CASE
          WHEN vehicle_year IS NULL OR posting_ts IS NULL THEN NULL
          ELSE EXTRACT(year FROM posting_ts) - vehicle_year
        END AS vehicle_age,

        CASE
          WHEN odometer IS NULL OR odometer = 0 OR price IS NULL THEN NULL
          ELSE price::DOUBLE / odometer::DOUBLE
        END AS price_per_mile

      FROM base
    )

    SELECT *
    FROM enriched
    WHERE
      price BETWEEN 500 AND 200000
      AND (vehicle_year BETWEEN 1950 AND EXTRACT(year FROM CURRENT_DATE) OR vehicle_year IS NULL)
      AND (odometer BETWEEN 0 AND 500000 OR odometer IS NULL);
    """).fetchall()
    return


@app.cell
def _(con):
    con.execute("SELECT COUNT(*) AS row_count FROM silver_vehicles;").df()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
      COUNT(*) AS total_rows,
      COUNT(posting_date) AS non_null_posting_date
    FROM silver_vehicles
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3) Gold: curated KPI view
    """)
    return


@app.cell
def _(con):
    con.execute("""

    CREATE OR REPLACE VIEW gold_kpi_month AS
    SELECT
      date_trunc('month', posting_date) AS month,
      COUNT(*) AS listings,
      MEDIAN(price) AS median_price,
      QUANTILE_CONT(price, 0.90) AS p90_price,
      AVG(price) AS avg_price
    FROM silver_vehicles
    WHERE posting_date IS NOT NULL
    GROUP BY 1
    ORDER BY 1;
    """).fetchall()
    return


@app.cell
def _(con):
    con.execute("SELECT COUNT(*) AS row_count FROM gold_kpi_month;").df()
    return


@app.cell
def _(con):
    con.execute("SELECT * FROM gold_kpi_month LIMIT 12;").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4) Chart helpers
    """)
    return


@app.cell
def _(plt):
    def plot_line_time(df, x, y, title):
        plt.figure(figsize=(10,4))
        plt.plot(df[x], df[y])
        plt.title(title)
        plt.xlabel(x); plt.ylabel(y)
        plt.tight_layout(); plt.show()

    def plot_line_num(df, x, y, title):
        plt.figure(figsize=(9,4))
        plt.plot(df[x], df[y])
        plt.title(title)
        plt.xlabel(x); plt.ylabel(y)
        plt.tight_layout(); plt.show()

    def plot_bar_cat(df, x, y, title, rotate=45):
        plt.figure(figsize=(10,4))
        plt.bar(df[x].astype(str), df[y])
        plt.title(title)
        plt.xlabel(x); plt.ylabel(y)
        plt.xticks(rotation=rotate, ha='right')
        plt.tight_layout(); plt.show()

    return plot_bar_cat, plot_line_num, plot_line_time


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5) 10 Insight Queries (English → SQL → Chart)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Insight 1 — Listings volume over time (monthly)

    ```sql
    SELECT month, listings FROM gold_kpi_month ORDER BY month;
    ```
    """)
    return


@app.cell
def _(con):
    df = con.execute(r"""SELECT month, listings FROM gold_kpi_month ORDER BY month;""").df()
    df
    return (df,)


@app.cell
def _(df, plot_line_time):
    plot_line_time(df, 'month', 'listings', 'Insight 1 — Listings volume over time (monthly)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Insight 2 — Median price trend over time (monthly)

    ```sql
    SELECT month, median_price FROM gold_kpi_month ORDER BY month;
    ```
    """)
    return


@app.cell
def _(con):
    df_2 = con.execute(r"""SELECT month, median_price FROM gold_kpi_month ORDER BY month;""").df()
    df_2
    return (df_2,)


@app.cell
def _(df_2, plot_line_time):
    plot_line_time(df_2, 'month', 'median_price', 'Insight 2 — Median price trend over time (monthly)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Insight 3 — Top 15 manufacturers by listings

    ```sql
    SELECT manufacturer, COUNT(*) AS listings
    FROM silver_vehicles
    WHERE manufacturer IS NOT NULL AND manufacturer != ''
    GROUP BY 1
    ORDER BY listings DESC
    LIMIT 15;
    ```
    """)
    return


@app.cell
def _(con):
    df_3 = con.execute(r"""
    SELECT
        manufacturer,
        COUNT(*) AS listings
    FROM silver_vehicles
    WHERE manufacturer IS NOT NULL AND manufacturer != ''
    GROUP BY manufacturer
    ORDER BY listings DESC
    LIMIT 15;
    """).df()
    df_3
    return (df_3,)


@app.cell
def _(df_3, plot_bar_cat):
    plot_bar_cat(df_3, 'manufacturer', 'listings', 'Insight 3 — Top 15 manufacturers by listings')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Insight 4 — Median price by manufacturer (top 15 by listings)

    ```sql
    WITH m AS (
      SELECT manufacturer, COUNT(*) AS listings
      FROM silver_vehicles
      WHERE manufacturer IS NOT NULL AND manufacturer != ''
      GROUP BY 1
      ORDER BY listings DESC
      LIMIT 15
    )
    SELECT s.manufacturer, MEDIAN(s.price) AS median_price
    FROM silver_vehicles s
    JOIN m USING(manufacturer)
    GROUP BY 1
    ORDER BY median_price DESC;
    ```
    """)
    return


@app.cell
def _(con):
    df_4 = con.execute(r"""
    WITH m AS (
      SELECT manufacturer, COUNT(*) AS listings
      FROM silver_vehicles
      WHERE manufacturer IS NOT NULL AND manufacturer != ''
      GROUP BY 1
      ORDER BY listings DESC
      LIMIT 15
    )
    SELECT s.manufacturer, MEDIAN(s.price) AS median_price
    FROM silver_vehicles s
    JOIN m USING(manufacturer)
    GROUP BY 1
    ORDER BY median_price DESC;
    """).df()
    df_4
    return (df_4,)


@app.cell
def _(df_4, plot_bar_cat):
    plot_bar_cat(df_4, 'manufacturer', 'median_price', 'Insight 4 — Median price by manufacturer (top 15 by listings)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Insight 5 — Median price by vehicle age (0–30)

    ```sql
    SELECT vehicle_age, MEDIAN(price) AS median_price, COUNT(*) AS listings
    FROM silver_vehicles
    WHERE vehicle_age BETWEEN 0 AND 30
    GROUP BY 1
    HAVING COUNT(*) >= 500
    ORDER BY 1;
    ```
    """)
    return


@app.cell
def _(con):
    df_5 = con.execute(r"""SELECT vehicle_age, MEDIAN(price) AS median_price, COUNT(*) AS listings
    FROM silver_vehicles
    WHERE vehicle_age BETWEEN 0 AND 30
    GROUP BY 1
    HAVING COUNT(*) >= 500
    ORDER BY 1;""").df()
    df_5
    return (df_5,)


@app.cell
def _(df_5, plot_line_num):
    plot_line_num(df_5, 'vehicle_age', 'median_price', 'Insight 5 — Median price by vehicle age (0–30)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Insight 6 — Median price by odometer bin

    ```sql
    WITH b AS (
      SELECT
        CASE
          WHEN odometer < 25000 THEN '0-25k'
          WHEN odometer < 50000 THEN '25k-50k'
          WHEN odometer < 100000 THEN '50k-100k'
          WHEN odometer < 150000 THEN '100k-150k'
          WHEN odometer < 200000 THEN '150k-200k'
          ELSE '200k+'
        END AS odo_bin,
        price
      FROM silver_vehicles
      WHERE odometer IS NOT NULL AND price IS NOT NULL
    )
    SELECT odo_bin, MEDIAN(price) AS median_price, COUNT(*) AS listings
    FROM b
    GROUP BY 1
    ORDER BY listings DESC;
    ```
    """)
    return


@app.cell
def _(con):
    df_6 = con.execute(r"""WITH b AS (
      SELECT
        CASE
          WHEN odometer < 25000 THEN '0-25k'
          WHEN odometer < 50000 THEN '25k-50k'
          WHEN odometer < 100000 THEN '50k-100k'
          WHEN odometer < 150000 THEN '100k-150k'
          WHEN odometer < 200000 THEN '150k-200k'
          ELSE '200k+'
        END AS odo_bin,
        price
      FROM silver_vehicles
      WHERE odometer IS NOT NULL AND price IS NOT NULL
    )
    SELECT odo_bin, MEDIAN(price) AS median_price, COUNT(*) AS listings
    FROM b
    GROUP BY 1
    ORDER BY listings DESC;""").df()
    df_6
    return (df_6,)


@app.cell
def _(df_6, plot_bar_cat):
    plot_bar_cat(df_6, 'odo_bin', 'median_price', 'Insight 6 — Median price by odometer bin')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Insight 7 — Fuel type distribution

    ```sql
    SELECT fuel, COUNT(*) AS listings
    FROM silver_vehicles
    WHERE fuel IS NOT NULL AND fuel != ''
    GROUP BY 1
    ORDER BY listings DESC;
    ```
    """)
    return


@app.cell
def _(con):
    df_7 = con.execute(r"""
    SELECT fuel, COUNT(*) AS listings
    FROM silver_vehicles
    WHERE fuel IS NOT NULL AND fuel != ''
    GROUP BY 1
    ORDER BY listings DESC;
    """).df()
    df_7
    return (df_7,)


@app.cell
def _(df_7, plot_bar_cat):
    plot_bar_cat(df_7, 'fuel', 'listings', 'Insight 7 — Fuel type distribution')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Insight 8 — Transmission: listings and median price

    ```sql
    SELECT transmission, COUNT(*) AS listings, MEDIAN(price) AS median_price
    FROM silver_vehicles
    WHERE transmission IS NOT NULL AND transmission != ''
    GROUP BY 1
    ORDER BY listings DESC;
    ```
    """)
    return


@app.cell
def _(con):
    df_8 = con.execute(r"""
    SELECT transmission, COUNT(*) AS listings, MEDIAN(price) AS median_price
    FROM silver_vehicles
    WHERE transmission IS NOT NULL AND transmission != ''
    GROUP BY 1
    ORDER BY listings DESC;
    """).df()
    df_8
    return (df_8,)


@app.cell
def _(df_8, plot_bar_cat):
    plot_bar_cat(df_8, 'transmission', 'median_price', 'Insight 8 — Transmission: listings and median price')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Insight 9 — Top states by median price (min 3000 listings)

    ```sql
    SELECT state, COUNT(*) AS listings, MEDIAN(price) AS median_price
    FROM silver_vehicles
    WHERE state IS NOT NULL AND state != ''
    GROUP BY 1
    HAVING COUNT(*) >= 3000
    ORDER BY median_price DESC
    LIMIT 15;
    ```
    """)
    return


@app.cell
def _(con):
    df_9 = con.execute(r"""
    SELECT state, COUNT(*) AS listings, MEDIAN(price) AS median_price
    FROM silver_vehicles
    WHERE state IS NOT NULL AND state != ''
    GROUP BY 1
    HAVING COUNT(*) >= 3000
    ORDER BY median_price DESC
    LIMIT 15;
    """).df()
    df_9
    return (df_9,)


@app.cell
def _(df_9, plot_bar_cat):
    plot_bar_cat(df_9, 'state', 'median_price', 'Insight 9 — Top states by median price (min 3000 listings)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Insight 10 — Outliers: top 20 by price

    ```sql
    SELECT posting_date, state, manufacturer, model, vehicle_year, odometer, price
    FROM silver_vehicles
    ORDER BY price DESC
    LIMIT 20;
    ```
    """)
    return


@app.cell
def _(con):
    _df = con.execute(r"""SELECT posting_date, state, manufacturer, model, vehicle_year, odometer, price
    FROM silver_vehicles
    ORDER BY price DESC
    LIMIT 20;""").df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    _Table output only (no chart for this one)._
    """)
    return


if __name__ == "__main__":
    app.run()
