import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Week 1 — A First Look at the Insurance Data (EDA + SQL)

    **Question for this notebook:** what makes a customer expensive?
    Six steps: load → structure → distribution → outliers → one hypothesis (smoking) → check it in SQL.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Data

    ```
    % head ../example_1_insurance/insurance.csv
    age,gender,bmi,children,smoker,region,charges
    19,female,27.9,0,yes,southwest,16884.924
    18,male,33.77,1,no,southeast,1725.5523
    28,male,33,3,no,southeast,4449.462
    33,male,22.705,0,no,northwest,21984.47061
    32,male,28.88,0,no,northwest,3866.8552
    31,female,25.74,0,no,southeast,3756.6216
    46,female,33.44,1,no,southeast,8240.5896
    37,female,27.74,3,no,northwest,7281.5056
    37,male,29.83,2,no,northeast,6406.4107
    ```

    One row per insured customer; `charges` = the yearly medical cost billed by the insurer (US $).
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
    **Observation:** 1,338 rows, no missing values. Ages 18–64. `charges` goes from about 1,100 to 63,800:
    a **mean of 13,270** but a **median (50%) of 9,382**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 3 — Distribution of Charges
    """)
    return


@app.cell
def _(df, plt):
    df['charges'].hist(bins=30)
    plt.title('Distribution of Charges')
    plt.xlabel('Charges (US $)')
    plt.ylabel('Customers')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Observation:** the distribution is **right-skewed**: about 3 in 4 customers (73%) cost under 15,000, and a long tail of expensive customers
    pulls the mean (13,270) 41% above the median (9,382). For a "typical customer", report the **median**.
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
    **Observation:** the box holds the middle half of the customers (about 4,700 to 16,600). The dots above the top whisker
    (charges above about 34,500) are **139 customers**: are they random, or do they share something?
    """)
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
    plt.ylabel('Average charges (US $)')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Insight:** smokers average **32,050**, non-smokers **8,434**: smokers cost **3.8×** as much.
    And the 139 outliers from Step 4? **136 of them are smokers.**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 6 — The Same Question in SQL (DuckDB)

    `con.register` lets SQL read the pandas DataFrame `df` as a table. In pandas, `smoker` is the text `'yes'` / `'no'`
    (DuckDB's own `read_csv` would make it BOOLEAN, as in the slides).
    """)
    return


@app.cell
def _(df, duckdb):
    con = duckdb.connect()
    con.register('insurance', df)

    con.execute("""
    SELECT smoker,
           COUNT(*)               AS customers,
           ROUND(AVG(charges), 0) AS avg_charges
    FROM insurance
    GROUP BY smoker
    ORDER BY avg_charges DESC
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Same answer** as the chart: 274 smokers at 32,050, 1,064 non-smokers at 8,434.
    Next: the exercises in `notebook_02_sql_exercises.py` check this with a **second dimension** (region × smoker).
    """)
    return


if __name__ == "__main__":
    app.run()
