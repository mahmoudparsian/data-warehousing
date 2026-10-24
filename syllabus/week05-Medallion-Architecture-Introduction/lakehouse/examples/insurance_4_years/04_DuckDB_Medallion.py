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
    # DuckDB Medallion Architecture Demo
    ## Bronze → Silver → Gold with SQL Insights

    This notebook demonstrates a simplified **Medallion Architecture** pipeline using DuckDB.

    Pipeline stages:

    **Bronze** → Raw CSV data

    **Silver** → Cleaned and standardized data

    **Gold** → Aggregated analytics tables

    ## Bronze Layer
    	•	Raw CSV files
    	•	Direct ingestion from:

    data/bronze/insurance.*.csv

    ## Silver Layer
    	•	Cleaned and standardized data
    	•	Data cleaning
    	•	Standardization
    	•	Type casting
    	•	Normalized categorical values

    ## Gold Layer
    	•	Aggregated analytics tables
    	•	Business-ready data

    We then run **12 SQL insight queries** and visualize the results.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Setup Environment
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import matplotlib.pyplot as plt

    # '%matplotlib inline' command supported automatically in marimo
    return duckdb, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Connect to DuckDB
    """)
    return


@app.cell
def _(duckdb):
    con = duckdb.connect("medallion_demo.duckdb")
    return (con,)


@app.cell
def _(con):
    print("con=", con)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Bronze Layer (Raw Data)

    The bronze layer stores the raw source files exactly as they arrive.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE bronze_insurance AS
    SELECT *
    FROM read_csv_auto('data/bronze/insurance.*.csv')
    """).fetchall()

    con.execute("SELECT * FROM bronze_insurance LIMIT 5").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Inspect Types in Bronze
    """)
    return


@app.cell
def _(con):
    con.execute("DESCRIBE bronze_insurance").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Silver Layer (Cleaned Data)

    The silver layer standardizes and validates data.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver_insurance AS
    SELECT
        CAST(age AS INTEGER) AS age,
        LOWER(TRIM(gender::VARCHAR)) AS gender,
        CAST(bmi AS DOUBLE) AS bmi,
        CAST(children AS INTEGER) AS children,
        LOWER(TRIM(smoker::VARCHAR)) AS smoker,
        LOWER(TRIM(region::VARCHAR)) AS region,
        CAST(charges AS DOUBLE) AS charges
    FROM bronze_insurance;
    """).fetchall()

    con.execute("SELECT * FROM silver_insurance LIMIT 5").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Gold Layer (Analytics Table)

    The gold layer stores aggregated analytics-ready tables.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE gold_insurance_summary AS
    SELECT
        smoker,
        region,
        COUNT(*) AS total_patients,
        AVG(charges) AS avg_charges
    FROM silver_insurance
    GROUP BY smoker, region
    """).fetchall()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Insight Query 1: Average Charges by Region

    **Business Insight:**
    Understanding regional cost differences can help insurers identify geographic risk patterns.
    """)
    return


@app.cell
def _(con):
    df = con.execute("""
    SELECT region, AVG(charges) avg_charges
    FROM silver_insurance
    GROUP BY region
    ORDER BY avg_charges DESC
    """).df()
    df.head()
    return (df,)


@app.cell
def _(df, plt):
    df.plot(kind='bar', x='region', y='avg_charges' if 'avg_charges' in df.columns else df.columns[1])
    plt.title("Average Charges by Region")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Insight Query 2: Charges by Smoking Status

    **Business Insight:**
    Smoking is a major risk factor affecting healthcare costs.
    """)
    return


@app.cell
def _(con):
    df_2 = con.execute("""
    SELECT smoker, AVG(charges) avg_charges
    FROM silver_insurance
    GROUP BY smoker
    """).df()
    df_2.head()
    return (df_2,)


@app.cell
def _(df_2, plt):
    df_2.plot(kind='bar', x='smoker', y='avg_charges' if 'avg_charges' in df_2.columns else df_2.columns[1])
    plt.title("Charges by Smoking Status")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Insight Query 3: Average Charges by Gender

    **Business Insight:**
    Examining potential gender-based differences in healthcare expenses.
    """)
    return


@app.cell
def _(con):
    df_3 = con.execute("""
    SELECT gender, AVG(charges) avg_charges
    FROM silver_insurance
    GROUP BY gender
    """).df()
    df_3.head()
    return (df_3,)


@app.cell
def _(df_3, plt):
    df_3.plot(kind='bar', x='gender', y='avg_charges' if 'avg_charges' in df_3.columns else df_3.columns[1])
    plt.title("Average Charges by Gender")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Insight Query 4: Charges by Number of Children

    **Business Insight:**
    Family size may influence healthcare spending patterns.
    """)
    return


@app.cell
def _(con):
    df_4 = con.execute("""
    SELECT children, AVG(charges) avg_charges
    FROM silver_insurance
    GROUP BY children
    ORDER BY children
    """).df()
    df_4.head()
    return (df_4,)


@app.cell
def _(df_4, plt):
    df_4.plot(kind='bar', x='children', y='avg_charges' if 'avg_charges' in df_4.columns else df_4.columns[1])
    plt.title("Charges by Number of Children")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Insight Query 5: BMI vs Charges Trend

    **Business Insight:**
    Understanding how BMI correlates with insurance costs.
    """)
    return


@app.cell
def _(con):
    df_5 = con.execute("""
    SELECT bmi, charges
    FROM silver_insurance
    LIMIT 1000
    """).df()
    df_5.head()
    return (df_5,)


@app.cell
def _(df_5, plt):
    plt.figure(figsize=(8,5))

    plt.scatter(df_5["bmi"], df_5["charges"], alpha=0.5)

    plt.title("BMI vs Insurance Charges")
    plt.xlabel("BMI")
    plt.ylabel("Charges")

    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Insight Query 6: Age vs Charges Trend

    **Business Insight:**
    Healthcare costs often increase with age.
    """)
    return


@app.cell
def _(con):
    df_6 = con.execute("""
    SELECT age, charges
    FROM silver_insurance
    LIMIT 1000
    """).df()
    df_6.head()
    return (df_6,)


@app.cell
def _(df_6, plt):
    import seaborn as sns
    plt.style.use("seaborn-v0_8")

    plt.figure(figsize=(8,5))

    sns.regplot(
        x="age",
        y="charges",
        data=df_6,
        scatter_kws={"alpha":0.4}
    )

    plt.title("Age vs Insurance Charges")
    plt.xlabel("Age")
    plt.ylabel("Charges")

    plt.show()
    return (sns,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Insight Query 7: Average Charges by Region and Smoking

    **Business Insight:**
    Combining lifestyle and geographic factors for deeper insights.
    """)
    return


@app.cell
def _(con):
    df_7 = con.execute("""
    SELECT region, smoker, AVG(charges) avg_charges
    FROM silver_insurance
    GROUP BY region, smoker
    """).df()
    df_7.head()
    return (df_7,)


@app.cell
def _(df_7, plt):
    df_7.plot(kind='bar', x='region', y='avg_charges' if 'avg_charges' in df_7.columns else df_7.columns[1])
    plt.title("Average Charges by Region and Smoking")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Insight Query 8: Top Regions by Average Charges

    **Business Insight:**
    Identifying the most expensive regions for insurance coverage.
    """)
    return


@app.cell
def _(con):
    df_8 = con.execute("""
    SELECT region, AVG(charges) avg_charges
    FROM silver_insurance
    GROUP BY region
    ORDER BY avg_charges DESC
    LIMIT 4
    """).df()
    df_8.head()
    return (df_8,)


@app.cell
def _(df_8, plt):
    df_8.plot(kind='bar', x='region', y='avg_charges' if 'avg_charges' in df_8.columns else df_8.columns[1])
    plt.title("Top Regions by Average Charges")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Insight Query 9: Average BMI by Region

    **Business Insight:**
    Examining regional health patterns.
    """)
    return


@app.cell
def _(con):
    df_9 = con.execute("""
    SELECT region, AVG(bmi) avg_bmi
    FROM silver_insurance
    GROUP BY region
    """).df()
    df_9.head()
    return (df_9,)


@app.cell
def _(df_9, plt):
    df_9.plot(kind='bar', x='region', y='avg_bmi' if 'avg_bmi' in df_9.columns else df_9.columns[1])
    plt.title("Average BMI by Region")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Insight Query 10: Average Charges by Age Group

    **Business Insight:**
    Grouping patients into age segments for insurance pricing strategies.
    """)
    return


@app.cell
def _(con):
    df_10 = con.execute("""
    SELECT
    CASE
    WHEN age < 30 THEN 'Under 30'
    WHEN age < 50 THEN '30-49'
    ELSE '50+'
    END AS age_group,
    AVG(charges) avg_charges
    FROM silver_insurance
    GROUP BY age_group
    """).df()
    df_10.head()
    return (df_10,)


@app.cell
def _(df_10, plt):
    df_10.plot(kind='bar', x='age_group', y='avg_charges' if 'avg_charges' in df_10.columns else df_10.columns[1])
    plt.title("Average Charges by Age Group")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Insight Query 11: Smoker Distribution

    **Business Insight:**
    Understanding the proportion of smokers among insured individuals.
    """)
    return


@app.cell
def _(con):
    df_11 = con.execute("""
    SELECT smoker, COUNT(*) total
    FROM silver_insurance
    GROUP BY smoker
    """).df()
    df_11.head()
    return (df_11,)


@app.cell
def _(df_11, plt):
    df_11.plot(kind='bar', x='smoker', y='total' if 'total' in df_11.columns else df_11.columns[1])
    plt.title("Smoker Distribution")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Insight Query 12: Regional Patient Counts

    **Business Insight:**
    Analyzing population distribution across regions.
    """)
    return


@app.cell
def _(con):
    df_12 = con.execute("""
    SELECT region, COUNT(*) total
    FROM silver_insurance
    GROUP BY region
    """).df()
    df_12.head()
    return (df_12,)


@app.cell
def _(df_12, plt):
    df_12.plot(kind='bar', x='region', y='total' if 'total' in df_12.columns else df_12.columns[1])
    plt.title("Regional Patient Counts")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Visualization 1 — Smoking Impact on Insurance Charges

    ## Business Insight

    ## Smoking dramatically increases healthcare costs.

    ## Smoking is the strongest predictor of high medical costs
    """)
    return


@app.cell
def _(con, plt):
    # Smoking vs Charges

    plt.style.use("seaborn-v0_8")

    smoker_analysis = con.execute("""
    SELECT
        smoker,
        AVG(charges) AS avg_charges
    FROM silver_insurance
    GROUP BY smoker
    """).df()

    plt.figure(figsize=(8,5))

    plt.bar(smoker_analysis["smoker"], smoker_analysis["avg_charges"])

    plt.title("Average Insurance Charges: Smokers vs Non-Smokers")
    plt.xlabel("Smoking Status")
    plt.ylabel("Average Charges")

    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Visualization 2 — Age vs Charges Trend

    ## Business Insight

    ## Healthcare costs tend to increase with age.

    ## Age is positively correlated with healthcare costs
    """)
    return


@app.cell
def _(con, plt, sns):
    # Age vs Charges Trend (Clean Version)


    df_age = con.execute("""
    SELECT age, charges
    FROM silver_insurance
    WHERE age IS NOT NULL
    AND charges IS NOT NULL
    """).df()

    # Remove extreme outliers (optional but useful for teaching)
    df_age = df_age[df_age["charges"] < 60000]

    plt.figure(figsize=(8,5))

    sns.regplot(
        x="age",
        y="charges",
        data=df_age,
        scatter_kws={"alpha":0.4},
        line_kws={"color":"red"}
    )

    plt.title("Age vs Insurance Charges")
    plt.xlabel("Age")
    plt.ylabel("Charges")

    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Visualization 3 — BMI Risk Groups

    ## Business Insight

    ## Higher BMI is associated with increased insurance costs.

    ## We see the health risk relationship between BMI and insurance costs.
    """)
    return


@app.cell
def _(con, pd, plt):
    # BMI Risk Analysis (Clean Version)

    df_bmi = con.execute("""
    SELECT bmi, charges
    FROM silver_insurance
    WHERE bmi IS NOT NULL
    AND charges IS NOT NULL
    """).df()

    df_bmi["bmi_group"] = pd.cut(
        df_bmi["bmi"],
        bins=[15,20,25,30,35,40,45],
        labels=["15-20","20-25","25-30","30-35","35-40","40-45"]
    )

    bmi_analysis = df_bmi.groupby("bmi_group", observed=True)["charges"].mean().reset_index()

    plt.figure(figsize=(8,5))

    plt.bar(bmi_analysis["bmi_group"], bmi_analysis["charges"])

    plt.title("Average Insurance Charges by BMI Range")
    plt.xlabel("BMI Range")
    plt.ylabel("Average Charges")

    plt.show()
    return


if __name__ == "__main__":
    app.run()
