---
marp: true
theme: default
paginate: true
---

# Week 8 Lab — Instructor Guide

---

# 🧠 Teaching Goal

Students must demonstrate:
- correct grain definition
- proper star schema design
- KPI awareness
- validation discipline

---

# PART A — BUSINESS QUESTIONS

Look for:
- meaningful questions
- mapping to dimensions + measures

---

# PART B — GRAIN

Correct answer (typical):
👉 one row per person per year

Check:
- clear statement
- understanding of impact

---

# PART C — DIMENSIONS

Expected:
- dim_region
- dim_smoker
- dim_time

Check:
- DISTINCT used
- surrogate keys created

---

# PART D — FACT

Check:
- correct joins
- no NULL foreign keys
- correct grain

---

# PART E — DATA MARTS

Expected:
- region summary
- time trend
- smoker analysis

Check:
- correct GROUP BY
- meaningful KPIs

---

# PART F — VALIDATION

Must include:
- row count comparison
- NULL checks
- KPI consistency

---

# PART G — KPI ANALYSIS

Students should recognize:
- modeling affects results
- aggregation depends on grain

---

# PART H — REASONING

Evaluate:
- clarity
- tradeoff awareness
- understanding of risks

---

# COMMON MISTAKES

- wrong grain
- missing dimension keys
- duplicate facts
- no validation
- KPI confusion

---

# FINAL MESSAGE

Gold = business truth layer
