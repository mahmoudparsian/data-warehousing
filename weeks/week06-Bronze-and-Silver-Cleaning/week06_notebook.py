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
    # Week 6 — Silver Layer Deep Dive (Elite Notebook)

    This notebook demonstrates a **Silver transformation pipeline** using the insurance dataset.

    ## Week 6 goals
    1. Profile Bronze-style raw data.
    2. Apply Silver transformations step by step.
    3. Validate the transformed dataset.
    4. Visualize before/after effects.
    5. Connect every cleaning decision to business impact.

    ## Core message
    You are not just cleaning data.

    You are building **trusted analytical data**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Dataset reminder

    Expected columns:
    - `age`
    - `gender`
    - `bmi`
    - `children`
    - `smoker`
    - `region`
    - `charges`

    We will intentionally simulate a few Bronze-style issues:
    - inconsistent region labels
    - missing charges
    - extreme outliers
    - duplicate rows
    """)
    return


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import duckdb

    # Load source data
    df = pd.read_csv("../week01-Foundations-SQL-for-Analytics/example_1_insurance/insurance.csv")

    # Simulate Bronze-style issues for teaching
    bronze = df.copy()

    # inconsistent categories
    bronze.loc[0, "region"] = "NE"
    bronze.loc[1, "region"] = "north-east"
    bronze.loc[2, "region"] = "Northeast"

    # missing metric
    bronze.loc[3, "charges"] = None

    # extreme outlier
    bronze.loc[4, "charges"] = 9999999

    # duplicate row
    bronze = pd.concat([bronze, bronze.iloc[[5]]], ignore_index=True)

    con = duckdb.connect()
    con.register("bronze", bronze)

    print("Bronze shape:", bronze.shape)
    bronze.head(10)
    return bronze, con, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 1 — Bronze profiling

    Before transforming anything, profile the Bronze data.

    ### Why profiling matters
    Profiling tells us:
    - where NULLs exist
    - which categories are inconsistent
    - whether outliers exist
    - whether duplicates may exist

    A strong Silver pipeline always starts with profiling.
    """)
    return


@app.cell
def _(con):
    row_count = con.execute("""
    SELECT COUNT(*) AS total_rows
    FROM bronze
    """).df()
    row_count
    return


@app.cell
def _(bronze):
    null_profile = bronze.isnull().sum().reset_index()
    null_profile.columns = ["column", "null_count"]
    null_profile
    return (null_profile,)


@app.cell
def _(null_profile, plt):
    plt.figure(figsize=(9, 5))
    plt.bar(null_profile["column"], null_profile["null_count"])
    plt.title("NULL Count by Column (Bronze)")
    plt.xlabel("Column")
    plt.ylabel("NULL count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    If the core metric `charges` is missing, the row may be unusable for cost analysis.
    NULLs are not just technical artifacts—they directly affect KPI trust.
    """)
    return


@app.cell
def _(con):
    region_profile = con.execute("""
    SELECT region, COUNT(*) AS n
    FROM bronze
    GROUP BY region
    ORDER BY n DESC, region
    """).df()
    region_profile
    return (region_profile,)


@app.cell
def _(plt, region_profile):
    plt.figure(figsize=(9, 5))
    plt.bar(region_profile["region"].astype(str), region_profile["n"])
    plt.title("Region Labels in Bronze Data")
    plt.xlabel("Region label")
    plt.ylabel("Count")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    The region field is inconsistent:
    - `NE`
    - `north-east`
    - `Northeast`
    - `northeast`

    If we group by raw region values, we split one real business category into several fake categories.
    """)
    return


@app.cell
def _(con):
    charges_profile = con.execute("""
    SELECT
        MIN(charges) AS min_charges,
        MAX(charges) AS max_charges,
        AVG(charges) AS avg_charges
    FROM bronze
    WHERE charges IS NOT NULL
    """).df()
    charges_profile
    return


@app.cell
def _(bronze, plt):
    plt.figure(figsize=(9, 5))
    plt.hist(bronze["charges"].dropna(), bins=40)
    plt.title("Charges Distribution (Bronze)")
    plt.xlabel("Charges")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    A single extreme outlier can distort the mean heavily.
    This means KPI design and data cleaning are deeply connected.
    """)
    return


@app.cell
def _(con):
    duplicate_check = con.execute("""
    SELECT age, gender, bmi, children, smoker, region, charges, COUNT(*) AS n
    FROM bronze
    GROUP BY age, gender, bmi, children, smoker, region, charges
    HAVING COUNT(*) > 1
    ORDER BY n DESC
    """).df()
    duplicate_check
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    Duplicates are dangerous because they silently inflate:
    - counts
    - averages
    - totals
    - segment sizes

    If not removed, they can create false business conclusions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 2 — Silver transformation plan

    We will apply the following pipeline:

    1. standardize region labels
    2. handle missing charges
    3. handle outliers
    4. remove duplicates
    5. enrich data with `age_group`
    6. validate the results
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1 — Standardize region labels

    ### Decision
    This belongs in Silver because Silver is responsible for consistency.

    ### Rule
    Map multiple raw labels to one standard label.
    """)
    return


@app.cell
def _(bronze):
    silver = bronze.copy()

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

    silver["region"] = (
        silver["region"]
        .astype(str)
        .str.strip()
        .replace(region_map)
        .str.lower()
    )

    silver["region"].value_counts(dropna=False)
    return (silver,)


@app.cell
def _(bronze, pd, silver):
    before_after_regions = pd.DataFrame({
        "bronze": bronze["region"].value_counts(),
        "silver_standardized": silver["region"].value_counts()
    }).fillna(0)

    before_after_regions
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    Standardization is not cosmetic.
    It directly changes the correctness of grouped analytics such as:
    - average charges by region
    - row count by region
    - regional trends
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2 — Handle missing metric values

    ### Decision
    For this teaching notebook, remove rows where `charges` is NULL.

    ### Why?
    Because `charges` is the primary metric and we want students to see a transparent, conservative rule.
    """)
    return


@app.cell
def _(pd, silver):
    before_null_removal = len(silver)
    _silver = silver[silver["charges"].notna()].copy()
    after_null_removal = len(_silver)

    pd.DataFrame({
        "stage": ["before removing NULL charges", "after removing NULL charges"],
        "row_count": [before_null_removal, after_null_removal]
    })
    return after_null_removal, before_null_removal


@app.cell
def _(after_null_removal, before_null_removal, plt):
    plt.figure(figsize=(7, 5))
    plt.bar(["before", "after"], [before_null_removal, after_null_removal])
    plt.title("Row Count Before vs After Removing NULL Charges")
    plt.xlabel("Stage")
    plt.ylabel("Row count")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    Removing NULLs reduces data volume but increases trust in the metric.
    This is a classic trade-off in Silver design.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 3 — Handle outliers

    ### Decision
    For teaching purposes, remove rows where `charges >= 100000`.

    ### Why?
    Because extremely large values can dominate averages and obscure normal business patterns.
    """)
    return


@app.cell
def _(pd, silver):
    before_outlier = len(silver)
    silver_2 = silver[silver["charges"] < 100000].copy()
    after_outlier = len(silver_2)

    pd.DataFrame({
        "stage": ["before outlier filter", "after outlier filter"],
        "row_count": [before_outlier, after_outlier]
    })
    return (silver_2,)


@app.cell
def _(plt, silver_2):
    plt.figure(figsize=(9, 5))
    plt.hist(silver_2["charges"], bins=40)
    plt.title("Charges Distribution After Outlier Removal (Silver)")
    plt.xlabel("Charges")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    This makes the dataset easier to interpret, but it is still a business decision.
    In another domain, you might keep and flag outliers instead of removing them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 4 — Deduplicate records

    ### Decision
    Here, a duplicate means an exact duplicate across all business fields.

    ### Why this matters
    If the same event appears twice, totals and averages can be inflated.
    """)
    return


@app.cell
def _(pd, silver_2):
    before_dedup = len(silver_2)
    silver_3 = silver_2.drop_duplicates()
    after_dedup = len(silver_3)

    pd.DataFrame({
        "stage": ["before dedup", "after dedup"],
        "row_count": [before_dedup, after_dedup]
    })
    return after_dedup, before_dedup, silver_3


@app.cell
def _(after_dedup, before_dedup, plt):
    plt.figure(figsize=(7, 5))
    plt.bar(["before", "after"], [before_dedup, after_dedup])
    plt.title("Row Count Before vs After Deduplication")
    plt.xlabel("Stage")
    plt.ylabel("Row count")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    Duplicates are one of the easiest ways to create silent KPI inflation.
    Deduplication is therefore one of the most important Silver responsibilities.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 5 — Enrichment with `age_group`

    ### Decision
    Create a business-friendly grouping from a raw numeric field.

    ### Why?
    Business users often think in categories rather than continuous variables.
    """)
    return


@app.cell
def _(silver_3):
    def age_group(age):
        if age < 30:
            return "young"
        elif age < 60:
            return "adult"
        else:
            return "senior"

    silver_3["age_group"] = silver_3["age"].apply(age_group)
    silver_3[["age", "age_group"]].head(10)
    return


@app.cell
def _(plt, silver_3):
    age_group_profile = (
        silver_3["age_group"]
        .value_counts()
        .reset_index()
    )
    age_group_profile.columns = ["age_group", "count"]

    plt.figure(figsize=(7, 5))
    plt.bar(age_group_profile["age_group"], age_group_profile["count"])
    plt.title("Population by Age Group (Silver)")
    plt.xlabel("Age group")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    Enrichment makes the dataset more reusable for:
    - segmentation
    - reporting
    - dashboarding
    - downstream Gold models
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 3 — Validation checks

    Validation is what turns a transformed dataset into a trusted dataset.
    """)
    return


@app.cell
def _(bronze, pd, silver_3):
    validation = pd.DataFrame({
        "metric": [
            "bronze_row_count",
            "silver_row_count",
            "bronze_null_charges",
            "silver_null_charges",
            "bronze_distinct_region_labels",
            "silver_distinct_region_labels"
        ],
        "value": [
            len(bronze),
            len(silver_3),
            bronze["charges"].isnull().sum(),
            silver_3["charges"].isnull().sum(),
            bronze["region"].nunique(dropna=True),
            silver_3["region"].nunique(dropna=True)
        ]
    })
    validation
    return


@app.cell
def _(bronze, pd, silver_3):
    bronze_avg = bronze["charges"].dropna().mean()
    silver_avg = silver_3["charges"].mean()

    kpi_compare = pd.DataFrame({
        "layer": ["Bronze", "Silver"],
        "avg_charges": [bronze_avg, silver_avg]
    })
    kpi_compare
    return (kpi_compare,)


@app.cell
def _(kpi_compare, plt):
    plt.figure(figsize=(7, 5))
    plt.bar(kpi_compare["layer"], kpi_compare["avg_charges"])
    plt.title("Average Charges: Bronze vs Silver")
    plt.xlabel("Layer")
    plt.ylabel("Average charges")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    This is one of the most important lessons in Week 6:

    **the average changes because the data changed**

    That does not automatically mean Silver is “wrong.”
    It means Silver is applying business rules that redefine what is trusted.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 4 — Compare Bronze and Silver by region

    This helps show how standardization changes business reporting.
    """)
    return


@app.cell
def _(bronze, silver_3):
    bronze_grouped = (
        bronze.groupby("region", dropna=False)["charges"]
        .mean()
        .reset_index()
    )
    silver_grouped = (
        silver_3.groupby("region")["charges"]
        .mean()
        .reset_index()
    )

    bronze_grouped.columns = ["region", "avg_charges"]
    silver_grouped.columns = ["region", "avg_charges"]

    bronze_grouped
    return bronze_grouped, silver_grouped


@app.cell
def _(bronze_grouped, plt):
    plt.figure(figsize=(10, 5))
    plt.bar(bronze_grouped["region"].astype(str), bronze_grouped["avg_charges"])
    plt.title("Average Charges by Region (Bronze)")
    plt.xlabel("Region")
    plt.ylabel("Average charges")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(plt, silver_grouped):
    plt.figure(figsize=(8, 5))
    plt.bar(silver_grouped["region"], silver_grouped["avg_charges"])
    plt.title("Average Charges by Region (Silver)")
    plt.xlabel("Region")
    plt.ylabel("Average charges")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    In Bronze, the same region can appear under multiple labels, fragmenting the KPI.
    In Silver, the region KPI is more trustworthy because the categories are standardized.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 5 — Final Silver dataset

    At this point, Silver should be:
    - cleaner
    - more consistent
    - easier to reuse
    - validated
    """)
    return


@app.cell
def _(silver_3):
    silver_3.head(10)
    return


@app.cell
def _(silver_3):
    silver_3.info()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Final summary

    ### What we did
    1. Profiled Bronze data
    2. Standardized categories
    3. Removed missing charges
    4. Removed outliers
    5. Deduplicated rows
    6. Enriched with `age_group`
    7. Validated the result

    ### Main lesson
    Silver is not “just cleaning.”
    Silver is where you:
    - define data quality
    - encode business rules
    - make downstream analytics trustworthy
    """)
    return


if __name__ == "__main__":
    app.run()
