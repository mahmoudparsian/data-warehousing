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
    # 🧭 Insurance Data EDA for Data Warehousing
    ## A Teaching-Grade Notebook for Bronze → Silver Readiness

    This notebook performs a **comprehensive Exploratory Data Analysis (EDA)** on messy insurance data across four years.

    The purpose is not just to “look at the data.”
    The purpose is to answer this warehouse question:

    > **What problems exist in Bronze, and what Silver business rules do we need?**

    ---

    ## Dataset

    Expected files:

    ```text
    data_messy/insurance.2021.messy.csv
    data_messy/insurance.2022.messy.csv
    data_messy/insurance.2023.messy.csv
    data_messy/insurance.2024.messy.csv
    ```

    Columns:

    ```text
    age, gender, bmi, children, smoker, region, charges
    ```

    ---

    ## Business Rules We Will Validate

    | Rule | Business Meaning | Silver Action |
    |---|---|---|
    | Age validity | Age must be realistic | Reject invalid |
    | BMI validity | BMI must be realistic | Reject invalid |
    | Charges validity | Charges cannot be negative/missing | Reject invalid |
    | Children count | Children must be realistic | Reject invalid |
    | Region domain | Keep valid/new regions, standardize messy regions | Standardize / reject |
    | Gender/smoker domains | Only approved category values | Standardize / reject |
    | Duplicates | Duplicate records inflate metrics | Deduplicate |
    | Semantic consistency | Smokers should generally have higher charges | Flag anomalies |

    ---

    ## Learning Goals

    By the end of this notebook, students should be able to:

    1. Perform EDA from a **data warehouse perspective**
    2. Identify data quality problems in Bronze
    3. Translate EDA findings into Silver business rules
    4. Understand why raw data must not flow directly into Gold analytics

    ## Valid Regions

    * southwest
    * southeast
    * northwest
    * northeast
    * south
    * north
    * midwest
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Part 1 — Environment Setup
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 01 — Import libraries and connect to DuckDB

    ### What are we doing?
    We import Python libraries and create a DuckDB connection.

    ### Why?
    DuckDB gives us SQL analytics inside Python, which is ideal for teaching warehouse-style EDA.

    ### DW value
    This simulates a small analytical warehouse where we can build Bronze, Silver, and Gold layers.
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import matplotlib.pyplot as plt

    con = duckdb.connect("insurance_dw_eda_teaching.duckdb")

    print("DuckDB version:", duckdb.__version__)
    return con, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 02 — Define input files

    ### What are we doing?
    We define the four yearly messy CSV files.

    ### Why?
    In real warehouses, data often arrives as partitioned files by year, month, or batch.

    ### DW value
    Tracking file/year lineage helps us debug data quality issues.
    """)
    return


@app.cell
def _():
    files = {
        2021: "data_messy/insurance.2021.messy.csv",
        2022: "data_messy/insurance.2022.messy.csv",
        2023: "data_messy/insurance.2023.messy.csv",
        2024: "data_messy/insurance.2024.messy.csv",
    }

    files
    return (files,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 03 — Create warehouse schemas

    ### What are we doing?
    We create schemas for the medallion layers.

    ### Why?
    Schemas separate responsibilities:

    - `bronze` = raw data
    - `silver` = cleaned and validated data
    - `gold` = analytics-ready data

    ### DW value
    This creates a professional warehouse organization even for a small teaching dataset.
    """)
    return


@app.cell
def _(con):
    con.execute("CREATE SCHEMA IF NOT EXISTS bronze;").fetchall()
    con.execute("CREATE SCHEMA IF NOT EXISTS silver;").fetchall()
    con.execute("CREATE SCHEMA IF NOT EXISTS gold;").fetchall()

    con.execute("""
    SELECT schema_name
    FROM information_schema.schemata
    WHERE schema_name IN ('bronze', 'silver', 'gold')
    ORDER BY schema_name;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Part 2 — Bronze Ingestion
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 04 — Load messy files into Bronze

    ### What are we doing?
    We load each messy CSV file into a separate Bronze table.

    ### Why?
    Bronze should preserve raw source values as much as possible.

    ### DW value
    We add technical lineage fields:

    - `source_year`
    - `source_file`
    - `raw_row_id`

    These help trace every problem back to the original source.
    """)
    return


@app.cell
def _(con, files):
    for year, path in files.items():
        con.execute(f"""
        CREATE OR REPLACE TABLE bronze.insurance_{year}_raw AS
        SELECT
            {year} AS source_year,
            '{path}' AS source_file,
            ROW_NUMBER() OVER () AS raw_row_id,
            *
        FROM read_csv_auto('{path}', header=true, all_varchar=true);
        """)

    con.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'bronze'
    ORDER BY table_name;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 05 — Combine yearly Bronze tables

    ### What are we doing?
    We combine all four yearly raw tables into one unified Bronze table.

    ### Why?
    EDA is more powerful when we can compare all years together.

    ### DW value
    This creates a single raw landing table while preserving year-level lineage.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE bronze.insurance_raw AS
    SELECT * FROM bronze.insurance_2021_raw
    UNION ALL
    SELECT * FROM bronze.insurance_2022_raw
    UNION ALL
    SELECT * FROM bronze.insurance_2023_raw
    UNION ALL
    SELECT * FROM bronze.insurance_2024_raw;
    """).fetchall()

    con.execute("""
    SELECT
        source_year,
        COUNT(*) AS bronze_rows
    FROM bronze.insurance_raw
    GROUP BY source_year
    ORDER BY source_year;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 06 — Preview Bronze records

    ### What are we doing?
    We inspect a few rows from the raw data.

    ### Why?
    Before writing rules, we need to see what the data actually looks like.

    ### DW value
    This is our first human-readable check of the Bronze layer.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT *
    FROM bronze.insurance_raw
    ORDER BY source_year, raw_row_id
    LIMIT 12;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Part 3 — Dataset Shape and Volume EDA
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 07 — Row counts by year

    ### What are we doing?
    We count rows per source year.

    ### Why?
    Volume changes can indicate either business change or data pipeline problems.

    ### DW value
    This is a basic reconciliation check.
    """)
    return


@app.cell
def _(con, plt):
    df_year_counts = con.execute("""
    SELECT
        source_year,
        COUNT(*) AS row_count
    FROM bronze.insurance_raw
    GROUP BY source_year
    ORDER BY source_year;
    """).df()

    plt.figure(figsize=(7,4))
    plt.bar(df_year_counts["source_year"].astype(str), df_year_counts["row_count"])
    plt.title("Bronze Row Count by Year")
    plt.xlabel("Source Year")
    plt.ylabel("Rows")
    plt.tight_layout()
    plt.show()

    df_year_counts
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot interpretation

    Each bar shows how much data arrived for a year.
    If one year is unexpectedly high, duplicate injection or duplicate loading may be present.
    If one year is unexpectedly low, the extract may be incomplete.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 08 — Schema inspection

    ### What are we doing?
    We inspect the Bronze table columns and data types.

    ### Why?
    Before cleaning, we need to know what DuckDB sees.

    ### DW value
    Schema inspection detects structural drift and confirms ingestion correctness.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        column_name,
        data_type
    FROM information_schema.columns
    WHERE table_schema = 'bronze'
      AND table_name = 'insurance_raw'
    ORDER BY ordinal_position;
    """).df()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        region,
        count(*) as count
    FROM bronze.insurance_raw
    GROUP BY region
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Part 4 — Business-Rule-Aligned EDA
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 09 — Create typed helper view for EDA

    ### What are we doing?
    We create a typed view that attempts safe casts.

    ### Why?
    Bronze is stored as text. For validation, we need numeric versions of age, BMI, children, and charges.

    ### DW value
    `TRY_CAST` lets us detect unparseable values without crashing the pipeline.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE VIEW silver.insurance_profile_view AS
    SELECT
        source_year,
        source_file,
        raw_row_id,

        age AS age_raw,
        TRY_CAST(NULLIF(TRIM(age), '') AS INTEGER) AS age_num,

        LOWER(NULLIF(TRIM(gender), '')) AS gender_clean,

        bmi AS bmi_raw,
        TRY_CAST(NULLIF(TRIM(bmi), '') AS DOUBLE) AS bmi_num,

        children AS children_raw,
        TRY_CAST(NULLIF(TRIM(children), '') AS INTEGER) AS children_num,

        LOWER(NULLIF(TRIM(smoker), '')) AS smoker_clean,

        region AS region_raw,
        LOWER(TRIM(region)) AS region_trimmed,
        REPLACE(LOWER(TRIM(region)), ' ', '') AS region_standardized,

        charges AS charges_raw,
        TRY_CAST(NULLIF(TRIM(charges), '') AS DOUBLE) AS charges_num

    FROM bronze.insurance_raw;
    """).fetchall()

    con.execute("""
    SELECT *
    FROM silver.insurance_profile_view
    LIMIT 10;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 10 — Rule summary dashboard

    ### What are we doing?
    We compute all major rule violations in one table.

    ### Why?
    This gives a high-level picture of dataset health.

    ### DW value
    This is the EDA equivalent of a data quality scorecard.
    """)
    return


@app.cell
def _(con):
    # DEFINE VALID Regions
    con.execute("""
    CREATE OR REPLACE TABLE silver.dim_valid_region AS
    SELECT * FROM (VALUES
        ('northeast'),
        ('northwest'),
        ('southeast'),
        ('southwest'),
        ('midwest'),
        ('north'),
        ('south')
    ) AS t(region);
    """).fetchall()

    con.execute("""
    SELECT * 
    FROM silver.dim_valid_region
    """).df()
    return


@app.cell
def _(con):
    df_rule_summary = con.execute("""
    WITH duplicate_groups AS (
        SELECT
            age_raw, gender_clean, bmi_raw, children_raw, smoker_clean, region_raw, charges_raw,
            COUNT(*) AS cnt
        FROM silver.insurance_profile_view
        GROUP BY age_raw, gender_clean, bmi_raw, children_raw, smoker_clean, region_raw, charges_raw
        HAVING COUNT(*) > 1
    )
    SELECT 'invalid_age' AS rule_check,
           COUNT(*) AS issue_count
    FROM silver.insurance_profile_view
    WHERE age_num IS NULL OR age_num < 0 OR age_num > 120

    UNION ALL
    SELECT 'invalid_bmi',
           COUNT(*)
    FROM silver.insurance_profile_view
    WHERE bmi_num IS NULL OR bmi_num < 10 OR bmi_num > 60

    UNION ALL
    SELECT 'invalid_charges',
           COUNT(*)
    FROM silver.insurance_profile_view
    WHERE charges_num IS NULL OR charges_num < 0

    UNION ALL
    SELECT 'invalid_children',
           COUNT(*)
    FROM silver.insurance_profile_view
    WHERE children_num IS NULL OR children_num < 0 OR children_num > 10

    UNION ALL
    SELECT 'invalid_gender',
           COUNT(*)
    FROM silver.insurance_profile_view
    WHERE gender_clean NOT IN ('male', 'female')

    UNION ALL
    SELECT 'invalid_smoker',
           COUNT(*)
    FROM silver.insurance_profile_view
    WHERE smoker_clean NOT IN ('yes', 'no')

    UNION ALL

    SELECT 'invalid_region_after_standardization' AS rule,
           COUNT(*)
    FROM silver.insurance_profile_view p
    LEFT JOIN silver.dim_valid_region v
        ON p.region_standardized = v.region
    WHERE v.region IS NULL


    UNION ALL
    SELECT 'extra_duplicate_rows',
           COALESCE(SUM(cnt - 1), 0)
    FROM duplicate_groups

    UNION ALL
    SELECT 'semantic_smoker_low_charge_flags',
           COUNT(*)
    FROM silver.insurance_profile_view
    WHERE smoker_clean = 'yes'
      AND charges_num IS NOT NULL
      AND charges_num < 500;
    """).df()

    df_rule_summary
    return (df_rule_summary,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 11 — Plot rule violations

    ### What are we doing?
    We visualize the rule summary.

    ### Why?
    A chart makes it clear which rules create the most issues.

    ### DW value
    This helps prioritize Silver-layer cleaning work.
    """)
    return


@app.cell
def _(df_rule_summary, plt):
    plt.figure(figsize=(11,5))
    plt.bar(df_rule_summary["rule_check"], df_rule_summary["issue_count"])
    plt.title("Business Rule Violations Found During EDA")
    plt.xlabel("Business Rule Check")
    plt.ylabel("Issue Count")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot interpretation

    The tallest bars show which issues are most common.
    Those rules deserve special attention in Silver because they affect many records.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Part 5 — Rule-by-Rule Deep Dive
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 12 — Rule 1: Age validity

    ### Business rule
    Age must be between **0 and 120**.

    ### What are we doing?
    We find records where age is missing, not numeric, negative, or unrealistically high.

    ### Why?
    Age is a core risk factor in insurance.

    ### DW value
    Invalid ages should not flow into Gold analytics.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        source_year,
        raw_row_id,
        age_raw,
        age_num,
        gender_clean,
        smoker_clean,
        charges_raw
    FROM silver.insurance_profile_view
    WHERE age_num IS NULL OR age_num < 0 OR age_num > 120
    ORDER BY source_year, raw_row_id
    LIMIT 25;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 13 — Age distribution

    ### What are we doing?
    We plot the valid age distribution.

    ### Why?
    This helps us understand the population profile.

    ### DW value
    This supports Gold-level age grouping and segmentation.
    """)
    return


@app.cell
def _(con, plt):
    df_age = con.execute("""
    SELECT age_num AS age
    FROM silver.insurance_profile_view
    WHERE age_num BETWEEN 0 AND 120;
    """).df()

    plt.figure(figsize=(8,4))
    plt.hist(df_age["age"], bins=30)
    plt.title("Distribution of Valid Ages")
    plt.xlabel("Age")
    plt.ylabel("Number of Records")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 14 — Rule 2: BMI validity

    ### Business rule
    BMI must be between **10 and 60**.

    ### What are we doing?
    We identify BMI values that are missing, not numeric, or outside a realistic human range.

    ### Why?
    BMI is a health risk variable.

    ### DW value
    Invalid BMI values distort segmentation and risk analysis.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        source_year,
        raw_row_id,
        bmi_raw,
        bmi_num,
        age_num,
        smoker_clean,
        charges_num
    FROM silver.insurance_profile_view
    WHERE bmi_num IS NULL OR bmi_num < 10 OR bmi_num > 60
    ORDER BY source_year, raw_row_id
    LIMIT 25;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 15 — BMI distribution

    ### What are we doing?
    We plot valid BMI values.

    ### Why?
    This reveals the shape of BMI distribution and possible outliers.

    ### DW value
    This helps decide BMI group thresholds in Silver/Gold.
    """)
    return


@app.cell
def _(con, plt):
    df_bmi = con.execute("""
    SELECT bmi_num AS bmi
    FROM silver.insurance_profile_view
    WHERE bmi_num BETWEEN 10 AND 60;
    """).df()

    plt.figure(figsize=(8,4))
    plt.hist(df_bmi["bmi"], bins=30)
    plt.title("Distribution of Valid BMI")
    plt.xlabel("BMI")
    plt.ylabel("Number of Records")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 16 — Rule 3: Charges validity

    ### Business rule
    Charges must be non-negative and numeric.

    ### What are we doing?
    We detect missing, non-numeric, and negative charges.

    ### Why?
    Charges are the primary financial measure.

    ### DW value
    Bad charges directly corrupt Gold KPIs such as average charges and total charges.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        source_year,
        raw_row_id,
        charges_raw,
        charges_num,
        age_num,
        bmi_num,
        smoker_clean
    FROM silver.insurance_profile_view
    WHERE charges_num IS NULL OR charges_num < 0
    ORDER BY source_year, raw_row_id
    LIMIT 25;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 17 — Charges distribution

    ### What are we doing?
    We plot valid charges.

    ### Why?
    Insurance charges are usually skewed and may contain high-cost outliers.

    ### DW value
    This helps determine whether averages, medians, or percentiles are better Gold KPIs.
    """)
    return


@app.cell
def _(con, plt):
    df_charges = con.execute("""
    SELECT charges_num AS charges
    FROM silver.insurance_profile_view
    WHERE charges_num >= 0;
    """).df()

    plt.figure(figsize=(8,4))
    plt.hist(df_charges["charges"], bins=40)
    plt.title("Distribution of Valid Charges")
    plt.xlabel("Charges")
    plt.ylabel("Number of Records")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 18 — Rule 4: Children count validity

    ### Business rule
    Children must be between **0 and 10**.

    ### What are we doing?
    We detect unrealistic or invalid children counts.

    ### Why?
    Children count is used in insurance pricing and family coverage analysis.

    ### DW value
    Invalid values distort segmentation and pricing analysis.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        source_year,
        raw_row_id,
        children_raw,
        children_num,
        age_num,
        charges_num
    FROM silver.insurance_profile_view
    WHERE children_num IS NULL OR children_num < 0 OR children_num > 10
    ORDER BY source_year, raw_row_id
    LIMIT 25;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 19 — Children distribution

    ### What are we doing?
    We show valid children counts.

    ### Why?
    This is a discrete variable, so a bar chart is appropriate.

    ### DW value
    This helps build family-size segmentation.
    """)
    return


@app.cell
def _(con, plt):
    df_children = con.execute("""
    SELECT
        children_num AS children,
        COUNT(*) AS row_count
    FROM silver.insurance_profile_view
    WHERE children_num BETWEEN 0 AND 10
    GROUP BY children_num
    ORDER BY children_num;
    """).df()

    plt.figure(figsize=(7,4))
    plt.bar(df_children["children"].astype(str), df_children["row_count"])
    plt.title("Distribution of Valid Children Count")
    plt.xlabel("Children")
    plt.ylabel("Number of Records")
    plt.tight_layout()
    plt.show()

    df_children
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 20 — Rule 5: Region standardization

    ### Business rule
    Valid regions are:

    ```text
    northeast, northwest, southeast, southwest, midwest, north, south
    ```

    But formatting issues such as `north east` and `south west` should be standardized, not rejected.

    ### What are we doing?
    We compare raw region values with standardized region values.

    ### Why?
    This teaches the difference between **messy formatting** and **invalid business values**.

    ### DW value
    Proper standardization prevents false categories in dashboards.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        region_raw,
        region_trimmed,
        region_standardized,
        COUNT(*) AS row_count
    FROM silver.insurance_profile_view
    GROUP BY region_raw, region_trimmed, region_standardized
    ORDER BY row_count DESC, region_raw
    LIMIT 50;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 21 — Region before vs after standardization

    ### What are we doing?
    We compare distinct raw regions to distinct standardized valid regions.

    ### Why?
    This shows how Silver cleaning reduces category chaos.

    ### DW value
    Cleaner categories create more reliable dimension tables and dashboards.
    """)
    return


@app.cell
def _(con, plt):
    df_region_compare = con.execute("""
    SELECT 'raw_distinct_regions' AS metric, COUNT(DISTINCT region_raw) AS value
    FROM silver.insurance_profile_view
    UNION ALL
    SELECT 'standardized_distinct_regions',
           COUNT(DISTINCT region_standardized)
    FROM silver.insurance_profile_view
    UNION ALL
    SELECT 'valid_standardized_regions',
           COUNT(DISTINCT region_standardized)
    FROM silver.insurance_profile_view
    WHERE region_standardized IN (
        'northeast','northwest','southeast','southwest',
        'midwest','north','south'
    );
    """).df()

    plt.figure(figsize=(8,4))
    plt.bar(df_region_compare["metric"], df_region_compare["value"])
    plt.title("Region Category Count: Before vs After Standardization")
    plt.xlabel("Metric")
    plt.ylabel("Distinct Count")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.show()

    df_region_compare
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot interpretation

    If raw regions have many distinct forms but standardized regions collapse to fewer categories, Silver cleaning is successfully reducing noise while preserving valid business meaning.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 22 — Invalid regions after standardization

    ### What are we doing?
    We find regions that remain invalid even after trimming, lowercasing, and removing spaces.

    ### Why?
    Values like `mars` are not formatting issues; they are invalid business values.

    ### DW value
    These records should be rejected or flagged in Silver.
    """)
    return


@app.cell
def _(con):
    con.execute("""

    WITH cleaned AS (

        SELECT

            region_raw,

            -- 🔧 full standardization

            REPLACE(

                REPLACE(LOWER(TRIM(region_raw)), ' ', ''),

                '-', ''

            ) AS region_standardized

        FROM silver.insurance_profile_view

    )

    SELECT

        c.region_raw,

        c.region_standardized,

        COUNT(*) AS row_count

    FROM cleaned c

    LEFT JOIN silver.dim_valid_region v

        ON c.region_standardized = v.region

    -- ❌ keep only invalid regions

    WHERE v.region IS NULL

    GROUP BY

        c.region_raw,

        c.region_standardized

    ORDER BY row_count DESC;

    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 23 — Rule 6: Gender and smoker domain integrity

    ### Business rule
    - gender must be `male` or `female`
    - smoker must be `yes` or `no`

    ### What are we doing?
    We inspect category values and invalid counts.

    ### Why?
    These fields are important dimensions for insurance analysis.

    ### DW value
    Invalid categories create incorrect groups in Gold dashboards.
    """)
    return


@app.cell
def _(con, mo):
    print("Gender profile:")
    mo.output.append(con.execute("""
    SELECT
        gender_clean,
        COUNT(*) AS row_count
    FROM silver.insurance_profile_view
    GROUP BY gender_clean
    ORDER BY row_count DESC;
    """).df())

    print("Smoker profile:")
    mo.output.append(con.execute("""
    SELECT
        smoker_clean,
        COUNT(*) AS row_count
    FROM silver.insurance_profile_view
    GROUP BY smoker_clean
    ORDER BY row_count DESC;
    """).df())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 24 — Rule 7: Duplicate records

    ### Business rule
    Duplicate rows should not exist.

    ### What are we doing?
    We find duplicate groups and extra duplicate rows.

    ### Why?
    Duplicates inflate row counts and distort averages.

    ### DW value
    Deduplication is a core Silver-layer responsibility.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    WITH duplicate_groups AS (
        SELECT
            age_raw, gender_clean, bmi_raw, children_raw, smoker_clean, region_raw, charges_raw,
            COUNT(*) AS cnt
        FROM silver.insurance_profile_view
        GROUP BY age_raw, gender_clean, bmi_raw, children_raw, smoker_clean, region_raw, charges_raw
        HAVING COUNT(*) > 1
    )
    SELECT
        COUNT(*) AS duplicate_groups,
        COALESCE(SUM(cnt - 1), 0) AS extra_duplicate_rows
    FROM duplicate_groups;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 25 — Example duplicate groups

    ### What are we doing?
    We show examples of duplicate values.

    ### Why?
    Students should see what duplicate records look like.

    ### DW value
    This supports the decision to deduplicate in Silver.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        age_raw,
        gender_clean,
        bmi_raw,
        children_raw,
        smoker_clean,
        region_raw,
        charges_raw,
        COUNT(*) AS duplicate_count
    FROM silver.insurance_profile_view
    GROUP BY age_raw, gender_clean, bmi_raw, children_raw, smoker_clean, region_raw, charges_raw
    HAVING COUNT(*) > 1
    ORDER BY duplicate_count DESC
    LIMIT 20;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 26 — Rule 8: Semantic consistency

    ### Business rule
    Smokers generally should have higher charges than non-smokers.

    ### What are we doing?
    We compare average charges by smoker status and flag unusually low smoker charges.

    ### Why?
    Some issues are not invalid by type or domain, but suspicious by business meaning.

    ### DW value
    Semantic anomalies may be flagged rather than rejected.
    """)
    return


@app.cell
def _(con, plt):
    df_smoker = con.execute("""
    SELECT
        smoker_clean AS smoker,
        COUNT(*) AS row_count,
        ROUND(AVG(charges_num), 2) AS avg_charges,
        ROUND(quantile_cont(charges_num, 0.50), 2) AS median_charges
    FROM silver.insurance_profile_view
    WHERE charges_num IS NOT NULL
      AND charges_num >= 0
      AND smoker_clean IN ('yes', 'no')
    GROUP BY smoker_clean
    ORDER BY avg_charges DESC;
    """).df()

    plt.figure(figsize=(6,4))
    plt.bar(df_smoker["smoker"], df_smoker["avg_charges"])
    plt.title("Average Charges by Smoker Status")
    plt.xlabel("Smoker")
    plt.ylabel("Average Charges")
    plt.tight_layout()
    plt.show()

    df_smoker
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot interpretation

    If smokers have much higher average charges, this confirms the expected business relationship.
    Very low smoker charges should be investigated as possible semantic anomalies.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 27 — Low-charge smoker anomaly examples

    ### What are we doing?
    We identify smokers with unusually low charges.

    ### Why?
    These rows may be technically valid but semantically suspicious.

    ### DW value
    This creates a useful anomaly flag for Silver or Gold.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        source_year,
        raw_row_id,
        age_num,
        bmi_num,
        children_num,
        smoker_clean,
        region_raw,
        charges_num
    FROM silver.insurance_profile_view
    WHERE smoker_clean = 'yes'
      AND charges_num IS NOT NULL
      AND charges_num >= 0
      AND charges_num < 500
    ORDER BY charges_num
    LIMIT 25;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Part 6 — Cross-Year and Segment EDA
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 28 — Average charges by year

    ### What are we doing?
    We compute average charges per year.

    ### Why?
    Year-over-year trends help detect business changes or data quality issues.

    ### DW value
    This may become a Gold-level KPI.
    """)
    return


@app.cell
def _(con, plt):
    df_year = con.execute("""
    SELECT
        source_year,
        COUNT(*) AS row_count,
        ROUND(AVG(charges_num), 2) AS avg_charges
    FROM silver.insurance_profile_view
    WHERE charges_num IS NOT NULL
      AND charges_num >= 0
    GROUP BY source_year
    ORDER BY source_year;
    """).df()

    plt.figure(figsize=(7,4))
    plt.plot(df_year["source_year"].astype(str), df_year["avg_charges"], marker="o")
    plt.title("Average Charges by Year")
    plt.xlabel("Year")
    plt.ylabel("Average Charges")
    plt.tight_layout()
    plt.show()

    df_year
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 29 — Charges by region after standardization

    ### What are we doing?
    We analyze average charges by cleaned region.

    ### Why?
    Region is now an evolved domain with new valid values.

    ### DW value
    This supports a region dimension in Gold.
    """)
    return


@app.cell
def _(con, plt):
    df_region = con.execute("""
    SELECT
        region_standardized AS region,
        COUNT(*) AS row_count,
        ROUND(AVG(charges_num), 2) AS avg_charges
    FROM silver.insurance_profile_view
    WHERE charges_num IS NOT NULL
      AND charges_num >= 0
      AND region_standardized IN (
        'northeast','northwest','southeast','southwest',
        'midwest','north','south'
      )
    GROUP BY region_standardized
    ORDER BY avg_charges DESC;
    """).df()

    plt.figure(figsize=(8,4))
    plt.bar(df_region["region"], df_region["avg_charges"])
    plt.title("Average Charges by Standardized Region")
    plt.xlabel("Region")
    plt.ylabel("Average Charges")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.show()

    df_region
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 30 — Create enriched analytical view

    ### What are we doing?
    We derive age groups and BMI groups for EDA.

    ### Why?
    Business users prefer categories over raw continuous variables.

    ### DW value
    These derived fields often become Gold reporting dimensions.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE VIEW silver.insurance_eda_enriched AS
    SELECT
        *,
        CASE
            WHEN age_num < 20 THEN 'under_20'
            WHEN age_num BETWEEN 20 AND 29 THEN '20s'
            WHEN age_num BETWEEN 30 AND 39 THEN '30s'
            WHEN age_num BETWEEN 40 AND 49 THEN '40s'
            WHEN age_num BETWEEN 50 AND 59 THEN '50s'
            WHEN age_num BETWEEN 60 AND 69 THEN '60s'
            ELSE '70_plus'
        END AS age_group,
        CASE
            WHEN bmi_num < 18.5 THEN 'underweight'
            WHEN bmi_num < 25 THEN 'normal'
            WHEN bmi_num < 30 THEN 'overweight'
            ELSE 'obese'
        END AS bmi_group
    FROM silver.insurance_profile_view
    WHERE age_num BETWEEN 0 AND 120
      AND bmi_num BETWEEN 10 AND 60
      AND children_num BETWEEN 0 AND 10
      AND charges_num >= 0
      AND gender_clean IN ('male', 'female')
      AND smoker_clean IN ('yes', 'no')
      AND region_standardized IN (
        'northeast','northwest','southeast','southwest',
        'midwest','north','south'
      );
    """).fetchall()

    con.execute("""
    SELECT *
    FROM silver.insurance_eda_enriched
    LIMIT 10;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 31 — Average charges by age group

    ### What are we doing?
    We compare charges by age group.

    ### Why?
    Age is usually an important insurance cost factor.

    ### DW value
    Age group should likely be modeled as a Gold reporting attribute.
    """)
    return


@app.cell
def _(con, plt):
    df_age_group = con.execute("""
    SELECT
        age_group,
        COUNT(*) AS row_count,
        ROUND(AVG(charges_num), 2) AS avg_charges
    FROM silver.insurance_eda_enriched
    GROUP BY age_group
    ORDER BY
        CASE age_group
            WHEN 'under_20' THEN 1
            WHEN '20s' THEN 2
            WHEN '30s' THEN 3
            WHEN '40s' THEN 4
            WHEN '50s' THEN 5
            WHEN '60s' THEN 6
            ELSE 7
        END;
    """).df()

    plt.figure(figsize=(8,4))
    plt.bar(df_age_group["age_group"], df_age_group["avg_charges"])
    plt.title("Average Charges by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Average Charges")
    plt.tight_layout()
    plt.show()

    df_age_group
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 32 — Average charges by BMI group

    ### What are we doing?
    We compare charges by BMI category.

    ### Why?
    BMI is a health-risk indicator.

    ### DW value
    BMI group is useful for Gold-level segmentation.
    """)
    return


@app.cell
def _(con, plt):
    df_bmi_group = con.execute("""
    SELECT
        bmi_group,
        COUNT(*) AS row_count,
        ROUND(AVG(charges_num), 2) AS avg_charges
    FROM silver.insurance_eda_enriched
    GROUP BY bmi_group
    ORDER BY
        CASE bmi_group
            WHEN 'underweight' THEN 1
            WHEN 'normal' THEN 2
            WHEN 'overweight' THEN 3
            ELSE 4
        END;
    """).df()

    plt.figure(figsize=(8,4))
    plt.bar(df_bmi_group["bmi_group"], df_bmi_group["avg_charges"])
    plt.title("Average Charges by BMI Group")
    plt.xlabel("BMI Group")
    plt.ylabel("Average Charges")
    plt.tight_layout()
    plt.show()

    df_bmi_group
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 33 — Smoker + BMI interaction

    ### What are we doing?
    We compare average charges by BMI group and smoker status.

    ### Why?
    Risk factors often interact.

    ### DW value
    This supports multi-dimensional Gold analysis.
    """)
    return


@app.cell
def _(con, plt):
    df_bmi_smoker = con.execute("""
    SELECT
        bmi_group,
        smoker_clean AS smoker,
        COUNT(*) AS row_count,
        ROUND(AVG(charges_num), 2) AS avg_charges
    FROM silver.insurance_eda_enriched
    GROUP BY bmi_group, smoker_clean
    ORDER BY bmi_group, smoker_clean;
    """).df()

    _pivot = df_bmi_smoker.pivot(index="bmi_group", columns="smoker", values="avg_charges")

    _pivot.plot(kind="bar", figsize=(8,4))
    plt.title("Average Charges by BMI Group and Smoker Status")
    plt.xlabel("BMI Group")
    plt.ylabel("Average Charges")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.show()

    df_bmi_smoker
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 34 — Region + smoker interaction

    ### What are we doing?
    We compare charges by region and smoker status.

    ### Why?
    This combines geography and risk behavior.

    ### DW value
    This helps identify high-cost segments.
    """)
    return


@app.cell
def _(con, plt):
    df_region_smoker = con.execute("""
    SELECT
        region_standardized AS region,
        smoker_clean AS smoker,
        COUNT(*) AS row_count,
        ROUND(AVG(charges_num), 2) AS avg_charges
    FROM silver.insurance_eda_enriched
    GROUP BY region_standardized, smoker_clean
    ORDER BY region_standardized, smoker_clean;
    """).df()

    _pivot = df_region_smoker.pivot(index="region", columns="smoker", values="avg_charges")

    _pivot.plot(kind="bar", figsize=(9,4))
    plt.title("Average Charges by Region and Smoker Status")
    plt.xlabel("Region")
    plt.ylabel("Average Charges")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.show()

    df_region_smoker
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 35 — Percentile analysis

    ### What are we doing?
    We compute percentiles for charges.

    ### Why?
    Averages can be misleading when data is skewed.

    ### DW value
    Percentiles can become Gold KPIs for more robust reporting.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        ROUND(quantile_cont(charges_num, 0.25), 2) AS p25_charges,
        ROUND(quantile_cont(charges_num, 0.50), 2) AS median_charges,
        ROUND(quantile_cont(charges_num, 0.75), 2) AS p75_charges,
        ROUND(quantile_cont(charges_num, 0.90), 2) AS p90_charges,
        ROUND(quantile_cont(charges_num, 0.95), 2) AS p95_charges,
        ROUND(quantile_cont(charges_num, 0.99), 2) AS p99_charges
    FROM silver.insurance_eda_enriched;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Part 7 — EDA Findings → Silver Actions
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 36 — EDA finding to Silver action map

    ### What are we doing?
    We summarize what the EDA found and what the Silver layer should do.

    ### Why?
    EDA is only valuable if it leads to better data engineering.

    ### DW value
    This becomes the design contract for the Silver layer.
    """)
    return


@app.cell
def _(pd):
    eda_to_silver = pd.DataFrame([
        ["Invalid age", "age_num is NULL, < 0, or > 120", "Reject row"],
        ["Invalid BMI", "bmi_num is NULL, < 10, or > 60", "Reject row"],
        ["Invalid charges", "charges_num is NULL or < 0", "Reject row"],
        ["Invalid children", "children_num is NULL, < 0, or > 10", "Reject row"],
        ["Messy region formatting", "north east, SOUTHWEST, extra spaces", "Standardize"],
        ["Invalid region", "mars or unknown non-business value", "Reject row"],
        ["Invalid gender/smoker", "outside approved domain", "Reject or standardize if mapped"],
        ["Duplicates", "same full record appears more than once", "Deduplicate"],
        ["Semantic anomaly", "smoker=yes but charges unusually low", "Flag, do not necessarily reject"],
    ], columns=["EDA Finding", "Detection Logic", "Silver Action"])

    eda_to_silver
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 37 — Recommended Silver clean logic

    ### What are we doing?
    We show the core SQL pattern for the future Silver table.

    ### Why?
    This connects EDA directly to implementation.

    ### DW value
    Students can see how business rules become SQL.
    """)
    return


@app.cell
def _():
    silver_pattern = r'''
    CREATE OR REPLACE TABLE silver.insurance_clean AS
    SELECT DISTINCT
        source_year,
        age_num AS age,
        gender_clean AS gender,
        bmi_num AS bmi,
        children_num AS children,
        smoker_clean AS smoker,
        region_standardized AS region,
        charges_num AS charges,

        CASE
            WHEN smoker_clean = 'yes' AND charges_num < 500 THEN 1
            ELSE 0
        END AS semantic_low_charge_smoker_flag

    FROM silver.insurance_profile_view
    WHERE age_num BETWEEN 0 AND 120
      AND bmi_num BETWEEN 10 AND 60
      AND children_num BETWEEN 0 AND 10
      AND charges_num >= 0
      AND gender_clean IN ('male', 'female')
      AND smoker_clean IN ('yes', 'no')
      AND region_standardized IN (
          'northeast','northwest','southeast','southwest',
          'central','east','west'
      );
    '''

    print(silver_pattern)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Part 8 — Final Teaching Summary
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Final Summary

    ## What did we learn?

    This EDA found several classes of data quality issues:

    | Issue Type | Example | Silver Strategy |
    |---|---|---|
    | Invalid numeric values | age = -5, bmi = 200 | reject |
    | Invalid financial values | charges = -1000 | reject |
    | Invalid domain values | smoker = maybe, region = mars | reject |
    | Formatting issues | north east, SOUTHWEST | standardize |
    | Duplicate records | repeated full records | deduplicate |
    | Semantic anomalies | smoker=yes but charges very low | flag |

    ---

    ## Key DW lesson

    EDA is not separate from data warehousing.

    EDA tells us:

    1. what is wrong in Bronze
    2. what rules are needed in Silver
    3. what dimensions and KPIs are safe for Gold

    ---

    ## Final message for students

    > **Do not build Gold dashboards until Bronze has been explored and Silver rules are justified.**
    """)
    return


if __name__ == "__main__":
    app.run()
