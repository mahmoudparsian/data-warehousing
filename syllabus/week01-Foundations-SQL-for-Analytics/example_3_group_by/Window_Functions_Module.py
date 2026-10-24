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
    # 🪟 Window Functions — SQL + Insight + Plot
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import matplotlib.pyplot as plt

    con = duckdb.connect()

    INPUT_PATH = "."
    file_path = f"{INPUT_PATH}/sales.csv"

    con.execute("""
    CREATE OR REPLACE TABLE sales AS
    SELECT * FROM read_csv_auto(?);
    """, [file_path]).fetchall()
    return con, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Revenue by Product — SQL
    """)
    return


@app.cell
def _(con, pd):
    pd.set_option('display.float_format', '{:,.2f}'.format)

    df = con.execute("""SELECT product_name, SUM(sales_amount) AS revenue FROM sales GROUP BY product_name ORDER BY revenue DESC""").df()
    df.head(20)
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Business Insight
    """)
    return


@app.cell
def _():
    print("""- Identify top products
    - Revenue concentration
    - Portfolio strategy""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Plot
    """)
    return


@app.cell
def _(df, plt):
    plt.figure(); plt.bar(df['product_name'], df['revenue']); plt.xticks(rotation=45); plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Top 3 Products per Country — SQL
    """)
    return


@app.cell
def _(con):
    df_2 = con.execute("""SELECT * FROM (SELECT country, product_name, SUM(sales_amount) AS revenue, RANK() OVER (PARTITION BY country ORDER BY SUM(sales_amount) DESC) rnk FROM sales GROUP BY country, product_name) t WHERE rnk <= 3""").df()
    df_2.head()
    return (df_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Business Insight
    """)
    return


@app.cell
def _():
    print("""- Local preferences
    - Market strategy
    - Targeted campaigns""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Plot
    """)
    return


@app.cell
def _(df_2, plt):
    plt.figure(); plt.bar(df_2['product_name'], df_2['revenue']); plt.xticks(rotation=45); plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Top Country per Year — SQL
    """)
    return


@app.cell
def _(con):
    df_3 = con.execute("""SELECT * FROM (SELECT EXTRACT(YEAR FROM transaction_date) AS year, country, SUM(sales_amount) AS revenue, RANK() OVER (PARTITION BY EXTRACT(YEAR FROM transaction_date) ORDER BY SUM(sales_amount) DESC) rnk FROM sales GROUP BY year, country) t WHERE rnk = 1""").df()
    df_3.head()
    return (df_3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Business Insight
    """)
    return


@app.cell
def _():
    print("""- Market leader tracking
    - Geographic trends""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Plot
    """)
    return


@app.cell
def _(df_3, plt):
    plt.figure(); plt.bar(df_3['year'].astype(str), df_3['revenue']); plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Running Total — SQL
    """)
    return


@app.cell
def _(con):
    df_4 = con.execute("""SELECT transaction_date, SUM(sales_amount) OVER (ORDER BY transaction_date) AS running_total FROM sales LIMIT 500""").df()
    df_4.head()
    return (df_4,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Business Insight
    """)
    return


@app.cell
def _():
    print("""- Growth trajectory
    - Business momentum""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Plot
    """)
    return


@app.cell
def _(df_4, plt):
    plt.figure(); plt.plot(df_4['running_total']); plt.show()
    return


if __name__ == "__main__":
    app.run()
