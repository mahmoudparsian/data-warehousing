---
marp: true
theme: default
paginate: true
title: Week 9 — Incremental Pipelines in DuckDB (patterns)
---

# Week 9
## Incremental Pipelines in DuckDB: the Patterns

Examples treat the four insurance files (`week05…/insurance_4_years/data/bronze/insurance.2021…2024.csv`) as batches that arrive over time.
The labs apply the same patterns to the pizza shop's monthly delivery files.

---

# 🔁 Full Rebuild vs Incremental

| | Full rebuild | Incremental |
|---|---|---|
| each run processes | **all** data | only **new / changed** data |
| cost | grows with history | grows with the new batch |
| simple? | very | needs **state** |
| state kept | none | a **load log** (+ lineage on every row) |

👉 Incremental is a performance optimization. It must give the **same answer** as a full rebuild

---

# 🧾 Pattern 1: A Load Log

```sql
CREATE TABLE load_log (run_id INT, file_name VARCHAR, rows_loaded BIGINT,
                       loaded_at TIMESTAMPTZ, status VARCHAR);
```

- One row per file per run: the pipeline's **memory**
- `status`: `loaded`, `superseded`, `failed`, …
- Every Bronze/Silver/Gold row carries **lineage**: `_run_id`, `_source_file`

---

# 🎛️ Pattern 2: Parameters with Session Variables

```sql
SET VARIABLE run_id = 2;
SET VARIABLE upto   = 'insurance.2024.csv';     -- "what has arrived"

SELECT getvariable('run_id');                    -- use them anywhere in SQL
```

👉 The same script (`.read run.sql`) runs again with new values: no copy-paste per run

---

# ➕ Pattern 3: Load Only New Files (Anti-Join)

```sql
INSERT INTO bronze_insurance
SELECT * EXCLUDE (filename), regexp_extract(filename, '[^/]+$'), getvariable('run_id')
FROM read_csv('insurance.*.csv', all_varchar = true, filename = true)
WHERE regexp_extract(filename, '[^/]+$') NOT IN (SELECT file_name FROM load_log)
  AND regexp_extract(filename, '[^/]+$') <= getvariable('upto');

INSERT INTO load_log
SELECT getvariable('run_id'), _source_file, COUNT(*), current_timestamp, 'loaded'
FROM bronze_insurance WHERE _run_id = getvariable('run_id') GROUP BY 1, 2;
```

| run_id | file_name | rows_loaded |
|---|---|---|
| 1 | insurance.2021.csv | 1,300 |
| 1 | insurance.2022.csv | 1,300 |
| 2 | insurance.2023.csv | 1,300 |
| 2 | insurance.2024.csv | 1,300 |

Run 3 with the same `upto` → **0 rows**: the pipeline is **idempotent**

---

# 🧩 Pattern 4: Package the Rules (Table Macro)

```sql
CREATE MACRO silver_by_run(run) AS TABLE
SELECT CAST(age AS INT) AS age, lower(trim(region)) AS region,
       CAST(charges AS DOUBLE) AS charges, _source_file, _run_id
FROM bronze_insurance
WHERE _run_id = run;

SELECT _source_file, COUNT(*), ROUND(AVG(charges), 2) FROM silver_by_run(2) GROUP BY 1;
```

| _source_file | count | avg |
|---|---|---|
| insurance.2023.csv | 1,300 | 17,149.93 |
| insurance.2024.csv | 1,300 | 17,726.50 |

👉 One definition of "the Silver rules", used by every run **and** by the full rebuild

---

# 🔑 Pattern 5: Append with New Surrogate Keys

```sql
INSERT INTO gold.fact
SELECT (SELECT MAX(line_key) FROM gold.fact) + ROW_NUMBER() OVER (ORDER BY <stable columns>),
       …
FROM silver_table WHERE _run_id = getvariable('run_id');
```

- Keys continue after the current maximum (or use a `SEQUENCE`)
- `ORDER BY` inside `ROW_NUMBER()` makes keys **reproducible**

---

# 🕰️ Pattern 6: Late Data → Rebuild Affected Partitions

A batch can contain rows for **periods you already reported** (late orders, time-zone edges, back-dated corrections)

```sql
-- which days did this run touch?
CREATE TEMP TABLE touched AS
SELECT DISTINCT d.full_date FROM gold.fact f JOIN gold.dim_date d USING (date_key)
WHERE f._run_id = getvariable('run_id');

DELETE FROM gold.mart_daily WHERE full_date IN (SELECT full_date FROM touched);
INSERT INTO gold.mart_daily SELECT … FROM gold.fact … WHERE full_date IN (SELECT full_date FROM touched) GROUP BY …;
```

👉 Rebuild **what changed**, not everything, and not only "the newest day"

---

# ♻️ Pattern 7: A Corrected Re-send Replaces, Never Adds

1. Land the new version in Bronze (keep the old one: audit)
2. `UPDATE load_log SET status = 'superseded' WHERE file_name = '<old file>'`
3. Remember the periods the old file touched
4. `DELETE` Silver/Gold rows `WHERE _source_file = '<old file>'` (lineage makes this possible)
5. Process the new version as a normal run
6. Rebuild the affected mart partitions (old ∪ new periods)

👉 Without `_source_file` on every row, step 4 is impossible and you are back to a full rebuild

---

# ✅ Pattern 8: Prove It (Incremental = Full)

```bash
duckdb full.duckdb < setup.sql        # empty warehouse
```
```sql
-- ONE run with the latest version of every file …
ATTACH 'warehouse.duckdb' AS inc (READ_ONLY);
SELECT 'full', COUNT(*), SUM(revenue) FROM gold.fact
UNION ALL SELECT 'incremental', COUNT(*), SUM(revenue) FROM inc.gold.fact;
-- and per month with EXCEPT: no rows = identical
```

👉 "A full rebuild is just one big incremental run from empty." Same code, so any difference is a bug in the **incremental logic**

---

# ✅ Summary

| Need | Pattern |
|---|---|
| remember what ran | load log + lineage columns |
| reuse one script | `SET VARIABLE` / `getvariable()` |
| only new data | anti-join on the load log |
| one set of rules | table macro |
| new keys | `MAX + ROW_NUMBER() OVER (ORDER BY …)` |
| late data | rebuild **touched** partitions |
| corrections | supersede + delete by `_source_file` + reprocess |
| trust | compare with a full rebuild (`ATTACH`) |
