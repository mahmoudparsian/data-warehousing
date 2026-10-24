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
    # Week 1 — EDA + SQL (Storytelling Approach)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1 — Load Data
    """)
    return


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import duckdb

    df = pd.read_csv('../example_1_insurance/insurance.csv')
    df.head()
    return df, duckdb, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2 — Understand Structure
    """)
    return


@app.cell
def _(df):
    df.describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 3 — Distribution of Charges
    """)
    return


@app.cell
def _(df, plt):
    df['charges'].hist()
    plt.title('Distribution of Charges')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Observation: Distribution is right-skewed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 4 — Outliers
    """)
    return


@app.cell
def _(df, plt):
    df.boxplot(column='charges')
    plt.title('Charges Boxplot')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 5 — Smoker vs Non-Smoker
    """)
    return


@app.cell
def _(df, plt):
    df.groupby('smoker')['charges'].mean().plot(kind='bar')
    plt.title('Avg Charges by Smoker')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Insight: Smokers have significantly higher costs.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 6 — SQL with DuckDB
    """)
    return


@app.cell
def _(df, duckdb):
    con = duckdb.connect()
    con.register('insurance', df)

    con.execute("""
    SELECT smoker, AVG(charges)
    FROM insurance
    GROUP BY smoker
    """).df()
    return


if __name__ == "__main__":
    app.run()
