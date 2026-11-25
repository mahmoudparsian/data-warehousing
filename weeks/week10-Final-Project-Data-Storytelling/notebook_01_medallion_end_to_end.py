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
    # Week 10 — The Whole Course in One Notebook: Bronze → Silver → Gold → KPI → Story

    A small messy source ([`insurance_bronze_raw.csv`](insurance_bronze_raw.csv), [metadata](insurance_bronze_raw.metadata.md)): 90 **versions**
    of 25 customers (`customer_id`, `region`, `smoker`, `charges`, `updated_at`). Every step in SQL, every number from a run.

    | Week | Step here |
    |---|---|
    | 5–6 | Bronze as received + profile |
    | 6–7 | Silver: conform with a mapping table, keep the latest version per customer, reconcile |
    | 8 | Gold: dimensions, fact, a mart of additive parts, KPIs as ratios of sums |
    | 9 | Day 2: new, updated and late versions; naive filter vs look-back; drift |
    | 10 | KPI card and a Situation → Complication → Resolution story |
    """)
    return


@app.cell
def _():
    import duckdb
    import matplotlib.pyplot as plt

    con = duckdb.connect()   # in memory
    con.execute("SET TimeZone = 'UTC'")

    def q(sql):
        return con.execute(sql).df()

    return con, plt, q


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Bronze: As Received, Then Profiled
    """)
    return


@app.cell
def _(con, q):
    con.execute("""
    CREATE SCHEMA IF NOT EXISTS bronze; CREATE SCHEMA IF NOT EXISTS silver; CREATE SCHEMA IF NOT EXISTS gold;
    CREATE OR REPLACE TABLE bronze.insurance AS
    SELECT *, 'insurance_bronze_raw.csv' AS _source_file, 1 AS _batch_id
    FROM read_csv('insurance_bronze_raw.csv', all_varchar = true);
    """)
    q("""
    SELECT COUNT(*) AS versions, COUNT(DISTINCT customer_id) AS customers, COUNT(DISTINCT region) AS region_spellings,
           COUNT(DISTINCT smoker) AS smoker_spellings, MIN(updated_at) AS first_update, MAX(updated_at) AS last_update
    FROM bronze.insurance
    """)
    return


@app.cell
def _(q):
    q("SELECT region, COUNT(*) AS versions FROM bronze.insurance GROUP BY 1 ORDER BY 2 DESC, 1")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **To-do list from the profile:** 11 spellings of 4 regions, smoker in several spellings, and 90 versions for 25 customers
    (each customer was updated several times: the business wants the **latest** version).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Silver: Conform, Keep the Latest Version, Reconcile
    """)
    return


@app.cell
def _(con, q):
    con.execute("""
    CREATE OR REPLACE MACRO norm_region(r) AS regexp_replace(lower(trim(r)), '[ -]', '', 'g');
    CREATE OR REPLACE TABLE silver.map_region AS SELECT * FROM (VALUES
        ('ne', 'northeast'), ('northeast', 'northeast'), ('nw', 'northwest'), ('northwest', 'northwest'),
        ('se', 'southeast'), ('southeast', 'southeast'), ('sw', 'southwest'), ('southwest', 'southwest')) t(region_key, region);
    CREATE OR REPLACE TABLE silver.map_smoker AS SELECT * FROM (VALUES ('yes', 'yes'), ('true', 'yes'), ('no', 'no'), ('false', 'no')) t(smoker_key, smoker);

    CREATE OR REPLACE TABLE silver.step1_standardized AS
    SELECT CAST(b.customer_id AS INT) AS customer_id, COALESCE(r.region, 'unknown') AS region, COALESCE(s.smoker, 'unknown') AS smoker,
           CAST(b.charges AS DECIMAL(10, 2)) AS charges, CAST(b.updated_at AS TIMESTAMP) AS updated_at, b.region AS region_raw
    FROM bronze.insurance b
    LEFT JOIN silver.map_region r ON r.region_key = norm_region(b.region)
    LEFT JOIN silver.map_smoker s ON s.smoker_key = lower(trim(b.smoker));

    CREATE OR REPLACE TABLE silver.customers AS                 -- one row per customer: the latest version
    SELECT * FROM silver.step1_standardized
    QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) = 1;
    """)
    q("""
    SELECT (SELECT COUNT(*) FROM bronze.insurance) AS bronze_versions,
           (SELECT COUNT(*) FROM silver.customers) AS silver_customers,
           (SELECT COUNT(*) FROM silver.step1_standardized) - (SELECT COUNT(*) FROM silver.customers) AS older_versions_superseded,
           (SELECT COUNT(*) FROM silver.customers WHERE region = 'unknown' OR smoker = 'unknown') AS flagged_unknown
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Every version has a fate: **90 = 25 current + 65 superseded** (older versions of the same customer, counted; Bronze keeps them).
    Every spelling maps (0 `unknown`).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Gold: Star Schema and a Mart of Additive Parts
    """)
    return


@app.cell
def _(con, q):
    con.execute("""
    CREATE OR REPLACE TABLE gold.dim_region AS
    SELECT ROW_NUMBER() OVER (ORDER BY region) AS region_key, region FROM (SELECT DISTINCT region FROM silver.customers);
    CREATE OR REPLACE TABLE gold.dim_smoker AS
    SELECT ROW_NUMBER() OVER (ORDER BY smoker) AS smoker_key, smoker FROM (SELECT DISTINCT smoker FROM silver.customers);
    CREATE OR REPLACE TABLE gold.fact_customer AS
    SELECT c.customer_id, r.region_key, s.smoker_key, c.charges, c.updated_at
    FROM silver.customers c JOIN gold.dim_region r USING (region) JOIN gold.dim_smoker s USING (smoker);
    CREATE OR REPLACE TABLE gold.mart_region_smoker AS
    SELECT r.region, s.smoker, COUNT(*) AS customers, SUM(f.charges) AS total_charges
    FROM gold.fact_customer f JOIN gold.dim_region r USING (region_key) JOIN gold.dim_smoker s USING (smoker_key)
    GROUP BY ALL;
    """)
    q("""
    SELECT 'fact rows = silver' AS test, (SELECT COUNT(*) FROM gold.fact_customer) = (SELECT COUNT(*) FROM silver.customers) AS passed
    UNION ALL SELECT 'mart charges = fact', (SELECT SUM(total_charges) FROM gold.mart_region_smoker) = (SELECT SUM(charges) FROM gold.fact_customer)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## KPI: Average Charges per Customer, Three Ways
    """)
    return


@app.cell
def _(q):
    q("""
    SELECT 'Bronze, every version' AS computed_from, COUNT(*) AS n_rows, ROUND(AVG(CAST(charges AS DOUBLE)), 2) AS avg_charges
    FROM bronze.insurance
    UNION ALL
    SELECT 'Gold mart, average of the cell averages', COUNT(*), ROUND(AVG(total_charges / customers), 2)
    FROM gold.mart_region_smoker
    UNION ALL
    SELECT 'Gold mart, ratio of sums (correct)', SUM(customers)::BIGINT, ROUND(SUM(total_charges) / SUM(customers), 2)
    FROM gold.mart_region_smoker
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    | KPI card | |
    |---|---|
    | Name | average charges per customer |
    | Formula | `SUM(charges) / COUNT(*)` over current customers (from the mart: `SUM(total_charges) / SUM(customers)`) |
    | Grain | customer (latest version) |
    | Additive? | no: recompute from the parts, never average averages |
    """)
    return


@app.cell
def _(plt, q):
    _df = q("""
    SELECT region, smoker, ROUND(SUM(total_charges) / SUM(customers), 2) AS avg_charges, SUM(customers)::BIGINT AS customers
    FROM gold.mart_region_smoker GROUP BY ALL ORDER BY region, smoker
    """)
    _p = _df.pivot(index="region", columns="smoker", values="avg_charges")
    _ax = _p.plot.bar(figsize=(8, 4), rot=0)
    _ax.set_title("Average charges per customer, by region and smoker status (n is small: 25 customers)")
    plt.tight_layout()
    _ax.figure
    return


@app.cell
def _(q):
    q("""
    SELECT smoker, SUM(customers)::BIGINT AS customers, ROUND(SUM(total_charges) / SUM(customers), 2) AS avg_charges
    FROM gold.mart_region_smoker GROUP BY 1 ORDER BY 1
    """)
    return


@app.cell
def _(q):
    q("""
    SELECT region, SUM(customers)::BIGINT AS customers, ROUND(SUM(total_charges) / SUM(customers), 2) AS avg_charges
    FROM gold.mart_region_smoker GROUP BY 1 ORDER BY 1
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Day 2: New, Updated and Late Versions (Week 9)

    Run 1 ran on Jan 5, 00:00. Day 2's feed (deterministic): 3 new customers, 4 updates (+20% charges), and 3 **late** versions (the 3 lowest-numbered non-smokers above 7 became
    smokers on Jan 4 at 23:00, but the change arrived after run 1). Run 2 (Jan 6, 00:00): naive (`updated_at > last run`) vs a 1-day look-back.
    """)
    return


@app.cell
def _(con, q):
    con.execute("""
    CREATE OR REPLACE TABLE day2 AS
    SELECT 100 + customer_id AS customer_id, region, smoker, charges, TIMESTAMP '2024-01-05 10:00' AS updated_at FROM silver.customers WHERE customer_id IN (1, 2, 3)
    UNION ALL SELECT customer_id, region, smoker, ROUND(charges * 1.20, 2), TIMESTAMP '2024-01-05 11:00' FROM silver.customers WHERE customer_id IN (4, 5, 6, 7)
    UNION ALL SELECT customer_id, region, 'yes', ROUND(charges * 1.50, 2), TIMESTAMP '2024-01-04 23:00' FROM silver.customers
    WHERE customer_id IN (SELECT customer_id FROM silver.customers WHERE smoker = 'no' AND customer_id > 7 ORDER BY customer_id LIMIT 3);

    CREATE OR REPLACE MACRO run2(since) AS TABLE
    SELECT * FROM (SELECT customer_id, region, smoker, charges, updated_at FROM silver.customers
                   UNION ALL
                   SELECT * FROM day2 WHERE updated_at > since)
    QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) = 1;
    """)
    drift = q("""
    SELECT 'day 1' AS state, COUNT(*) AS customers, COUNT(*) FILTER (WHERE smoker = 'yes') AS smokers,
           ROUND(SUM(charges) / COUNT(*), 2) AS avg_charges FROM silver.customers
    UNION ALL
    SELECT 'day 2, naive (updated_at > Jan 5)', COUNT(*), COUNT(*) FILTER (WHERE smoker = 'yes'), ROUND(SUM(charges) / COUNT(*), 2)
    FROM run2(TIMESTAMP '2024-01-05 00:00')
    UNION ALL
    SELECT 'day 2, look-back (updated_at > Jan 4)', COUNT(*), COUNT(*) FILTER (WHERE smoker = 'yes'), ROUND(SUM(charges) / COUNT(*), 2)
    FROM run2(TIMESTAMP '2024-01-04 00:00')
    """)
    drift
    return (drift,)


@app.cell
def _(mo):
    mo.md(r"""
    The naive run misses the 3 late versions: both day-2 runs have **28 customers**, but the naive one has 16 smokers instead of 19 and an average of
    $8,612.63 instead of $8,941.00. Same row count, different KPI: a count check would not catch it; a comparison with a full rebuild would (week 9).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The One-Slide Story (Situation → Complication → Resolution)

    Every number below comes from a query above (≤ 60 words in the real slide):

    > **Situation:** our 25 customers cost **$8,100.46** each on average (ratio of sums; the raw versions would say $8,307.62).
    > **Complication:** at this size nothing clearly drives cost: smokers average **$7,987.29**, non-smokers **$8,270.20**; regions range from
    > $6,848.89 (southeast, 9 customers) to $10,151.00 (northeast, **2** customers). And a naive daily load would silently miss late changes.
    > **Resolution:** don't change prices on 25 customers; collect a year of data, load it with a look-back window, and prove every run against a full rebuild.
    > *Caveat: 25 customers, synthetic data. "No clear driver yet" is a finding too.*

    """)
    return


if __name__ == "__main__":
    app.run()
