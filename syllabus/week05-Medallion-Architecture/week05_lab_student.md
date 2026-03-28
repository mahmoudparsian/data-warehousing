# Week 5 Lab — Medallion Architecture Mapping (ELITE)

## 🎯 Objective
Bridge **Traditional DW → Medallion Architecture** using your Week 4 pipeline.

You will:
- map ETL steps to **Bronze / Silver / Gold**
- justify **where each transformation belongs**
- redesign a pipeline using Medallion
- identify **bad layer placement**

---

## 📊 Context (From Week 4)

You built:
- Extract: multi-year insurance files
- Transform: cleaning (region, nulls, outliers, age_group)
- Load: star schema (fact + dimensions)
- OLAP: queries

---

# 🧠 PART A — PIPELINE MAPPING

## A1 — Identify Bronze
**Task**
List ALL data that belongs in Bronze.

**Expectation**
- raw files
- no cleaning
- explain WHY

---

## A2 — Identify Silver
**Task**
List ALL transformations that belong in Silver.

Include:
- region standardization
- null handling
- outlier handling
- derived columns

**Expectation**
Explain WHY each belongs in Silver (not Bronze/Gold).

---

## A3 — Identify Gold
**Task**
List ALL Gold layer objects.

Include:
- fact table
- dimension tables
- aggregates

**Expectation**
Explain WHY Gold is business-ready.

---

# 🔍 PART B — TRANSFORMATION JUSTIFICATION (CRITICAL)

For EACH transformation below:
- state the correct layer
- justify decision

## B1 — Remove NULL charges  
## B2 — Standardize region values  
## B3 — Create age_group  
## B4 — Compute revenue by region  
## B5 — Deduplicate records  

---

# 🔁 PART C — RE-DESIGN PIPELINE

## C1 — Traditional Pipeline

Write your Week 4 pipeline:

Raw → ETL → Star Schema

---

## C2 — Medallion Version

Rewrite as:

Raw → Bronze → Silver → Gold

---

## C3 — Detailed Flow

Provide step-by-step mapping:

- what happens in Bronze
- what happens in Silver
- what happens in Gold

---

# 🧪 PART D — ERROR ANALYSIS

## Scenario

Dashboard shows incorrect result:
“Region West has lowest cost”

---

## Task

1. Where do you check first? (Gold/Silver/Bronze)
2. What could be wrong in Silver?
3. What could be wrong in Bronze?
4. How do you fix it?

---

# ⚠️ PART E — BAD DESIGN IDENTIFICATION

For each case, identify the mistake:

## E1
Cleaning data in Bronze

## E2
Building aggregates in Silver

## E3
Skipping Silver layer

## E4
Putting raw data directly into Gold

---

# 📊 PART F — MULTI-USE THINKING

Map use cases to layers:

| Use Case | Layer |
|----------|------|
| auditing raw data | ? |
| machine learning features | ? |
| executive dashboard | ? |

Explain each choice.

---

# 📦 DELIVERABLES

For EACH section:
- answer
- explanation (2–4 sentences)
- diagrams optional

---

# 📏 GRADING

- Correct mapping: 30%
- Reasoning quality: 40%
- Architecture clarity: 20%
- Completeness: 10%

---

# 🔥 KEY MESSAGE

You are not transforming data.

You are designing a **data platform**.
