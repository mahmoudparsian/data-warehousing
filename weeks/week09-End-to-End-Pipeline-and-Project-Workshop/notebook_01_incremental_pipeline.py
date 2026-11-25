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
    # Week 9 — An Incremental Pipeline, Run by Run (Insurance Change Feed)

    The scenario of [slides 1](lecture_notes_01_incremental_pipelines.md), with one function per run and charts.
    A source system sends **versions** of 1,300 customers: day-1 rows, new customers, updates, a customer updated twice, and **late** rows
    (changed before run 1, arrived after it). Two pipelines run side by side:

    | Pipeline | Reads | Loads |
    |---|---|---|
    | **naive** | `updated_at > last run` | the latest version per customer, `MERGE` |
    | **safe** | `updated_at > last run - 1 day` (look-back) | the same |

    At the end, both are compared with a **full rebuild**.
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


@app.cell
def _(con, q):
    con.execute("""
    CREATE OR REPLACE TABLE src AS
    SELECT ROW_NUMBER() OVER (ORDER BY age, gender, bmi, children, smoker, region, charges) AS customer_id,
           age, smoker, region, CAST(charges AS DECIMAL(10, 2)) AS charges
    FROM read_csv('../week07-Silver-Layer-Cleaning-and-Conforming/data/insurance.2024.csv', types = {'smoker': 'VARCHAR'});

    CREATE OR REPLACE TABLE changes AS
    SELECT customer_id, region, smoker, charges, TIMESTAMP '2024-01-01 09:00' AS updated_at, TIMESTAMP '2024-01-01 09:05' AS arrived_at, 'day 1' AS kind
    FROM src WHERE customer_id <= 1200
    UNION ALL SELECT customer_id, region, smoker, charges, TIMESTAMP '2024-01-02 09:00', TIMESTAMP '2024-01-02 09:05', 'new customer'
    FROM src WHERE customer_id > 1200
    UNION ALL SELECT customer_id, region, smoker, ROUND(charges * 1.10, 2), TIMESTAMP '2024-01-02 10:00', TIMESTAMP '2024-01-02 10:01', 'update'
    FROM src WHERE customer_id <= 1200 AND customer_id % 100 = 0
    UNION ALL SELECT customer_id, region, smoker, ROUND(charges * 1.05, 2), TIMESTAMP '2024-01-02 11:00', TIMESTAMP '2024-01-02 11:01', 'update twice (1st)'
    FROM src WHERE customer_id <= 1200 AND customer_id % 100 = 50
    UNION ALL SELECT customer_id, region, smoker, ROUND(charges * 1.20, 2), TIMESTAMP '2024-01-02 12:00', TIMESTAMP '2024-01-02 12:01', 'update twice (2nd)'
    FROM src WHERE customer_id <= 1200 AND customer_id % 100 = 50
    UNION ALL SELECT customer_id, region, 'yes', ROUND(charges * 1.50, 2), TIMESTAMP '2024-01-01 23:00', TIMESTAMP '2024-01-02 08:00', 'late (smoker since Jan 1)'
    FROM src WHERE customer_id <= 1200 AND customer_id % 100 = 25
    UNION ALL SELECT customer_id, 'northeast', smoker, charges, TIMESTAMP '2024-01-03 09:00', TIMESTAMP '2024-01-03 09:01', 'moved to northeast'
    FROM src WHERE customer_id IN (7, 8, 9);
    """)
    q("SELECT kind, COUNT(*) AS versions, MIN(updated_at) AS updated_at, MIN(arrived_at) AS arrived_at FROM changes GROUP BY 1 ORDER BY MIN(arrived_at)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Pipeline: One Function, Two Settings

    Each run: read what is **visible** at run time (arrived) and newer than the filter → keep the latest version per customer → `MERGE`
    (update only if newer) → log the run. The run time is midnight UTC of each day.
    """)
    return


@app.cell
def _(con):
    def setup(name):
        con.execute(f"""
        CREATE OR REPLACE TABLE {name}_silver (customer_id INT PRIMARY KEY, region VARCHAR, smoker VARCHAR,
                                               charges DECIMAL(10, 2), updated_at TIMESTAMP, _run_id INT);
        CREATE OR REPLACE TABLE {name}_log (run_id INT, run_at TIMESTAMP, read_from TIMESTAMP, versions_read BIGINT, rows_changed BIGINT);
        """)

    def run(name, run_id, run_at, last_run, lookback_hours):
        read_from = "TIMESTAMP '1900-01-01'" if last_run is None else f"TIMESTAMP '{last_run}' - INTERVAL {lookback_hours} HOUR"
        con.execute(f"""
        CREATE OR REPLACE TEMP TABLE batch AS
        SELECT * EXCLUDE (arrived_at, kind) FROM changes
        WHERE arrived_at <= TIMESTAMP '{run_at}' AND updated_at > {read_from};

        CREATE OR REPLACE TEMP TABLE batch_latest AS
        SELECT * FROM batch QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) = 1;

        INSERT INTO {name}_log
        SELECT {run_id}, TIMESTAMP '{run_at}', {read_from}, (SELECT COUNT(*) FROM batch),
               (SELECT COUNT(*) FROM batch_latest b LEFT JOIN {name}_silver t USING (customer_id)
                WHERE t.customer_id IS NULL OR b.updated_at > t.updated_at);

        MERGE INTO {name}_silver AS t
        USING (SELECT *, {run_id} AS _run_id FROM batch_latest) AS s
        ON t.customer_id = s.customer_id
        WHEN MATCHED AND s.updated_at > t.updated_at THEN UPDATE SET region = s.region, smoker = s.smoker, charges = s.charges,
                                                               updated_at = s.updated_at, _run_id = s._run_id
        WHEN NOT MATCHED THEN INSERT VALUES (s.customer_id, s.region, s.smoker, s.charges, s.updated_at, s._run_id);
        """)

    runs = [(1, "2024-01-02 00:00", None), (2, "2024-01-03 00:00", "2024-01-02 00:00"),
            (3, "2024-01-04 00:00", "2024-01-03 00:00"), (4, "2024-01-04 00:00", "2024-01-04 00:00")]   # run 4 = run 3 again
    for _name, _lookback in [("naive", 0), ("safe", 24)]:
        setup(_name)
        for _run_id, _run_at, _last in runs:
            run(_name, _run_id, _run_at, _last, _lookback)
            if _name == "safe" and _run_id == 2:
                con.execute("CREATE OR REPLACE TABLE safe_after_run_2 AS SELECT * FROM safe_silver")
    return


@app.cell
def _(q):
    logs = q("""
    SELECT 'naive' AS pipeline, * FROM naive_log
    UNION ALL
    SELECT 'safe', * FROM safe_log
    ORDER BY pipeline, run_id
    """)
    logs
    return (logs,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Run 2** is where the pipelines part ways: the naive one reads 136 versions, the safe one 1,348 (its look-back re-reads day 1),
    yet both change only versions **newer** than Silver's, so re-reading adds nothing. The safe run changes **12 more rows**: the late ones.
    **Run 4** repeats run 3 with nothing new: 0 rows changed in both pipelines (idempotent).
    """)
    return


@app.cell
def _(logs, plt):
    _p = logs.pivot(index="run_id", columns="pipeline", values="rows_changed")
    _ax = _p.plot.bar(figsize=(8, 4), rot=0, logy=True)
    _ax.set_title("Rows changed per run (log scale)")
    _ax.set_ylabel("rows changed")
    plt.tight_layout()
    _ax.figure
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Proof: Each Pipeline vs a Full Rebuild
    """)
    return


@app.cell
def _(con, q):
    con.execute("""
    CREATE OR REPLACE TABLE full_rebuild AS
    SELECT customer_id, region, smoker, charges, updated_at FROM changes
    WHERE arrived_at <= TIMESTAMP '2024-01-04 00:00'
    QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) = 1;
    """)
    q("""
    SELECT 'naive' AS pipeline,
           (SELECT COUNT(*) FROM (SELECT customer_id, region, smoker, charges, updated_at FROM naive_silver EXCEPT SELECT * FROM full_rebuild)) AS rows_that_differ,
           (SELECT COUNT(*) FILTER (WHERE smoker = 'yes') FROM naive_silver) AS smokers,
           (SELECT SUM(charges) FROM naive_silver) AS total_charges
    UNION ALL
    SELECT 'safe',
           (SELECT COUNT(*) FROM (SELECT customer_id, region, smoker, charges, updated_at FROM safe_silver EXCEPT SELECT * FROM full_rebuild)),
           (SELECT COUNT(*) FILTER (WHERE smoker = 'yes') FROM safe_silver), (SELECT SUM(charges) FROM safe_silver)
    UNION ALL
    SELECT 'full rebuild', 0, (SELECT COUNT(*) FILTER (WHERE smoker = 'yes') FROM full_rebuild), (SELECT SUM(charges) FROM full_rebuild)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The safe pipeline equals the full rebuild (0 rows differ). The naive one differs in exactly the **12 late customers**: 10 smokers too few and
    $90,845.71 less in charges, and no run ever reported an error.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Gold: Rebuild Only the Touched Partitions

    Run 3 moved customers 7, 8 and 9 to the northeast. A mart by region stores additive parts, so only the regions they left and joined change.
    """)
    return


@app.cell
def _(q):
    mart = q("""
    WITH b AS (SELECT region, COUNT(*) AS customers_before_run_3, SUM(charges) AS charges_before FROM safe_after_run_2 GROUP BY 1),
         a AS (SELECT region, COUNT(*) AS customers_after_run_3,  SUM(charges) AS charges_after  FROM safe_silver GROUP BY 1)
    SELECT region, customers_before_run_3, customers_after_run_3,
           charges_after - charges_before AS charges_change,
           customers_before_run_3 <> customers_after_run_3 OR charges_before <> charges_after AS partition_to_rebuild
    FROM b JOIN a USING (region) ORDER BY region
    """)
    mart
    return (mart,)


@app.cell
def _(mart, plt):
    _ax = mart.set_index("region")["charges_change"].plot.bar(figsize=(8, 4), rot=0)
    _ax.set_title("Run 3: change in total charges per region (only touched partitions move)")
    plt.tight_layout()
    _ax.figure
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The three customers left the northwest (2) and the southwest (1) for the northeast (+3): 3 regions to rebuild, the southeast untouched.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What to Remember

    - **State** (run log, last run) is the pipeline's memory; filtering on `updated_at > last run` loses late rows **forever**.
    - A **look-back** window catches them, but only works with an **idempotent** load: deduplicate inside the batch, `MERGE` only newer versions.
    - **Run twice, change nothing**: run 4 changed 0 rows.
    - **Prove it**: incremental = full rebuild (`EXCEPT` both ways). Here the safe pipeline passes, the naive one fails by 12 customers.
    - **Gold**: store parts and rebuild only the partitions a run touched (old and new region of a customer who moves).
    """)
    return


if __name__ == "__main__":
    app.run()
