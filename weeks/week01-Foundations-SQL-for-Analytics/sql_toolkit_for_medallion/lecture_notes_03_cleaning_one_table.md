---
marp: true
title: Week 1 — SQL Toolkit for the Medallion Architecture, Part 1 (Clean One Table)
paginate: true
theme: default
class: lead
---

# Week 1 — SQL Toolkit, Part 1
## Getting Ready for the Medallion Architecture: Clean One Table

NULLs and defaults · text cleanup · types · flag and keep · `CREATE SCHEMA / TABLE / VIEW`

---

# 🎯 Why Now?

In weeks 5–9 we build a **medallion** pipeline:

| Layer | What it holds |
|---|---|
| 🥉 **Bronze** | the data **exactly as it arrived** (often all text) |
| 🥈 **Silver** | the same data **cleaned**: right types, standard values, no duplicates |
| 🥇 **Gold** | star schema + business tables, ready for reports |

Bronze → Silver is mostly **one big `SELECT`** with a dozen functions you can learn **today**.

- **Part 1 (this week):** clean **one** table
- **Part 2 (week 2):** many files, dates, duplicates, joins, reconciliation

---

# 🚲 Our Data: City Bike-Share Members

`data/members.csv`: one row per member (43 rows, 9 columns). A real export, so it is **messy**.

**Bronze habit:** load every column **as text** (`all_varchar = true`). Loading never fails; we fix types later.

```sql
CREATE OR REPLACE TABLE raw_members AS
SELECT * FROM read_csv('data/members.csv', all_varchar = true);

SELECT member_id, city, plan, monthly_fee, age
FROM raw_members
LIMIT 6;
```

<!-- RESULT -->

| member_id | city           | plan     | monthly_fee | age |
|-----------|----------------|----------|-------------|-----|
| 101       | santa clara    | annual   | 9.50        | 32  |
| 102       | San Francisco  | Monthly  | 15.00       | 33  |
| 103       | SANTA CLARA    | monthly  | 15.00       | 36  |
| 104       | San Francisco  |          | NULL        | 60  |
| 105       | san jose       | Monthly  | 15.00       | 31  |
| 106       |  San Jose      |  ANNUAL  | 9.50        |  51 |

*(6 rows)*

<!-- /RESULT -->

👉 Spaces, upper/lower case, a blank plan, a blank fee… The next slide lists **every** problem in this file.

---

# 🔍 The Problems in This File (and Where We Fix Them)

| Column | Problem in Bronze (member ids) | Silver goal | Slide |
|---|---|---|---|
| `email` | NULL (108), blank `' '` (121), upper case (133) | lower case, `'unknown'` if missing | `COALESCE`, `NULLIF` |
| `city` | 12 spellings of 3 cities: case, spaces at the ends, `SF`, `SJ` | `San Jose` / `San Francisco` / `Santa Clara` | Text cleanup, `CASE` |
| `plan` | case, `' ANNUAL '`, blank (104), NULL (126), `'N/A'` (117) | `Annual` / `Monthly` / `Unknown` | `CASE` |
| `monthly_fee` | `'$15.00'` (110, 122), blank (114), `'free'` (129), NULL (104, 117, 126) | `DECIMAL(6, 2)`, NULL if unknown | `REPLACE` + `TRY_CAST` |
| `age` | `'unknown'` (112), blank (119), NULL (137), `230` (131), `' 51'` (106) | `INTEGER` 16–100, else NULL | `TRY_CAST`, flag |
| `signup_date` | `2025-02-30` (124): a day that does not exist | `DATE`, NULL if impossible | Dates |
| `member_id` | 103, 115, 128 appear **twice** (an update on 2026-01-20) | one row per member | **Part 2** (`QUALIFY`) |

Rule for the whole session: **never lose a row, never hide a problem**: 43 rows in Bronze → 43 rows in Silver, every NULL and default counted.

---

# 🤔 Why Load as Text?

If we let DuckDB **guess** the types, one bad value turns a whole column into text anyway:

```sql
SELECT column_name, column_type
FROM (DESCRIBE SELECT * FROM read_csv('data/members.csv'));
```

<!-- RESULT -->

| column_name | column_type |
|-------------|-------------|
| member_id   | BIGINT      |
| full_name   | VARCHAR     |
| email       | VARCHAR     |
| city        | VARCHAR     |
| plan        | VARCHAR     |
| monthly_fee | VARCHAR     |
| age         | VARCHAR     |
| signup_date | VARCHAR     |
| updated_at  | TIMESTAMP   |

*(9 rows)*

<!-- /RESULT -->

- `age` is text because of values like `unknown`, `monthly_fee` because of `$15.00` and `free`, `signup_date` because of one impossible date.
- With `all_varchar = true` every column is text, **on purpose**. Silver decides the types.

---

# Part A — NULL: "We Don't Know"

`NULL` means **missing / unknown**. It is **not** `0` and **not** an empty or blank string.

| Rule | Example |
|---|---|
| Any comparison with NULL is unknown → row not kept | `WHERE plan = NULL` finds **nothing** |
| Test for NULL with `IS NULL` / `IS NOT NULL` | `WHERE plan IS NULL` |
| `COUNT(*)` counts rows; `COUNT(col)` skips NULLs | see next slide |
| `SUM`, `AVG`, `MIN`, `MAX` skip NULLs | `AVG` of (10, NULL, 20) = 15 |
| `GROUP BY` puts all NULLs in **one** group | next slides |
| Arithmetic with NULL gives NULL | `5 + NULL` = NULL |

---

# 🐞 `= NULL` Never Works

```sql
SELECT
  (SELECT COUNT(*) FROM raw_members WHERE plan = NULL)  AS with_equals,
  (SELECT COUNT(*) FROM raw_members WHERE plan IS NULL) AS with_is_null;
```

<!-- RESULT -->

| with_equals | with_is_null |
|------------:|-------------:|
|           0 |            1 |

*(1 row)*

<!-- /RESULT -->

👉 The query with `= NULL` runs **without an error** and gives a **wrong** answer: the most dangerous kind of bug.

---

# 🔢 `COUNT(*)` vs `COUNT(column)`

```sql
SELECT COUNT(*)                  AS n_rows,
       COUNT(email)              AS n_email,
       COUNT(plan)               AS n_plan,
       COUNT(age)                AS n_age,
       COUNT(DISTINCT member_id) AS n_members
FROM raw_members;
```

<!-- RESULT -->

| n_rows | n_email | n_plan | n_age | n_members |
|-------:|--------:|-------:|------:|----------:|
|     43 |      42 |     42 |    42 |        40 |

*(1 row)*

<!-- /RESULT -->

- `COUNT(*) - COUNT(col)` = number of NULLs in `col`: the first **profiling** query of every Bronze table.
- 43 rows but only 40 members: some members appear **twice** (fixed in Part 2).

---

# 👀 What Values Are Really There?

```sql
SELECT plan, COUNT(*) AS n
FROM raw_members
GROUP BY plan
ORDER BY n DESC, plan;
```

<!-- RESULT -->

| plan     |  n |
|----------|---:|
| Monthly  | 15 |
|  ANNUAL  |  7 |
| Annual   |  7 |
| monthly  |  7 |
| annual   |  4 |
|          |  1 |
| N/A      |  1 |
| NULL     |  1 |

*(8 rows)*

<!-- /RESULT -->

Only **2** real plans (Annual, Monthly), but **8** groups: case, spaces, a NULL, a blank `' '` and `'N/A'`.

---

# 🩹 `COALESCE`: Replace NULL with a Default

`COALESCE(a, b, c, …)` returns the **first value that is not NULL**.

```sql
SELECT member_id,
       email,
       COALESCE(email, 'unknown') AS email_or_default
FROM raw_members
WHERE email IS NULL OR TRIM(email) = '';
```

<!-- RESULT -->

| member_id | email | email_or_default |
|-----------|-------|------------------|
| 108       | NULL  | unknown          |
| 121       |       |                  |

*(2 rows)*

<!-- /RESULT -->

⚠️ The blank email `' '` was **not** replaced: `COALESCE` only replaces **NULL**.
(`IFNULL(a, b)` is the same as `COALESCE(a, b)` with two values.)

---

# 🔁 `NULLIF`: Turn a "Fake" Value into NULL

`NULLIF(a, b)` returns **NULL if a = b**, otherwise `a`.

```sql
SELECT member_id,
       email,
       NULLIF(TRIM(email), '')                         AS email_null_if_blank,
       COALESCE(NULLIF(TRIM(email), ''), 'unknown')    AS email_clean
FROM raw_members
WHERE email IS NULL OR TRIM(email) = '';
```

<!-- RESULT -->

| member_id | email | email_null_if_blank | email_clean |
|-----------|-------|---------------------|-------------|
| 108       | NULL  | NULL                | unknown     |
| 121       |       | NULL                | unknown     |

*(2 rows)*

<!-- /RESULT -->

⭐ **The Silver pattern:** `COALESCE(NULLIF(TRIM(col), ''), 'default')`: trim → blank becomes NULL → NULL becomes the default.

---

# ➗ `NULLIF` Also Prevents "Divide by Zero"

Revenue per ride, when a station had **no** rides:

```sql
SELECT station,
       revenue / rides               AS per_ride_unsafe,
       revenue / NULLIF(rides, 0)    AS per_ride_safe
FROM (VALUES ('Diridon', 96.0, 40), ('Market St', 0.0, 0)) AS t(station, revenue, rides);
```

<!-- RESULT -->

| station   | per_ride_unsafe | per_ride_safe |
|-----------|----------------:|--------------:|
| Diridon   |             2.4 |           2.4 |
| Market St |             nan |          NULL |

*(2 rows)*

<!-- /RESULT -->

- In DuckDB 2.0, `x / 0` gives `inf` (and `0 / 0` gives `nan`); `x // 0` raises an error. One `inf` or `nan` poisons every `SUM` and `AVG` that uses it.
- `NULLIF(rides, 0)` makes the result NULL ("no answer"), which `AVG` then skips.

---

# Part B — Text Cleanup

| Function | Does | Example → result |
|---|---|---|
| `TRIM(s)` | removes spaces at both ends | `' San Jose'` → `'San Jose'` |
| `UPPER(s)` / `LOWER(s)` | changes case | `'san jose'` → `'SAN JOSE'` |
| `REPLACE(s, from, to)` | replaces text | `REPLACE('$15.00', '$', '')` → `'15.00'` |
| `LENGTH(s)` | number of characters (finds hidden spaces) | `LENGTH('SF ')` → 3 |
| `s1 \|\| s2` | joins text | `'[' \|\| city \|\| ']'` shows the spaces |

👉 Always **compare** text after `TRIM` + `UPPER` (or `LOWER`), never raw.

---

# 🏙️ How Many Cities Are There Really?

```sql
SELECT UPPER(TRIM(city)) AS city_key,
       COUNT(*)          AS n,
       COUNT(DISTINCT city) AS spellings
FROM raw_members
GROUP BY city_key
ORDER BY n DESC, city_key;
```

<!-- RESULT -->

| city_key      |  n | spellings |
|---------------|---:|----------:|
| SAN JOSE      | 15 |         4 |
| SANTA CLARA   | 15 |         3 |
| SAN FRANCISCO | 11 |         3 |
| SF            |  1 |         1 |
| SJ            |  1 |         1 |

*(5 rows)*

<!-- /RESULT -->

`TRIM` + `UPPER` turned 12 spellings into 5 keys. `SJ` and `SF` are **abbreviations**: no function fixes those, we need a rule.

---

# 🗺️ `CASE` Maps Messy Values to Standard Values

```sql
SELECT CASE
         WHEN UPPER(TRIM(city)) IN ('SAN JOSE', 'SJ')      THEN 'San Jose'
         WHEN UPPER(TRIM(city)) IN ('SAN FRANCISCO', 'SF') THEN 'San Francisco'
         WHEN UPPER(TRIM(city)) = 'SANTA CLARA'            THEN 'Santa Clara'
         ELSE 'Unknown'
       END      AS city_clean,
       COUNT(*) AS n
FROM raw_members
GROUP BY city_clean
ORDER BY n DESC;
```

<!-- RESULT -->

| city_clean    |  n |
|---------------|---:|
| San Jose      | 16 |
| Santa Clara   | 15 |
| San Francisco | 12 |

*(3 rows)*

<!-- /RESULT -->

- Always add `ELSE 'Unknown'` (never silently NULL): a **new** spelling next month shows up as `Unknown` instead of disappearing.
- In week 7 this list becomes a **mapping table** you `JOIN` to.

---

# 📋 Same Idea for `plan`

```sql
SELECT CASE LOWER(TRIM(plan))
         WHEN 'annual'  THEN 'Annual'
         WHEN 'monthly' THEN 'Monthly'
         ELSE 'Unknown'
       END      AS plan_clean,
       COUNT(*) AS n
FROM raw_members
GROUP BY plan_clean
ORDER BY n DESC;
```

<!-- RESULT -->

| plan_clean |  n |
|------------|---:|
| Monthly    | 22 |
| Annual     | 18 |
| Unknown    |  3 |

*(3 rows)*

<!-- /RESULT -->

The NULL, the blank and `'N/A'` all fall into `ELSE`: `CASE NULL WHEN …` never matches.

---

# Part C — Types: `CAST` vs `TRY_CAST`

`CAST(x AS type)` (short form `x::type`) **fails** on the first bad value:

```sql
SELECT CAST(age AS INTEGER) AS age FROM raw_members;
```

<!-- ERROR -->

```text
Conversion Error: Could not convert string 'unknown' to INT32 when casting from source column age

LINE 1: SELECT CAST(age AS INTEGER) AS age FROM raw_members;
               ^^^^^^^^^^^^^^^^^^^^
```

<!-- /ERROR -->

`TRY_CAST` returns **NULL** instead of failing:

```sql
SELECT age AS raw_age, TRY_CAST(age AS INTEGER) AS age_int
FROM raw_members
WHERE TRY_CAST(age AS INTEGER) IS NULL OR TRY_CAST(age AS INTEGER) > 100;
```

<!-- RESULT -->

| raw_age | age_int |
|---------|--------:|
| unknown |    NULL |
|         |    NULL |
| 230     |     230 |
| NULL    |    NULL |

*(4 rows)*

<!-- /RESULT -->

⚠️ `TRY_CAST` **hides** problems. Always **count** the rows it turned into NULL. And a value that casts fine can still be **impossible** (age 230).
(`' 51'`, member 106, is not in the list: a cast to a number ignores spaces at the ends.)

---

# 💲 Numbers Stored as Text

```sql
SELECT monthly_fee                                           AS raw_fee,
       TRY_CAST(REPLACE(TRIM(monthly_fee), '$', '') AS DECIMAL(6, 2)) AS fee,
       COUNT(*)                                              AS n
FROM raw_members
GROUP BY ALL
ORDER BY n DESC, raw_fee;
```

<!-- RESULT -->

| raw_fee |   fee |  n |
|---------|------:|---:|
| 15.00   | 15.00 | 19 |
| 9.50    |  9.50 | 17 |
| NULL    |  NULL |  3 |
| $15.00  | 15.00 |  2 |
|         |  NULL |  1 |
| free    |  NULL |  1 |

*(6 rows)*

<!-- /RESULT -->

- Remove the `'$'` first, then cast. `DECIMAL(6, 2)` = exact money (never `DOUBLE` for money).
- `'free'`: is it `0.00` or unknown? That is a **business** question: ask the data owner, then write the rule down.
- Checking a computed amount? Allow for rounding: `ABS(total - (price - discount)) > 0.01`, never `=`.

---

# 📅 Dates Stored as Text

```sql
SELECT member_id,
       signup_date                     AS raw_date,
       TRY_CAST(signup_date AS DATE)   AS signup_date_clean
FROM raw_members
WHERE TRY_CAST(signup_date AS DATE) IS NULL;
```

<!-- RESULT -->

| member_id | raw_date   | signup_date_clean |
|-----------|------------|-------------------|
| 124       | 2025-02-30 | NULL              |

*(1 row)*

<!-- /RESULT -->

- `CAST(text AS DATE)` reads the ISO format `YYYY-MM-DD` only. February 30 does not exist → NULL.
- Other formats (`03/15/2026`, `15.03.2026`) need `strptime`: **Part 2**, week 2.

---

# 🚩 Flag and Keep (Don't Silently Delete)

Silver usually **keeps** a bad row and says what is wrong with it:

```sql
WITH flagged AS (
  SELECT member_id, age, signup_date,
         concat_ws(', ',
           CASE WHEN TRY_CAST(age AS INTEGER) IS NULL                THEN 'age missing' END,
           CASE WHEN TRY_CAST(age AS INTEGER) NOT BETWEEN 16 AND 100 THEN 'age invalid' END,
           CASE WHEN TRY_CAST(signup_date AS DATE) IS NULL           THEN 'bad date'    END
         ) AS dq_issue
  FROM raw_members
)
SELECT * FROM flagged
WHERE dq_issue <> ''
ORDER BY member_id;
```

<!-- RESULT -->

| member_id | age     | signup_date | dq_issue    |
|-----------|---------|-------------|-------------|
| 112       | unknown | 2025-08-07  | age missing |
| 119       |         | 2025-01-29  | age missing |
| 124       | 55      | 2025-02-30  | bad date    |
| 131       | 230     | 2025-01-26  | age invalid |
| 137       | NULL    | 2025-10-18  | age missing |

*(5 rows)*

<!-- /RESULT -->

`concat_ws(sep, …)` joins the non-NULL parts: each `CASE` without `ELSE` adds a message or nothing.
Here we only **look** at the flags; in Part 2 the Silver table `silver.rentals` keeps a `dq_issue` column.

---

# Part D — Save the Layers: `CREATE SCHEMA`

A **schema** is a folder for tables inside one database: `bronze.members`, `silver.members`.

```sql
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;

CREATE OR REPLACE TABLE bronze.members AS
SELECT *, current_timestamp AS _loaded_at       -- lineage: when did it arrive?
FROM read_csv('data/members.csv', all_varchar = true);

SELECT COUNT(*) AS bronze_rows FROM bronze.members;
```

<!-- RESULT -->

| bronze_rows |
|------------:|
|          43 |

*(1 row)*

<!-- /RESULT -->

`CREATE OR REPLACE TABLE … AS SELECT …` (CTAS) creates the table from a query: re-running it gives the same result.

---

# 🥈 One `SELECT` Builds the Silver Table

```sql
CREATE OR REPLACE TABLE silver.members AS
SELECT
  TRY_CAST(member_id AS INTEGER)                               AS member_id,
  TRIM(full_name)                                              AS full_name,
  LOWER(COALESCE(NULLIF(TRIM(email), ''), 'unknown'))          AS email,
  CASE WHEN UPPER(TRIM(city)) IN ('SAN JOSE', 'SJ')      THEN 'San Jose'
       WHEN UPPER(TRIM(city)) IN ('SAN FRANCISCO', 'SF') THEN 'San Francisco'
       WHEN UPPER(TRIM(city)) = 'SANTA CLARA'            THEN 'Santa Clara'
       ELSE 'Unknown' END                                      AS city,
  CASE LOWER(TRIM(plan)) WHEN 'annual'  THEN 'Annual'
                         WHEN 'monthly' THEN 'Monthly'
                         ELSE 'Unknown' END                    AS plan,
  TRY_CAST(REPLACE(TRIM(monthly_fee), '$', '') AS DECIMAL(6, 2)) AS monthly_fee,
  CASE WHEN TRY_CAST(age AS INTEGER) BETWEEN 16 AND 100
       THEN TRY_CAST(age AS INTEGER) END                       AS age,
  TRY_CAST(signup_date AS DATE)                                AS signup_date,
  TRY_CAST(updated_at AS TIMESTAMP)                            AS updated_at
FROM bronze.members;
```

Every line is a pattern from this session. The **order** of the steps matters: `TRIM` before `UPPER` before `CASE`; `REPLACE` before `TRY_CAST`.

---

# 🥈 The Silver Table

```sql
SELECT member_id, city, plan, monthly_fee, age, signup_date, updated_at
FROM silver.members
ORDER BY member_id
LIMIT 5;
```

<!-- RESULT -->

| member_id | city          | plan    | monthly_fee | age | signup_date | updated_at          |
|----------:|---------------|---------|------------:|----:|-------------|---------------------|
|       101 | Santa Clara   | Annual  |        9.50 |  32 | 2025-06-22  | 2025-06-22 09:00:00 |
|       102 | San Francisco | Monthly |       15.00 |  33 | 2025-04-27  | 2025-04-27 09:00:00 |
|       103 | Santa Clara   | Monthly |       15.00 |  36 | 2025-10-21  | 2025-10-21 09:00:00 |
|       103 | San Francisco | Annual  |        9.50 |  36 | 2025-10-21  | 2026-01-20 18:30:00 |
|       104 | San Francisco | Unknown |        NULL |  60 | 2025-04-07  | 2025-04-07 09:00:00 |

*(5 rows)*

<!-- /RESULT -->

👉 Member **103 appears twice** (an old row and an update from 2026-01-20). Choosing the newest row per member is **Part 2** (`QUALIFY`).

---

# ✅ Check the Silver Table

```sql
SELECT (SELECT COUNT(*) FROM bronze.members) AS bronze_rows,
       COUNT(*)                              AS silver_rows,
       COUNT(*) FILTER (WHERE email = 'unknown') AS email_unknown,
       COUNT(*) FILTER (WHERE plan  = 'Unknown') AS plan_unknown,
       COUNT(*) - COUNT(monthly_fee)         AS fee_null,
       COUNT(*) - COUNT(age)                 AS age_null,
       COUNT(*) - COUNT(signup_date)         AS date_null
FROM silver.members;
```

<!-- RESULT -->

| bronze_rows | silver_rows | email_unknown | plan_unknown | fee_null | age_null | date_null |
|------------:|------------:|--------------:|-------------:|---------:|---------:|----------:|
|          43 |          43 |             2 |            3 |        5 |        4 |         1 |

*(1 row)*

<!-- /RESULT -->

**Reconcile:** rows in = rows out, and every default / NULL is **counted**, so nothing is hidden:
5 fees = 3 missing + 1 blank + `'free'` · 4 ages = 3 missing + the impossible 230 · 1 date = February 30.
(`COUNT(*) FILTER (WHERE …)` counts only the rows that pass the condition.)

---

# 👓 `CREATE VIEW`: a Saved Query

A **view** stores the **query**, not the data: it is recomputed every time you read it.

```sql
CREATE OR REPLACE VIEW silver.members_by_city_plan AS
SELECT city, plan, COUNT(*) AS member_rows, ROUND(AVG(age), 1) AS avg_age
FROM silver.members
GROUP BY city, plan;

SELECT * FROM silver.members_by_city_plan ORDER BY city, plan;
```

<!-- RESULT -->

| city          | plan    | member_rows | avg_age |
|---------------|---------|------------:|--------:|
| San Francisco | Annual  |           5 |    40.0 |
| San Francisco | Monthly |           6 |    45.3 |
| San Francisco | Unknown |           1 |    60.0 |
| San Jose      | Annual  |           6 |    43.4 |
| San Jose      | Monthly |           9 |    41.9 |
| San Jose      | Unknown |           1 |    68.0 |
| Santa Clara   | Annual  |           7 |    35.0 |
| Santa Clara   | Monthly |           7 |    39.6 |
| Santa Clara   | Unknown |           1 |    38.0 |

*(9 rows)*

<!-- /RESULT -->

⚠️ The counts add up to **43 rows, not 40 members**: 103, 115 and 128 are still counted twice (103 even in two cities). Part 2 fixes it.

| | Table (`CREATE TABLE AS`) | View (`CREATE VIEW`) |
|---|---|---|
| Stores | the rows | the query |
| Speed | fast to read | recomputed each time |
| Medallion use | Bronze, Silver, Gold facts/dims | Gold reports, checks |

---

# 🧰 Cheat Sheet (Part 1)

| Problem in Bronze | Silver fix |
|---|---|
| NULL needs a default | `COALESCE(col, 'Unknown')` |
| Blank / `'N/A'` should be NULL | `NULLIF(TRIM(col), '')` · `NULLIF(col, 'N/A')` |
| Divide by zero | `x / NULLIF(n, 0)` |
| Extra spaces, mixed case | `TRIM`, `UPPER`, `LOWER` |
| Unwanted characters | `REPLACE(col, '$', '')` |
| Many spellings of one value | `CASE … WHEN … IN (…) THEN … ELSE 'Unknown' END` |
| Text → number / date | `TRY_CAST(col AS INTEGER / DECIMAL(p,s) / DATE)` (+ count the NULLs) |
| Compare computed money | `ABS(a - b) > 0.01` (a tolerance, not `=`) |
| Impossible values | `CASE WHEN col BETWEEN lo AND hi THEN col END` |
| Keep bad rows visible | `dq_issue` column with `concat_ws` |
| Save a layer | `CREATE SCHEMA` · `CREATE OR REPLACE TABLE … AS` · `CREATE VIEW` |

---

# ✍️ Your Turn

- Every query above, live: the notebook **`lecture_notes_03_cleaning_one_table.py`** (`marimo edit lecture_notes_03_cleaning_one_table.py`, in this folder).
- Then practice: **`exercises_03_cleaning_one_table.py`**: **6 short exercises** (solutions at the end).

**Next week (Part 2):** read **many** files at once, parse dates in different formats,
remove duplicates (`QUALIFY`), find orphans (`LEFT JOIN … IS NULL`) and reconcile (`EXCEPT`).
