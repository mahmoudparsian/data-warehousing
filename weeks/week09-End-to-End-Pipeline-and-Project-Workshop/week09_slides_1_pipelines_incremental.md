---
marp: true
theme: default
paginate: true
size: 16:9
---

# Week 9  
## Pipelines + Incremental Processing (Elite v7 — SYSTEM + FAILURE + DESIGN MASTER)

---

# PART 0 — WHAT BREAKS FIRST?

---

## Reality in Production

Pipelines do NOT fail like this:
❌ error → stop  

They fail like this:
✅ run successfully  
❌ produce WRONG data  

---

## Core Insight

👉 The biggest risk is **silent incorrectness**

---

# PART 1 — THINKING IN TIME (CRITICAL SHIFT)

---

## Static World (Student Thinking)

Data is fixed  
Query once → done  

---

## Dynamic World (Production)

Data is changing  
Pipeline runs repeatedly  

---

## Timeline Example

Day 1 → correct  
Day 10 → slightly wrong  
Day 50 → completely wrong  

---

## Insight

👉 correctness must be preserved **over time**

---

# PART 2 — WHAT IS “INCREMENTAL STATE”?

---

## State = Memory of Pipeline

- last_run_time  
- watermark  
- processed IDs  

---

## Example

```text
last_run = 2024-01-01 02:00
```

---

## Problem

If state is wrong:
- data skipped  
- duplicates created  

---

## Insight

👉 state errors = systemic corruption

---

# PART 3 — WATERMARK VS LAST_RUN (IMPORTANT)

---

## Common Mistake

```sql
WHERE updated_at > last_run
```

---

## Problem

Late data missed forever  

---

## Watermark

Safe boundary (delayed)

---

## Better Logic

```sql
WHERE updated_at > watermark
```

---

## Insight

👉 watermark introduces safety margin

---

# PART 4 — LATE DATA (MULTI-CASE)

---

## Case 1 — Slight Delay

Handled by sliding window  

---

## Case 2 — Large Delay

Needs backfill  

---

## Case 3 — Missing Timestamp

Needs fallback strategy  

---

## Insight

👉 late data is inevitable

---

# PART 5 — SLIDING WINDOW DESIGN

---

## Example

```sql
WHERE updated_at > last_run - INTERVAL '2 days'
```

---

## Design Question

How large should window be?

---

## Tradeoff

| Window | Effect |
|--------|-------|
| small | miss data |
| large | more compute |

---

## Insight

👉 no perfect window size

---

# PART 6 — DEDUP IS A BUSINESS DECISION

---

## Not Just Technical

You must define:

- what is duplicate?
- which record wins?

---

## Example

| id | status | updated_at |
|----|--------|------------|
| 1  | active | 10:00 |
| 1  | inactive | 11:00 |

---

## Decision

Keep latest OR keep first?

---

## Insight

👉 dedup = business rule

---

# PART 7 — MULTI-UPDATE PROBLEM

---

## Scenario

Same record updated multiple times in batch  

---

## Example

| id | updated_at |
|----|------------|
| 1  | 10:00 |
| 1  | 10:05 |
| 1  | 10:10 |

---

## Required Logic

Keep latest only  

---

## Insight

👉 ordering matters

---

# PART 8 — INCREMENTAL SILVER (FULL DESIGN)

---

## Pipeline

```text
Bronze
 ↓ incremental filter
 ↓ cleaning
 ↓ normalization
 ↓ deduplication
 ↓ merge
Silver
```

---

## Failure Case

Skip dedup → duplicates propagate  

---

## Insight

👉 Silver = correctness boundary

---

# PART 9 — INCREMENTAL GOLD (NUMERICAL EXAMPLE)

---

## Original Data

100, 200, 300 → avg = 200  

---

## Update One Row

100 → 1000  

New avg = 500  

---

## Problem

Need to recompute ALL aggregates  

---

## Insight

👉 Gold is globally sensitive

---

# PART 10 — PARTITION REBUILD (STRONG EXAMPLE)

---

## Scenario

Data partitioned by year  

---

## Update affects 2024 only  

---

## SQL

```sql
DELETE FROM fact WHERE year = 2024;

INSERT INTO fact
SELECT ...
FROM silver
WHERE year = 2024;
```

---

## Insight

👉 isolate recomputation

---

# PART 11 — KPI DRIFT (DEEP CASE)

---

## Pipeline Change

small logic tweak  

---

## KPI Evolution

200 → 205 → 210 → 230  

---

## Problem

No alert triggered  

---

## Insight

👉 drift is slow corruption

---

# PART 12 — VALIDATION DESIGN (NOT OPTIONAL)

---

## Basic Checks

- row count  
- nulls  
- duplicates  

---

## Advanced Checks

- distribution shift  
- KPI thresholds  
- anomaly detection  

---

## Insight

👉 validation must evolve with pipeline

---

# PART 13 — DISTRIBUTION CHECK (IMPORTANT)

---

## Example

charges distribution shifts suddenly  

---

## SQL Idea

```sql
SELECT MIN, MAX, AVG, STDDEV
```

---

## Insight

👉 not just counts — check shape of data

---

# PART 14 — ANOMALY DETECTION

---

## Examples

- sudden spike in revenue  
- sudden drop in rows  

---

## Approach

- thresholds  
- historical comparison  

---

## Insight

👉 pipelines must detect abnormal patterns

---

# PART 15 — OBSERVABILITY (DEEPER)

---

## Track Over Time

- rows per run  
- runtime trend  
- failure rate  

---

## Example

| day | rows | runtime |
|-----|------|--------|

---

## Insight

👉 trends reveal hidden issues

---

# PART 16 — FAILURE PROPAGATION (CASE)

---

## Scenario

Silver duplicates  

---

## Result

Gold inflated  

---

## Result

Dashboard wrong  

---

## Insight

👉 upstream errors cascade

---

# PART 17 — TESTING STRATEGY (REAL)

---

## Test Types

- data tests  
- logic tests  
- regression tests  

---

## Example

```sql
ASSERT COUNT(*) > 0
ASSERT COUNT(*) = COUNT(DISTINCT id)
```

---

## Insight

👉 test data behavior, not just code

---

# PART 18 — PERFORMANCE VS CORRECTNESS

---

## Tradeoff

| Choice | Effect |
|--------|--------|
| fast pipeline | risk errors |
| safe pipeline | slower |

---

## Insight

👉 correctness > speed

---

# PART 19 — FULL PIPELINE WALKTHROUGH

---

## Day 1

100 rows  

---

## Day 2

+10 new  
+5 updates  
+3 late  

---

## Correct Pipeline

- sliding window  
- dedup  
- merge  
- validate  

---

## Wrong Pipeline

- append only  
→ duplicates + missing  

---

# PART 20 — FINAL SYSTEM VIEW

---

```text
State + Time + Logic + Validation + Monitoring
```

---

# FINAL MESSAGE

---

You are not writing SQL.

You are:

👉 managing evolving data  
👉 preserving correctness over time  
👉 preventing silent failures  
👉 building trusted systems  

---

## FINAL TRUTH

Correct once ≠ correct forever
