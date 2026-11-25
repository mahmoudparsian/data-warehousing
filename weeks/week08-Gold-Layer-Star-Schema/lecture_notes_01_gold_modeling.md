---
marp: true
theme: default
paginate: true
size: 16:9
title: Week 8 — Session 1 — Gold Modeling
---

# Week 8 — Session 1
## Gold: From a Clean Silver Table to a Star Schema

Running example: week 7's insurance Silver table (`silver.insurance`, 4 yearly sources, 5,197 rows). Every query runs.
**Lab 8.1** builds the pizza shop's star schema; **Lab 8.2** its KPIs and marts.

---

# ⚙️ Setup: Week 7's Silver Table

The same rules as week 7 (also in [`insurance_silver_week07.sql`](insurance_silver_week07.sql)): conform → deduplicate → reject / flag.

```sql
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;

CREATE OR REPLACE TABLE bronze.insurance AS
SELECT * EXCLUDE (filename),
       regexp_extract(filename, '[^/]+$')                  AS _source_file,
       CAST(regexp_extract(filename, '(\d{4})', 1) AS INT) AS _batch_id,
       current_timestamp                                   AS _ingested_at
FROM read_csv('../week07-Silver-Layer-Cleaning-and-Conforming/data_messy/insurance.*.messy.csv', all_varchar = true, filename = true);

CREATE OR REPLACE MACRO norm_region(r) AS regexp_replace(lower(trim(r)), '[ -]', '', 'g');
CREATE OR REPLACE TABLE silver.map_region AS SELECT * FROM (VALUES
    ('northeast', 'northeast'), ('northwest', 'northwest'),
    ('southeast', 'southeast'), ('southwest', 'southwest')) t(region_key, region);
CREATE OR REPLACE TABLE silver.map_smoker AS SELECT * FROM (VALUES ('yes', 'yes'), ('no', 'no')) t(smoker_key, smoker);
CREATE OR REPLACE TABLE silver.map_gender AS SELECT * FROM (VALUES ('female', 'female'), ('male', 'male'), ('m', 'male')) t(gender_key, gender);

CREATE OR REPLACE TABLE silver.step1_standardized AS
SELECT b._batch_id,
       TRY_CAST(TRY_CAST(b.age AS DOUBLE) AS INTEGER)      AS age,
       COALESCE(g.gender, 'unknown')                       AS gender,
       TRY_CAST(b.bmi AS DECIMAL(5, 2))                    AS bmi,
       TRY_CAST(TRY_CAST(b.children AS DOUBLE) AS INTEGER) AS children,
       COALESCE(s.smoker, 'unknown')                       AS smoker,
       COALESCE(r.region, 'unknown')                       AS region,
       TRY_CAST(b.charges AS DECIMAL(10, 2))               AS charges,
       b.region                                            AS region_raw
FROM bronze.insurance b
LEFT JOIN silver.map_region r ON r.region_key = norm_region(b.region)
LEFT JOIN silver.map_smoker s ON s.smoker_key = lower(trim(b.smoker))
LEFT JOIN silver.map_gender g ON g.gender_key = lower(trim(b.gender));

CREATE OR REPLACE TABLE silver.step2_dedup AS
SELECT * FROM silver.step1_standardized
QUALIFY ROW_NUMBER() OVER (PARTITION BY _batch_id, age, gender, bmi, children, smoker, region, charges ORDER BY region_raw) = 1;

CREATE OR REPLACE TABLE silver.insurance_rejected AS
SELECT *,
       CASE WHEN age IS NULL OR bmi IS NULL OR children IS NULL OR charges IS NULL THEN 'missing value'
            WHEN age NOT BETWEEN 18 AND 100     THEN 'age outside 18-100'
            WHEN bmi NOT BETWEEN 12 AND 70      THEN 'bmi outside 12-70'
            WHEN children NOT BETWEEN 0 AND 10  THEN 'children outside 0-10'
            ELSE 'charges <= 0' END AS reject_reason
FROM silver.step2_dedup
WHERE age IS NULL OR bmi IS NULL OR children IS NULL OR charges IS NULL
   OR age NOT BETWEEN 18 AND 100 OR bmi NOT BETWEEN 12 AND 70
   OR children NOT BETWEEN 0 AND 10 OR charges <= 0;

CREATE OR REPLACE TABLE silver.insurance AS
SELECT _batch_id AS year, age, gender, bmi, children, smoker, region, charges, region_raw,
       gender = 'unknown' AS is_gender_unknown,
       smoker = 'unknown' AS is_smoker_unknown,
       region = 'unknown' AS is_region_unknown
FROM silver.step2_dedup
WHERE NOT (age IS NULL OR bmi IS NULL OR children IS NULL OR charges IS NULL
           OR age NOT BETWEEN 18 AND 100 OR bmi NOT BETWEEN 12 AND 70
           OR children NOT BETWEEN 0 AND 10 OR charges <= 0);

SELECT COUNT(*) AS silver_rows FROM silver.insurance;   -- 5,197
```

<!-- RESULT -->

| silver_rows |
|------------:|
|        5197 |

*(1 row)*

<!-- /RESULT -->

---

# PART 0 — Gold = Shaped for Decisions

- Bronze = what the sources sent · Silver = one trusted row per real thing · **Gold = shaped for the business**
- Gold is built **only from Silver**, and uses Silver's flags **explicitly** (`WHERE NOT is_region_unknown`, or an `unknown` member)
- Gold is not "always aggregated": a star schema keeps the detail; **marts** aggregate for one audience
- BI dashboards, ML and audits are **consumers** of Gold, not extra layers (week 5)

---

# PART 1 — Business-First Modeling

| Wrong order | Right order |
|---|---|
| tables → queries → "what can we answer?" | **questions → KPIs → grain → model → tables** |

The insurer's questions:
1. Which regions and profiles cost the most per policy-holder?
2. How do smokers' charges compare, by age band?
3. How do charges change from 2021 to 2024?

→ measures: `charges`, number of policy-years · dimensions: region, smoker, age band, year

---

# PART 2 — The Star Schema

```text
              dim_age_band
                   |
dim_region — fact_policy_year — dim_smoker
                   |
                 year (a time attribute: the grain is one year)
```

- **Fact** = one row per measured event, with keys + numbers
- **Dimensions** = the words people filter and group by (small, stable, descriptive)

---

# PART 3 — Grain: Write It as a Sentence, Then Test It

**Grain:** one row = **one policy-holder in one year**.

```sql
SELECT COUNT(*) AS rows,
       COUNT(DISTINCT (year, age, gender, bmi, children, smoker, region, charges)) AS distinct_grain_values
FROM silver.insurance;
```

<!-- RESULT -->

| rows | distinct_grain_values |
|-----:|----------------------:|
| 5197 |                  5197 |

*(1 row)*

<!-- /RESULT -->

Equal: Silver already removed the copies (week 7), so the grain holds. There is **no customer id** in the files, so the fact gets a **surrogate key**.
A copy left in Silver would double-count its charges in every total, silently: grain errors don't raise errors.

---

# PART 4 — Additive vs Non-Additive Measures

| Kind | Example here | Rule |
|---|---|---|
| additive | `charges`, number of policy-years | `SUM` across any dimension |
| non-additive | average charges, smoker share, `bmi` | recompute from additive parts: `SUM(charges) / COUNT(*)` |

```sql
WITH by_region AS (SELECT region, AVG(charges) AS avg_charges FROM silver.insurance GROUP BY 1)
SELECT ROUND((SELECT AVG(avg_charges) FROM by_region), 2)       AS avg_of_region_averages,
       ROUND((SELECT SUM(charges) / COUNT(*) FROM silver.insurance), 2) AS true_average;
```

<!-- RESULT -->

| avg_of_region_averages | true_average |
|-----------------------:|-------------:|
|               18872.95 |     18481.91 |

*(1 row)*

<!-- /RESULT -->

$18,872.95 vs $18,481.91: the average of 5 region averages weights the 813-row `unknown` group like the 1,255-row southeast. Store the parts, divide last.

---

# PART 5 — Dimensions

| Good dimension | Bad dimension |
|---|---|
| small, stable, descriptive: region, smoker, age band | one row per event (that is the fact) |
| has an **unknown member** for values Silver flagged | silently drops rows whose value is unknown |

```sql
CREATE SCHEMA IF NOT EXISTS gold;

CREATE OR REPLACE TABLE gold.dim_region AS
SELECT ROW_NUMBER() OVER (ORDER BY region = 'unknown', region) AS region_key, region
FROM (SELECT DISTINCT region FROM silver.insurance);

CREATE OR REPLACE TABLE gold.dim_smoker AS
SELECT ROW_NUMBER() OVER (ORDER BY smoker = 'unknown', smoker) AS smoker_key, smoker
FROM (SELECT DISTINCT smoker FROM silver.insurance);

CREATE OR REPLACE TABLE gold.dim_age_band AS SELECT * FROM (VALUES
    (1, '18-29', 18, 29), (2, '30-44', 30, 44), (3, '45-59', 45, 59), (4, '60+', 60, 100)) t(age_band_key, age_band, age_from, age_to);

SELECT 'dim_region' AS dim, region_key AS key, region AS value FROM gold.dim_region
UNION ALL SELECT 'dim_smoker', smoker_key, smoker FROM gold.dim_smoker
UNION ALL SELECT 'dim_age_band', age_band_key, age_band FROM gold.dim_age_band
ORDER BY dim, key;
```

<!-- RESULT -->

| dim          | key | value     |
|--------------|----:|-----------|
| dim_age_band |   1 | 18-29     |
| dim_age_band |   2 | 30-44     |
| dim_age_band |   3 | 45-59     |
| dim_age_band |   4 | 60+       |
| dim_region   |   1 | northeast |
| dim_region   |   2 | northwest |
| dim_region   |   3 | southeast |
| dim_region   |   4 | southwest |
| dim_region   |   5 | unknown   |
| dim_smoker   |   1 | no        |
| dim_smoker   |   2 | yes       |
| dim_smoker   |   3 | unknown   |

*(12 rows)*

<!-- /RESULT -->

---

# PART 6 — Surrogate Keys (and a Classic Bug)

A surrogate key = a meaningless integer owned by the warehouse: stable, small, fast to join, independent of source spellings
(the spellings were already **conformed** in Silver; a key doesn't fix them).

🐞 A common way to number a dimension, and what it really does:

```sql
SELECT COUNT(*) AS rows_in_dim_region
FROM (SELECT DISTINCT ROW_NUMBER() OVER () AS region_id, region FROM silver.insurance);
```

<!-- RESULT -->

| rows_in_dim_region |
|-------------------:|
|               5197 |

*(1 row)*

<!-- /RESULT -->

5,197 "regions" instead of 5: `ROW_NUMBER()` runs **before** `DISTINCT`, every row gets its own number, so nothing is distinct. Number the **distinct values**
(subquery first, as in Part 5), and order the numbering (`OVER (ORDER BY …)`): `OVER ()` can number differently on every run.

---

# PART 7 — The Fact Table

```sql
CREATE OR REPLACE TABLE gold.fact_policy_year AS
SELECT ROW_NUMBER() OVER (ORDER BY s.year, s.age, s.gender, s.bmi, s.children, s.smoker, s.region, s.charges) AS policy_year_key,
       s.year, r.region_key, k.smoker_key, a.age_band_key,
       s.gender, s.age, s.bmi, s.children,               -- descriptive values kept on the fact (small, used rarely)
       s.charges,                                        -- the measure
       s.is_region_unknown OR s.is_smoker_unknown OR s.is_gender_unknown AS is_flagged
FROM silver.insurance s
JOIN gold.dim_region   r ON r.region = s.region
JOIN gold.dim_smoker   k ON k.smoker = s.smoker
JOIN gold.dim_age_band a ON s.age BETWEEN a.age_from AND a.age_to;

SELECT COUNT(*) AS fact_rows, SUM(charges) AS total_charges, COUNT(*) FILTER (WHERE is_flagged) AS flagged_rows
FROM gold.fact_policy_year;
```

<!-- RESULT -->

| fact_rows | total_charges | flagged_rows |
|----------:|--------------:|-------------:|
|      5197 |   96050494.08 |         1037 |

*(1 row)*

<!-- /RESULT -->

---

# PART 8 — Validate the Fact Against Silver (All Must Pass)

```sql
SELECT 'rows: fact = silver' AS test,
       (SELECT COUNT(*) FROM gold.fact_policy_year) = (SELECT COUNT(*) FROM silver.insurance) AS passed
UNION ALL SELECT 'charges: fact = silver',
       (SELECT SUM(charges) FROM gold.fact_policy_year) = (SELECT SUM(charges) FROM silver.insurance)
UNION ALL SELECT 'no NULL foreign keys',
       (SELECT COUNT(*) FROM gold.fact_policy_year WHERE region_key IS NULL OR smoker_key IS NULL OR age_band_key IS NULL) = 0
UNION ALL SELECT 'surrogate key unique',
       (SELECT COUNT(DISTINCT policy_year_key) FROM gold.fact_policy_year) = (SELECT COUNT(*) FROM gold.fact_policy_year)
UNION ALL SELECT 'every dimension key used once per value',
       (SELECT COUNT(*) FROM gold.dim_region) = (SELECT COUNT(DISTINCT region) FROM gold.dim_region);
```

<!-- RESULT -->

| test                                    | passed |
|-----------------------------------------|--------|
| rows: fact = silver                     | true   |
| charges: fact = silver                  | true   |
| no NULL foreign keys                    | true   |
| surrogate key unique                    | true   |
| every dimension key used once per value | true   |

*(5 rows)*

<!-- /RESULT -->

An inner join to a dimension **drops** fact rows whose key is missing: the row-count test catches it. That is why the dimensions have an `unknown` member.

---

# PART 9 — KPI Engineering: Data + Rules + Context

"Average charges per policy-holder", but which rows?

```sql
SELECT 'all rows (flags included)' AS kpi_definition, COUNT(*) AS policy_years, ROUND(SUM(charges) / COUNT(*), 2) AS avg_charges
FROM gold.fact_policy_year
UNION ALL
SELECT 'known region only', COUNT(*), ROUND(SUM(charges) / COUNT(*), 2)
FROM gold.fact_policy_year f JOIN gold.dim_region r USING (region_key) WHERE r.region <> 'unknown'
UNION ALL
SELECT 'not flagged at all', COUNT(*), ROUND(SUM(charges) / COUNT(*), 2)
FROM gold.fact_policy_year WHERE NOT is_flagged;
```

<!-- RESULT -->

| kpi_definition            | policy_years | avg_charges |
|---------------------------|-------------:|------------:|
| all rows (flags included) |         5197 |    18481.91 |
| known region only         |         4384 |    17094.97 |
| not flagged at all        |         4160 |    17028.39 |

*(3 rows)*

<!-- /RESULT -->

$18,481.91, $17,094.97 or $17,028.39: three honest numbers, three definitions. A KPI is a **written definition** (which rows, which measure, which period), not just a query.

---

# PART 10 — Performance in DuckDB

- DuckDB is **columnar**: a query reads only the columns it needs; there are no indexes to tune for analytics
- Small integer keys make joins and `GROUP BY` cheap; wide text columns stay in the (small) dimensions
- **Materialize** what dashboards ask again and again (marts, Part 13); keep the star for new questions
- Big data: one Parquet file per year/month (`PARTITION_BY`), so a query on 2024 reads only 2024

---

# PART 11 — Case Study: One Outlier, Two Answers

```sql
SELECT ROUND(AVG(x), 2) AS avg_all, ROUND(AVG(x) FILTER (WHERE x < 10000), 2) AS avg_without_outlier,
       MEDIAN(x) AS median_all
FROM (VALUES (100), (200), (300), (10000)) t(x);
```

<!-- RESULT -->

| avg_all | avg_without_outlier | median_all |
|--------:|--------------------:|-----------:|
|  2650.0 |               200.0 |      250.0 |

*(1 row)*

<!-- /RESULT -->

Which is correct? It depends on the **business definition**. If 10,000 is impossible, Silver **rejects** it (week 7). If it is real but rare,
keep it, **flag** it (`is_high_cost`), and let each KPI say whether it includes it, or report the median next to the mean.

---

# PART 12 — Multi-Dimension Query: Star Joins

```sql
SELECT r.region, k.smoker,
       COUNT(*)                         AS policy_years,
       ROUND(SUM(f.charges) / COUNT(*)) AS avg_charges
FROM gold.fact_policy_year f
JOIN gold.dim_region r USING (region_key)
JOIN gold.dim_smoker k USING (smoker_key)
WHERE f.year = 2024 AND k.smoker <> 'unknown'
GROUP BY r.region_key, r.region, k.smoker
ORDER BY r.region_key, k.smoker;
```

<!-- RESULT -->

| region    | smoker | policy_years | avg_charges |
|-----------|--------|-------------:|------------:|
| northeast | no     |          209 |     12977.0 |
| northeast | yes    |           51 |     40101.0 |
| northwest | no     |          214 |     13269.0 |
| northwest | yes    |           50 |     40535.0 |
| southeast | no     |          254 |     13301.0 |
| southeast | yes    |           62 |     38479.0 |
| southwest | no     |          203 |     13073.0 |
| southwest | yes    |           34 |     40400.0 |
| unknown   | no     |          270 |     12982.0 |
| unknown   | yes    |           56 |     38678.0 |

*(10 rows)*

<!-- /RESULT -->

In every region a smoker costs about **3×** a non-smoker in 2024 ($38,479–$40,535 vs $12,977–$13,301): the smoker status matters far more than the region.

---

# PART 13 — Data Marts: Small, Declared Grain, Built from the Star

```sql
CREATE OR REPLACE TABLE gold.mart_region_year AS          -- grain: one row per region per year
SELECT f.year, r.region,
       COUNT(*)                                   AS policy_years,   -- additive parts only:
       SUM(f.charges)                             AS total_charges,  -- the dashboard divides
       COUNT(*) FILTER (WHERE k.smoker = 'yes')   AS smokers
FROM gold.fact_policy_year f
JOIN gold.dim_region r USING (region_key)
JOIN gold.dim_smoker k USING (smoker_key)
GROUP BY ALL;

SELECT (SELECT SUM(total_charges) FROM gold.mart_region_year) = (SELECT SUM(charges) FROM gold.fact_policy_year) AS charges_match,
       (SELECT SUM(policy_years) FROM gold.mart_region_year) = (SELECT COUNT(*) FROM gold.fact_policy_year)     AS rows_match,
       (SELECT COUNT(*) FROM gold.mart_region_year) AS mart_rows;
```

<!-- RESULT -->

| charges_match | rows_match | mart_rows |
|---------------|------------|----------:|
| true          | true       |        20 |

*(1 row)*

<!-- /RESULT -->

20 rows (5 regions × 4 years), totals equal to the fact. Store **parts** (sums, counts), not averages: an `avg_charges` column can't be combined into a yearly or national number. Build a mart when a
question is asked again and again (a dashboard), for **one** audience.

---

# PART 14 — Failure Modes (All Silent)

| Failure | What you see | Test that catches it |
|---|---|---|
| wrong grain / copies | totals a little too high | `COUNT(*)` = `COUNT(DISTINCT grain)` |
| missing dimension key | rows vanish in an inner join | fact rows = Silver rows |
| average of averages | a plausible but wrong KPI | recompute from parts |
| marts that disagree | two dashboards, two numbers | mart totals = fact totals |
| `ROW_NUMBER() OVER ()` keys | keys change between runs | order the numbering |

---

# PART 15 — Design Trade-offs

- **Detail vs simplicity:** the star keeps every policy-year (any new question); marts answer known questions fast
- **Flexibility vs speed:** more dimensions = more ways to slice, more joins
- **Storage vs compute:** materialize a mart, or compute it on the fly from the star (DuckDB is fast enough for 5,197 rows; not for 5 billion)

---

# PART 16 — Exam-Style Questions

1. What happens if the grain is too fine? Too coarse?
2. Why compute KPIs in Gold instead of inside each dashboard?
3. Why use surrogate keys when the data already has a natural key?
4. When should a mart be created, and what must it never store?
5. Why does `SELECT DISTINCT ROW_NUMBER() OVER () …` not build a dimension?

---

# PART 17 — Mini Project Exercise

Given a Silver table of your project data:
- write the **grain** sentence and test it
- design a fact table and **3** dimensions (with an `unknown` member where Silver flags values)
- build **2** marts for 2 different audiences, with additive parts only
- validate: rows, totals, NULL keys, marts = fact

---

# PART 18 — The Whole Picture

```text
Bronze (as received) → Silver (one trusted row per real thing, every row with a fate)
      → Gold (star schema: fact + dimensions) → marts (one audience each) → dashboard → decision
```

**Bad Gold → wrong decisions, silently. Good Gold → one number everyone trusts.**
