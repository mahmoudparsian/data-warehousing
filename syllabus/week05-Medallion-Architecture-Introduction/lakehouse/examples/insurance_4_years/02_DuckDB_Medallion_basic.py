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
    # Insurance Lakehouse with DuckDB
    Bronze → Silver → Gold architecture example.
    """)
    return


@app.cell
def _():
    import duckdb
    from pathlib import Path

    BASE_DIR = Path(".")
    BRONZE_DIR = BASE_DIR / "insurance" / "data" / "bronze"
    print("BRONZE_DIR", BRONZE_DIR)
    return (duckdb,)


@app.cell
def _(duckdb):
    con = duckdb.connect("insurance_lakehouse.duckdb")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Bronze Layer
    """)
    return


@app.cell
def _(con):
    con.execute("""

    CREATE OR REPLACE VIEW bronze_insurance AS
    SELECT
        *,
        CAST(split_part(filename, '.', 2) AS INTEGER) AS year
    FROM read_csv_auto(
        'data/bronze/insurance.*.csv',
        header = true,
        filename = true
    );
    """).fetchall()

    con.execute("SELECT year, COUNT(*) as rows FROM bronze_insurance GROUP BY year ORDER BY year").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Silver Layer
    """)
    return


@app.cell
def _(con):
    con.execute("""

    CREATE OR REPLACE TABLE silver_insurance AS
    SELECT
        age::INTEGER AS age,
        gender,
        bmi::DOUBLE AS bmi,
        children::INTEGER AS children,
        region,
        charges::DOUBLE AS charges,
        year::INTEGER AS year
    FROM bronze_insurance
    """).fetchall()

    con.execute("SELECT year, COUNT(*) FROM silver_insurance GROUP BY year ORDER BY year").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Gold Layer
    """)
    return


@app.cell
def _(con):
    con.execute("""

    CREATE OR REPLACE VIEW gold_kpi_year AS
    SELECT
        year,
        COUNT(*) members,
        AVG(charges) avg_charges,
        SUM(charges) total_charges
    FROM silver_insurance
    GROUP BY year
    ORDER BY year
    """).fetchall()

    con.execute("SELECT * FROM gold_kpi_year").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Example Insights
    """)
    return


@app.cell
def _(con):
    con.execute("""SELECT year, AVG(charges) avg_charges FROM silver_insurance GROUP BY year ORDER BY year""").df()
    return


@app.cell
def _(con):
    con.execute("""SELECT region, AVG(charges) avg_charges FROM silver_insurance GROUP BY region""").df()
    return


@app.cell
def _(con):
    con.execute("""SELECT smoker, AVG(charges) avg_charges FROM bronze_insurance GROUP BY smoker""").df()
    return


@app.cell
def _(con):
    con.execute("""SELECT age, charges FROM silver_insurance ORDER BY charges DESC LIMIT 10""").df()
    return


if __name__ == "__main__":
    app.run()
