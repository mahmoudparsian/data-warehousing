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
    # Insurance Data Warehouse: Full Medallion Architecture
    ## Applying Business Rules from `business_rules.md`

    [Business Rules are Defined Here](./business_rules.md)

    ![](./images/medallion_architecture.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # What does this notebook do?

    ### This notebook builds a complete **Bronze → Silver → Gold** <br> pipeline for the messy 4-year insurance dataset.

    ### Bronze to Silver transformation <br > is done by applying the [Business Rules](./business_rules.md)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # INPUT data files...
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Expected files:

    ```text
    data_messy/insurance.2021.messy.csv
    data_messy/insurance.2022.messy.csv
    data_messy/insurance.2023.messy.csv
    data_messy/insurance.2024.messy.csv
    ```

    ### View sample data:

    ```
    # magic command not supported in marimo; please file an issue to add support
    # %head -5 data_messy/insurance.2022.messy.csv
    age,gender,bmi,children,smoker,region,charges
    32.0,male,30.63,0.0,no,northwest,1694.72
    55.0,male,46.03,3.0,no,northeast,22892.53
    35.0,female,22.75,1.0,no,northeast,12303.52
    34.0,male,31.51,0.0,no,northwest,8358.63
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Business Rules
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Business Rules Applied

    | Rule | Meaning | Silver Action |
    |---|---|---|
    | Rule 1 | Age must be between 0 and 120 | reject invalid rows |
    | Rule 2 | BMI must be between 10 and 60 | reject invalid rows |
    | Rule 3 | Charges must be >= 0 | reject invalid rows |
    | Rule 4 | Children must be between 0 and 10 | reject invalid rows |
    | Rule 5 | Region must be valid after standardization | standardize then validate |
    | Rule 6 | Gender and smoker must be valid domains | reject invalid rows |
    | Rule 7 | Duplicate records should not exist | deduplicate |
    | Rule 8 | Smokers with unusually low charges should be flagged | flag anomaly, do not reject |

    ---
    # Final Goal: Create a STAR SCHEMA
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Final Goal: : Create a STAR SCHEMA

    Make the data ready for a **Star Schema**:

    - `gold.dim_year`
    - `gold.dim_region`
    - `gold.dim_person_profile`
    - `gold.dim_risk_profile`
    - `gold.fact_insurance_charges`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Part 1 — Setup
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 01 — Import libraries and connect to DuckDB

    ### What are we doing?
    We import Python libraries and create a DuckDB database connection.

    ### Why are we doing it?
    DuckDB lets us write warehouse-style SQL directly inside a notebook.

    ### Business value
    This creates a reproducible analytical environment.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    import pandas as pd
    import matplotlib.pyplot as plt
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    import pandas as pd
    import matplotlib.pyplot as plt
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Make sure that DuckDB is installed:
    """)
    return


@app.cell
def _():
    # Make sure that DuckDB is installed:
    try:
        import duckdb
        print('DuckDB is already installed.')
    except ImportError:
        pass  # (pip install removed: see the course setup)
    return (duckdb,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Install other libraries...
    """)
    return


@app.cell
def _():
    # Install other libraries...
    import pandas as pd
    import matplotlib.pyplot as plt

    return (plt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Create a CONNECTION object to a DuckDB database
    """)
    return


@app.cell
def _(duckdb):
    # Create a CONNECTION object to a DuckDB database
    con = duckdb.connect("insurance_medallion_dw.duckdb")
    print("DuckDB version:", duckdb.__version__)
    print("con=", con)
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Cell 02 — Define source files

    ### What are we doing?
    We define the location of the four messy source files.

    ### Why are we doing it?
    The files represent yearly source-system extracts.

    ### Business value
    Keeping source-year information allows row-level lineage and time-based analysis.
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
    ---
    ## Cell 03 — Create Medallion schemas

    ### What are we doing?
    We create three schemas: `bronze`, `silver`, and `gold`.

    ### Why are we doing it?
    Each schema has a different responsibility.

    ### Business value
    This separates raw data, trusted data, and analytics-ready data.
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
    # Part 2 — Bronze Layer: Raw Ingestion
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 04 — Load messy CSV files into Bronze

    ### What are we doing?
    We load each yearly messy CSV file into a Bronze table.

    ### Why are we doing it?
    Bronze should preserve raw data as close to the source as possible.

    ### Business value
    If something goes wrong downstream, we can trace back to the original row.

    ### Business rules solved
    None yet. Bronze does **not** clean data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## ADDING 3 new columns:
    * `source-year`,
    * `source-file`,
    * `raw_row_id`
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
    We union all yearly Bronze tables into one `bronze.insurance_raw` table.

    ### Why are we doing it?
    A single Bronze table makes cross-year profiling and downstream transformation easier.

    ### Business value
    We get one consistent raw landing table with full lineage.

    ### Business rules solved
    None yet. This is still raw data.
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
    ## Cell 06 — Preview Bronze data

    ### What are we doing?
    We look at raw records.

    ### Why are we doing it?
    Before transforming data, we need to see what values look like.

    ### Business value
    Students see why Bronze cannot be trusted directly.
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
    # Part 3 — Silver Reference Table
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 07 — Create valid region reference table

    ### What are we doing?
    We create `silver.dim_valid_region`.

    ### Why are we doing it?
    Valid business regions should be defined once, not hardcoded everywhere.

    ### Business value
    This supports governance and makes region validation reusable.

    ### Business rule solved
    Rule 5 — Region must be valid after standardization.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.dim_valid_region AS
    SELECT *
    FROM (VALUES
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
    ORDER BY region;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Part 4 — Silver Step 01: Deduplication
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 08 — Deduplicate raw data

    ### What are we doing?
    We remove exact duplicate records from Bronze.

    ### Why are we doing it?
    Duplicates inflate row counts and distort metrics such as average charges.

    ### Business value
    This prevents duplicated records from corrupting KPIs.

    ### Business rule solved
    Rule 7 — Duplicate records should not exist.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.step01_dedup AS
    SELECT *
    FROM (
        SELECT
            *,
            ROW_NUMBER() OVER (
                PARTITION BY
                    source_year,
                    age,
                    gender,
                    bmi,
                    children,
                    smoker,
                    region,
                    charges
                ORDER BY raw_row_id
            ) AS rn
        FROM bronze.insurance_raw
    )
    WHERE rn = 1;
    """).fetchall()

    con.execute("""
    SELECT
        (SELECT COUNT(*) FROM bronze.insurance_raw) AS bronze_rows,
        (SELECT COUNT(*) FROM silver.step01_dedup) AS dedup_rows,
        (SELECT COUNT(*) FROM bronze.insurance_raw) -
        (SELECT COUNT(*) FROM silver.step01_dedup) AS removed_duplicate_rows;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 09 — Plot Bronze vs Dedup rows

    ### What are we doing?
    We visualize row counts before and after deduplication.

    ### Why are we doing it?
    Students can see the impact of Rule 7.

    ### Business value
    A simple funnel builds confidence that the pipeline is improving data quality.
    """)
    return


@app.cell
def _(con, plt):
    df_dedup = con.execute("""
    SELECT 'Bronze Raw' AS stage, COUNT(*) AS row_count FROM bronze.insurance_raw
    UNION ALL
    SELECT 'After Dedup', COUNT(*) FROM silver.step01_dedup;
    """).df()

    plt.figure(figsize=(6,4))
    plt.bar(df_dedup["stage"], df_dedup["row_count"])
    plt.title("Row Count Before and After Deduplication")
    plt.xlabel("Stage")
    plt.ylabel("Rows")
    plt.tight_layout()
    plt.show()

    df_dedup
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Part 5 — Silver Step 02: Standardization and Safe Typing
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 10 — Standardize and type raw values
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 10 — Standardize and type raw values

    ### What are we doing?
    We create `silver.step02_standardized`.

    This step:
    - trims text
    - lowercases categorical values
    - safely casts numeric fields
    - standardizes regions by removing spaces and hyphens

    ### Why are we doing it?
    Raw text values cannot be reliably validated or analyzed.

    ### Business value
    This prepares data for rule validation without losing original raw values.

    ### Business rules solved
    Prepares for Rules 1–6 and Rule 8.

    ### Data Engineering / SQL Explanation:

    ```
    ⸻

    1.

    TRY_CAST(NULLIF(TRIM(age), '') AS INTEGER) AS age

    Step-by-step

    * TRIM(age)
        * Removes extra spaces before and after the value.
        * Example: ' 45 '  →  '45'

    * NULLIF(..., '')
        * If the value becomes an empty string (''), convert it to NULL.
        * Example: ''  →  NULL

    * TRY_CAST(... AS INTEGER)
        * Tries to convert the value into a whole number.
        * If conversion fails, it returns NULL instead of crashing.
        * Example:
                '45'     → 45
                'abc'    → NULL
                NULL     → NULL

    Simple English
                    Clean the age value, remove spaces,
                    turn blanks into NULL, and safely
                    convert it into a whole number.

    ⸻

    2.

    LOWER(NULLIF(TRIM(gender), '')) AS gender

    Step-by-step

    * TRIM(gender)
        * Removes extra spaces.
        * Example: ' Male ' → 'Male'

    * NULLIF(..., '')
        * Converts empty strings into NULL.

    * LOWER(...)
        * Converts text to lowercase.
        * Example:
                   'Male' → 'male'
                   'FEMALE' → 'female'

    Simple English
                   Clean the gender text, remove blanks,
                   and make everything lowercase for consistency.

    ⸻

    3.

    TRY_CAST(NULLIF(TRIM(bmi), '') AS DOUBLE) AS bmi

    Step-by-step

    * TRIM(bmi)
        * Removes spaces.

    * NULLIF(..., '')
        * Converts blank values into NULL.

    * TRY_CAST(... AS DOUBLE)
        * Safely converts the value into a decimal number.
        * Example:
                   '27.5' → 27.5
                   'abc'  → NULL

    Simple English
                    Clean the BMI value and safely convert
                    it into a decimal number.

    ⸻

    4.

    TRY_CAST(NULLIF(TRIM(children), '') AS INTEGER) AS children

    Step-by-step

    * Remove spaces
    * Convert blanks to NULL
    * Safely convert to a whole number

    Example
            ' 3 ' → 3
            ''    → NULL
            'two' → NULL

    Simple English
                   Clean the children column and safely
                   convert it into a whole number.

    ⸻

    5.

    LOWER(NULLIF(TRIM(smoker), '')) AS smoker

    Step-by-step

    * Remove spaces
    * Convert blanks to NULL
    * Convert text to lowercase

    Example
             ' YES ' → 'yes'
             'No'    → 'no'

    Simple English
                   Clean the smoker column and make all
                   values lowercase for consistency.

    ⸻

    Why This Pattern Is Important

    This pattern helps create clean and
    reliable data in the Silver Layer of
    a medallion architecture.

    It:

    * removes messy spaces
    * handles blank values
    * standardizes text
    * safely converts data types
    * prevents SQL errors

    This is a very common real-world data engineering pattern.
    ```
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.step02_standardized AS
    SELECT
        source_year,
        source_file,
        raw_row_id,

        -- Raw values preserved for audit
        age AS age_raw,
        gender AS gender_raw,
        bmi AS bmi_raw,
        children AS children_raw,
        smoker AS smoker_raw,
        region AS region_raw,
        charges AS charges_raw,

        -- Typed / cleaned values
        TRY_CAST(NULLIF(TRIM(age), '') AS INTEGER) AS age,
        LOWER(NULLIF(TRIM(gender), '')) AS gender,
        TRY_CAST(NULLIF(TRIM(bmi), '') AS DOUBLE) AS bmi,
        TRY_CAST(NULLIF(TRIM(children), '') AS INTEGER) AS children,
        LOWER(NULLIF(TRIM(smoker), '')) AS smoker,

        -- Region standardization: trim, lowercase, remove spaces, remove hyphens
        REPLACE(
            REPLACE(LOWER(TRIM(region)), ' ', ''),
            '-', ''
        ) AS region,

        TRY_CAST(NULLIF(TRIM(charges), '') AS DOUBLE) AS charges

    FROM silver.step01_dedup;
    """).fetchall()

    con.execute("""
    SELECT *
    FROM silver.step02_standardized
    LIMIT 10;
    """).df()
    return


@app.cell
def _(con):
    # Find about BMI and charges

    con.execute("""
    SELECT
        COUNT(*) AS both_bmi_and_charges
    FROM silver.step02_standardized
    WHERE
        (bmi IS NULL OR bmi < 10 OR bmi > 60)
    AND
        (charges IS NULL OR charges < 0);
    """).df()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        'BMI only' AS category,
        COUNT(*) AS rows
    FROM silver.step02_standardized
    WHERE
        (bmi IS NULL OR bmi < 10 OR bmi > 60)
    AND NOT (charges IS NULL OR charges < 0)

    UNION ALL

    SELECT
        'Charges only',
        COUNT(*)
    FROM silver.step02_standardized
    WHERE
        (charges IS NULL OR charges < 0)
    AND NOT (bmi IS NULL OR bmi < 10 OR bmi > 60)

    UNION ALL

    SELECT
        'Both',
        COUNT(*)
    FROM silver.step02_standardized
    WHERE
        (bmi IS NULL OR bmi < 10 OR bmi > 60)
    AND
        (charges IS NULL OR charges < 0);
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Teaching Gold Question

    ```
    Ask students:

    “Why is ‘Both’ much smaller than individual categories?”

    Expected answer:

        Because errors are mostly independent,

        not caused by a single upstream failure.
    ```
    """)
    return


@app.cell
def _(con, plt):
    df = con.execute("""
    SELECT
        category,
        rows
    FROM (
        SELECT 'BMI only' AS category, 254 AS rows
        UNION ALL
        SELECT 'Charges only', 254
        UNION ALL
        SELECT 'Both', 39
    )
    """).df()


    plt.figure(figsize=(6,4))
    plt.bar(df["category"], df["rows"])
    plt.title("Error Distribution: BMI vs Charges")
    plt.xlabel("Category")
    plt.ylabel("Rows")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 11 — Show region standardization examples

    ### What are we doing?
    We compare raw regions to standardized regions.

    ### Why are we doing it?
    Region data can be messy without being truly invalid.

    ### Business value
    This teaches the difference between formatting issues and invalid business values.

    ### Business rule solved
    Rule 5 — Region standardization.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        region_raw,
        region AS region_standardized,
        COUNT(*) AS row_count
    FROM silver.step02_standardized
    GROUP BY region_raw, region
    ORDER BY row_count DESC, region_raw
    LIMIT 30;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Part 6 — Silver Step 03: Rejected Records
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 12 — Create rejected records table

    ### What are we doing?
    We create `silver.rejected_records` with a rejection reason.

    ### Why are we doing it?
    Bad records should not silently disappear. We preserve them for auditing.

    ### Business value
    Rejected records help identify upstream data-quality problems.

    ### Business rules solved
    Rules 1–6.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        COUNT(*) FILTER (WHERE bmi IS NULL OR bmi < 10 OR bmi > 60) AS invalid_bmi,
        COUNT(*) FILTER (WHERE charges IS NULL OR charges < 0) AS invalid_charges,
        COUNT(*) FILTER (WHERE gender NOT IN ('male','female')) AS invalid_gender,
        COUNT(*) FILTER (WHERE smoker NOT IN ('yes','no')) AS invalid_smoker,
        COUNT(*) FILTER (WHERE v.region IS NULL) AS invalid_region
    FROM silver.step02_standardized s
    LEFT JOIN silver.dim_valid_region v
        ON s.region = v.region;
    """).df()
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.rejected_records AS
    WITH base AS (
        SELECT
            s.*,
            v.region AS valid_region,

            -- Individual rule flags (0/1)
            CASE WHEN age IS NULL OR age < 0 OR age > 120 THEN 1 ELSE 0 END AS f_invalid_age,
            CASE WHEN bmi IS NULL OR bmi < 10 OR bmi > 60 THEN 1 ELSE 0 END AS f_invalid_bmi,
            CASE WHEN charges IS NULL OR charges < 0 THEN 1 ELSE 0 END AS f_invalid_charges,
            CASE WHEN children IS NULL OR children < 0 OR children > 10 THEN 1 ELSE 0 END AS f_invalid_children,
            CASE WHEN gender IS NULL OR gender NOT IN ('male','female') THEN 1 ELSE 0 END AS f_invalid_gender,
            CASE WHEN smoker IS NULL OR smoker NOT IN ('yes','no') THEN 1 ELSE 0 END AS f_invalid_smoker,
            CASE WHEN v.region IS NULL THEN 1 ELSE 0 END AS f_invalid_region

        FROM silver.step02_standardized s
        LEFT JOIN silver.dim_valid_region v
            ON s.region = v.region
    )

    SELECT
        *,

        -- Total number of violations per row
        (
            f_invalid_age +
            f_invalid_bmi +
            f_invalid_charges +
            f_invalid_children +
            f_invalid_gender +
            f_invalid_smoker +
            f_invalid_region
        ) AS total_violations,

        -- Concatenate ALL violations into a readable string
        CONCAT_WS('|',
            CASE WHEN f_invalid_age = 1 THEN 'INVALID_AGE' END,
            CASE WHEN f_invalid_bmi = 1 THEN 'INVALID_BMI' END,
            CASE WHEN f_invalid_charges = 1 THEN 'INVALID_CHARGES' END,
            CASE WHEN f_invalid_children = 1 THEN 'INVALID_CHILDREN' END,
            CASE WHEN f_invalid_gender = 1 THEN 'INVALID_GENDER' END,
            CASE WHEN f_invalid_smoker = 1 THEN 'INVALID_SMOKER' END,
            CASE WHEN f_invalid_region = 1 THEN 'INVALID_REGION' END
        ) AS reject_reasons

    FROM base

    -- Only keep rows that violate at least one rule
    WHERE
        (
            f_invalid_age +
            f_invalid_bmi +
            f_invalid_charges +
            f_invalid_children +
            f_invalid_gender +
            f_invalid_smoker +
            f_invalid_region
        ) > 0;
    """).fetchall()

    con.execute("""
    SELECT
        reject_reasons,
        COUNT(*) AS rejected_rows
    FROM silver.rejected_records
    GROUP BY reject_reasons
    ORDER BY rejected_rows DESC;
    """).df()
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        total_violations,
        COUNT(*) AS rows
    FROM silver.rejected_records
    GROUP BY total_violations
    ORDER BY total_violations DESC;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 13 — Plot rejected records by reason

    ### What are we doing?
    We visualize rejection counts.

    ### Why are we doing it?
    This shows which rules are causing the most data loss.

    ### Business value
    The business can prioritize fixing the most common upstream problems.
    """)
    return


@app.cell
def _(con, plt):
    df_rules = con.execute("""
    SELECT
        rule,
        COUNT(*) AS rows
    FROM (
        SELECT
            UNNEST(string_split(reject_reasons, '|')) AS rule
        FROM silver.rejected_records
    ) t
    GROUP BY rule
    ORDER BY rows DESC;
    """).df()

    plt.figure(figsize=(8,4))
    plt.bar(df_rules["rule"], df_rules["rows"])
    plt.title("Data Quality Issues by Rule")
    plt.xlabel("Rule")
    plt.ylabel("Rejected Rows")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 14 — Inspect invalid region records

    ### What are we doing?
    We inspect region values that failed validation.

    ### Why are we doing it?
    This confirms formatting issues were fixed but truly invalid values remain rejected.

    ### Business value
    This proves the region business rule is working correctly.
    """)
    return


@app.cell
def _(con):
    con.execute("""

    SELECT

        region_raw,

        region AS region_standardized,

        COUNT(*) AS row_count

    FROM silver.rejected_records

    WHERE reject_reasons LIKE '%INVALID_REGION%'

    GROUP BY region_raw, region

    ORDER BY row_count DESC;

    """).df()
    return


@app.cell
def _(con, plt):
    ### “Show me all region values that were rejected 
    ### because they had an invalid region, and count 
    ### how many times each bad region appeared.”
    ###
    ### UNNEST(...) : Turns the list into multiple rows.
    ###
    ### Final Plain-English Summary:
    ###        Look at all rejected records, find the ones 
    ###        rejected because of invalid regions, count 
    ###        how many times each bad region appears, sort 
    ###        from most common to least common, and store 
    ###        the result in a Pandas DataFrame.
    

    _df_region = con.execute("""

    SELECT
        region AS region_standardized,
        COUNT(*) AS rows
    FROM silver.rejected_records,
         UNNEST(string_split(reject_reasons, '|')) AS t(rule)
    WHERE rule = 'INVALID_REGION'

    GROUP BY region

    ORDER BY rows DESC;

    """).df()



    plt.figure(figsize=(6,4))

    plt.bar(_df_region["region_standardized"], _df_region["rows"])

    plt.title("Invalid Region Distribution")

    plt.xlabel("Region")

    plt.ylabel("Rows")

    plt.tight_layout()

    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Part 7 — Silver Clean and Enriched Tables
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 15 — Create Silver clean table

    ### What are we doing?
    We create `silver.insurance_clean` with valid records only.

    ### Why are we doing it?
    This is the trusted dataset that can feed analytics and Gold tables.

    ### Business value
    Only validated, standardized data should flow into dashboards and reports.

    ### Business rules solved
    Rules 1–7 are enforced.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.insurance_clean AS
    SELECT DISTINCT
        s.source_year,
        s.source_file,
        s.raw_row_id,
        s.age,
        s.gender,
        s.bmi,
        s.children,
        s.smoker,
        s.region,
        s.charges

    FROM silver.step02_standardized s
    JOIN silver.dim_valid_region v
        ON s.region = v.region

    WHERE s.age BETWEEN 0 AND 120
      AND s.bmi BETWEEN 10 AND 60
      AND s.charges >= 0
      AND s.children BETWEEN 0 AND 10
      AND s.gender IN ('male', 'female')
      AND s.smoker IN ('yes', 'no');
    """).fetchall()

    con.execute("""
    SELECT
        (SELECT COUNT(*) FROM bronze.insurance_raw) AS bronze_rows,
        (SELECT COUNT(*) FROM silver.step01_dedup) AS dedup_rows,
        (SELECT COUNT(*) FROM silver.rejected_records) AS rejected_rows,
        (SELECT COUNT(*) FROM silver.insurance_clean) AS clean_rows;
    """).df()
    return


@app.cell
def _(con):
    # KPI
    con.execute("""
    SELECT
        ROUND(100.0 * rejected_rows / dedup_rows, 2) AS rejection_rate_pct,
        ROUND(100.0 * clean_rows / dedup_rows, 2) AS clean_rate_pct
    FROM (
        SELECT
            (SELECT COUNT(*) FROM silver.step01_dedup) AS dedup_rows,
            (SELECT COUNT(*) FROM silver.rejected_records) AS rejected_rows,
            (SELECT COUNT(*) FROM silver.insurance_clean) AS clean_rows
    );
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Find Minimum, Maximum, Average Charges <br> for Smokers and Non-Smokers
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        smoker,
        MIN(charges),
        MAX(charges),
        AVG(charges)
    FROM silver.insurance_clean
    GROUP BY smoker;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 16 — Pipeline funnel

    ### What are we doing?
    We show row counts across Bronze and Silver stages.

    ### Why are we doing it?
    This shows the impact of each transformation stage.

    ### Business value
    A row-count funnel is a useful governance and audit artifact.
    """)
    return


@app.cell
def _(con, plt):
    df_funnel = con.execute("""
    SELECT 'Bronze Raw' AS stage, COUNT(*) AS row_count FROM bronze.insurance_raw
    UNION ALL
    SELECT 'Deduplicated', COUNT(*) FROM silver.step01_dedup
    UNION ALL
    SELECT 'Rejected', COUNT(*) FROM silver.rejected_records
    UNION ALL
    SELECT 'Silver Clean', COUNT(*) FROM silver.insurance_clean;
    """).df()

    plt.figure(figsize=(8,4))
    plt.bar(df_funnel["stage"], df_funnel["row_count"])
    plt.title("Medallion Pipeline Row Count Funnel")
    plt.xlabel("Pipeline Stage")
    plt.ylabel("Rows")
    plt.tight_layout()
    plt.show()

    df_funnel
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Cell 17 — Create enriched Silver table

    ### What are we doing?
    We add:
    - `age_group`
    - `bmi_group`
    - `semantic_low_charge_smoker_flag`

    ### Why are we doing it?
    Gold dimensions and dashboards need business-friendly categories.

    ### Business value
    This makes the data ready for star schema modeling.

    ### Business rule solved
    Rule 8 — Smokers with unusually low charges are flagged, not rejected.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Create a table called silver.insurance_enriched

    ```
        This creates or replaces a table called silver.insurance_enriched.

        Inside the query, a temporary result called smoker_threshold is created.

        That temporary result calculates the 10th percentile of insurance charges
        for smokers (smoker = 'yes').

        In simple terms:    It finds the charge amount below which the
                            lowest 10% of smoker insurance charges fall.

                            Finds the 10% Mark: It uses PERCENTILE_CONT(0.10)
                            to calculate the exact dollar amount where only 10%
                            of smokers pay less, and the other 90% pay more.

        The value is calculated from the silver.insurance_clean table.
    ```
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE silver.insurance_enriched AS
    WITH smoker_threshold AS (
        -- Compute a data-driven threshold (10th percentile for smokers)
        SELECT
            PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY charges) AS p10_smoker_charges
        FROM silver.insurance_clean
        WHERE smoker = 'yes'
    )

    SELECT
        -- Core columns
        source_year,
        source_file,
        raw_row_id,

        age,
        gender,
        bmi,
        children,
        smoker,
        region,
        charges,

        -- -----------------------------------
        -- Derived: Age Group
        -- -----------------------------------
        CASE
            WHEN age < 20 THEN 'under_20'
            WHEN age BETWEEN 20 AND 29 THEN '20s'
            WHEN age BETWEEN 30 AND 39 THEN '30s'
            WHEN age BETWEEN 40 AND 49 THEN '40s'
            WHEN age BETWEEN 50 AND 59 THEN '50s'
            WHEN age BETWEEN 60 AND 69 THEN '60s'
            ELSE '70_plus'
        END AS age_group,

        -- -----------------------------------
        -- Derived: BMI Group
        -- -----------------------------------
        CASE
            WHEN bmi < 18.5 THEN 'underweight'
            WHEN bmi < 25 THEN 'normal'
            WHEN bmi < 30 THEN 'overweight'
            ELSE 'obese'
        END AS bmi_group,

        -- -----------------------------------
        -- Derived: Semantic Feature (FIXED ✅)
        -- -----------------------------------
        CASE
            WHEN smoker = 'yes'
             AND charges < (SELECT p10_smoker_charges FROM smoker_threshold)
            THEN 1
            ELSE 0
        END AS semantic_low_charge_smoker_flag

    FROM silver.insurance_clean;
    """).df()

    con.execute("""
    SELECT * 
    FROM silver.insurance_enriched 
    LIMIT 15;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 18 — Semantic anomaly count

    ### What are we doing?
    We count smoker records with unusually low charges.

    ### Why are we doing it?
    These records are not necessarily invalid, but they are suspicious.

    ### Business value
    Flagging preserves data while alerting analysts to possible anomalies.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        semantic_low_charge_smoker_flag,
        COUNT(*) AS row_count
    FROM silver.insurance_enriched
    GROUP BY semantic_low_charge_smoker_flag
    ORDER BY semantic_low_charge_smoker_flag;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Part 8 — Gold Layer: Star Schema Ready Tables
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 19 — Create Gold dimension: dim_year

    ### What are we doing?
    We create a small year dimension.

    ### Why are we doing it?
    Year is a common analytical slice.

    ### Business value
    Supports year-over-year reporting.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE gold.dim_year AS
    SELECT
        ROW_NUMBER() OVER (ORDER BY source_year) AS year_key,
        source_year
    FROM (
        SELECT DISTINCT source_year
        FROM silver.insurance_enriched
    );
    """).fetchall()

    con.execute("""
    SELECT *
    FROM gold.dim_year
    ORDER BY year_key;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 20 — Create Gold dimension: dim_region

    ### What are we doing?
    We create a region dimension from clean Silver data.

    ### Why are we doing it?
    Region is a business dimension for geographic analysis.

    ### Business value
    Enables regional cost reporting and comparison.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE gold.dim_region AS
    SELECT
        ROW_NUMBER() OVER (ORDER BY region) AS region_key,
        region
    FROM (
        SELECT DISTINCT region
        FROM silver.insurance_enriched
    );
    """).fetchall()

    con.execute("""
    SELECT *
    FROM gold.dim_region
    ORDER BY region_key;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 21 — Create Gold dimension: dim_person_profile

    ### What are we doing?
    We create a dimension for demographic and family attributes.

    ### Why are we doing it?
    Age group, gender, and children are descriptive attributes used for slicing facts.

    ### Business value
    Supports demographic analysis of insurance charges.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE gold.dim_person_profile AS
    SELECT
        ROW_NUMBER() OVER (
            ORDER BY gender, age_group, children
        ) AS person_profile_key,
        gender,
        age_group,
        children
    FROM (
        SELECT DISTINCT
            gender,
            age_group,
            children
        FROM silver.insurance_enriched
    );
    """).fetchall()

    con.execute("""
    SELECT *
    FROM gold.dim_person_profile
    ORDER BY person_profile_key
    LIMIT 20;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 22 — Create Gold dimension: dim_risk_profile

    ### What are we doing?
    We create a dimension for risk-related attributes.

    ### Why are we doing it?
    Smoker status and BMI group are risk indicators.

    ### Business value
    Supports risk-based cost analysis.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE gold.dim_risk_profile AS
    SELECT
        ROW_NUMBER() OVER (
            ORDER BY smoker, bmi_group, semantic_low_charge_smoker_flag
        ) AS risk_profile_key,
        smoker,
        bmi_group,
        semantic_low_charge_smoker_flag
    FROM (
        SELECT DISTINCT
            smoker,
            bmi_group,
            semantic_low_charge_smoker_flag
        FROM silver.insurance_enriched
    );
    """).fetchall()

    con.execute("""
    SELECT *
    FROM gold.dim_risk_profile
    ORDER BY risk_profile_key;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 23 — Create Gold fact table

    ### What are we doing?
    We create `gold.fact_insurance_charges`.

    ### Why are we doing it?
    The fact table stores measurable insurance events and foreign keys to dimensions.

    ### Business value
    This is the analytics-ready star schema foundation.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE gold.fact_insurance_charges AS
    SELECT
        ROW_NUMBER() OVER (
            ORDER BY e.source_year, e.raw_row_id
        ) AS insurance_fact_key,

        y.year_key,
        r.region_key,
        p.person_profile_key,
        rp.risk_profile_key,

        -- Degenerate / traceability fields
        e.source_year,
        e.raw_row_id,

        -- Measures
        e.age,
        e.bmi,
        e.charges

    FROM silver.insurance_enriched e

    JOIN gold.dim_year y
        ON e.source_year = y.source_year

    JOIN gold.dim_region r
        ON e.region = r.region

    JOIN gold.dim_person_profile p
        ON e.gender = p.gender
       AND e.age_group = p.age_group
       AND e.children = p.children

    JOIN gold.dim_risk_profile rp
        ON e.smoker = rp.smoker
       AND e.bmi_group = rp.bmi_group
       AND e.semantic_low_charge_smoker_flag = rp.semantic_low_charge_smoker_flag;
    """).fetchall()

    con.execute("""
    SELECT *
    FROM gold.fact_insurance_charges
    LIMIT 15;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 24 — Fact table sanity check

    ### What are we doing?
    We compare Silver enriched row count to Gold fact row count.

    ### Why are we doing it?
    The fact table should preserve the grain of Silver enriched data.

    ### Business value
    This catches join explosions or lost records.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    SELECT
        (SELECT COUNT(*) FROM silver.insurance_enriched) AS silver_enriched_rows,
        (SELECT COUNT(*) FROM gold.fact_insurance_charges) AS fact_rows;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Part 9 — Gold OLAP Examples
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 25 — OLAP 1: Average charges by year

    ### What are we doing?
    We analyze charges over time.

    ### Why are we doing it?
    Yearly trends are core DW analytics.

    ### Business value
    Supports executive trend reporting.
    """)
    return


@app.cell
def _(con, plt):
    df_year = con.execute("""
    SELECT
        y.source_year,
        COUNT(*) AS policy_count,
        ROUND(AVG(f.charges), 2) AS avg_charges
    FROM gold.fact_insurance_charges f
    JOIN gold.dim_year y
        ON f.year_key = y.year_key
    GROUP BY y.source_year
    ORDER BY y.source_year;
    """).df()

    plt.figure(figsize=(7,4))
    plt.plot(df_year["source_year"].astype(str), df_year["avg_charges"], marker="o")
    plt.title("Gold OLAP: Average Charges by Year")
    plt.xlabel("Year")
    plt.ylabel("Average Charges")
    plt.tight_layout()
    plt.show()

    df_year
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 26 — OLAP 2: Average charges by region

    ### What are we doing?
    We compare charges across regions.

    ### Why are we doing it?
    Geography can affect cost patterns.

    ### Business value
    Supports regional business planning.
    """)
    return


@app.cell
def _(con, plt):
    _df_region = con.execute("""
    SELECT
        r.region,
        COUNT(*) AS policy_count,
        ROUND(AVG(f.charges), 2) AS avg_charges
    FROM gold.fact_insurance_charges f
    JOIN gold.dim_region r
        ON f.region_key = r.region_key
    GROUP BY r.region
    ORDER BY avg_charges DESC;
    """).df()

    plt.figure(figsize=(8,4))
    plt.bar(_df_region["region"], _df_region["avg_charges"])
    plt.title("Gold OLAP: Average Charges by Region")
    plt.xlabel("Region")
    plt.ylabel("Average Charges")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.show()

    _df_region
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cell 27 — OLAP 3: Average charges by risk profile

    ### What are we doing?
    We compare charges by smoker and BMI group.

    ### Why are we doing it?
    Risk profile is one of the most important dimensions in insurance.

    ### Business value
    Supports risk-based pricing and customer segmentation.
    """)
    return


@app.cell
def _(con, plt):
    df_risk = con.execute("""
    SELECT
        rp.smoker,
        rp.bmi_group,
        COUNT(*) AS policy_count,
        ROUND(AVG(f.charges), 2) AS avg_charges
    FROM gold.fact_insurance_charges f
    JOIN gold.dim_risk_profile rp
        ON f.risk_profile_key = rp.risk_profile_key
    GROUP BY rp.smoker, rp.bmi_group
    ORDER BY avg_charges DESC;
    """).df()

    pivot = df_risk.pivot(index="bmi_group", columns="smoker", values="avg_charges")

    pivot.plot(kind="bar", figsize=(8,4))
    plt.title("Gold OLAP: Average Charges by BMI Group and Smoker")
    plt.xlabel("BMI Group")
    plt.ylabel("Average Charges")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.show()

    df_risk
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Final Summary
    ---

    ## What We Built

    | Layer | Tables | Purpose |
    |---|---|---|
    | Bronze | `bronze.insurance_raw` | raw messy source data |
    | Silver | `step01_dedup`, `step02_standardized`, `rejected_records`, `insurance_clean`, `insurance_enriched` | cleaning, validation, enrichment |
    | Gold | dimensions + fact table | star-schema-ready analytics |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Key Teaching Message

    ### 1. EDA tells us what is wrong.

    ### 2. Business rules tell us what to do.

    ### 3. Silver applies the business rules.

    ### 4. Gold makes the data ready for analytics.


    > **Never build Gold dashboards directly on Bronze data.**
    """)
    return


if __name__ == "__main__":
    app.run()
