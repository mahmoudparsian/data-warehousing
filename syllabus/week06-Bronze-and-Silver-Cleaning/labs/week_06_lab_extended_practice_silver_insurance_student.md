# Week 6 — Extended Practice (optional)
## Silver Transformations on the Insurance Data

> Practice the Session 2 Silver ideas on the insurance data the slides use: week 1's [`insurance.csv`](../../week01-Foundations-SQL-for-Analytics/example_1_insurance/insurance.csv)
> or week 2's yearly files in [`EDA/data/`](../../week02-SQL-Analytical-Thinking-and-EDA/EDA/data/). The demo notebook is [`../week06_notebook.py`](../week06_notebook.py).

## 🎯 Objective
Build a **robust Silver pipeline** from messy Bronze data.

You will:
- profile data
- apply transformations (clean, standardize, deduplicate, enrich)
- validate results
- explain business impact

---

## 📊 Dataset
Use: insurance.csv (or your multi-year dataset)

Columns:
age, gender, bmi, children, smoker, region, charges

---

# 🧱 PART A — DATA PROFILING (MANDATORY FIRST STEP)

## A1 — Row Count
Write SQL to count total rows.

## A2 — NULL Analysis
Count NULLs per column.

## A3 — Category Exploration
List distinct values of:
- region
- smoker

## A4 — Outlier Detection
Find:
- min(charges)
- max(charges)
- avg(charges)

### 🎯 Expectation
For each:
- SQL query
- result table
- 2–3 sentence interpretation

---

# 🔧 PART B — CLEANING DECISIONS

## B1 — NULL Handling (charges)
Choose ONE:
- remove rows
- impute values
- flag

👉 Explain WHY

---

## B2 — Region Standardization
Fix inconsistent values:
- NE
- north-east
- northeast

👉 Output a clean column

---

## B3 — Outlier Handling
Define threshold (e.g., charges < 100000)

👉 Explain your threshold choice

---

## B4 — Deduplication
Identify duplicates and remove them.

👉 Define what “duplicate” means

---

# 🧩 PART C — ENRICHMENT

## C1 — Create age_group

Rules:
- <30 → young
- 30–59 → adult
- 60+ → senior

---

## C2 — Optional Enrichment
Create ONE additional feature:
(e.g., bmi_group, charge_band)

---

# ✅ PART D — VALIDATION (CRITICAL)

## D1 — Row Count Before vs After
Show difference

## D2 — NULL Check
Ensure charges has no NULLs (if removed)

## D3 — Distinct Region Values
Show cleaned categories

## D4 — Distribution Check
Compare avg charges before vs after cleaning

---

# 📊 PART E — KPI IMPACT ANALYSIS

## Task
Compare:

1. AVG(charges) in Bronze  
2. AVG(charges) in Silver  

👉 Explain difference

---

# 🧠 PART F — REASONING

For EACH transformation:
- what you did
- why you did it
- what happens if you did NOT do it

---

# 📦 DELIVERABLES

For EACH part:
- SQL or code
- output
- explanation (2–4 sentences)

---

# 📏 GRADING

- Profiling quality: 20%
- Transformations: 30%
- Validation: 20%
- Reasoning: 30%

---

# 🔥 KEY MESSAGE

You are not cleaning data.

You are defining **trusted data**.
