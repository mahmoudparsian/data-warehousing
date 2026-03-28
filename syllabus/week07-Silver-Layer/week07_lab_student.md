# Week 7 Lab — Silver Integration & Conformance (ELITE)

## 🎯 Objective
Build a **multi-source Silver dataset** from 4 yearly insurance files.

You will:
- align schemas
- standardize values (conformance)
- integrate (UNION)
- clean + deduplicate
- enrich
- validate
- explain decisions

---

## 📊 Dataset

Use:
- insurance.2021.csv
- insurance.2022.csv
- insurance.2023.csv
- insurance.2024.csv

Columns (may vary slightly):
age, gender, bmi, children, smoker, region, charges

---

# 🧱 PART A — DATA PROFILING (PER FILE)

For EACH file:

## A1 — Row count
## A2 — NULL analysis (charges)
## A3 — Distinct region values
## A4 — Charges distribution (min/max/avg)

### 🎯 Expectation
- SQL or pandas
- result table
- short explanation

---

# 🔧 PART B — SCHEMA ALIGNMENT

## Task

Ensure ALL files have:
- same column names
- same data types

---

## B1 — Rename columns if needed
(e.g., region_name → region)

## B2 — Cast types
- charges → DOUBLE
- age → INTEGER

---

## 🎯 Expectation
Explain:
- what differences existed
- how you fixed them

---

# 🔁 PART C — CONFORMANCE

## C1 — Region normalization

Map:
- NE, north-east → northeast
- NW → northwest
- etc.

---

## C2 — Smoker normalization

Map:
- Y/N, 1/0 → yes/no

---

## 🎯 Expectation
- show mapping logic
- show before/after counts

---

# 🔗 PART D — INTEGRATION

## D1 — UNION ALL

Combine all 4 datasets

---

## D2 — Add year column

---

## 🎯 Expectation
- combined dataset
- row count per year

---

# 🧹 PART E — CLEANING

## E1 — Remove NULL charges
## E2 — Handle outliers (define threshold)
## E3 — Deduplicate rows

---

## 🎯 Expectation
Explain:
- why threshold chosen
- what defines duplicate

---

# 🧩 PART F — ENRICHMENT

## F1 — Create age_group
## F2 — Create bmi_group (optional)

---

# ✅ PART G — VALIDATION

## G1 — Row counts (before vs after)
## G2 — NULL checks
## G3 — Distinct region values
## G4 — Distribution check (avg charges)

---

# 📊 PART H — KPI IMPACT

Compare:
- Bronze avg charges (combined raw)
- Silver avg charges

👉 Explain difference

---

# 🧠 PART I — REASONING

For EACH step:
- what you did
- why you did it
- what happens if skipped

---

# 📦 DELIVERABLES

- code
- outputs
- explanations

---

# 🔥 KEY MESSAGE

You are building ONE trusted dataset  
from MANY inconsistent sources.
