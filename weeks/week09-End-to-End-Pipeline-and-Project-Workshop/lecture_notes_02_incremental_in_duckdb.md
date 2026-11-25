---
marp: true
theme: default
paginate: true
title: Week 9 — Incremental Pipelines in DuckDB (patterns)
---

# Week 9
## Incremental Pipelines in DuckDB: the Patterns

Examples treat the four clean insurance files of week 7 (`week07…/data/insurance.2021…2024.csv`, 1,300 rows each) as batches that arrive over time;
the queries run one after the other, results filled in.
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
CREATE OR REPLACE TABLE load_log (run_id INT, file_name VARCHAR, rows_loaded BIGINT,
                                  loaded_at TIMESTAMPTZ, status VARCHAR);
CREATE OR REPLACE TABLE bronze_insurance (age VARCHAR, gender VARCHAR, bmi VARCHAR, children VARCHAR, smoker VARCHAR,
                                          region VARCHAR, charges VARCHAR, _source_file VARCHAR, _run_id INT);
```

- One row per file per run: the pipeline's **memory**
- `status`: `loaded`, `superseded`, `failed`, …
- Every Bronze/Silver/Gold row carries **lineage**: `_run_id`, `_source_file`

---

# 🎛️ Pattern 2: Parameters with Session Variables

```sql
SET VARIABLE run_id = 1;
SET VARIABLE upto   = 'insurance.2022.csv';     -- "what has arrived": the 2021 and 2022 files

SELECT getvariable('run_id') AS run_id, getvariable('upto') AS upto;   -- use them anywhere in SQL
```

<!-- RESULT -->

| run_id | upto               |
|-------:|--------------------|
|      1 | insurance.2022.csv |

*(1 row)*

<!-- /RESULT -->

👉 The same script (`.read run.sql`) runs again with new values: no copy-paste per run

---

# ➕ Pattern 3: Load Only New Files (Anti-Join)

The run script (the same text for every run; only the variables change):

```sql
CREATE OR REPLACE MACRO run_load() AS TABLE
SELECT * EXCLUDE (filename), regexp_extract(filename, '[^/]+$') AS _source_file, getvariable('run_id') AS _run_id
FROM read_csv('../week07-Silver-Layer-Cleaning-and-Conforming/data/insurance.*.csv', all_varchar = true, filename = true)
WHERE regexp_extract(filename, '[^/]+$') NOT IN (SELECT file_name FROM load_log)
  AND regexp_extract(filename, '[^/]+$') <= getvariable('upto');

INSERT INTO bronze_insurance SELECT * FROM run_load();                      -- run 1: 2021 + 2022
INSERT INTO load_log
SELECT getvariable('run_id'), _source_file, COUNT(*), current_timestamp, 'loaded'
FROM bronze_insurance WHERE _run_id = getvariable('run_id') GROUP BY 1, 2;

SET VARIABLE run_id = 2;  SET VARIABLE upto = 'insurance.2024.csv';          -- run 2: the next two files arrived
INSERT INTO bronze_insurance SELECT * FROM run_load();
INSERT INTO load_log
SELECT getvariable('run_id'), _source_file, COUNT(*), current_timestamp, 'loaded'
FROM bronze_insurance WHERE _run_id = getvariable('run_id') GROUP BY 1, 2;

SET VARIABLE run_id = 3;                                                     -- run 3: nothing new arrived
INSERT INTO bronze_insurance SELECT * FROM run_load();

SELECT run_id, file_name, rows_loaded, status FROM load_log
UNION ALL
SELECT 3, '(run 3: new rows)', (SELECT COUNT(*) FROM bronze_insurance WHERE _run_id = 3), NULL
ORDER BY run_id, file_name;
```

<!-- RESULT -->

| run_id | file_name          | rows_loaded | status |
|-------:|--------------------|------------:|--------|
|      1 | insurance.2021.csv |        1300 | loaded |
|      1 | insurance.2022.csv |        1300 | loaded |
|      2 | insurance.2023.csv |        1300 | loaded |
|      2 | insurance.2024.csv |        1300 | loaded |
|      3 | (run 3: new rows)  |           0 | NULL   |

*(5 rows)*

<!-- /RESULT -->

Run 3 with the same `upto` → **0 rows**: the pipeline is **idempotent** (running it twice changes nothing).

---

# 🧩 Pattern 4: Package the Rules (Table Macro)

```sql
CREATE OR REPLACE MACRO silver_by_run(run) AS TABLE
SELECT TRY_CAST(age AS INT) AS age, lower(trim(region)) AS region,
       TRY_CAST(charges AS DECIMAL(10, 2)) AS charges, _source_file, _run_id
FROM bronze_insurance
WHERE _run_id = run;

SELECT _source_file, COUNT(*) AS n_rows, ROUND(AVG(charges), 2) AS avg_charges FROM silver_by_run(2) GROUP BY 1 ORDER BY 1;
```

<!-- RESULT -->

| _source_file       | n_rows | avg_charges |
|--------------------|-------:|------------:|
| insurance.2023.csv |   1300 |    17149.93 |
| insurance.2024.csv |   1300 |     17726.5 |

*(2 rows)*

<!-- /RESULT -->

👉 One definition of "the Silver rules", used by every run **and** by the full rebuild (here only typing; the clean files need no rejects:
a real Silver macro holds all the week 7 rules, and its reject table gets the same `_run_id`)

---

# 🔑 Pattern 5: Append with New Surrogate Keys

```sql no-run
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

```sql no-run
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
```sql no-run
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
