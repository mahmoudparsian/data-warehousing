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
    # Week 5 — Medallion Layers on the Insurance Data

    The insurance data from weeks 1–2, with a few realistic problems added by the "source system". We follow **the same rows**
    through Bronze → Silver → Gold and prove, with a reconciliation, that none is lost.
    Definitions: [Medallion in a nutshell](../Medallion_Architecture_in_a_Nutshell.md).

    | Layer | Table | Rule |
    |---|---|---|
    | 🟫 Bronze | `bronze.insurance_raw` | as received (all text) + lineage |
    | ⚪ Silver | `silver.insurance`, `silver.rejected` | region names standardized; no charges → rejected; exact copies removed (counted) |
    | 🟡 Gold | `gold.dim_region`, `gold.fact_policy`, `gold.avg_charges_by_region` | star schema + one business table |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup: the "Source File"

    The source system sends `insurance.csv` with problems (we add them here, to have something messy): two northeast customers spelled
    `NE` and `north-east`, one row with no charges, and two rows sent twice. The original file also already contains **one** exact duplicate row.
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE source_insurance AS
WITH original AS (
  SELECT * FROM read_csv('../../week01-Foundations-SQL-for-Analytics/example_1_insurance/insurance.csv', all_varchar = true)
)
SELECT * REPLACE (CASE WHEN charges = '6406.4107' THEN 'NE'            -- a northeast customer, spelled NE
                       WHEN charges = '2721.3208' THEN 'north-east'    -- a northeast customer, spelled north-east
                       ELSE region END                        AS region,
                  CASE WHEN charges = '4449.462' THEN NULL
                       ELSE charges END                       AS charges)   -- charges lost in transfer
FROM original
UNION ALL
SELECT * FROM original WHERE charges IN ('21984.47061', '3866.8552')        -- 2 rows sent twice
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🟫 Bronze: As Received, Plus Lineage

    All text, nothing fixed, nothing removed. `_source_file` and `_ingested_at` say where and when each row arrived.
    """)
    return


@app.cell
def _(mo, source_insurance):
    _df = mo.sql(
        f"""
        CREATE SCHEMA IF NOT EXISTS bronze;
        CREATE SCHEMA IF NOT EXISTS silver;
        CREATE SCHEMA IF NOT EXISTS gold;
        
        CREATE OR REPLACE TABLE bronze.insurance_raw AS
        SELECT *,
               'insurance_export.csv' AS _source_file,
               current_timestamp      AS _ingested_at
        FROM source_insurance;
        
        SELECT region, COUNT(*) AS n_rows
        FROM bronze.insurance_raw
        GROUP BY region
        ORDER BY region
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Bronze:** 1,340 rows (1,338 + 2 sent twice), six region spellings. We **see** the problems here, but we do not fix them here.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ⚪ Silver Step 1: Remove Exact Copies (Counted)
    """)
    return


@app.cell
def _(insurance_raw, mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE silver.step1_dedup AS
        SELECT DISTINCT * EXCLUDE (_ingested_at)
        FROM bronze.insurance_raw;
        
        SELECT (SELECT COUNT(*) FROM bronze.insurance_raw) AS bronze_rows,
               (SELECT COUNT(*) FROM silver.step1_dedup)   AS after_dedup
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ⚪ Silver Step 2: Quarantine, Type, Standardize

    - **Rule:** no `charges` → **rejected** (`silver.rejected`, with a reason). Not deleted: kept and counted.
    - **Rule:** `NE` and `north-east` mean `northeast` (a written mapping, applied to every row).
    """)
    return


@app.cell
def _(mo, step1_dedup):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE silver.rejected AS
        SELECT *, 'missing charges' AS reject_reason
        FROM silver.step1_dedup
        WHERE charges IS NULL;
        
        CREATE OR REPLACE TABLE silver.insurance AS
        SELECT age::INTEGER          AS age,
               gender,
               bmi::DOUBLE           AS bmi,
               children::INTEGER     AS children,
               smoker = 'yes'        AS smoker,
               CASE WHEN LOWER(TRIM(region)) IN ('ne', 'north-east') THEN 'northeast'
                    ELSE LOWER(TRIM(region)) END AS region,
               charges::DOUBLE       AS charges,
               _source_file
        FROM silver.step1_dedup
        WHERE charges IS NOT NULL;            -- exactly the rows not in silver.rejected
        
        SELECT region, COUNT(*) AS n_rows
        FROM silver.insurance
        GROUP BY region
        ORDER BY region
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Four standard regions now. The Bronze table still has `NE` and `north-east`, so "how many rows did the source send as `NE`?" can still be answered.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ⚖️ Reconcile: Bronze Rows = Valid + Flagged + Rejected + Duplicates
    """)
    return


@app.cell
def _(insurance, insurance_raw, mo, rejected, step1_dedup):
    _df = mo.sql(
        f"""
        SELECT (SELECT COUNT(*) FROM bronze.insurance_raw)                                        AS bronze_rows,
               (SELECT COUNT(*) FROM silver.insurance)                                            AS valid,
               0                                                                                  AS flagged,
               (SELECT COUNT(*) FROM silver.rejected)                                             AS rejected,
               (SELECT COUNT(*) FROM bronze.insurance_raw) - (SELECT COUNT(*) FROM silver.step1_dedup) AS duplicates
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **1,340 = 1,336 valid + 0 flagged + 1 rejected + 3 duplicates** (the 2 rows sent twice + 1 copy that was already in the original file). No rule flags anything in this data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🟡 Gold: a Star Schema and a Business Table (Built Only from Silver)

    Grain of `gold.fact_policy`: **one insured customer**. `region` moves to a dimension with a surrogate key.
    """)
    return


@app.cell
def _(insurance, mo):
    gold_avg = mo.sql(
        f"""
        CREATE OR REPLACE TABLE gold.dim_region AS
        SELECT ROW_NUMBER() OVER (ORDER BY region) AS region_key, region
        FROM (SELECT DISTINCT region FROM silver.insurance);
        
        CREATE OR REPLACE TABLE gold.fact_policy AS
        SELECT r.region_key, s.age, s.gender, s.bmi, s.children, s.smoker, s.charges
        FROM silver.insurance AS s
        JOIN gold.dim_region AS r USING (region);
        
        CREATE OR REPLACE TABLE gold.avg_charges_by_region AS
        SELECT r.region, COUNT(*) AS customers, ROUND(AVG(f.charges), 0) AS avg_charges
        FROM gold.fact_policy AS f
        JOIN gold.dim_region AS r USING (region_key)
        GROUP BY r.region
        ORDER BY avg_charges DESC;
        
        SELECT * FROM gold.avg_charges_by_region
        """
    )
    return (gold_avg,)


@app.cell
def _(gold_avg):
    import matplotlib.pyplot as plt

    _df = gold_avg.to_pandas() if hasattr(gold_avg, "to_pandas") else gold_avg
    plt.figure()
    plt.bar(_df["region"], _df["avg_charges"])
    plt.title("Average Charges by Region (Gold)")
    plt.ylabel("Average charges (US $)")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What Each Layer Gave Us

    | Layer | Answers |
    |---|---|
    | Bronze | "what did the source send?" (six region spellings, one row without charges, three copies) |
    | Silver | "what really happened?" (1,336 customers, four regions, one rejected row with its reason) |
    | Gold | "what does the business need?" (average charges per region; the southeast is highest) |

    The reconciliation (**1,340 = 1,336 + 0 + 1 + 3**) is the proof that the three layers tell one consistent story.
    """)
    return


if __name__ == "__main__":
    app.run()
