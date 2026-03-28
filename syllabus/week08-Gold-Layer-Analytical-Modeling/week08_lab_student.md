---
marp: true
theme: default
paginate: true
---

# Week 8 Lab — Gold Modeling (Student Version)

---

# 🎯 Objective

Build a **Gold Layer (Star Schema + Data Marts)** from a Silver dataset.

You will:
- define grain
- design fact + dimensions
- build Gold tables
- create data marts
- validate KPIs
- justify decisions

---

# 📊 Dataset

Use your **Silver dataset from Week 7**:
`silver_insurance`

Columns:
- age
- region
- smoker
- charges
- year
- (optional) age_group, bmi_group

---

# 🧠 PART A — BUSINESS THINKING FIRST

## A1 — Define Business Questions

Write at least 3:

Example:
- avg charges by region
- smoker vs non-smoker cost
- trend over time

---

## 🎯 Expectation

For each:
- question
- required dimensions
- required measure

---

# 🧱 PART B — DEFINE GRAIN (CRITICAL)

## B1 — Define Grain

Write clearly:

👉 “One row represents ______”

---

## B2 — Justify

Explain:
- why this grain
- what happens if wrong

---

# 🧩 PART C — DESIGN DIMENSIONS

## C1 — Choose Dimensions (at least 3)

Example:
- region
- smoker
- time

---

## C2 — Create Dimension Tables

Each must:
- remove duplicates
- include surrogate key

---

## 🎯 Deliverable

Table schema + SQL

---

# 📦 PART D — BUILD FACT TABLE

## D1 — Create Fact Table

Include:
- foreign keys
- measures (charges)

---

## D2 — Join with Dimensions

Ensure:
- no NULL foreign keys

---

## 🎯 Deliverable

SQL + explanation

---

# 📊 PART E — BUILD DATA MARTS

## E1 — Create 2 Data Marts

Examples:
- avg charges by region
- avg charges by year
- smoker analysis

---

## E2 — Write SQL

---

## 🎯 Deliverable

- SQL
- output
- interpretation

---

# ✅ PART F — VALIDATION

## F1 — Check Fact Table

- row count
- NULL keys

---

## F2 — Check KPI Consistency

Compare:

- SUM(charges) in Silver  
- SUM(charges) in Fact  

---

## F3 — Check Dimensions

- uniqueness
- completeness

---

# 📊 PART G — KPI ANALYSIS

Compare:

- KPI from Silver  
- KPI from Gold  

Explain differences

---

# 🧠 PART H — REASONING

For EACH step:

- what you did  
- why you did it  
- what breaks if skipped  

---

# 📦 DELIVERABLES

- SQL
- outputs
- explanations

---

# 🔥 FINAL MESSAGE

Gold is not about tables.

It is about:
👉 defining business truth
