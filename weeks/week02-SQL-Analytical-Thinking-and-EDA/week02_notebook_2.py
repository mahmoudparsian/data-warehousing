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
    # Insurance Data Analytics with DuckDB
    This notebook includes NL Query, SQL, visualization, and business insights.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Create DuckDB Connection
    **NL Query:** Create a connection to DuckDB
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import matplotlib.pyplot as plt

    con = duckdb.connect(database=':memory:')
    return con, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Load Data
    **NL Query:** Load insurance.csv into DuckDB
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE insurance AS
    SELECT *
    FROM read_csv_auto('../week01-Foundations-SQL-for-Analytics/example_1_insurance/insurance.csv');
    """).fetchall()

    con.execute("SELECT COUNT(*) FROM insurance").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Top 3 Charges per Region
    **Business Insight:** Identify high-cost customers per region
    """)
    return


@app.cell
def _(con):
    _query = """
    SELECT *
    FROM (
        SELECT region, age, charges,
               RANK() OVER (PARTITION BY region ORDER BY charges DESC) AS rnk
        FROM insurance
    ) t
    WHERE rnk <= 3;
    """

    df = con.execute(_query).df()
    df
    return (df,)


@app.cell
def _(df, plt):
    plt.figure(figsize=(10,5))
    plt.bar(range(len(df)), df['charges'])
    plt.title("Top 3 Charges per Region")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Compare to Regional Average
    """)
    return


@app.cell
def _(con):
    _query = """
    SELECT region, age, charges,
           AVG(charges) OVER (PARTITION BY region) AS regional_avg
    FROM insurance;
    """

    df_2 = con.execute(_query).df()
    return (df_2,)


@app.cell
def _(df_2, plt):
    plt.scatter(df_2['regional_avg'], df_2['charges'])
    plt.title("Customer vs Regional Avg")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Above Average Customers
    """)
    return


@app.cell
def _(con):
    _query = """
    SELECT *
    FROM (
        SELECT *, AVG(charges) OVER (PARTITION BY region) AS regional_avg
        FROM insurance
    ) t
    WHERE charges > regional_avg;
    """

    df_3 = con.execute(_query).df()
    return (df_3,)


@app.cell
def _(df_3, plt):
    plt.hist(df_3['charges'], bins=30)
    plt.title("Above Average Charges")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. % Contribution
    """)
    return


@app.cell
def _(con):
    _query = """
    SELECT charges,
           charges * 100.0 / SUM(charges) OVER () AS pct_total
    FROM insurance;
    """

    df_4 = con.execute(_query).df()
    return (df_4,)


@app.cell
def _(df_4, plt):
    plt.hist(df_4['pct_total'], bins=30)
    plt.title("% Contribution")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Running Total by Age
    """)
    return


@app.cell
def _(con):
    _query = """
    SELECT age,
           SUM(charges) AS total_charges,
           SUM(SUM(charges)) OVER (ORDER BY age) AS running_total
    FROM insurance
    GROUP BY age;
    """

    df_5 = con.execute(_query).df()
    return (df_5,)


@app.cell
def _(df_5, plt):
    plt.plot(df_5['age'], df_5['running_total'])
    plt.title("Running Total by Age")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Do Smokers Pay More?
    """)
    return


@app.cell
def _(con):
    _query = """
    SELECT smoker, AVG(charges) AS avg_charges
    FROM insurance
    GROUP BY smoker;
    """

    df_6 = con.execute(_query).df()
    return (df_6,)


@app.cell
def _(df_6, plt):
    plt.bar(df_6['smoker'], df_6['avg_charges'])
    plt.title("Smoker vs Charges")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. BMI vs Charges
    """)
    return


@app.cell
def _(con):
    _query = "SELECT bmi, charges FROM insurance;"
    df_7 = con.execute(_query).df()
    return (df_7,)


@app.cell
def _(df_7, plt):
    plt.scatter(df_7['bmi'], df_7['charges'])
    plt.title("BMI vs Charges")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Smokers vs BMI
    """)
    return


@app.cell
def _(con):
    _query = "SELECT smoker, bmi FROM insurance;"
    df_8 = con.execute(_query).df()
    return (df_8,)


@app.cell
def _(df_8, plt):
    for s in df_8['smoker'].unique():
        subset = df_8[df_8['smoker']==s]
        plt.hist(subset['bmi'], alpha=0.5, label=s)

    plt.legend()
    plt.title("BMI Distribution by Smoker")
    plt.show()
    return


if __name__ == "__main__":
    app.run()
