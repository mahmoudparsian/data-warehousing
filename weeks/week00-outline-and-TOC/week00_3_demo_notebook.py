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
    # Week 0 — Live Demo Notebook

    Simple DuckDB demo: raw → insight
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Create Raw Data
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql("""
    CREATE OR REPLACE TABLE sales AS
    SELECT * FROM (
        SELECT 'West' AS region, 1000 AS amount
        UNION ALL
        SELECT 'west', 2000
        UNION ALL
        SELECT 'East', 1500
        UNION ALL
        SELECT 'East', NULL
    );
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Run Simple Query (Potentially Wrong)
    """)
    return


@app.cell
def _(mo, sales):
    _df = mo.sql("""
    SELECT region, SUM(amount) FROM sales GROUP BY region;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Clean Data (Fix Case + Nulls)
    """)
    return


@app.cell
def _(mo, sales):
    _df = mo.sql("""
    SELECT LOWER(region) AS region, SUM(amount)
    FROM sales
    WHERE amount IS NOT NULL
    GROUP BY LOWER(region);
    """)
    return


if __name__ == "__main__":
    app.run()
