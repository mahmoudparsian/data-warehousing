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
    # Exploratory Data Analysis (EDA), Basic
    ## Insurance Data, 2021–2024 (4 yearly files) with DuckDB + pandas

    Goal: a first **profile** of the raw (Bronze) files, mostly with **charts**: shape, missing values, duplicates,
    distributions, categories, and the first relationships. Slides: `1.What_is_Exploratory_Data_Analysis.md`.
    The step-by-step Bronze → Silver → Gold version is `3.EDA_comprehensive.py`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Setup
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    return duckdb, plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Connect to DuckDB

    In memory: nothing is written to disk.
    """)
    return


@app.cell
def _(duckdb):
    con = duckdb.connect()
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Load the Four Yearly Files (Bronze)

    `filename = true` keeps the source file, which we turn into a `year` column: without it, the 4 years would be mixed with no way back.
    """)
    return


@app.cell
def _(con):
    df = con.execute("""
    SELECT * EXCLUDE (filename),
           regexp_extract(filename, '(\\d{4})', 1)::INTEGER AS year
    FROM read_csv('data/insurance.*.csv', filename = true, union_by_name = true)
    """).df()
    df.head()
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Shape, Columns, Types, Rows per Year
    """)
    return


@app.cell
def _(df):
    print("rows, columns:", df.shape)
    print(df.dtypes)
    df['year'].value_counts().sort_index()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Observation:** 6,121 rows, 7 data columns + `year`. 2022 has only 1,300 rows (the other years 1,540–1,732): a smaller year or a missing part of the file?
    `smoker` arrives as `True` / `False` (DuckDB reads `yes` / `no` as BOOLEAN).
    """)
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
    **Observation:** ages 18–65, BMI 15.5–52.0: plausible ranges. `charges`: mean 18,455 but median (50%) 14,816 → right-skewed,
    and a minimum of exactly **200.00** (step 9).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Missing Values and Duplicates
    """)
    return


@app.cell
def _(df):
    print("missing values per column:")
    print(df.isnull().sum())
    print()
    print("exact duplicate rows (same year, all columns equal):", df.duplicated().sum())
    _unique = df.drop_duplicates()
    _no_region = [c for c in _unique.columns if c != 'region']
    _conflicts = _unique[_unique.duplicated(subset=_no_region, keep=False)]
    print("rows that differ from another row ONLY in region:", len(_conflicts))
    df[df.duplicated(keep=False)].groupby('year').size()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Observation:** no missing values, but **222 duplicate rows** (the table above counts, per year, every row that has a copy, copies included). The files have no customer id,
    so a whole repeated row is our only signal. Worse: **1,350 rows** (675 pairs) are identical except for `region`, and every pair has one copy
    in the **northeast**. A customer cannot live in two regions in the same year: only the source system can say which copy is right.
    Every count and average below still **includes** all of these: Silver must remove or flag them first.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Age Distribution
    """)
    return


@app.cell
def _(df, plt):
    plt.figure(figsize=(6, 4))
    plt.hist(df['age'], bins=24)
    plt.title('Age Distribution')
    plt.xlabel('Age')
    plt.ylabel('Rows')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Observation:** ages spread fairly evenly from 18 to 65 (median 41).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. BMI Distribution
    """)
    return


@app.cell
def _(df, plt):
    plt.figure(figsize=(6, 4))
    plt.hist(df['bmi'], bins=20)
    plt.title('BMI Distribution')
    plt.xlabel('BMI')
    plt.ylabel('Rows')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Observation:** bell-shaped around a median of 30.1: half of the customers are obese (BMI ≥ 30).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Charges Distribution
    """)
    return


@app.cell
def _(df, plt):
    plt.figure(figsize=(6, 4))
    plt.hist(df['charges'], bins=30)
    plt.title('Insurance Charges Distribution')
    plt.xlabel('Charges (US $)')
    plt.ylabel('Rows')
    plt.show()
    df['charges'].value_counts().head(3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Observation:** right-skewed, with a long tail up to 61,974. And one value repeats far more than any other: **exactly 200.00, 76 times**,
    all non-smokers. A spike at a round number is usually a **default, a minimum fee or a placeholder**: ask the data owner before you use it.
    """)
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
    plt.ylabel('Rows')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Observation:** 3,169 male and 2,952 female rows; only the two expected values.
    """)
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
    plt.ylabel('Rows')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Observation:** not balanced: northeast **2,049** rows, southwest only 1,196. Only the four expected values, but 675 northeast rows
    are copies of rows from another region (step 6), so the northeast count is inflated.
    """)
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
    df.groupby('smoker')['charges'].agg(['count', 'mean', 'median']).round(0)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Observation:** smokers average **36,986**, non-smokers **12,274** (3.0×). The boxes do not even touch: 75% of non-smokers cost less than 16,358, and 75% of smokers more than 31,423.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 13. BMI vs Charges
    """)
    return


@app.cell
def _(df, plt):
    plt.figure(figsize=(6, 4))
    plt.scatter(df['bmi'], df['charges'], s=5)
    plt.title('BMI vs Charges')
    plt.xlabel('BMI')
    plt.ylabel('Charges (US $)')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Observation:** no clear line: BMI alone says little about charges (correlation 0.11, step 15).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 14. Average Charges by Region
    """)
    return


@app.cell
def _(con, df, plt):
    region_charges = con.execute("""
    SELECT region, COUNT(*) AS n_rows, ROUND(AVG(charges), 0) AS avg_charges
    FROM df
    GROUP BY region
    ORDER BY avg_charges DESC
    """).df()
    region_charges.plot(kind='bar', x='region', y='avg_charges', legend=False)
    plt.title('Average Charges by Region')
    plt.ylabel('Average charges (US $)')
    plt.show()
    region_charges
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Observation:** the northeast is the most expensive (**21,527**, the others 16,700–17,200). But this is **not** a regional effect yet:
    the 675 northeast copies (step 6) are 58% smokers, so they raise the northeast's smoker mix (analytical-thinking deck, habit 4).
    Fix the data first, then compare regions. (DuckDB can query the pandas DataFrame `df` by its name.)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 15. Correlation Matrix
    """)
    return


@app.cell
def _(df, plt, sns):
    corr = df[['age', 'bmi', 'children', 'charges']].corr(numeric_only=True)
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Observation:** with charges, `age` **0.32**, `bmi` 0.11, `children` 0.06. (`smoker` is not in the matrix, yet it is the biggest driver.)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Findings

    | Kind | Finding |
    |---|---|
    | Data quality | **222** exact duplicates; **675** pairs differing only in region (one copy always northeast); **76** charges of exactly 200.00; 2022 has ~250 fewer rows; no NULLs |
    | Distribution | charges right-skewed (median 14,816 < mean 18,455) |
    | Drivers | smoking (3.0×), then age (0.32); BMI alone weak (0.11) |
    | Segments | northeast "most expensive", but inflated by the region copies: not a finding until the data is fixed |

    Next: `3.EDA_comprehensive.py` turns these findings into Silver rules, and **Lab 2.2** follows the yearly averages.
    """)
    return


if __name__ == "__main__":
    app.run()
