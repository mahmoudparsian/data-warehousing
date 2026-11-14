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
    # 🧠 Week 1 — SQL Foundations (MASTER NOTEBOOK)

    ## Insurance Dataset — Full Analytical Journey

    Raw Data → Question → SQL → Pattern → Insight → Decision
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🔧 Setup
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import matplotlib.pyplot as plt

    con = duckdb.connect()

    con.execute("CREATE OR REPLACE TABLE insurance AS SELECT * FROM read_csv_auto('../example_1_insurance/insurance.csv')").fetchall()
    return con, pd, plt


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
def _(pd):
    df = pd.read_csv('../example_1_insurance/insurance.csv')
    df.head()
    return (df,)


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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Week 1 — SQL Foundations (Aligned with Slides)
    ## Insurance Dataset Analysis
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup
    """)
    return


@app.cell
def _():
    import duckdb as _duckdb
    _duckdb.execute("ATTACH IF NOT EXISTS 'week01.duckdb' AS week01; USE week01").fetchall()
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
    CREATE OR REPLACE TABLE insurance AS SELECT * FROM read_csv_auto('../example_1_insurance/insurance.csv');
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Preview Data
    """)
    return


@app.cell
def _(insurance, mo):
    result = mo.sql(f"""SELECT * FROM insurance LIMIT 5""")
    result
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 1 — Exploration
    **Question:** What does the dataset look like?
    """)
    return


@app.cell
def _():
    # Write your SQL below
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Solution
    """)
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql("""
    SELECT * FROM insurance LIMIT 10
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 2 — High Cost Customers
    **Question:** Who are the top 10 most expensive customers?
    """)
    return


@app.cell
def _():
    # Write your SQL below
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Solution
    """)
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql("""
    SELECT * FROM insurance ORDER BY charges DESC LIMIT 10
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 3 — Hypothesis Testing
    **Question:** Do smokers pay more?
    """)
    return


@app.cell
def _():
    # Write your SQL below
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Solution
    """)
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql("""
    SELECT smoker, AVG(charges) FROM insurance GROUP BY smoker
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 4 — Regional Analysis
    **Question:** Which region has highest average charges?
    """)
    return


@app.cell
def _():
    # Write your SQL below
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Solution
    """)
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql("""
    SELECT region, AVG(charges) 
    FROM insurance 
    GROUP BY region 
    ORDER BY AVG(charges) DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 5 — Multi-Dimensional Analysis
    **Question:** Analyze charges by region AND smoker
    """)
    return


@app.cell
def _():
    # Write your SQL below
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Solution
    """)
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql("""
    SELECT region, smoker, AVG(charges) 
    FROM insurance 
    GROUP BY region, smoker
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 6 — Filtering
    **Question:** Find high-risk customers (smokers with BMI > 30)
    """)
    return


@app.cell
def _():
    # Write your SQL below
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Solution
    """)
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql("""
    SELECT * 
    FROM insurance 
    WHERE smoker='yes' AND bmi > 30
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 7 — Distribution
    **Question:** Count customers per region
    """)
    return


@app.cell
def _():
    # Write your SQL below
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Solution
    """)
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql("""
    SELECT region, COUNT(*) FROM insurance GROUP BY region
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 8 — Business Insight
    **Question:** Which segment should be targeted for pricing strategy?
    """)
    return


@app.cell
def _():
    # Write your SQL below
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Solution
    """)
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql("""
    SELECT smoker, region, AVG(charges) 
    FROM insurance 
    GROUP BY smoker, region 
    ORDER BY AVG(charges) DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reflection Questions
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - What variables drive cost most?
    - Why is smoking important?
    - What would you do if you were the business?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 📊 Final Analysis — What Drives Cost?
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("SELECT age, AVG(charges) as avg_charges FROM insurance GROUP BY age ORDER BY age").df()

    plt.figure()
    plt.plot(_df['age'], _df['avg_charges'])
    plt.title("Charges vs Age")
    plt.xlabel("Age")
    plt.ylabel("Avg Charges")
    plt.grid()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Insight
    Charges increase with age → lifecycle cost effect
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("SELECT bmi, charges FROM insurance").df()

    plt.figure()
    plt.scatter(_df['bmi'], _df['charges'])
    plt.title("BMI vs Charges")
    plt.xlabel("BMI")
    plt.ylabel("Charges")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Insight
    Higher BMI correlates with higher charges → health risk factor
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🎯 Final Business Summary

    Key Drivers:
    - Smoking
    - BMI
    - Age

    Actions:
    - Risk-based pricing
    - Preventive programs
    """)
    return


if __name__ == "__main__":
    app.run()
