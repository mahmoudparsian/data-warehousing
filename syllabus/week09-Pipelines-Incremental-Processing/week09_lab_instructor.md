---
marp: true
theme: default
paginate: true
---

# Week 9 Lab — Instructor Guide (Elite)

---

# 🎯 Evaluation Goals

Students must demonstrate:
- correct incremental logic
- proper deduplication
- understanding of late data
- awareness of failure modes
- validation discipline

---

# PART A — STATE

Expected:
- watermark preferred
- explanation of late data handling

---

# PART B — DAY 1

Check:
- clean Silver
- correct Gold schema
- valid mart

---

# PART C — DAY 2

Students must:
- simulate new, updated, late rows
- show naive vs correct logic

---

# PART D — DEDUP

Correct:
ROW_NUMBER() with business key

Look for:
- correct partition
- correct ordering

---

# PART E — UPSERT

Check:
- dedup BEFORE merge
- explanation of duplicate issue

---

# PART F — SILVER PIPELINE

Expected steps:
- incremental filter
- clean
- dedup
- merge

Must be modular

---

# PART G — GOLD STRATEGY

Good answers:
- partition rebuild (balanced)
- clear tradeoff explanation

---

# PART H — MART UPDATE

Check:
- correct aggregation
- meaningful interpretation

---

# PART I — VALIDATION

Must include:
- row counts
- duplicate checks
- KPI consistency

---

# PART J — FAILURE SIMULATION

Critical section

Students should show:
- missed late data
- duplicate inflation
- KPI drift

---

# PART K — REFLECTION

Strong answers:
- incremental complexity > modeling
- silent failure awareness
- need for monitoring

---

# COMMON MISTAKES

- no sliding window
- no dedup
- wrong business key
- no validation
- ignoring late data

---

# GRADING RUBRIC

| Area | Weight |
|------|-------|
| Incremental logic | 25% |
| Dedup correctness | 20% |
| Gold update strategy | 15% |
| Validation | 20% |
| Failure analysis | 20% |

---

# FINAL MESSAGE

A correct pipeline once is easy.

A correct pipeline every day is hard.
