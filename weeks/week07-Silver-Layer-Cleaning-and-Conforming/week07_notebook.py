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
    # Week 7 — Silver Integration & Conformance (Elite Notebook)

    This notebook demonstrates a **multi-source Silver pipeline** using a four-year insurance dataset.

    ## Week 7 goals
    1. Profile multiple source files independently.
    2. Align schemas across years.
    3. Conform inconsistent values into canonical domains.
    4. Integrate datasets with `UNION ALL`.
    5. Clean, deduplicate, and enrich the result.
    6. Validate the integrated Silver dataset.
    7. Connect pipeline decisions to KPI impact.

    ## Core message
    You are not just combining files.

    You are building **one trusted dataset from many inconsistent sources**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Expected files

    This notebook expects the following CSV files in the working directory:

    - `insurance.2021.csv`
    - `insurance.2022.csv`
    - `insurance.2023.csv`
    - `insurance.2024.csv`

    Expected columns are broadly similar to:
    - `age`
    - `gender`
    - `bmi`
    - `children`
    - `smoker`
    - `region`
    - `charges`

    If your files differ slightly, update the alignment logic below.
    """)
    return


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import duckdb

    # Update paths if needed
    f2021 = "./data_messy/insurance.2021.messy.csv"
    f2022 = "./data_messy/insurance.2022.messy.csv"
    f2023 = "./data_messy/insurance.2023.messy.csv"
    f2024 = "./data_messy/insurance.2024.messy.csv"

    y2021 = pd.read_csv(f2021)
    y2022 = pd.read_csv(f2022)
    y2023 = pd.read_csv(f2023)
    y2024 = pd.read_csv(f2024)

    print("Shapes:")
    print("2021:", y2021.shape)
    print("2022:", y2022.shape)
    print("2023:", y2023.shape)
    print("2024:", y2024.shape)
    return duckdb, pd, plt, y2021, y2022, y2023, y2024


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 1 — Simulate realistic multi-source inconsistencies

    To make the integration lesson visible, we intentionally inject a few realistic cross-source problems:
    - different region labels
    - different smoker encodings
    - one text-formatted `charges` column
    - a missing charge
    - a duplicate row
    """)
    return


@app.cell
def _(pd, y2021, y2022, y2023, y2024):
    # Work on copies so original files remain untouched in memory
    b2021 = y2021.copy()
    b2022 = y2022.copy()
    b2023 = y2023.copy()
    b2024 = y2024.copy()

    # Region inconsistencies
    if len(b2021) > 0:
        b2021.loc[b2021.index[:3], "region"] = ["NE", "north-east", "Northeast"]

    # Smoker inconsistencies
    if len(b2022) > 1:
        b2022.loc[b2022.index[:2], "smoker"] = ["Y", "N"]

    # Charges as text in one year
    b2023["charges"] = b2023["charges"].astype(str)
    if len(b2023) > 0:
        b2023.loc[b2023.index[0], "charges"] = "1,234.56"

    # Missing charge in one year
    if len(b2024) > 0:
        b2024.loc[b2024.index[0], "charges"] = None

    # Duplicate row in one year
    if len(b2024) > 5:
        b2024 = pd.concat([b2024, b2024.iloc[[5]]], ignore_index=True)

    bronze_sources = {
        2021: b2021,
        2022: b2022,
        2023: b2023,
        2024: b2024
    }

    for _yr, _df in bronze_sources.items():
        print(_yr, _df.shape)
    return b2021, b2022, b2023, b2024, bronze_sources


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 2 — Profile each Bronze source independently

    Before integrating anything, we should profile each source separately.

    ### Why?
    Because integration can hide source-specific problems.
    We need to understand:
    - row counts
    - NULL rates
    - category inconsistencies
    - type/format problems
    """)
    return


@app.cell
def _(bronze_sources, pd):
    profile_rows = []
    for _yr, _df in bronze_sources.items():
        profile_rows.append({
            "year": _yr,
            "rows": len(_df),
            "null_charges": _df["charges"].isna().sum(),
            "distinct_region_values": _df["region"].astype(str).nunique(dropna=True),
            "distinct_smoker_values": _df["smoker"].astype(str).nunique(dropna=True)
        })

    profile_df = pd.DataFrame(profile_rows).sort_values("year")
    profile_df
    return (profile_df,)


@app.cell
def _(plt, profile_df):
    plt.figure(figsize=(8, 5))
    plt.bar(profile_df["year"].astype(str), profile_df["rows"])
    plt.title("Row Count by Source File")
    plt.xlabel("Year")
    plt.ylabel("Rows")
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(plt, profile_df):
    plt.figure(figsize=(8, 5))
    plt.bar(profile_df["year"].astype(str), profile_df["null_charges"])
    plt.title("NULL Charges by Source File")
    plt.xlabel("Year")
    plt.ylabel("NULL count")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    A multi-source pipeline is only as good as its weakest source.
    Profiling by source helps identify:
    - incomplete files
    - source-specific data quality problems
    - differences that must be handled before integration
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Inspect categorical inconsistencies by source

    We now inspect region and smoker values by year.
    """)
    return


@app.cell
def _(bronze_sources):
    for _yr, _df in bronze_sources.items():
        print(f"\nYear {_yr} — region values")
        print(_df["region"].astype(str).value_counts(dropna=False).head(10))
        print(f"\nYear {_yr} — smoker values")
        print(_df["smoker"].astype(str).value_counts(dropna=False).head(10))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    This is where conformance begins.
    If equivalent business concepts have different labels across years, then:
    - grouping is wrong
    - comparisons are wrong
    - trend analysis is wrong
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 3 — Schema alignment

    Before we integrate, all sources must share:
    - the same column names
    - the same data types
    - the same broad semantics

    ### Teaching note
    Schema alignment happens **before** union.
    """)
    return


@app.cell
def _(b2021, b2022, b2023, b2024, pd):
    def align_schema(df, year):
        x = df.copy()

        # Rename if an alternate column name exists
        if "region_name" in x.columns and "region" not in x.columns:
            x = x.rename(columns={"region_name": "region"})

        # Ensure expected columns exist
        expected = ["age", "gender", "bmi", "children", "smoker", "region", "charges"]
        for col in expected:
            if col not in x.columns:
                x[col] = pd.NA

        # Align data types carefully
        x["age"] = pd.to_numeric(x["age"], errors="coerce")
        x["bmi"] = pd.to_numeric(x["bmi"], errors="coerce")
        x["children"] = pd.to_numeric(x["children"], errors="coerce")

        # charges may be text like "1,234.56"
        x["charges"] = (
            x["charges"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .replace({"None": pd.NA, "nan": pd.NA, "<NA>": pd.NA})
        )
        x["charges"] = pd.to_numeric(x["charges"], errors="coerce")

        x["gender"] = x["gender"].astype(str).str.strip()
        x["smoker"] = x["smoker"].astype(str).str.strip()
        x["region"] = x["region"].astype(str).str.strip()

        x["year"] = year

        return x[expected + ["year"]]

    a2021 = align_schema(b2021, 2021)
    a2022 = align_schema(b2022, 2022)
    a2023 = align_schema(b2023, 2023)
    a2024 = align_schema(b2024, 2024)

    a2023.head()
    return a2021, a2022, a2023, a2024


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Confirm aligned schemas

    All aligned source tables should now have the same structure.
    """)
    return


@app.cell
def _(a2021, a2022, a2023, a2024):
    for _yr, _df in {2021:a2021, 2022:a2022, 2023:a2023, 2024:a2024}.items():
        print(f"\nYear {_yr}")
        print(_df.dtypes)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    Alignment is the foundation of integration.
    If one source still has incompatible types, the union may succeed technically but fail semantically.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 4 — Conformance: canonical domains

    Now we standardize values into one agreed representation.

    ### Examples
    - `NE`, `north-east`, `Northeast` → `northeast`
    - `Y`, `1` → `yes`
    - `N`, `0` → `no`
    """)
    return


@app.cell
def _(a2021, a2022, a2023, a2024):
    def conform_values(df):
        x = df.copy()

        region_map = {
            "NE": "northeast",
            "north-east": "northeast",
            "Northeast": "northeast",
            "northeast": "northeast",
            "NW": "northwest",
            "north-west": "northwest",
            "Northwest": "northwest",
            "northwest": "northwest",
            "SE": "southeast",
            "south-east": "southeast",
            "Southeast": "southeast",
            "southeast": "southeast",
            "SW": "southwest",
            "south-west": "southwest",
            "Southwest": "southwest",
            "southwest": "southwest",
        }

        smoker_map = {
            "Y": "yes", "y": "yes", "1": "yes", "yes": "yes",
            "N": "no", "n": "no", "0": "no", "no": "no"
        }

        x["region"] = x["region"].replace(region_map).str.lower()
        x["smoker"] = x["smoker"].replace(smoker_map).str.lower()

        return x

    c2021 = conform_values(a2021)
    c2022 = conform_values(a2022)
    c2023 = conform_values(a2023)
    c2024 = conform_values(a2024)
    return c2021, c2022, c2023, c2024


@app.cell
def _(c2021, c2022, c2023, c2024):
    for _yr, _df in {2021:c2021, 2022:c2022, 2023:c2023, 2024:c2024}.items():
        print(f"\nYear {_yr} — conformed regions")
        print(_df["region"].value_counts(dropna=False))
        print(f"\nYear {_yr} — conformed smoker values")
        print(_df["smoker"].value_counts(dropna=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    Conformance gives us canonical business categories.
    Without this step, trends across years would compare labels, not realities.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 5 — Integration with `UNION ALL`

    Now that schemas and values are aligned, we can integrate all years into one combined Silver candidate table.
    """)
    return


@app.cell
def _(c2021, c2022, c2023, c2024, pd):
    silver_candidate = pd.concat([c2021, c2022, c2023, c2024], ignore_index=True)
    silver_candidate.head()
    return (silver_candidate,)


@app.cell
def _(duckdb, silver_candidate):
    con = duckdb.connect()
    con.register("silver_candidate", silver_candidate)

    rows_by_year = con.execute('''
    SELECT year, COUNT(*) AS row_count
    FROM silver_candidate
    GROUP BY year
    ORDER BY year
    ''').df()
    rows_by_year
    return (rows_by_year,)


@app.cell
def _(plt, rows_by_year):
    plt.figure(figsize=(8, 5))
    plt.bar(rows_by_year["year"].astype(str), rows_by_year["row_count"])
    plt.title("Integrated Row Count by Year")
    plt.xlabel("Year")
    plt.ylabel("Row count")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    A correct `UNION ALL` preserves source row counts while making the years analytically comparable.
    This is one of the most common real-world Silver patterns.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 6 — Cleaning after integration

    Once data is integrated, we can clean it consistently across all years.

    We will:
    1. remove NULL charges
    2. remove obvious outliers
    3. deduplicate exact duplicates
    """)
    return


@app.cell
def _(pd, silver_candidate):
    silver = silver_candidate.copy()

    before_clean_rows = len(silver)

    # Remove NULL metric
    silver = silver[silver["charges"].notna()].copy()

    # Remove obvious outliers for teaching purposes
    silver = silver[silver["charges"] < 100000].copy()

    # Deduplicate exact duplicates
    silver = silver.drop_duplicates()

    after_clean_rows = len(silver)

    pd.DataFrame({
        "stage": ["before cleaning", "after cleaning"],
        "row_count": [before_clean_rows, after_clean_rows]
    })
    return after_clean_rows, before_clean_rows, silver


@app.cell
def _(after_clean_rows, before_clean_rows, plt):
    plt.figure(figsize=(8, 5))
    plt.bar(["before", "after"], [before_clean_rows, after_clean_rows])
    plt.title("Row Count Before vs After Integrated Cleaning")
    plt.xlabel("Stage")
    plt.ylabel("Rows")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    Cleaning after integration ensures that all sources are treated under the same rules.
    This is often more consistent than cleaning each source differently.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 7 — Enrichment

    Now we add derived columns that increase business usability.

    We create:
    - `age_group`
    - `bmi_group`
    """)
    return


@app.cell
def _(pd, silver):
    def age_group(age):
        if age < 30:
            return "young"
        elif age < 60:
            return "adult"
        return "senior"

    def bmi_group(bmi):
        if pd.isna(bmi):
            return pd.NA
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
    return


@app.cell
def _(plt, silver):
    age_group_year = (
        silver.groupby(["year", "age_group"])
        .size()
        .reset_index(name="count")
    )

    for grp in age_group_year["age_group"].dropna().unique():
        subset = age_group_year[age_group_year["age_group"] == grp]
        plt.plot(subset["year"], subset["count"], marker="o", label=grp)

    plt.title("Population by Age Group Across Years")
    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.legend()
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    Enrichment converts raw attributes into business-friendly categories that can support:
    - segmentation
    - cohort analysis
    - later Gold models
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 8 — Validation

    Validation is what makes Silver trustworthy.

    We now check:
    - row counts
    - NULLs
    - distinct canonical categories
    - distribution sanity
    """)
    return


@app.cell
def _(pd, silver, silver_candidate):
    validation = pd.DataFrame({
        "metric": [
            "bronze_total_rows_all_sources",
            "silver_total_rows",
            "silver_null_charges",
            "silver_distinct_region_labels",
            "silver_distinct_smoker_labels"
        ],
        "value": [
            len(silver_candidate),
            len(silver),
            silver["charges"].isnull().sum(),
            silver["region"].nunique(dropna=True),
            silver["smoker"].nunique(dropna=True)
        ]
    })
    validation
    return


@app.cell
def _(pd, silver, silver_candidate):
    bronze_avg = silver_candidate["charges"].dropna().mean()
    silver_avg = silver["charges"].mean()

    kpi_compare = pd.DataFrame({
        "layer": ["Integrated Bronze candidate", "Silver"],
        "avg_charges": [bronze_avg, silver_avg]
    })
    kpi_compare
    return (kpi_compare,)


@app.cell
def _(kpi_compare, plt):
    plt.figure(figsize=(8, 5))
    plt.bar(kpi_compare["layer"], kpi_compare["avg_charges"])
    plt.title("Average Charges Before vs After Silver Processing")
    plt.ylabel("Average charges")
    plt.xticks(rotation=10)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    This is one of the most important lessons in Week 7:

    **integration + conformance + cleaning change KPIs**

    That is why these steps must be:
    - explicit
    - justified
    - validated
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 9 — Region KPI before vs after conformance

    This is the clearest way to show why conformance matters.
    """)
    return


@app.cell
def _(a2021, a2022, a2023, a2024, pd, silver):
    # Before conformance (aligned but not conformed)
    aligned_union = pd.concat([a2021, a2022, a2023, a2024], ignore_index=True)

    bronze_region_kpi = (
        aligned_union.groupby("region")["charges"]
        .mean()
        .reset_index(name="avg_charges")
    )

    silver_region_kpi = (
        silver.groupby("region")["charges"]
        .mean()
        .reset_index(name="avg_charges")
    )

    bronze_region_kpi
    return bronze_region_kpi, silver_region_kpi


@app.cell
def _(bronze_region_kpi, plt):
    plt.figure(figsize=(10, 5))
    plt.bar(bronze_region_kpi["region"].astype(str), bronze_region_kpi["avg_charges"])
    plt.title("Average Charges by Region Before Conformance")
    plt.xlabel("Region label")
    plt.ylabel("Average charges")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(plt, silver_region_kpi):
    plt.figure(figsize=(8, 5))
    plt.bar(silver_region_kpi["region"], silver_region_kpi["avg_charges"])
    plt.title("Average Charges by Region After Conformance")
    plt.xlabel("Canonical region")
    plt.ylabel("Average charges")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business insight
    Before conformance, one real business category can fragment into several fake reporting categories.
    After conformance, the KPI reflects the real business grouping.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 10 — Final Silver table

    At this point, the Silver dataset is:
    - integrated across years
    - standardized
    - cleaned
    - enriched
    - validated
    """)
    return


@app.cell
def _(silver):
    silver.info()
    return


@app.cell
def _(silver):
    silver.head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Final summary

    ### What we did
    1. Profiled each source independently
    2. Aligned schemas
    3. Conformed inconsistent values
    4. Integrated all years with `UNION ALL`
    5. Cleaned and deduplicated the result
    6. Added business-friendly features
    7. Validated the final Silver dataset

    ### Final lesson
    Week 7 is not just about cleaning.
    It is about making **multiple datasets agree** so that the final analytical dataset is trustworthy.
    """)
    return


if __name__ == "__main__":
    app.run()
