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
    # 🧠 Week 1 — SQL Foundations (Insurance Dataset)

    ## Story-Driven Analytics with DuckDB

    In this notebook, we follow the **Analyst Journey**:

    > Raw Data → Question → SQL → Pattern → Insight → Decision

    Each section includes:
    - Problem definition
    - SQL solution
    - Explanation
    - Business insight
    - Visualization (when applicable)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🔧 Setup: Load Data into DuckDB
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import matplotlib.pyplot as plt

    con = duckdb.connect()

    con.execute("""
    CREATE OR REPLACE TABLE insurance AS 
    SELECT * FROM read_csv_auto('insurance.csv');
    """).fetchall()
    return con, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🔹 Section 1 — Understanding the Data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 1: What does the dataset look like?

    ### Goal
    Get a quick feel for the structure and values.
    """)
    return


@app.cell
def _(con):
    con.execute('SELECT * FROM insurance LIMIT 10').df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    Before analysis, always inspect data to avoid wrong assumptions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🔹 Section 2 — Basic Aggregations
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 2: What is the average insurance cost?

    ### Goal
    Understand baseline cost across all customers.
    """)
    return


@app.cell
def _(con):
    _df = con.execute("SELECT AVG(charges) AS avg_charges FROM insurance").df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Insight
    This gives us a benchmark for all comparisons.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🔥 Section 3 — Key Business Question
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 3: Do smokers pay more?

    ### Goal
    Understand impact of smoking on insurance cost.
    """)
    return


@app.cell
def _(con):
    df = con.execute("""
    SELECT smoker, AVG(charges) AS avg_charges
    FROM insurance
    GROUP BY smoker
    """).df()

    df
    return (df,)


@app.cell
def _(df, plt):
    plt.figure()
    plt.bar(df['smoker'], df['avg_charges'])
    plt.title("Average Charges: Smokers vs Non-Smokers")
    plt.xlabel("Smoker")
    plt.ylabel("Charges")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight 🚨
    Smokers typically incur significantly higher costs → higher risk → higher premiums.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 4: How does BMI affect cost?

    ### Goal
    Group customers into BMI categories.
    """)
    return


@app.cell
def _(con):
    df_2 = con.execute("""
    SELECT 
      CASE 
        WHEN bmi < 25 THEN 'Normal'
        WHEN bmi < 30 THEN 'Overweight'
        ELSE 'Obese'
      END AS bmi_group,
      AVG(charges) AS avg_charges
    FROM insurance
    GROUP BY bmi_group
    """).df()

    df_2
    return (df_2,)


@app.cell
def _(df_2, plt):
    plt.figure()
    plt.bar(df_2['bmi_group'], df_2['avg_charges'])
    plt.title("Charges by BMI Category")
    plt.xlabel("BMI Group")
    plt.ylabel("Charges")
    plt.show()
    return


@app.cell
def _(con):
    df_3 = con.execute("""
    SELECT 
      CASE 
        WHEN age < 20 THEN 'group-1'
        WHEN age < 30 THEN 'group-2'
        WHEN age < 40 THEN 'group-3'
        WHEN age < 50 THEN 'group-4'
        WHEN age < 60 THEN 'group-5'
        ELSE 'group-6'
      END AS age_group,
      AVG(charges) AS avg_charges
    FROM insurance
    GROUP BY age_group
    ORDER BY avg_charges
    """).df()

    df_3
    return (df_3,)


@app.cell
def _(df_3, plt):
    plt.figure()
    plt.bar(df_3['age_group'], df_3['avg_charges'])
    plt.title("Charges by Age Category/Group")
    plt.xlabel("Age Group")
    plt.ylabel("Charges")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # AVG Charges Per Gender
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
    SELECT 
      gender,
      AVG(charges) AS avg_charges
    FROM insurance
    GROUP BY gender
    ORDER BY avg_charges
    """).df()

    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Insight
    Higher BMI → higher healthcare costs → pricing impact.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 5: Do regions differ in cost?
    """)
    return


@app.cell
def _(con):
    df_4 = con.execute("""
    SELECT region, 
           AVG(charges) AS avg_charges
    FROM insurance
    GROUP BY region
    ORDER BY avg_charges DESC
    """).df()

    df_4
    return (df_4,)


@app.cell
def _(df_4, plt):
    plt.figure()
    plt.bar(df_4['region'], df_4['avg_charges'])
    plt.title("Average Charges by Region")
    plt.xlabel("Region")
    plt.ylabel("Charges")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Insight
    Geographic factors may influence pricing.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🔺 Section 4 — Advanced SQL
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 6: Who are the highest-risk customers?

    ### Goal
    Rank customers by charges.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT *, RANK() OVER (ORDER BY charges DESC) AS rnk
    FROM insurance
    LIMIT 10
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Insight
    Top-ranked individuals are high-cost → high-risk segment.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🧪 Section 5 — Debugging SQL
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 7: Why does this query fail?
    """)
    return


@app.cell
def _(con):
    # Intentional error: run it and read the message (the try/except only keeps the notebook running)
    try:
        con.execute("""
        SELECT region AVG(charges)
        FROM insurance
        GROUP BY region
        """).fetchall()
    except Exception as e:
        print("DuckDB error:", e)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Fix the issue
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT region, AVG(charges)
    FROM insurance
    GROUP BY region
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🎯 Final Takeaways

    - SQL is a thinking tool, not just syntax
    - Always connect queries to business meaning
    - Visualization helps communicate insights
    """)
    return


if __name__ == "__main__":
    app.run()
