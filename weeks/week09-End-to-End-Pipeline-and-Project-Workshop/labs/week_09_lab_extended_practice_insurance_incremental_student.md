# Week 9 — Extended Practice (optional): Incremental Processing with Updates (Insurance)

> Adds what the pizza labs don't cover: **updated** records (upserts), a look-back window for late updates, and partition rebuilds.
> Worked example of the same patterns (try first, then compare): [slides 1](../lecture_notes_01_incremental_pipelines.md) and
> [`../notebook_01_incremental_pipeline.py`](../notebook_01_incremental_pipeline.py). DuckDB CLI or a notebook, run from this `labs/` folder.

## 🎯 Objective

Run an insurer's customer **change feed** through an incremental Silver table and a Gold mart, three runs in a row, choose a look-back window that
really catches the late rows, and prove that the result equals a full rebuild.

## ⚙️ Setup: the change feed

Each row is a **version** of a customer: `updated_at` = when it changed, `arrived_at` = when the pipeline can see it.
The pipeline runs at **midnight UTC** on Jan 2, Jan 3 and Jan 4, 2024, and sees only rows with `arrived_at <=` the run time.

```sql
SET TimeZone = 'UTC';
CREATE OR REPLACE TABLE src AS
SELECT ROW_NUMBER() OVER (ORDER BY age, gender, bmi, children, smoker, region, charges) AS customer_id,
       age, smoker, region, CAST(charges AS DECIMAL(10, 2)) AS charges
FROM read_csv('../../week07-Silver-Layer-Cleaning-and-Conforming/data/insurance.2023.csv', types = {'smoker': 'VARCHAR'});

CREATE OR REPLACE TABLE changes AS
SELECT customer_id, region, smoker, charges, TIMESTAMP '2024-01-01 09:00' AS updated_at, TIMESTAMP '2024-01-01 09:05' AS arrived_at
FROM src WHERE customer_id <= 1250                                                                   -- day 1
UNION ALL SELECT customer_id, region, smoker, charges, TIMESTAMP '2024-01-02 14:00', TIMESTAMP '2024-01-02 14:02'
FROM src WHERE customer_id > 1250                                                                    -- new customers
UNION ALL SELECT customer_id, region, smoker, ROUND(charges * 1.08, 2), TIMESTAMP '2024-01-02 15:00', TIMESTAMP '2024-01-02 15:01'
FROM src WHERE customer_id <= 1250 AND customer_id % 60 = 0                                          -- updates
UNION ALL SELECT customer_id, region, smoker, ROUND(charges * f, 2), TIMESTAMP '2024-01-02 16:00' + INTERVAL (f * 10) MINUTE, TIMESTAMP '2024-01-02 18:00'
FROM src, (VALUES (1.02), (1.04)) t(f) WHERE customer_id <= 1250 AND customer_id % 125 = 7           -- two updates in one batch
UNION ALL SELECT customer_id, CASE region WHEN 'southeast' THEN 'southwest' ELSE 'southeast' END, smoker, charges,
                 TIMESTAMP '2024-01-01 20:00', TIMESTAMP '2024-01-03 02:00'
FROM src WHERE customer_id <= 1250 AND customer_id % 80 = 11;                                        -- late: moved on Jan 1, arrived 30 hours later
```

---

## Part A — State and lateness

**A1.** Create `ops.run_log (run_id, run_at, read_from, versions_read, rows_changed)` and `silver.customers` (one row per customer, `customer_id`
primary key, `region`, `smoker`, `charges`, `updated_at`, `_run_id`).
**A2.** Measure the delays: per kind of change, the maximum `arrived_at - updated_at`. (Group by `arrived_at`.) What is the latest arrival?

## Part B — Run 1 (Jan 2, 00:00)

**B1.** Load everything visible: keep the latest version per customer, insert it, log the run. Rows in Silver?

## Part C — Runs 2 and 3: which filter?

**C1.** Run 2 (Jan 3, 00:00) and run 3 (Jan 4, 00:00), three times, on three copies of Silver, with three filters:
`updated_at > last run` · `updated_at > last run - 1 day` · `updated_at > last run - 2 days`. Use an idempotent `MERGE` (update only if newer).
**C2.** For each filter: versions read and rows changed per run. 🔮 Predict first: does a 1-day look-back catch the late rows?
✍️ Use A2 to explain the result. How would you choose the window in production?

## Part D — Idempotency and dedup

**D1.** Run run 3 once more with the same settings: rows changed? **D2.** 🐞 Remove the in-batch dedup (merge all versions of a run): what happens
with the customers updated twice in one batch?

## Part E — Gold: touched partitions

**E1.** `gold.mart_region` (region, customers, total_charges) from the 2-day pipeline after run 2. **E2.** After run 3: which regions changed?
Rebuild only those, and check that the mart equals Silver.

## Part F — The proof

**F1.** Full rebuild = the latest version of every customer from all rows arrived by Jan 4. Compare each pipeline with it (`EXCEPT` both ways).

---

## ✅ Deliverables

SQL and results for every part, and 4–6 sentences: which filter you would ship, how you chose the window, and the one test you would run after every load.
