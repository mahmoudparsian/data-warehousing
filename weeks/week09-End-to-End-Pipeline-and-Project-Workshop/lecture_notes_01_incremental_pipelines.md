---
marp: true
theme: default
paginate: true
size: 16:9
title: Week 9 — Session 1 — Pipelines and Incremental Processing
---

# Week 9
## Pipelines Over Time: Incremental Processing

Running example: an insurer's **customer change feed** (1,300 customers from week 7's clean 2024 file). Every query runs, in order.
**Labs 9.1–9.2** do the same with the pizza shop's monthly delivery files. DuckDB patterns: [slides 2](lecture_notes_02_incremental_in_duckdb.md).

---

# PART 0 — What Breaks First?

| Pipelines rarely fail like this | They fail like this |
|---|---|
| ❌ error → stop → someone fixes it | ✅ the run succeeds · ❌ the data is **wrong** · nobody notices |

👉 The biggest risk of a pipeline that runs every day is **silent incorrectness**: a few rows skipped or counted twice per run.

---

# PART 1 — Thinking in Time: the Change Feed

The source system sends **versions** of customers: every change has an `updated_at` (when it happened) and an `arrived_at` (when we can see it).

```sql
SET TimeZone = 'UTC';
CREATE OR REPLACE TABLE src AS
SELECT ROW_NUMBER() OVER (ORDER BY age, gender, bmi, children, smoker, region, charges) AS customer_id,   -- a stable id
       age, smoker, region, CAST(charges AS DECIMAL(10, 2)) AS charges
FROM read_csv('../week07-Silver-Layer-Cleaning-and-Conforming/data/insurance.2024.csv', types = {'smoker': 'VARCHAR'});  -- else yes/no → BOOLEAN

CREATE OR REPLACE TABLE changes AS
SELECT customer_id, region, smoker, charges, TIMESTAMP '2024-01-01 09:00' AS updated_at, TIMESTAMP '2024-01-01 09:05' AS arrived_at, 'day 1' AS kind
FROM src WHERE customer_id <= 1200
UNION ALL SELECT customer_id, region, smoker, charges, TIMESTAMP '2024-01-02 09:00', TIMESTAMP '2024-01-02 09:05', 'new customer'
FROM src WHERE customer_id > 1200
UNION ALL SELECT customer_id, region, smoker, ROUND(charges * 1.10, 2), TIMESTAMP '2024-01-02 10:00', TIMESTAMP '2024-01-02 10:01', 'update'
FROM src WHERE customer_id <= 1200 AND customer_id % 100 = 0
UNION ALL SELECT customer_id, region, smoker, ROUND(charges * 1.05, 2), TIMESTAMP '2024-01-02 11:00', TIMESTAMP '2024-01-02 11:01', 'update twice (1st)'
FROM src WHERE customer_id <= 1200 AND customer_id % 100 = 50
UNION ALL SELECT customer_id, region, smoker, ROUND(charges * 1.20, 2), TIMESTAMP '2024-01-02 12:00', TIMESTAMP '2024-01-02 12:01', 'update twice (2nd)'
FROM src WHERE customer_id <= 1200 AND customer_id % 100 = 50
UNION ALL SELECT customer_id, region, 'yes', ROUND(charges * 1.50, 2), TIMESTAMP '2024-01-01 23:00', TIMESTAMP '2024-01-02 08:00', 'late (smoker since Jan 1)'
FROM src WHERE customer_id <= 1200 AND customer_id % 100 = 25;

SELECT kind, COUNT(*) AS versions, MIN(updated_at) AS updated_at, MIN(arrived_at) AS arrived_at
FROM changes GROUP BY 1 ORDER BY MIN(arrived_at);
```

<!-- RESULT -->

| kind                      | versions | updated_at          | arrived_at          |
|---------------------------|---------:|---------------------|---------------------|
| day 1                     |     1200 | 2024-01-01 09:00:00 | 2024-01-01 09:05:00 |
| late (smoker since Jan 1) |       12 | 2024-01-01 23:00:00 | 2024-01-02 08:00:00 |
| new customer              |      100 | 2024-01-02 09:00:00 | 2024-01-02 09:05:00 |
| update                    |       12 | 2024-01-02 10:00:00 | 2024-01-02 10:01:00 |
| update twice (1st)        |       12 | 2024-01-02 11:00:00 | 2024-01-02 11:01:00 |
| update twice (2nd)        |       12 | 2024-01-02 12:00:00 | 2024-01-02 12:01:00 |

*(6 rows)*

<!-- /RESULT -->

---

# PART 2 — Incremental State: the Pipeline's Memory

```sql
CREATE SCHEMA IF NOT EXISTS ops;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE OR REPLACE TABLE ops.run_log (run_id INT, run_at TIMESTAMP, read_from TIMESTAMP, rows_read BIGINT, rows_changed BIGINT);
CREATE OR REPLACE TABLE silver.customers (customer_id INT PRIMARY KEY, region VARCHAR, smoker VARCHAR,
                                         charges DECIMAL(10, 2), updated_at TIMESTAMP, _run_id INT);

-- what the source shows at a given moment: only what has ARRIVED
CREATE OR REPLACE MACRO visible_at(t) AS TABLE SELECT * EXCLUDE (arrived_at, kind) FROM changes WHERE arrived_at <= t;
SELECT COUNT(*) AS visible_at_run_1 FROM visible_at(TIMESTAMP '2024-01-02 00:00');
```

<!-- RESULT -->

| visible_at_run_1 |
|-----------------:|
|             1200 |

*(1 row)*

<!-- /RESULT -->

State = what the pipeline remembers between runs: the **last run time** (or a watermark), the **load log**, and the lineage on every row (`_run_id`).
Wrong state → rows skipped or loaded twice, silently.

---

# PART 3 — `last_run` vs a Watermark with a Look-Back

Run 1 (Jan 2, 00:00) loads everything. Run 2 (Jan 3, 00:00), **naive**: `WHERE updated_at > last_run`.

```sql
SELECT 'naive: updated_at > last run (Jan 2 00:00)' AS filter_used, COUNT(*) AS versions_read,
       COUNT(*) FILTER (WHERE updated_at < TIMESTAMP '2024-01-02 00:00') AS late_versions_read
FROM visible_at(TIMESTAMP '2024-01-03 00:00') WHERE updated_at > TIMESTAMP '2024-01-02 00:00'
UNION ALL
SELECT 'look-back: updated_at > last run - 1 day', COUNT(*), COUNT(*) FILTER (WHERE updated_at < TIMESTAMP '2024-01-02 00:00')
FROM visible_at(TIMESTAMP '2024-01-03 00:00') WHERE updated_at > TIMESTAMP '2024-01-02 00:00' - INTERVAL 1 DAY;
```

<!-- RESULT -->

| filter_used                                | versions_read | late_versions_read |
|--------------------------------------------|--------------:|-------------------:|
| naive: updated_at > last run (Jan 2 00:00) |           136 |                  0 |
| look-back: updated_at > last run - 1 day   |          1348 |               1212 |

*(2 rows)*

<!-- /RESULT -->

The 12 late versions happened **before** run 1 but **arrived after** it: the naive filter never reads them, **forever**.
The look-back reads them, and re-reads 1,200 versions it already has: safe **only** if loading the same version twice changes nothing (Part 8).

---

# PART 4 — Late Data: How Late Is Late?

```sql
SELECT kind, MAX(arrived_at - updated_at) AS max_delay FROM changes GROUP BY 1 ORDER BY 2 DESC;
```

<!-- RESULT -->

| kind                      | max_delay |
|---------------------------|-----------|
| late (smoker since Jan 1) | 9:00:00   |
| day 1                     | 0:05:00   |
| new customer              | 0:05:00   |
| update                    | 0:01:00   |
| update twice (1st)        | 0:01:00   |
| update twice (2nd)        | 0:01:00   |

*(6 rows)*

<!-- /RESULT -->

| Delay | Handling |
|---|---|
| minutes to hours | look-back window (Part 5) |
| days to months | a backfill run for that period, then rebuild its partitions (Part 10) |
| no timestamp at all | load by **file** (load log, slides 2), not by time |

Measure the delays you really have (here 9 hours), then choose the window.

---

# PART 5 — Choosing the Look-Back Window

| Window | Effect |
|---|---|
| too small (1 hour) | late rows skipped silently |
| right (1 day here) | every late row read; some rows read twice |
| too large (30 days) | correct, but every run re-reads a month |

👉 A look-back window **requires** an idempotent load: re-reading must never add a row.

---

# PART 6 — Deduplication Is a Business Decision

Several versions of one customer arrive in the same run. Which one wins?

```sql
SELECT customer_id, charges, updated_at FROM changes WHERE customer_id = 50 ORDER BY updated_at;
```

<!-- RESULT -->

| customer_id | charges | updated_at          |
|------------:|--------:|---------------------|
|          50 |  200.00 | 2024-01-01 09:00:00 |
|          50 |  210.00 | 2024-01-02 11:00:00 |
|          50 |  240.00 | 2024-01-02 12:00:00 |

*(3 rows)*

<!-- /RESULT -->

Rule here: **the latest `updated_at` wins** (a tie would need a second rule, e.g. the latest `arrived_at`). Another business might keep the first
version (a signed contract) or keep all of them (history, a type-2 dimension).

---

# PART 7 — Many Updates in One Batch

```sql
CREATE OR REPLACE MACRO latest_versions(t, since) AS TABLE
SELECT * FROM visible_at(t) WHERE updated_at > since
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) = 1;

SELECT COUNT(*) AS versions_read,
       (SELECT COUNT(*) FROM latest_versions(TIMESTAMP '2024-01-03 00:00', TIMESTAMP '2024-01-01 00:00')) AS customers_after_dedup
FROM visible_at(TIMESTAMP '2024-01-03 00:00') WHERE updated_at > TIMESTAMP '2024-01-01 00:00';
```

<!-- RESULT -->

| versions_read | customers_after_dedup |
|--------------:|----------------------:|
|          1348 |                  1300 |

*(1 row)*

<!-- /RESULT -->

Deduplicate **inside the batch** first (one row per customer), **then** merge: merging two versions of the same key in one statement is an error
or, worse, depends on the row order.

---

# PART 8 — Incremental Silver: an Idempotent MERGE

```sql
MERGE INTO silver.customers AS t
USING (SELECT *, 1 AS _run_id FROM latest_versions(TIMESTAMP '2024-01-02 00:00', TIMESTAMP '1900-01-01')) AS s
ON t.customer_id = s.customer_id
WHEN MATCHED AND s.updated_at > t.updated_at THEN UPDATE SET region = s.region, smoker = s.smoker, charges = s.charges,
                                                       updated_at = s.updated_at, _run_id = s._run_id
WHEN NOT MATCHED THEN INSERT VALUES (s.customer_id, s.region, s.smoker, s.charges, s.updated_at, s._run_id);

SELECT COUNT(*) AS silver_rows_after_run_1, MAX(updated_at) AS newest_version FROM silver.customers;
```

<!-- RESULT -->

| silver_rows_after_run_1 | newest_version      |
|------------------------:|---------------------|
|                    1200 | 2024-01-01 09:00:00 |

*(1 row)*

<!-- /RESULT -->

```sql
MERGE INTO silver.customers AS t
USING (SELECT *, 2 AS _run_id FROM latest_versions(TIMESTAMP '2024-01-03 00:00', TIMESTAMP '2024-01-01 00:00')) AS s   -- look-back: last run - 1 day
ON t.customer_id = s.customer_id
WHEN MATCHED AND s.updated_at > t.updated_at THEN UPDATE SET region = s.region, smoker = s.smoker, charges = s.charges,
                                                       updated_at = s.updated_at, _run_id = s._run_id
WHEN NOT MATCHED THEN INSERT VALUES (s.customer_id, s.region, s.smoker, s.charges, s.updated_at, s._run_id);

SELECT _run_id, COUNT(*) AS customers FROM silver.customers GROUP BY 1 ORDER BY 1;
```

<!-- RESULT -->

| _run_id | customers |
|--------:|----------:|
|       1 |      1164 |
|       2 |       136 |

*(2 rows)*

<!-- /RESULT -->

Run 2 read 1,348 versions (1,300 customers after the in-batch dedup) but changed only what was **newer**: 100 new customers + 12 updates
+ 12 double updates + 12 late versions = 136 rows with `_run_id = 2`. `WHEN MATCHED AND s.updated_at > t.updated_at` is what makes the re-read harmless: run it again and nothing changes.

---

# PART 9 — Incremental Gold: Store Parts, Not Averages

```sql
CREATE SCHEMA IF NOT EXISTS gold;
CREATE OR REPLACE TABLE gold.mart_region AS
SELECT region, COUNT(*) AS customers, SUM(charges) AS total_charges, COUNT(*) FILTER (WHERE smoker = 'yes') AS smokers
FROM silver.customers GROUP BY 1;

SELECT region, customers, total_charges, ROUND(total_charges / customers, 2) AS avg_charges, smokers FROM gold.mart_region ORDER BY 1;
```

<!-- RESULT -->

| region    | customers | total_charges | avg_charges | smokers |
|-----------|----------:|--------------:|------------:|--------:|
| northeast |       284 |    5325880.80 |     18753.1 |      58 |
| northwest |       318 |    5715902.70 |    17974.54 |      57 |
| southeast |       400 |    7005697.19 |    17514.24 |      70 |
| southwest |       298 |    5143240.87 |     17259.2 |      50 |

*(4 rows)*

<!-- /RESULT -->

An update changes one customer's charges: with **parts** (sum, count) stored, only that customer's **region row** must be recomputed.
A stored average could not be corrected without recomputing it from all the detail.

---

# PART 10 — Rebuild Only the Affected Partitions

Run 3: three customers change region or charges.

```sql
INSERT INTO changes
SELECT customer_id, 'northeast', smoker, charges, TIMESTAMP '2024-01-03 09:00', TIMESTAMP '2024-01-03 09:01', 'moved to northeast'
FROM src WHERE customer_id IN (7, 8, 9);

CREATE OR REPLACE TEMP TABLE touched AS                       -- only versions NEWER than Silver's: old region AND new region
SELECT t.region FROM latest_versions(TIMESTAMP '2024-01-04 00:00', TIMESTAMP '2024-01-02 00:00') s
JOIN silver.customers t USING (customer_id) WHERE s.updated_at > t.updated_at
UNION
SELECT s.region FROM latest_versions(TIMESTAMP '2024-01-04 00:00', TIMESTAMP '2024-01-02 00:00') s
LEFT JOIN silver.customers t USING (customer_id) WHERE t.customer_id IS NULL OR s.updated_at > t.updated_at;

MERGE INTO silver.customers AS t
USING (SELECT *, 3 AS _run_id FROM latest_versions(TIMESTAMP '2024-01-04 00:00', TIMESTAMP '2024-01-02 00:00')) AS s
ON t.customer_id = s.customer_id
WHEN MATCHED AND s.updated_at > t.updated_at THEN UPDATE SET region = s.region, smoker = s.smoker, charges = s.charges,
                                                       updated_at = s.updated_at, _run_id = s._run_id
WHEN NOT MATCHED THEN INSERT VALUES (s.customer_id, s.region, s.smoker, s.charges, s.updated_at, s._run_id);

DELETE FROM gold.mart_region WHERE region IN (SELECT region FROM touched);
INSERT INTO gold.mart_region
SELECT region, COUNT(*), SUM(charges), COUNT(*) FILTER (WHERE smoker = 'yes')
FROM silver.customers WHERE region IN (SELECT region FROM touched) GROUP BY 1;

SELECT (SELECT string_agg(region, ', ' ORDER BY region) FROM touched) AS rebuilt_regions,
       (SELECT SUM(customers) FROM gold.mart_region) AS mart_customers, (SELECT COUNT(*) FROM silver.customers) AS silver_customers;
```

<!-- RESULT -->

| rebuilt_regions                 | mart_customers | silver_customers |
|---------------------------------|---------------:|-----------------:|
| northeast, northwest, southwest |           1300 |             1300 |

*(1 row)*

<!-- /RESULT -->

3 of the 4 regions were rebuilt (southeast untouched), and the mart still equals Silver: 1,300 customers.
A customer who **moves** touches two partitions: the old region loses them, the new one gains them. Rebuild the old **and** the new.

---

# PART 11 — KPI Drift: Small Errors per Run Add Up

```sql
WITH naive AS (                                    -- the naive pipeline of Part 3: never sees the 12 late versions
  SELECT * FROM changes WHERE kind <> 'late (smoker since Jan 1)'
  QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) = 1
)
SELECT 'correct (look-back + MERGE)' AS pipeline, COUNT(*) FILTER (WHERE smoker = 'yes') AS smokers, SUM(charges) AS total_charges FROM silver.customers
UNION ALL
SELECT 'naive (updated_at > last run)', COUNT(*) FILTER (WHERE smoker = 'yes'), SUM(charges) FROM naive;
```

<!-- RESULT -->

| pipeline                      | smokers | total_charges |
|-------------------------------|--------:|--------------:|
| correct (look-back + MERGE)   |     235 |   23190721.56 |
| naive (updated_at > last run) |     225 |   23099875.85 |

*(2 rows)*

<!-- /RESULT -->

Every run "succeeds"; the naive warehouse has 10 smokers too few (2 of the 12 late customers already smoked) and $90,845.71 less in charges.
Next month a few more, and so on: **drift**.

---

# PART 12 — Validation Is Not Optional

```sql
SELECT 'one row per customer' AS test, COUNT(*) = COUNT(DISTINCT customer_id) AS passed FROM silver.customers
UNION ALL SELECT 'every customer in the source is in Silver',
       (SELECT COUNT(DISTINCT customer_id) FROM changes) = (SELECT COUNT(*) FROM silver.customers)
UNION ALL SELECT 'Silver holds the latest version',
       NOT EXISTS (SELECT 1 FROM changes c JOIN silver.customers s USING (customer_id) WHERE c.updated_at > s.updated_at)
UNION ALL SELECT 'mart = Silver (customers, charges)',
       (SELECT SUM(customers) FROM gold.mart_region) = (SELECT COUNT(*) FROM silver.customers)
   AND (SELECT SUM(total_charges) FROM gold.mart_region) = (SELECT SUM(charges) FROM silver.customers);
```

<!-- RESULT -->

| test                                      | passed |
|-------------------------------------------|--------|
| one row per customer                      | true   |
| every customer in the source is in Silver | true   |
| Silver holds the latest version           | true   |
| mart = Silver (customers, charges)        | true   |

*(4 rows)*

<!-- /RESULT -->

---

# PART 13 — Check the Shape, Not Only the Count

```sql
SELECT _run_id, COUNT(*) AS rows, MIN(charges) AS min_c, ROUND(AVG(charges), 2) AS avg_c, MAX(charges) AS max_c,
       ROUND(STDDEV(charges), 2) AS sd_c, ROUND(AVG((smoker = 'yes')::INT), 3) AS smoker_share
FROM silver.customers GROUP BY 1 ORDER BY 1;
```

<!-- RESULT -->

| _run_id | rows |   min_c |    avg_c |    max_c |     sd_c | smoker_share |
|--------:|-----:|--------:|---------:|---------:|---------:|-------------:|
|       1 | 1161 |  200.00 |  17135.8 | 61413.30 | 11900.68 |        0.171 |
|       2 |  136 |  240.00 |  23900.1 | 76107.15 | 14465.52 |        0.265 |
|       3 |    3 | 5626.56 | 15215.74 | 34201.41 | 16442.35 |        0.333 |

*(3 rows)*

<!-- /RESULT -->

Run 2's rows look very different from run 1's: average $23,900 vs $17,136, smoker share 26.5% vs 17.1%. Expected here (updates raise charges, late rows are smokers);
in production, a shift like this is the question to ask **before** publishing.

---

# PART 14 — Anomaly Checks Against History

- rows per run outside the usual range (e.g. more than 3 standard deviations from the last 30 runs)
- a KPI that moves more than X% in one run
- a run that changes 0 rows on a day that always has data

With only 3 runs there is no history yet: these checks start once the run log has a few weeks of runs (Lab 9.1's `ops.load_log`).

---

# PART 15 — Observability: a Run Log Over Time

Track per run: rows read, rows changed, runtime, failures. A slowly rising runtime or a slowly falling row count shows a problem
long before a dashboard does. (Lab 9.1 builds `ops.load_log`; slides 2, Pattern 1.)

---

# PART 16 — Failure Propagation

```sql
WITH append_only AS (SELECT * FROM changes)       -- no dedup, no MERGE: every version appended
SELECT 'append only' AS silver_built_by, COUNT(*) AS rows, SUM(charges) AS total_charges FROM append_only
UNION ALL
SELECT 'MERGE (latest version)', COUNT(*), SUM(charges) FROM silver.customers;
```

<!-- RESULT -->

| silver_built_by        | rows | total_charges |
|------------------------|-----:|--------------:|
| append only            | 1351 |   23982525.81 |
| MERGE (latest version) | 1300 |   23190721.56 |

*(2 rows)*

<!-- /RESULT -->

51 extra rows and $791,804.25 of charges counted twice. Silver duplicates → Gold totals inflated → every dashboard wrong. Errors flow **downstream**; fix them where they start.

---

# PART 17 — Tests That Stop the Pipeline

DuckDB has no `ASSERT` statement: make a failing test raise an error with `error()`, so the run stops before Gold is published.

```sql
SELECT CASE WHEN COUNT(*) <> COUNT(DISTINCT customer_id) THEN error('duplicate customers in silver.customers') END AS check_result
FROM silver.customers;
```

<!-- RESULT -->

| check_result |
|--------------|
| NULL         |

*(1 row)*

<!-- /RESULT -->

```sql
SELECT CASE WHEN COUNT(*) > 0 THEN error('the append-only table has duplicate customers') END AS check_result
FROM (SELECT customer_id FROM changes GROUP BY 1 HAVING COUNT(*) > 1);
```

<!-- ERROR -->

```text
Invalid Input Error: the append-only table has duplicate customers
```

<!-- /ERROR -->

NULL = passed. An error = the run stops, and the scheduler alerts someone.

---

# PART 18 — Performance vs Correctness

| Choice | Effect |
|---|---|
| process only new files / rows | fast, needs state and idempotency |
| look-back window, MERGE, partition rebuilds | a bit slower, correct |
| full rebuild every night | slowest, simplest, always correct (if the code is) |

👉 Incremental is a **performance optimization**. When in doubt, compare it with a full rebuild (Part 19).

---

# PART 19 — The Proof: Incremental = Full Rebuild

```sql
CREATE OR REPLACE TABLE full_rebuild AS                  -- one big run from empty, on everything that has arrived
SELECT customer_id, region, smoker, charges, updated_at FROM latest_versions(TIMESTAMP '2024-01-04 00:00', TIMESTAMP '1900-01-01');

SELECT (SELECT COUNT(*) FROM (SELECT customer_id, region, smoker, charges, updated_at FROM silver.customers
                              EXCEPT SELECT * FROM full_rebuild)) AS only_in_incremental,
       (SELECT COUNT(*) FROM (SELECT * FROM full_rebuild
                              EXCEPT SELECT customer_id, region, smoker, charges, updated_at FROM silver.customers)) AS only_in_full;
```

<!-- RESULT -->

| only_in_incremental | only_in_full |
|--------------------:|-------------:|
|                   0 |            0 |

*(1 row)*

<!-- /RESULT -->

0 and 0: three incremental runs give exactly the full rebuild. Any difference would be a bug in the **incremental** logic.

---

# PART 20 — The System View

```text
State (run log, watermark, lineage) + Time (look-back for late data)
  + Logic (dedup in the batch, idempotent MERGE, partition rebuilds)
  + Validation (tests that stop the run) + Monitoring (shape, history)
  = a pipeline that is correct every day, not just once
```

**Correct once ≠ correct forever.**
