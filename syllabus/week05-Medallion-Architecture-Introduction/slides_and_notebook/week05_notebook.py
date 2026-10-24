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
    # Week 5 — Medallion Architecture Notebook (Elite)

    Simulate Bronze → Silver → Gold pipeline using insurance data.

    Goal: Understand how the SAME data evolves across layers.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup
    """)
    return


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import duckdb

    con = duckdb.connect()
    return con, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Load Raw Data (Bronze Layer)
    """)
    return


@app.cell
def _(pd):
    df = pd.read_csv("../../week01-Foundations-SQL-for-Analytics/example_1_insurance/insurance.csv")

    # Simulate messy data
    df.loc[0, "region"] = "NE"
    df.loc[1, "region"] = "north-east"
    df.loc[2, "charges"] = None

    bronze = df.copy()
    bronze.head()
    return (bronze,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Bronze Characteristics
    - raw
    - messy
    - unclean
    - preserved
    """)
    return


@app.cell
def _(bronze):
    bronze["region"].value_counts(dropna=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Silver Layer — Cleaning
    """)
    return


@app.cell
def _(bronze):
    silver = bronze.copy()

    # Clean region
    region_map = {
        "NE": "northeast",
        "north-east": "northeast"
    }
    silver["region"] = silver["region"].replace(region_map).str.lower()

    # Remove null charges
    silver = silver[silver["charges"].notna()]

    # Derived column
    def age_group(age):
        if age < 30:
            return "young"
        elif age < 60:
            return "adult"
        else:
            return "senior"

    silver["age_group"] = silver["age"].apply(age_group)

    silver.head()
    return (silver,)


@app.cell
def _(silver):
    silver["region"].value_counts()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Insight
    Cleaning merges categories → affects analytics
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Compare Bronze vs Silver
    """)
    return


@app.cell
def _(bronze, pd, silver):
    compare = pd.DataFrame({
        "bronze_regions": bronze["region"].value_counts(),
        "silver_regions": silver["region"].value_counts()
    }).fillna(0)

    compare
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Gold Layer — Star Schema
    """)
    return


@app.cell
def _(silver):
    # dim_region
    dim_region = silver[["region"]].drop_duplicates().reset_index(drop=True)
    dim_region["region_id"] = range(1, len(dim_region)+1)

    # dim_person
    dim_person = silver[["age","gender","bmi","children","age_group"]].copy()
    dim_person["person_id"] = range(1, len(dim_person)+1)

    # fact
    fact = silver.copy().reset_index(drop=True)
    fact["person_id"] = dim_person["person_id"]

    fact = fact.merge(dim_region, on="region")

    fact = fact[["person_id","region_id","charges"]]

    fact.head()
    return dim_person, dim_region, fact


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Insight
    Gold = structured, optimized for queries
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Register Tables
    """)
    return


@app.cell
def _(con, dim_person, dim_region, fact):
    con.register("fact", fact)
    con.register("dim_region", dim_region)
    con.register("dim_person", dim_person)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## OLAP Query — Revenue by Region
    """)
    return


@app.cell
def _(con):
    q = con.execute(
    """
    SELECT r.region, AVG(f.charges) avg_charge
    FROM fact f
    JOIN dim_region r ON f.region_id = r.region_id
    GROUP BY r.region
    """
    ).df()

    q
    return (q,)


@app.cell
def _(plt, q):
    plt.figure()
    plt.bar(q["region"], q["avg_charge"])
    plt.title("Avg Charges by Region (Gold Layer)")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Comparison
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    | Layer | Purpose |
    |------|--------|
    | Bronze | raw data |
    | Silver | cleaned data |
    | Gold | analytical model |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Final Insight
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Same data → different value at each layer:

    - Bronze → traceability
    - Silver → trust
    - Gold → decisions

    👉 Medallion = structured evolution of data
    """)
    return


if __name__ == "__main__":
    app.run()
