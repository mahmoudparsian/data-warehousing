# test: skip — needs a MySQL server with the example's destination_table (MySQL reference example; see README.md)
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

    Target Table: `destination_table`
    """)
    return


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    from sqlalchemy import create_engine

    return create_engine, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Load Data from MySQL
    """)
    return


@app.cell
def _(create_engine, pd):
    engine = create_engine(
        "mysql+mysqlconnector://root:YOUR_MYSQL_PASSWORD@localhost/scu2_homeworks"
    )

    query = '''
    SELECT id, name, age, country, salary, continent
    FROM destination_table
    '''

    df = pd.read_sql(query, engine)
    df.head()
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Dataset Overview
    """)
    return


@app.cell
def _(df):
    df.info()
    df.describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Salary Distribution
    """)
    return


@app.cell
def _(df, plt):
    plt.hist(df['salary'], bins=20)
    plt.xlabel("Salary")
    plt.ylabel("Frequency")
    plt.title("Salary Distribution")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Salary by Continent
    """)
    return


@app.cell
def _(df, plt):
    df.boxplot(column='salary', by='continent')
    plt.title("Salary Distribution by Continent")
    plt.suptitle("")
    plt.xlabel("Continent")
    plt.ylabel("Salary")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Average Salary per Country
    """)
    return


@app.cell
def _(df, plt):
    avg_salary_country = df.groupby('country')['salary'].mean().sort_values(ascending=False)
    avg_salary_country.plot(kind='bar')
    plt.xlabel("Country")
    plt.ylabel("Average Salary")
    plt.title("Average Salary per Country")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Employee Count per Continent
    """)
    return


@app.cell
def _(df, plt):
    df['continent'].value_counts().plot(kind='bar')
    plt.xlabel("Continent")
    plt.ylabel("Employee Count")
    plt.title("Employee Distribution by Continent")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Age vs Salary
    """)
    return


@app.cell
def _(df, plt):
    plt.scatter(df['age'], df['salary'])
    plt.xlabel("Age")
    plt.ylabel("Salary")
    plt.title("Age vs Salary")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Salary Bands
    """)
    return


@app.cell
def _(df, pd, plt):
    df['salary_band'] = pd.cut(
        df['salary'],
        bins=[0, 40000, 60000, 80000, 100000, 200000],
        labels=["Low", "Mid", "Upper-Mid", "High", "Very High"]
    )

    df['salary_band'].value_counts().sort_index().plot(kind='bar')
    plt.xlabel("Salary Band")
    plt.ylabel("Count")
    plt.title("Salary Band Distribution")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Missing Values
    """)
    return


@app.cell
def _(df):
    df.isnull().sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Correlation Analysis
    """)
    return


@app.cell
def _(df):
    corr = df[['age', 'salary']].corr(numeric_only=True)
    corr
    return (corr,)


@app.cell
def _(corr, plt):
    plt.imshow(corr)
    plt.colorbar()
    plt.xticks(range(len(corr)), corr.columns)
    plt.yticks(range(len(corr)), corr.columns)
    plt.title("Correlation Matrix")
    plt.show()
    return


if __name__ == "__main__":
    app.run()
