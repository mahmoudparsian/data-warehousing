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
    # Week 10 — Medallion Architecture (Elite v2 Notebook)

    ## Goal
    Demonstrate **Bronze → Silver → Gold** with:
    - messy data
    - failures (duplicates, inconsistent values)
    - incremental updates (Day 2)
    - sliding window vs naive incremental
    - KPI drift and fixes

    ## Core Message
    👉 Medallion = progressive trust
    👉 Pipelines must handle **change over time**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Load Bronze Data (CSV)
    """)
    return


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    raw = pd.read_csv("insurance_bronze_raw.csv")
    raw["updated_at"] = pd.to_datetime(raw["updated_at"])

    raw.head()
    return pd, plt, raw


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Bronze Characteristics
    - messy regions (NE, north-east, etc.)
    - inconsistent smoker values
    - duplicates
    - no guarantees

    👉 **No trust yet**
    """)
    return


@app.cell
def _(raw):
    print("Rows:", len(raw))
    print("\nRegion distribution (raw):")
    print(raw["region"].value_counts().head(10))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1 — Silver (Cleaning + Dedup)
    We:
    - standardize region + smoker
    - deduplicate by latest updated_at per customer_id
    """)
    return


@app.cell
def _(raw):
    def build_silver(df):
        x = df.copy()

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
            "southwest": "southwest"
        }

        x["region"] = x["region"].replace(region_map).str.lower()
        x["smoker"] = x["smoker"].str.lower()

        # dedup latest per customer_id
        x = x.sort_values(["customer_id", "updated_at"], ascending=[True, False])
        x["rn"] = x.groupby("customer_id").cumcount() + 1
        x = x[x["rn"] == 1].drop(columns="rn")

        return x

    silver_day1 = build_silver(raw)
    silver_day1.head()
    return build_silver, silver_day1


@app.cell
def _(silver_day1):
    print("Rows (Silver):", len(silver_day1))
    print("\nRegion distribution (silver):")
    print(silver_day1["region"].value_counts())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2 — Gold (Model + KPI)
    """)
    return


@app.cell
def _(silver_day1):
    # dimensions
    dim_region = silver_day1[["region"]].drop_duplicates().reset_index(drop=True)
    dim_region["region_id"] = range(1, len(dim_region)+1)

    dim_smoker = silver_day1[["smoker"]].drop_duplicates().reset_index(drop=True)
    dim_smoker["smoker_id"] = range(1, len(dim_smoker)+1)

    # fact
    fact = (
        silver_day1
        .merge(dim_region, on="region")
        .merge(dim_smoker, on="smoker")
    )

    fact = fact[["customer_id", "region_id", "smoker_id", "charges", "updated_at"]]

    # mart
    mart_day1 = (
        fact.merge(dim_region, on="region_id")
            .groupby("region")["charges"]
            .mean()
            .reset_index(name="avg_charges")
    )

    mart_day1
    return (mart_day1,)


@app.cell
def _(mart_day1, plt):
    plt.figure()
    plt.bar(mart_day1["region"], mart_day1["avg_charges"])
    plt.title("Day 1 KPI (Gold)")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🔁 Day 2 — Incremental Scenario

    We simulate:
    - new rows
    - updates
    - late-arriving rows
    """)
    return


@app.cell
def _(pd, raw):
    # new rows
    new_rows = raw.sample(8, random_state=1).copy()
    new_rows["customer_id"] = range(raw["customer_id"].max()+1, raw["customer_id"].max()+1+len(new_rows))
    new_rows["updated_at"] = pd.Timestamp("2024-01-04")

    # updates
    updates = raw.sample(6, random_state=2).copy()
    updates["charges"] = updates["charges"] * 1.2
    updates["updated_at"] = pd.Timestamp("2024-01-04 01:00")

    # late data (older timestamp)
    late = raw.sample(4, random_state=3).copy()
    late["customer_id"] = range(new_rows["customer_id"].max()+1, new_rows["customer_id"].max()+1+len(late))
    late["updated_at"] = pd.Timestamp("2024-01-02")

    day2 = pd.concat([new_rows, updates, late], ignore_index=True)
    day2.head()
    return (day2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Naive Incremental (FAILURE)
    """)
    return


@app.cell
def _(day2, pd):
    last_run = pd.Timestamp("2024-01-03")

    naive = day2[day2["updated_at"] > last_run]

    print("Naive rows:", len(naive))
    return (last_run,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    👉 Late data is missed → KPI becomes wrong
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Sliding Window (FIX)
    """)
    return


@app.cell
def _(day2, last_run, pd):
    safe = day2[day2["updated_at"] > last_run - pd.Timedelta(days=2)]
    print("Sliding window rows:", len(safe))
    return (safe,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Dedup BEFORE Merge
    """)
    return


@app.cell
def _(pd, raw, safe):
    combined = pd.concat([raw, safe], ignore_index=True)

    dedup = combined.sort_values(["customer_id", "updated_at"], ascending=[True, False])
    dedup["rn"] = dedup.groupby("customer_id").cumcount() + 1
    dedup = dedup[dedup["rn"] == 1].drop(columns="rn")

    dedup.head()
    return (dedup,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Rebuild Silver + Gold (Day 2)
    """)
    return


@app.cell
def _(build_silver, dedup):
    silver_day2 = build_silver(dedup)

    dim_region2 = silver_day2[["region"]].drop_duplicates().reset_index(drop=True)
    dim_region2["region_id"] = range(1, len(dim_region2)+1)

    fact2 = silver_day2.merge(dim_region2, on="region")
    fact2 = fact2[["customer_id", "region_id", "charges", "updated_at"]]   # keep keys + measures only (as on Day 1)

    mart_day2 = (
        fact2.merge(dim_region2, on="region_id")
            .groupby("region")["charges"]
            .mean()
            .reset_index(name="avg_charges")
    )

    mart_day2
    return (mart_day2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## KPI Drift Comparison
    """)
    return


@app.cell
def _(mart_day1, mart_day2):
    compare = mart_day1.merge(mart_day2, on="region", how="outer", suffixes=("_day1","_day2"))
    compare
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## FINAL MESSAGE

    ### Bronze
    data exists

    ### Silver
    data is trusted

    ### Gold
    data is usable

    ---

    ### WITH INCREMENTAL

    👉 correctness must be maintained over time

    ---

    ## FINAL TRUTH

    👉 Medallion = trust
    👉 Pipeline = preserves trust over time
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🧠 Executive Storytelling Section (Capstone)

    ## Business Question
    👉 How do data quality and pipeline design affect business decisions?

    ---

    ## What We Did

    We built a full system:

    - Bronze → raw, messy data
    - Silver → cleaned, deduplicated, standardized
    - Gold → modeled, KPI-ready

    Then we simulated:
    - new data
    - updates
    - late-arriving data

    ---

    ## Key Findings

    ### 1. Raw Data Is Misleading
    - inconsistent regions
    - duplicates
    - unreliable KPIs

    👉 Raw data should NEVER be used for decisions

    ---

    ### 2. Silver Creates Trust
    - standardized values
    - deduplication
    - consistent records

    👉 Silver = trusted foundation

    ---

    ### 3. Gold Produces Business Truth
    - structured schema
    - clear aggregations
    - stable KPIs

    👉 Gold = decision-ready data

    ---

    ### 4. Pipelines Must Handle Change

    We showed:

    - naive incremental → misses late data
    - no dedup → duplicates inflate KPI

    👉 pipelines must handle:
    - time
    - updates
    - late data

    ---

    ## KPI Impact

    Bad pipeline:
    - inflated or missing values

    Correct pipeline:
    - consistent KPI
    - reliable insights

    ---

    ## Business Insight Example

    KPI:
    👉 average charges by region

    Insight:
    👉 some regions have significantly higher costs

    Decision:
    👉 adjust pricing, policy, or resource allocation

    ---

    ## Final Executive Message

    👉 Data systems are NOT about storage

    👉 They are about:

    - trust
    - consistency
    - decision-making

    ---

    ## Final Truth

    Bronze → data exists
    Silver → data is trusted
    Gold → data drives decisions

    ---

    👉 If KPI is wrong, the decision is wrong
    """)
    return


if __name__ == "__main__":
    app.run()
