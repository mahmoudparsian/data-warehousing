---
marp: true
theme: default
paginate: true
title: Week 6 — Session 1 — Bronze in Depth
---

# Week 6 — Session 1
## Bronze in Depth: Landing Data You Can Trust Later

Every query on these slides runs on files from week 5 (insurance by year, the 1,400 messy sales). **Lab 6.1** does the same with the pizza shop.

---

# 🎯 Bronze Has One Job

> Keep **exactly what arrived**, and know **where and when** it came from.

| Bronze does | Bronze never does |
|---|---|
| land every file **as text**, every row | fix, filter, deduplicate or type anything |
| add lineage: `_source_file`, `_batch_id`, `_ingested_at` | overwrite or delete older batches |
| **record** load problems (`reject_errors`) | hide load problems (`ignore_errors`) |
| append each new batch **once** (idempotent) | load the same file twice |

👉 If a Silver rule turns out wrong, we rebuild Silver **from Bronze**. That only works if Bronze is untouched.
(The definitions: [Medallion in a nutshell](../week05-Medallion-Architecture-Introduction/Medallion_Architecture_in_a_Nutshell.md).)

---

# 🗂️ Step 0: What Arrived?

```sql
SELECT regexp_extract(filename, '[^/]+$') AS file, size AS bytes
FROM read_blob('../week05-Medallion-Architecture-Introduction/lakehouse/examples/insurance_4_years/data/bronze/*.csv')
ORDER BY file;
```

<!-- RESULT -->

| file               | bytes |
|--------------------|------:|
| insurance.2021.csv | 50185 |
| insurance.2022.csv | 50250 |
| insurance.2023.csv | 50161 |
| insurance.2024.csv | 50246 |

*(4 rows)*

<!-- /RESULT -->

- Inventory **first**, load second: which files are **transactions** (a new one every period) and which are **reference data** (a menu, a product list)?
- `read_blob` reads only the file metadata (name, size, date): nothing is parsed yet.

---

# 🧾 Land a Batch, with Lineage

```sql
CREATE SCHEMA IF NOT EXISTS bronze;

CREATE OR REPLACE TABLE bronze.insurance AS
SELECT * EXCLUDE (filename),
       regexp_extract(filename, '[^/]+$')                        AS _source_file,   -- where from
       regexp_extract(filename, '(\d{4})', 1)::INTEGER           AS _batch_id,      -- which batch
       current_timestamp                                         AS _ingested_at    -- when
FROM read_csv('../week05-Medallion-Architecture-Introduction/lakehouse/examples/insurance_4_years/data/bronze/insurance.2021.csv',
              all_varchar = true, filename = true);

SELECT _source_file, _batch_id, COUNT(*) AS n_rows FROM bronze.insurance GROUP BY ALL;
```

<!-- RESULT -->

| _source_file       | _batch_id | n_rows |
|--------------------|----------:|-------:|
| insurance.2021.csv |      2021 |   1300 |

*(1 row)*

<!-- /RESULT -->

The leading `_` says "technical column, not business data". Other common ones: `_row_number`, `_checksum`.

---

# 🔤 Why Land as Text?

Typing **while loading** loses rows. Force `sale_date` to a date while reading the 1,400 messy sales:

```sql
CREATE OR REPLACE TABLE typed_load AS
SELECT * FROM read_csv('../week05-Medallion-Architecture-Introduction/sales_1400_messy_records/sale_records_1400_messy.csv',
                       types = {'sale_date': 'DATE'}, dateformat = '%m/%d/%Y', store_rejects = true);

SELECT (SELECT COUNT(*) FROM typed_load)                                      AS loaded,
       (SELECT COUNT(*) FROM reject_errors)                                   AS rejected_by_the_load,
       (SELECT COUNT(*) FROM reject_errors
        WHERE regexp_matches(trim(csv_line, chr(10) || chr(13) || ' '), ',\d{4}-\d{2}-\d{2}$'))           AS valid_iso_dates_among_them;
```

<!-- RESULT -->

| loaded | rejected_by_the_load | valid_iso_dates_among_them |
|-------:|---------------------:|---------------------------:|
|   1350 |                   50 |                         29 |

*(1 row)*

<!-- /RESULT -->

**29 of the 50** rejected rows have a perfectly **valid** date, just in the other format (`2025-02-13`); only 21 are really malformed. With `all_varchar = true`, every row lands, and **Silver** decides how to parse.

---

# 🚨 When a File Won't Load: Three Options

| Option | What happens | In Bronze? |
|---|---|---|
| default | the whole load **fails** with an error | ✅ you notice |
| `ignore_errors = true` | bad rows are **silently dropped** | ❌ never: data vanishes without a trace |
| `store_rejects = true` | good rows load; bad rows go to `reject_errors`, with line and reason | ✅ best: load + evidence |

```sql
SELECT line, column_name, error_type, trim(csv_line, chr(10) || chr(13)) AS csv_line
FROM reject_errors
ORDER BY line
LIMIT 3;
```

<!-- RESULT -->

| line | column_name | error_type | csv_line                                                                                           |
|-----:|-------------|------------|----------------------------------------------------------------------------------------------------|
| 1300 | sale_date   | CAST       | 400637,IN-STORE,IPHONE,Betty Rivera,betty.rivera70@icloud.com,ITALY,1,1100,0.00,ENGLAND,2025-02-13 |
| 1301 | sale_date   | CAST       | 400638,ON-LINE,TV,Rebecca White,rebecca.white18@proton.me,USA,1,900,27.00,ENGLAND,2025-11-20       |
| 1302 | sale_date   | CAST       | 400639,ON-LINE,COMPUTER,Kevin Johnson,kevin.johnson34@yahoo.com,USA,2,1400,140.00,USA,2025-12-25   |

*(3 rows)*

<!-- /RESULT -->

Error types include `CAST`, `MISSING COLUMNS`, `TOO MANY COLUMNS` and **`INVALID ENCODING`** (next slide).

---

# 🔠 Encoding and Broken Files

- A CSV file is just bytes. UTF-8 is the standard; files from Excel or older Windows systems are often **Windows-1252 / Latin-1**.
- One "smart quote" (`‘`), one accented letter, or one **full-width comma** (`，`) in the wrong place: the load fails, or one column swallows the whole line.
- Fix it at the **source** (ask for a corrected UTF-8 file), then **land the corrected file as a new file**. Never edit the original in place.

👉 Bronze keeps the evidence (`reject_errors`, the bad file) **and** the corrected file, each with its own `_source_file`.
Silver then decides which version is true. (Lab 6.1: the pizza menu.)

---

# ➕ The Next Batch: Append, Exactly Once

```sql
INSERT INTO bronze.insurance
SELECT * EXCLUDE (filename),
       regexp_extract(filename, '[^/]+$'), regexp_extract(filename, '(\d{4})', 1)::INTEGER, current_timestamp
FROM read_csv('../week05-Medallion-Architecture-Introduction/lakehouse/examples/insurance_4_years/data/bronze/insurance.2022.csv',
              all_varchar = true, filename = true)
WHERE NOT EXISTS (SELECT 1 FROM bronze.insurance WHERE _source_file = 'insurance.2022.csv');   -- idempotent

-- run the same statement a second time: it inserts 0 rows
INSERT INTO bronze.insurance
SELECT * EXCLUDE (filename),
       regexp_extract(filename, '[^/]+$'), regexp_extract(filename, '(\d{4})', 1)::INTEGER, current_timestamp
FROM read_csv('../week05-Medallion-Architecture-Introduction/lakehouse/examples/insurance_4_years/data/bronze/insurance.2022.csv',
              all_varchar = true, filename = true)
WHERE NOT EXISTS (SELECT 1 FROM bronze.insurance WHERE _source_file = 'insurance.2022.csv');

SELECT _source_file, COUNT(*) AS n_rows FROM bronze.insurance GROUP BY ALL ORDER BY 1;
```

<!-- RESULT -->

| _source_file       | n_rows |
|--------------------|-------:|
| insurance.2021.csv |   1300 |
| insurance.2022.csv |   1300 |

*(2 rows)*

<!-- /RESULT -->

**Append, don't replace. Idempotent:** a re-run (after a crash, by mistake) must not load a file twice. Real pipelines also keep a **load log** (file, rows, time, status): week 9.

---

# 🔑 Keys Across Batches

Each source file often numbers its rows **from 1**. Two tiny batches:

```sql
CREATE OR REPLACE TABLE bronze.lines AS
SELECT * FROM (VALUES (2015, 1, 'A'), (2015, 2, 'B'), (2015, 3, 'C'),
                      (2016, 1, 'X'), (2016, 2, 'Y'))
     AS t(_batch_id, line_id, item);

SELECT COUNT(*) AS line_ids_in_both_batches
FROM (SELECT line_id FROM bronze.lines GROUP BY line_id HAVING COUNT(DISTINCT _batch_id) > 1);
```

<!-- RESULT -->

| line_ids_in_both_batches |
|-------------------------:|
|                        2 |

*(1 row)*

<!-- /RESULT -->

Line 1 of 2015 and line 1 of 2016 are **different** records. The key is **(`_batch_id`, `line_id`)**, or a new surrogate key.
👉 Always test "is this id really unique?" **across** batches, not just inside one file. (Lab 6.1: thousands of pizza order lines.)

---

# 🧩 Same Source, Different File Layouts

Batches from the "same" system can differ in invisible ways: line endings (`\r\n` vs `\n`), encoding, delimiter, header spelling, **column order**.

```sql no-run
-- one glob over files with different layouts: let DuckDB read each file's header
SELECT * FROM read_csv('orders_201*.csv', all_varchar = true, filename = true, union_by_name = true);
```

👉 Without `union_by_name = true`, columns are matched by **position**, and a file with another column order or an extra column is read wrong
(week 2, SQL toolkit Part 2: the extra column is silently dropped).

---

# 🔍 Profile Bronze → the Silver To-Do List

The insurance batches are clean (try it: every count is 0, and a clean profile is a finding too). The 1,400 messy sales are not:

```sql
CREATE OR REPLACE TABLE bronze.sales AS
SELECT *, 'sale_records_1400_messy.csv' AS _source_file, current_timestamp AS _ingested_at
FROM read_csv('../week05-Medallion-Architecture-Introduction/sales_1400_messy_records/sale_records_1400_messy.csv', all_varchar = true);

SELECT COUNT(*)                                                                        AS n_rows,
       COUNT(*) - COUNT(sale_id)                                                       AS null_sale_id,
       COUNT(*) - COUNT(product)                                                       AS null_product,
       COUNT(*) - (SELECT COUNT(*) FROM (SELECT DISTINCT * EXCLUDE (_source_file, _ingested_at)
                                         FROM bronze.sales))           AS duplicate_rows,
       COUNT(*) FILTER (WHERE sale_date LIKE '__/__/____')                             AS dates_mm_dd_yyyy,
       COUNT(*) FILTER (WHERE sale_date LIKE '____-__-__')                             AS dates_yyyy_mm_dd,
       COUNT(*) FILTER (WHERE NOT (sale_date LIKE '__/__/____' OR sale_date LIKE '____-__-__')
                          OR sale_date IS NULL)                                        AS dates_other
FROM bronze.sales;
```

<!-- RESULT -->

| n_rows | null_sale_id | null_product | duplicate_rows | dates_mm_dd_yyyy | dates_yyyy_mm_dd | dates_other |
|-------:|-------------:|-------------:|---------------:|-----------------:|-----------------:|------------:|
|   1400 |           33 |           30 |             31 |             1343 |               29 |          28 |

*(1 row)*

<!-- /RESULT -->

Each count becomes a **Silver rule** (fix, reject or deduplicate), and later a line of the **reconciliation**:
Bronze rows = valid + flagged + rejected + duplicates (week 5: 1,400 = 1,258 + 33 + 78 + 31).

---

# ✅ Summary

| Bronze rule | How (DuckDB) |
|---|---|
| know what arrived | `read_blob('folder/*')`: names, sizes, before loading |
| keep what arrived | `all_varchar = true`, no fixes |
| know where / when / which batch | `filename = true` → `_source_file`, `_batch_id`, `_ingested_at` |
| record failures | `store_rejects = true` → `reject_errors` (never `ignore_errors`) |
| append each file once | `INSERT … WHERE NOT EXISTS (…)` |
| know your keys | test ids **across** batches: `(_batch_id, id)` |
| hand over a to-do list | a profile per batch: NULLs, duplicates, variants |

👉 Now: **Lab 6.1** (pizza shop: two batches and a menu that won't load).
