---
marp: true
theme: default
paginate: true
size: 16:9
---

# Week 6  
## Silver Layer Deep Dive — Transformations (Elite v3 — Full Story)

---

# PART 0 — WHY SILVER IS THE HEART OF THE PLATFORM

---

## The Most Important Layer

Bronze stores raw history.  
Gold serves business users.  
Silver creates **trusted data**.

---

## Critical Statement

If Silver is wrong:

- Gold is wrong
- dashboards are wrong
- KPIs are wrong
- machine learning features are wrong
- executive decisions are wrong

---

## Week 6 Core Message

👉 Silver is where **data becomes trustworthy**

---

## What Students Often Think

“Silver means just cleaning data.”

That is incomplete.

Silver also means:
- defining business rules
- enforcing consistency
- validating assumptions
- preparing reusable data assets

---

## Better Definition

Silver is the layer where data becomes:

- consistent
- validated
- standardized
- enriched
- reusable

---

## Why This Week Matters

Week 5 taught:
- Bronze keeps raw truth
- Gold serves business truth

Week 6 teaches:
👉 how Silver creates **trusted operational truth**

---

# PART 1 — SILVER AS A SYSTEM, NOT A STEP

---

## Silver Is Not One Query

Silver is not:
- one SQL statement
- one cleaning action
- one notebook cell

Silver is a **pipeline of rules**

---

## Silver Pipeline Pattern

```text
Bronze
  ↓
profile
  ↓
clean
  ↓
standardize
  ↓
deduplicate
  ↓
enrich
  ↓
validate
  ↓
Silver
```

---

## Key Insight

👉 Every stage changes the meaning of the data

---

## Why This Is Dangerous

If a transformation is wrong:

- the error may look “clean”
- the dashboard may still run
- the result may still seem believable

That makes Silver errors especially dangerous.

---

# PART 2 — DATA QUALITY DIMENSIONS

---

## Data Quality Framework

When we say “clean data,” we should be precise.

Silver quality usually involves:

1. completeness
2. consistency
3. validity
4. uniqueness
5. timeliness
6. reasonableness

---

## Completeness

Question:
Are required values present?

Example:
- missing charges
- missing smoker flag
- missing region

---

## Consistency

Question:
Do equivalent values appear in one standard form?

Example:
- NE
- north-east
- northeast

---

## Validity

Question:
Does the value follow expected rules?

Example:
- negative charges
- impossible ages
- invalid category labels

---

## Uniqueness

Question:
Do duplicate rows exist?

Example:
same record loaded twice

---

## Timeliness

Question:
Is the data up to date?

Example:
2024 dashboard accidentally built from 2023 data only

---

## Reasonableness

Question:
Does the data make business sense?

Example:
charges = 9,999,999 in a consumer insurance dataset

---

## Important Insight

👉 Data quality is multi-dimensional

One dataset may be:
- complete but inconsistent
- valid but duplicated
- standardized but outdated

---

# PART 3 — RUNNING CASE STUDY

---

## Running Case Study: Insurance Data

Assume Bronze contains these issues:

| age | smoker | region      | charges |
|-----|--------|-------------|---------|
| 19  | yes    | NE          | 16884   |
| 18  | no     | north-east  | 1725    |
| 28  | no     | northeast   | NULL    |
| 33  | no     | northeast   | 9999999 |
| 19  | yes    | NE          | 16884   |

---

## What Problems Do You See?

- inconsistent region values
- missing metric
- extreme outlier
- duplicate row

---

## Why This Matters

If we move this directly into Gold:

- KPIs will be wrong
- regional counts will split
- averages will be distorted
- duplicate individuals may double count

---

# PART 4 — PROFILING BEFORE TRANSFORMING

---

## Rule 1

👉 Never clean before you profile

---

## Why Profile First?

You need to understand:

- how many rows exist
- where NULLs exist
- what categories exist
- whether duplicates exist
- whether values are extreme

---

## Example Profiling Questions

- How many rows by year?
- How many NULL charges?
- What distinct region labels exist?
- Are there duplicate records?
- What is min/max charges?

---

## Example SQL — NULL Profile

```sql
SELECT
  COUNT(*) AS total_rows,
  SUM(CASE WHEN charges IS NULL THEN 1 ELSE 0 END) AS null_charges
FROM bronze_insurance;
```

---

## Example SQL — Distinct Categories

```sql
SELECT region, COUNT(*) AS n
FROM bronze_insurance
GROUP BY region
ORDER BY n DESC;
```

---

## Example SQL — Outlier Scan

```sql
SELECT MIN(charges) AS min_c,
       MAX(charges) AS max_c,
       AVG(charges) AS avg_c
FROM bronze_insurance
WHERE charges IS NOT NULL;
```

---

## Key Insight

👉 Profiling tells you what needs fixing

---

# PART 5 — TRANSFORMATION TYPE 1: NULL HANDLING

---

## Problem

Some rows have `charges = NULL`.

Question:
What should we do?

---

## Option A — Remove Rows

Use when:
- charges is the core metric
- missing metric makes record analytically unusable
- transparency matters more than retention

---

## Option B — Impute

Use when:
- domain supports estimation
- missingness is limited
- you can justify the method

Examples:
- fill with mean
- fill with median
- fill by group average

---

## Option C — Flag and Keep

Use when:
- you want to preserve row for downstream workflows
- business wants visibility into missingness

Example:
`is_charge_missing = 1`

---

## Numerical Example

Data:
100, 200, NULL, 10000

### Remove NULL, keep outlier
AVG = (100 + 200 + 10000) / 3 = 3433.33

### Remove NULL, remove outlier
AVG = (100 + 200) / 2 = 150

---

## Business Insight

👉 Transformation choices change KPIs dramatically

---

## Teaching Insight

There is no universal “correct” null strategy.

The correct strategy depends on:
- domain meaning
- downstream use
- governance requirements

---

# PART 6 — TRANSFORMATION TYPE 2: STANDARDIZATION

---

## Problem

Equivalent categories appear in multiple forms:

- NE
- north-east
- northeast

---

## Why This Is Serious

If uncleaned, then:

```sql
SELECT region, AVG(charges)
FROM data
GROUP BY region;
```

returns three groups instead of one

---

## Before Standardization

| region      | total_charges |
|-------------|---------------|
| NE          | 2500          |
| north-east  | 1200          |
| northeast   | 3700          |

---

## After Standardization

| region      | total_charges |
|-------------|---------------|
| northeast   | 7400          |

---

## Example SQL

```sql
CASE
  WHEN region IN ('NE', 'north-east') THEN 'northeast'
  ELSE LOWER(region)
END AS region_clean
```

---

## Key Insight

👉 Standardization is not cosmetic  
👉 It changes aggregation logic

---

# PART 7 — TRANSFORMATION TYPE 3: OUTLIER HANDLING

---

## Problem

One row has:
`charges = 9,999,999`

---

## Why Outliers Matter

Outliers can:
- distort averages
- dominate charts
- mislead segmentation
- hide real patterns

---

## Possible Strategies

1. remove
2. cap
3. keep and flag
4. investigate manually

---

## Remove

Use when:
- clearly invalid
- proven data error
- impossible in domain context

---

## Cap (Winsorize)

Use when:
- value may be real but too influential
- business still wants record retained

Example:
all values above threshold → threshold

---

## Keep and Flag

Use when:
- outlier may represent meaningful rare event
- downstream users need transparency

Example:
`is_outlier = 1`

---

## Numerical Example

Values:
100, 200, 300, 10000

AVG = 2650

After removing 10000:
AVG = 200

---

## Business Insight

👉 Outlier strategy is a business policy choice, not just a technical one

---

# PART 8 — TRANSFORMATION TYPE 4: DEDUPLICATION

---

## Problem

A row appears twice.

| person | region | charges |
|--------|--------|---------|
| 19     | NE     | 16884   |
| 19     | NE     | 16884   |

---

## Consequence

If duplicated record represents the same event:

- cost doubles
- counts inflate
- segments skew

---

## Deduplication Questions

- What defines a duplicate?
- Exact row match?
- Same business key?
- Same timestamp + entity?

---

## Example SQL — Exact Duplicate Check

```sql
SELECT age, smoker, region, charges, COUNT(*) AS n
FROM bronze_insurance
GROUP BY age, smoker, region, charges
HAVING COUNT(*) > 1;
```

---

## Important Insight

👉 Deduplication depends on business grain

---

# PART 9 — TRANSFORMATION TYPE 5: ENRICHMENT

---

## Enrichment Means

Adding useful derived attributes.

---

## Example

Age is numeric.  
Business users prefer age groups.

---

## SQL Example

```sql
CASE
  WHEN age < 30 THEN 'young'
  WHEN age < 60 THEN 'adult'
  ELSE 'senior'
END AS age_group
```

---

## Why This Matters

Silver is not just about removing bad data.

It is also about making data more useful.

---

## Other Enrichment Examples

- charge_band
- bmi_category
- year extracted from date
- normalized city/state attributes

---

## Key Insight

👉 Enrichment adds business usability

---

# PART 10 — ORDER OF TRANSFORMATIONS

---

## Order Matters

Bad order can create bad Silver data.

---

## Example Order

1. profile
2. standardize categories
3. handle NULLs
4. handle outliers
5. deduplicate
6. enrich
7. validate

---

## Why This Order?

Because:
- standardization helps duplicate detection
- null handling stabilizes metrics
- enrichment should happen after core cleaning

---

## Critical Insight

👉 Silver is not just rules  
👉 It is rule sequencing

---

# PART 11 — VALIDATION AS A FIRST-CLASS STEP

---

## Validation Is Not Optional

Silver without validation is just a guess.

---

## Validation Questions

- Did row count drop unexpectedly?
- Did region categories collapse correctly?
- Did NULLs go to zero where expected?
- Did duplicates disappear?
- Do averages still make sense?

---

## Example Validation Table

| check | before | after |
|------|--------|-------|
| row_count | 1000 | 850 |
| null_charges | 20 | 0 |
| distinct_region_labels | 7 | 4 |
| duplicate_rows | 10 | 0 |

---

## Example SQL — Row Count

```sql
SELECT COUNT(*) FROM silver_insurance;
```

---

## Example SQL — Distinct Categories

```sql
SELECT COUNT(DISTINCT region_clean)
FROM silver_insurance;
```

---

## Example SQL — Duplicate Audit

```sql
SELECT person_id, COUNT(*) AS n
FROM silver_insurance
GROUP BY person_id
HAVING COUNT(*) > 1;
```

---

## Example SQL — Distribution Sanity Check

```sql
SELECT
  MIN(charges) AS min_c,
  MAX(charges) AS max_c,
  AVG(charges) AS avg_c
FROM silver_insurance;
```

---

## Key Insight

👉 Validation creates trust  
👉 Trust creates adoption

---

# PART 12 — BEFORE/AFTER KPI COMPARISON

---

## Raw KPI

Average charge from Bronze:
may be distorted by:
- NULL handling assumptions
- outliers
- duplicates

---

## Silver KPI

Average charge from Silver:
- more consistent
- more defensible
- more stable for reporting

---

## Important Insight

Silver does not guarantee “perfect truth.”

It guarantees:
👉 controlled, explainable truth

---

# PART 13 — CASE STUDY: WRONG DASHBOARD

---

## Scenario

Dashboard says:
“Smokers cost less than non-smokers.”

This seems suspicious.

---

## Step 1 — Check Gold

The Gold query is correct.

So the problem is upstream.

---

## Step 2 — Check Silver

Find:
- missing smoker values were defaulted to “no”
- some smoker labels were inconsistent
- duplicates inflated the non-smoker group

---

## Step 3 — Root Cause

Silver transformation logic was wrong.

---

## Fix

- treat missing smoker as unknown
- standardize smoker labels
- deduplicate correctly
- rebuild downstream Gold

---

## Lesson

👉 Gold can be wrong even when Gold SQL is correct  
👉 because Silver was wrong

---

# PART 14 — GOOD SILVER VS BAD SILVER

---

## Bad Silver

- undocumented rules
- inconsistent thresholds
- no validation
- no reasoning
- no reproducibility

---

## Good Silver

- explicit rules
- justified transformations
- validation checks
- documented assumptions
- reproducible pipeline

---

## Insight

👉 Good Silver is explainable

---

# PART 15 — SILVER VS GOLD

---

## Silver

- row-level
- detailed
- flexible
- evolving
- supports many downstream uses

---

## Gold

- aggregated or modeled
- stable
- business-facing
- simpler for dashboards

---

## Key Relationship

👉 One Silver layer can feed many Gold tables

---

## Example

Silver insurance may feed:
- Gold pricing dashboard
- Gold regional cost mart
- Gold smoker risk analysis
- ML feature table

---

# PART 16 — COMMON FAILURES

---

## Failure 1 — Over-Cleaning

Removing too many rows.

Consequence:
- biased results
- false confidence

---

## Failure 2 — Under-Cleaning

Leaving inconsistencies.

Consequence:
- fragmented KPIs
- duplicate categories

---

## Failure 3 — Hidden Business Rules

Rule exists only in someone’s notebook.

Consequence:
- pipeline not reproducible

---

## Failure 4 — No Validation

Consequence:
- silent errors reach executives

---

## Failure 5 — Hardcoded Thresholds Without Context

Example:
`charges < 100000`

Question:
Why 100000?
Why not 50000?

---

## Insight

👉 Silver must be governed, not improvised

---

# PART 17 — INTERACTIVE THINKING

---

## Question 1

A row has NULL charges.  
What are three valid Silver strategies?

---

## Answer

- remove
- impute
- flag and keep

Correct choice depends on business context.

---

## Question 2

Where should age_group be created?

A) Bronze  
B) Silver  
C) Gold

---

## Answer

👉 Usually Silver

Because it is an enriched, reusable business-friendly attribute.

---

## Question 3

Where should a regional summary table live?

A) Bronze  
B) Silver  
C) Gold

---

## Answer

👉 Gold

Because it is aggregated and consumer-facing.

---

# PART 18 — FINAL SILVER PIPELINE VIEW

---

## Final Pattern

```text
Bronze
  ↓
Profile
  ↓
Clean NULLs
  ↓
Standardize values
  ↓
Handle outliers
  ↓
Deduplicate
  ↓
Enrich
  ↓
Validate
  ↓
Silver
```

---

## Final Insight

👉 Silver is where raw records become trusted analytical assets

---

# FINAL MESSAGE

---

You are not “cleaning data.”

You are:

👉 defining trusted data  
👉 encoding business logic  
👉 controlling quality  
👉 protecting KPIs  
👉 enabling reliable analytics
