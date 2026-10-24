---
marp: true
theme: default
paginate: true
title: Week 6 — Session 1 — Bronze in Depth
---

# Week 6 — Session 1
## Bronze in Depth: Landing Data You Can Trust Later

---

# 🎯 Bronze Has One Job

> Keep **exactly what arrived**, and know **where and when** it came from.

- No cleaning, no "small fixes"
- Append-only: new data is **added**, never overwrites
- Every row traceable to a file and a batch
- Every load problem **recorded**

👉 If Silver has a bug, we rebuild Silver **from Bronze**. Only possible if Bronze is untouched.

---

# 🗂️ Step 0: What Arrived?

```sql
SELECT regexp_extract(filename, '[^/]+$') AS file, size
FROM read_blob('lakehouse/examples/insurance_4_years/data/bronze/*.csv')
ORDER BY file;
```

| file | size |
|---|---|
| insurance.2021.csv | 50,185 |
| insurance.2022.csv | 50,250 |
| … | … |

- Which files are **transactions** (a new one every period) and which are **reference data** (a menu, a product list)?
- Inventory first, load second

---

# 🧾 Lineage Columns

```sql
CREATE TABLE bronze.insurance AS
SELECT * EXCLUDE (filename),
       regexp_extract(filename, '[^/]+$') AS _source_file,   -- where from
       current_timestamp                  AS _ingested_at    -- when
FROM read_csv('…/insurance.2021.csv', all_varchar = true, filename = true);
```

Common lineage columns: `_source_file`, `_batch_id` (load / period), `_ingested_at`, sometimes `_row_number`, `_checksum`

👉 The leading `_` says "technical column, not business data"

---

# 🔤 Why Load as Text?

Typing at load time **silently loses rows**. Example: force `sale_date` to a date while loading the 1,400 messy sales:

```sql
CREATE TABLE s AS
SELECT * FROM read_csv('sales_1400_messy_records/sale_records_1400_messy.csv',
                       types = {'sale_date': 'DATE'}, dateformat = '%m/%d/%Y',
                       store_rejects = true);
```

→ 1,350 rows loaded, **50 rejected**: 21 truly malformed dates, but also **29 valid `YYYY-MM-DD` dates** the load format didn't expect

👉 Bronze: `all_varchar = true`. Silver decides how to parse.

---

# 🚨 When a File Won't Load

| Option | What happens | Use in Bronze? |
|---|---|---|
| default | the whole load **fails** with an error | ✅ good: you notice |
| `ignore_errors = true` | bad rows **silently dropped** | ❌ never: data vanishes |
| `store_rejects = true` | good rows load; bad rows go to `reject_errors` | ✅ best: load + evidence |

```sql
SELECT line, column_name, error_type, csv_line FROM reject_errors;
```

| line | column_name | error_type | csv_line |
|---|---|---|---|
| 1300 | sale_date | CAST | 400637,IN-STORE,IPHONE,…,2025-02-13 |

Error types include `CAST`, `MISSING COLUMNS`, `TOO MANY COLUMNS`, **`INVALID ENCODING`**

---

# 🔠 Encoding

- CSV files are just bytes. UTF-8 is the standard, but files from Excel or old Windows systems are often **Windows-1252 / Latin-1**
- One "smart quote" (`‘`) or accented letter in the wrong encoding → `Invalid unicode … not utf-8 encoded`
- Fix at the **source** (ask for a UTF-8 file) or convert it, and **land the corrected file as a new file**: don't edit the original

👉 Bronze keeps both the bad file's evidence and the corrected file

---

# ➕ The Next Batch Arrives

```sql
INSERT INTO bronze.insurance
SELECT * EXCLUDE (filename),
       regexp_extract(filename, '[^/]+$'), current_timestamp
FROM read_csv('…/insurance.2022.csv', all_varchar = true, filename = true)
WHERE NOT EXISTS (SELECT 1 FROM bronze.insurance
                  WHERE _source_file = 'insurance.2022.csv');   -- idempotent
```

- Append, don't replace
- **Idempotent**: running it twice must not load twice (2nd run → 0 rows)
- Real pipelines keep a **load log**: file, rows, checksum, time, status

---

# 🔑 Keys Across Batches

- Each source file often numbers its rows **from 1**
- Batch 1 `line_id = 1` and batch 2 `line_id = 1` are **different** records
- So in Bronze/Silver the key is **(batch, id)**, or a new surrogate key

```sql
SELECT COUNT(*) FROM (SELECT line_id FROM bronze.lines
                      GROUP BY line_id HAVING COUNT(DISTINCT _batch_id) > 1);
```

👉 Always test "is this id really unique?" **across** batches, not just within one file

---

# 🧩 Same Source, Different File Formats

Batches from the "same" system can differ in invisible ways:

- line endings: `\r\n` (Windows) in one year, `\n` in the next
- encoding (UTF-8 vs Windows-1252), delimiter, header spelling, column order

```sql
-- one glob over files with different layouts: let DuckDB sniff each file
SELECT * FROM read_csv('orders_201*.csv', all_varchar = true, filename = true,
                       union_by_name = true);
```

👉 Without `union_by_name = true`, DuckDB sniffs the **first** file only, and a later file's header can be misread

---

# 🔍 Profile Bronze → Silver To-Do List

Before writing any Silver rule, measure per batch:

- NULLs in key columns
- exact duplicate rows
- format variants (dates, codes, case)
- rows that failed to load (`reject_errors`)
- ids that collide across batches

👉 These counts become the **reconciliation** at the end of Silver

---

# ✅ Summary

| Bronze rule | How (DuckDB) |
|---|---|
| keep what arrived | `all_varchar = true`, no fixes |
| know where/when | `filename = true`, `_batch_id`, `_ingested_at` |
| record failures | `store_rejects = true` → `reject_errors` |
| append, once | `INSERT … WHERE NOT EXISTS (…)` |
| know your keys | check ids across batches |

👉 Now: **Lab 6.1** (pizza shop, two batches)
