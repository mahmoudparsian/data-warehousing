---
marp: true
theme: default
paginate: true
size: 16:9
title: Week 7 — Session 1 — Conformance & Integration
---

# Week 7 — Session 1
## Silver: Conformance & Integration

Week 6 made **one** source trustworthy. Week 7 makes **several** sources agree.
Running example: 4 yearly insurance files (`data_messy/insurance.20*.messy.csv`), every query on the slides runs.
**Labs 7.1 and 7.2** do the same with the pizza shop's second source, the **delivery app**.

---

# 🔁 From Cleaning to Integration

| Step | Fixes | Question it answers |
|---|---|---|
| **cleaning** (week 6) | records | Is this row correct? |
| **conformance** | meaning | Do `north-east` and `NORTHEAST` mean the same region? |
| **integration** | system boundaries | Can rows from different sources sit in one table? |

👉 Two sources can each look clean and still give the **wrong answer** when combined:
one says `Medium`, the other `M`; one stores UTC, the other local time; both use order id `1001` for different orders.

---

# 🧭 Where This Happens in the Medallion Flow

```text
Bronze   one table per source, exactly as received (+ _source_file, _batch_id, _ingested_at)
   ↓
Silver   1. align       same column names and types in every source
         2. conform     same codes and spellings (macros + mapping tables)
         3. deduplicate remove and COUNT the copies
         4. reject/flag every row gets one fate: valid · flagged · rejected · duplicate
         5. integrate   UNION ALL the sources (+ a source / channel column)
         6. reconcile   Bronze rows = valid + flagged + rejected + duplicates, per source
   ↓
Gold     shaped for the business (week 8)
```

Same fates and same reconciliation as [week 5](../week05-Medallion-Architecture-Introduction/Medallion_Architecture_in_a_Nutshell.md) and week 6: only the number of sources is new.

---

# 🧩 Problem 1: Different Column Names and Types

Two branches of an insurer send the same facts in different shapes (a small inline example):

```sql
CREATE OR REPLACE TABLE branch_a AS SELECT * FROM (VALUES ('northeast', 1725.55), ('southwest', 4449.46))
    t(region, charges);                                   -- charges is a number
CREATE OR REPLACE TABLE branch_b AS SELECT * FROM (VALUES ('north-east', '1,234.56'), ('SE', '21,984.47'))
    t(region_name, charges);                              -- other column name, charges is text with a comma

SELECT 'A' AS source, region, charges FROM branch_a
UNION ALL BY NAME
SELECT 'B' AS source, region_name AS region, CAST(replace(charges, ',', '') AS DOUBLE) AS charges FROM branch_b;
```

<!-- RESULT -->

| source | region     |  charges |
|--------|------------|---------:|
| A      | northeast  |  1725.55 |
| A      | southwest  |  4449.46 |
| B      | north-east |  1234.56 |
| B      | SE         | 21984.47 |

*(4 rows)*

<!-- /RESULT -->

**Aligned** (same names, same types), but **not conformed**: `north-east` and `SE` still don't match `northeast` / `southeast`.
👉 Write the **schema mapping** first (target column ← source column + transformation), then the SQL.

---

# 🔑 Problem 2: Keys That Don't Match

```sql
CREATE OR REPLACE TABLE customers    AS SELECT * FROM (VALUES ('00123', 'Ana'), ('00456', 'Ben')) t(customer_id, name);
CREATE OR REPLACE TABLE transactions AS SELECT * FROM (VALUES ('123', 50.00), ('456', 75.00), ('00123', 20.00)) t(customer_id, amount);

SELECT 'raw keys' AS join_on, COUNT(*) AS matched_rows, SUM(amount) AS matched_amount
FROM transactions t JOIN customers c ON c.customer_id = t.customer_id
UNION ALL
SELECT 'conformed keys', COUNT(*), SUM(amount)
FROM transactions t JOIN customers c ON c.customer_id = lpad(t.customer_id, 5, '0');
```

<!-- RESULT -->

| join_on        | matched_rows | matched_amount |
|----------------|-------------:|---------------:|
| raw keys       |            1 |          20.00 |
| conformed keys |            3 |         145.00 |

*(2 rows)*

<!-- /RESULT -->

The raw join **silently loses** 2 of 3 transactions ($125 of $145): no error, just a smaller number.
👉 A join is only as trustworthy as the key conformance behind it. Conform keys **before** joining.

---

# 🏥 The Running Case: 4 Yearly Files = 4 Sources

```sql
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;

CREATE OR REPLACE TABLE bronze.insurance AS
SELECT * EXCLUDE (filename),
       regexp_extract(filename, '[^/]+$')               AS _source_file,
       CAST(regexp_extract(filename, '(\d{4})', 1) AS INT) AS _batch_id,
       current_timestamp                                AS _ingested_at
FROM read_csv('data_messy/insurance.*.messy.csv', all_varchar = true, filename = true);

SELECT _source_file, COUNT(*) AS bronze_rows FROM bronze.insurance GROUP BY 1 ORDER BY 1;
```

<!-- RESULT -->

| _source_file             | bronze_rows |
|--------------------------|------------:|
| insurance.2021.messy.csv |        1602 |
| insurance.2022.messy.csv |        1443 |
| insurance.2023.messy.csv |        1615 |
| insurance.2024.messy.csv |        1807 |

*(4 rows)*

<!-- /RESULT -->

Bronze = every row **as text**, with lineage. Here the 4 files share one header (`age, gender, bmi, children, smoker, region, charges`),
so alignment is easy; the hard part is the **values**.

---

# 🔍 Profile Every Source (Before Changing Anything)

```sql
SELECT _batch_id AS year,
       COUNT(*)                                                       AS n_rows,
       COUNT(DISTINCT region)                                         AS region_spellings,
       COUNT(*) FILTER (smoker IS NULL OR smoker NOT IN ('yes', 'no')) AS odd_smoker,
       COUNT(*) FILTER (age IS NULL OR bmi IS NULL OR children IS NULL OR charges IS NULL) AS missing_value,
       COUNT(*) FILTER (TRY_CAST(age AS DOUBLE) NOT BETWEEN 18 AND 100) AS odd_age,
       COUNT(*) FILTER (TRY_CAST(charges AS DOUBLE) <= 0)              AS charges_le_0,
       MIN(TRY_CAST(age AS DOUBLE)) AS min_age, MAX(TRY_CAST(age AS DOUBLE)) AS max_age
FROM bronze.insurance
GROUP BY 1 ORDER BY 1;
```

<!-- RESULT -->

| year | n_rows | region_spellings | odd_smoker | missing_value | odd_age | charges_le_0 | min_age | max_age |
|-----:|-------:|-----------------:|-----------:|--------------:|--------:|-------------:|--------:|--------:|
| 2021 |   1602 |               14 |         78 |           119 |      55 |           32 |   -10.0 |   150.0 |
| 2022 |   1443 |               14 |         80 |            94 |      51 |           35 |   -10.0 |   150.0 |
| 2023 |   1615 |               14 |         84 |            90 |      55 |           41 |   -10.0 |   150.0 |
| 2024 |   1807 |               14 |        105 |           119 |      67 |           42 |   -10.0 |   150.0 |

*(4 rows)*

<!-- /RESULT -->

Every file has the **same kinds** of problems in similar amounts: 14 region spellings, 78–105 odd smoker values, 90–119 rows with a missing value,
ages from −10 to 150. One set of rules, written once, handles all 4 sources.

---

# 🗺️ What the Region Column Really Holds

```sql
SELECT region, COUNT(*) AS n_rows FROM bronze.insurance GROUP BY 1 ORDER BY 2 DESC, 1;
```

<!-- RESULT -->

| region      | n_rows |
|-------------|-------:|
| southeast   |   1537 |
| northwest   |   1328 |
| northeast   |   1181 |
| southwest   |   1161 |
| south       |    413 |
| midwest     |    293 |
| north       |    220 |
| unknown     |     43 |
| north-east  |     42 |
|  SOUTHWEST  |     40 |
| mars        |     40 |
| moon        |     37 |
| south west  |     37 |
|  NORTHEAST  |     34 |
| south-west  |     34 |
| north east  |     27 |

*(16 rows)*

<!-- /RESULT -->

16 values, **1,046 rows** (16%) outside the 4 real regions. Three kinds of values: **real regions** in up to 4 spellings each (` NORTHEAST`, `north-east`, `north east`) · **ambiguous** (`south`, `midwest`, `north`: which region?)
· **invalid** (`unknown`, `mars`, `moon`). Smoker (`maybe`, `occasionally`, NULL) and gender (`M`, `unknown`, NULL) have the same pattern.

---

# 📋 The Business Rules (Written Down, with Fates)

| # | Rule | Fate |
|---|---|---|
| C1 | region: `norm_region()` macro (trim, lower, drop spaces and dashes) + mapping table `silver.map_region` | fixed |
| C2 | smoker `yes`/`no`, gender `female`/`male`/`m` via mapping tables | fixed |
| C3 | a value that doesn't map → `'unknown'` + a flag column | **flagged** (kept) |
| D1 | rows identical **after** C1–C2, in the same yearly file | **duplicate** (removed, counted) |
| R1 | age, bmi, children or charges missing | **rejected**: `missing value` |
| R2–R5 | age outside 18–100 · bmi outside 12–70 · children outside 0–10 · charges ≤ 0 | **rejected**, one reason each |

Order (week 5): **standardize → deduplicate → reject / flag**. Why flag and not reject an unknown region? The row's charges, age and smoker status are still good facts.

---

# 1️⃣ Conform: a Macro and Mapping Tables (Not a Long CASE)

```sql
CREATE OR REPLACE MACRO norm_region(r) AS regexp_replace(lower(trim(r)), '[ -]', '', 'g');

CREATE OR REPLACE TABLE silver.map_region AS SELECT * FROM (VALUES
    ('northeast', 'northeast'), ('northwest', 'northwest'),
    ('southeast', 'southeast'), ('southwest', 'southwest')) t(region_key, region);
CREATE OR REPLACE TABLE silver.map_smoker AS SELECT * FROM (VALUES ('yes', 'yes'), ('no', 'no')) t(smoker_key, smoker);
CREATE OR REPLACE TABLE silver.map_gender AS SELECT * FROM (VALUES ('female', 'female'), ('male', 'male'), ('m', 'male')) t(gender_key, gender);

CREATE OR REPLACE TABLE silver.step1_standardized AS
SELECT b._batch_id,
       TRY_CAST(TRY_CAST(b.age AS DOUBLE) AS INTEGER)      AS age,        -- '42.0' → 42
       COALESCE(g.gender, 'unknown')                       AS gender,
       TRY_CAST(b.bmi AS DECIMAL(5, 2))                    AS bmi,
       TRY_CAST(TRY_CAST(b.children AS DOUBLE) AS INTEGER) AS children,
       COALESCE(s.smoker, 'unknown')                       AS smoker,
       COALESCE(r.region, 'unknown')                       AS region,
       TRY_CAST(b.charges AS DECIMAL(10, 2))               AS charges,
       b.region                                            AS region_raw  -- lineage: what the source said
FROM bronze.insurance b
LEFT JOIN silver.map_region r ON r.region_key = norm_region(b.region)
LEFT JOIN silver.map_smoker s ON s.smoker_key = lower(trim(b.smoker))
LEFT JOIN silver.map_gender g ON g.gender_key = lower(trim(b.gender));

SELECT region, COUNT(*) AS n_rows FROM silver.step1_standardized GROUP BY 1 ORDER BY 1;
```

<!-- RESULT -->

| region    | n_rows |
|-----------|-------:|
| northeast |   1284 |
| northwest |   1328 |
| southeast |   1537 |
| southwest |   1272 |
| unknown   |   1046 |

*(5 rows)*

<!-- /RESULT -->

16 spellings → **4 regions + `unknown`** (1,046 rows): northeast collects 1,181 + 42 + 34 + 27 = 1,284 rows. A new spelling next year = one new row in `map_region`, no code change; the business can **review** the table.

---

# 2️⃣ Deduplicate on the Standardized Values

```sql
CREATE OR REPLACE TABLE silver.step2_dedup AS
SELECT * FROM silver.step1_standardized
QUALIFY ROW_NUMBER() OVER (PARTITION BY _batch_id, age, gender, bmi, children, smoker, region, charges
                           ORDER BY region_raw) = 1;

SELECT (SELECT COUNT(*) FROM bronze.insurance)
     - (SELECT COUNT(*) FROM (SELECT DISTINCT * EXCLUDE (_source_file, _ingested_at) FROM bronze.insurance)) AS copies_raw,
       (SELECT COUNT(*) FROM silver.step1_standardized) - (SELECT COUNT(*) FROM silver.step2_dedup)      AS copies_standardized;
```

<!-- RESULT -->

| copies_raw | copies_standardized |
|-----------:|--------------------:|
|        287 |                 296 |

*(1 row)*

<!-- /RESULT -->

Standardizing finds **9 more** copies (296, not 287). They differ **only in the region spelling** (`north-east` / `northeast`, or two unmappable labels such as `midwest` / `mars`) on rows with the same
age, bmi, children and charges to the cent: the **same customer** sent twice. Deduplicating the raw text would keep both and double-count them.
`_batch_id` is in the key: the same person in **two** years is two policy years, not a duplicate.

---

# 3️⃣ Reject What Can't Be Used (with a Reason)

```sql
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

SELECT reject_reason, COUNT(*) AS n_rows FROM silver.insurance_rejected GROUP BY 1 ORDER BY 2 DESC;
```

<!-- RESULT -->

| reject_reason         | n_rows |
|-----------------------|-------:|
| missing value         |    406 |
| age outside 18-100    |    175 |
| bmi outside 12-70     |    152 |
| children outside 0-10 |    149 |
| charges <= 0          |     92 |

*(5 rows)*

<!-- /RESULT -->

**974 rows** rejected, most for a missing value (406). They are **kept** (quarantine), each with its first failing reason: the source owner can fix them and re-send.

---

# 4️⃣ The Silver Table: Valid + Flagged Rows

```sql
CREATE OR REPLACE TABLE silver.insurance AS
SELECT _batch_id AS year, age, gender, bmi, children, smoker, region, charges, region_raw,
       gender = 'unknown' AS is_gender_unknown,
       smoker = 'unknown' AS is_smoker_unknown,
       region = 'unknown' AS is_region_unknown
FROM silver.step2_dedup
WHERE NOT (age IS NULL OR bmi IS NULL OR children IS NULL OR charges IS NULL     -- the same rules as the reject table
           OR age NOT BETWEEN 18 AND 100 OR bmi NOT BETWEEN 12 AND 70
           OR children NOT BETWEEN 0 AND 10 OR charges <= 0);

SELECT region, COUNT(*) AS customers, ROUND(AVG(charges), 2) AS avg_charges,
       ROUND(AVG((smoker = 'yes')::INT), 3) AS smoker_share
FROM silver.insurance GROUP BY 1 ORDER BY 1;
```

<!-- RESULT -->

| region    | customers | avg_charges | smoker_share |
|-----------|----------:|------------:|-------------:|
| northeast |      1018 |    17514.06 |        0.189 |
| northwest |      1096 |    17293.04 |         0.19 |
| southeast |      1255 |    16921.23 |        0.194 |
| southwest |      1015 |    16675.59 |        0.175 |
| unknown   |       813 |    25960.81 |         0.53 |

*(5 rows)*

<!-- /RESULT -->

**Why flag, not drop:** the 813 `unknown`-region customers are **not** a random sample: **53%** smokers (17.5–19.4% in the real regions) and
average charges of **$25,961** (real regions $16,676–$17,514).
A silent `WHERE region <> 'unknown'` would make the whole book of business look cheaper than it is.

---

# 🧮 Reconcile: Every Bronze Row Has One Fate

```sql
WITH c AS (
  SELECT (SELECT COUNT(*) FROM bronze.insurance) AS bronze,
         COUNT(*) FILTER (WHERE NOT (is_gender_unknown OR is_smoker_unknown OR is_region_unknown)) AS valid,
         COUNT(*) FILTER (WHERE is_gender_unknown OR is_smoker_unknown OR is_region_unknown)     AS flagged,
         (SELECT COUNT(*) FROM silver.insurance_rejected)                                       AS rejected,
         (SELECT COUNT(*) FROM silver.step1_standardized) - (SELECT COUNT(*) FROM silver.step2_dedup) AS duplicates
  FROM silver.insurance
)
SELECT *, valid + flagged + rejected + duplicates AS total, bronze = total AS reconciled FROM c;
```

<!-- RESULT -->

| bronze | valid | flagged | rejected | duplicates | total | reconciled |
|-------:|------:|--------:|---------:|-----------:|------:|------------|
|   6467 |  4160 |    1037 |      974 |        296 |  6467 | true       |

*(1 row)*

<!-- /RESULT -->

**6,467 = 4,160 valid + 1,037 flagged + 974 rejected + 296 duplicates.** Silver holds 4,160 + 1,037 = 5,197 rows.
👉 With several sources, reconcile **per source** too (`GROUP BY _batch_id`): a gap in one file hides easily in a combined total.

---

# ✅ Validate: Tests That Must Return 0

```sql
SELECT 'region not canonical' AS test, COUNT(*) AS failures FROM silver.insurance
WHERE region NOT IN (SELECT region FROM silver.map_region) AND NOT is_region_unknown
UNION ALL SELECT 'missing measure', COUNT(*) FROM silver.insurance
WHERE age IS NULL OR bmi IS NULL OR children IS NULL OR charges IS NULL
UNION ALL SELECT 'impossible value', COUNT(*) FROM silver.insurance
WHERE age NOT BETWEEN 18 AND 100 OR bmi NOT BETWEEN 12 AND 70 OR children NOT BETWEEN 0 AND 10 OR charges <= 0
UNION ALL SELECT 'duplicate rows', COUNT(*) - COUNT(DISTINCT (year, age, gender, bmi, children, smoker, region, charges))
FROM silver.insurance;
```

<!-- RESULT -->

| test                 | failures |
|----------------------|---------:|
| region not canonical |        0 |
| missing measure      |        0 |
| impossible value     |        0 |
| duplicate rows       |        0 |

*(4 rows)*

<!-- /RESULT -->

Run them after **every** load; a non-zero row stops the pipeline before Gold is built.

---

# 📊 KPI Impact: the Same Question, Bronze vs Silver

"Average charges in the northeast?"

```sql
SELECT 'Bronze, region = ''northeast''' AS answer_from, COUNT(*) AS n_rows,
       ROUND(AVG(TRY_CAST(charges AS DOUBLE)), 2) AS avg_charges
FROM bronze.insurance WHERE region = 'northeast'
UNION ALL
SELECT 'Bronze, all 4 spellings', COUNT(*), ROUND(AVG(TRY_CAST(charges AS DOUBLE)), 2)
FROM bronze.insurance WHERE norm_region(region) = 'northeast'
UNION ALL
SELECT 'Silver', COUNT(*), ROUND(AVG(charges), 2)
FROM silver.insurance WHERE region = 'northeast';
```

<!-- RESULT -->

| answer_from                  | n_rows | avg_charges |
|------------------------------|-------:|------------:|
| Bronze, region = 'northeast' |   1181 |     17119.0 |
| Bronze, all 4 spellings      |   1284 |    17002.87 |
| Silver                       |   1018 |    17514.06 |

*(3 rows)*

<!-- /RESULT -->

Three answers to one question: $17,119 (1,181 rows), $17,003 (1,284) and **$17,514 (1,018)**. Bronze misses the other spellings, counts the copies and
averages in rows Silver rejects (charges of −100, ages of 150). Silver answers from **one row per customer-year**, all usable: $395 (2.3%) higher than the naive query.

---

# 💬 Discussion

1. Age 150: reject the row, or set `age = NULL` and keep the charges? What would the business lose either way?
2. `midwest` is not one of the insurer's 4 regions. Flag it as `unknown`, or ask the source to fix it and reject until then?
3. The same person appears in 2021 and 2022: duplicate or two facts? What **key** decides?
4. A new file arrives with `region_name` instead of `region`. Which step catches it: Bronze, profiling or validation?

---

# ✅ Summary

| Step | Insurance case |
|---|---|
| align | 4 files, one header; types from `all_varchar` text with `TRY_CAST` |
| conform | macro `norm_region` + 3 mapping tables; unmappable → `'unknown'` + flag |
| deduplicate | on standardized values, per year: 296 copies counted (287 raw) |
| reject | 974 rows, 5 reasons, kept in `silver.insurance_rejected` |
| reconcile | 6,467 = 4,160 + 1,037 + 974 + 296 ✅ |
| validate | 4 tests, all 0 |

Next ([slides 2](lecture_notes_02_conforming_in_duckdb.md)): the DuckDB patterns one by one, time zones, when sources **disagree**, and `UNION ALL` across sources.
