---
marp: true
theme: beam
paginate: true
title: Week 1 — SQL Foundations for Analytics
author: Mahmoud Parsian
class: lead
style: |
  section {
    justify-content: flex-start;
  }

  h2 {
    background: linear-gradient(90deg, #2c3e50, #4ca1af);
    color: white;
    padding: 8px 16px;
    border-radius: 6px;
    width: fit-content;
  }
---

# SQL Foundations for Analytics
## Insurance Data Case Study

---

## Why SQL?

- Every analyst speaks SQL
- SQL = bridge between **data** and **decision**
- Foundation for:
  - Data Warehousing
  - BI Tools
  - AI + Data Systems

---

## The Analyst Journey

```
Raw Data 
→ Question 
→ SQL 
→ Pattern 
→ Insight 
→ Decision
```

👉 This course = mastering this pipeline

---

## Dataset Overview

- ~1338 customers
- Real-world healthcare pricing scenario
- Each row = one individual

---

## Columns

| Column   | Meaning |
|----------|--------|
| age      | Age of person |
| bmi      | Health indicator |
| smoker   | Risk factor |
| region   | Geography |
| charges  | Insurance cost |

---

## Business Questions

- Do smokers cost more?
- Does BMI impact cost?
- Are some regions more expensive?
- Do families pay more?

---

# Section 1 — BASIC SQL

---

## First Look at Data

```sql
SELECT * FROM insurance LIMIT 10;
```

👉 Always start by understanding your data

---

## Dataset Size

```sql
SELECT COUNT(*) FROM insurance;
```

👉 Are we working with 1K rows or 1B rows?

---

## Distinct Values

```sql
SELECT DISTINCT region FROM insurance;
```

👉 Understand categories early

---

## Basic Aggregation

```sql
SELECT AVG(charges) FROM insurance;
```

👉 Baseline metric

---

## Top Customers

```sql
SELECT *
FROM insurance
ORDER BY charges DESC
LIMIT 5;
```

👉 Who are the expensive cases?

---

# Section 2 — INTERMEDIATE SQL

---

## Group By — Key Skill

```sql
SELECT smoker, AVG(charges)
FROM insurance
GROUP BY smoker;
```

👉 FIRST REAL INSIGHT

---

## 🚨 Business Insight

- Smokers ≫ Non-smokers in cost
- Smoking = high risk = high premium

👉 This is actionable

---

## By Region

```sql
SELECT region, AVG(charges)
FROM insurance
GROUP BY region;
```

👉 Geography matters

---

## CASE — Categorization

```sql
SELECT 
  CASE 
    WHEN age < 30 THEN 'Young'
    WHEN age < 50 THEN 'Middle'
    ELSE 'Senior'
  END AS age_group,
  AVG(charges)
FROM insurance
GROUP BY age_group;
```

👉 Turn raw data → business segments

---

## BMI Categories

```sql
SELECT 
  CASE 
    WHEN bmi < 25 THEN 'Normal'
    WHEN bmi < 30 THEN 'Overweight'
    ELSE 'Obese'
  END AS bmi_group,
  AVG(charges)
FROM insurance
GROUP BY bmi_group;
```

👉 Health → cost relationship

---

## Multiple Dimensions

```sql
SELECT region, smoker, AVG(charges)
FROM insurance
GROUP BY region, smoker;
```

👉 Multi-dimensional thinking (important for DW)

---

# Section 3 — ADVANCED SQL

---

## Window Functions

```sql
SELECT *,
RANK() OVER (ORDER BY charges DESC) AS rank
FROM insurance;
```

👉 Ranking without losing rows

---

## Top per Region

```sql
SELECT *
FROM (
    SELECT *,
           RANK() OVER (PARTITION BY region ORDER BY charges DESC) rnk
    FROM insurance
) t
WHERE rnk <= 2;
```

👉 Classic interview + real-world problem

---

## Contribution Analysis

```sql
SELECT 
  smoker,
  SUM(charges) AS total,
  SUM(charges) * 100.0 / SUM(SUM(charges)) OVER () AS pct
FROM insurance
GROUP BY smoker;
```

👉 Who drives total cost?

---

# Section 4 — DEBUGGING (CRITICAL SKILL)

---

## Intentional Error

```sql
SELECT region AVG(charges)
FROM insurance
GROUP BY region;
```

❌ What’s wrong?

---

## Fix

```sql
SELECT region, AVG(charges)
FROM insurance
GROUP BY region;
```

---

## Teaching Moment

👉 SQL is not about memorization  
👉 It is about:
- reading errors
- thinking logically
- debugging

---

# Section 5 — BUSINESS STORY

---

## What Did We Learn?

- Smokers cost significantly more
- BMI increases cost
- Regional variation exists
- Segmentation matters

---

## Real Business Actions

- Adjust premiums
- Target health programs
- Risk-based pricing
- Customer segmentation

---

# Section 6 — BRIDGE TO DATA WAREHOUSING

---

## Problem with Raw Data

- Not clean
- Not structured for analytics
- Repeated transformations

---

## Solution → Data Warehousing

Next weeks:

- Data Models
- Star Schema
- Fact vs Dimension
- Medallion Architecture

---

## Example Mapping

| Raw | Warehouse |
|-----|----------|
| insurance.csv | fact_insurance |
| region | dim_region |
| smoker | dim_risk |

---

# Week 1 Summary

- SQL = analytical thinking tool
- Queries → insights → decisions
- Foundation for everything ahead

---

# Next Week

👉 Data Warehousing Foundations

---

# Thank You 🚀
