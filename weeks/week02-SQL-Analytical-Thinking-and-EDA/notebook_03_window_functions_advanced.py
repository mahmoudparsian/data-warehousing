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
    # Week 2 — Window Functions, Advanced (with Charts)

    Optional, after `lecture_notes_02_window_functions.md` and `notebook_01_window_functions_practice.py`. Four analyses that need
    **more than one** window idea at once. Each section: question → SQL → chart → insight with numbers.

    | # | Question | Windows used |
    |---|---|---|
    | 1 | How does cost change with age, once the noise is smoothed? | `AVG … ROWS BETWEEN`, `LAG` |
    | 2 | How concentrated is the cost, and who is in the expensive deciles? | `NTILE`, `SUM(SUM()) OVER` |
    | 3 | Where does a typical smoker sit among all customers? | `PERCENT_RANK` |
    | 4 | Is a region expensive, or does it just have more smokers? | `AVG(…) OVER ()`, `FILTER` (mix effect) |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup

    DuckDB in memory (nothing is written to disk); `con.execute(...).df()` returns a pandas DataFrame for the charts.
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
    con.execute("SELECT * FROM insurance LIMIT 5").df()
    return con, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Cost by Age: Moving Average and Change

    One row per age **first** (`GROUP BY age`), then the windows: the ages are unique, so "previous row" and "last 3 rows" are well defined.
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT age,
           AVG(charges)                                         AS avg_charges,
           AVG(AVG(charges)) OVER (ORDER BY age
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)       AS moving_avg_3,
           AVG(charges) - LAG(AVG(charges)) OVER (ORDER BY age) AS change_vs_prev_age
    FROM insurance
    GROUP BY age
    ORDER BY age
    """).df()

    _fig, (_ax1, _ax2) = plt.subplots(2, 1, figsize=(8, 7), sharex=True)
    _ax1.plot(_df['age'], _df['avg_charges'], marker='.', label='average per age')
    _ax1.plot(_df['age'], _df['moving_avg_3'], linewidth=3, label='3-age moving average')
    _ax1.set_ylabel("Charges (US $)")
    _ax1.legend()
    _ax1.set_title("Average Charges by Age")
    _ax2.bar(_df['age'], _df['change_vs_prev_age'])
    _ax2.axhline(0, color='black')
    _ax2.set_xlabel("Age")
    _ax2.set_ylabel("Change vs previous age")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Insight:** single ages jump by thousands up **and** down (each age has only 22–69 customers); the moving average climbs
    from about 8,400 at 18–19 to about 21,000 in the 60s. Report the smoothed line, not the jumps.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Deciles: How Concentrated Is the Cost, and Who Causes It?

    `NTILE(10)` puts the customers, most expensive first, into 10 groups of ~134.
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT decile,
           COUNT(*)                                                    AS customers,
           COUNT(*) FILTER (WHERE smoker)                              AS smokers,
           100 * SUM(charges) / SUM(SUM(charges)) OVER ()              AS pct_of_charges,
           100 * SUM(SUM(charges)) OVER (ORDER BY decile)
               / SUM(SUM(charges)) OVER ()                             AS cumulative_pct
    FROM (SELECT charges, smoker,
                 NTILE(10) OVER (ORDER BY charges DESC) AS decile
          FROM insurance)
    GROUP BY decile
    ORDER BY decile
    """).df()

    _fig, _ax = plt.subplots(figsize=(8, 4))
    _ax.bar(_df['decile'], _df['pct_of_charges'], label='% of charges')
    _ax.plot(_df['decile'], _df['cumulative_pct'], color='black', marker='o', label='cumulative %')
    _ax.set_xticks(range(1, 11))
    _ax.set_xlabel("Decile (1 = most expensive 10%)")
    _ax.set_ylabel("% of all charges")
    _ax.legend()
    plt.title("Share of Charges by Decile")
    plt.show()
    _df[['decile', 'customers', 'smokers']]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Insight:** decile 1 causes **32%** of all charges and holds **131 smokers out of 134**. All **274** smokers are in the
    4 most expensive deciles; the cheapest **60%** of customers contain **no smoker at all**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Where Does a Typical Smoker Sit?

    `PERCENT_RANK()` = the share of customers who are cheaper than this one (0 = cheapest, 1 = most expensive).
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT smoker,
           PERCENT_RANK() OVER (ORDER BY charges) AS pct_rank
    FROM insurance
    """).df()

    plt.figure()
    for _value, _label in [(False, 'non-smoker'), (True, 'smoker')]:
        plt.hist(100 * _df[_df['smoker'] == _value]['pct_rank'], bins=20, alpha=0.6, label=_label)
    plt.xlabel("Percentile among all customers (100 = most expensive)")
    plt.ylabel("Customers")
    plt.legend()
    plt.title("Percentile Rank of Charges")
    plt.show()
    con.execute("""
    SELECT smoker, ROUND(100 * MEDIAN(pct_rank), 1) AS median_percentile
    FROM (SELECT smoker, PERCENT_RANK() OVER (ORDER BY charges) AS pct_rank FROM insurance)
    GROUP BY smoker
    ORDER BY smoker DESC
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Insight:** the typical smoker is more expensive than **89.6%** of all customers; the typical non-smoker sits at the
    **39.8th** percentile. The window runs over **all** customers, and only then do we split by `smoker`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Mix Effect: Expensive Region or More Smokers?

    The **same-mix average** gives every region the overall smoker share (from `AVG(smoker::INTEGER) OVER ()`).
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    WITH r AS (
      SELECT region,
             AVG(charges)                           AS avg_charges,
             AVG(charges) FILTER (WHERE smoker)     AS avg_smokers,
             AVG(charges) FILTER (WHERE NOT smoker) AS avg_non_smokers,
             SUM(smoker::INTEGER)                   AS smokers,
             COUNT(*)                               AS customers
      FROM insurance
      GROUP BY region
    )
    SELECT region,
           ROUND(100.0 * smokers / customers, 1)                              AS pct_smokers,
           ROUND(avg_charges, 0)                                              AS avg_charges,
           ROUND(share * avg_smokers + (1 - share) * avg_non_smokers, 0)      AS same_mix_avg
    FROM (SELECT *, SUM(smokers) OVER () / SUM(customers) OVER () AS share FROM r)
    ORDER BY avg_charges DESC
    """).df()

    _x = range(len(_df))
    plt.figure(figsize=(8, 4))
    plt.bar([i - 0.2 for i in _x], _df['avg_charges'], width=0.4, label='actual average')
    plt.bar([i + 0.2 for i in _x], _df['same_mix_avg'], width=0.4, label='same smoker mix')
    plt.xticks(list(_x), _df['region'])
    plt.ylim(11000, 15500)
    plt.ylabel("Average charges (US $)")
    plt.legend()
    plt.title("Regions: Actual vs Same-Mix Average")
    plt.show()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Insight:** the southeast has the most smokers (**25%**). With the same smoker mix everywhere, the gap between the most and
    least expensive region shrinks from about **2,400 to about 540**: most of the regional difference is a **mix effect**.
    (The y-axis starts at 11,000 to make the gaps visible: read the numbers, not the bar heights.)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    | Analysis | Finding |
    |---|---|
    | Age | cost climbs from ~8,400 (18–19) to ~21,000 (60s); single ages are noisy |
    | Deciles | top 10% → 32% of charges; all smokers are in the top 40% |
    | Percentile | typical smoker: 89.6th percentile; typical non-smoker: 39.8th |
    | Regions | mostly a smoker-mix effect, not a regional one |
    """)
    return


if __name__ == "__main__":
    app.run()
