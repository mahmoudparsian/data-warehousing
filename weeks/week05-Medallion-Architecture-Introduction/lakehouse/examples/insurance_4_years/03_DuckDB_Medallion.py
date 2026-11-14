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
    # Insurance Lakehouse Teaching Notebook
    ## DuckDB Bronze → Silver → Gold

    This notebook demonstrates a **complete mini Lakehouse pipeline**.

    Students learn:

    - Bronze ingestion
    - Silver transformations
    - Gold analytics
    - SQL insight queries
    - Charts for insights

    ---

    ## Lakehouse Architecture

    ```
    Raw Files
       │
       ▼
    ┌──────────────┐
    │   BRONZE     │
    │ Raw CSV Data │
    └──────────────┘
            │
            ▼
    ┌──────────────┐
    │    SILVER    │
    │ Clean Tables │
    └──────────────┘
            │
            ▼
    ┌──────────────┐
    │     GOLD     │
    │  KPIs / BI   │
    └──────────────┘
    ```
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import matplotlib.pyplot as plt
    from pathlib import Path

    BASE_DIR = Path(".")
    BRONZE_DIR = BASE_DIR / "insurance" / "data" / "bronze"
    return duckdb, plt


@app.cell
def _(duckdb):
    con = duckdb.connect("insurance_lakehouse.duckdb")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Bronze Layer – Raw Data
    """)
    return


@app.cell
def _(con):
    con.execute("""

    CREATE OR REPLACE VIEW bronze_insurance AS
    SELECT
        *,
        CAST(split_part(filename,'.',2) AS INTEGER) AS year
    FROM read_csv_auto(
        'data/bronze/insurance.*.csv',
        header=true,
        filename=true
    );
    """).fetchall()

    con.execute("""
    SELECT year, 
    COUNT(*) AS num_of_rows
    FROM bronze_insurance
    GROUP BY year
    ORDER BY year
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Silver Layer – Cleaned Data
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
        smoker,
        region,
        charges::DOUBLE AS charges,
        year::INTEGER AS year,

        CASE
            WHEN bmi < 18.5 THEN 'underweight'
            WHEN bmi < 25 THEN 'normal'
            WHEN bmi < 30 THEN 'overweight'
            ELSE 'obese'
        END AS bmi_class,

        CASE
            WHEN age < 30 THEN '18-29'
            WHEN age < 40 THEN '30-39'
            WHEN age < 50 THEN '40-49'
            WHEN age < 60 THEN '50-59'
            ELSE '60+'
        END AS age_band

    FROM bronze_insurance
    """).fetchall()

    con.execute("""
    SELECT year, COUNT(*) AS num_of_rows
    FROM silver_insurance
    GROUP BY year
    ORDER BY year
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Gold Layer – KPIs
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
        MEDIAN(charges) median_charges,
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
    ## Insight Queries and Charts
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Average Charges by Year
    """)
    return


@app.cell
def _(con):
    df = con.execute("""SELECT year, AVG(charges) avg_charges FROM silver_insurance GROUP BY year ORDER BY year""").df()
    df
    return (df,)


@app.cell
def _(df, plt):
    plt.figure()
    plt.plot(df["year"], df["avg_charges"])
    plt.xlabel("year")
    plt.ylabel("avg_charges")
    plt.title("Average Charges by Year")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Charges by Region
    """)
    return


@app.cell
def _(con):
    df_2 = con.execute("""SELECT region, AVG(charges) avg_charges FROM silver_insurance GROUP BY region""").df()
    df_2
    return (df_2,)


@app.cell
def _(df_2, plt):
    plt.figure()
    plt.bar(df_2["region"].astype(str), df_2["avg_charges"])
    plt.xlabel("region")
    plt.ylabel("avg_charges")
    plt.title("Charges by Region")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Charges by Smoker
    """)
    return


@app.cell
def _(con):
    df_3 = con.execute("""SELECT smoker, AVG(charges) avg_charges FROM silver_insurance GROUP BY smoker""").df()
    df_3
    return (df_3,)


@app.cell
def _(df_3, plt):
    plt.figure()
    plt.bar(df_3["smoker"].astype(str), df_3["avg_charges"])
    plt.xlabel("smoker")
    plt.ylabel("avg_charges")
    plt.title("Charges by Smoker")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Charges by BMI Class
    """)
    return


@app.cell
def _(con):
    df_4 = con.execute("""SELECT bmi_class, AVG(charges) avg_charges FROM silver_insurance GROUP BY bmi_class""").df()
    df_4
    return (df_4,)


@app.cell
def _(df_4, plt):
    plt.figure()
    plt.bar(df_4["bmi_class"].astype(str), df_4["avg_charges"])
    plt.xlabel("bmi_class")
    plt.ylabel("avg_charges")
    plt.title("Charges by BMI Class")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Charges by Age Band
    """)
    return


@app.cell
def _(con):
    df_5 = con.execute("""SELECT age_band, AVG(charges) avg_charges FROM silver_insurance GROUP BY age_band""").df()
    df_5
    return (df_5,)


@app.cell
def _(df_5, plt):
    plt.figure()
    plt.bar(df_5["age_band"].astype(str), df_5["avg_charges"])
    plt.xlabel("age_band")
    plt.ylabel("avg_charges")
    plt.title("Charges by Age Band")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Total Charges by Year
    """)
    return


@app.cell
def _(con):
    df_6 = con.execute("""SELECT year, SUM(charges) total_charges FROM silver_insurance GROUP BY year ORDER BY year""").df()
    df_6
    return (df_6,)


@app.cell
def _(df_6, plt):
    plt.figure()
    plt.plot(df_6["year"], df_6["total_charges"])
    plt.xlabel("year")
    plt.ylabel("total_charges")
    plt.title("Total Charges by Year")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Children vs Charges
    """)
    return


@app.cell
def _(con):
    df_7 = con.execute("""SELECT children, AVG(charges) avg_charges FROM silver_insurance GROUP BY children ORDER BY children""").df()
    df_7
    return (df_7,)


@app.cell
def _(df_7, plt):
    plt.figure()
    plt.plot(df_7["children"], df_7["avg_charges"])
    plt.xlabel("children")
    plt.ylabel("avg_charges")
    plt.title("Children vs Charges")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Regional Cost Ranking
    """)
    return


@app.cell
def _(con):
    df_8 = con.execute("""SELECT region, SUM(charges) total_charges FROM silver_insurance GROUP BY region ORDER BY total_charges DESC""").df()
    df_8
    return (df_8,)


@app.cell
def _(df_8, plt):
    plt.figure()
    plt.bar(df_8["region"].astype(str), df_8["total_charges"])
    plt.xlabel("region")
    plt.ylabel("total_charges")
    plt.title("Regional Cost Ranking")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Average BMI by Region
    """)
    return


@app.cell
def _(con):
    df_9 = con.execute("""SELECT region, AVG(bmi) avg_bmi FROM silver_insurance GROUP BY region""").df()
    df_9
    return (df_9,)


@app.cell
def _(df_9, plt):
    plt.figure()
    plt.bar(df_9["region"].astype(str), df_9["avg_bmi"])
    plt.xlabel("region")
    plt.ylabel("avg_bmi")
    plt.title("Average BMI by Region")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Top 20 Charges
    """)
    return


@app.cell
def _(con):
    df_10 = con.execute("""SELECT age, charges FROM silver_insurance ORDER BY charges DESC LIMIT 20""").df()
    df_10
    return (df_10,)


@app.cell
def _(df_10, plt):
    plt.figure()
    plt.plot(df_10["age"], df_10["charges"])
    plt.xlabel("age")
    plt.ylabel("charges")
    plt.title("Top 20 Charges")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Data Story

    Key insights:

    - Smoking status dramatically increases insurance costs
    - Charges increase with age
    - Higher BMI correlates with higher costs
    - A small group of high-cost patients drives overall spending
    - Regional cost differences exist but are smaller than lifestyle effects
    """)
    return


if __name__ == "__main__":
    app.run()
