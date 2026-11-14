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
    # 📊 Executive Dashboard — Insurance Medallion DW (Gold Layer)

    **Database:** `insurance_medallion_dw.duckdb`

    This notebook demonstrates executive-level analytics using a **star schema (Gold layer)**.

    Each section includes:
    - 🧠 Business Question
    - 💬 Natural Language (NL) Query
    - 🧾 SQL (star-schema correct)
    - 📊 Visualization
    - 💡 Insight

    ---

    ## 🧠 Star Schema Reminder
    - **Fact**: `gold.fact_insurance_charges` (measures + keys)
    - **Dimensions**:
      - `gold.dim_region` → region
      - `gold.dim_year` → year
      - `gold.dim_risk_profile` → smoker, bmi_group, semantic flags

    ---
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import matplotlib.pyplot as plt

    con = duckdb.connect('insurance_medallion_dw.duckdb')
    print('Connected to DuckDB')
    return con, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🔷 1. Cost Trend by Year

    **🧠 Business Question:** Are insurance costs increasing over time?

    **💬 NL Query:** Show average insurance charges by year.
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT
        y.source_year,
        COUNT(*) AS policies,
        ROUND(AVG(f.charges), 2) AS avg_charges
    FROM gold.fact_insurance_charges f
    JOIN gold.dim_year y
        ON f.year_key = y.year_key
    GROUP BY y.source_year
    ORDER BY y.source_year
    """).df()

    plt.figure(figsize=(7,4))
    plt.plot(_df['source_year'], _df['avg_charges'], marker='o')
    plt.title('Average Charges by Year')
    plt.xlabel('Year')
    plt.ylabel('Avg Charges')
    plt.tight_layout()
    plt.show()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🔷 2. Regional Comparison

    **🧠 Business Question:** Which regions are most expensive?

    **💬 NL Query:** Compare average insurance cost across regions.
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT
        r.region,
        COUNT(*) AS policies,
        ROUND(AVG(f.charges), 2) AS avg_charges
    FROM gold.fact_insurance_charges f
    JOIN gold.dim_region r
        ON f.region_key = r.region_key
    GROUP BY r.region
    ORDER BY avg_charges DESC
    """).df()

    plt.figure(figsize=(8,4))
    plt.bar(_df['region'], _df['avg_charges'])
    plt.title('Average Charges by Region')
    plt.xlabel('Region')
    plt.ylabel('Avg Charges')
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.show()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🔷 3. Impact of Smoking

    **🧠 Business Question:** How much does smoking affect cost?

    **💬 NL Query:** Compare charges between smokers and non-smokers.
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT
        rp.smoker,
        COUNT(*) AS policies,
        ROUND(AVG(f.charges), 2) AS avg_charges
    FROM gold.fact_insurance_charges f
    JOIN gold.dim_risk_profile rp
        ON f.risk_profile_key = rp.risk_profile_key
    GROUP BY rp.smoker
    ORDER BY avg_charges DESC
    """).df()

    plt.figure(figsize=(6,4))
    plt.bar(_df['smoker'], _df['avg_charges'])
    plt.title('Smoking vs Charges')
    plt.xlabel('Smoker')
    plt.ylabel('Avg Charges')
    plt.tight_layout()
    plt.show()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🔷 4. BMI vs Smoking

    **🧠 Business Question:** Are BMI and smoking related? How do they impact cost together?

    **💬 NL Query:** Show average charges by BMI group and smoking status.
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT
        rp.smoker,
        rp.bmi_group,
        ROUND(AVG(f.charges), 2) AS avg_charges
    FROM gold.fact_insurance_charges f
    JOIN gold.dim_risk_profile rp
        ON f.risk_profile_key = rp.risk_profile_key
    GROUP BY rp.smoker, rp.bmi_group
    ORDER BY avg_charges DESC
    """).df()

    pivot = _df.pivot(index='bmi_group', columns='smoker', values='avg_charges')

    pivot.plot(kind='bar', figsize=(8,4))
    plt.title('BMI vs Smoking Impact on Charges')
    plt.xlabel('BMI Group')
    plt.ylabel('Avg Charges')
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.show()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🔷 5. Low-Charge Smokers (Anomaly Detection)

    **🧠 Business Question:** Are there smokers with unusually low charges?

    **💬 NL Query:** Identify smokers with unexpectedly low insurance costs.
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT
        rp.semantic_low_charge_smoker_flag,
        COUNT(*) AS policies,
        ROUND(AVG(f.charges), 2) AS avg_charges
    FROM gold.fact_insurance_charges f
    JOIN gold.dim_risk_profile rp
        ON f.risk_profile_key = rp.risk_profile_key
    WHERE rp.smoker = 'yes'
    GROUP BY rp.semantic_low_charge_smoker_flag
    ORDER BY rp.semantic_low_charge_smoker_flag
    """).df()

    plt.figure(figsize=(6,4))
    plt.bar(_df['semantic_low_charge_smoker_flag'], _df['avg_charges'])
    plt.title('Low-Charge Smokers (Anomaly)')
    plt.xlabel('Flag (1 = anomaly)')
    plt.ylabel('Avg Charges')
    plt.tight_layout()
    plt.show()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🏆 Executive Summary

    - Smoking is the strongest driver of cost
    - BMI amplifies health risk significantly
    - Regional variation exists in pricing
    - Data pipeline successfully cleans ~20% bad data
    - Feature engineering enabled anomaly detection

    ---

    ✅ This notebook demonstrates **production-grade analytics on a Medallion architecture**
    """)
    return


if __name__ == "__main__":
    app.run()
