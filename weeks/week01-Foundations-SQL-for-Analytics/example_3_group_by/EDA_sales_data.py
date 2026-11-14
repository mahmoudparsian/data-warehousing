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
    # 📊 FULL EDA NOTEBOOK — GROUP BY MASTERCLASS

    Focus: Learn GROUP BY through business questions.
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import matplotlib.pyplot as plt

    return duckdb, plt


@app.cell
def _():
    # INPUT_PATH = "."                  # current folder
    # INPUT_PATH = "./data"             # subfolder

    # absolute path (Mac)
    INPUT_PATH = "."
    return (INPUT_PATH,)


@app.cell
def _(duckdb):
    con = duckdb.connect()
    return (con,)


@app.cell
def _(INPUT_PATH, con):
    con.execute(f"""
    CREATE OR REPLACE TABLE sales AS
    SELECT * FROM read_csv_auto('{INPUT_PATH}/sales.csv');
    """).fetchall()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🔍 Data Preview
    """)
    return


@app.cell
def _(con):
    con.execute("SELECT * FROM sales LIMIT 5").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 📊 Country Distribution
    **Business Question:** Which countries generate most transactions?
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""SELECT country, COUNT(*) AS cnt
    FROM sales
    GROUP BY country
    ORDER BY cnt DESC""").df()

    plt.figure()
    if "bar" == "bar":
        plt.bar(_df[_df.columns[0]], _df[_df.columns[1]])
    elif "bar" == "pie":
        plt.pie(_df[_df.columns[1]], labels=_df[_df.columns[0]], autopct='%1.1f%%')

    plt.xticks(rotation=45)
    plt.title("Country Distribution")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 📊 Gender Distribution
    **Business Question:** What is the gender split?
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""SELECT gender, COUNT(*) AS cnt
    FROM sales
    GROUP BY gender""").df()

    plt.figure()
    if "pie" == "bar":
        plt.bar(_df[_df.columns[0]], _df[_df.columns[1]])
    elif "pie" == "pie":
        plt.pie(_df[_df.columns[1]], labels=_df[_df.columns[0]], autopct='%1.1f%%')

    plt.xticks(rotation=45)
    plt.title("Gender Distribution")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 📊 Product Popularity
    **Business Question:** Which products sell the most?
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""SELECT product_name, COUNT(*) AS cnt
    FROM sales
    GROUP BY product_name
    ORDER BY cnt DESC""").df()

    plt.figure()
    if "bar" == "bar":
        plt.bar(_df[_df.columns[0]], _df[_df.columns[1]])
    elif "bar" == "pie":
        plt.pie(_df[_df.columns[1]], labels=_df[_df.columns[0]], autopct='%1.1f%%')

    plt.xticks(rotation=45)
    plt.title("Product Popularity")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 📊 Revenue by Country
    **Business Question:** Which countries generate most revenue?
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""SELECT country, SUM(sales_amount) AS revenue
    FROM sales
    GROUP BY country
    ORDER BY revenue DESC""").df()

    plt.figure()
    if "bar" == "bar":
        plt.bar(_df[_df.columns[0]], _df[_df.columns[1]])
    elif "bar" == "pie":
        plt.pie(_df[_df.columns[1]], labels=_df[_df.columns[0]], autopct='%1.1f%%')

    plt.xticks(rotation=45)
    plt.title("Revenue by Country")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 📊 Revenue by Product
    **Business Question:** Which products generate most revenue?
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""SELECT product_name, SUM(sales_amount) AS revenue
    FROM sales
    GROUP BY product_name
    ORDER BY revenue DESC""").df()

    plt.figure()
    if "bar" == "bar":
        plt.bar(_df[_df.columns[0]], _df[_df.columns[1]])
    elif "bar" == "pie":
        plt.pie(_df[_df.columns[1]], labels=_df[_df.columns[0]], autopct='%1.1f%%')

    plt.xticks(rotation=45)
    plt.title("Revenue by Product")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 📊 Revenue by Gender
    **Business Question:** Who spends more?
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""SELECT gender, SUM(sales_amount) AS revenue
    FROM sales
    GROUP BY gender""").df()

    plt.figure()
    if "pie" == "bar":
        plt.bar(_df[_df.columns[0]], _df[_df.columns[1]])
    elif "pie" == "pie":
        plt.pie(_df[_df.columns[1]], labels=_df[_df.columns[0]], autopct='%1.1f%%')

    plt.xticks(rotation=45)
    plt.title("Revenue by Gender")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 📊 Age Group Revenue
    **Business Question:** Which age group spends most?
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""SELECT 
    CASE 
     WHEN age < 30 THEN '18-29'
     WHEN age < 50 THEN '30-49'
     ELSE '50+'
    END AS age_group,
    SUM(sales_amount) AS revenue
    FROM sales
    GROUP BY age_group""").df()

    plt.figure()
    if "bar" == "bar":
        plt.bar(_df[_df.columns[0]], _df[_df.columns[1]])
    elif "bar" == "pie":
        plt.pie(_df[_df.columns[1]], labels=_df[_df.columns[0]], autopct='%1.1f%%')

    plt.xticks(rotation=45)
    plt.title("Age Group Revenue")
    plt.tight_layout()
    plt.show()
    return


if __name__ == "__main__":
    app.run()
