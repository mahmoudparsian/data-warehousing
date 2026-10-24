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
    # Week 9 — Pipelines + Incremental Processing (Elite Notebook)

    This notebook demonstrates a **production-like incremental pipeline** using a simple insurance example.

    ## Week 9 goals
    1. Simulate Day 1 and Day 2 pipeline runs.
    2. Show the difference between full reload and incremental logic.
    3. Demonstrate why state matters.
    4. Simulate late-arriving data.
    5. Deduplicate updates correctly.
    6. Update Silver and Gold layers incrementally.
    7. Validate the pipeline after each run.
    8. Show failure cases and how to fix them.

    ## Core message
    A correct pipeline once is easy.

    A correct pipeline every day is hard.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pipeline scenario

    We will simulate:
    - **Day 1**: initial load
    - **Day 2**: new rows + updated rows + late-arriving rows

    We will compare:
    - naive incremental logic
    - safer incremental logic with a sliding window
    - deduplication before merge
    - KPI differences before and after corrections
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup and base dataset

    For teaching simplicity, we start from `insurance.csv` and simulate:
    - an entity key
    - an update timestamp
    - event year

    In a real production system, these would come from source systems.
    """)
    return


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import duckdb

    base = pd.read_csv("../week01-Foundations-SQL-for-Analytics/example_1_insurance/insurance.csv").copy()

    # Simulate a business key and timestamps
    base = base.reset_index(drop=True)
    base["record_id"] = range(1, len(base) + 1)
    base["updated_at"] = pd.Timestamp("2024-01-01 01:00:00")
    base["year"] = 2024

    base.head()
    return base, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Day 1 — Initial pipeline run

    On Day 1, we do an initial full load.

    ### Initial state
    We assume:
    - no prior watermark
    - all rows are new
    """)
    return


@app.cell
def _(base):
    day1_source = base.copy()
    day1_source.shape
    return (day1_source,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Build Day 1 Silver

    We simulate a simple Silver process:
    - standardize region
    - remove NULL charges
    - deduplicate by `record_id`
    """)
    return


@app.cell
def _(day1_source):
    def build_silver(df):
        x = df.copy()

        # Standardize region
        region_map = {
            "NE": "northeast",
            "north-east": "northeast",
            "Northeast": "northeast",
            "NW": "northwest",
            "north-west": "northwest",
            "Northwest": "northwest",
            "SE": "southeast",
            "south-east": "southeast",
            "Southeast": "southeast",
            "SW": "southwest",
            "south-west": "southwest",
            "Southwest": "southwest"
        }

        x["region"] = x["region"].astype(str).str.strip().replace(region_map).str.lower()
        x["smoker"] = x["smoker"].astype(str).str.strip().str.lower()

        # Remove NULL metric rows
        x = x[x["charges"].notna()].copy()

        # Deduplicate by record_id keeping latest updated_at
        x = x.sort_values(["record_id", "updated_at"], ascending=[True, False])
        x["rn"] = x.groupby("record_id").cumcount() + 1
        x = x[x["rn"] == 1].drop(columns=["rn"])

        return x

    silver_day1 = build_silver(day1_source)
    silver_day1.head()
    return build_silver, silver_day1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Build Day 1 Gold

    We will create:
    - `dim_region`
    - `dim_smoker`
    - `fact_insurance`
    - a simple mart by region
    """)
    return


@app.cell
def _(silver_day1):
    def build_gold(silver_df):
        # Dimensions
        dim_region = (
            silver_df[["region"]]
            .drop_duplicates()
            .sort_values("region")
            .reset_index(drop=True)
        )
        dim_region["region_id"] = range(1, len(dim_region) + 1)
        dim_region = dim_region[["region_id", "region"]]

        dim_smoker = (
            silver_df[["smoker"]]
            .drop_duplicates()
            .sort_values("smoker")
            .reset_index(drop=True)
        )
        dim_smoker["smoker_id"] = range(1, len(dim_smoker) + 1)
        dim_smoker = dim_smoker[["smoker_id", "smoker"]]

        # Fact
        fact = (
            silver_df
            .merge(dim_region, on="region", how="left")
            .merge(dim_smoker, on="smoker", how="left")
        )
        fact = fact[["record_id", "region_id", "smoker_id", "charges", "year", "updated_at"]]

        # Mart
        mart_region = (
            fact.merge(dim_region, on="region_id", how="left")
            .groupby("region", as_index=False)["charges"]
            .mean()
            .rename(columns={"charges": "avg_charges"})
        )

        return dim_region, dim_smoker, fact, mart_region

    dim_region_d1, dim_smoker_d1, fact_day1, mart_region_day1 = build_gold(silver_day1)

    fact_day1.head()
    return build_gold, fact_day1, mart_region_day1


@app.cell
def _(mart_region_day1):
    mart_region_day1
    return


@app.cell
def _(mart_region_day1, plt):
    plt.figure(figsize=(8, 5))
    plt.bar(mart_region_day1["region"], mart_region_day1["avg_charges"])
    plt.title("Day 1 Gold Mart — Average Charges by Region")
    plt.xlabel("Region")
    plt.ylabel("Average charges")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Day 1 validation

    A production pipeline must validate every run.
    We check:
    - row counts
    - NULL keys
    - Silver vs Gold sums
    """)
    return


@app.cell
def _(day1_source, fact_day1, pd, silver_day1):
    validation_day1 = pd.DataFrame({
        "metric": [
            "day1_source_rows",
            "silver_day1_rows",
            "fact_day1_rows",
            "null_region_id",
            "null_smoker_id",
            "silver_sum_charges",
            "fact_sum_charges"
        ],
        "value": [
            len(day1_source),
            len(silver_day1),
            len(fact_day1),
            fact_day1["region_id"].isnull().sum(),
            fact_day1["smoker_id"].isnull().sum(),
            silver_day1["charges"].sum(),
            fact_day1["charges"].sum()
        ]
    })
    validation_day1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    Validation is not an optional extra.
    A pipeline that runs but produces inconsistent totals is not a success.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Day 2 — New rows, updates, and late-arriving data

    Now we simulate the real production problem:
    - 10 new rows
    - 5 updated rows
    - 3 late-arriving rows whose timestamps are earlier than the pipeline run time
    """)
    return


@app.cell
def _(base, pd):
    day2_new = base.sample(10, random_state=42).copy().reset_index(drop=True)
    day2_new["record_id"] = range(base["record_id"].max() + 1, base["record_id"].max() + 1 + len(day2_new))
    day2_new["updated_at"] = pd.Timestamp("2024-01-02 01:00:00")

    # Updated rows: same record_id, changed charges, later timestamp
    day2_updates = base.sample(5, random_state=7).copy()
    day2_updates["charges"] = day2_updates["charges"] * 1.10
    day2_updates["updated_at"] = pd.Timestamp("2024-01-02 01:30:00")

    # Late rows: arrive on Day 2 but have earlier timestamp
    day2_late = base.sample(3, random_state=99).copy()
    day2_late["record_id"] = range(
        day2_new["record_id"].max() + 1,
        day2_new["record_id"].max() + 1 + len(day2_late)
    )
    day2_late["updated_at"] = pd.Timestamp("2024-01-01 12:00:00")  # before the next pipeline run watermark

    day2_source_arrivals = pd.concat([day2_new, day2_updates, day2_late], ignore_index=True)
    day2_source_arrivals[["record_id", "charges", "updated_at"]].head(15)
    return (day2_source_arrivals,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Why state matters

    We now simulate a stored pipeline state.

    ### Example state
    - `last_run_time = 2024-01-02 00:00:00`

    A naive pipeline may do:
    `updated_at > last_run_time`

    But this can miss late-arriving rows.
    """)
    return


@app.cell
def _(pd):
    last_run_time = pd.Timestamp("2024-01-02 00:00:00")
    last_run_time
    return (last_run_time,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Naive incremental filter

    This is the common but unsafe pattern:
    only process rows strictly newer than the last run time.
    """)
    return


@app.cell
def _(day2_source_arrivals, last_run_time):
    naive_incremental = day2_source_arrivals[day2_source_arrivals["updated_at"] > last_run_time].copy()
    naive_incremental[["record_id", "updated_at"]].sort_values("updated_at").head(20)
    return (naive_incremental,)


@app.cell
def _(day2_source_arrivals, naive_incremental, pd):
    pd.DataFrame({
        "batch": ["day2 arrivals", "naive incremental"],
        "rows": [len(day2_source_arrivals), len(naive_incremental)]
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    Notice that rows arriving late with older timestamps are missed by the naive strategy.
    That means the pipeline can run “successfully” while still losing data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Safer incremental filter with sliding window

    Now we reprocess a small lookback window.

    ### Logic
    Instead of:
    `updated_at > last_run_time`

    Use:
    `updated_at > last_run_time - 1 day`
    """)
    return


@app.cell
def _(day2_source_arrivals, last_run_time, naive_incremental, pd):
    sliding_window_start = last_run_time - pd.Timedelta(days=1)

    safe_incremental = day2_source_arrivals[
        day2_source_arrivals["updated_at"] > sliding_window_start
    ].copy()

    pd.DataFrame({
        "batch": ["naive incremental", "sliding window incremental"],
        "rows": [len(naive_incremental), len(safe_incremental)]
    })
    return (safe_incremental,)


@app.cell
def _(safe_incremental):
    safe_incremental[["record_id", "updated_at"]].sort_values("updated_at").head(20)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    The sliding window strategy intentionally reprocesses some already-seen time range.
    This increases compute a bit, but protects correctness by capturing late-arriving records.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Why deduplication is required before merge

    Because the sliding window reprocesses overlapping data, duplicates may appear.
    We must deduplicate before merging into Silver.
    """)
    return


@app.cell
def _(day1_source, pd, safe_incremental):
    # Simulate overlap by combining previous day's tail with new arrivals
    incremental_candidate = pd.concat([day1_source.tail(5), safe_incremental], ignore_index=True)

    incremental_candidate[["record_id", "updated_at"]].sort_values(["record_id", "updated_at"]).head(20)
    return (incremental_candidate,)


@app.cell
def _(incremental_candidate):
    dup_counts = (
        incremental_candidate.groupby("record_id")
        .size()
        .reset_index(name="count")
        .query("count > 1")
    )
    dup_counts.head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    This is a real production pattern:
    to catch late data, we intentionally reprocess overlap.
    That overlap must be controlled with deduplication.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Deduplicate incremental batch

    We keep the latest version of each `record_id`.
    """)
    return


@app.cell
def _(incremental_candidate):
    incremental_dedup = incremental_candidate.sort_values(
        ["record_id", "updated_at"], ascending=[True, False]
    ).copy()

    incremental_dedup["rn"] = incremental_dedup.groupby("record_id").cumcount() + 1
    incremental_dedup = incremental_dedup[incremental_dedup["rn"] == 1].drop(columns=["rn"])

    incremental_dedup[["record_id", "updated_at"]].sort_values("record_id").head(20)
    return (incremental_dedup,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What happens if we skip deduplication?

    We now show the failure case explicitly.
    """)
    return


@app.cell
def _(incremental_dedup, pd, safe_incremental, silver_day1):
    silver_without_dedup = pd.concat([silver_day1, safe_incremental], ignore_index=True)
    silver_with_dedup = pd.concat([silver_day1, incremental_dedup], ignore_index=True)

    failure_compare = pd.DataFrame({
        "scenario": ["without dedup", "with dedup"],
        "row_count": [len(silver_without_dedup), len(silver_with_dedup)],
        "sum_charges": [silver_without_dedup["charges"].sum(), silver_with_dedup["charges"].sum()]
    })
    failure_compare
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    This is one of the most important Week 9 lessons:

    **MERGE without deduplication can silently inflate business metrics.**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Merge into Silver correctly

    Now we perform a proper Silver update:
    - combine previous Silver with incremental batch
    - rebuild latest record per `record_id`
    """)
    return


@app.cell
def _(build_silver, incremental_dedup, pd, silver_day1):
    silver_combined = pd.concat([silver_day1, incremental_dedup], ignore_index=True)

    silver_day2 = silver_combined.sort_values(
        ["record_id", "updated_at"], ascending=[True, False]
    ).copy()
    silver_day2["rn"] = silver_day2.groupby("record_id").cumcount() + 1
    silver_day2 = silver_day2[silver_day2["rn"] == 1].drop(columns=["rn"])

    # Re-apply Silver transformations just to be safe
    silver_day2 = build_silver(silver_day2)

    silver_day2.head()
    return (silver_day2,)


@app.cell
def _(pd, silver_day1, silver_day2):
    pd.DataFrame({
        "dataset": ["silver_day1", "silver_day2"],
        "rows": [len(silver_day1), len(silver_day2)],
        "sum_charges": [silver_day1["charges"].sum(), silver_day2["charges"].sum()]
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Build Day 2 Gold

    For teaching clarity, we will rebuild Gold from updated Silver.
    In production, this could be:
    - full rebuild
    - partition rebuild
    - true incremental Gold

    Here we use rebuild for correctness and simplicity.
    """)
    return


@app.cell
def _(build_gold, silver_day2):
    dim_region_d2, dim_smoker_d2, fact_day2, mart_region_day2 = build_gold(silver_day2)

    mart_region_day2
    return fact_day2, mart_region_day2


@app.cell
def _(mart_region_day2, plt):
    plt.figure(figsize=(8, 5))
    plt.bar(mart_region_day2["region"], mart_region_day2["avg_charges"])
    plt.title("Day 2 Gold Mart — Average Charges by Region")
    plt.xlabel("Region")
    plt.ylabel("Average charges")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Compare Day 1 vs Day 2 mart outputs

    This shows how incremental updates propagate into business-facing metrics.
    """)
    return


@app.cell
def _(mart_region_day1, mart_region_day2):
    mart_compare = mart_region_day1.merge(
        mart_region_day2,
        on="region",
        how="outer",
        suffixes=("_day1", "_day2")
    )
    mart_compare
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    A change in raw or Silver data should eventually appear in Gold and marts.
    That is the purpose of the pipeline.
    The challenge is doing this accurately, repeatedly, and efficiently.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Day 2 validation

    We validate again after the Day 2 pipeline run.
    """)
    return


@app.cell
def _(fact_day2, pd, silver_day2):
    validation_day2 = pd.DataFrame({
        "metric": [
            "silver_day2_rows",
            "fact_day2_rows",
            "null_region_id",
            "null_smoker_id",
            "silver_sum_charges",
            "fact_sum_charges"
        ],
        "value": [
            len(silver_day2),
            len(fact_day2),
            fact_day2["region_id"].isnull().sum(),
            fact_day2["smoker_id"].isnull().sum(),
            silver_day2["charges"].sum(),
            fact_day2["charges"].sum()
        ]
    })
    validation_day2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    If Silver and Gold do not reconcile after an incremental update, then the pipeline is not trustworthy.
    This is why validation must run on every batch, not just once.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # KPI drift demonstration

    We now compare:
    - a correct pipeline
    - a broken pipeline that skips late data and deduplication
    """)
    return


@app.cell
def _(
    build_gold,
    build_silver,
    naive_incremental,
    pd,
    silver_day1,
    silver_day2,
):
    # Broken path: naive incremental + no dedup
    broken_silver = pd.concat([silver_day1, naive_incremental], ignore_index=True)
    broken_fact_region, broken_fact_smoker, broken_fact, broken_mart = build_gold(
        build_silver(broken_silver)
    )

    kpi_drift = pd.DataFrame({
        "scenario": ["correct pipeline", "broken pipeline"],
        "avg_total_charge": [
            silver_day2["charges"].mean(),
            build_silver(broken_silver)["charges"].mean()
        ],
        "sum_total_charge": [
            silver_day2["charges"].sum(),
            build_silver(broken_silver)["charges"].sum()
        ]
    })
    kpi_drift
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    This is the most important production lesson:
    a broken pipeline may still produce valid-looking numbers.
    The danger is not a crash.
    The danger is **believable wrongness**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Modularity and pipeline design

    A good production pipeline is modular.

    ### Better structure
    - step_1_extract_incremental
    - step_2_clean_and_standardize
    - step_3_deduplicate
    - step_4_merge_silver
    - step_5_build_gold
    - step_6_refresh_marts
    - step_7_validate
    """)
    return


@app.cell
def _(pd):
    pipeline_steps = pd.DataFrame({
        "step": [
            "extract_incremental",
            "clean_standardize",
            "deduplicate",
            "merge_silver",
            "build_gold",
            "refresh_marts",
            "validate"
        ],
        "purpose": [
            "capture changed data",
            "enforce Silver rules",
            "keep latest truth",
            "update trusted layer",
            "rebuild business model",
            "refresh summaries",
            "protect correctness"
        ]
    })
    pipeline_steps
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Final summary

    ### What we demonstrated
    1. Day 1 initial full load
    2. Day 2 new + updated + late data
    3. naive incremental filter failure
    4. sliding window improvement
    5. deduplication before merge
    6. Silver update
    7. Gold rebuild
    8. mart refresh
    9. validation and KPI drift comparison

    ### Final lesson
    Incremental pipelines are hard because they must manage:
    - time
    - state
    - change
    - correctness

    That is what makes Week 9 production-grade.
    """)
    return


if __name__ == "__main__":
    app.run()
