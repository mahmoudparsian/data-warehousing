# SQL Toolkit, Part 2 — Exercises (with solutions)

Practice for [the Part 2 slides](lecture_notes_03_combine_dedup_reconcile.md), on the same files in `data/`.
The notebook [`exercises_03_combine_dedup_reconcile.py`](exercises_03_combine_dedup_reconcile.py) (`marimo edit exercises_03_combine_dedup_reconcile.py`) has these exercises
with an empty cell after each one and the solutions at the end: try each one before you look.

Setup (the tables from the slides; the exercises notebook runs them first):

```sql
CREATE OR REPLACE TABLE bronze_rentals AS
SELECT * EXCLUDE (filename),
       filename          AS _source_file,
       current_timestamp AS _loaded_at
FROM read_csv('data/rentals_*.csv', all_varchar = true, union_by_name = true, filename = true);

CREATE SCHEMA IF NOT EXISTS silver;

CREATE OR REPLACE TABLE silver.members AS
SELECT TRY_CAST(member_id AS INTEGER)                         AS member_id,
       CASE LOWER(TRIM(plan)) WHEN 'annual'  THEN 'Annual'
                              WHEN 'monthly' THEN 'Monthly'
                              ELSE 'Unknown' END              AS plan,
       TRY_CAST(updated_at AS TIMESTAMP)                      AS updated_at
FROM read_csv('data/members.csv', all_varchar = true)
QUALIFY ROW_NUMBER() OVER (PARTITION BY member_id ORDER BY updated_at DESC) = 1;

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

## Exercise 1 — Lineage

For each `_source_file` in `bronze_rentals`: the number of rows, and the **first** and **last** start time (parsed).
Do the dates match the file names?

```sql
SELECT _source_file,
       COUNT(*) AS n_rows,
       MIN(try_strptime(start_time, ['%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M'])) AS first_start,
       MAX(try_strptime(start_time, ['%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M'])) AS last_start
FROM bronze_rentals
GROUP BY _source_file
ORDER BY _source_file;
```

<!-- RESULT -->

| _source_file             | n_rows | first_start         | last_start          |
|--------------------------|-------:|---------------------|---------------------|
| data/rentals_2026_01.csv |     64 | 2026-01-01 07:20:00 | 2026-01-28 19:16:00 |
| data/rentals_2026_02.csv |     69 | 2026-01-02 09:58:00 | 2026-02-28 21:16:00 |

*(2 rows)*

<!-- /RESULT -->

The February file starts in **January**: it carries the 3 corrected January rentals. Lineage columns let you see that.

## Exercise 2 — Dates: busiest weekday

Using `silver.rentals`, count the rides per weekday (`dayname(start_ts)`), busiest first. Leave out rides with no start time.

```sql
SELECT dayname(start_ts) AS weekday, COUNT(*) AS rides
FROM silver.rentals
WHERE start_ts IS NOT NULL
GROUP BY weekday
ORDER BY rides DESC, weekday;
```

<!-- RESULT -->

| weekday   | rides |
|-----------|------:|
| Sunday    |    24 |
| Thursday  |    23 |
| Saturday  |    17 |
| Wednesday |    17 |
| Monday    |    16 |
| Tuesday   |    16 |
| Friday    |    11 |

*(7 rows)*

<!-- /RESULT -->

## Exercise 3 — What changed for the duplicated members?

In the raw `members.csv`, list every row of the members who appear more than once, with `plan`, `city` and `updated_at`, oldest first.

```sql
SELECT member_id, plan, city, updated_at
FROM read_csv('data/members.csv', all_varchar = true)
WHERE member_id IN (SELECT member_id
                    FROM read_csv('data/members.csv', all_varchar = true)
                    GROUP BY member_id
                    HAVING COUNT(*) > 1)
ORDER BY member_id, updated_at;
```

<!-- RESULT -->

| member_id | plan    | city          | updated_at          |
|-----------|---------|---------------|---------------------|
| 103       | monthly | SANTA CLARA   | 2025-10-21 09:00:00 |
| 103       | Annual  | San Francisco | 2026-01-20 18:30:00 |
| 115       | Annual  | Santa Clara   | 2025-01-03 09:00:00 |
| 115       | Monthly | Santa Clara   | 2026-01-20 18:30:00 |
| 128       | Monthly |  San Jose     | 2025-04-16 09:00:00 |
| 128       | Annual  | San Jose      | 2026-01-20 18:30:00 |

*(6 rows)*

<!-- /RESULT -->

Each member changed plan or city on 2026-01-20. Silver keeps the newer row; the history is lost
(week 4: slowly changing dimensions keep it).

## Exercise 4 — 🐞 Debug it: the old price wins

A teammate deduplicates the rentals like this and checks the 3 corrected rentals:

```sql
SELECT rental_id, price, _source_file
FROM bronze_rentals
WHERE rental_id IN ('5004', '5028', '5045')
QUALIFY ROW_NUMBER() OVER (PARTITION BY rental_id ORDER BY _source_file) = 1
ORDER BY rental_id;
```

<!-- RESULT -->

| rental_id | price | _source_file             |
|-----------|-------|--------------------------|
| 5004      | 4.00  | data/rentals_2026_01.csv |
| 5028      | 2.90  | data/rentals_2026_01.csv |
| 5045      | 4.80  | data/rentals_2026_01.csv |

*(3 rows)*

<!-- /RESULT -->

The query runs, but all 3 prices are the **old** January prices. Fix it.

```sql
SELECT rental_id, price, _source_file
FROM bronze_rentals
WHERE rental_id IN ('5004', '5028', '5045')
QUALIFY ROW_NUMBER() OVER (PARTITION BY rental_id ORDER BY _source_file DESC) = 1
ORDER BY rental_id;
```

<!-- RESULT -->

| rental_id | price | _source_file             |
|-----------|-------|--------------------------|
| 5004      | 2.00  | data/rentals_2026_02.csv |
| 5028      | 4.10  | data/rentals_2026_02.csv |
| 5045      | 0.00  | data/rentals_2026_02.csv |

*(3 rows)*

<!-- /RESULT -->

`ORDER BY` without `DESC` sorts oldest first, so `rn = 1` is the **oldest** copy. "Newest wins" needs `DESC`.

## Exercise 5 — Orphans with `NOT EXISTS`

Count the rentals in `bronze_rentals` whose `member_id` has **no** match in `silver.members`, using `NOT EXISTS`.
Then count only the real orphans (a `member_id` is given, but unknown).

```sql
SELECT COUNT(*)                                     AS no_match,
       COUNT(*) FILTER (WHERE r.member_id IS NOT NULL) AS real_orphans
FROM bronze_rentals AS r
WHERE NOT EXISTS (SELECT 1
                  FROM silver.members AS m
                  WHERE m.member_id = TRY_CAST(r.member_id AS INTEGER));
```

<!-- RESULT -->

| no_match | real_orphans |
|---------:|-------------:|
|        7 |            3 |

*(1 row)*

<!-- /RESULT -->

Same answer as the `LEFT JOIN … IS NULL` slide: 7 rows without a match, 4 guests + 3 real orphans.

## Exercise 6 — A first Gold-style result

Revenue and rides per **month** and **plan**, from `silver.rentals` joined to `silver.members`.
Leave out flagged rows (`dq_issue <> ''`); guests (no `member_id`) get the plan `'Guest'`.

```sql
SELECT strftime(r.start_ts, '%Y-%m')   AS month,
       COALESCE(m.plan, 'Guest')        AS plan,
       COUNT(*)                         AS rides,
       SUM(r.price)                     AS revenue
FROM silver.rentals AS r
LEFT JOIN silver.members AS m ON r.member_id = m.member_id
WHERE r.dq_issue = ''
GROUP BY ALL
ORDER BY month, plan;
```

<!-- RESULT -->

| month   | plan    | rides | revenue |
|---------|---------|------:|--------:|
| 2026-01 | Annual  |    26 |  138.50 |
| 2026-01 | Guest   |     2 |   11.50 |
| 2026-01 | Monthly |    27 |  142.90 |
| 2026-01 | Unknown |     1 |    4.10 |
| 2026-02 | Annual  |    24 |  129.80 |
| 2026-02 | Guest   |     2 |    7.60 |
| 2026-02 | Monthly |    33 |  174.30 |
| 2026-02 | Unknown |     2 |    6.40 |

*(8 rows)*

<!-- /RESULT -->

Bronze (raw files) → Silver (typed, deduplicated, flagged) → this kind of query is what the **Gold** layer serves.
