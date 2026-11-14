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
    # Insurance Mini Lakehouse (DuckDB) — Reference Notebook

    Covers:
    - DuckDB metadata inspection for `insurance.csv`
    - Bronze view over `insurance.<year>.csv` files with injected year
    - Silver table (typed + derived columns)
    - Gold KPI view

    Assumes:
    - insurance.csv exists
    - data/bronze/insurance.2021.csv ... insurance.2024.csv exist
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import matplotlib.pyplot as plt

    con = duckdb.connect("insurance_lakehouse.duckdb")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1) Metadata from insurance.csv
    """)
    return


@app.cell
def _(con):
    con.execute("""

    CREATE OR REPLACE VIEW insurance_raw AS
    SELECT * FROM read_csv_auto('../../../../week01-Foundations-SQL-for-Analytics/example_1_insurance/insurance.csv', header=true);
    """).fetchall()

    con.execute("DESCRIBE insurance_raw").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2) Bronze view across yearly files + year from filename
    """)
    return


@app.cell
def _(con):
    con.execute("""

    CREATE OR REPLACE VIEW bronze_insurance AS
    SELECT
      *,
      CAST(split_part(filename, '.', 2) AS INTEGER) AS year
    FROM read_csv_auto('data/bronze/insurance.*.csv', header=true, filename=true);
    """).fetchall()

    con.execute("SELECT year, COUNT(*) AS rows FROM bronze_insurance GROUP BY year ORDER BY year;").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3) Silver table
    """)
    return


@app.cell
def _(con):
    con.execute("""

    CREATE OR REPLACE TABLE silver_insurance AS
    SELECT
      CAST(age AS INTEGER) AS age,
      lower(trim(CAST(gender AS VARCHAR))) AS gender,
      CAST(bmi AS DOUBLE) AS bmi,
      CAST(children AS INTEGER) AS children,
      lower(trim(CAST(smoker AS VARCHAR))) AS smoker,
      lower(trim(CAST(region AS VARCHAR))) AS region,
      CAST(charges AS DOUBLE) AS charges,
      CAST(year AS INTEGER) AS year,
      CASE
        WHEN bmi < 18.5 THEN 'underweight'
        WHEN bmi < 25 THEN 'normal'
        WHEN bmi < 30 THEN 'overweight'
        ELSE 'obese'
      END AS bmi_class
    FROM bronze_insurance;
    """).fetchall()

    con.execute("SELECT year, COUNT(*) AS rows FROM silver_insurance GROUP BY year ORDER BY year;").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4) Gold KPI view
    """)
    return


@app.cell
def _(con):
    con.execute("""

    CREATE OR REPLACE VIEW gold_kpi_year AS
    SELECT
      year,
      COUNT(*) AS members,
      AVG(charges) AS avg_charges,
      MEDIAN(charges) AS median_charges,
      QUANTILE_CONT(charges, 0.90) AS p90_charges,
      SUM(charges) AS total_charges
    FROM silver_insurance
    GROUP BY year
    ORDER BY year;
    """).fetchall()

    con.execute("SELECT * FROM gold_kpi_year").df()
    return


if __name__ == "__main__":
    app.run()
