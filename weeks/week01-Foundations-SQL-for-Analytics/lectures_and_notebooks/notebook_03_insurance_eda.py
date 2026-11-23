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
    # Full EDA — Insurance Dataset
    Comprehensive analysis with proper plotting
    """)
    return


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.read_csv('../example_1_insurance/insurance.csv')
    df.head()
    return df, plt


@app.cell
def _(df):
    df.info()
    df.describe()
    return


@app.cell
def _(df):
    df.isnull().sum()
    return


@app.cell
def _(df, plt):
    num_cols = ['age','bmi','children','charges']
    for _col in num_cols:
        plt.figure()
        plt.hist(df[_col], bins=30)
        plt.title(f'Distribution of {_col}')
        plt.xlabel(_col)
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.show()
    return (num_cols,)


@app.cell
def _(df, num_cols, plt):
    for _col in num_cols:
        plt.figure()
        plt.boxplot(df[_col])
        plt.title(f'Boxplot of {_col}')
        plt.tight_layout()
        plt.show()
    return


@app.cell
def _(df, plt):
    cat_cols = ['gender','smoker','region']
    for _col in cat_cols:
        counts = df[_col].value_counts()
        plt.figure()
        plt.bar(counts.index, counts.values)
        plt.title(f'{_col} Distribution')
        plt.xlabel(_col)
        plt.ylabel('Count')
        plt.tight_layout()
        plt.show()
    return


@app.cell
def _(df, plt):
    groups = df.groupby('smoker')['charges']
    data = [groups.get_group(x) for x in groups.groups]
    plt.figure()
    plt.boxplot(data, tick_labels=list(groups.groups.keys()))   # matplotlib ≥ 3.9: tick_labels (was labels)
    plt.title('Charges by Smoker')
    plt.xlabel('Smoker')
    plt.ylabel('Charges')
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df, plt):
    plt.figure()
    plt.scatter(df['age'], df['charges'])
    plt.title('Charges vs Age')
    plt.xlabel('Age')
    plt.ylabel('Charges')
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df, plt):
    plt.figure()
    plt.scatter(df['bmi'], df['charges'])
    plt.title('Charges vs BMI')
    plt.xlabel('BMI')
    plt.ylabel('Charges')
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df, plt):
    region_avg = df.groupby('region')['charges'].mean()
    plt.figure()
    plt.bar(region_avg.index, region_avg.values)
    plt.title('Average Charges by Region')
    plt.xlabel('Region')
    plt.ylabel('Avg Charges')
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df, plt):
    corr = df[['age','bmi','children','charges']].corr(numeric_only=True)
    plt.figure()
    plt.imshow(corr)
    plt.xticks(range(len(corr)), corr.columns, rotation=45)
    plt.yticks(range(len(corr)), corr.columns)
    plt.title('Correlation Matrix')
    plt.colorbar()
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Insights
    - Smoking has a major impact on charges
    - Charges increase with age
    - BMI shows moderate relationship
    - Region differences are smaller compared to smoking effect
    """)
    return


if __name__ == "__main__":
    app.run()
