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
    # Week 7 — Conforming 4 Sources into One Silver Table (Insurance Data)

    The pipeline of [slides 1](lecture_notes_01_conformance_and_integration.md), run on the 4 messy yearly files in `data_messy/`,
    with every number **per source** and charts. Each file is a separate source: it arrives on its own, and it must reconcile on its own.

    | # | Rule | Fate |
    |---|---|---|
    | C1 | region: macro `norm_region` + mapping table | fixed |
    | C2 | smoker, gender: mapping tables (`m` → `male`) | fixed |
    | C3 | a value that doesn't map → `'unknown'` + a flag column | **flagged** (kept) |
    | D1 | rows identical after C1–C2, in the same yearly file | **duplicate** (removed, counted) |
    | R1–R5 | a missing value · age outside 18–100 · bmi outside 12–70 · children outside 0–10 · charges ≤ 0 | **rejected** (with a reason) |

    Order: standardize → deduplicate → reject / flag → reconcile → test.
    """)
    return


@app.cell
def _():
    import duckdb
    import matplotlib.pyplot as plt

    con = duckdb.connect()   # in memory: nothing is written to disk

    def q(sql):
        return con.execute(sql).df()

    return con, plt, q


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Bronze: Every Source As Received

    All columns as text, plus lineage: `_source_file`, `_batch_id` (the year), `_ingested_at`.
    """)
    return


@app.cell
def _(con, q):
    con.execute("""
    CREATE SCHEMA IF NOT EXISTS bronze;
    CREATE SCHEMA IF NOT EXISTS silver;

    CREATE OR REPLACE TABLE bronze.insurance AS
    SELECT * EXCLUDE (filename),
           regexp_extract(filename, '[^/]+$')                  AS _source_file,
           CAST(regexp_extract(filename, '(\\d{4})', 1) AS INT) AS _batch_id,
           current_timestamp                                   AS _ingested_at
    FROM read_csv('data_messy/insurance.*.messy.csv', all_varchar = true, filename = true);
    """)
    q("SELECT _source_file, COUNT(*) AS bronze_rows FROM bronze.insurance GROUP BY 1 ORDER BY 1")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 0 — Profile Each Source
    """)
    return


@app.cell
def _(q):
    q("""
    SELECT _batch_id AS year,
           COUNT(*)                                                          AS n_rows,
           COUNT(DISTINCT region)                                            AS region_spellings,
           COUNT(*) FILTER (WHERE smoker IS NULL OR smoker NOT IN ('yes', 'no'))  AS odd_smoker,
           COUNT(*) FILTER (WHERE gender IS NULL OR gender NOT IN ('female', 'male')) AS odd_gender,
           COUNT(*) FILTER (WHERE age IS NULL OR bmi IS NULL OR children IS NULL OR charges IS NULL) AS missing_value,
           COUNT(*) FILTER (WHERE TRY_CAST(age AS DOUBLE) NOT BETWEEN 18 AND 100)  AS odd_age,
           COUNT(*) FILTER (WHERE TRY_CAST(charges AS DOUBLE) <= 0)               AS charges_le_0
    FROM bronze.insurance
    GROUP BY 1 ORDER BY 1
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The point of the profile: **the 4 sources have the same kinds of problems in similar amounts**, so one set of rules can serve all of them.
    """)
    return


@app.cell
def _(plt, q):
    _df = q("""
    SELECT _batch_id AS year, '[' || COALESCE(region, 'NULL') || ']' AS region_as_received, COUNT(*) AS n_rows
    FROM bronze.insurance GROUP BY ALL ORDER BY region_as_received, year
    """)
    _pivot = _df.pivot(index="region_as_received", columns="year", values="n_rows").fillna(0)
    _pivot = _pivot.loc[_pivot.sum(axis=1).sort_values().index]
    _ax = _pivot.plot.barh(stacked=True, figsize=(9, 5))
    _ax.set_title("Bronze: 16 region values, in every source")
    _ax.set_xlabel("rows")
    plt.tight_layout()
    _ax.figure
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1 — Conform: a Macro + Mapping Tables
    """)
    return


@app.cell
def _(con, q):
    con.execute("""
    CREATE OR REPLACE MACRO norm_region(r) AS regexp_replace(lower(trim(r)), '[ -]', '', 'g');

    CREATE OR REPLACE TABLE silver.map_region AS SELECT * FROM (VALUES
        ('northeast', 'northeast'), ('northwest', 'northwest'),
        ('southeast', 'southeast'), ('southwest', 'southwest')) t(region_key, region);
    CREATE OR REPLACE TABLE silver.map_smoker AS SELECT * FROM (VALUES ('yes', 'yes'), ('no', 'no')) t(smoker_key, smoker);
    CREATE OR REPLACE TABLE silver.map_gender AS SELECT * FROM (VALUES ('female', 'female'), ('male', 'male'), ('m', 'male')) t(gender_key, gender);

    CREATE OR REPLACE TABLE silver.step1_standardized AS
    SELECT b._batch_id,
           TRY_CAST(TRY_CAST(b.age AS DOUBLE) AS INTEGER)      AS age,
           COALESCE(g.gender, 'unknown')                       AS gender,
           TRY_CAST(b.bmi AS DECIMAL(5, 2))                    AS bmi,
           TRY_CAST(TRY_CAST(b.children AS DOUBLE) AS INTEGER) AS children,
           COALESCE(s.smoker, 'unknown')                       AS smoker,
           COALESCE(r.region, 'unknown')                       AS region,
           TRY_CAST(b.charges AS DECIMAL(10, 2))               AS charges,
           b.region                                            AS region_raw
    FROM bronze.insurance b
    LEFT JOIN silver.map_region r ON r.region_key = norm_region(b.region)
    LEFT JOIN silver.map_smoker s ON s.smoker_key = lower(trim(b.smoker))
    LEFT JOIN silver.map_gender g ON g.gender_key = lower(trim(b.gender));
    """)
    q("""
    SELECT region, COUNT(*) AS n_rows, COUNT(DISTINCT region_raw) AS spellings_mapped_here
    FROM silver.step1_standardized
    GROUP BY 1 ORDER BY 1
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    16 region spellings → **4 regions + `unknown`** (1,046 rows). The `region_raw` column keeps what the source said (lineage).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2 — Deduplicate (After Standardizing, Within Each Source)
    """)
    return


@app.cell
def _(con, q):
    con.execute("""
    CREATE OR REPLACE TABLE silver.step2_dedup AS
    SELECT * FROM silver.step1_standardized
    QUALIFY ROW_NUMBER() OVER (PARTITION BY _batch_id, age, gender, bmi, children, smoker, region, charges
                               ORDER BY region_raw) = 1;
    """)
    q("""
    WITH raw AS (SELECT _batch_id, COUNT(*) AS n FROM bronze.insurance GROUP BY 1),
         raw_distinct AS (SELECT _batch_id, COUNT(*) AS n
                          FROM (SELECT DISTINCT * EXCLUDE (_source_file, _ingested_at) FROM bronze.insurance) GROUP BY 1),
         std_distinct AS (SELECT _batch_id, COUNT(*) AS n FROM silver.step2_dedup GROUP BY 1)
    SELECT _batch_id AS year, raw.n - raw_distinct.n AS copies_raw, raw.n - std_distinct.n AS copies_standardized
    FROM raw JOIN raw_distinct USING (_batch_id) JOIN std_distinct USING (_batch_id)
    ORDER BY year
    """)
    return


@app.cell
def _(q):
    q("""
    WITH g AS (SELECT *, COUNT(*) OVER (PARTITION BY _batch_id, age, gender, bmi, children, smoker, region, charges) AS copies,
                         COUNT(DISTINCT region_raw) OVER (PARTITION BY _batch_id, age, gender, bmi, children, smoker, region, charges) AS spellings
               FROM silver.step1_standardized)
    SELECT _batch_id AS year, age, gender, bmi, charges, region, region_raw
    FROM g WHERE copies > 1 AND spellings > 1
    ORDER BY year, charges, region_raw
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **287 raw copies, 296 after standardizing.** The 9 extra copies (above, as pairs) have the same age, bmi and charges to the cent, and differ only in the
    region spelling: `north-east` / `northeast`, or two unmappable labels such as `midwest` / `mars`. Same customer-year, sent twice.
    (For order lines without a line id it is the other way round: see slides 2, Step 4.)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 3 — Reject (Quarantine with a Reason) and Flag
    """)
    return


@app.cell
def _(con, q):
    con.execute("""
    CREATE OR REPLACE TABLE silver.insurance_rejected AS
    SELECT *,
           CASE WHEN age IS NULL OR bmi IS NULL OR children IS NULL OR charges IS NULL THEN 'missing value'
                WHEN age NOT BETWEEN 18 AND 100     THEN 'age outside 18-100'
                WHEN bmi NOT BETWEEN 12 AND 70      THEN 'bmi outside 12-70'
                WHEN children NOT BETWEEN 0 AND 10  THEN 'children outside 0-10'
                ELSE 'charges <= 0' END AS reject_reason
    FROM silver.step2_dedup
    WHERE age IS NULL OR bmi IS NULL OR children IS NULL OR charges IS NULL
       OR age NOT BETWEEN 18 AND 100 OR bmi NOT BETWEEN 12 AND 70
       OR children NOT BETWEEN 0 AND 10 OR charges <= 0;

    CREATE OR REPLACE TABLE silver.insurance AS
    SELECT _batch_id AS year, age, gender, bmi, children, smoker, region, charges, region_raw,
           gender = 'unknown' AS is_gender_unknown,
           smoker = 'unknown' AS is_smoker_unknown,
           region = 'unknown' AS is_region_unknown
    FROM silver.step2_dedup
    WHERE NOT (age IS NULL OR bmi IS NULL OR children IS NULL OR charges IS NULL
               OR age NOT BETWEEN 18 AND 100 OR bmi NOT BETWEEN 12 AND 70
               OR children NOT BETWEEN 0 AND 10 OR charges <= 0);
    """)
    q("""
    PIVOT (SELECT _batch_id AS year, reject_reason FROM silver.insurance_rejected)
    ON year USING COUNT(*) GROUP BY reject_reason ORDER BY reject_reason
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ⚖️ Reconcile Each Source: Bronze = Valid + Flagged + Rejected + Duplicates
    """)
    return


@app.cell
def _(q):
    recon = q("""
    WITH b AS (SELECT _batch_id AS year, COUNT(*) AS bronze FROM bronze.insurance GROUP BY 1),
         s AS (SELECT year,
                      COUNT(*) FILTER (WHERE NOT (is_gender_unknown OR is_smoker_unknown OR is_region_unknown)) AS valid,
                      COUNT(*) FILTER (WHERE is_gender_unknown OR is_smoker_unknown OR is_region_unknown)     AS flagged
               FROM silver.insurance GROUP BY 1),
         r AS (SELECT _batch_id AS year, COUNT(*) AS rejected FROM silver.insurance_rejected GROUP BY 1),
         d AS (SELECT a._batch_id AS year, a.n - c.n AS duplicates
               FROM (SELECT _batch_id, COUNT(*) AS n FROM silver.step1_standardized GROUP BY 1) a
               JOIN (SELECT _batch_id, COUNT(*) AS n FROM silver.step2_dedup GROUP BY 1) c USING (_batch_id))
    SELECT CAST(year AS VARCHAR) AS source_year, bronze, valid, flagged, rejected, duplicates,
           bronze = valid + flagged + rejected + duplicates AS reconciled
    FROM b JOIN s USING (year) JOIN r USING (year) JOIN d USING (year)
    UNION ALL
    SELECT 'all sources', SUM(bronze)::BIGINT, SUM(valid)::BIGINT, SUM(flagged)::BIGINT, SUM(rejected)::BIGINT, SUM(duplicates)::BIGINT,
           SUM(bronze) = SUM(valid + flagged + rejected + duplicates)
    FROM b JOIN s USING (year) JOIN r USING (year) JOIN d USING (year)
    ORDER BY source_year
    """)
    recon
    return (recon,)


@app.cell
def _(plt, recon):
    _per_year = recon[recon["source_year"] != "all sources"].set_index("source_year")[["valid", "flagged", "rejected", "duplicates"]]
    _ax = _per_year.plot.bar(stacked=True, figsize=(8, 4), rot=0)
    _ax.set_title("Every Bronze row has exactly one fate, per source")
    _ax.set_ylabel("rows")
    plt.tight_layout()
    _ax.figure
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **6,467 = 4,160 valid + 1,037 flagged + 974 rejected + 296 duplicates**, and every source reconciles on its own (the last line is the total).
    Silver holds the valid and flagged rows: **5,197**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🚩 Why Flag the Unknown Regions Instead of Dropping Them?
    """)
    return


@app.cell
def _(q):
    by_region = q("""
    SELECT region, COUNT(*) AS customers, ROUND(AVG(charges), 2) AS avg_charges,
           ROUND(AVG((smoker = 'yes')::INT), 3) AS smoker_share
    FROM silver.insurance GROUP BY 1 ORDER BY 1
    """)
    by_region
    return (by_region,)


@app.cell
def _(by_region, plt):
    _df = by_region
    _fig, (_a, _b) = plt.subplots(1, 2, figsize=(12, 4))
    _colors = ["tab:red" if r == "unknown" else "tab:blue" for r in _df["region"]]
    _a.bar(_df["region"], _df["smoker_share"], color=_colors)
    _a.set_title("Smoker share by region (Silver)")
    _b.bar(_df["region"], _df["avg_charges"], color=_colors)
    _b.set_title("Average charges by region (Silver)")
    plt.tight_layout()
    _fig
    return


@app.cell
def _(q):
    q("""
    SELECT 'all Silver rows (flags kept)' AS population, COUNT(*) AS customers, ROUND(AVG(charges), 2) AS avg_charges
    FROM silver.insurance
    UNION ALL
    SELECT 'unknown regions dropped', COUNT(*), ROUND(AVG(charges), 2)
    FROM silver.insurance WHERE NOT is_region_unknown
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The 813 `unknown`-region customers are **53%** smokers (17.5–19.4% in the real regions) and average **$25,961** in charges.
    Dropping them would lower the average charge of the whole book from **$18,481.91 to $17,094.97**: a 7.5% understatement, with no trace.
    Flagged, they stay in every total, and a region report can still show them as their own `unknown` bar.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✅ Tests (All Must Be 0)
    """)
    return


@app.cell
def _(q):
    q("""
    SELECT 'region not canonical' AS test, COUNT(*) AS failures FROM silver.insurance
    WHERE region NOT IN (SELECT region FROM silver.map_region) AND NOT is_region_unknown
    UNION ALL SELECT 'missing measure', COUNT(*) FROM silver.insurance
    WHERE age IS NULL OR bmi IS NULL OR children IS NULL OR charges IS NULL
    UNION ALL SELECT 'impossible value', COUNT(*) FROM silver.insurance
    WHERE age NOT BETWEEN 18 AND 100 OR bmi NOT BETWEEN 12 AND 70 OR children NOT BETWEEN 0 AND 10 OR charges <= 0
    UNION ALL SELECT 'duplicate rows', COUNT(*) - COUNT(DISTINCT (year, age, gender, bmi, children, smoker, region, charges))
    FROM silver.insurance
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 📊 Before / After: One KPI, Three Answers
    """)
    return


@app.cell
def _(q):
    q("""
    SELECT 'Bronze, region = ''northeast''' AS answer_from, COUNT(*) AS n_rows,
           ROUND(AVG(TRY_CAST(charges AS DOUBLE)), 2) AS avg_charges
    FROM bronze.insurance WHERE region = 'northeast'
    UNION ALL
    SELECT 'Bronze, all 4 spellings', COUNT(*), ROUND(AVG(TRY_CAST(charges AS DOUBLE)), 2)
    FROM bronze.insurance WHERE norm_region(region) = 'northeast'
    UNION ALL
    SELECT 'Silver', COUNT(*), ROUND(AVG(charges), 2)
    FROM silver.insurance WHERE region = 'northeast'
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What to Remember

    - **Profile each source** first: the rules come from the numbers, and similar problems across sources mean one set of rules.
    - **Conform with a macro and mapping tables**: 16 spellings → 4 regions + `unknown`; the tables are data the business can review.
    - **Deduplicate after standardizing** when two different customers can't look identical: 296 copies, not 287.
    - **Reject with a reason, flag what is still useful**: the flagged rows are not a random sample (53% smokers).
    - **Reconcile per source and test** after every load: 6,467 = 4,160 + 1,037 + 974 + 296, every test 0.
    """)
    return


if __name__ == "__main__":
    app.run()
