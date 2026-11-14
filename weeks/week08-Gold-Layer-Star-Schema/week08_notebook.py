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
    # Week 8 — Gold Layer (Elite v2 Notebook)

    This notebook is a **case-driven, end-to-end Gold modeling tutorial**.

    ## Core business story
    We already have Bronze and Silver concepts.
    Now we want to answer business questions quickly, consistently, and repeatedly.

    That means we need a **Gold layer**.

    ## Week 8 goals
    1. Start from a Silver-style dataset.
    2. Define business questions first.
    3. Define grain explicitly.
    4. Build dimensions and a fact table.
    5. Validate the Gold model.
    6. Build data marts.
    7. Compare Silver-style analysis vs Gold-style analysis.
    8. Show how modeling choices affect KPIs.

    ## Guiding principle
    You are not just building tables.

    You are defining how the business measures itself.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Business questions that should drive the Gold model

    Before building any table, we ask what the business wants to know.

    ### Example questions
    - Which regions have the highest average charges?
    - Do smokers cost more than non-smokers?
    - How do costs change over time?
    - Which age groups drive the highest costs?

    These questions imply:
    - `charges` is a core measure
    - `region`, `smoker`, `year`, and `age_group` are useful dimensions

    ### Important insight
    A strong Gold model starts from **questions → KPIs → schema**, not the other way around.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Load a Silver-style dataset

    For teaching purposes, we will start from `insurance.csv` and create a Silver-like dataset in memory.

    If you already have a true Silver table from Week 7, you can replace this step with that dataset directly.
    """)
    return


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import duckdb

    silver = pd.read_csv("../week01-Foundations-SQL-for-Analytics/example_1_insurance/insurance.csv")

    # Create a simple time attribute for teaching.
    # In a real pipeline, year would come from integrated historical data.
    silver["year"] = 2024

    # Add business-friendly features, simulating Silver enrichment
    def age_group(age):
        if age < 30:
            return "young"
        elif age < 60:
            return "adult"
        return "senior"

    def bmi_group(bmi):
        if bmi < 18.5:
            return "underweight"
        elif bmi < 25:
            return "normal"
        elif bmi < 30:
            return "overweight"
        return "obese"

    silver["age_group"] = silver["age"].apply(age_group)
    silver["bmi_group"] = silver["bmi"].apply(bmi_group)

    silver.head()
    return duckdb, pd, plt, silver


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Inspect the Silver-style dataset

    We want to confirm that the dataset looks suitable for Gold modeling:
    - clean categories
    - numeric metric
    - useful descriptive columns
    """)
    return


@app.cell
def _(silver):
    silver.info()
    return


@app.cell
def _(silver):
    silver.describe(include="all")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    Silver is flexible and detailed, but it is not yet ideal for repeated business reporting.
    An analyst can query it directly, but every dashboard would need to redefine logic repeatedly.
    That is exactly why Gold exists.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 1 — Define the grain

    ## Most important design decision
    We must explicitly define what one row in the Gold fact table represents.

    ### Chosen grain
    **One row = one person record per year**

    ### Why this is reasonable here
    - the dataset is person-level
    - `year` is included
    - we want to analyze charges across dimensions such as region and smoker

    ### Why grain matters
    If the grain is wrong:
    - totals can inflate
    - counts can become meaningless
    - marts can mislead business users
    """)
    return


@app.cell
def _(silver):
    grain_check = silver[["age", "gender", "bmi", "children", "smoker", "region", "charges", "year"]].copy()
    grain_check.head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Wrong grain demonstration (teaching moment)

    We now intentionally create a duplicate to show how grain violations affect results.
    """)
    return


@app.cell
def _(pd, silver):
    wrong_grain = silver.copy()
    wrong_grain = pd.concat([wrong_grain, wrong_grain.iloc[[0]]], ignore_index=True)

    original_sum = silver["charges"].sum()
    wrong_sum = wrong_grain["charges"].sum()

    pd.DataFrame({
        "dataset": ["correct grain dataset", "duplicated row dataset"],
        "sum_charges": [original_sum, wrong_sum],
        "row_count": [len(silver), len(wrong_grain)]
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    Notice how a duplicate row may not be obvious in a dashboard, but it changes totals immediately.
    This is why grain errors are some of the most dangerous modeling mistakes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 2 — Build Gold dimensions

    We will create these dimensions:
    - `dim_region`
    - `dim_smoker`
    - `dim_time`
    - `dim_person`

    ### Why these?
    Because they match the business questions:
    - by region
    - by smoker
    - over time
    - by person attributes / age group
    """)
    return


@app.cell
def _(silver):
    dim_region = (
        silver[["region"]]
        .drop_duplicates()
        .sort_values("region")
        .reset_index(drop=True)
    )
    dim_region["region_id"] = range(1, len(dim_region) + 1)
    dim_region = dim_region[["region_id", "region"]]
    dim_region
    return (dim_region,)


@app.cell
def _(silver):
    dim_smoker = (
        silver[["smoker"]]
        .drop_duplicates()
        .sort_values("smoker")
        .reset_index(drop=True)
    )
    dim_smoker["smoker_id"] = range(1, len(dim_smoker) + 1)
    dim_smoker = dim_smoker[["smoker_id", "smoker"]]
    dim_smoker
    return (dim_smoker,)


@app.cell
def _(silver):
    dim_time = (
        silver[["year"]]
        .drop_duplicates()
        .sort_values("year")
        .reset_index(drop=True)
    )
    dim_time["time_id"] = range(1, len(dim_time) + 1)
    dim_time = dim_time[["time_id", "year"]]
    dim_time
    return (dim_time,)


@app.cell
def _(silver):
    dim_person = silver[["age", "gender", "bmi", "children", "age_group", "bmi_group"]].copy()
    dim_person = dim_person.reset_index(drop=True)
    dim_person["person_id"] = range(1, len(dim_person) + 1)
    dim_person = dim_person[["person_id", "age", "gender", "bmi", "children", "age_group", "bmi_group"]]
    dim_person.head()
    return (dim_person,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    Dimensions should be:
    - descriptive
    - reusable
    - stable enough to support filtering and slicing

    They give business meaning to fact table measures.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 3 — Build the Gold fact table

    ### Rule
    A fact table should contain:
    - foreign keys
    - measures
    - event-like attributes that belong at the chosen grain

    In this case:
    - `person_id`
    - `region_id`
    - `smoker_id`
    - `time_id`
    - `charges`
    """)
    return


@app.cell
def _(dim_region, dim_smoker, dim_time, silver):
    gold_base = silver.copy().reset_index(drop=True)
    gold_base["person_id"] = range(1, len(gold_base) + 1)

    fact_insurance = (
        gold_base
        .merge(dim_region, on="region", how="left")
        .merge(dim_smoker, on="smoker", how="left")
        .merge(dim_time, on="year", how="left")
    )

    fact_insurance = fact_insurance[["person_id", "region_id", "smoker_id", "time_id", "charges"]]
    fact_insurance.head()
    return (fact_insurance,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Why surrogate keys matter

    Instead of joining on text like:
    - `region = 'northwest'`

    we join on:
    - `region_id = 2`

    ### Benefits
    - faster joins
    - smaller storage footprint
    - better consistency
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 4 — Validate the Gold model

    Validation is mandatory.
    A Gold layer that is fast but wrong is useless.
    """)
    return


@app.cell
def _(dim_region, dim_smoker, dim_time, fact_insurance, pd, silver):
    validation_table = pd.DataFrame({
        "metric": [
            "silver_row_count",
            "fact_row_count",
            "null_region_id",
            "null_smoker_id",
            "null_time_id",
            "dim_region_unique_rows",
            "dim_smoker_unique_rows",
            "dim_time_unique_rows"
        ],
        "value": [
            len(silver),
            len(fact_insurance),
            fact_insurance["region_id"].isnull().sum(),
            fact_insurance["smoker_id"].isnull().sum(),
            fact_insurance["time_id"].isnull().sum(),
            len(dim_region),
            len(dim_smoker),
            len(dim_time)
        ]
    })
    validation_table
    return


@app.cell
def _(fact_insurance, pd, silver):
    silver_sum = silver["charges"].sum()
    fact_sum = fact_insurance["charges"].sum()

    pd.DataFrame({
        "layer": ["silver", "fact_insurance"],
        "sum_charges": [silver_sum, fact_sum]
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    The fact table should preserve the core numerical truth from Silver.
    If totals do not reconcile, then the Gold model is broken.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 5 — Register Gold tables in DuckDB

    We now simulate a simple warehouse environment and run Gold queries against it.
    """)
    return


@app.cell
def _(dim_person, dim_region, dim_smoker, dim_time, duckdb, fact_insurance):
    con = duckdb.connect()
    con.register("fact_insurance", fact_insurance)
    con.register("dim_region", dim_region)
    con.register("dim_smoker", dim_smoker)
    con.register("dim_time", dim_time)
    con.register("dim_person", dim_person)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 6 — Gold query vs Silver query

    We now compare a business question answered in:
    - Silver directly
    - Gold star schema

    This helps students see why Gold exists.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Business question
    What is the average charge by region?
    """)
    return


@app.cell
def _(silver):
    silver_region = (
        silver.groupby("region")["charges"]
        .mean()
        .reset_index(name="avg_charges")
    )
    silver_region
    return


@app.cell
def _(con):
    gold_region = con.execute('''
    SELECT r.region,
           AVG(f.charges) AS avg_charges
    FROM fact_insurance f
    JOIN dim_region r ON f.region_id = r.region_id
    GROUP BY r.region
    ORDER BY avg_charges DESC
    ''').df()

    gold_region
    return (gold_region,)


@app.cell
def _(gold_region, plt):
    plt.figure(figsize=(8, 5))
    plt.bar(gold_region["region"], gold_region["avg_charges"])
    plt.title("Average Charges by Region (Gold)")
    plt.xlabel("Region")
    plt.ylabel("Average charges")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    Silver can answer the question, but Gold answers it in a structured, reusable, governed way.
    That is the core value of Gold modeling.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 7 — Build Gold data marts

    Data marts are business-facing summary tables.
    They make common dashboard queries faster and simpler.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Mart 1 — Region summary
    This mart supports the question:
    - Which regions are most expensive?
    """)
    return


@app.cell
def _(con):
    mart_region_summary = con.execute('''
    SELECT r.region,
           AVG(f.charges) AS avg_charges,
           SUM(f.charges) AS total_charges,
           COUNT(*) AS population
    FROM fact_insurance f
    JOIN dim_region r ON f.region_id = r.region_id
    GROUP BY r.region
    ORDER BY avg_charges DESC
    ''').df()

    mart_region_summary
    return (mart_region_summary,)


@app.cell
def _(mart_region_summary, plt):
    plt.figure(figsize=(8, 5))
    plt.bar(mart_region_summary["region"], mart_region_summary["avg_charges"])
    plt.title("Gold Mart: Average Charges by Region")
    plt.xlabel("Region")
    plt.ylabel("Average charges")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Mart 2 — Smoker summary
    This mart supports:
    - smoker vs non-smoker cost analysis
    """)
    return


@app.cell
def _(con):
    mart_smoker_summary = con.execute('''
    SELECT s.smoker,
           AVG(f.charges) AS avg_charges,
           SUM(f.charges) AS total_charges,
           COUNT(*) AS population
    FROM fact_insurance f
    JOIN dim_smoker s ON f.smoker_id = s.smoker_id
    GROUP BY s.smoker
    ORDER BY avg_charges DESC
    ''').df()

    mart_smoker_summary
    return (mart_smoker_summary,)


@app.cell
def _(mart_smoker_summary, plt):
    plt.figure(figsize=(7, 5))
    plt.bar(mart_smoker_summary["smoker"], mart_smoker_summary["avg_charges"])
    plt.title("Gold Mart: Average Charges by Smoker")
    plt.xlabel("Smoker")
    plt.ylabel("Average charges")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Mart 3 — Time trend
    This mart supports:
    - trend analysis over time
    """)
    return


@app.cell
def _(con):
    mart_year_summary = con.execute('''
    SELECT t.year,
           AVG(f.charges) AS avg_charges,
           SUM(f.charges) AS total_charges,
           COUNT(*) AS population
    FROM fact_insurance f
    JOIN dim_time t ON f.time_id = t.time_id
    GROUP BY t.year
    ORDER BY t.year
    ''').df()

    mart_year_summary
    return (mart_year_summary,)


@app.cell
def _(mart_year_summary, plt):
    plt.figure(figsize=(7, 5))
    plt.plot(mart_year_summary["year"], mart_year_summary["avg_charges"], marker="o")
    plt.title("Gold Mart: Average Charges by Year")
    plt.xlabel("Year")
    plt.ylabel("Average charges")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    Marts are optimized answers to repeated business questions.
    They are one of the main reasons Gold is valuable in practice.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 8 — Multi-dimensional Gold analysis

    Now we show that Gold makes more complex slicing straightforward.
    """)
    return


@app.cell
def _(con):
    mart_region_smoker_time = con.execute('''
    SELECT r.region,
           s.smoker,
           t.year,
           AVG(f.charges) AS avg_charges
    FROM fact_insurance f
    JOIN dim_region r ON f.region_id = r.region_id
    JOIN dim_smoker s ON f.smoker_id = s.smoker_id
    JOIN dim_time t ON f.time_id = t.time_id
    GROUP BY r.region, s.smoker, t.year
    ORDER BY r.region, s.smoker, t.year
    ''').df()

    mart_region_smoker_time.head(12)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    This is where Gold becomes powerful:
    simple SQL can answer multi-dimensional questions because the model was designed correctly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 9 — KPI design and ambiguity

    Gold is not just structure.
    It is where metric definitions are standardized.

    ### Example KPI
    Average charges

    ### Questions you must answer
    - include outliers?
    - include all years together or by year?
    - count one record per person or per event?
    - what happens if duplicates exist?
    """)
    return


@app.cell
def _(pd):
    # Numerical teaching example
    kpi_example = pd.DataFrame({
        "charges": [100, 200, 300, 10000]
    })

    kpi_with_outlier = kpi_example["charges"].mean()
    kpi_without_outlier = kpi_example[kpi_example["charges"] < 1000]["charges"].mean()

    pd.DataFrame({
        "scenario": ["include outlier", "exclude outlier"],
        "avg_charges": [kpi_with_outlier, kpi_without_outlier]
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    The KPI is not an objective fact floating in space.
    It depends on modeling rules and inclusion criteria.
    That is why KPI logic belongs in Gold, not scattered across dashboards.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 10 — Performance discussion

    Gold exists partly for correctness, but also for speed.

    ### Why Gold is faster
    - smaller, curated tables
    - surrogate-key joins
    - reusable marts
    - fewer repeated calculations
    """)
    return


@app.cell
def _(fact_insurance, mart_region_summary, pd, silver):
    # Compare a simple Silver-style query and Gold-style mart usage conceptually
    silver_query_rows = len(silver)
    gold_fact_rows = len(fact_insurance)
    gold_mart_rows = len(mart_region_summary)

    pd.DataFrame({
        "object": ["silver table", "gold fact", "gold mart_region_summary"],
        "row_count": [silver_query_rows, gold_fact_rows, gold_mart_rows]
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    A mart may be much smaller than either Silver or the fact table.
    That reduction in size often means much faster dashboards.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 11 — Failure modes in Gold modeling

    A Gold layer can still fail if modeling choices are poor.
    """)
    return


@app.cell
def _(pd):
    failure_modes = pd.DataFrame({
        "failure_mode": [
            "wrong grain",
            "duplicate facts",
            "missing dimension key",
            "inconsistent KPI logic",
            "text-based joins"
        ],
        "business_effect": [
            "wrong totals/counts",
            "inflated KPIs",
            "missing rows in reports",
            "different dashboards disagree",
            "slow and fragile queries"
        ]
    })
    failure_modes
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    Most Gold failures are dangerous because they can still produce a dashboard that looks professional.
    The problem is not visual quality.
    The problem is business truth.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 12 — Mini design exercise inside the notebook

    ### Given
    A Silver table with:
    - age
    - region
    - smoker
    - charges
    - year

    ### Design challenge
    - write the grain as a sentence
    - list 3 dimensions
    - define 2 marts
    - explain one KPI risk

    This is the thinking pattern students should learn.
    """)
    return


@app.cell
def _():
    design_exercise = {
        "grain": "one row = one person per year",
        "dimensions": ["dim_region", "dim_smoker", "dim_time"],
        "marts": ["mart_region_summary", "mart_smoker_summary"],
        "kpi_risk": "avg_charges changes if outlier policy changes"
    }
    design_exercise
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Final summary

    ## What we built
    1. Started from a Silver-style dataset
    2. Defined business questions
    3. Defined grain explicitly
    4. Built dimensions
    5. Built a fact table
    6. Validated the Gold model
    7. Created multiple marts
    8. Explored KPI design and failure modes

    ## Final message
    Gold is not just the last layer in the pipeline.

    It is the layer where:
    - business meaning is formalized
    - KPIs are governed
    - performance is optimized
    - decisions become scalable
    """)
    return


if __name__ == "__main__":
    app.run()
