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
    # Week 6 — Silver Cleaning, Step by Step (Insurance Data)

    The steps of the Silver slides (`lecture_notes_02_silver_cleaning.md`) on **1,338 customers** instead of 10 rows, with charts.
    Every step: the **rule**, the **SQL**, the **result** in numbers. At the end, the reconciliation proves that no row was lost.

    | Rule | Fate |
    |---|---|
    | S1 region: trim, lower case, `ne` / `north-east` / `se` / `south west` → standard names | fixed |
    | S2 rows identical after S1 | **duplicate** (removed, counted) |
    | S3 missing `charges` | **rejected** (`missing charges`) |
    | S4 `charges` above 100,000 (impossible for this insurer) | **rejected** (`impossible charges`) |
    | S5 `age_band`, `bmi_class` | computed |
    """)
    return


@app.cell
def _():
    import duckdb
    import matplotlib.pyplot as plt

    con = duckdb.connect()   # in memory
    return con, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Bronze: the "Source File", As Received

    The source sends the week 1 insurance data with typical problems (we create them here so the notebook is self-contained):
    region spellings (`NE`, `north-east`, `SE`, `South West `), 18 rows without charges, 3 charges multiplied by 100,
    and rows sent twice (some of them with another spelling of the region).
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
    CREATE SCHEMA IF NOT EXISTS bronze;
    CREATE SCHEMA IF NOT EXISTS silver;
    
    CREATE OR REPLACE TABLE bronze.insurance AS
    WITH o AS (SELECT * FROM read_csv('../week01-Foundations-SQL-for-Analytics/example_1_insurance/insurance.csv', all_varchar = true))
    SELECT age, gender, bmi, children, smoker,
           CASE WHEN region = 'northeast' AND age::INT % 5 = 0 THEN 'NE'
                WHEN region = 'northeast' AND age::INT % 5 = 1 THEN 'north-east'
                WHEN region = 'southeast' AND age::INT % 4 = 0 THEN 'SE'
                WHEN region = 'southwest' AND bmi::DOUBLE > 40 THEN 'South West '
                ELSE region END                                            AS region,
           CASE WHEN children = '5'            THEN NULL                    -- lost in transfer
                WHEN charges::DOUBLE > 60000    THEN (charges::DOUBLE * 100)::VARCHAR   -- a decimal-point error
                ELSE charges END                                           AS charges
    FROM o
    UNION ALL SELECT age, gender, bmi, children, smoker, region, charges FROM o WHERE bmi::DOUBLE > 45                     -- sent twice
    UNION ALL SELECT age, gender, bmi, children, smoker, 'Northeast', charges FROM o WHERE region = 'northeast' AND bmi::DOUBLE > 40;  -- sent twice, other spelling
    
    SELECT COUNT(*) AS bronze_rows FROM bronze.insurance
    """).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 0 — Profile Bronze
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
    SELECT COUNT(*)                                                   AS n_rows,
           COUNT(*) - COUNT(charges)                                  AS null_charges,
           COUNT(*) FILTER (WHERE charges::DOUBLE > 100000)           AS impossible_charges,
           COUNT(DISTINCT region)                                     AS region_spellings,
           COUNT(*) - (SELECT COUNT(*) FROM (SELECT DISTINCT * FROM bronze.insurance)) AS exact_duplicates
    FROM bronze.insurance
    """).df()
    _df
    return


@app.cell
def _(con):
    _df = con.execute("""
    SELECT '[' || region || ']' AS region_as_received, COUNT(*) AS n_rows
    FROM bronze.insurance
    GROUP BY ALL
    ORDER BY n_rows DESC
    """).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **The to-do list:** 9 spellings of 4 regions, 18 missing and 3 impossible charges, and duplicates (13 exact copies so far; more appear after S1).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1 — Standardize (S1)
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
    CREATE OR REPLACE TABLE silver.step1_standardized AS
    SELECT age::INTEGER       AS age,
           gender,
           bmi::DOUBLE        AS bmi,
           children::INTEGER  AS children,
           smoker = 'yes'     AS smoker,
           CASE REPLACE(LOWER(TRIM(region)), ' ', '')
                WHEN 'ne'         THEN 'northeast'
                WHEN 'north-east' THEN 'northeast'
                WHEN 'se'         THEN 'southeast'
                ELSE REPLACE(LOWER(TRIM(region)), ' ', '')
           END                AS region,
           charges::DOUBLE    AS charges
    FROM bronze.insurance;
    
    SELECT region, COUNT(*) AS n_rows FROM silver.step1_standardized GROUP BY ALL ORDER BY region
    """).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2 — Deduplicate (S2), After Standardizing
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
    SELECT (SELECT COUNT(*) FROM (SELECT DISTINCT * FROM bronze.insurance))          AS distinct_before_s1,
           (SELECT COUNT(*) FROM (SELECT DISTINCT * FROM silver.step1_standardized))  AS distinct_after_s1
    """).df()
    _df
    return


@app.cell
def _(con):
    _df = con.execute("""
    CREATE OR REPLACE TABLE silver.step2_dedup AS
    SELECT DISTINCT * FROM silver.step1_standardized;
    
    SELECT (SELECT COUNT(*) FROM silver.step1_standardized) - COUNT(*) AS duplicates_removed
    FROM silver.step2_dedup
    """).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    21 copies are found **only after** S1: they differ from their original only in how the region is spelled (`Northeast` vs `northeast`).
    Deduplicating first would have left them in, and every count by region would be too high.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Steps 3–4 — Quarantine Missing and Impossible Charges (S3, S4)
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
    CREATE OR REPLACE TABLE silver.rejected AS
    SELECT *,
           CASE WHEN charges IS NULL THEN 'missing charges' ELSE 'impossible charges' END AS reject_reason
    FROM silver.step2_dedup
    WHERE charges IS NULL OR charges > 100000;
    
    SELECT reject_reason, COUNT(*) AS n_rows, MIN(charges) AS min_charges, MAX(charges) AS max_charges
    FROM silver.rejected
    GROUP BY ALL
    ORDER BY reject_reason
    """).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The 3 impossible values are 6,002,140 to 6,377,043: real charges of 60,021 to 63,770, each multiplied by 100. A Silver rule could also **fix** them
    (divide by 100) if the business confirms the cause; until then they are rejected, with the reason, and nothing is guessed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 5 — Enrich (S5) → `silver.insurance`
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
    CREATE OR REPLACE TABLE silver.insurance AS
    SELECT *,
           (age // 10) * 10                        AS age_band,
           CASE WHEN bmi < 18.5 THEN 'underweight'
                WHEN bmi < 25   THEN 'normal'
                WHEN bmi < 30   THEN 'overweight'
                ELSE 'obese' END                   AS bmi_class
    FROM silver.step2_dedup
    WHERE NOT (charges IS NULL OR charges > 100000);      -- exactly the rows not rejected
    
    SELECT bmi_class, COUNT(*) AS customers, ROUND(AVG(charges), 0) AS avg_charges
    FROM silver.insurance
    GROUP BY ALL
    ORDER BY avg_charges
    """).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ⚖️ Validation 1 — Reconcile
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
    SELECT (SELECT COUNT(*) FROM bronze.insurance)                                               AS bronze_rows,
           (SELECT COUNT(*) FROM silver.insurance)                                               AS valid,
           0                                                                                     AS flagged,
           (SELECT COUNT(*) FROM silver.rejected)                                                AS rejected,
           (SELECT COUNT(*) FROM silver.step1_standardized) - (SELECT COUNT(*) FROM silver.step2_dedup) AS duplicates
    """).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **1,373 = 1,318 valid + 0 flagged + 21 rejected + 34 duplicates.** (One of the 34 copies was already in the original week 1 file.)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✅ Validation 2 — Rules as Tests (all must be 0)
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
    SELECT COUNT(*) - (SELECT COUNT(*) FROM (SELECT DISTINCT * FROM silver.insurance))          AS duplicates_left,
           COUNT(*) FILTER (WHERE region NOT IN ('northeast', 'northwest', 'southeast', 'southwest')) AS bad_regions,
           COUNT(*) FILTER (WHERE charges IS NULL OR charges > 100000)                              AS bad_charges,
           COUNT(*) FILTER (WHERE age_band IS NULL OR bmi_class IS NULL)                            AS missing_enrichment
    FROM silver.insurance
    """).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 📊 Before / After by Region
    """)
    return


@app.cell
def _(con, plt):
    _bronze = con.execute("""
    SELECT region, AVG(TRY_CAST(charges AS DOUBLE)) AS avg_charges FROM bronze.insurance GROUP BY ALL ORDER BY region
    """).df()
    _silver = con.execute("""
    SELECT region, AVG(charges) AS avg_charges FROM silver.insurance GROUP BY ALL ORDER BY region
    """).df()

    _fig, (_a, _b) = plt.subplots(1, 2, figsize=(12, 4))
    _a.bar(_bronze["region"].str.replace(" ", "·"), _bronze["avg_charges"])
    _a.set_title("Bronze (naive): 9 'regions', impossible values included")
    _a.tick_params(axis="x", rotation=45)
    _b.bar(_silver["region"], _silver["avg_charges"])
    _b.set_title("Silver: 4 regions, rules applied")
    _b.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(con):
    _df = con.execute("""
    SELECT 'Bronze (naive)' AS source, COUNT(*) AS n_rows, COUNT(DISTINCT region) AS regions,
           ROUND(AVG(TRY_CAST(charges AS DOUBLE)), 0) AS avg_charges
    FROM bronze.insurance
    UNION ALL
    SELECT 'Silver', COUNT(*), COUNT(DISTINCT region), ROUND(AVG(charges), 0)
    FROM silver.insurance
    """).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What to Remember

    - Profile first: every rule came from a number in Step 0.
    - Standardize **before** deduplicating: 21 copies were visible only after S1.
    - Reject with a reason, never filter silently: `silver.rejected` explains every missing row.
    - Reconcile and test after every load: **1,373 = 1,318 + 0 + 21 + 34**, and every test returns 0.
    - Silver changes the KPIs (the average, the number of regions): Bronze numbers are not a report.
    """)
    return


if __name__ == "__main__":
    app.run()
