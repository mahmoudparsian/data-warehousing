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
    # Week 2 — Analytical Thinking + Window Functions
    """)
    return


@app.cell
def _():
    import duckdb as _duckdb
    _duckdb.execute("ATTACH IF NOT EXISTS 'week02.duckdb' AS week02; USE week02").fetchall()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Load Data
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
    ## 1) Top-N per Region (ROW_NUMBER)
    """)
    return


@app.cell
def _():
    # TODO: write query for top 3 per region
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Solution
    """)
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql("""
    SELECT *
    FROM (
      SELECT *, ROW_NUMBER() OVER (PARTITION BY region ORDER BY charges DESC) AS rn
      FROM insurance
    ) t
    WHERE rn <= 3;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2) Compare to Regional Average
    """)
    return


@app.cell
def _():
    # TODO
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Solution
    """)
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql("""
    SELECT *, AVG(charges) OVER (PARTITION BY region) AS regional_avg
    FROM insurance;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3) Above-Average Customers
    """)
    return


@app.cell
def _():
    # TODO
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Solution
    """)
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql("""
    SELECT *
    FROM (
      SELECT *, AVG(charges) OVER (PARTITION BY region) AS regional_avg
      FROM insurance
    ) t
    WHERE charges > regional_avg;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4) % of Total Contribution
    """)
    return


@app.cell
def _():
    # TODO
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Solution
    """)
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql("""
    SELECT *, charges / SUM(charges) OVER () AS pct_total
    FROM insurance;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5) Running Total by Age
    """)
    return


@app.cell
def _():
    # TODO
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Solution
    """)
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql("""
    SELECT age, charges,
           SUM(charges) OVER (ORDER BY age) AS running_total
    FROM insurance;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6) LAG / LEAD Comparison
    """)
    return


@app.cell
def _():
    # TODO
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Solution
    """)
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql("""
    SELECT age, charges,
           LAG(charges) OVER (ORDER BY age) AS prev,
           LEAD(charges) OVER (ORDER BY age) AS next
    FROM insurance;
    """)
    return


if __name__ == "__main__":
    app.run()
