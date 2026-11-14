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
    # Exploratory Data Analysis (EDA)
    ## Insurance Dataset using DuckDB

    This notebook performs exploratory data analysis on the insurance dataset located in the bronze layer.

    Goals:
    - Demonstrate EDA workflow
    - Use DuckDB to query CSV files
    - Generate visual insights
    - Prepare for Bronze → Silver → Gold pipeline
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
    import seaborn as sns
    # '%matplotlib inline' command supported automatically in marimo
    return duckdb, plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Connect to DuckDB
    """)
    return


@app.cell
def _(duckdb):
    con = duckdb.connect('insurance_eda.duckdb')
    return (con,)


@app.cell
def _(con):
    print("con=", con)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Load Bronze Data (All CSV Files)
    """)
    return


@app.cell
def _(con):
    df = con.execute("""
    SELECT *
    FROM read_csv_auto('./data/insurance.*.csv')
    """).df()
    df.head()
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Basic Dataset Information
    """)
    return


@app.cell
def _(df):
    df.shape
    return


@app.cell
def _(df):
    df.columns
    return


@app.cell
def _(df):
    df.dtypes
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Summary Statistics
    """)
    return


@app.cell
def _(df):
    df.describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Missing Values
    """)
    return


@app.cell
def _(df):
    df.isnull().sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Age Distribution
    """)
    return


@app.cell
def _(df, plt):
    plt.figure(figsize=(6,4))
    plt.hist(df['age'], bins=20)
    plt.title('Age Distribution')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. BMI Distribution
    """)
    return


@app.cell
def _(df, plt):
    plt.figure(figsize=(6,4))
    plt.hist(df['bmi'], bins=20)
    plt.title('BMI Distribution')
    plt.xlabel('BMI')
    plt.ylabel('Frequency')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Charges Distribution
    """)
    return


@app.cell
def _(df, plt):
    plt.figure(figsize=(6,4))
    plt.hist(df['charges'], bins=30)
    plt.title('Insurance Charges Distribution')
    plt.xlabel('Charges')
    plt.ylabel('Frequency')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Gender Distribution
    """)
    return


@app.cell
def _(df, plt):
    df['gender'].value_counts().plot(kind='bar')
    plt.title('Gender Distribution')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 11. Region Distribution
    """)
    return


@app.cell
def _(df, plt):
    df['region'].value_counts().plot(kind='bar')
    plt.title('Region Distribution')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 12. Smokers vs Charges
    """)
    return


@app.cell
def _(df, plt, sns):
    sns.boxplot(x='smoker', y='charges', data=df)
    plt.title('Charges: Smokers vs Non-Smokers')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 13. BMI vs Charges
    """)
    return


@app.cell
def _(df, plt):
    plt.figure(figsize=(6,4))
    plt.scatter(df['bmi'], df['charges'])
    plt.title('BMI vs Charges')
    plt.xlabel('BMI')
    plt.ylabel('Charges')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 14. Average Charges by Region
    """)
    return


@app.cell
def _(con, plt):
    region_charges = con.execute("""
    SELECT region, AVG(charges) avg_charges
    FROM df
    GROUP BY region
    ORDER BY avg_charges DESC
    """).df()

    region_charges.plot(kind='bar', x='region', y='avg_charges')
    plt.title('Average Charges by Region')
    plt.ylabel('Average Charges')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 15. Correlation Matrix
    """)
    return


@app.cell
def _(df, plt, sns):
    corr = df[['age','bmi','children','charges']].corr(numeric_only=True)
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Insights
    - Smokers tend to have significantly higher insurance charges.
    - Age appears positively correlated with charges.
    - BMI shows moderate correlation with charges.
    - Regional differences are relatively small.

    Next step: move from **Bronze → Silver → Gold** in a Medallion Architecture pipeline.
    """)
    return


if __name__ == "__main__":
    app.run()
