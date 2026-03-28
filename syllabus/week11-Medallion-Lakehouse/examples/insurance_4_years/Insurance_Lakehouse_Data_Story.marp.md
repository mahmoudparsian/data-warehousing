---
marp: true
title: Insurance Lakehouse Data Story (DuckDB)
paginate: true
size: 16:9
---

# Insurance Lakehouse Data Story  
### Bronze → Silver → Gold with DuckDB (2021–2024)

**Dataset:** insurance members with demographics and annual charges  
**Goal:** teach lakehouse layers + realistic analytics with simple tools

---

## Business framing

An insurer wants to understand:

- **Cost drivers** (smoking, BMI, age, family size)
- **Regional differences**
- **Year-over-year trends** (inflation, distribution changes)
- **Outliers** (extreme claims)

This is a great teaching case because it’s small, interpretable, and very “analytics-friendly.”

---

## Data layers in a lakehouse

### Bronze (raw)
- Raw CSV files, minimal assumptions
- Preserves original shape & categories
- Adds *partition metadata* at read time (e.g., `year` from file name)

### Silver (cleaned)
- Standardize types and category values
- Apply data quality rules
- Add derived attributes used often in analytics

### Gold (curated)
- KPI tables and curated views
- Designed for BI dashboards and repeatable reporting

---

## Bronze layer in this project

**Files**
- `insurance.2021.csv`
- `insurance.2022.csv`
- `insurance.2023.csv`
- `insurance.2024.csv`

**Key teaching concept:**  
The `year` column is *not stored in the raw rows* — it is injected from the filename on read.

---

## Bronze → DuckDB: schema inference

DuckDB can infer metadata directly from CSV:

- column names
- detected types
- nullability
- fast scanning (no external engine needed)

This makes it perfect for explaining “raw landing + discoverability.”

---

## Silver layer: what changes?

We convert raw rows into a clean, consistent table:

- enforce types (`age` int, `bmi` double, `charges` double)
- normalize categories (lower/trim)
- validate domains (age range, BMI range, region set)
- remove duplicates (safe-ish for teaching)
- derive:
  - `bmi_class` (underweight/normal/overweight/obese)
  - `age_band` (18–29, …)

**Result:** trusted data for consistent analytics.

---

## Gold layer: why it exists

Gold answers “what the business asks repeatedly”:

- Average / median / p90 charges by year
- Total charges by year
- Smoker vs non-smoker KPIs
- Region rollups

Gold is where you design tables for dashboards & stakeholders.

---

## What we learned from trends (example insights)

In a realistic insurance dataset, we usually see:

- **Smokers** have much higher average charges
- Charges increase with **age**
- **Obesity** correlates with higher costs (not perfectly)
- **Outliers** heavily affect totals (p90/p95 matter)
- Regions differ modestly (mix + pricing variation)

---

## Example Gold KPI table (yearly)

A yearly KPI view typically includes:

- members
- avg charges
- median charges
- p90 charges
- total charges
- avg smoker charges
- avg non-smoker charges

This single view can power multiple dashboard pages.

---

## Teaching angle: the same SQL “means different things” by layer

- Bronze query: “what did we receive?” (raw validation)
- Silver query: “what do we trust?” (cleaned truth)
- Gold query: “what will we report?” (curated metric)

**Takeaway:** layers are a *contract* about quality and intent.

---

## 10 Insights used in the notebook

1. Avg charges trend by year  
2. Smoker vs non-smoker gap by year  
3. Region ranking by year (avg charges)  
4. 90th percentile charges trend  
5. BMI class composition by year  
6. Top 10 high-charge members per year  
7. Children vs charges (split by smoker)  
8. Segment view: age-band × BMI-class (latest year)  
9. Above 95th percentile counts (outlier proxy)  
10. Contribution of smoker vs non-smoker to total cost

---

## Wrap-up

This mini-lakehouse demonstrates:

- file partitioning by year
- “injecting” partition keys during ingestion
- Silver data quality + derived attributes
- Gold KPI design for repeatable analytics
- meaningful query patterns (percentiles, ranking, segmentation)

**Next extension:** add a small “data quality report” table and show how failures flow through the layers.

---
