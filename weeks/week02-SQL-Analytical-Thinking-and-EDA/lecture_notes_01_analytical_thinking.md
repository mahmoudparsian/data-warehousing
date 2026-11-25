---
marp: true
title: Week 2 — SQL & Analytical Thinking
paginate: true
theme: default
class: lead
---

# Week 2
## SQL & Analytical Thinking

Six habits that turn a correct query into a **trustworthy** answer

---

# 🎯 Learning Objectives

Week 1 taught the SQL: `WHERE`, `GROUP BY`, `HAVING`, `CASE`. Today: **how to think** with it.

By the end of this session you can:

- rewrite a vague business question as a precise one (metric, grain, comparison)
- tell when a group is **too small** to trust its average
- compare every number to a **baseline**
- detect a **mix effect**: an average that differs because the group's **composition** differs
- report **share**, **median** and **count**, not only the average
- write a one-sentence insight with numbers in it

---

# 🔧 Setup: the Insurance Data from Week 1

```sql
CREATE OR REPLACE TABLE insurance AS
SELECT * FROM read_csv('../week01-Foundations-SQL-for-Analytics/example_1_insurance/insurance.csv');

SELECT COUNT(*) AS customers, ROUND(AVG(charges), 0) AS avg_charges FROM insurance;
```

<!-- RESULT -->

| customers | avg_charges |
|----------:|------------:|
|      1338 |     13270.0 |

*(1 row)*

<!-- /RESULT -->

Reminder: one row per customer; `charges` = the yearly medical cost billed by the insurer; `smoker` is BOOLEAN.

---

# Habit 1 — Make the Question Precise

| Vague | Precise |
|---|---|
| "Who are our most valuable customers?" | Which customers have the **highest yearly charges**? |
| "What drives cost?" | Which **single column** splits **average charges** the most? |
| "Where should we act?" | Which **region × smoker** segment has the largest **total** charges? |

A precise question names:

- the **metric** (`charges`: a cost for the insurer, not revenue)
- the **grain**: one row per what? (customer, region, region × smoker)
- the **comparison**: compared with what? (other groups, the overall average)

👉 If you cannot write the `SELECT` and `GROUP BY` from the question, the question is not precise yet.

---

# Habit 2 — Check the Size Before You Trust the Average

**Question:** Which single age is the most expensive?

```sql
SELECT age,
       COUNT(*)                         AS customers,
       COUNT(*) FILTER (WHERE smoker)   AS smokers,
       ROUND(AVG(charges), 0)           AS avg_charges
FROM insurance
GROUP BY age
ORDER BY avg_charges DESC
LIMIT 5;
```

<!-- RESULT -->

| age | customers | smokers | avg_charges |
|----:|----------:|--------:|------------:|
|  64 |        22 |       7 |     23276.0 |
|  61 |        23 |       6 |     22024.0 |
|  60 |        23 |       5 |     21979.0 |
|  63 |        23 |       5 |     19885.0 |
|  43 |        27 |      12 |     19267.0 |

*(5 rows)*

<!-- /RESULT -->

💡 Age **43** sits among the 60-year-olds, not because 43 is a risky age: **12 of its 27** customers smoke (44%, vs 20.5% overall).
Groups of 20–30 rows are **noisy**: use bands (`FLOOR(age / 10) * 10`) or `HAVING COUNT(*) >= 100`.

---

# Habit 3 — Compare to a Baseline

A number alone means nothing. **Index** = group average ÷ overall average × 100 (100 = average).

```sql
SELECT region,
       ROUND(AVG(charges), 0)                                           AS avg_charges,
       ROUND(100 * AVG(charges) / (SELECT AVG(charges) FROM insurance)) AS index_vs_all
FROM insurance
GROUP BY region
ORDER BY index_vs_all DESC;
```

<!-- RESULT -->

| region    | avg_charges | index_vs_all |
|-----------|------------:|-------------:|
| southeast |     14735.0 |        111.0 |
| northeast |     13406.0 |        101.0 |
| northwest |     12418.0 |         94.0 |
| southwest |     12347.0 |         93.0 |

*(4 rows)*

<!-- /RESULT -->

💡 The southeast is **11% above** the average customer; the two western regions are **6–7% below**. "14,735" alone says neither.
👉 The overall average on **every row**, without a subquery, is exactly what a **window function** does (next deck).

---

# Habit 4 — Check the Mix (1/2)

**Question:** Why is the southeast the most expensive region? Look at **who** lives there.

```sql
SELECT region,
       COUNT(*)                              AS customers,
       ROUND(100 * AVG(smoker::INTEGER), 1)  AS pct_smokers,
       ROUND(AVG(charges), 0)                AS avg_charges
FROM insurance
GROUP BY region
ORDER BY avg_charges DESC;
```

<!-- RESULT -->

| region    | customers | pct_smokers | avg_charges |
|-----------|----------:|------------:|------------:|
| southeast |       364 |        25.0 |     14735.0 |
| northeast |       324 |        20.7 |     13406.0 |
| northwest |       325 |        17.8 |     12418.0 |
| southwest |       325 |        17.8 |     12347.0 |

*(4 rows)*

<!-- /RESULT -->

- `smoker::INTEGER` turns `true` / `false` into 1 / 0, so `AVG` of it = the **share** of smokers.
- 💡 The region ranking **follows the smoker share**: the southeast has the most smokers (25%).

---

# Habit 4 — Check the Mix (2/2): a Same-Mix Comparison

What would each region cost if **every region had the same smoker share** (the overall 20.5%)?

```sql
WITH overall AS (SELECT AVG(smoker::INTEGER) AS share FROM insurance)
SELECT region,
       ROUND(AVG(charges), 0) AS avg_charges,
       ROUND(  (SELECT share FROM overall)     * AVG(charges) FILTER (WHERE smoker)
             + (1 - (SELECT share FROM overall)) * AVG(charges) FILTER (WHERE NOT smoker), 0) AS same_mix_avg
FROM insurance
GROUP BY region
ORDER BY avg_charges DESC;
```

<!-- RESULT -->

| region    | avg_charges | same_mix_avg |
|-----------|------------:|-------------:|
| southeast |     14735.0 |      13523.0 |
| northeast |     13406.0 |      13365.0 |
| northwest |     12418.0 |      12987.0 |
| southwest |     12347.0 |      12985.0 |

*(4 rows)*

<!-- /RESULT -->

💡 With the same mix, the gap between the most and least expensive region shrinks from about **2,400 to about 540**.
Most of "the southeast is expensive" is really "the southeast has more smokers". This is a **mix effect**: you will meet it again in Lab 2.2.

---

# 🧠 The Mix Effect in One Line

**A group's average = (share of part A × average of A) + (share of part B × average of B)**

So a group's average can change because:

1. the parts **themselves** changed (smokers got more expensive), **or**
2. the **mix** changed (more smokers in the group), even if no part changed at all.

👉 Before you explain a difference between groups (or years), split it by the biggest driver (here: `smoker`) and compare **like with like**.

---

# Habit 5 — Total, Average **and** Share

**Question:** How much of the insurer's cost comes from smokers?

```sql
SELECT ROUND(100 * AVG(smoker::INTEGER), 1)                               AS pct_of_customers,
       ROUND(100 * SUM(charges) FILTER (WHERE smoker) / SUM(charges), 1)   AS pct_of_charges
FROM insurance;
```

<!-- RESULT -->

| pct_of_customers | pct_of_charges |
|-----------------:|---------------:|
|             20.5 |           49.5 |

*(1 row)*

<!-- /RESULT -->

💡 **One customer in five** causes **half** of all charges. The average (3.8×) hides how big this is for the business; the **share** shows it.

---

# Habit 6 — Look at the Distribution, Not Only the Average

```sql
SELECT smoker,
       ROUND(quantile_cont(charges, 0.25), 0)  AS p25,
       ROUND(MEDIAN(charges), 0)               AS median,
       ROUND(AVG(charges), 0)                  AS avg,
       ROUND(quantile_cont(charges, 0.75), 0)  AS p75
FROM insurance
GROUP BY smoker
ORDER BY smoker DESC;
```

<!-- RESULT -->

| smoker |     p25 |  median |     avg |     p75 |
|--------|--------:|--------:|--------:|--------:|
| true   | 20826.0 | 34456.0 | 32050.0 | 41019.0 |
| false  |  3986.0 |  7345.0 |  8434.0 | 11363.0 |

*(2 rows)*

<!-- /RESULT -->

- `quantile_cont(col, 0.25)` = the value below which 25% of the rows fall (`MEDIAN` = 0.5).
- 💡 Non-smokers: the average (8,434) is **above** the median (7,345): a few expensive non-smokers pull it up.
  Smokers: half of them cost more than **34,456**. The "typical" values differ by **4.7×**, not 3.8×.

---

# ⚠️ Common Mistake: the Average of Averages

```sql
SELECT ROUND(AVG(avg_charges), 0)                     AS avg_of_group_avgs,
       (SELECT ROUND(AVG(charges), 0) FROM insurance) AS true_avg
FROM (SELECT smoker, AVG(charges) AS avg_charges
      FROM insurance
      GROUP BY smoker);
```

<!-- RESULT -->

| avg_of_group_avgs | true_avg |
|------------------:|---------:|
|           20242.0 |  13270.0 |

*(1 row)*

<!-- /RESULT -->

The two groups have **different sizes** (274 vs 1,064), so their averages cannot simply be averaged. Always go back to the rows:
`SUM(charges) / COUNT(*)`, or `AVG(charges)` over the whole table.

---

# ✍️ Writing the Insight

**Template:** *[group] [metric] is [number] ([n = …]), [comparison]; so [decision].*

| ❌ Vague | ✅ Precise |
|---|---|
| "Smokers cost significantly more." | "Smokers (n = 274) average 32,050 in charges, 3.8× non-smokers, and cause 49.5% of all charges; price smoking first." |
| "Some regions amplify risk." | "The southeast is 11% above average, but only ~4% above the cheapest region once the smoker mix is equal; region is a weak price factor." |
| "Family size affects cost." | "Customers with 5 children average 8,786, but n = 18: too few to act on." |

---

# 🧰 Summary: Habit → SQL

| Habit | SQL |
|---|---|
| 1. Precise question | metric + grain + comparison → `SELECT … GROUP BY …` |
| 2. Size before average | `COUNT(*)` next to every `AVG`; bands; `HAVING COUNT(*) >= n` |
| 3. Baseline | `100 * AVG(x) / (SELECT AVG(x) FROM t)` → window functions next |
| 4. Mix | share per group: `AVG(flag::INTEGER)`; same-mix comparison |
| 5. Share | `SUM(x) FILTER (WHERE …) / SUM(x)` |
| 6. Distribution | `MEDIAN`, `quantile_cont(x, 0.25 / 0.75)` |

**Next:** window functions put the baseline, the rank and the share **on every row**.
