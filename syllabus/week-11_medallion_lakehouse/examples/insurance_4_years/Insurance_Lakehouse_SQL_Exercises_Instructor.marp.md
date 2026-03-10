---
marp: true
paginate: true
size: 16:9
---
# Insurance Lakehouse SQL Exercises (Instructor)
### DuckDB • Bronze → Silver → Gold — with Solutions

![bg right:45% w:520](lakehouse_etl_diagram.png)

---

## Exercise 1 — Solution (Bronze view)

```sql
DROP VIEW IF EXISTS bronze_insurance;

CREATE VIEW bronze_insurance AS
SELECT
  *,
  CAST(split_part(filename, '.', 2) AS INTEGER) AS year
FROM read_csv_auto(
  'data/bronze/insurance.*.csv',
  header=true,
  filename=true
);

SELECT year, COUNT(*) AS rows
FROM bronze_insurance
GROUP BY year
ORDER BY year;
```

---

## Exercise 2 — Solution (Metadata + sample)

```sql
DESCRIBE bronze_insurance;

SELECT * FROM bronze_insurance LIMIT 5;
```

---

## Exercise 3 — Solution (Silver table)

> Note: DuckDB may infer `smoker` as BOOLEAN on some datasets.
> This solution standardizes `smoker` safely.

```sql
DROP TABLE IF EXISTS silver_insurance;

CREATE TABLE silver_insurance AS
SELECT
  CAST(age AS INTEGER) AS age,
  lower(trim(CAST(gender AS VARCHAR))) AS gender,
  CAST(bmi AS DOUBLE) AS bmi,
  CAST(children AS INTEGER) AS children,

  CASE
    WHEN TRY_CAST(smoker AS BOOLEAN) = TRUE THEN 'yes'
    WHEN TRY_CAST(smoker AS BOOLEAN) = FALSE THEN 'no'
    ELSE lower(trim(CAST(smoker AS VARCHAR)))
  END AS smoker,

  lower(trim(CAST(region AS VARCHAR))) AS region,
  CAST(charges AS DOUBLE) AS charges,
  CAST(year AS INTEGER) AS year,

  CASE
    WHEN bmi < 18.5 THEN 'underweight'
    WHEN bmi < 25 THEN 'normal'
    WHEN bmi < 30 THEN 'overweight'
    ELSE 'obese'
  END AS bmi_class,

  CASE
    WHEN age < 30 THEN '18-29'
    WHEN age < 40 THEN '30-39'
    WHEN age < 50 THEN '40-49'
    WHEN age < 60 THEN '50-59'
    ELSE '60+'
  END AS age_band
FROM bronze_insurance;
```

---

## Exercise 4 — Solution (Silver checks)

```sql
-- rows per year
SELECT year, COUNT(*) AS rows
FROM silver_insurance
GROUP BY year
ORDER BY year;

-- distinct categories
SELECT 'gender' AS col, gender AS val, COUNT(*) AS n
FROM silver_insurance GROUP BY gender
UNION ALL
SELECT 'smoker', smoker, COUNT(*) FROM silver_insurance GROUP BY smoker
UNION ALL
SELECT 'region', region, COUNT(*) FROM silver_insurance GROUP BY region
UNION ALL
SELECT 'bmi_class', bmi_class, COUNT(*) FROM silver_insurance GROUP BY bmi_class
UNION ALL
SELECT 'age_band', age_band, COUNT(*) FROM silver_insurance GROUP BY age_band;

-- min/max sanity
SELECT
  MIN(age) AS min_age, MAX(age) AS max_age,
  MIN(bmi) AS min_bmi, MAX(bmi) AS max_bmi,
  MIN(charges) AS min_charges, MAX(charges) AS max_charges
FROM silver_insurance;
```

---

## Exercise 5 — Solution (Gold KPI view)

```sql
DROP VIEW IF EXISTS gold_kpi_year;

CREATE VIEW gold_kpi_year AS
SELECT
  year,
  COUNT(*) AS members,
  AVG(charges) AS avg_charges,
  MEDIAN(charges) AS median_charges,
  QUANTILE_CONT(charges, 0.90) AS p90_charges,
  SUM(charges) AS total_charges,
  AVG(CASE WHEN smoker='yes' THEN charges END) AS avg_smoker_charges,
  AVG(CASE WHEN smoker='no'  THEN charges END) AS avg_nonsmoker_charges
FROM silver_insurance
GROUP BY year
ORDER BY year;
```

---

## Exercise 6 — Solution (Trend)

```sql
SELECT year, AVG(charges) AS avg_charges
FROM silver_insurance
GROUP BY year
ORDER BY year;
```

Python plot (minimal):

```python
df = con.execute("""
SELECT year, AVG(charges) AS avg_charges
FROM silver_insurance
GROUP BY year
ORDER BY year
""").df()

plt.figure()
plt.plot(df["year"], df["avg_charges"])
plt.xlabel("year"); plt.ylabel("avg_charges"); plt.title("Average Charges by Year")
plt.show()
```

---

## Exercise 7 — Solution (Smoker gap)

```sql
SELECT
  year,
  AVG(CASE WHEN smoker='yes' THEN charges END) AS avg_smoker,
  AVG(CASE WHEN smoker='no'  THEN charges END) AS avg_nonsmoker,
  AVG(CASE WHEN smoker='yes' THEN charges END) -
  AVG(CASE WHEN smoker='no'  THEN charges END) AS gap
FROM silver_insurance
GROUP BY year
ORDER BY year;
```

---

## Exercise 8 — Solution (Region ranking by year)

```sql
WITH r AS (
  SELECT year, region, AVG(charges) AS avg_charges
  FROM silver_insurance
  GROUP BY year, region
)
SELECT
  year, region, avg_charges,
  ROW_NUMBER() OVER (PARTITION BY year ORDER BY avg_charges DESC) AS rank_in_year
FROM r
ORDER BY year, rank_in_year;
```

---

## Exercise 9 — Solution (BMI class composition)

```sql
WITH c AS (
  SELECT year, bmi_class, COUNT(*) AS cnt
  FROM silver_insurance
  GROUP BY year, bmi_class
),
t AS (
  SELECT year, SUM(cnt) AS total
  FROM c
  GROUP BY year
)
SELECT
  c.year, c.bmi_class, c.cnt,
  ROUND(100.0 * c.cnt / t.total, 2) AS pct
FROM c
JOIN t USING(year)
ORDER BY c.year, pct DESC;
```

---

## Exercise 10 — Solution (p95 + above p95)

```sql
WITH p AS (
  SELECT year, QUANTILE_CONT(charges, 0.95) AS p95
  FROM silver_insurance
  GROUP BY year
),
m AS (
  SELECT s.year, COUNT(*) AS above_p95_count
  FROM silver_insurance s
  JOIN p USING(year)
  WHERE s.charges > p.p95
  GROUP BY s.year
)
SELECT p.year, p.p95, m.above_p95_count
FROM p
JOIN m USING(year)
ORDER BY p.year;
```

---

## Exercise 11 — Solution (Segment view for latest year)

```sql
CREATE OR REPLACE VIEW gold_segment_latest AS
WITH latest AS (SELECT MAX(year) AS year FROM silver_insurance)
SELECT
  age_band,
  bmi_class,
  COUNT(*) AS members,
  AVG(charges) AS avg_charges
FROM silver_insurance
WHERE year = (SELECT year FROM latest)
GROUP BY age_band, bmi_class
ORDER BY avg_charges DESC;
```

---

## Exercise 12 — Example answer key

1) **Biggest cost driver:** smoker status (avg and tail metrics jump).  
2) **Regional differences:** present but smaller than smoker effect.  
3) **Heavier tail:** check p90/p95 trend; outlier counts above p95.  
4) **Most expensive segment:** older + obese tends to lead.

---
