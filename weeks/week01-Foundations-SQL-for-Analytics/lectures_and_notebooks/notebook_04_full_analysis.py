import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🧠 Week 1 — SQL Foundations, All in One (optional)

    ## Insurance Dataset — the Full Analytical Journey

    Raw data → question → SQL → pattern → insight → decision. Three parts in one notebook:

    | Part | Same as | What you do |
    |---|---|---|
    | 1. EDA story | `notebook_01_insurance_first_look.py` | look at the data with pandas charts; form a hypothesis |
    | 2. SQL exercises | `notebook_02_sql_exercises.py` | 8 questions, each with a solution and the answer in numbers |
    | 3. Final analysis | (only here) | age and BMI charts from SQL, then a business summary |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 1 — EDA Story (pandas)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Data

    ```
    % head ../example_1_insurance/insurance.csv
    age,gender,bmi,children,smoker,region,charges
    19,female,27.9,0,yes,southwest,16884.924
    18,male,33.77,1,no,southeast,1725.5523
    28,male,33,3,no,southeast,4449.462
    33,male,22.705,0,no,northwest,21984.47061
    32,male,28.88,0,no,northwest,3866.8552
    31,female,25.74,0,no,southeast,3756.6216
    46,female,33.44,1,no,southeast,8240.5896
    37,female,27.74,3,no,northwest,7281.5056
    37,male,29.83,2,no,northeast,6406.4107
    ```

    One row per insured customer; `charges` = the yearly medical cost billed by the insurer (US $).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1 — Load Data
    """)
    return


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import duckdb

    df = pd.read_csv('../example_1_insurance/insurance.csv')
    df.head()
    return df, duckdb, plt


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
    **Observation:** 1,338 rows, no missing values. Ages 18–64. `charges` goes from about 1,100 to 63,800:
    a **mean of 13,270** but a **median (50%) of 9,382**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 3 — Distribution of Charges
    """)
    return


@app.cell
def _(df, plt):
    df['charges'].hist(bins=30)
    plt.title('Distribution of Charges')
    plt.xlabel('Charges (US $)')
    plt.ylabel('Customers')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Observation:** the distribution is **right-skewed**: about 3 in 4 customers (73%) cost under 15,000, and a long tail of expensive customers
    pulls the mean (13,270) 41% above the median (9,382). For a "typical customer", report the **median**.
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
    **Observation:** the box holds the middle half of the customers (about 4,700 to 16,600). The dots above the top whisker
    (charges above about 34,500) are **139 customers**: are they random, or do they share something?
    """)
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
    plt.ylabel('Average charges (US $)')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Insight:** smokers average **32,050**, non-smokers **8,434**: smokers cost **3.8×** as much.
    And the 139 outliers from Step 4? **136 of them are smokers.**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 6 — The Same Question in SQL (DuckDB)

    `con.register` lets SQL read the pandas DataFrame `df` as a table. In pandas, `smoker` is the text `'yes'` / `'no'`
    (DuckDB's own `read_csv` would make it BOOLEAN, as in the slides).
    """)
    return (con,)


@app.cell
def _(df, duckdb):
    con = duckdb.connect()
    con.register('insurance', df)

    con.execute("""
    SELECT smoker,
           COUNT(*)               AS customers,
           ROUND(AVG(charges), 0) AS avg_charges
    FROM insurance
    GROUP BY smoker
    ORDER BY avg_charges DESC
    """).df()
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Same answer** as the chart: 274 smokers at 32,050, 1,064 non-smokers at 8,434.
    Next: Part 2 checks this with a **second dimension** (region × smoker).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 2 — SQL Exercises (DuckDB, `mo.sql`)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Load the Data

    DuckDB in memory (nothing is written to disk). `smoker` is read as **BOOLEAN** (`true` / `false`), so `WHERE smoker` means "smokers only" (`smoker = 'yes'` also works: DuckDB converts `'yes'` to `true`).
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE insurance
        AS
        SELECT * FROM read_csv('../example_1_insurance/insurance.csv');
        """
    )
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM insurance LIMIT 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 1 — Exploration
    **Question:** Which columns does the table have, and what is the **type** of each one? Which type surprises you?
    """)
    return


@app.cell
def _():
    # Write your SQL below
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Solution
    """)
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql(
        f"""
        DESCRIBE insurance
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** 7 columns. The CSV says `yes` / `no`, but `smoker` is **BOOLEAN**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 2 — High-Cost Customers
    **Question:** Show the 10 most expensive customers (`age`, `gender`, `bmi`, `smoker`, `region`, `charges` rounded to whole dollars).
    What do they have in common?
    """)
    return


@app.cell
def _():
    # Write your SQL below
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Solution
    """)
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql(
        f"""
        SELECT age, gender, bmi, smoker, region,
               ROUND(charges, 0) AS charges
        FROM insurance
        ORDER BY charges DESC
        LIMIT 10
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** all 10 are **smokers**, and all 10 have a BMI above 30. That is a hypothesis (10 rows of 1,338): Exercise 3 tests it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 3 — Test the Hypothesis
    **Question:** Do smokers pay more? Show, per `smoker` value, the number of customers and the average charges (whole dollars).
    """)
    return


@app.cell
def _():
    # Write your SQL below
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Solution
    """)
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql(
        f"""
        SELECT smoker,
               COUNT(*)               AS customers,
               ROUND(AVG(charges), 0) AS avg_charges
        FROM insurance
        GROUP BY smoker
        ORDER BY avg_charges DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** 274 smokers average **32,050**, 1,064 non-smokers **8,434**: smokers cost **3.8×** as much.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 4 — Regional Analysis
    **Question:** Which region has the highest average charges? Show `region`, number of customers and average charges, highest first.
    """)
    return


@app.cell
def _():
    # Write your SQL below
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Solution
    """)
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql(
        f"""
        SELECT region,
               COUNT(*)               AS customers,
               ROUND(AVG(charges), 0) AS avg_charges
        FROM insurance
        GROUP BY region
        ORDER BY avg_charges DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** the **southeast** (14,735). The gap between regions (about 2,400) is small next to the smoker gap (about 23,600).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 5 — Two Dimensions
    **Question:** Show the average charges for every **region × smoker** pair (with the number of customers).
    Is the southeast expensive for **non-smokers** too?
    """)
    return


@app.cell
def _():
    # Write your SQL below
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Solution
    """)
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql(
        f"""
        SELECT region, -- dimension 1
               smoker, -- dimension 2
               COUNT(*)               AS customers,
               ROUND(AVG(charges), 0) AS avg_charges
        FROM insurance
        GROUP BY region, smoker
        ORDER BY smoker DESC, avg_charges DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** no. Southeast non-smokers average **8,032**, among the cheapest. The southeast's high average comes from having the **most smokers** (91).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 6 — The High-Risk Segment
    **Question:** How many customers are smokers **and** obese (BMI 30 or more), and what are their average charges?
    """)
    return


@app.cell
def _():
    # Write your SQL below
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Solution
    """)
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql(
        f"""
        SELECT COUNT(*)               AS customers,
               ROUND(AVG(charges), 0) AS avg_charges
        FROM insurance
        WHERE smoker AND bmi >= 30
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** **145** customers average **41,558**, about 5× a non-smoker (8,434).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 7 — Distribution
    **Question:** How many customers live in each region? Are the regions balanced?
    """)
    return


@app.cell
def _():
    # Write your SQL below
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Solution
    """)
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql(
        f"""
        SELECT region,
               COUNT(*) AS customers
        FROM insurance
        GROUP BY region
        ORDER BY customers DESC, region
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** almost balanced: southeast **364**, the other three 324–325. So a region's **total** charges mostly follow its average, not its size.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 8 — Business Insight
    **Question:** Which **smoker × region** segments cost the most **in total**? Show the top 4 with customers, average and total charges.
    """)
    return


@app.cell
def _():
    # Write your SQL below
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Solution
    """)
    return


@app.cell
def _(insurance, mo):
    _df = mo.sql(
        f"""
        SELECT smoker, region,
               COUNT(*)               AS customers,
               ROUND(AVG(charges), 0) AS avg_charges,
               ROUND(SUM(charges), 0) AS total_charges
        FROM insurance
        GROUP BY smoker, region
        ORDER BY total_charges DESC
        LIMIT 4
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** just **91 southeast smokers** (7% of customers) cost **3,170,895** in total, more than any group of ~260 non-smokers.
    Pricing should focus on **smoking** first; region matters much less.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reflection Questions

    - Which variable drives cost the most? Give the number that shows it.
    - Exercise 4 vs 5: why can a one-dimension result mislead you?
    - If you ran this insurer, what **one** pricing rule would you write, and which query supports it?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 3 — Final Analysis: What Drives Cost?

    Two charts from SQL (on the `con` connection from Part 1), then the business summary.
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT age,
           AVG(charges) AS avg_charges
    FROM insurance
    GROUP BY age
    ORDER BY age
    """).df()

    plt.figure()
    plt.plot(_df['age'], _df['avg_charges'])
    plt.title("Average Charges by Age")
    plt.xlabel("Age")
    plt.ylabel("Average charges (US $)")
    plt.grid()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Insight
    Charges rise steadily with age (correlation **0.30**): customers in their 60s average **21,248**, about **2.5×** the 18–19-year-olds (8,407).
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT bmi, charges, smoker
    FROM insurance
    """).df()

    plt.figure()
    for _value, _label in [('no', 'non-smoker'), ('yes', 'smoker')]:
        _part = _df[_df['smoker'] == _value]
        plt.scatter(_part['bmi'], _part['charges'], s=10, label=_label)
    plt.axvline(30, linestyle='--', color='gray')
    plt.title("BMI vs Charges, by Smoker")
    plt.xlabel("BMI (dashed line: 30 = obese)")
    plt.ylabel("Charges (US $)")
    plt.legend()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Insight
    BMI alone is a weak signal (correlation **0.20**), but **together with smoking** it is the strongest one:
    smokers with BMI 30+ (right of the dashed line) average **41,558**, about 5× a non-smoker (8,434).
    BMI 30+ nearly **doubles** a smoker's cost (21,363 → 41,558) but adds only 11% for a non-smoker (7,977 → 8,843).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🎯 Final Business Summary

    | Driver | Evidence |
    |---|---|
    | **Smoking** | 32,050 vs 8,434 on average (3.8×); 136 of the 139 most expensive outliers smoke |
    | **Smoking + BMI 30+** | 145 customers average 41,558 |
    | **Age** | 60s average 2.5× the 18–19-year-olds |
    | Region | only 12,347–14,735; the southeast is high because it has the most smokers |

    **Actions:** risk-based pricing (smoking first, then age), and preventive programs (quit smoking, weight) aimed at smokers with BMI 30+.
    """)
    return


if __name__ == "__main__":
    app.run()
