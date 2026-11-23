# SQL Toolkit, Part 1 — Exercises (with solutions)

Practice for [the Part 1 slides](week01_slides_3_sql_toolkit_part1.md), on the same `data/members.csv`.
The notebook [`sql_toolkit_part1_exercises.py`](sql_toolkit_part1_exercises.py) (`marimo edit sql_toolkit_part1_exercises.py`) has these exercises
with an empty cell after each one and the solutions at the end: try each one before you look.

Setup (the Bronze table and the `silver` schema from the slides; the exercises notebook runs them first):

```sql
CREATE OR REPLACE TABLE raw_members AS
SELECT * FROM read_csv('data/members.csv', all_varchar = true);

CREATE SCHEMA IF NOT EXISTS silver;
```

## Exercise 1 — Missing or blank?

How many members have an `email` that is **NULL or blank**? Answer with one query and one number.

```sql
SELECT COUNT(*) AS no_email
FROM raw_members
WHERE NULLIF(TRIM(email), '') IS NULL;
```

<!-- RESULT -->

| no_email |
|---------:|
|        2 |

*(1 row)*

<!-- /RESULT -->

`NULLIF(TRIM(email), '')` turns the blank into NULL, so one `IS NULL` test finds both kinds.

## Exercise 2 — Make hidden spaces visible

List every distinct raw `city` value as `'[' || city || ']'` with its `LENGTH`. Which values have spaces at the ends?

```sql
SELECT DISTINCT '[' || city || ']' AS city_shown, LENGTH(city) AS len
FROM raw_members
WHERE city <> TRIM(city)
ORDER BY city_shown;
```

<!-- RESULT -->

| city_shown       | len |
|------------------|----:|
| [ San Jose]      |   9 |
| [SANTA CLARA ]   |  12 |
| [San Francisco ] |  14 |

*(3 rows)*

<!-- /RESULT -->

`city <> TRIM(city)` is true only when trimming changes something.

## Exercise 3 — What did `TRY_CAST` hide?

List the members whose `monthly_fee` is **not NULL** in Bronze but becomes NULL after
`TRY_CAST(REPLACE(TRIM(monthly_fee), '$', '') AS DECIMAL(6, 2))`.

```sql
SELECT member_id, '[' || monthly_fee || ']' AS raw_fee
FROM raw_members
WHERE monthly_fee IS NOT NULL
  AND TRY_CAST(REPLACE(TRIM(monthly_fee), '$', '') AS DECIMAL(6, 2)) IS NULL
ORDER BY member_id;
```

<!-- RESULT -->

| member_id | raw_fee |
|-----------|---------|
| 114       | [ ]     |
| 129       | [free]  |

*(2 rows)*

<!-- /RESULT -->

These are the values a business rule must decide about. The 3 NULL fees were already missing in Bronze.

## Exercise 4 — Write a business rule

The bike-share office says: **`'free'` means 0.00**; every other bad fee stays unknown (NULL).
Write the cleaned fee and show how many members get each fee.

```sql
SELECT CASE WHEN LOWER(TRIM(monthly_fee)) = 'free' THEN 0.00
            ELSE TRY_CAST(REPLACE(TRIM(monthly_fee), '$', '') AS DECIMAL(6, 2))
       END      AS fee,
       COUNT(*) AS n
FROM raw_members
GROUP BY fee
ORDER BY fee NULLS LAST;
```

<!-- RESULT -->

|   fee |  n |
|------:|---:|
|  0.00 |  1 |
|  9.50 | 17 |
| 15.00 | 21 |
|  NULL |  4 |

*(4 rows)*

<!-- /RESULT -->

The rule comes **first** in the `CASE`; everything else falls through to `TRY_CAST`.

## Exercise 5 — 🐞 Debug it: a default that lies

A teammate wants "the average age of our members" and writes:

```sql
SELECT ROUND(AVG(COALESCE(TRY_CAST(age AS INTEGER), 0)), 1) AS avg_age
FROM raw_members;
```

<!-- RESULT -->

| avg_age |
|--------:|
|    43.4 |

*(1 row)*

<!-- /RESULT -->

The query runs, but the answer is wrong. Why? Fix it (keep only ages from 16 to 100).

```sql
SELECT ROUND(AVG(CASE WHEN TRY_CAST(age AS INTEGER) BETWEEN 16 AND 100
                      THEN TRY_CAST(age AS INTEGER) END), 1) AS avg_age,
       COUNT(*) - COUNT(CASE WHEN TRY_CAST(age AS INTEGER) BETWEEN 16 AND 100
                             THEN 1 END)                     AS ages_unknown
FROM raw_members;
```

<!-- RESULT -->

| avg_age | ages_unknown |
|--------:|-------------:|
|    42.0 |            4 |

*(1 row)*

<!-- /RESULT -->

`COALESCE(…, 0)` turns the 3 unknown ages into 0-year-olds, and nothing removes the 230-year-old. Here the two errors
almost cancel out (43.4 vs 42.0), which is exactly why this bug is hard to spot. Defaults are for **labels** (`'Unknown'`),
not for **measures**: leave an unknown number NULL, so `AVG` skips it, and report how many were unknown (4: 3 missing + 1 impossible).

## Exercise 6 — Your first Silver table

In schema `silver` (created in the slides), create table `silver.member_contacts` with three columns: `member_id` (INTEGER),
`full_name` (trimmed) and `email` (trimmed, lower case, `'unknown'` when NULL or blank).
Then show the 3 rows whose email had a problem in Bronze (NULL, blank or upper case).

```sql
CREATE OR REPLACE TABLE silver.member_contacts AS
SELECT DISTINCT
       TRY_CAST(member_id AS INTEGER)                        AS member_id,
       TRIM(full_name)                                       AS full_name,
       LOWER(COALESCE(NULLIF(TRIM(email), ''), 'unknown'))   AS email
FROM raw_members;

SELECT c.*
FROM silver.member_contacts AS c
JOIN raw_members AS r ON c.member_id = TRY_CAST(r.member_id AS INTEGER)
WHERE r.email IS NULL OR TRIM(r.email) = '' OR r.email <> LOWER(r.email)
ORDER BY c.member_id;
```

<!-- RESULT -->

| member_id | full_name  | email                   |
|----------:|------------|-------------------------|
|       108 | Rosa Silva | unknown                 |
|       121 | Rosa Smith | unknown                 |
|       133 | Rosa Kim   | rosa.kim133@example.com |

*(3 rows)*

<!-- /RESULT -->

`DISTINCT` removes the 3 members who appear twice in Bronze with the same name and email (40 rows, not 43).
Removing duplicates properly, by keeping the newest row, is Part 2.
