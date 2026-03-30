# Week 4 Lab — Instructor Version
## ETL, OLAP, and Medallion Architecture

## 1) Instructor Goals

This lab should help students move from abstract architecture to operational understanding.

By the end of the lab, students should clearly understand:

- why raw data should not be queried directly for business reporting
- how Silver creates trust through cleaning and validation
- why Gold should contain business-ready metrics
- how OLAP ideas help analysts move between detail and summary

A strong student answer should always include:
- correct SQL
- correct layer reasoning
- business interpretation

---

## 2) Core Teaching Message

Repeat these ideas often:

- **Bronze captures**
- **Silver cleans**
- **Gold explains**

And:

- **ETL/ELT builds trust**
- **OLAP builds insight**

---

# Part A — Bronze Layer

## Task 1 — Inspect the Raw Data

### Sample SQL
```sql
SELECT *
FROM bronze_sales;
```

### What we are doing
- looking at the data exactly as it arrived
- identifying raw formatting problems
- beginning the profiling process

### Why this matters
Bronze is not meant to be elegant.  
It is meant to preserve the source truth.

### Teaching note
Students should notice issues such as:
- inconsistent capitalization
- trailing spaces
- non-numeric values in amount

This is the moment to reinforce:
> Raw data is valuable, but not trustworthy enough for reporting.

---

## Task 2 — Count Raw Rows

### Sample SQL
```sql
SELECT COUNT(*) AS bronze_row_count
FROM bronze_sales;
```

### What we are doing
- measuring the ingestion volume
- creating a baseline for later comparison
- supporting observability of the pipeline

### Why this matters
If Bronze loads 10,000 rows today and 4,000 tomorrow, that may indicate:
- a source issue
- a missing file
- a failed ingestion step

### Teaching note
Students should understand that row counts are one of the simplest but most important pipeline checks.

---

## Task 3 — Identify Potentially Bad Numeric Values

### Sample SQL
```sql
SELECT *
FROM bronze_sales
WHERE TRY_CAST(amount AS DOUBLE) IS NULL;
```

### What we are doing
- testing which rows fail numeric conversion
- isolating problematic raw values
- preparing for Silver-layer cleaning

### Why this matters
If `amount` is not numeric, then:
- sums fail
- averages fail
- Gold metrics become unreliable

### Teaching note
This is a strong example of why type profiling belongs early in ETL.

---

# Part B — Silver Layer

## Task 4 — Standardize Region Values

### Sample SQL
```sql
SELECT
    order_id,
    LOWER(TRIM(region)) AS region_clean
FROM bronze_sales;
```

### What we are doing
- removing extra spaces
- forcing a consistent case
- standardizing category values

### Why this matters
Without standardization:
- `West`
- `west`
- `West `
would become separate groups in an aggregate query.

### Teaching note
This is one of the simplest and most important transformation patterns in ETL.

---

## Task 5 — Convert Amount to Numeric

### Sample SQL
```sql
SELECT
    order_id,
    TRY_CAST(amount AS DOUBLE) AS amount_num
FROM bronze_sales;
```

### What we are doing
- converting text into a true numeric field
- safely handling bad values
- preparing the measure for analysis

### Why this matters
Analytical measures must be typed correctly before aggregation.

### Teaching note
Emphasize why `TRY_CAST` is safer than a direct cast in messy data contexts.

---

## Task 6 — Create the Silver Table

### Sample SQL
```sql
CREATE TABLE silver_sales AS
SELECT
    order_id,
    LOWER(TRIM(region)) AS region,
    TRY_CAST(amount AS DOUBLE) AS amount
FROM bronze_sales
WHERE TRY_CAST(amount AS DOUBLE) IS NOT NULL;
```

### What we are doing
- cleaning text columns
- converting the measure
- excluding clearly invalid rows

### Why this matters
Silver is the trusted layer where analysis becomes possible.

### Teaching note
Students should explain not only what was changed, but why those changes were necessary.

---

## Task 7 — Validate Silver Row Count

### Sample SQL
```sql
SELECT COUNT(*) AS silver_row_count
FROM silver_sales;
```

### What we are doing
- counting surviving rows after cleaning
- comparing against Bronze volume
- validating pipeline impact

### Why this matters
A reduction in row count is acceptable only if it is understood and justified.

### Teaching note
Ask:
- Was row loss expected?
- Was it small or large?
- Does the business accept that cleaning rule?

---

## Task 8 — Check for Negative or Invalid Values

### Sample SQL
```sql
SELECT *
FROM silver_sales
WHERE amount < 0
   OR amount IS NULL;
```

### What we are doing
- validating the cleaned layer
- checking for remaining suspicious values
- confirming Silver quality

### Why this matters
Silver should be trusted, but trust must be tested.

### Teaching note
This helps students understand that validation is continuous, not one-time.

---

# Part C — Gold Layer

## Task 9 — Revenue by Region

### Sample SQL
```sql
SELECT
    region,
    SUM(amount) AS total_revenue
FROM silver_sales
GROUP BY region
ORDER BY total_revenue DESC;
```

### What we are doing
- rolling detailed rows into a business metric
- summarizing by one important dimension
- producing a management-friendly result

### Why this matters
This is a classic Gold metric:
- simple
- trusted
- immediately useful

### Teaching note
This is a good place to reinforce the difference between:
- Silver = trusted data
- Gold = trusted business metric

---

## Task 10 — Create the Gold Table

### Sample SQL
```sql
CREATE TABLE gold_sales AS
SELECT
    region,
    SUM(amount) AS total_revenue
FROM silver_sales
GROUP BY region;
```

### What we are doing
- storing a curated aggregate
- creating a reusable reporting asset
- separating business-facing logic from raw processing

### Why this matters
Gold tables reduce repeated work and simplify dashboarding.

### Teaching note
Students should understand why Gold tables are usually smaller, simpler, and more business-oriented.

---

## Task 11 — Interpret the Gold Result

### Expected interpretation guidance
A strong student answer should say something like:

- the Gold table summarizes revenue by region
- it identifies stronger and weaker regional performance
- management could use this to prioritize resources, promotions, or investigation
- further drill-down might examine why one region performs differently

### Teaching note
Do not accept answers that only repeat the query result without business meaning.

---

# Part D — OLAP Thinking

## Task 12 — Slice

### Sample SQL
```sql
SELECT
    region,
    SUM(amount) AS total_revenue
FROM silver_sales
WHERE region = 'west'
GROUP BY region;
```

### What we are doing
- fixing one dimension value
- narrowing the scope of analysis
- focusing on a single business segment

### Why this matters
Managers often care about one segment at a time.

### Teaching note
A slice is conceptually simple but extremely common in business analysis.

---

## Task 13 — Dice

### Sample SQL
```sql
SELECT
    region,
    SUM(amount) AS total_revenue
FROM silver_sales
WHERE region = 'west'
  AND amount > 1000
GROUP BY region;
```

### What we are doing
- applying more than one condition
- narrowing analysis with multiple filters
- creating a more targeted business view

### Why this matters
This is closer to how real business questions are asked.

### Teaching note
The exact dice condition may vary; what matters is the concept of multi-dimensional filtering.

---

## Task 14 — Roll-Up

### Sample SQL
```sql
SELECT
    region,
    SUM(amount) AS total_revenue
FROM silver_sales
GROUP BY region;
```

### What we are doing
- aggregating detailed rows into a higher-level summary
- producing a compact metric view
- moving from operations to management reporting

### Why this matters
Roll-up is one of the most common forms of business analysis.

### Teaching note
Students should explain what detail is lost and what clarity is gained.

---

## Task 15 — Drill-Down

### Sample SQL
```sql
SELECT *
FROM silver_sales
WHERE region = 'west';
```

### What we are doing
- moving from a summary result to supporting detail
- investigating the rows behind a metric
- connecting Gold back to Silver

### Why this matters
Executives may ask:
> Why is West so high?

Drill-down lets the analyst answer.

### Teaching note
This is where traceability across layers becomes especially important.

---

# Part E — Integrated Thinking

## Task 16 — Describe the Full Pipeline

### Strong answer should include
- Bronze stores the raw source data for traceability
- Silver cleans and validates data for trust
- Gold stores curated metrics for reporting and dashboards
- each layer has a distinct role and audience

### Teaching note
Students should avoid describing Medallion as “just three tables.”  
It is a workflow and trust model, not only a naming convention.

---

## Task 17 — ETL vs ELT

### Strong answer should include
- ETL transforms before loading
- ELT loads first and transforms later
- modern warehouses often prefer ELT because compute is inside the warehouse
- both still require transformation rules and validation logic

### Teaching note
The conceptual distinction matters more than strict vendor terminology.

---

## Task 18 — Final Synthesis Question

### Strong answer should include ideas such as
- raw files are messy and inconsistent
- direct querying of raw data creates fragile reporting
- pipelines improve data trust, repeatability, and explainability
- layered architecture makes debugging and reuse easier
- OLAP-style analysis depends on trusted, structured data

### Teaching note
This final answer should sound like systems thinking, not isolated SQL syntax.

---

# Final Instructor Guidance

By the end of this lab, students should clearly understand:

- why pipelines exist
- why trust must be engineered
- why Gold should be simple but powerful
- why architecture is part of analytical thinking

A successful Week 4 student now understands:

> Data engineering prepares the truth.  
> Analytics turns that truth into decisions.
