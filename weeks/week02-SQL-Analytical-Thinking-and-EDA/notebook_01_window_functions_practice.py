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
    # Week 2 — Window Functions: 8 Practice Exercises
    ## Insurance data (goes with `lecture_notes_02_window_functions.md`)

    Same patterns as the slides, **different questions**. Each exercise: a question, an empty cell for your SQL,
    then the solution and the answer in numbers. Write your query first, then compare.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Load the Data

    DuckDB in memory (nothing is written to disk). `smoker` is BOOLEAN, so `WHERE smoker` / `NOT smoker` work directly.
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE insurance AS
        SELECT * FROM read_csv('../week01-Foundations-SQL-for-Analytics/example_1_insurance/insurance.csv');
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 1 — `OVER ()`: Compare with Everyone
    **Question:** Show `age`, `bmi`, `smoker`, `charges` and the **overall** average charges for the **5 customers with the highest BMI**, plus an index (`100 * charges / overall average`).
    Is a very high BMI enough to be expensive?
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
        SELECT age, bmi, smoker,
               ROUND(charges, 0)                          AS charges,
               ROUND(AVG(charges) OVER (), 0)             AS overall_avg,
               ROUND(100 * charges / AVG(charges) OVER ()) AS index_vs_all
        FROM insurance
        ORDER BY bmi DESC
        LIMIT 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** no. 4 of the 5 are **non-smokers** with an index of 9–86 (cheaper than average); only the smoker (age 22, BMI 52.58) costs 3.4× the average (index 335).
    The window is computed **before** `ORDER BY … LIMIT`, so the average is over all 1,338 customers.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 2 — `PARTITION BY`: Compare with Your Own Group
    **Question:** Compare each customer with the average of **their smoker group**. Show the 5 **non-smokers** who are furthest above the non-smoker average (`diff`). Use `QUALIFY` to keep only non-smokers.
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
        SELECT age, bmi, region,
               ROUND(charges, 0)                                           AS charges,
               ROUND(AVG(charges) OVER (PARTITION BY smoker), 0)           AS group_avg,
               ROUND(charges - AVG(charges) OVER (PARTITION BY smoker), 0) AS diff
        FROM insurance
        QUALIFY NOT smoker
        ORDER BY diff DESC
        LIMIT 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** the top non-smoker (age 59, southwest) costs **36,911**, 28,476 above the non-smoker average (8,434): expensive non-smokers exist, but they are rare.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 3 — Filter on a Window Result
    **Question:** Per smoker group: how many customers are **above their group's average**, out of how many?
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
               COUNT(*) FILTER (WHERE charges > group_avg) AS above_group_avg,
               COUNT(*)                                    AS customers
        FROM (SELECT smoker, charges,
                     AVG(charges) OVER (PARTITION BY smoker) AS group_avg
              FROM insurance)
        GROUP BY smoker
        ORDER BY smoker DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** smokers **150 of 274** (55%), non-smokers **462 of 1,064** (43%). The non-smoker average is pulled up by a few expensive customers, so fewer than half are above it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 4 — Share of the Total
    **Question:** For each 10-year age band (`FLOOR(age / 10) * 10`): the % of **customers** and the % of **charges**. Which bands cost more than their share?
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
        SELECT FLOOR(age / 10) * 10                                      AS age_band,
               COUNT(*)                                                  AS customers,
               ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)          AS pct_customers,
               ROUND(100 * SUM(charges) / SUM(SUM(charges)) OVER (), 1)  AS pct_charges
        FROM insurance
        GROUP BY age_band
        ORDER BY age_band
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** from 40 up, every band causes more than its share: the 60s are **8.5%** of customers but **13.6%** of charges; the under-20s are 10.2% of customers and only 6.5% of charges.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 5 — `RANK` vs `DENSE_RANK` with a Tie
    **Question:** Rank the regions by their **number of smokers** (most first) with both `RANK()` and `DENSE_RANK()`. Where do they differ?
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
               COUNT(*) FILTER (WHERE smoker)                                  AS smokers,
               RANK()       OVER (ORDER BY COUNT(*) FILTER (WHERE smoker) DESC) AS rank,
               DENSE_RANK() OVER (ORDER BY COUNT(*) FILTER (WHERE smoker) DESC) AS dense_rank
        FROM insurance
        GROUP BY region
        ORDER BY smokers DESC, region
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** northwest and southwest tie with **58** smokers, so both get rank 3 in both columns. They would differ only for a region **after** the tie: `RANK` would give it 5, `DENSE_RANK` 4.
    A window over a `GROUP BY` result works: the window runs **after** the grouping.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 6 — Top-N per Group
    **Question:** The **most expensive customer** for each number of `children` (one row per value, 0–5).
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
        SELECT children, age, smoker,
               ROUND(charges, 0) AS charges
        FROM insurance
        QUALIFY ROW_NUMBER() OVER (PARTITION BY children ORDER BY charges DESC) = 1
        ORDER BY children
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** all 6 are **smokers**. The most expensive overall (63,770) has no children; the top customer with 5 children costs only 19,023 (but that group has just 18 customers).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 7 — Running Total on the Right Grain
    **Question:** One row per number of `children`: customers, a **running total** of customers and a **running %** (ordered by `children`).
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
        SELECT children,
               COUNT(*)                                                       AS customers,
               SUM(COUNT(*)) OVER (ORDER BY children)                         AS running_customers,
               ROUND(100 * SUM(COUNT(*)) OVER (ORDER BY children)
                         / SUM(COUNT(*)) OVER (), 1)                          AS running_pct
        FROM insurance
        GROUP BY children
        ORDER BY children
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** **85.1%** of customers have 2 children or fewer; only 43 customers (3.2%) have 4 or 5.
    We grouped **first** (one row per `children` value), so the running total has no ties.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 8 — `LAG`: Change from the Previous Step
    **Question:** Average charges per 10-year age band, the change vs the **previous** band, and that change in %.
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
        SELECT FLOOR(age / 10) * 10                                                     AS age_band,
               ROUND(AVG(charges), 0)                                                   AS avg_charges,
               ROUND(AVG(charges) - LAG(AVG(charges)) OVER (ORDER BY age_band), 0)      AS change,
               ROUND(100 * (AVG(charges) / LAG(AVG(charges)) OVER (ORDER BY age_band) - 1), 1) AS pct_change
        FROM insurance
        GROUP BY age_band
        ORDER BY age_band
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** every band costs more than the one before; the biggest step is from the 50s to the 60s: **+4,753 (+28.8%)**. The first band has no previous row, so its change is NULL.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reflection

    - Exercises 1 and 2: why does the same customer look "expensive" against one baseline and "normal" against another?
    - Exercise 5: when would you **want** `DENSE_RANK` instead of `RANK` in a report?
    - Exercises 7 and 8 group **first**. What goes wrong if you run a running total over the 1,338 customer rows ordered by `age`?
    """)
    return


if __name__ == "__main__":
    app.run()
