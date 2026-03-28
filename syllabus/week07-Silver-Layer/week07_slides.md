---
marp: true
theme: default
paginate: true
size: 16:9
---

# Week 7  
## Silver — Cleaning, Conformance & Integration (Elite v3 — Diagrams + Full SQL Pipeline)

---

# PART 0 — FROM CLEANING TO INTEGRATION

---

## Recap

Week 6:
- make one dataset trustworthy

Week 7:
- make multiple datasets agree

---

## Core Shift

👉 Cleaning fixes records  
👉 Conformance fixes meaning  
👉 Integration fixes system boundaries

---

## Critical Insight

Two datasets can each be “clean”
and still produce the wrong answer when combined.

---

# PART 1 — VISUAL BIG PICTURE

---

## Silver in the Medallion Flow

```text
Bronze (raw files / raw tables)
          ↓
   Schema Alignment
          ↓
 Conformance / Standardization
          ↓
   Integration (UNION / JOIN)
          ↓
 Cleaning / Dedup / Enrichment
          ↓
        Validation
          ↓
          Silver
          ↓
          Gold
```

---

## What Silver Really Does

```text
Raw systems do not naturally agree.
Silver forces them to agree.
```

---

## Why This Matters

Without Silver:
- joins fail
- KPIs split
- categories fragment
- rows multiply unexpectedly

---

# PART 2 — VISUAL CONFORMANCE DIAGRAM

---

## Same Concept, Different Labels

```text
Source A: NE
Source B: NorthEast
Source C: northeast
            ↓
      conformance rule
            ↓
        northeast
```

---

## Same Boolean, Different Encodings

```text
Source A: yes / no
Source B: Y / N
Source C: 1 / 0
            ↓
      conformance rule
            ↓
         yes / no
```

---

## Key Rule

👉 Canonical domain first, integration second

---

# PART 3 — SCHEMA ALIGNMENT VISUAL

---

## Before Alignment

```text
File A
------
region
charges (DOUBLE)

File B
------
region_name
charges (TEXT)
```

---

## After Alignment

```text
Aligned A
---------
region
charges (DOUBLE)

Aligned B
---------
region
charges (DOUBLE)
```

---

## Insight

👉 You cannot safely UNION before schemas mean the same thing

---

# PART 4 — JOIN RISK VISUAL

---

## Dirty Keys Cause Bad Joins

```text
Customers table:     00123
Transactions table:    123

Result:
no match
```

---

## Conformed Keys

```text
Customers table:     00123
Transactions table:  00123

Result:
match
```

---

## Important Lesson

👉 A join is only as trustworthy as the key standardization behind it

---

# PART 5 — RUNNING INSURANCE CASE

---

## Multi-Year Insurance Data

We have:
- insurance.2021.csv
- insurance.2022.csv
- insurance.2023.csv
- insurance.2024.csv

---

## Real Problems Across Years

- region labels differ
- one year may store charges as text
- one year may contain missing charges
- duplicates may appear after union
- derived columns may not exist consistently

---

## Silver Goal

👉 Produce one integrated, trusted insurance table across all years

---

# PART 6 — END-TO-END SQL PIPELINE (FULL EXAMPLE)

---

## Step 1 — Bronze Tables

Assume raw Bronze tables already exist:

- bronze_insurance_2021
- bronze_insurance_2022
- bronze_insurance_2023
- bronze_insurance_2024

---

## Step 2 — Schema Alignment SQL

```sql
WITH aligned_2021 AS (
    SELECT
        CAST(age AS INTEGER)              AS age,
        LOWER(TRIM(gender))               AS gender,
        CAST(bmi AS DOUBLE)               AS bmi,
        CAST(children AS INTEGER)         AS children,
        LOWER(TRIM(smoker))               AS smoker,
        LOWER(TRIM(region))               AS region_raw,
        CAST(charges AS DOUBLE)           AS charges,
        2021                              AS year
    FROM bronze_insurance_2021
),
aligned_2022 AS (
    SELECT
        CAST(age AS INTEGER)              AS age,
        LOWER(TRIM(gender))               AS gender,
        CAST(bmi AS DOUBLE)               AS bmi,
        CAST(children AS INTEGER)         AS children,
        LOWER(TRIM(smoker))               AS smoker,
        LOWER(TRIM(region_name))          AS region_raw,
        CAST(REPLACE(charges, ',', '') AS DOUBLE) AS charges,
        2022                              AS year
    FROM bronze_insurance_2022
),
aligned_2023 AS (
    SELECT
        CAST(age AS INTEGER)              AS age,
        LOWER(TRIM(gender))               AS gender,
        CAST(bmi AS DOUBLE)               AS bmi,
        CAST(children AS INTEGER)         AS children,
        LOWER(TRIM(smoker))               AS smoker,
        LOWER(TRIM(region))               AS region_raw,
        CAST(charges AS DOUBLE)           AS charges,
        2023                              AS year
    FROM bronze_insurance_2023
),
aligned_2024 AS (
    SELECT
        CAST(age AS INTEGER)              AS age,
        LOWER(TRIM(gender))               AS gender,
        CAST(bmi AS DOUBLE)               AS bmi,
        CAST(children AS INTEGER)         AS children,
        LOWER(TRIM(smoker))               AS smoker,
        LOWER(TRIM(region))               AS region_raw,
        CAST(charges AS DOUBLE)           AS charges,
        2024                              AS year
    FROM bronze_insurance_2024
)
SELECT * FROM aligned_2021
UNION ALL
SELECT * FROM aligned_2022
UNION ALL
SELECT * FROM aligned_2023
UNION ALL
SELECT * FROM aligned_2024;
```

---

## What This Step Does

- aligns column names
- aligns types
- adds year
- prepares the data for conformance

---

# PART 7 — CONFORMANCE SQL

---

## Step 3 — Standardize Domains

```sql
WITH conformed AS (
    SELECT
        age,
        gender,
        bmi,
        children,
        CASE
            WHEN smoker IN ('y', '1') THEN 'yes'
            WHEN smoker IN ('n', '0') THEN 'no'
            ELSE smoker
        END AS smoker_clean,
        CASE
            WHEN region_raw IN ('ne', 'north-east', 'northeast') THEN 'northeast'
            WHEN region_raw IN ('nw', 'north-west', 'northwest') THEN 'northwest'
            WHEN region_raw IN ('se', 'south-east', 'southeast') THEN 'southeast'
            WHEN region_raw IN ('sw', 'south-west', 'southwest') THEN 'southwest'
            ELSE region_raw
        END AS region_clean,
        charges,
        year
    FROM aligned_union
)
SELECT * FROM conformed;
```

---

## What This Step Does

- standardizes smoker values
- standardizes region values
- creates comparable categories across years

---

# PART 8 — CLEANING SQL

---

## Step 4 — NULLs, Outliers, and Deduplication

```sql
WITH cleaned AS (
    SELECT DISTINCT
        age,
        gender,
        bmi,
        children,
        smoker_clean,
        region_clean,
        charges,
        year
    FROM conformed
    WHERE charges IS NOT NULL
      AND charges < 100000
)
SELECT * FROM cleaned;
```

---

## Why This Matters

- removes unusable metric rows
- limits obvious outlier distortion
- removes exact duplicates

---

# PART 9 — ENRICHMENT SQL

---

## Step 5 — Add Business-Friendly Features

```sql
WITH enriched AS (
    SELECT
        age,
        gender,
        bmi,
        children,
        smoker_clean,
        region_clean,
        charges,
        year,
        CASE
            WHEN age < 30 THEN 'young'
            WHEN age < 60 THEN 'adult'
            ELSE 'senior'
        END AS age_group,
        CASE
            WHEN bmi < 18.5 THEN 'underweight'
            WHEN bmi < 25 THEN 'normal'
            WHEN bmi < 30 THEN 'overweight'
            ELSE 'obese'
        END AS bmi_group
    FROM cleaned
)
SELECT * FROM enriched;
```

---

## Why This Matters

Silver is not only about removing bad data.
It is also about adding reusable business features.

---

# PART 10 — VALIDATION SQL

---

## Step 6 — Validation Checks

```sql
SELECT COUNT(*) AS silver_rows
FROM enriched;

SELECT COUNT(*) AS null_charges
FROM enriched
WHERE charges IS NULL;

SELECT region_clean, COUNT(*) AS n
FROM enriched
GROUP BY region_clean
ORDER BY n DESC;

SELECT
  MIN(charges) AS min_c,
  MAX(charges) AS max_c,
  AVG(charges) AS avg_c
FROM enriched;
```

---

## Validation Logic

Check that:
- the table still has expected volume
- the metric is not NULL
- categories collapsed properly
- the distribution is reasonable

---

# PART 11 — FINAL SILVER TABLE

---

## Final Output

```sql
CREATE OR REPLACE TABLE silver_insurance AS
WITH aligned_2021 AS (...),
     aligned_2022 AS (...),
     aligned_2023 AS (...),
     aligned_2024 AS (...),
     aligned_union AS (
         SELECT * FROM aligned_2021
         UNION ALL
         SELECT * FROM aligned_2022
         UNION ALL
         SELECT * FROM aligned_2023
         UNION ALL
         SELECT * FROM aligned_2024
     ),
     conformed AS (
         SELECT
             age,
             gender,
             bmi,
             children,
             CASE
                 WHEN smoker IN ('y', '1') THEN 'yes'
                 WHEN smoker IN ('n', '0') THEN 'no'
                 ELSE smoker
             END AS smoker_clean,
             CASE
                 WHEN region_raw IN ('ne', 'north-east', 'northeast') THEN 'northeast'
                 WHEN region_raw IN ('nw', 'north-west', 'northwest') THEN 'northwest'
                 WHEN region_raw IN ('se', 'south-east', 'southeast') THEN 'southeast'
                 WHEN region_raw IN ('sw', 'south-west', 'southwest') THEN 'southwest'
                 ELSE region_raw
             END AS region_clean,
             charges,
             year
         FROM aligned_union
     ),
     cleaned AS (
         SELECT DISTINCT
             age,
             gender,
             bmi,
             children,
             smoker_clean,
             region_clean,
             charges,
             year
         FROM conformed
         WHERE charges IS NOT NULL
           AND charges < 100000
     )
SELECT
    age,
    gender,
    bmi,
    children,
    smoker_clean AS smoker,
    region_clean AS region,
    charges,
    year,
    CASE
        WHEN age < 30 THEN 'young'
        WHEN age < 60 THEN 'adult'
        ELSE 'senior'
    END AS age_group,
    CASE
        WHEN bmi < 18.5 THEN 'underweight'
        WHEN bmi < 25 THEN 'normal'
        WHEN bmi < 30 THEN 'overweight'
        ELSE 'obese'
    END AS bmi_group
FROM cleaned;
```

---

## Teaching Point

This is not just SQL.

It is:
- schema alignment
- conformance
- cleaning
- integration
- enrichment
- validation

All inside one coherent Silver pipeline.

---

# PART 12 — DISCUSSION SLIDES

---

## Discussion 1

Which step is most dangerous:
- schema alignment
- conformance
- join logic
- validation

Why?

---

## Discussion 2

Would you always remove outliers?

What if the outlier is a real high-cost patient?

---

## Discussion 3

Is a duplicate always an error?

What if the same person legitimately appears in two years?

---

# PART 13 — KPI IMPACT EXAMPLE

---

## Before Conformance

```text
NE          → avg 1200
north-east  → avg 1400
northeast   → avg 1300
```

---

## After Conformance

```text
northeast   → avg 1300
```

---

## Insight

Same data, different pipeline quality, different KPI.

---

# PART 14 — JOIN-SPECIFIC EXAMPLE

---

## Customer / Transaction Integration

```text
customers.customer_id = '00123'
transactions.customer_id = '123'
```

Join result:
❌ no match

---

## After Key Standardization

```text
customers.customer_id = '00123'
transactions.customer_id = '00123'
```

Join result:
✅ correct match

---

## Insight

Key conformance is not optional.
It is fundamental to integration quality.

---

# PART 15 — FINAL VISUAL SUMMARY

---

## Silver Responsibilities

```text
Profile
  + Align
  + Conform
  + Integrate
  + Clean
  + Deduplicate
  + Enrich
  + Validate
  = Trusted Silver Data
```

---

## Final Message

You are not just cleaning data.

You are:

👉 aligning meaning across systems  
👉 protecting KPI correctness  
👉 producing one trusted integrated dataset
