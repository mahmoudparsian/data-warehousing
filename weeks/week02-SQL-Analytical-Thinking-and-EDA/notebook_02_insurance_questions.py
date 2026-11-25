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
    # Insurance Questions: Question → SQL → Chart → Insight

    Ten business questions on the week 1 insurance data (1,338 customers). Each one: the **question**, the **SQL** (window functions
    from `lecture_notes_02_window_functions.md`), a **chart**, and the **insight with its numbers**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Connect and Load

    DuckDB in memory; `con.execute(...).df()` returns a pandas DataFrame for the charts.
    """)
    return


@app.cell
def _():
    import duckdb
    import matplotlib.pyplot as plt

    con = duckdb.connect()
    con.execute("""
    CREATE OR REPLACE TABLE insurance AS
    SELECT * FROM read_csv('../week01-Foundations-SQL-for-Analytics/example_1_insurance/insurance.csv')
    """).fetchall()
    con.execute("SELECT COUNT(*) AS customers FROM insurance").df()
    return con, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Who Are the 3 Most Expensive Customers in Each Region?
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT region, age, smoker, ROUND(charges, 0) AS charges,
           RANK() OVER (PARTITION BY region ORDER BY charges DESC) AS rnk
    FROM insurance
    QUALIFY rnk <= 3
    ORDER BY region, rnk
    """).df()

    plt.figure(figsize=(10, 4))
    plt.bar(_df['region'] + ' #' + _df['rnk'].astype(str), _df['charges'])
    plt.xticks(rotation=60)
    plt.title("Top 3 Charges per Region")
    plt.ylabel("Charges (US $)")
    plt.tight_layout()
    plt.show()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Insight:** all **12** are smokers. Each region's top 3 cost 47,500–63,800, 3.6–4.8× the average customer (13,270).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. How Far Is Each Customer from Their Region's Average?
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT region, charges,
           charges - AVG(charges) OVER (PARTITION BY region) AS diff_from_region
    FROM insurance
    """).df()

    plt.figure()
    plt.hist(_df['diff_from_region'], bins=40)
    plt.axvline(0, color='black', linestyle='--')
    plt.title("Charges minus the Regional Average")
    plt.xlabel("Difference (US $); left of the line = below average")
    plt.ylabel("Customers")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Insight:** **68%** of customers are **below** their region's average; a long tail of expensive customers (right) pulls each average up.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. How Many Customers Are Above Their Regional Average?
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT region, COUNT(*) AS above_avg
    FROM (SELECT region, charges,
                 AVG(charges) OVER (PARTITION BY region) AS regional_avg
          FROM insurance)
    WHERE charges > regional_avg
    GROUP BY region
    ORDER BY region
    """).df()

    plt.figure()
    plt.bar(_df['region'], _df['above_avg'])
    plt.title("Customers Above Their Regional Average")
    plt.ylabel("Customers")
    plt.show()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Insight:** 97–116 customers per region, **428 of 1,338** in total (32%): about one in three.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Pareto: What Share of All Charges Comes from the Most Expensive Customers?
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT 100.0 * ROW_NUMBER() OVER (ORDER BY charges DESC) / COUNT(*) OVER ()       AS pct_customers,
           100.0 * SUM(charges) OVER (ORDER BY charges DESC
                                      ROWS UNBOUNDED PRECEDING) / SUM(charges) OVER () AS cumulative_pct_charges
    FROM insurance
    ORDER BY pct_customers
    """).df()

    plt.figure()
    plt.plot(_df['pct_customers'], _df['cumulative_pct_charges'])
    plt.plot([0, 100], [0, 100], linestyle='--', color='gray')
    plt.title("Pareto Curve of Charges")
    plt.xlabel("% of customers (most expensive first)")
    plt.ylabel("Cumulative % of all charges")
    plt.grid()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Insight:** the most expensive **10%** of customers cause **32%** of all charges, the top **20%** more than **half** (51.7%).
    The dashed line is "everyone costs the same". `ROWS UNBOUNDED PRECEDING` makes the running sum go row by row, even when two charges are equal.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Running Total of Charges by Age
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT age,
           SUM(charges)                                                    AS total_charges,
           100 * SUM(SUM(charges)) OVER (ORDER BY age) / SUM(SUM(charges)) OVER () AS running_pct
    FROM insurance
    GROUP BY age
    ORDER BY age
    """).df()

    plt.figure()
    plt.plot(_df['age'], _df['running_pct'])
    plt.axhline(50, linestyle='--', color='gray')
    plt.title("Running % of All Charges by Age")
    plt.xlabel("Age")
    plt.ylabel("Running % of charges")
    plt.grid()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Insight:** half of all charges come from customers aged **18–45**, the other half from ages 46–64 (fewer years, higher cost per customer).
    We grouped by age **first**, so there is one row per age and the running total has no ties.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Do Smokers Pay More?
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT CASE WHEN smoker THEN 'smoker' ELSE 'non-smoker' END AS smoker,
           COUNT(*)               AS customers,
           ROUND(AVG(charges), 0) AS avg_charges
    FROM insurance
    GROUP BY ALL
    ORDER BY avg_charges DESC
    """).df()

    plt.figure()
    plt.bar(_df['smoker'], _df['avg_charges'])
    plt.title("Average Charges: Smokers vs Non-Smokers")
    plt.ylabel("Average charges (US $)")
    plt.show()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Insight:** smokers average **32,050**, non-smokers **8,434**: **3.8×**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. BMI vs Charges, by Smoker
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("SELECT bmi, charges, smoker FROM insurance").df()

    plt.figure()
    for _value, _label in [(False, 'non-smoker'), (True, 'smoker')]:
        _part = _df[_df['smoker'] == _value]
        plt.scatter(_part['bmi'], _part['charges'], s=10, label=_label)
    plt.axvline(30, linestyle='--', color='gray')
    plt.title("BMI vs Charges")
    plt.xlabel("BMI (dashed line: 30 = obese)")
    plt.ylabel("Charges (US $)")
    plt.legend()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Insight:** for **smokers**, crossing BMI 30 nearly doubles the cost (21,363 → 41,558); for non-smokers, BMI changes little (7,977 → 8,843).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Do Smokers Have a Different BMI?
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("SELECT smoker, bmi FROM insurance").df()

    plt.figure()
    for _value, _label in [(False, 'non-smoker'), (True, 'smoker')]:
        plt.hist(_df[_df['smoker'] == _value]['bmi'], bins=30, alpha=0.5, density=True, label=_label)
    plt.legend()
    plt.title("BMI Distribution by Smoker")
    plt.xlabel("BMI")
    plt.ylabel("Share of the group")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Insight:** no: both groups average a BMI of **30.7**. Smoking and BMI are independent here, so the high cost of
    "smoker **and** obese" (question 8) is the **combination**, not one factor hiding behind the other.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Summary

    | Question | Answer |
    |---|---|
    | Top customers | the top 3 of every region are smokers |
    | Typical vs average | 68% of customers are below their region's average |
    | Concentration | top 10% → 32% of charges; top 20% → 51.7% |
    | Smoking | 3.8× the cost; with BMI 30+ about 5× |
    | BMI | matters only together with smoking |
    """)
    return


if __name__ == "__main__":
    app.run()
