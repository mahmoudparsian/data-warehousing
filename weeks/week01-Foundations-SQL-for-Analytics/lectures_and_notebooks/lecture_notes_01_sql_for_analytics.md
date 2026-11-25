---
marp: true
title: Week 1 — Foundations of SQL for Analytics
paginate: true
theme: default
class: lead
---

# Week 1
## Foundations of SQL for Analytics

Question → SQL → result → insight → decision

---

# 🎯 Learning Objectives

By the end of this session you can:

- turn a **business question** into a `SELECT` with `WHERE`, `GROUP BY`, `ORDER BY`, `LIMIT`
- choose the right aggregate: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`
- read a result and state **one insight with a number** in it
- check an insight with a **second dimension** before you believe it
- explain the error *"must appear in the GROUP BY clause"*

---

# 🧠 The Analyst Loop

| Step | Example |
|---|---|
| 1. **Question** | "Do smokers cost more?" |
| 2. **SQL** | `SELECT smoker, AVG(charges) … GROUP BY smoker` |
| 3. **Result** | 32,050 vs 8,434 |
| 4. **Insight** | smokers cost **3.8×** as much |
| 5. **Decision** | price smoking as a risk factor |

👉 SQL is not about memorizing syntax: it is **structured thinking**. The goal is always the insight, not the query.

---

# 📊 Our Data: `insurance.csv`

1,338 rows, **one row per insured customer**, 7 columns:

| Column | Meaning |
|---|---|
| `age` | age in years (18–64) |
| `gender` | `male` / `female` |
| `bmi` | body mass index (≥ 30 = obese) |
| `children` | number of children covered by the plan |
| `smoker` | smokes or not |
| `region` | `northeast`, `northwest`, `southeast`, `southwest` (US) |
| `charges` | yearly medical cost billed by the insurer (US $) |

**Business context:** an insurer prices by **risk**. Which customers are expensive, and why?

---

# 🔧 Setup: Load the CSV into DuckDB

```sql
CREATE OR REPLACE TABLE insurance AS
SELECT * FROM read_csv('../example_1_insurance/insurance.csv');

DESCRIBE insurance;
```

<!-- RESULT -->

| column_name | column_type | null | key  | default | extra |
|-------------|-------------|------|------|---------|-------|
| age         | BIGINT      | YES  | NULL | NULL    | NULL  |
| gender      | VARCHAR     | YES  | NULL | NULL    | NULL  |
| bmi         | DOUBLE      | YES  | NULL | NULL    | NULL  |
| children    | BIGINT      | YES  | NULL | NULL    | NULL  |
| smoker      | BOOLEAN     | YES  | NULL | NULL    | NULL  |
| region      | VARCHAR     | YES  | NULL | NULL    | NULL  |
| charges     | DOUBLE      | YES  | NULL | NULL    | NULL  |

*(7 rows)*

<!-- /RESULT -->

⚠️ The file says `yes` / `no`, but DuckDB reads `smoker` as **BOOLEAN** (`true` / `false`). Write `WHERE smoker` (or `WHERE NOT smoker`); `WHERE smoker = 'yes'` also works (DuckDB converts `'yes'` to `true`).

---

# 🔍 First Look: Exploration, Not Analysis Yet

```sql
SELECT * FROM insurance LIMIT 5;
```

<!-- RESULT -->

| age | gender |    bmi | children | smoker | region    |     charges |
|----:|--------|-------:|---------:|--------|-----------|------------:|
|  19 | female |   27.9 |        0 | true   | southwest |   16884.924 |
|  18 | male   |  33.77 |        1 | false  | southeast |   1725.5523 |
|  28 | male   |   33.0 |        3 | false  | southeast |    4449.462 |
|  33 | male   | 22.705 |        0 | false  | northwest | 21984.47061 |
|  32 | male   |  28.88 |        0 | false  | northwest |   3866.8552 |

*(5 rows)*

<!-- /RESULT -->

- `LIMIT` shows a sample: never print 1,338 rows (or 1 billion) to "look at the data".
- **Exploration** = looking at data. **Analysis** = answering a question. Always move from the first to the second.

---

# 🎯 Today's Questions

1. Who are the **most expensive** customers, and what do they share?
2. Do **smokers** cost more? How much more?
3. Does **region** matter, or is it something else in disguise?
4. How big is the **high-risk** group (smoker **and** obese)?
5. Which **segments** should pricing focus on?

---

# Q1 — Who Are the Most Expensive Customers?

```sql
SELECT age, gender, bmi, smoker, region, ROUND(charges, 0) AS charges
FROM insurance
ORDER BY charges DESC
LIMIT 10;
```

<!-- RESULT -->

| age | gender |    bmi | smoker | region    | charges |
|----:|--------|-------:|--------|-----------|--------:|
|  54 | female |  47.41 | true   | southeast | 63770.0 |
|  45 | male   |  30.36 | true   | southeast | 62593.0 |
|  52 | male   | 34.485 | true   | northwest | 60021.0 |
|  31 | female | 38.095 | true   | northeast | 58571.0 |
|  33 | female |  35.53 | true   | northwest | 55135.0 |
|  60 | male   |   32.8 | true   | southwest | 52591.0 |
|  28 | male   |   36.4 | true   | southwest | 51195.0 |
|  64 | male   |  36.96 | true   | southeast | 49578.0 |
|  59 | male   |  41.14 | true   | southeast | 48970.0 |
|  44 | female |  38.06 | true   | southeast | 48885.0 |

*(10 rows)*

<!-- /RESULT -->

💡 **All 10 are smokers**, and all 10 have a BMI above 30. That is a **hypothesis**, not a proof: 10 rows out of 1,338.

---

# Q2 — Test the Hypothesis: Do Smokers Cost More?

```sql
SELECT smoker,
       COUNT(*)                  AS customers,
       ROUND(AVG(charges), 0)    AS avg_charges
FROM insurance
GROUP BY smoker
ORDER BY avg_charges DESC;
```

<!-- RESULT -->

| smoker | customers | avg_charges |
|--------|----------:|------------:|
| true   |       274 |     32050.0 |
| false  |      1064 |      8434.0 |

*(2 rows)*

<!-- /RESULT -->

💡 Smokers cost **3.8×** as much on average (32,050 vs 8,434), and the groups are large (274 and 1,064), so this is **not** an accident of a few rows.
**Business meaning:** smoking is the strongest single price factor in this data.

---

# Q3 — Does Region Affect Cost?

```sql
SELECT region,
       COUNT(*)                  AS customers,
       ROUND(AVG(charges), 0)    AS avg_charges
FROM insurance
GROUP BY region
ORDER BY avg_charges DESC;
```

<!-- RESULT -->

| region    | customers | avg_charges |
|-----------|----------:|------------:|
| southeast |       364 |     14735.0 |
| northeast |       324 |     13406.0 |
| northwest |       325 |     12418.0 |
| southwest |       325 |     12347.0 |

*(4 rows)*

<!-- /RESULT -->

💡 The **southeast** is the most expensive region (14,735), but the gap between regions (about 2,400) is small next to the smoker gap (about 23,600).
**Is it really the region?** Next slide.

---

# 📊 Two Dimensions: Region × Smoker

```sql
SELECT region,
       smoker,
       COUNT(*)                  AS customers,
       ROUND(AVG(charges), 0)    AS avg_charges
FROM insurance
GROUP BY region, smoker
ORDER BY smoker DESC, avg_charges DESC;
```

<!-- RESULT -->

| region    | smoker | customers | avg_charges |
|-----------|--------|----------:|------------:|
| southeast | true   |        91 |     34845.0 |
| southwest | true   |        58 |     32269.0 |
| northwest | true   |        58 |     30192.0 |
| northeast | true   |        67 |     29674.0 |
| northeast | false  |       257 |      9166.0 |
| northwest | false  |       267 |      8556.0 |
| southeast | false  |       273 |      8032.0 |
| southwest | false  |       267 |      8019.0 |

*(8 rows)*

<!-- /RESULT -->

💡 For **non-smokers**, the southeast is one of the **cheapest** regions (8,032). Its high average comes mostly from having the **most smokers** (91).
👉 Always check an insight with a **second dimension** before you act on it.

---

# Q4 — Outliers: Who Costs More Than $20,000?

```sql
SELECT smoker,
       COUNT(*)                  AS customers,
       ROUND(AVG(charges), 0)    AS avg_charges
FROM insurance
WHERE charges > 20000
GROUP BY smoker
ORDER BY smoker DESC;
```

<!-- RESULT -->

| smoker | customers | avg_charges |
|--------|----------:|------------:|
| true   |       212 |     36330.0 |
| false  |        61 |     25837.0 |

*(2 rows)*

<!-- /RESULT -->

💡 273 customers cost more than $20,000, and **212 of them (78%) are smokers**, although smokers are only 20% of all customers.
`WHERE` filters **rows before** the groups are made.

---

# 📊 The High-Risk Segment: Smoker **and** Obese

```sql
SELECT COUNT(*)                  AS customers,
       ROUND(AVG(charges), 0)    AS avg_charges
FROM insurance
WHERE smoker AND bmi >= 30;
```

<!-- RESULT -->

| customers | avg_charges |
|----------:|------------:|
|       145 |     41558.0 |

*(1 row)*

<!-- /RESULT -->

💡 145 customers (11%) average **41,558**: about **5×** a non-smoker (8,434). Two risk factors together **amplify** the cost.
`AND` combines conditions: both must be true.

---

# 📊 Aggregates: Which One Answers Which Question?

| Aggregate | Answers | Example |
|---|---|---|
| `COUNT(*)` | how **many**? | customers per region |
| `SUM(col)` | how much **in total**? | total charges per region |
| `AVG(col)` | how much **per one**, typically? | charges per customer |
| `MIN(col)` / `MAX(col)` | the **extremes** | cheapest / most expensive customer |

👉 A group can be big in **total** only because it is big in **count**. Compare totals **and** averages.

---

# 📊 Total vs Average

```sql
SELECT region,
       COUNT(*)                  AS customers,
       ROUND(SUM(charges), 0)    AS total_charges,
       ROUND(AVG(charges), 0)    AS avg_charges
FROM insurance
GROUP BY region
ORDER BY total_charges DESC;
```

<!-- RESULT -->

| region    | customers | total_charges | avg_charges |
|-----------|----------:|--------------:|------------:|
| southeast |       364 |     5363690.0 |     14735.0 |
| northeast |       324 |     4343669.0 |     13406.0 |
| northwest |       325 |     4035712.0 |     12418.0 |
| southwest |       325 |     4012755.0 |     12347.0 |

*(4 rows)*

<!-- /RESULT -->

💡 The southeast's total is 1.3× the southwest's: partly more customers (364 vs 325), partly a higher average. `SUM` alone cannot tell you which.

---

# 📊 Family Size: Is It a Straight Line?

```sql
SELECT children,
       COUNT(*)                  AS customers,
       ROUND(AVG(charges), 0)    AS avg_charges
FROM insurance
GROUP BY children
ORDER BY children;
```

<!-- RESULT -->

| children | customers | avg_charges |
|---------:|----------:|------------:|
|        0 |       574 |     12366.0 |
|        1 |       324 |     12731.0 |
|        2 |       240 |     15074.0 |
|        3 |       157 |     15355.0 |
|        4 |        25 |     13851.0 |
|        5 |        18 |      8786.0 |

*(6 rows)*

<!-- /RESULT -->

💡 Cost rises up to 3 children, then falls, so it is **not** a straight line. But 4 and 5 children are only 25 and 18 customers:
an average of **few rows is unreliable**. Always show `COUNT(*)` next to `AVG`.

---

# ⚠️ Common SQL Error: a Column Not in `GROUP BY`

```sql
SELECT region, charges
FROM insurance
GROUP BY region;
```

<!-- ERROR -->

```text
Binder Error: column "charges" must appear in the GROUP BY clause or must be part of an aggregate function.
Either add it to the GROUP BY list, or use ANY_VALUE("charges") if the exact value of "charges" is not important.

LINE 1: SELECT region, charges
                       ^^^^^^^
```

<!-- /ERROR -->

One row per region, but each region has ~330 different `charges`: which one should SQL show? Say it: `AVG(charges)`, `MAX(charges)`, …

---

# ✅ The GROUP BY Rule

With `GROUP BY`, every column in `SELECT` is **either**

- in the `GROUP BY` list (`region`), **or**
- inside an aggregate (`AVG(charges)`, `COUNT(*)`).

```sql
SELECT region, ROUND(AVG(charges), 0) AS avg_charges   -- ✅
FROM insurance
GROUP BY region;
```

---

# 🧠 Written Order vs Execution Order

| You **write** | DuckDB **runs** |
|---|---|
| `SELECT` | 1. `FROM`: pick the table |
| `FROM` | 2. `WHERE`: keep some **rows** |
| `WHERE` | 3. `GROUP BY`: make groups |
| `GROUP BY` | 4. `SELECT`: compute the output columns |
| `ORDER BY` | 5. `ORDER BY`: sort |
| `LIMIT` | 6. `LIMIT`: cut |

- This explains surprises: `WHERE` cannot use `AVG(…)` (no groups exist yet), but `ORDER BY` can use a `SELECT` alias.
- Session 2 adds `HAVING` (filter **groups**) between steps 3 and 4.

---

# 📊 Categories: `DISTINCT` and `COUNT(DISTINCT …)`

```sql
SELECT COUNT(DISTINCT region)  AS regions,
       COUNT(DISTINCT gender)  AS genders,
       COUNT(DISTINCT age)     AS distinct_ages,
       COUNT(DISTINCT bmi)     AS distinct_bmis
FROM insurance;
```

<!-- RESULT -->

| regions | genders | distinct_ages | distinct_bmis |
|--------:|--------:|--------------:|--------------:|
|       4 |       2 |            47 |           548 |

*(1 row)*

<!-- /RESULT -->

💡 `region` (4 values) is a good `GROUP BY` column. `bmi` (548 values) is not: `GROUP BY bmi` gives 548 tiny groups. Put it in **bands** first (next slide).

---

# 📊 Bands: Group a Number into Ranges

```sql
SELECT FLOOR(age / 10) * 10      AS age_band,     -- 18 → 10, 27 → 20, 64 → 60
       COUNT(*)                  AS customers,
       ROUND(AVG(charges), 0)    AS avg_charges
FROM insurance
GROUP BY age_band
ORDER BY age_band;
```

<!-- RESULT -->

| age_band | customers | avg_charges |
|---------:|----------:|------------:|
|     10.0 |       137 |      8407.0 |
|     20.0 |       280 |      9562.0 |
|     30.0 |       257 |     11739.0 |
|     40.0 |       279 |     14399.0 |
|     50.0 |       271 |     16495.0 |
|     60.0 |       114 |     21248.0 |

*(6 rows)*

<!-- /RESULT -->

💡 Cost rises steadily with age: the 60s cost **2.5×** the teens. (`FLOOR` rounds down: `FLOOR(2.7)` = 2. Session 2 builds bands of any width with `CASE`.)

---

# 📊 Case Study: Where Should Pricing Focus?

```sql
SELECT smoker,
       region,
       COUNT(*)                  AS customers,
       ROUND(AVG(charges), 0)    AS avg_charges,
       ROUND(SUM(charges), 0)    AS total_charges
FROM insurance
GROUP BY smoker, region
ORDER BY total_charges DESC
LIMIT 4;
```

<!-- RESULT -->

| smoker | region    | customers | avg_charges | total_charges |
|--------|-----------|----------:|------------:|--------------:|
| true   | southeast |        91 |     34845.0 |     3170895.0 |
| false  | northeast |       257 |      9166.0 |     2355542.0 |
| false  | northwest |       267 |      8556.0 |     2284576.0 |
| false  | southeast |       273 |      8032.0 |     2192795.0 |

*(4 rows)*

<!-- /RESULT -->

💡 Just **91 southeast smokers** (7% of customers) cost more in total than any group of ~260 non-smokers.
**Decision:** price smoking first; a regional price difference matters much less.

---

# ✍️ Practice: Try Before You Look

| # | Question | Hint |
|---|---|---|
| 1 | Do men and women cost the same on average? | `GROUP BY gender` |
| 2 | What is the most expensive customer in each region? | `MAX(charges)` |
| 3 | What are the cheapest, most expensive and average charges? | `MIN`, `MAX`, `AVG` in one row |
| 4 | Is the average a "typical" customer? | compare `AVG` with `MEDIAN` |
| 5 | Does cost rise with BMI? | bands: `FLOOR(bmi / 5) * 5` |

Solutions on the next slides. More practice: notebook **`notebook_02_sql_exercises.py`**.

---

# ✅ Practice 1–2

```sql
SELECT gender, COUNT(*) AS customers, ROUND(AVG(charges), 0) AS avg_charges
FROM insurance
GROUP BY gender
ORDER BY gender;
```

<!-- RESULT -->

| gender | customers | avg_charges |
|--------|----------:|------------:|
| female |       662 |     12570.0 |
| male   |       676 |     13957.0 |

*(2 rows)*

<!-- /RESULT -->

```sql
SELECT region, ROUND(MAX(charges), 0) AS max_charges
FROM insurance
GROUP BY region
ORDER BY max_charges DESC;
```

<!-- RESULT -->

| region    | max_charges |
|-----------|------------:|
| southeast |     63770.0 |
| northwest |     60021.0 |
| northeast |     58571.0 |
| southwest |     52591.0 |

*(4 rows)*

<!-- /RESULT -->

---

# ✅ Practice 3–4: Range, Average and Median

```sql
SELECT ROUND(MIN(charges), 0)     AS min_charges,
       ROUND(MAX(charges), 0)     AS max_charges,
       ROUND(AVG(charges), 0)     AS avg_charges,
       ROUND(MEDIAN(charges), 0)  AS median_charges
FROM insurance;
```

<!-- RESULT -->

| min_charges | max_charges | avg_charges | median_charges |
|------------:|------------:|------------:|---------------:|
|      1122.0 |     63770.0 |     13270.0 |         9382.0 |

*(1 row)*

<!-- /RESULT -->

💡 The average (13,270) is **41% above** the median (9,382): a few very expensive customers pull the average up (a **right-skewed** distribution).
For a "typical customer", report the **median**.

---

# ✅ Practice 5: BMI Bands

```sql
SELECT FLOOR(bmi / 5) * 5        AS bmi_band,
       COUNT(*)                  AS customers,
       ROUND(AVG(charges), 0)    AS avg_charges
FROM insurance
GROUP BY bmi_band
ORDER BY bmi_band;
```

<!-- RESULT -->

| bmi_band | customers | avg_charges |
|---------:|----------:|------------:|
|     15.0 |        41 |      8839.0 |
|     20.0 |       204 |     10572.0 |
|     25.0 |       386 |     10988.0 |
|     30.0 |       391 |     14420.0 |
|     35.0 |       225 |     17022.0 |
|     40.0 |        71 |     16570.0 |
|     45.0 |        17 |     17815.0 |
|     50.0 |         3 |     16034.0 |

*(8 rows)*

<!-- /RESULT -->

💡 The jump is at **BMI 30** (obese): +31% vs the 25–30 band (14,420 vs 10,988). From 45 up the groups are tiny (17 and 3 customers): don't trust those averages.

---

# 🧰 Summary: Question → SQL Pattern

| Business question | SQL pattern |
|---|---|
| What does the data look like? | `SELECT * … LIMIT 5`, `DESCRIBE` |
| Who is the top / bottom N? | `ORDER BY col DESC LIMIT N` |
| Does X change Y? | `SELECT x, COUNT(*), AVG(y) … GROUP BY x` |
| Is it really X? | add a second dimension: `GROUP BY x, z` |
| Only some rows | `WHERE cond1 AND cond2` (before grouping) |
| A number with too many values | bands: `FLOOR(col / 10) * 10` |
| Typical value | `MEDIAN` next to `AVG` |
| Big in total or per customer? | `SUM` **and** `AVG` **and** `COUNT` |

**Better questions → better SQL → better decisions.**
