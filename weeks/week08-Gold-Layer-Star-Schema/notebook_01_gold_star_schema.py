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
    # Week 8 — Gold: a Star Schema on Week 7's Insurance Silver

    The steps of [slides 1](lecture_notes_01_gold_modeling.md), with charts: questions → grain → dimensions → fact → validation → marts → answers.
    Input: week 7's `silver.insurance` (5,197 policy-years, 2021–2024), rebuilt by [`insurance_silver_week07.sql`](insurance_silver_week07.sql).

    Business questions:
    1. Which regions and profiles cost the most per policy-holder?
    2. How do smokers' charges compare, by age band?
    3. How do charges change from 2021 to 2024?
    """)
    return


@app.cell
def _():
    import duckdb
    import matplotlib.pyplot as plt

    con = duckdb.connect()   # in memory: nothing is written to disk
    con.execute(open("insurance_silver_week07.sql").read())

    def q(sql):
        return con.execute(sql).df()

    q("SELECT year, COUNT(*) AS silver_rows, COUNT(*) FILTER (WHERE is_region_unknown OR is_smoker_unknown OR is_gender_unknown) AS flagged FROM silver.insurance GROUP BY 1 ORDER BY 1")
    return con, plt, q


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 1 — Grain: One Row = One Policy-Holder in One Year

    Test it: the number of rows must equal the number of distinct grain values. No customer id exists, so the fact will get a surrogate key.
    """)
    return


@app.cell
def _(q):
    q("""
    SELECT COUNT(*) AS rows,
           COUNT(DISTINCT (year, age, gender, bmi, children, smoker, region, charges)) AS distinct_grain_values
    FROM silver.insurance
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### What a grain error does

    One copy of every 2024 smoker (as if Silver had not deduplicated): no error, just bigger numbers.
    """)
    return


@app.cell
def _(q):
    q("""
    WITH with_copies AS (
        SELECT * FROM silver.insurance
        UNION ALL
        SELECT * FROM silver.insurance WHERE year = 2024 AND smoker = 'yes'
    )
    SELECT 'correct grain' AS version, COUNT(*) AS rows, SUM(charges) AS total_charges_2024
    FROM silver.insurance WHERE year = 2024
    UNION ALL
    SELECT 'smokers copied', COUNT(*), SUM(charges) FROM with_copies WHERE year = 2024
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 2 — Dimensions (with an `unknown` Member)
    """)
    return


@app.cell
def _(con, q):
    con.execute("""
    CREATE SCHEMA IF NOT EXISTS gold;

    CREATE OR REPLACE TABLE gold.dim_region AS
    SELECT ROW_NUMBER() OVER (ORDER BY region = 'unknown', region) AS region_key, region
    FROM (SELECT DISTINCT region FROM silver.insurance);

    CREATE OR REPLACE TABLE gold.dim_smoker AS
    SELECT ROW_NUMBER() OVER (ORDER BY smoker = 'unknown', smoker) AS smoker_key, smoker
    FROM (SELECT DISTINCT smoker FROM silver.insurance);

    CREATE OR REPLACE TABLE gold.dim_age_band AS SELECT * FROM (VALUES
        (1, '18-29', 18, 29), (2, '30-44', 30, 44), (3, '45-59', 45, 59), (4, '60+', 60, 100)) t(age_band_key, age_band, age_from, age_to);
    """)
    q("""
    SELECT 'dim_region' AS dim, region_key AS key, region AS value FROM gold.dim_region
    UNION ALL SELECT 'dim_smoker', smoker_key, smoker FROM gold.dim_smoker
    UNION ALL SELECT 'dim_age_band', age_band_key, age_band FROM gold.dim_age_band
    ORDER BY dim, key
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 3 — The Fact Table and Its Validation
    """)
    return


@app.cell
def _(con, q):
    con.execute("""
    CREATE OR REPLACE TABLE gold.fact_policy_year AS
    SELECT ROW_NUMBER() OVER (ORDER BY s.year, s.age, s.gender, s.bmi, s.children, s.smoker, s.region, s.charges) AS policy_year_key,
           s.year, r.region_key, k.smoker_key, a.age_band_key,
           s.gender, s.age, s.bmi, s.children, s.charges,
           s.is_region_unknown OR s.is_smoker_unknown OR s.is_gender_unknown AS is_flagged
    FROM silver.insurance s
    JOIN gold.dim_region   r ON r.region = s.region
    JOIN gold.dim_smoker   k ON k.smoker = s.smoker
    JOIN gold.dim_age_band a ON s.age BETWEEN a.age_from AND a.age_to;
    """)
    q("""
    SELECT 'rows: fact = silver' AS test,
           (SELECT COUNT(*) FROM gold.fact_policy_year) = (SELECT COUNT(*) FROM silver.insurance) AS passed
    UNION ALL SELECT 'charges: fact = silver',
           (SELECT SUM(charges) FROM gold.fact_policy_year) = (SELECT SUM(charges) FROM silver.insurance)
    UNION ALL SELECT 'no NULL foreign keys',
           (SELECT COUNT(*) FROM gold.fact_policy_year WHERE region_key IS NULL OR smoker_key IS NULL OR age_band_key IS NULL) = 0
    UNION ALL SELECT 'surrogate key unique',
           (SELECT COUNT(DISTINCT policy_year_key) FROM gold.fact_policy_year) = (SELECT COUNT(*) FROM gold.fact_policy_year)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 4 — Marts: Additive Parts, Declared Grain, Checked Against the Fact
    """)
    return


@app.cell
def _(con, q):
    con.execute("""
    CREATE OR REPLACE TABLE gold.mart_region_year AS              -- grain: region × year (regional managers)
    SELECT f.year, r.region, COUNT(*) AS policy_years, SUM(f.charges) AS total_charges,
           COUNT(*) FILTER (WHERE k.smoker = 'yes') AS smokers
    FROM gold.fact_policy_year f
    JOIN gold.dim_region r USING (region_key) JOIN gold.dim_smoker k USING (smoker_key)
    GROUP BY ALL;

    CREATE OR REPLACE TABLE gold.mart_profile AS                  -- grain: smoker × age band (pricing team)
    SELECT k.smoker, a.age_band_key, a.age_band, COUNT(*) AS policy_years, SUM(f.charges) AS total_charges
    FROM gold.fact_policy_year f
    JOIN gold.dim_smoker k USING (smoker_key) JOIN gold.dim_age_band a USING (age_band_key)
    GROUP BY ALL;
    """)
    q("""
    SELECT 'mart_region_year' AS mart, COUNT(*) AS mart_rows,
           SUM(total_charges) = (SELECT SUM(charges) FROM gold.fact_policy_year) AS charges_match,
           SUM(policy_years)  = (SELECT COUNT(*)     FROM gold.fact_policy_year) AS rows_match
    FROM gold.mart_region_year
    UNION ALL
    SELECT 'mart_profile', COUNT(*),
           SUM(total_charges) = (SELECT SUM(charges) FROM gold.fact_policy_year),
           SUM(policy_years)  = (SELECT COUNT(*)     FROM gold.fact_policy_year)
    FROM gold.mart_profile
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 1 — Which Regions Cost the Most per Policy-Holder?
    """)
    return


@app.cell
def _(q):
    by_region = q("""
    SELECT region, SUM(policy_years)::BIGINT AS policy_years,
           ROUND(SUM(total_charges) / SUM(policy_years), 2) AS avg_charges,
           ROUND(SUM(smokers) / SUM(policy_years), 3)       AS smoker_share
    FROM gold.mart_region_year GROUP BY 1 ORDER BY avg_charges DESC
    """)
    by_region
    return (by_region,)


@app.cell
def _(by_region, plt):
    _fig, _ax = plt.subplots(figsize=(8, 4))
    _ax.bar(by_region["region"], by_region["avg_charges"],
            color=["tab:red" if r == "unknown" else "tab:blue" for r in by_region["region"]])
    _ax.set_title("Average charges per policy-year, by region (2021–2024)")
    _ax.set_ylabel("charges ($)")
    plt.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The four real regions are within about $850 of each other ($16,676–$17,514). The `unknown` region is far higher ($25,961) because 53% of its
    policy-holders smoke: region is not what drives cost. The ratio is computed **from the parts** in the mart (sum ÷ count), never by averaging averages.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 2 — Smokers vs Non-Smokers, by Age Band
    """)
    return


@app.cell
def _(q):
    profile = q("""
    PIVOT (SELECT age_band_key, age_band, smoker, ROUND(total_charges / policy_years) AS avg_charges
           FROM gold.mart_profile WHERE smoker <> 'unknown')
    ON smoker USING FIRST(avg_charges)
    ORDER BY age_band_key
    """)
    profile
    return (profile,)


@app.cell
def _(plt, profile):
    _fig, _ax = plt.subplots(figsize=(8, 4))
    _x = range(len(profile))
    _ax.bar([i - 0.2 for i in _x], profile["no"], width=0.4, label="non-smoker")
    _ax.bar([i + 0.2 for i in _x], profile["yes"], width=0.4, label="smoker")
    _ax.set_xticks(list(_x), profile["age_band"])
    _ax.set_title("Average charges by age band and smoker status")
    _ax.legend()
    plt.tight_layout()
    _fig
    return


@app.cell
def _(q):
    q("""
    SELECT age_band,
           ROUND(SUM(total_charges) FILTER (WHERE smoker = 'yes') / SUM(policy_years) FILTER (WHERE smoker = 'yes')
               - SUM(total_charges) FILTER (WHERE smoker = 'no')  / SUM(policy_years) FILTER (WHERE smoker = 'no')) AS smoker_premium
    FROM gold.mart_profile GROUP BY age_band_key, age_band ORDER BY age_band_key
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Smokers cost about **$25,000 more** per year than non-smokers **in every age band** ($24,634–$25,029), and charges rise with age for both groups.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 3 — The Trend, 2021–2024
    """)
    return


@app.cell
def _(q):
    trend = q("""
    SELECT year, SUM(policy_years)::BIGINT AS policy_years,
           ROUND(SUM(total_charges) / SUM(policy_years), 2) AS avg_charges,
           ROUND(SUM(smokers) / SUM(policy_years), 3)       AS smoker_share
    FROM gold.mart_region_year GROUP BY 1 ORDER BY 1
    """)
    trend
    return (trend,)


@app.cell
def _(plt, trend):
    _fig, _ax = plt.subplots(figsize=(8, 4))
    _ax.plot(trend["year"].astype(str), trend["avg_charges"], marker="o")
    _ax.set_title("Average charges per policy-year")
    _ax.set_ylabel("charges ($)")
    plt.tight_layout()
    _fig
    return


@app.cell
def _(q):
    q("""
    SELECT f.year, k.smoker, COUNT(*) AS policy_years, ROUND(SUM(f.charges) / COUNT(*), 2) AS avg_charges
    FROM gold.fact_policy_year f JOIN gold.dim_smoker k USING (smoker_key)
    WHERE k.smoker <> 'unknown'
    GROUP BY ALL ORDER BY k.smoker, f.year
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The yearly average jumps up and down ($18,592 → $16,784 → $20,578 → $17,838) because the **smoker share** jumps (29.8%, 18.6%, 30.8%, 17.4%).
    **Within** each group, charges rise every year: non-smokers $11,291 → $13,121 (+16%), smokers $34,972 → $39,515 (+13%).
    The overall line hides a steady increase behind a change in the mix. Before reporting a trend, slice it by the dimension that drives the measure.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What to Remember

    - **Grain first**, written as a sentence and tested (5,197 rows = 5,197 distinct grain values).
    - **Dimensions** are small, numbered over their **distinct values** with an ordered `ROW_NUMBER()`, with an `unknown` member for flagged values.
    - **Validate** the fact against Silver: rows, totals, NULL keys, unique keys.
    - **Marts** store additive parts (sums, counts), declare their grain, and reconcile with the fact; ratios are computed last.
    """)
    return


if __name__ == "__main__":
    app.run()
