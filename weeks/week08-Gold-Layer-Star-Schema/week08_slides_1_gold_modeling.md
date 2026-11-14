---
marp: true
theme: default
paginate: true
size: 16:9
---

# Week 8  
## Gold Layer — Analytical Modeling (Elite v7 — FINAL COMPLETE MASTER)

---

# PART 0 — GOLD = DECISION ENGINE

---

## Ultimate Purpose

Data is not valuable because it exists.  
Data is valuable because it **changes decisions**.

---

## Gold Layer Role

👉 transforms data into **decision-ready insights**

---

## Reality Check

- CEOs don’t see Bronze  
- Analysts rarely touch Silver  

👉 Everyone consumes Gold

---

# PART 1 — BUSINESS-FIRST MODELING (DEEP)

---

## WRONG ORDER

Tables → Queries → Questions  

---

## CORRECT ORDER

Questions → KPIs → Model → Tables  

---

## Example

Question:
👉 “Which regions are most expensive?”

Model implication:
- need dim_region  
- need fact.charges  

---

## Insight

👉 Gold design is driven by **questions**

---

# PART 2 — STAR SCHEMA (ULTIMATE VIEW)

---

```text
                 dim_time
                    |
dim_region — fact_insurance — dim_smoker
                    |
                dim_person
```

---

## Interpretation

Fact = numeric truth  
Dimensions = interpretation context  

---

## Critical Insight

👉 Without dimensions, facts are meaningless

---

# PART 3 — GRAIN (ULTIMATE DEEP DIVE)

---

## Golden Rule

👉 Write grain as a sentence

---

## Example

“One row represents one person per year”

---

## Why This Matters

Everything depends on grain:
- joins  
- aggregations  
- KPIs  

---

## Deep Example

| person | year | charges |
|--------|------|--------|
| A | 2021 | 100 |
| A | 2021 | 100 |

SUM = 200 (wrong if duplicate)

---

## Fix

👉 enforce unique grain key

---

## Insight

👉 Grain errors are invisible but fatal

---

# PART 4 — ADDITIVE VS NON-ADDITIVE (CRITICAL)

---

## Types of Measures

Additive:
- sum works (charges)

Non-additive:
- avg, ratios

---

## Pitfall

AVG of averages is WRONG

---

## Example

Group A avg = 100  
Group B avg = 200  

Global avg ≠ (100+200)/2

---

## Insight

👉 aggregation logic must match metric type

---

# PART 5 — DIMENSION STRATEGY (ADVANCED)

---

## Good Dimensions

- small  
- stable  
- reusable  

---

## Example Dimensions

- region  
- smoker  
- age_group  
- time  

---

## Bad Dimension Example

transaction_id (too granular)

---

## Insight

👉 dimension design defines analysis flexibility

---

# PART 6 — SURROGATE KEYS (PERFORMANCE + LOGIC)

---

## Natural Key Problem

Text mismatch:
- “north-east”
- “northeast”

---

## Surrogate Key

region_id = 1

---

## Why It Matters

- fast joins  
- smaller data  
- consistency  

---

## Insight

👉 Gold optimizes both correctness and speed

---

# PART 7 — FULL SQL PIPELINE (EXPANDED)

---

## Step 1 — Dimension (Region)

```sql
CREATE TABLE dim_region AS
SELECT DISTINCT
  ROW_NUMBER() OVER() AS region_id,
  region
FROM silver_insurance;
```

---

## Step 2 — Dimension (Smoker)

```sql
CREATE TABLE dim_smoker AS
SELECT DISTINCT
  ROW_NUMBER() OVER() AS smoker_id,
  smoker
FROM silver_insurance;
```

---

## Step 3 — Fact Table

```sql
CREATE TABLE fact_insurance AS
SELECT
  r.region_id,
  s.smoker_id,
  si.charges,
  si.year
FROM silver_insurance si
JOIN dim_region r ON si.region = r.region
JOIN dim_smoker s ON si.smoker = s.smoker;
```

---

## Step 4 — Mart

```sql
CREATE TABLE mart_region_year AS
SELECT
  year,
  r.region,
  AVG(f.charges) AS avg_charges,
  COUNT(*) AS population
FROM fact_insurance f
JOIN dim_region r ON f.region_id = r.region_id
GROUP BY year, r.region;
```

---

# PART 8 — VALIDATION (REALISTIC)

---

## Required Checks

1. Fact row count matches Silver  
2. No NULL foreign keys  
3. Dimension uniqueness  
4. KPI consistency  

---

## Example

```sql
SELECT COUNT(*) FROM fact WHERE region_id IS NULL;
```

---

## Insight

👉 validation = trust

---

# PART 9 — KPI ENGINEERING (ADVANCED)

---

## KPI = Data + Rules + Context

---

## Example

Average charges:

Questions:
- include outliers?
- include missing?
- per year or global?

---

## Insight

👉 KPIs are engineered, not discovered

---

# PART 10 — PERFORMANCE ARCHITECTURE

---

## Bottlenecks

- large joins  
- full table scans  

---

## Solutions

- partition by year  
- indexes on keys  
- materialized marts  

---

## Insight

👉 Gold = performance layer

---

# PART 11 — CASE STUDY (DEEP)

---

## Raw Data

100, 200, 300, 10000

---

## Decision A

Include outlier → avg = 2650  

---

## Decision B

Exclude outlier → avg = 200  

---

## Question

Which is correct?

---

## Answer

👉 depends on business definition

---

# PART 12 — MULTI-DIMENSION QUERY (ADVANCED)

---

## SQL

```sql
SELECT
  r.region,
  s.smoker,
  f.year,
  AVG(f.charges)
FROM fact_insurance f
JOIN dim_region r ON f.region_id = r.region_id
JOIN dim_smoker s ON f.smoker_id = s.smoker_id
GROUP BY r.region, s.smoker, f.year;
```

---

## Insight

👉 Gold enables complex slicing with simple SQL

---

# PART 13 — DATA MART STRATEGY (DEEP)

---

## When to Build Mart?

- repeated query  
- dashboard use  
- heavy aggregation  

---

## Types

- regional mart  
- temporal mart  
- segmentation mart  

---

## Insight

👉 marts = optimized business answers

---

# PART 14 — FAILURE MODES (REAL INDUSTRY)

---

## ❌ Wrong grain

---

## ❌ Missing keys

---

## ❌ Duplicate facts

---

## ❌ KPI inconsistency

---

## ❌ Over-engineering

---

## Insight

👉 most failures are silent

---

# PART 15 — DESIGN TRADEOFFS

---

## Tradeoffs

- flexibility vs speed  
- detail vs simplicity  
- storage vs compute  

---

## Insight

👉 no perfect model, only optimal model

---

# PART 16 — EXAM-STYLE QUESTIONS

---

## Q1

What happens if grain is too fine?

---

## Q2

Why not compute KPIs in dashboards?

---

## Q3

Why use surrogate keys?

---

## Q4

When should a mart be created?

---

# PART 17 — MINI PROJECT EXERCISE

---

## Given

Silver dataset

---

## Design

- fact table  
- 3 dimensions  
- 2 marts  

---

## Explain

- grain  
- KPIs  
- tradeoffs  

---

# PART 18 — FINAL MASTER VISUAL

---

```text
Bronze → Silver → Gold

Raw → Clean → Integrate → Model → Aggregate → Insight → Decision
```

---

# FINAL MESSAGE

---

You are not building tables.

You are:

👉 defining how a company measures itself  
👉 encoding business logic  
👉 enabling decisions at scale  

---

## FINAL TRUTH

Bad Gold → wrong decisions  
Good Gold → competitive advantage
