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
    # Exploratory Data Analysis (EDA) for Data Warehousing
    ## Insurance Dataset: 2021–2024

    This notebook performs a comprehensive **Data Warehousing-oriented EDA** using DuckDB.

    Expected files:

    ```text
    data/insurance.2021.csv
    data/insurance.2022.csv
    data/insurance.2023.csv
    data/insurance.2024.csv
    ```

    Columns:

    ```text
    age, gender, bmi, children, smoker, region, charges
    ```

    ## DW focus

    This notebook explores the data from a warehouse perspective:

    - Bronze ingestion and lineage
    - schema consistency
    - missing values
    - duplicates
    - valid domain values
    - numeric ranges and outliers
    - year-over-year patterns
    - segmentation analysis
    - Gold-layer design ideas
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 01 — Setup

    We use DuckDB for SQL-based EDA and Matplotlib for plots.
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import matplotlib.pyplot as plt

    con = duckdb.connect("insurance_dw_eda.duckdb")
    print("DuckDB version:", duckdb.__version__)
    return con, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 02 — Define source files

    Each CSV file represents one source-year extract.
    """)
    return


@app.cell
def _():
    files = {
        2021: "data/insurance.2021.csv",
        2022: "data/insurance.2022.csv",
        2023: "data/insurance.2023.csv",
        2024: "data/insurance.2024.csv",
    }

    files
    return (files,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 03 — Create warehouse schemas

    We use schemas to simulate a Medallion Architecture:

    - `bronze`: raw data
    - `silver`: typed and validated data
    - `gold`: analytics-ready summaries
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
    ## Cell 04 — Load yearly CSVs into Bronze

    Bronze keeps the raw values as strings by using `all_varchar=true`.

    We also add:

    - `source_year`
    - `source_file`
    - `raw_row_id`

    These are useful for lineage and debugging.
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
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE table_schema = 'bronze'
    ORDER BY table_name;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 05 — Combine Bronze tables

    A unified Bronze table allows cross-year EDA.
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
    SELECT source_year, COUNT(*) AS row_count
    FROM bronze.insurance_raw
    GROUP BY source_year
    ORDER BY source_year;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 06 — Row count by year

    ### Why this matters
    Row-count checks detect missing files, duplicate loads, or unexpected changes in source volume.
    """)
    return


@app.cell
def _(con, plt):
    df_counts = con.execute("""
    SELECT source_year, COUNT(*) AS row_count
    FROM bronze.insurance_raw
    GROUP BY source_year
    ORDER BY source_year;
    """).df()

    plt.figure(figsize=(7,4))
    plt.bar(df_counts["source_year"].astype(str), df_counts["row_count"])
    plt.title("Row Count by Source Year")
    plt.xlabel("Year")
    plt.ylabel("Rows")
    plt.tight_layout()
    plt.show()

    df_counts
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot interpretation

    A large year-to-year difference may be normal business growth, but it may also indicate missing or duplicated source data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 07 — Inspect Bronze schema

    Schema inspection confirms that the source columns landed correctly.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'bronze'
      AND table_name = 'insurance_raw'
    ORDER BY ordinal_position;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 08 — Preview raw data

    A quick sample helps us see values before any cleaning.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT *
    FROM bronze.insurance_raw
    ORDER BY source_year, raw_row_id
    LIMIT 10;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Bronze EDA: Data Quality Profiling
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 09 — Missing value profile

    Missing values affect joins, aggregations, and downstream KPIs.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT 'age' AS column_name, SUM(CASE WHEN NULLIF(TRIM(age), '') IS NULL THEN 1 ELSE 0 END) AS missing_count FROM bronze.insurance_raw
    UNION ALL
    SELECT 'gender', SUM(CASE WHEN NULLIF(TRIM(gender), '') IS NULL THEN 1 ELSE 0 END) FROM bronze.insurance_raw
    UNION ALL
    SELECT 'bmi', SUM(CASE WHEN NULLIF(TRIM(bmi), '') IS NULL THEN 1 ELSE 0 END) FROM bronze.insurance_raw
    UNION ALL
    SELECT 'children', SUM(CASE WHEN NULLIF(TRIM(children), '') IS NULL THEN 1 ELSE 0 END) FROM bronze.insurance_raw
    UNION ALL
    SELECT 'smoker', SUM(CASE WHEN NULLIF(TRIM(smoker), '') IS NULL THEN 1 ELSE 0 END) FROM bronze.insurance_raw
    UNION ALL
    SELECT 'region', SUM(CASE WHEN NULLIF(TRIM(region), '') IS NULL THEN 1 ELSE 0 END) FROM bronze.insurance_raw
    UNION ALL
    SELECT 'charges', SUM(CASE WHEN NULLIF(TRIM(charges), '') IS NULL THEN 1 ELSE 0 END) FROM bronze.insurance_raw
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 10 — Plot missing values

    This plot helps communicate completeness issues quickly.
    """)
    return


@app.cell
def _(con, plt):
    df_missing = con.execute("""
    SELECT 'age' AS column_name, SUM(CASE WHEN NULLIF(TRIM(age), '') IS NULL THEN 1 ELSE 0 END) AS missing_count FROM bronze.insurance_raw
    UNION ALL
    SELECT 'gender', SUM(CASE WHEN NULLIF(TRIM(gender), '') IS NULL THEN 1 ELSE 0 END) FROM bronze.insurance_raw
    UNION ALL
    SELECT 'bmi', SUM(CASE WHEN NULLIF(TRIM(bmi), '') IS NULL THEN 1 ELSE 0 END) FROM bronze.insurance_raw
    UNION ALL
    SELECT 'children', SUM(CASE WHEN NULLIF(TRIM(children), '') IS NULL THEN 1 ELSE 0 END) FROM bronze.insurance_raw
    UNION ALL
    SELECT 'smoker', SUM(CASE WHEN NULLIF(TRIM(smoker), '') IS NULL THEN 1 ELSE 0 END) FROM bronze.insurance_raw
    UNION ALL
    SELECT 'region', SUM(CASE WHEN NULLIF(TRIM(region), '') IS NULL THEN 1 ELSE 0 END) FROM bronze.insurance_raw
    UNION ALL
    SELECT 'charges', SUM(CASE WHEN NULLIF(TRIM(charges), '') IS NULL THEN 1 ELSE 0 END) FROM bronze.insurance_raw
    """).df()

    plt.figure(figsize=(8,4))
    plt.bar(df_missing["column_name"], df_missing["missing_count"])
    plt.title("Missing Values by Column")
    plt.xlabel("Column")
    plt.ylabel("Missing Count")
    plt.tight_layout()
    plt.show()

    df_missing
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot interpretation

    High missingness suggests a Silver-layer rule is needed: reject, impute, or flag.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 11 — Duplicate profile

    Duplicates can inflate counts, averages, and KPIs.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    WITH grouped AS (
        SELECT
            age, gender, bmi, children, smoker, region, charges,
            COUNT(*) AS cnt
        FROM bronze.insurance_raw
        GROUP BY age, gender, bmi, children, smoker, region, charges
        HAVING COUNT(*) > 1
    )
    SELECT
        COUNT(*) AS duplicate_groups,
        COALESCE(SUM(cnt - 1), 0) AS extra_duplicate_rows
    FROM grouped;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 12 — Categorical domain profile

    We check the distinct values for categorical columns.
    """)
    return


@app.cell
def _(con, mo):
    print("Gender values:")
    mo.output.append(con.execute("""
    SELECT gender, COUNT(*) AS row_count
    FROM bronze.insurance_raw
    GROUP BY gender
    ORDER BY row_count DESC;
    """).df())

    print("Smoker values:")
    mo.output.append(con.execute("""
    SELECT smoker, COUNT(*) AS row_count
    FROM bronze.insurance_raw
    GROUP BY smoker
    ORDER BY row_count DESC;
    """).df())

    print("Region values:")
    mo.output.append(con.execute("""
    SELECT region, COUNT(*) AS row_count
    FROM bronze.insurance_raw
    GROUP BY region
    ORDER BY row_count DESC;
    """).df())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 13 — Invalid domain checks

    Domain validation asks whether values belong to the business-approved list.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        SUM(CASE WHEN LOWER(TRIM(gender)) NOT IN ('male', 'female') THEN 1 ELSE 0 END) AS invalid_gender_rows,
        SUM(CASE WHEN LOWER(TRIM(smoker)) NOT IN ('yes', 'no') THEN 1 ELSE 0 END) AS invalid_smoker_rows,
        SUM(CASE WHEN LOWER(TRIM(region)) NOT IN ('northeast', 'northwest', 'southeast', 'southwest') THEN 1 ELSE 0 END) AS invalid_region_rows
    FROM bronze.insurance_raw;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Silver Layer: Type Conversion and Validation
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 14 — Create typed Silver table

    Bronze values are strings. Silver converts them into analytical types.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.insurance_typed AS
    SELECT
        source_year,
        source_file,
        raw_row_id,
        TRY_CAST(NULLIF(TRIM(age), '') AS INTEGER) AS age,
        LOWER(NULLIF(TRIM(gender), '')) AS gender,
        TRY_CAST(NULLIF(TRIM(bmi), '') AS DOUBLE) AS bmi,
        TRY_CAST(NULLIF(TRIM(children), '') AS INTEGER) AS children,
        LOWER(NULLIF(TRIM(smoker), '')) AS smoker,
        LOWER(NULLIF(TRIM(region), '')) AS region,
        TRY_CAST(NULLIF(TRIM(charges), '') AS DOUBLE) AS charges
    FROM bronze.insurance_raw;
    """).fetchall()

    con.execute("""
    SELECT *
    FROM silver.insurance_typed
    LIMIT 10;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 15 — Numeric and business validity checks

    Some values can be numeric but still invalid from a business perspective.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        COUNT(*) AS total_rows,
        SUM(CASE WHEN age IS NULL OR age < 0 OR age > 120 THEN 1 ELSE 0 END) AS invalid_age_rows,
        SUM(CASE WHEN bmi IS NULL OR bmi <= 0 OR bmi > 100 THEN 1 ELSE 0 END) AS invalid_bmi_rows,
        SUM(CASE WHEN children IS NULL OR children < 0 OR children > 20 THEN 1 ELSE 0 END) AS invalid_children_rows,
        SUM(CASE WHEN charges IS NULL OR charges < 0 THEN 1 ELSE 0 END) AS invalid_charges_rows,
        SUM(CASE WHEN gender NOT IN ('male', 'female') THEN 1 ELSE 0 END) AS invalid_gender_rows,
        SUM(CASE WHEN smoker NOT IN ('yes', 'no') THEN 1 ELSE 0 END) AS invalid_smoker_rows,
        SUM(CASE WHEN region NOT IN ('northeast', 'northwest', 'southeast', 'southwest') THEN 1 ELSE 0 END) AS invalid_region_rows
    FROM silver.insurance_typed;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 16 — Create clean Silver table

    This table contains trusted records for analysis.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.insurance_clean AS
    SELECT DISTINCT
        source_year,
        age,
        gender,
        bmi,
        children,
        smoker,
        region,
        charges
    FROM silver.insurance_typed
    WHERE age BETWEEN 0 AND 120
      AND bmi > 0 AND bmi <= 100
      AND children BETWEEN 0 AND 20
      AND charges >= 0
      AND gender IN ('male', 'female')
      AND smoker IN ('yes', 'no')
      AND region IN ('northeast', 'northwest', 'southeast', 'southwest');
    """).fetchall()

    con.execute("""
    SELECT
        (SELECT COUNT(*) FROM bronze.insurance_raw) AS bronze_rows,
        (SELECT COUNT(*) FROM silver.insurance_typed) AS typed_rows,
        (SELECT COUNT(*) FROM silver.insurance_clean) AS clean_rows;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 17 — Pipeline row-count funnel

    The funnel shows how many rows survive each stage.
    """)
    return


@app.cell
def _(con, plt):
    df_funnel = con.execute("""
    SELECT 'Bronze Raw' AS stage, COUNT(*) AS row_count FROM bronze.insurance_raw
    UNION ALL
    SELECT 'Silver Typed', COUNT(*) FROM silver.insurance_typed
    UNION ALL
    SELECT 'Silver Clean', COUNT(*) FROM silver.insurance_clean;
    """).df()

    plt.figure(figsize=(7,4))
    plt.bar(df_funnel["stage"], df_funnel["row_count"])
    plt.title("Insurance Data Pipeline Funnel")
    plt.xlabel("Pipeline Stage")
    plt.ylabel("Rows")
    plt.tight_layout()
    plt.show()

    df_funnel
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot interpretation

    If the clean row count is much lower than Bronze, inspect which rule removed the most records.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Descriptive EDA on Clean Silver Data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 18 — Overall numeric summary

    Summarize core numerical attributes.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        COUNT(*) AS row_count,
        MIN(age) AS min_age,
        ROUND(AVG(age), 2) AS avg_age,
        MAX(age) AS max_age,
        MIN(bmi) AS min_bmi,
        ROUND(AVG(bmi), 2) AS avg_bmi,
        MAX(bmi) AS max_bmi,
        MIN(charges) AS min_charges,
        ROUND(AVG(charges), 2) AS avg_charges,
        MAX(charges) AS max_charges
    FROM silver.insurance_clean;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 19 — Charges distribution

    A histogram shows skew and outliers in charges.
    """)
    return


@app.cell
def _(con, plt):
    df_charges = con.execute("""
    SELECT charges
    FROM silver.insurance_clean;
    """).df()

    plt.figure(figsize=(8,4))
    plt.hist(df_charges["charges"], bins=40)
    plt.title("Distribution of Insurance Charges")
    plt.xlabel("Charges")
    plt.ylabel("Number of Records")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot interpretation

    A long right tail means a small number of high-charge records can strongly affect the average.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 20 — Average charges by year

    This shows year-over-year cost patterns.
    """)
    return


@app.cell
def _(con, plt):
    df_year = con.execute("""
    SELECT
        source_year,
        COUNT(*) AS row_count,
        ROUND(AVG(charges), 2) AS avg_charges,
        ROUND(MIN(charges), 2) AS min_charges,
        ROUND(MAX(charges), 2) AS max_charges
    FROM silver.insurance_clean
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
    ### Plot interpretation

    A sharp jump or drop in a year may indicate a true business trend or a source data issue.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 21 — Average charges by smoker status

    Smoking status is often a strong cost driver.
    """)
    return


@app.cell
def _(con, plt):
    df_smoker = con.execute("""
    SELECT
        smoker,
        COUNT(*) AS row_count,
        ROUND(AVG(charges), 2) AS avg_charges
    FROM silver.insurance_clean
    GROUP BY smoker
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

    If smokers have much higher charges, `smoker` should be a key dimension or segmentation field in Gold.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 22 — Average charges by region

    Region can reveal geography-related cost differences.
    """)
    return


@app.cell
def _(con, plt):
    df_region = con.execute("""
    SELECT
        region,
        COUNT(*) AS row_count,
        ROUND(AVG(charges), 2) AS avg_charges
    FROM silver.insurance_clean
    GROUP BY region
    ORDER BY avg_charges DESC;
    """).df()

    plt.figure(figsize=(7,4))
    plt.bar(df_region["region"], df_region["avg_charges"])
    plt.title("Average Charges by Region")
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
    ### Plot interpretation

    Regional differences can guide geography-based risk analysis or operational review.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 23 — Average charges by gender

    Gender is a segmentation attribute, but results must be interpreted carefully.
    """)
    return


@app.cell
def _(con, plt):
    df_gender = con.execute("""
    SELECT
        gender,
        COUNT(*) AS row_count,
        ROUND(AVG(charges), 2) AS avg_charges
    FROM silver.insurance_clean
    GROUP BY gender
    ORDER BY avg_charges DESC;
    """).df()

    plt.figure(figsize=(6,4))
    plt.bar(df_gender["gender"], df_gender["avg_charges"])
    plt.title("Average Charges by Gender")
    plt.xlabel("Gender")
    plt.ylabel("Average Charges")
    plt.tight_layout()
    plt.show()

    df_gender
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot interpretation

    Differences by gender should be interpreted alongside other factors such as age, BMI, smoking status, and region.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 24 — Create analytical groups

    We derive `age_group` and `bmi_group` for easier business analysis.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.insurance_enriched AS
    SELECT
        *,
        CASE
            WHEN age < 20 THEN 'under_20'
            WHEN age BETWEEN 20 AND 29 THEN '20s'
            WHEN age BETWEEN 30 AND 39 THEN '30s'
            WHEN age BETWEEN 40 AND 49 THEN '40s'
            WHEN age BETWEEN 50 AND 59 THEN '50s'
            WHEN age BETWEEN 60 AND 69 THEN '60s'
            ELSE '70_plus'
        END AS age_group,
        CASE
            WHEN bmi < 18.5 THEN 'underweight'
            WHEN bmi < 25 THEN 'normal'
            WHEN bmi < 30 THEN 'overweight'
            ELSE 'obese'
        END AS bmi_group
    FROM silver.insurance_clean;
    """).fetchall()

    con.execute("""
    SELECT *
    FROM silver.insurance_enriched
    LIMIT 10;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 25 — Average charges by age group

    Age groups help business users interpret age-related patterns.
    """)
    return


@app.cell
def _(con, plt):
    df_age = con.execute("""
    SELECT
        age_group,
        COUNT(*) AS row_count,
        ROUND(AVG(charges), 2) AS avg_charges
    FROM silver.insurance_enriched
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
    plt.bar(df_age["age_group"], df_age["avg_charges"])
    plt.title("Average Charges by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Average Charges")
    plt.tight_layout()
    plt.show()

    df_age
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot interpretation

    If charges rise with age, age group is an important reporting dimension.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 26 — Average charges by BMI group

    BMI groups convert a continuous variable into a business-friendly category.
    """)
    return


@app.cell
def _(con, plt):
    df_bmi = con.execute("""
    SELECT
        bmi_group,
        COUNT(*) AS row_count,
        ROUND(AVG(charges), 2) AS avg_charges
    FROM silver.insurance_enriched
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
    plt.bar(df_bmi["bmi_group"], df_bmi["avg_charges"])
    plt.title("Average Charges by BMI Group")
    plt.xlabel("BMI Group")
    plt.ylabel("Average Charges")
    plt.tight_layout()
    plt.show()

    df_bmi
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot interpretation

    If charge levels vary by BMI group, BMI group should be retained in Gold summaries.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 27 — Average charges by BMI group and smoker status

    This checks whether smoker status changes charges within BMI segments.
    """)
    return


@app.cell
def _(con, plt):
    df_bmi_smoker = con.execute("""
    SELECT
        bmi_group,
        smoker,
        COUNT(*) AS row_count,
        ROUND(AVG(charges), 2) AS avg_charges
    FROM silver.insurance_enriched
    GROUP BY bmi_group, smoker
    ORDER BY bmi_group, smoker;
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
    ### Plot interpretation

    Large gaps between smokers and non-smokers within BMI groups suggest smoker status is a dominant cost driver.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 28 — Average charges by region and smoker status

    This combines geographic segmentation with risk behavior.
    """)
    return


@app.cell
def _(con, plt):
    df_region_smoker = con.execute("""
    SELECT
        region,
        smoker,
        COUNT(*) AS row_count,
        ROUND(AVG(charges), 2) AS avg_charges
    FROM silver.insurance_enriched
    GROUP BY region, smoker
    ORDER BY region, smoker;
    """).df()

    _pivot = df_region_smoker.pivot(index="region", columns="smoker", values="avg_charges")

    _pivot.plot(kind="bar", figsize=(8,4))
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
    ### Plot interpretation

    If smokers are consistently more expensive in every region, smoker status is more important than region alone.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 29 — Percentile analysis for charges

    Percentiles show the shape of charges better than average alone.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        ROUND(quantile_cont(charges, 0.25), 2) AS p25_charges,
        ROUND(quantile_cont(charges, 0.50), 2) AS median_charges,
        ROUND(quantile_cont(charges, 0.75), 2) AS p75_charges,
        ROUND(quantile_cont(charges, 0.90), 2) AS p90_charges,
        ROUND(quantile_cont(charges, 0.95), 2) AS p95_charges,
        ROUND(quantile_cont(charges, 0.99), 2) AS p99_charges
    FROM silver.insurance_enriched;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 30 — Top high-charge records

    Outlier review helps determine whether values are valid high-cost cases or data quality issues.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        source_year,
        age,
        gender,
        bmi,
        bmi_group,
        children,
        smoker,
        region,
        charges
    FROM silver.insurance_enriched
    ORDER BY charges DESC
    LIMIT 15;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Gold Layer Design Suggestions
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 31 — Gold yearly KPI table

    This table is useful for executive dashboards.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE gold.yearly_insurance_kpis AS
    SELECT
        source_year,
        COUNT(*) AS policy_count,
        ROUND(AVG(charges), 2) AS avg_charges,
        ROUND(MIN(charges), 2) AS min_charges,
        ROUND(MAX(charges), 2) AS max_charges,
        ROUND(quantile_cont(charges, 0.50), 2) AS median_charges
    FROM silver.insurance_enriched
    GROUP BY source_year
    ORDER BY source_year;
    """).fetchall()

    con.execute("""
    SELECT *
    FROM gold.yearly_insurance_kpis;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 32 — Gold segment KPI table

    This table supports dashboards by smoker, region, age group, and BMI group.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE gold.segment_insurance_kpis AS
    SELECT
        source_year,
        smoker,
        region,
        age_group,
        bmi_group,
        COUNT(*) AS policy_count,
        ROUND(AVG(charges), 2) AS avg_charges,
        ROUND(quantile_cont(charges, 0.50), 2) AS median_charges
    FROM silver.insurance_enriched
    GROUP BY source_year, smoker, region, age_group, bmi_group;
    """).fetchall()

    con.execute("""
    SELECT *
    FROM gold.segment_insurance_kpis
    ORDER BY avg_charges DESC
    LIMIT 15;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 33 — Recommended Gold model

    | Table | Purpose |
    |---|---|
    | `gold.yearly_insurance_kpis` | Year-level executive KPIs |
    | `gold.segment_insurance_kpis` | Segment-level dashboard metrics |
    | `silver.insurance_enriched` | Trusted detailed analytical table |

    ## Useful dimensions

    | Dimension | Attributes |
    |---|---|
    | Time | `source_year` |
    | Person | `age_group`, `gender`, `children` |
    | Health risk | `smoker`, `bmi_group` |
    | Geography | `region` |

    ## Core measures

    | Measure | Meaning |
    |---|---|
    | `policy_count` | number of records / policies |
    | `avg_charges` | average insurance charge |
    | `median_charges` | robust center |
    | `max_charges` | highest observed charge |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Final DW-Oriented EDA Summary

    A strong EDA in a data warehouse context should answer:

    1. Can the source data be trusted?
    2. Are all years structurally consistent?
    3. Are there missing values or duplicates?
    4. Are categorical values valid?
    5. Are numeric values business-valid?
    6. Which dimensions are analytically useful?
    7. Which Gold summaries should be created?

    ## Final message

    EDA is the bridge between:

    ```text
    raw source files → trusted analytical model
    ```

    A good EDA tells us how to clean the data, how to model it, and what business insights are safe to trust.
    """)
    return


if __name__ == "__main__":
    app.run()
