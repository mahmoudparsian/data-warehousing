---
marp: true
theme: default
paginate: true
title: Week 6 — Session 2 — Silver Cleaning
---

# Week 6 — Session 2
## Silver Cleaning: From Bronze to Data You Can Trust

Profile → standardize → handle NULLs and outliers → deduplicate → enrich → **validate and reconcile**.
One small insurance Bronze table, every step on the slides. **Lab 6.2** does the same with the pizza shop.

---

# 🎯 What Silver Is (and Is Not)

| Silver **is** | Silver is **not** |
|---|---|
| one row per real event or entity | a copy of Bronze with nicer column names |
| correct **types**, **standard** values | a place for business KPIs (that is Gold) |
| every **business rule** applied, in a fixed order | "let's quickly remove the bad rows" |
| every Bronze row with exactly **one fate** | silent `WHERE … IS NOT NULL` filters |
| **proven**: reconciled, validated | trusted because it "looks fine" |

**Fates** ([week 5](../week05-Medallion-Architecture-Introduction/Medallion_Architecture_in_a_Nutshell.md)): **valid** · **flagged** (kept, marked) · **rejected** (quarantined with a reason) · **duplicate** (removed, counted).

---

# 📏 Data-Quality Dimensions: What We Check

| Dimension | Question | SQL check |
|---|---|---|
| **Completeness** | are required values present? | `COUNT(*) - COUNT(col)` |
| **Validity** | in the allowed list / range / format? | `col NOT IN (…)`, `NOT BETWEEN`, `LIKE '____-__-__'` |
| **Consistency** | one value written one way? | `GROUP BY col` shows `NE`, `north-east`, `northeast` |
| **Uniqueness** | one row per real thing? | `COUNT(*) - COUNT(DISTINCT key)` |
| **Reasonableness** | plausible for the business? | `MIN`, `MAX`, `quantile_cont` |
| **Timeliness** | is the batch the expected one, complete? | rows per `_batch_id`, max date |

Every Silver rule exists because one of these checks failed in the **profile**.

---

# 🧪 Our Bronze Table (As Received, All Text)

```sql
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;

CREATE OR REPLACE TABLE bronze.insurance AS
SELECT *, 'insurance_export.csv' AS _source_file
FROM (VALUES ('19', 'yes', '27.9',  'NE',         '16884.92'),
             ('18', 'no',  '33.77', 'north-east', '1725.55'),
             ('28', 'no',  '33.0',  'northeast',  NULL),
             ('33', 'no',  '22.7',  'northeast',  '9999999'),
             ('19', 'yes', '27.9',  'NE',         '16884.92'),
             ('19', 'yes', '27.9',  'northeast',  '16884.92'),
             ('45', 'no',  '29.83', 'Southeast ', '8240.59'),
             ('60', 'yes', '32.8',  'southwest',  '47896.79'),
             ('31', 'no',  '25.74', 'SOUTHEAST',  '3756.62'),
             ('52', 'no',  '30.2',  'northwest',  '10600.55'))
     AS t(age, smoker, bmi, region, charges);

SELECT COUNT(*) AS bronze_rows FROM bronze.insurance;
```

<!-- RESULT -->

| bronze_rows |
|------------:|
|          10 |

*(1 row)*

<!-- /RESULT -->

---

# 🔍 Step 0: Profile Before You Transform

```sql
SELECT COUNT(*)                                                    AS n_rows,
       COUNT(*) - COUNT(charges)                                   AS null_charges,
       COUNT(DISTINCT region)                                      AS region_spellings,
       COUNT(*) - (SELECT COUNT(*) FROM (SELECT DISTINCT * FROM bronze.insurance)) AS exact_duplicates,
       MIN(charges::DOUBLE)                                        AS min_charges,
       MAX(charges::DOUBLE)                                        AS max_charges
FROM bronze.insurance;
```

<!-- RESULT -->

| n_rows | null_charges | region_spellings | exact_duplicates | min_charges | max_charges |
|-------:|-------------:|-----------------:|-----------------:|------------:|------------:|
|     10 |            1 |                7 |                1 |     1725.55 |   9999999.0 |

*(1 row)*

<!-- /RESULT -->

**The to-do list:** 1 NULL metric (completeness) · 7 spellings of 4 regions (consistency) · an impossible 9,999,999 (reasonableness) · copies (uniqueness).
👉 **Never clean before you profile**: you would not know what you fixed, or what you missed.

---

# 📋 The Business Rules (Written Down, with Fates)

| # | Rule | Fate |
|---|---|---|
| S1 | `region`: trim, lower case; `ne` / `north-east` → `northeast` | fixed |
| S2 | rows identical after S1 | **duplicate** (removed, counted) |
| S3 | `charges` missing: no metric, no analysis | **rejected**: reason `missing charges` |
| S4 | `charges` above 100,000: impossible for this insurer | **rejected**: reason `impossible charges` |
| S5 | add `age_band`, `bmi_class` (enrichment) | computed |

The rules come from the **business** (S4: "our highest claim ever was 64,000"), not from the analyst's taste.

---

# 1️⃣ Standardization (S1)

```sql
CREATE OR REPLACE TABLE silver.step1_standardized AS
SELECT age::INTEGER                          AS age,
       smoker = 'yes'                        AS smoker,
       bmi::DOUBLE                           AS bmi,
       CASE LOWER(TRIM(region))
            WHEN 'ne'         THEN 'northeast'
            WHEN 'north-east' THEN 'northeast'
            ELSE LOWER(TRIM(region))
       END                                   AS region,
       charges::DOUBLE                       AS charges,
       _source_file
FROM bronze.insurance;

SELECT region, COUNT(*) AS n_rows FROM silver.step1_standardized GROUP BY ALL ORDER BY region;
```

<!-- RESULT -->

| region    | n_rows |
|-----------|-------:|
| northeast |      6 |
| northwest |      1 |
| southeast |      2 |
| southwest |      1 |

*(4 rows)*

<!-- /RESULT -->

7 spellings → 4 regions. Without this, every "by region" report **splits** one region into three rows.

---

# 2️⃣ Deduplication (S2), and Why the Order Matters

```sql
SELECT (SELECT COUNT(*) FROM (SELECT DISTINCT * FROM bronze.insurance))           AS distinct_before_standardizing,
       (SELECT COUNT(*) FROM (SELECT DISTINCT * FROM silver.step1_standardized))   AS distinct_after_standardizing;
```

<!-- RESULT -->

| distinct_before_standardizing | distinct_after_standardizing |
|------------------------------:|-----------------------------:|
|                             9 |                            8 |

*(1 row)*

<!-- /RESULT -->

The third copy of the 19-year-old smoker says `northeast` instead of `NE`: identical **only after** standardizing.
**Deduplicate after standardizing**, or copies that differ only in spelling survive and double-count.
(The rule behind it: a duplicate = the **same real thing** sent twice. Two customers can't share age, bmi and charges to the cent, so compare standardized values.
[Week 7](../week07-Silver-Layer-Cleaning-and-Conforming/lecture_notes_02_conforming_in_duckdb.md) shows the other case: order lines with no line id, where two real pizzas can look identical.)

```sql
CREATE OR REPLACE TABLE silver.step2_dedup AS
SELECT DISTINCT * FROM silver.step1_standardized;
```

---

# 3️⃣ NULLs: Three Options, One Decision

| Option | Fate | Use when |
|---|---|---|
| **reject** (quarantine with a reason) | rejected | the value is required, and there is no honest way to fill it (here: charges is **the** metric) |
| **default / impute** + a flag column | fixed + flagged | the business agrees on a value (discount NULL → 0) or a method (median by group) |
| **keep the NULL** + a flag column | flagged | the row is still useful; analysts must see that the value is unknown |

Numbers change with the choice: charges 100, 200, NULL, 10,000 → `AVG` 3,433 (NULL skipped), 2,575 (NULL = 0), 150 (outlier removed too).
👉 There is no universal "correct" choice: **write the rule down**, apply it in Silver, and count what it did.

---

# 4️⃣ Outliers: Valid but Rare, or Impossible?

| Strategy | Fate | When |
|---|---|---|
| **reject** | rejected | **impossible** values (a 9,999,999 claim, age 230, a sale dated 2099) |
| **cap** (winsorize) + flag | fixed + flagged | a model needs bounded values; keep the original in Bronze |
| **keep and flag** (`is_extreme`) | flagged | **real** but rare values: the most expensive customers are real customers |

Use the business limit (S4), not a statistical rule alone: the 47,896.79 smoker is extreme for this sample, but real.

---

# 3️⃣ + 4️⃣ Quarantine the Rejected Rows (S3, S4)

```sql
CREATE OR REPLACE TABLE silver.rejected AS
SELECT *,
       CASE WHEN charges IS NULL THEN 'missing charges'
            ELSE 'impossible charges' END AS reject_reason
FROM silver.step2_dedup
WHERE charges IS NULL OR charges > 100000;

SELECT age, region, charges, reject_reason FROM silver.rejected ORDER BY age;
```

<!-- RESULT -->

| age | region    |   charges | reject_reason      |
|----:|-----------|----------:|--------------------|
|  28 | northeast |      NULL | missing charges    |
|  33 | northeast | 9999999.0 | impossible charges |

*(2 rows)*

<!-- /RESULT -->

Not deleted: kept with the reason, so the source can be fixed, and the reconciliation can count them.

---

# 5️⃣ Enrichment (S5) → the Silver Table

```sql
CREATE OR REPLACE TABLE silver.insurance AS
SELECT *,
       (age // 10) * 10                                 AS age_band,
       CASE WHEN bmi < 18.5 THEN 'underweight'
            WHEN bmi < 25   THEN 'normal'
            WHEN bmi < 30   THEN 'overweight'
            ELSE 'obese' END                            AS bmi_class
FROM silver.step2_dedup
WHERE NOT (charges IS NULL OR charges > 100000);        -- exactly the rows not rejected

SELECT age, smoker, region, charges, age_band, bmi_class FROM silver.insurance ORDER BY age;
```

<!-- RESULT -->

| age | smoker | region    |  charges | age_band | bmi_class  |
|----:|--------|-----------|---------:|---------:|------------|
|  18 | false  | northeast |  1725.55 |       10 | obese      |
|  19 | true   | northeast | 16884.92 |       10 | overweight |
|  31 | false  | southeast |  3756.62 |       30 | overweight |
|  45 | false  | southeast |  8240.59 |       40 | overweight |
|  52 | false  | northwest | 10600.55 |       50 | obese      |
|  60 | true   | southwest | 47896.79 |       60 | obese      |

*(6 rows)*

<!-- /RESULT -->

Enrichment = new columns **derived** from existing ones, with one definition for everyone. (`age` is INTEGER here, so `//` works.)

---

# 🔁 The Order of Transformations

1. **type + standardize** (S1): so equal values look equal
2. **deduplicate** (S2): on standardized values
3. **validate → reject / flag** (S3, S4): on clean, unique rows
4. **enrich** (S5): only rows that stay in Silver
5. **reconcile + validate** the result

Change the order and the result changes: dedup before S1 keeps an extra copy; enrich before rejecting computes bands for rows that leave.
Week 3's lesson was the same: deduplicate **before** filling defaults.

---

# ⚖️ Validation 1: Reconcile

```sql
SELECT (SELECT COUNT(*) FROM bronze.insurance)                                              AS bronze_rows,
       (SELECT COUNT(*) FROM silver.insurance)                                              AS valid,
       0                                                                                    AS flagged,
       (SELECT COUNT(*) FROM silver.rejected)                                               AS rejected,
       (SELECT COUNT(*) FROM silver.step1_standardized) - (SELECT COUNT(*) FROM silver.step2_dedup) AS duplicates;
```

<!-- RESULT -->

| bronze_rows | valid | flagged | rejected | duplicates |
|------------:|------:|--------:|---------:|-----------:|
|          10 |     6 |       0 |        2 |          2 |

*(1 row)*

<!-- /RESULT -->

**10 = 6 valid + 0 flagged + 2 rejected + 2 duplicates.** If the equation fails, a rule lost rows: Silver is **not** done.

---

# ✅ Validation 2: Rules as Tests

```sql
SELECT COUNT(*) - COUNT(DISTINCT (age, smoker, bmi, region, charges))                          AS duplicates_left,
       COUNT(*) FILTER (WHERE region NOT IN ('northeast', 'northwest', 'southeast', 'southwest')) AS bad_regions,
       COUNT(*) FILTER (WHERE charges IS NULL OR charges > 100000)                              AS bad_charges,
       COUNT(*) FILTER (WHERE age_band IS NULL OR bmi_class IS NULL)                            AS missing_enrichment
FROM silver.insurance;
```

<!-- RESULT -->

| duplicates_left | bad_regions | bad_charges | missing_enrichment |
|----------------:|------------:|------------:|-------------------:|
|               0 |           0 |           0 |                  0 |

*(1 row)*

<!-- /RESULT -->

Every rule becomes a test that must return **0** after every load. A non-zero test **stops** the pipeline before Gold.

---

# 📊 Before / After: Why It Matters

```sql
SELECT 'Bronze (naive)' AS source,
       COUNT(*) AS n_rows, COUNT(DISTINCT region) AS regions, ROUND(AVG(charges::DOUBLE), 0) AS avg_charges
FROM bronze.insurance
UNION ALL
SELECT 'Silver', COUNT(*), COUNT(DISTINCT region), ROUND(AVG(charges), 0)
FROM silver.insurance;
```

<!-- RESULT -->

| source         | n_rows | regions | avg_charges |
|----------------|-------:|--------:|------------:|
| Bronze (naive) |     10 |       7 |   1124764.0 |
| Silver         |      6 |       4 |     14851.0 |

*(2 rows)*

<!-- /RESULT -->

The naive average is **76×** too high (one impossible value), and "regions" counts spellings. Same data, different truth:
a dashboard on Bronze would be confidently wrong.

---

# 🔍 Case: the Wrong Dashboard

**Gold says** "northeast has the fewest customers". Debug **backward**:

1. **Gold:** the query is correct (`COUNT(*) … GROUP BY region`).
2. **Silver:** `northeast` = 2 customers; check the rules: is S1's mapping complete?
3. **Bronze:** `GROUP BY region` → `NE`, `north-east`, `Northeast `… a new spelling arrived, the mapping missed it, and `ELSE` passed it through.

**Fix in Silver** (add the spelling, or map unknown values to `'unknown'` and **flag** them), rebuild from Bronze, and add the test "`bad_regions` = 0".

---

# 🧭 Good Silver vs Bad Silver

| Bad Silver | Good Silver |
|---|---|
| `WHERE charges IS NOT NULL` (rows vanish) | `silver.rejected` with `reject_reason` |
| `DISTINCT` on raw spellings | standardize first, then deduplicate |
| rules live in someone's head | rules written, numbered, one SQL step each |
| no counts | reconciliation after every load |
| cleaning also inside reports | **all** cleaning in Silver, once |
| "too clean": every rare value removed | real extremes kept, flagged |

---

# 🥈 Silver vs 🥇 Gold

| | Silver | Gold |
|---|---|---|
| Grain | one row per event / entity (a customer, an order line) | shaped for a question (star schema, KPI tables) |
| Contains | **all** valid rows, typed, standardized, enriched | joins, aggregates, business measures |
| Users | data engineers, data scientists, analysts | dashboards, executives |
| Changes | when a **rule** changes | when a **question** changes |

Silver answers "what really happened?"; Gold answers "what does the business need to know?" (week 8).

---

# ⚠️ Common Failures

| Failure | Example | Instead |
|---|---|---|
| over-cleaning | removing the 47,896 smoker as an "outlier" | business limits, flag real extremes |
| under-cleaning | `NE` and `northeast` as two regions | profile every column, every load |
| hidden rules | a filter nobody wrote down | numbered rules → one Silver step each |
| no validation | "the job ran, so it's fine" | reconcile + tests that must return 0 |
| magic thresholds | "remove everything above the 99th percentile" | a threshold the business signed off |

---

# ✅ Summary

| Step | Pizza shop (Lab 6.2) |
|---|---|
| profile | the Lab 6.1 to-do list |
| standardize + type | two date formats → one `DATE` (rule 1) |
| deduplicate | exact duplicate orders (rule 3) |
| reject with a reason | NULL `order_id` (rule 2), NULL fields in order lines (rule 4) → reject tables |
| enrich | `silver.order_lines`: orders + lines + menu, `line_revenue` |
| validate | reconcile per batch, 0 orphans, **control total $817,860.05** |

👉 Now: **Lab 6.2** (30 minutes). Deep dive, same ideas on more data: [`notebook_01_silver_cleaning.py`](notebook_01_silver_cleaning.py).
