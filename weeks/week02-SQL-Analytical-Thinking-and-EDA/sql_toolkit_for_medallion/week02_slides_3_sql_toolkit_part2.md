---
marp: true
title: Week 2 — SQL Toolkit for the Medallion Architecture, Part 2 (Combine, Parse, Deduplicate, Reconcile)
paginate: true
theme: default
class: lead
---

# Week 2 — SQL Toolkit, Part 2
## Getting Ready for the Medallion Architecture: Combine · Parse · Deduplicate · Reconcile

many files · dates in many formats · duplicates (`QUALIFY`) · orphans · reconciliation

---

# 🎯 From One Table to a Pipeline

**Part 1 (week 1):** clean **one** table: NULL defaults, `TRIM`/`UPPER`, `CASE`, `TRY_CAST`, `CREATE SCHEMA / TABLE / VIEW`.

**Part 2 (today):** real data arrives as **many files**, again and again:

| Problem | Today's tool |
|---|---|
| A new file every month, columns change | `read_csv('*.csv', union_by_name = true, filename = true)` |
| Dates written in different formats | `strptime` / `try_strptime`, `date_trunc`, `strftime` |
| The same row arrives twice, or corrected later | `ROW_NUMBER()` + `QUALIFY` |
| A rental points to a member we don't know | `LEFT JOIN … IS NULL`, `NOT EXISTS` |
| "Did we lose any rows?" | reconcile: counts, `EXCEPT` |

Week 3 (ETL) and weeks 5–9 (Bronze → Silver → Gold) use **all** of these.

---

# 🚲 Our Data: Bike-Share Rentals, Two Monthly Files

`data/members.csv` (Part 1) + `data/rentals_2026_01.csv` + `data/rentals_2026_02.csv`.

```sql
SELECT * FROM read_csv('data/rentals_2026_01.csv', all_varchar = true) LIMIT 3;
```

<!-- RESULT -->

| rental_id | member_id | bike_id | start_station | start_time          | duration_min | price |
|-----------|-----------|---------|---------------|---------------------|--------------|-------|
| 5001      | 109       | B030    | SCU Campus    | 2026-01-01 07:20:00 | 58           | 7.30  |
| 5002      | 103       | B025    | Civic Center  | 2026-01-01 15:44:00 | 57           | 7.20  |
| 5003      | 111       | B024    | Caltrain SF   | 2026-01-01 20:26:00 | 48           | 6.30  |

*(3 rows)*

<!-- /RESULT -->

```sql
SELECT * FROM read_csv('data/rentals_2026_02.csv', all_varchar = true) LIMIT 3;
```

<!-- RESULT -->

| rental_id | start_time       | member_id | start_station | bike_id | bike_type | price | duration_min |
|-----------|------------------|-----------|---------------|---------|-----------|-------|--------------|
| 5101      | 02/01/2026 10:17 | 111       | Santana Row   | B058    | classic   | 4.00  | 25           |
| 5102      | 02/01/2026 14:57 | 133       | Diridon       | B048    | classic   | 8.80  | 73           |
| 5103      | 02/02/2026 06:38 | 103       | Market St     | B038    | classic   | 7.70  | 62           |

*(3 rows)*

<!-- /RESULT -->

👉 February: **different column order**, a **new column** `bike_type`, and a **different date format**.

---

# Part A — Read Many Files at Once

A `*` in the file name reads every matching file. Two options matter:

```sql
SELECT
  (SELECT COUNT(*) FROM (DESCRIBE SELECT * FROM
     read_csv('data/rentals_*.csv', all_varchar = true)))                        AS columns_default,
  (SELECT COUNT(*) FROM (DESCRIBE SELECT * FROM
     read_csv('data/rentals_*.csv', all_varchar = true, union_by_name = true)))  AS columns_by_name;
```

<!-- RESULT -->

| columns_default | columns_by_name |
|----------------:|----------------:|
|               7 |               8 |

*(1 row)*

<!-- /RESULT -->

- Without `union_by_name = true`, the new column `bike_type` is **silently dropped**.
- With it, columns are matched **by name**; a column missing from a file is NULL there (January has no `bike_type`).
- `filename = true` adds the **source file** of every row: free **lineage**.

---

# 🥉 The Bronze Table

```sql
CREATE OR REPLACE TABLE bronze_rentals AS
SELECT * EXCLUDE (filename),
       filename          AS _source_file,
       current_timestamp AS _loaded_at
FROM read_csv('data/rentals_*.csv', all_varchar = true, union_by_name = true, filename = true);

SELECT _source_file, COUNT(*) AS n_rows, COUNT(bike_type) AS n_bike_type
FROM bronze_rentals
GROUP BY _source_file
ORDER BY _source_file;
```

<!-- RESULT -->

| _source_file             | n_rows | n_bike_type |
|--------------------------|-------:|------------:|
| data/rentals_2026_01.csv |     64 |           0 |
| data/rentals_2026_02.csv |     69 |          69 |

*(2 rows)*

<!-- /RESULT -->

`SELECT * EXCLUDE (col)` = every column except `col`. Lineage columns start with `_` (as in weeks 6–9).

---

# ➕ `UNION` vs `UNION ALL` vs `UNION ALL BY NAME`

```sql
SELECT 'UNION' AS kind, COUNT(*) AS n_rows
FROM (SELECT 'Diridon' AS station, 5 AS rides UNION     SELECT 'Diridon', 5)
UNION ALL
SELECT 'UNION ALL', COUNT(*)
FROM (SELECT 'Diridon' AS station, 5 AS rides UNION ALL SELECT 'Diridon', 5);
```

<!-- RESULT -->

| kind      | n_rows |
|-----------|-------:|
| UNION     |      1 |
| UNION ALL |      2 |

*(2 rows)*

<!-- /RESULT -->

```sql
SELECT 'Diridon' AS station, 5 AS rides
UNION ALL         SELECT 7 AS rides, 'Market St' AS station    -- by position: wrong!
UNION ALL BY NAME SELECT 9 AS rides, 'Civic Center' AS station; -- by name: right
```

<!-- RESULT -->

| station      | rides     |
|--------------|-----------|
| Diridon      | 5         |
| 7            | Market St |
| Civic Center | 9         |

*(3 rows)*

<!-- /RESULT -->

- `UNION` **removes** duplicate rows: never use it to stack data you still have to check. Use `UNION ALL`.
- Plain `UNION ALL` matches columns **by position**: `7` became a station name, **without an error**.

---

# Part B — Dates in Many Formats

First **profile** the formats (Bronze is text, so `LIKE` works):

```sql
SELECT CASE WHEN start_time LIKE '____-__-__ __:__:__' THEN 'YYYY-MM-DD hh:mm:ss'
            WHEN start_time LIKE '__/__/____ __:__'    THEN 'MM/DD/YYYY hh:mm'
            ELSE 'other' END AS format,
       _source_file,
       COUNT(*)              AS n
FROM bronze_rentals
GROUP BY ALL
ORDER BY _source_file, format;
```

<!-- RESULT -->

| format              | _source_file             |  n |
|---------------------|--------------------------|---:|
| YYYY-MM-DD hh:mm:ss | data/rentals_2026_01.csv | 64 |
| MM/DD/YYYY hh:mm    | data/rentals_2026_02.csv | 69 |

*(2 rows)*

<!-- /RESULT -->

In `LIKE`, `_` = exactly one character, `%` = any text.

---

# 🕰️ `strptime`: Text → Timestamp with a Format

| Code | Means | Example |
|---|---|---|
| `%Y` | 4-digit year | 2026 |
| `%m` / `%d` | month / day (2 digits) | 02 / 15 |
| `%H` / `%M` / `%S` | hour (00–23) / minute / second | 14 / 05 / 00 |

```sql
SELECT strptime('2026-01-15 08:30:00', '%Y-%m-%d %H:%M:%S') AS iso_text,
       strptime('01/15/2026 08:30',    '%m/%d/%Y %H:%M')    AS us_text;
```

<!-- RESULT -->

| iso_text            | us_text             |
|---------------------|---------------------|
| 2026-01-15 08:30:00 | 2026-01-15 08:30:00 |

*(1 row)*

<!-- /RESULT -->

`strptime` **fails** if the text does not match; `try_strptime` returns **NULL**, and accepts a **list** of formats (the first that fits wins).

---

# 🧩 Parse Every Format in One Expression

```sql
SELECT start_time,
       try_strptime(start_time, ['%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M']) AS start_ts,
       _source_file
FROM bronze_rentals
WHERE try_strptime(start_time, ['%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M']) IS NULL;
```

<!-- RESULT -->

| start_time          | start_ts | _source_file             |
|---------------------|----------|--------------------------|
| 2026-01-32 08:10:00 | NULL     | data/rentals_2026_01.csv |
| 13/02/2026 25:00    | NULL     | data/rentals_2026_02.csv |

*(2 rows)*

<!-- /RESULT -->

- Only 2 of 133 values fail: January 32 and hour 25 do not exist. They stay NULL and get **flagged**.
- Same result, older style: `COALESCE(try_strptime(x, '%Y-%m-%d %H:%M:%S'), try_strptime(x, '%m/%d/%Y %H:%M'))`. Add `::DATE` to drop the time.
- ⚠️ `02/03/2026`: February 3 or March 2? A format list cannot know. Ask the source owner, write the format down per source.

---

# 📆 Working with Timestamps

```sql
WITH typed AS (
  SELECT try_strptime(start_time, ['%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M']) AS start_ts,
         TRY_CAST(duration_min AS INTEGER)                                AS duration_min
  FROM bronze_rentals
)
SELECT date_trunc('month', start_ts)                              AS month_start,
       strftime(start_ts, '%Y-%m')                                AS month_label,
       COUNT(*)                                                   AS n_rows,
       MAX(start_ts + duration_min * INTERVAL 1 MINUTE)           AS last_ride_end
FROM typed
GROUP BY ALL
ORDER BY month_start NULLS LAST;
```

<!-- RESULT -->

| month_start         | month_label | n_rows | last_ride_end       |
|---------------------|-------------|-------:|---------------------|
| 2026-01-01 00:00:00 | 2026-01     |     66 | 2026-01-28 19:43:00 |
| 2026-02-01 00:00:00 | 2026-02     |     65 | 2026-02-28 21:48:00 |
| NULL                | NULL        |      2 | NULL                |

*(3 rows)*

<!-- /RESULT -->

Bronze still holds duplicates (Part C), so these are **rows**, not yet rides.
`date_trunc` → a date you can sort and join; `strftime` → **text** for labels (ts → text; `strptime` is text → ts).
Also useful: `year(ts)`, `quarter(ts)`, `month(ts)`, `monthname(ts)`, `dayname(ts)`, `hour(ts)`, `date_diff('minute', ts1, ts2)`.

---

# Part C — Two Kinds of Duplicates

```sql
SELECT COUNT(*)                                    AS bronze_rows,
       COUNT(DISTINCT rental_id)                   AS distinct_rentals,
       COUNT(*) - COUNT(DISTINCT rental_id)        AS extra_rows
FROM bronze_rentals;
```

<!-- RESULT -->

| bronze_rows | distinct_rentals | extra_rows |
|------------:|-----------------:|-----------:|
|         133 |              126 |          7 |

*(1 row)*

<!-- /RESULT -->

1. **Exact duplicates**: every column is the same (a file was partly exported twice).
2. **Same key, different values**: a later file **corrects** an earlier row.

---

# 🔍 Find Both Kinds

```sql
SELECT rental_id, _source_file, start_time, price, COUNT(*) AS copies
FROM bronze_rentals
WHERE rental_id IN (SELECT rental_id FROM bronze_rentals
                    GROUP BY rental_id HAVING COUNT(*) > 1)
GROUP BY ALL
ORDER BY rental_id, _source_file;
```

<!-- RESULT -->

| rental_id | _source_file             | start_time          | price | copies |
|-----------|--------------------------|---------------------|-------|-------:|
| 5004      | data/rentals_2026_01.csv | 2026-01-02 09:58:00 | 4.00  |      1 |
| 5004      | data/rentals_2026_02.csv | 01/02/2026 09:58    | 2.00  |      1 |
| 5010      | data/rentals_2026_01.csv | 2026-01-04 16:32:00 | 6.40  |      2 |
| 5011      | data/rentals_2026_01.csv | 2026-01-05 06:25:00 | 4.70  |      2 |
| 5012      | data/rentals_2026_01.csv | 2026-01-06 07:41:00 | 4.90  |      2 |
| 5028      | data/rentals_2026_01.csv | 2026-01-15 18:36:00 | 2.90  |      1 |
| 5028      | data/rentals_2026_02.csv | 01/15/2026 18:36    | 4.10  |      1 |
| 5045      | data/rentals_2026_01.csv | 2026-01-22 20:35:00 | 4.80  |      1 |
| 5045      | data/rentals_2026_02.csv | 01/22/2026 20:35    | 0.00  |      1 |
| 5053      | data/rentals_2026_01.csv | 2026-01-25 09:03:00 | 3.10  |      2 |

*(10 rows)*

<!-- /RESULT -->

- `copies = 2` in one file: **exact** duplicates.
- Same `rental_id` in **both** files with a different `price`: February **corrected** January. Which row wins?

---

# 🏆 Keep the Newest Row per Key: `ROW_NUMBER()` …

```sql
SELECT rental_id, _source_file, price,
       ROW_NUMBER() OVER (PARTITION BY rental_id ORDER BY _source_file DESC) AS rn
FROM bronze_rentals
WHERE rental_id IN ('5004', '5010')
ORDER BY rental_id, rn;
```

<!-- RESULT -->

| rental_id | _source_file             | price | rn |
|-----------|--------------------------|-------|---:|
| 5004      | data/rentals_2026_02.csv | 2.00  |  1 |
| 5004      | data/rentals_2026_01.csv | 4.00  |  2 |
| 5010      | data/rentals_2026_01.csv | 6.40  |  1 |
| 5010      | data/rentals_2026_01.csv | 6.40  |  2 |

*(4 rows)*

<!-- /RESULT -->

- `PARTITION BY` the **key**, `ORDER BY` "newest first" (here: the later file name). Keep `rn = 1`.
- In real pipelines, order by a load time or an `updated_at` column.
- No such column? Keep the **most complete** copy: `ORDER BY (price IS NULL)::INT + (member_id IS NULL)::INT` (`TRUE::INT` = 1).

---

# … and Filter It with `QUALIFY`

`QUALIFY` filters on a window function, like `HAVING` filters on an aggregate:

```sql
SELECT COUNT(*) AS rows_kept
FROM (
  SELECT *
  FROM bronze_rentals
  QUALIFY ROW_NUMBER() OVER (PARTITION BY rental_id ORDER BY _source_file DESC) = 1
);
```

<!-- RESULT -->

| rows_kept |
|----------:|
|       126 |

*(1 row)*

<!-- /RESULT -->

Without `QUALIFY`, put the `ROW_NUMBER()` in a subquery and add `WHERE rn = 1`: same result, more typing.
Exact duplicates disappear too: they share the key, so only one copy gets `rn = 1`.

---

# 🧑 Same Pattern for Members (from Part 1)

Three members appear twice in `members.csv`. Keep the row with the **newest** `updated_at`:

```sql
CREATE SCHEMA IF NOT EXISTS silver;

CREATE OR REPLACE TABLE silver.members AS
SELECT TRY_CAST(member_id AS INTEGER)                         AS member_id,
       CASE LOWER(TRIM(plan)) WHEN 'annual'  THEN 'Annual'
                              WHEN 'monthly' THEN 'Monthly'
                              ELSE 'Unknown' END              AS plan,
       TRY_CAST(updated_at AS TIMESTAMP)                      AS updated_at
FROM read_csv('data/members.csv', all_varchar = true)
QUALIFY ROW_NUMBER() OVER (PARTITION BY member_id ORDER BY updated_at DESC) = 1;

SELECT COUNT(*) AS members, COUNT(DISTINCT member_id) AS distinct_ids FROM silver.members;
```

<!-- RESULT -->

| members | distinct_ids |
|--------:|-------------:|
|      40 |           40 |

*(1 row)*

<!-- /RESULT -->

---

# Part D — Orphans: Rentals Without a Known Member

```sql
SELECT CASE WHEN r.member_id IS NULL THEN 'guest ride (no member_id)'
            ELSE 'orphan (member_id not in members)' END AS problem,
       COUNT(*)                                           AS n,
       string_agg(DISTINCT r.member_id, ', ' ORDER BY r.member_id) AS member_ids
FROM bronze_rentals AS r
LEFT JOIN silver.members AS m
       ON TRY_CAST(r.member_id AS INTEGER) = m.member_id
WHERE m.member_id IS NULL
GROUP BY problem
ORDER BY problem;
```

<!-- RESULT -->

| problem                           | n | member_ids |
|-----------------------------------|--:|------------|
| guest ride (no member_id)         | 4 | NULL       |
| orphan (member_id not in members) | 3 | 998, 999   |

*(2 rows)*

<!-- /RESULT -->

- **`LEFT JOIN … WHERE right.key IS NULL`** = rows with **no match** (an *anti-join*). `INNER JOIN` would drop them **silently**.
- Same question with `NOT EXISTS (SELECT 1 FROM silver.members m WHERE m.member_id = …)`: try it in the exercises.

---

# 🏷️ Keep Orphans, Label Them

```sql
SELECT COALESCE(m.plan,
                CASE WHEN r.member_id IS NULL THEN 'Guest' ELSE 'Unknown member' END) AS plan,
       COUNT(*) AS rides
FROM bronze_rentals AS r
LEFT JOIN silver.members AS m
       ON TRY_CAST(r.member_id AS INTEGER) = m.member_id
GROUP BY ALL
ORDER BY rides DESC, plan;
```

<!-- RESULT -->

| plan           | rides |
|----------------|------:|
| Monthly        |    67 |
| Annual         |    55 |
| Guest          |     4 |
| Unknown        |     4 |
| Unknown member |     3 |

*(5 rows)*

<!-- /RESULT -->

Every ride is counted **once**, in a named group. In week 8 the Gold layer gives such rows an "Unknown" dimension member.

---

# Part E — Data-Quality Checks in One Query

```sql
SELECT COUNT(*)                                                                      AS rows,
       COUNT(*) FILTER (WHERE try_strptime(start_time,
                         ['%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M']) IS NULL)           AS bad_time,
       COUNT(*) FILTER (WHERE TRY_CAST(price AS DECIMAL(6, 2)) IS NULL)              AS price_missing,
       COUNT(*) FILTER (WHERE TRY_CAST(price AS DECIMAL(6, 2)) < 0)                  AS price_negative,
       COUNT(*) FILTER (WHERE TRY_CAST(duration_min AS INTEGER) <= 0)                AS duration_zero,
       COUNT(*) FILTER (WHERE member_id IS NULL)                                     AS guest_rides
FROM bronze_rentals;
```

<!-- RESULT -->

| rows | bad_time | price_missing | price_negative | duration_zero | guest_rides |
|-----:|---------:|--------------:|---------------:|--------------:|------------:|
|  133 |        2 |             2 |              1 |             1 |           4 |

*(1 row)*

<!-- /RESULT -->

One row = the **data-quality report** of a load. Run it on every new file (week 9 stores it in a log table).

---

# 🥈 The Silver Table: One CTE Pipeline

```sql
CREATE OR REPLACE TABLE silver.rentals AS
WITH typed AS (
  SELECT TRY_CAST(rental_id AS INTEGER)                                         AS rental_id,
         TRY_CAST(member_id AS INTEGER)                                         AS member_id,
         TRIM(start_station)                                                    AS start_station,
         try_strptime(start_time, ['%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M'])      AS start_ts,
         TRY_CAST(duration_min AS INTEGER)                                      AS duration_min,
         TRY_CAST(NULLIF(TRIM(price), '') AS DECIMAL(6, 2))                     AS price,
         COALESCE(bike_type, 'unknown')                                         AS bike_type,
         _source_file
  FROM bronze_rentals
),
deduped AS (
  SELECT * FROM typed
  QUALIFY ROW_NUMBER() OVER (PARTITION BY rental_id ORDER BY _source_file DESC) = 1
)
SELECT d.*,
       concat_ws(', ',
         CASE WHEN d.start_ts IS NULL                          THEN 'bad start time' END,
         CASE WHEN d.price IS NULL OR d.price < 0              THEN 'bad price'      END,
         CASE WHEN d.duration_min <= 0                         THEN 'bad duration'   END,
         CASE WHEN d.member_id IS NOT NULL AND m.member_id IS NULL THEN 'unknown member' END
       ) AS dq_issue
FROM deduped AS d
LEFT JOIN silver.members AS m ON d.member_id = m.member_id;
```

Steps in order: **type** → **deduplicate** → **join + flag**. Each CTE does one job, and you can `SELECT` from any of them to debug.

---

# ⚖️ Reconcile: Did We Lose Anything?

```sql
SELECT (SELECT COUNT(*) FROM bronze_rentals)                          AS bronze_rows,
       (SELECT COUNT(*) - COUNT(DISTINCT rental_id) FROM bronze_rentals) AS removed_duplicates,
       COUNT(*)                                                       AS silver_rows,
       COUNT(*) FILTER (WHERE dq_issue <> '')                         AS flagged_rows
FROM silver.rentals;
```

<!-- RESULT -->

| bronze_rows | removed_duplicates | silver_rows | flagged_rows |
|------------:|-------------------:|------------:|-------------:|
|         133 |                  7 |         126 |            9 |

*(1 row)*

<!-- /RESULT -->

```sql
SELECT TRY_CAST(rental_id AS INTEGER) AS rental_id FROM bronze_rentals
EXCEPT
SELECT rental_id FROM silver.rentals;
```

<!-- RESULT -->

| rental_id |
|----------:|

*(0 rows)*

<!-- /RESULT -->

**bronze = silver + removed duplicates**, and `EXCEPT` returns **no** rental that went missing. Then you can trust Silver.

---

# 🧰 Cheat Sheet (Part 2)

| Problem | SQL |
|---|---|
| Read all monthly files, keep new columns | `read_csv('data/x_*.csv', union_by_name = true)` |
| Know where each row came from | `filename = true` → `_source_file`; `current_timestamp AS _loaded_at` |
| Stack two queries | `UNION ALL` (by position) · `UNION ALL BY NAME` · not `UNION` |
| Text → timestamp | `try_strptime(col, ['%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M'])` |
| Timestamp → month / label | `date_trunc('month', ts)` · `strftime(ts, '%Y-%m')` |
| Add minutes | `ts + n * INTERVAL 1 MINUTE` |
| Keep the newest row per key | `QUALIFY ROW_NUMBER() OVER (PARTITION BY key ORDER BY newest DESC) = 1` |
| Rows with no match | `LEFT JOIN … WHERE right.key IS NULL` · `NOT EXISTS` |
| Quality report | `COUNT(*) FILTER (WHERE <problem>)` per problem |
| Nothing lost? | counts in = out + removed · `A EXCEPT B` returns 0 rows |

---

# ✍️ Your Turn

- Every query above, live: the notebook **`week02_slides_3_sql_toolkit_part2.py`** (`marimo edit week02_slides_3_sql_toolkit_part2.py`, in this folder).
- Then practice: **`sql_toolkit_part2_exercises.py`**: **6 short exercises** (solutions at the end).

**Next week (ETL):** you will use Parts 1 and 2 on a messy book-seller file: profile → clean → deduplicate → load → reconcile.
