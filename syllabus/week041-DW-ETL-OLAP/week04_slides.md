---
marp: true
title: Week 4 — ETL, OLAP, and Medallion Architecture (Ultimate)
paginate: true
theme: default
class: lead
---

# Week 4
## ETL, OLAP, and Medallion Architecture

---

# 🎯 Learning Objectives

- Understand the full ETL and ELT pipeline
- Learn how OLAP supports analytical exploration
- Master Bronze, Silver, and Gold layers
- Connect SQL and Python to business-ready analytics

---

# 🧠 Why Week 4 Matters

- SQL analysis is only as good as the data underneath it
- Real businesses need repeatable pipelines, not one-off queries
- Modern analytics requires both engineering discipline and analytical thinking
- This week connects data engineering to business intelligence

---

# 📦 Before Analytics: Raw Data Problems

- Raw data often has missing values, wrong types, and messy formatting
- Different files may use different naming rules for the same concept
- Analysts cannot trust dashboards built on inconsistent raw data
- Pipelines exist to turn raw data into trusted data

---

# 💡 ETL in Plain English

- **Extract**: get data from source systems
- **Transform**: clean, standardize, enrich, and validate
- **Load**: place data into analytical storage
- The goal is trust, consistency, and speed for business analysis

---

# 🧭 ETL vs ELT

- ETL transforms before loading into the warehouse
- ELT loads raw data first, then transforms inside the warehouse
- Modern cloud systems often prefer ELT because warehouse compute is strong
- Both approaches require careful business logic and data quality checks

---

# 🏢 Business Scenario

- A retail company receives orders from stores, web systems, and suppliers
- Source data arrives as CSV, API responses, and transactional database exports
- Leaders want reliable revenue dashboards and product performance reports
- We need a pipeline from raw operational data to decision-ready data

---

# 🔹 Extract Phase

- Pull data from OLTP systems, files, logs, APIs, or streams
- Preserve the original data as faithfully as possible
- Capture metadata such as load time or source file
- Extraction is about completeness, not yet about perfection

---

# 🔹 Transform Phase

- Fix data types, formatting, duplicates, and missing values
- Standardize naming, dates, and categorical values
- Add derived fields that analysts actually need
- This is where business rules become executable logic

---

# 🔹 Load Phase

- Store cleaned data in analytical tables
- Organize tables for fast reads and understandable SQL
- Support repeatable reporting and dashboard refreshes
- Loading completes the pipeline but not the data lifecycle

---

# 🧪 SQL Example — Basic Cleaning

```sql
SELECT
    LOWER(TRIM(region)) AS region_clean,
    CAST(amount AS DOUBLE) AS amount_num
FROM raw_sales;
```

- `TRIM` removes extra spaces from messy text
- `LOWER` standardizes case so categories are consistent
- `CAST` converts text into a true numeric type for analysis
- This is classic Silver-layer transformation logic

---

# 🐍 Python Example — Basic Cleaning

```python
import pandas as pd

df = pd.read_csv("raw_sales.csv")
df["region_clean"] = df["region"].str.strip().str.lower()
df["amount_num"] = pd.to_numeric(df["amount"], errors="coerce")
df.head()
```

- Python is often used for inspection, orchestration, or preprocessing
- String cleanup and type conversion mirror SQL transformation logic
- `errors="coerce"` is useful when dirty values appear in numeric columns
- Python complements SQL well in ETL workflows

---

# 🧪 SQL Example — Deduplication Pattern

```sql
SELECT DISTINCT *
FROM raw_customers;
```

- `DISTINCT` removes exact duplicate rows
- This is a simple but common data-quality step
- Deduplication prevents inflated counts and wrong KPIs
- Always ask whether duplicates are exact or business duplicates

---

# 🐍 Python Example — Deduplication Pattern

```python
df = pd.read_csv("raw_customers.csv")
df = df.drop_duplicates()
print(df.shape)
```

- Python makes it easy to inspect row counts before and after cleanup
- This supports data-quality validation during transformation
- In practice, teams often log duplicate counts for pipeline monitoring
- Deduplication should be documented, not done silently

---

# ⚠️ Common Data Quality Problems

- Missing values break aggregations and models
- Inconsistent types cause SQL and Python errors
- Duplicate rows distort revenue and customer counts
- Bad source data creates bad business decisions

---

# 🧪 SQL Example — Missing Value Check

```sql
SELECT
    COUNT(*) AS total_rows,
    COUNT(region) AS non_null_region,
    COUNT(amount) AS non_null_amount
FROM raw_sales;
```

- `COUNT(*)` counts all rows, including nulls
- `COUNT(column)` counts only non-null values
- This quickly reveals missingness in key fields
- Basic data profiling should happen early in every pipeline

---

# 🐍 Python Example — Missing Value Check

```python
df = pd.read_csv("raw_sales.csv")
print(df.isna().sum())
```

- Python makes null inspection very fast and visual
- This is useful before designing transformation rules
- Analysts can spot whether issues are rare or widespread
- Profiling raw data reduces surprises later in the pipeline

---

# 🧱 Introducing Medallion Architecture

- Bronze stores raw ingested data
- Silver stores cleaned, validated, structured data
- Gold stores business-ready aggregates and semantic views
- Each layer has a different purpose and audience

---

# 🥉 Bronze Layer

- Raw ingestion should preserve original detail
- Minimal transformation keeps the source of truth intact
- Bronze supports reprocessing when business logic changes
- This layer is for capture and traceability, not dashboarding

---

# 🥈 Silver Layer

- Silver applies cleaning, standardization, and validation
- Data becomes trustworthy enough for broader reuse
- This is often where joins and business rules begin
- Silver is the workhorse layer for analytical preparation

---

# 🥇 Gold Layer

- Gold exposes business metrics and curated summaries
- Tables are optimized for analyst productivity and dashboards
- Gold answers questions like revenue by region or top products
- The closer to executives, the more likely they consume Gold

---

# 🧪 SQL Example — Bronze Query

```sql
SELECT *
FROM bronze_sales
LIMIT 10;
```

- Bronze queries are mostly for inspection and validation
- We expect noise, inconsistencies, and source-system weirdness
- The goal is to verify ingestion rather than final insight
- This is a source-trust checkpoint

---

# 🐍 Python Example — Bronze Inspection

```python
import pandas as pd

bronze_df = pd.read_parquet("bronze_sales.parquet")
bronze_df.head()
```

- Python is useful for raw-file inspection outside SQL
- Analysts can preview schemas and values quickly
- This is common during early ingestion validation
- It helps compare raw files to loaded Bronze tables

---

# 🧪 SQL Example — Silver Query

```sql
SELECT
    order_id,
    LOWER(TRIM(region)) AS region,
    CAST(amount AS DOUBLE) AS amount
FROM bronze_sales
WHERE amount IS NOT NULL;
```

- Silver transformations clean and filter obviously bad data
- Columns become standardized and analysis-ready
- Business rules begin to shape the dataset here
- Silver makes downstream Gold logic simpler and safer

---

# 🐍 Python Example — Silver Transformation

```python
silver_df = bronze_df.copy()
silver_df["region"] = silver_df["region"].str.strip().str.lower()
silver_df["amount"] = pd.to_numeric(silver_df["amount"], errors="coerce")
silver_df = silver_df[silver_df["amount"].notna()]
silver_df.head()
```

- Python transformations can mirror SQL logic one-to-one
- This is helpful when teaching equivalent concepts across tools
- Filtering null amounts is a common trust-building step
- Silver exists to reduce ambiguity before analysis

---

# 🧪 SQL Example — Gold Query

```sql
SELECT
    region,
    SUM(amount) AS total_revenue
FROM silver_sales
GROUP BY region
ORDER BY total_revenue DESC;
```

- Gold focuses on business metrics, not raw cleanup
- Aggregation becomes the primary concern at this layer
- Results should be simple for analysts to consume
- Gold is the decision-ready layer of the medallion pattern

---

# 🐍 Python Example — Gold Aggregation

```python
gold_df = (
    silver_df.groupby("region", as_index=False)["amount"]
    .sum()
    .rename(columns={"amount": "total_revenue"})
    .sort_values("total_revenue", ascending=False)
)
gold_df
```

- Python groupby mirrors SQL aggregation closely
- This is useful when explaining how BI metrics are computed
- Gold outputs are often small, readable, and dashboard-friendly
- The business conversation usually starts here

---

# 📈 Python Example — Plot Gold Results

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 4))
plt.bar(gold_df["region"], gold_df["total_revenue"])
plt.title("Revenue by Region")
plt.xlabel("Region")
plt.ylabel("Total Revenue")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()
```

- Plots help move from numbers to pattern recognition
- Visuals make Gold outputs easier to discuss in class
- This bridges data engineering to business communication
- A chart often reveals what a table hides

---

# 🧠 Why Medallion Works

- It separates raw capture from cleaning and from reporting
- It reduces confusion about where transformations belong
- It makes debugging easier when a business metric looks wrong
- It supports reusability across many analytical use cases

---

# 🏗️ Pipeline Thinking

- Data should move through clearly defined stages
- Each stage should have a specific purpose and owner
- Good pipelines are repeatable, testable, and explainable
- Pipeline design is as important as query design

---

# 🧪 SQL Example — Validation Rule

```sql
SELECT *
FROM silver_sales
WHERE amount < 0;
```

- Negative revenue may indicate refunds, errors, or bad data
- Validation queries are essential in the Silver layer
- Teams should decide whether bad rows are fixed, flagged, or excluded
- Data quality is not just technical; it is also business policy

---

# 🐍 Python Example — Validation Rule

```python
bad_rows = silver_df[silver_df["amount"] < 0]
print(bad_rows)
```

- Python makes bad-row inspection easy during debugging
- This is especially helpful in teaching and development
- Validation is stronger when both SQL and Python can verify results
- Trustworthy pipelines always include checks

---

# 📊 OLAP Refresher

- OLAP means online analytical processing
- It emphasizes multi-dimensional aggregation and exploration
- Analysts move across time, geography, products, and customers
- OLAP is a thinking style as much as a technology style

---

# 📦 Dimensions and Measures

- Dimensions describe business context: who, what, when, where
- Measures are the numeric values we aggregate
- OLAP combines measures across many dimension cuts
- Good dimensional design makes business questions easier to express

---

# 🧮 OLAP Example — Basic Multi-Dimensional Query

```sql
SELECT
    region,
    product,
    SUM(revenue) AS total_revenue
FROM sales
GROUP BY region, product;
```

- This query analyzes two dimensions at once
- It reveals product performance inside each region
- Multi-dimensional thinking is central to warehouse analytics
- The goal is not just totals, but structured comparison

---

# 🐍 Python Example — Pivot Table

```python
pivot = sales_df.pivot_table(
    values="revenue",
    index="region",
    columns="product",
    aggfunc="sum",
    fill_value=0
)
pivot
```

- Pivot tables in Python mirror OLAP thinking nicely
- They help students visualize dimension intersections
- This is a strong bridge between SQL and spreadsheet-style analysis
- Pivoting makes cube-like thinking concrete

---

# 🔼 Roll-Up

- Roll-up aggregates to a higher business level
- Example: day to month, month to quarter, quarter to year
- It supports strategic summaries for leaders
- Roll-up reduces detail in exchange for simplicity

---

# 🧪 SQL Example — Roll-Up by Month

```sql
SELECT
    year,
    month,
    SUM(revenue) AS total_revenue
FROM sales
GROUP BY year, month
ORDER BY year, month;
```

- Grouping by year and month is a practical roll-up pattern
- This supports trend detection and period-based reporting
- Time roll-ups are among the most common warehouse queries
- Businesses rarely look only at individual transactions

---

# 🔽 Drill-Down

- Drill-down moves from summary to more detail
- Example: year to quarter, quarter to month, month to day
- It helps explain why a high-level metric changed
- Drill-down is a core investigative pattern in BI

---

# 🧪 SQL Example — Drill-Down by Day

```sql
SELECT
    full_date,
    SUM(revenue) AS daily_revenue
FROM sales
GROUP BY full_date
ORDER BY full_date;
```

- Daily detail reveals spikes, dips, and anomalies
- This is the natural follow-up to monthly or yearly summaries
- Drill-down supports root-cause analysis
- Good dimensional time tables make this easy

---

# 🔪 Slice

- Slice fixes one dimension value to narrow analysis
- Example: only region = 'west'
- It simplifies the question to one focused perspective
- Slicing is common in managerial reporting

---

# 🧪 SQL Example — Slice

```sql
SELECT
    product,
    SUM(revenue) AS total_revenue
FROM sales
WHERE region = 'west'
GROUP BY product
ORDER BY total_revenue DESC;
```

- A slice isolates one region while keeping product comparison
- This creates a focused, actionable report
- Slicing is useful when teams own a specific segment
- Smaller scope often produces clearer decisions

---

# 🎲 Dice

- Dice filters on multiple dimensions at the same time
- Example: west region, bikes category, 2023 only
- This creates a highly targeted business view
- Dicing supports nuanced decision-making

---

# 🧪 SQL Example — Dice

```sql
SELECT
    region,
    category,
    year,
    SUM(revenue) AS total_revenue
FROM sales
WHERE region = 'west'
  AND category = 'bikes'
  AND year = 2023
GROUP BY region, category, year;
```

- Dicing focuses analysis on a specific business context
- This is how managers often ask real questions
- A good warehouse supports this naturally
- Dice is more powerful than a generic summary

---

# 🧊 CUBE

- `CUBE` generates many subtotal combinations automatically
- It is powerful for multi-dimensional exploration
- Analysts can see detail, subtotal, and grand-total views together
- CUBE is conceptually important even when used selectively

---

# 🧪 SQL Example — CUBE

```sql
SELECT
    region,
    category,
    SUM(revenue) AS total_revenue
FROM sales
GROUP BY CUBE(region, category);
```

- This creates totals by region, by category, by both, and overall
- It reduces the need to write multiple separate queries
- CUBE is useful for broad dimensional exploration
- It can be computationally expensive on large data

---

# 🪜 ROLLUP

- `ROLLUP` generates hierarchical subtotals
- It is ideal for dimensions with natural hierarchy
- Time analysis is a classic ROLLUP use case
- ROLLUP is more structured than CUBE

---

# 🧪 SQL Example — ROLLUP

```sql
SELECT
    year,
    month,
    SUM(revenue) AS total_revenue
FROM sales
GROUP BY ROLLUP(year, month);
```

- This produces month totals, year totals, and grand totals
- It matches common reporting hierarchy expectations
- ROLLUP is excellent for board-style summaries
- It is a natural fit for time dimensions

---

# 🧠 Business Insight Example — Revenue by Region

- If one region dominates revenue, strategy may be overconcentrated
- If weak regions lag, the business may need targeted interventions
- Regional comparison supports expansion and staffing decisions
- A simple Gold query can drive major decisions

---

# 🧠 Business Insight Example — Product Mix

- Strong category revenue does not always mean strong profitability
- Product mix affects marketing, inventory, and supplier strategy
- Accessory sales may support bike sales indirectly
- Analysts should always connect metrics to business context

---

# 🧠 Business Insight Example — Time Trends

- Growth over time may reflect seasonality, promotions, or expansion
- Declines may signal operational issues or market weakness
- Leaders need both roll-up summaries and drill-down detail
- Time intelligence is central to warehouse design

---

# 🔍 ETL Monitoring

- Pipelines should record row counts and error counts
- Teams need visibility into failures and anomalies
- Monitoring prevents silent data corruption
- Good data systems are observable, not mysterious

---

# 🧪 SQL Example — Row Count Validation

```sql
SELECT
    'bronze' AS layer,
    COUNT(*) AS row_count
FROM bronze_sales
UNION ALL
SELECT
    'silver' AS layer,
    COUNT(*) AS row_count
FROM silver_sales
UNION ALL
SELECT
    'gold' AS layer,
    COUNT(*) AS row_count
FROM gold_sales;
```

- Row-count checks help detect unexpected data loss
- Comparing layers is a practical ETL monitoring pattern
- Validation queries are simple but powerful
- Pipelines should not rely on trust alone

---

# 🐍 Python Example — Layer Validation Report

```python
report = {
    "bronze_rows": len(bronze_df),
    "silver_rows": len(silver_df),
    "gold_rows": len(gold_df),
}
print(report)
```

- Python can orchestrate and summarize pipeline health checks
- A small validation report is useful in teaching and production
- Monitoring should be part of the workflow, not an afterthought
- Data trust is built through evidence

---

# 🧠 ETL Documentation Matters

- Business rules should be written down, not hidden in code
- Analysts need to know how Gold metrics were derived
- Documentation improves maintainability and onboarding
- Good pipelines are explainable to both engineers and analysts

---

# 🧩 Putting It All Together

- Bronze captures the source truth
- Silver creates trust and structure
- Gold creates business value and analytical speed
- OLAP turns Gold into insight across multiple dimensions

---

# 📘 End-to-End Mini Tutorial

1. Ingest raw files into Bronze
2. Clean and standardize into Silver
3. Aggregate and curate into Gold
4. Use OLAP queries and charts for decision-making

- This is the modern analytical lifecycle
- SQL and Python both play important roles
- Architecture determines analytical ease
- Good pipeline design multiplies business value

---

# 🎯 Final Summary

- ETL and ELT turn raw inputs into trustworthy analytical assets
- OLAP enables rich multi-dimensional exploration of business performance
- Medallion architecture organizes data by purpose and trust level
- SQL and Python together provide a practical modern analytics toolkit

---

# 💬 Final Thought

- Bad raw data creates confusion
- Good Silver data creates trust
- Great Gold data creates decisions
- Strong architecture turns analytics into a repeatable business capability
