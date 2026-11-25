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
    # Week 1 — SQL Foundations: 8 Exercises
    ## Insurance data (goes with `lecture_notes_01_sql_for_analytics.md`)

    Each exercise has a **question**, an **empty cell** for your SQL, then the **solution** and the **answer** in numbers.
    Write your query first, then compare.
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


if __name__ == "__main__":
    app.run()
