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
    # 📝 Basic Data Exploration Report

    This notebook contains a simple exploratory data analysis on a sample dataset.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Table of Contents
    1. Introduction
    2. Loading the Data
    3. Data Overview
    4. Missing Values
    5. Descriptive Statistics
    6. Univariate Analysis
    7. Bivariate Analysis
    8. Observations & Insights
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Loading the Data
    """)
    return


@app.cell
def _():
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt

    # Sample data
    data = {
        'age': [19, 18, 28, 45, 34],
        'gender': ['female', 'male', 'male', 'female', 'male'],
        'bmi': [27.9, 33.77, 33.0, 28.5, 31.0],
        'children': [0, 1, 3, 2, 1],
        'smoker': ['yes', 'no', 'no', 'yes', 'no'],
        'region': ['west', 'south-east', 'south-west', 'north', 'east'],
        'charges': [16884.92, 1725.55, 4449.46, 21984.5, 12365.0]
    }

    df = pd.DataFrame(data)
    return df, plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Data Overview
    """)
    return


@app.cell
def _(df):
    print('Shape:', df.shape)
    print('\nData types:\n', df.dtypes)
    df.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Missing Values
    """)
    return


@app.cell
def _(df):
    df.isnull().sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Descriptive Statistics
    """)
    return


@app.cell
def _(df):
    df.describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Univariate Analysis
    """)
    return


@app.cell
def _(df, plt, sns):
    sns.histplot(df['charges'], kde=True)
    plt.title('Distribution of Charges')
    plt.show()
    return


@app.cell
def _(df, plt, sns):
    sns.countplot(x='smoker', data=df)
    plt.title('Smoker Count')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Bivariate Analysis
    """)
    return


@app.cell
def _(df, plt, sns):
    sns.scatterplot(x='age', y='charges', hue='smoker', data=df)
    plt.title('Age vs Charges by Smoker')
    plt.show()
    return


@app.cell
def _(df, plt, sns):
    sns.boxplot(x='smoker', y='charges', data=df)
    plt.title('Charges by Smoking Status')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Observations & Insights
    - Smokers tend to have higher charges.
    - Age and number of children may impact charges.
    - No missing values detected.
    - BMI does not show a strong trend with charges in this small sample.
    """)
    return


if __name__ == "__main__":
    app.run()
