---
marp: true
theme: default
paginate: true
---

# Week 9 Lab — Pipelines + Incremental Processing (Student)

---

# 🎯 Objective

Build a **production-like incremental pipeline** that:
- processes new + updated + late data
- deduplicates correctly
- maintains Silver correctness
- updates Gold and marts
- validates every run

---

# 📊 Dataset

Start from your Week 7 Silver dataset or `insurance.csv`.

You will simulate:
- Day 1 (initial load)
- Day 2 (new rows + updates + late rows)

---

# 🧠 PART A — DEFINE STATE

## A1 — Choose State Strategy
Pick ONE:
- last_run_time
- watermark (recommended)

Write:
- what you store
- why

---

# 🧪 PART B — SIMULATE DAY 1

## B1 — Initial Load
- load full dataset into Bronze
- build Silver (clean + dedup)
- build Gold (fact + dimensions)
- build 1 mart

## Deliverable
- SQL / code
- outputs

---

# 🔁 PART C — SIMULATE DAY 2 (CRITICAL)

Create:
- 10 new rows
- 5 updated rows
- 3 late rows (timestamp BEFORE last_run)

---

## C1 — Incremental Filter

Implement:
- naive filter
- sliding window filter

Compare results

---

# 🧹 PART D — DEDUPLICATION

## D1 — Implement Dedup

Use:
ROW_NUMBER() OVER (PARTITION BY business_key ORDER BY updated_at DESC)

---

## D2 — Explain

- what is your business key?
- why keep latest?

---

# 🔄 PART E — UPSERT / MERGE

## E1 — Apply Upsert

- update existing rows
- insert new rows

---

## E2 — Show Failure

Run merge WITHOUT dedup

Explain:
- what goes wrong?

---

# 🏗 PART F — INCREMENTAL SILVER

Pipeline steps:
1. incremental extract
2. clean
3. dedup
4. merge

---

## Deliverable
- SQL pipeline (modular)
- explanation of each step

---

# 📊 PART G — INCREMENTAL GOLD

## G1 — Choose Strategy

Pick one:
- full rebuild
- partition rebuild
- incremental update

---

## G2 — Justify

Explain tradeoffs:
- correctness
- performance

---

# 📈 PART H — DATA MART UPDATE

Update one mart:
- region summary OR smoker summary

Show:
- before vs after Day 2

---

# ✅ PART I — VALIDATION

## I1 — Checks

- row count change
- duplicates
- NULL keys
- KPI consistency

---

## I2 — Compare

- Silver SUM(charges)
- Gold SUM(charges)

---

# ⚠️ PART J — FAILURE SIMULATION

## J1 — Remove Sliding Window

Show:
- missed late data

---

## J2 — Remove Dedup

Show:
- duplicate inflation

---

## J3 — KPI Drift

Show how KPI changes incorrectly

---

# 🧠 PART K — DESIGN REFLECTION

Answer:

1. What is hardest part of incremental pipelines?
2. How do you prevent silent errors?
3. When would you rebuild everything?

---

# 📦 FINAL DELIVERABLES

- SQL / notebook
- outputs
- explanations
- failure analysis

---

# 🔥 FINAL MESSAGE

Pipelines are not about running once.

They are about staying correct forever.
