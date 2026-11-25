---
marp: true
title: Week 2 — Window Functions
paginate: true
theme: default
class: lead
---

# Week 2
## Window Functions: Compare Each Row with Its Group

`OVER()` · `PARTITION BY` · ranking · top-N per group · running totals · `LAG` · shares

---

# 🎯 Learning Goals

By the end of this session you can:

- explain why `GROUP BY` **collapses** rows and `OVER()` **keeps** them
- put a group value (average, total, rank) **next to each row** with `PARTITION BY`
- choose between `ROW_NUMBER`, `RANK` and `DENSE_RANK`, and solve **top-N per group**
- filter on a window result with `QUALIFY`
- compute running totals, moving averages and `LAG` / `LEAD` changes **on the right grain**
- compute shares of a total (Pareto: "the top 10% cause …%")

---

# 🔧 Setup

```sql
CREATE OR REPLACE TABLE insurance AS
SELECT * FROM read_csv('../week01-Foundations-SQL-for-Analytics/example_1_insurance/insurance.csv');
```

Same 1,338 customers as in week 1 and in the analytical-thinking deck.

---

# 🧠 `GROUP BY` Collapses, `OVER()` Keeps

```sql
SELECT region, ROUND(AVG(charges), 0) AS regional_avg
FROM insurance
GROUP BY region
ORDER BY region;
```

<!-- RESULT -->

| region    | regional_avg |
|-----------|-------------:|
| northeast |      13406.0 |
| northwest |      12418.0 |
| southeast |      14735.0 |
| southwest |      12347.0 |

*(4 rows)*

<!-- /RESULT -->

```sql
SELECT region, age, ROUND(charges, 0) AS charges,
       ROUND(AVG(charges) OVER (PARTITION BY region), 0) AS regional_avg
FROM insurance
ORDER BY charges DESC
LIMIT 4;
```

<!-- RESULT -->

| region    | age | charges | regional_avg |
|-----------|----:|--------:|-------------:|
| southeast |  54 | 63770.0 |      14735.0 |
| southeast |  45 | 62593.0 |      14735.0 |
| northwest |  52 | 60021.0 |      12418.0 |
| northeast |  31 | 58571.0 |      13406.0 |

*(4 rows)*

<!-- /RESULT -->

👉 4 rows vs **1,338 rows**: every customer keeps its row and gets its region's average **next to it**.

---

# 📊 `OVER ()`: One Window = the Whole Table

```sql
SELECT age, smoker, ROUND(charges, 0) AS charges,
       ROUND(AVG(charges) OVER (), 0)                    AS overall_avg,
       ROUND(charges - AVG(charges) OVER (), 0)          AS diff,
       ROUND(100 * charges / AVG(charges) OVER ())       AS index_vs_all
FROM insurance
ORDER BY charges DESC
LIMIT 5;
```

<!-- RESULT -->

| age | smoker | charges | overall_avg |    diff | index_vs_all |
|----:|--------|--------:|------------:|--------:|-------------:|
|  54 | true   | 63770.0 |     13270.0 | 50500.0 |        481.0 |
|  45 | true   | 62593.0 |     13270.0 | 49322.0 |        472.0 |
|  52 | true   | 60021.0 |     13270.0 | 46751.0 |        452.0 |
|  31 | true   | 58571.0 |     13270.0 | 45301.0 |        441.0 |
|  33 | true   | 55135.0 |     13270.0 | 41865.0 |        415.0 |

*(5 rows)*

<!-- /RESULT -->

💡 The most expensive customer costs **4.8×** the average customer (index 481). The baseline from the analytical-thinking deck, now on every row, with no subquery.

---

# 📊 `PARTITION BY`: One Window per Group

Who is furthest above **their own region's** average?

```sql
SELECT region, age, smoker, ROUND(charges, 0) AS charges,
       ROUND(AVG(charges) OVER (PARTITION BY region), 0)            AS regional_avg,
       ROUND(charges - AVG(charges) OVER (PARTITION BY region), 0)  AS diff_from_region
FROM insurance
ORDER BY diff_from_region DESC
LIMIT 5;
```

<!-- RESULT -->

| region    | age | smoker | charges | regional_avg | diff_from_region |
|-----------|----:|--------|--------:|-------------:|-----------------:|
| southeast |  54 | true   | 63770.0 |      14735.0 |          49035.0 |
| southeast |  45 | true   | 62593.0 |      14735.0 |          47857.0 |
| northwest |  52 | true   | 60021.0 |      12418.0 |          47604.0 |
| northeast |  31 | true   | 58571.0 |      13406.0 |          45165.0 |
| northwest |  33 | true   | 55135.0 |      12418.0 |          42718.0 |

*(5 rows)*

<!-- /RESULT -->

`PARTITION BY region` = "compute the average separately for each region". Without it, every row gets the overall average.

---

# 🚫 You Cannot Filter a Window in `WHERE`

```sql
SELECT region, charges
FROM insurance
WHERE charges > AVG(charges) OVER (PARTITION BY region);
```

<!-- ERROR -->

```text
Binder Error: WHERE clause cannot contain window functions!

LINE 3: WHERE charges > AVG(charges) OVER (PARTITION BY region);
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

<!-- /ERROR -->

`WHERE` runs **before** windows are computed. Two fixes: a subquery, or DuckDB's **`QUALIFY`** (a `WHERE` for window results):

```sql
SELECT region, COUNT(*) AS above_regional_avg
FROM (SELECT region, charges,
             AVG(charges) OVER (PARTITION BY region) AS regional_avg
      FROM insurance)
WHERE charges > regional_avg
GROUP BY region
ORDER BY region;
```

<!-- RESULT -->

| region    | above_regional_avg |
|-----------|-------------------:|
| northeast |                109 |
| northwest |                106 |
| southeast |                116 |
| southwest |                 97 |

*(4 rows)*

<!-- /RESULT -->

💡 Only about **1 customer in 3** is above their region's average: the right-skewed charges pull every average up.

---

# 📊 Share of the Total

```sql
SELECT region,
       ROUND(SUM(charges), 0)                                   AS region_total,
       ROUND(100 * SUM(charges) / SUM(SUM(charges)) OVER (), 1) AS pct_of_total
FROM insurance
GROUP BY region
ORDER BY pct_of_total DESC;
```

<!-- RESULT -->

| region    | region_total | pct_of_total |
|-----------|-------------:|-------------:|
| southeast |    5363690.0 |         30.2 |
| northeast |    4343669.0 |         24.5 |
| northwest |    4035712.0 |         22.7 |
| southwest |    4012755.0 |         22.6 |

*(4 rows)*

<!-- /RESULT -->

- `SUM(SUM(charges)) OVER ()`: the inner `SUM` is the `GROUP BY` total per region; the outer `SUM … OVER ()` adds up those 4 rows.
- Multiply by **100** to get percent: `charges / SUM(charges) OVER ()` alone is a fraction (0.30, not 30).

---

# 🏅 Ranking: `ROW_NUMBER` vs `RANK` vs `DENSE_RANK`

Northwest smokers aged 55 or older, by number of children (ties!):

```sql
SELECT age, children, ROUND(charges, 0) AS charges,
       ROW_NUMBER() OVER (ORDER BY children DESC, charges DESC) AS row_number,
       RANK()       OVER (ORDER BY children DESC)               AS rank,
       DENSE_RANK() OVER (ORDER BY children DESC)               AS dense_rank
FROM insurance
WHERE region = 'northwest' AND smoker AND age >= 55
ORDER BY row_number;
```

<!-- RESULT -->

| age | children | charges | row_number | rank | dense_rank |
|----:|---------:|--------:|-----------:|-----:|-----------:|
|  62 |        3 | 46718.0 |          1 |    1 |          1 |
|  60 |        3 | 46131.0 |          2 |    1 |          1 |
|  58 |        2 | 47496.0 |          3 |    3 |          2 |
|  61 |        1 | 28869.0 |          4 |    4 |          3 |
|  56 |        1 | 26109.0 |          5 |    4 |          3 |
|  56 |        0 | 43921.0 |          6 |    6 |          4 |
|  57 |        0 | 43579.0 |          7 |    6 |          4 |
|  64 |        0 | 29331.0 |          8 |    6 |          4 |
|  61 |        0 | 29141.0 |          9 |    6 |          4 |
|  63 |        0 | 28950.0 |         10 |    6 |          4 |
|  59 |        0 | 25679.0 |         11 |    6 |          4 |

*(11 rows)*

<!-- /RESULT -->

| Function | Ties get | After a tie |
|---|---|---|
| `ROW_NUMBER` | different numbers (add a **tie-breaker** column!) | 1, 2, 3, 4 |
| `RANK` | the same number | skips: 1, 1, 3 |
| `DENSE_RANK` | the same number | no gap: 1, 1, 2 |

---

# 🏆 Top-N per Group

The 2 most expensive customers in each region:

```sql
SELECT region, age, smoker, bmi, ROUND(charges, 0) AS charges
FROM insurance
QUALIFY ROW_NUMBER() OVER (PARTITION BY region ORDER BY charges DESC) <= 2
ORDER BY region, charges DESC;
```

<!-- RESULT -->

| region    | age | smoker |    bmi | charges |
|-----------|----:|--------|-------:|--------:|
| northeast |  31 | true   | 38.095 | 58571.0 |
| northeast |  54 | true   | 40.565 | 48549.0 |
| northwest |  52 | true   | 34.485 | 60021.0 |
| northwest |  33 | true   |  35.53 | 55135.0 |
| southeast |  54 | true   |  47.41 | 63770.0 |
| southeast |  45 | true   |  30.36 | 62593.0 |
| southwest |  60 | true   |   32.8 | 52591.0 |
| southwest |  28 | true   |   36.4 | 51195.0 |

*(8 rows)*

<!-- /RESULT -->

- `ROW_NUMBER` gives **exactly** N per group; with `RANK`, a tie on place N gives **more** than N rows.
- Without `QUALIFY`: wrap it in a subquery and filter `WHERE rn <= 2` (works in every database).
- 💡 All 8 are smokers with a BMI above 30.

---

# ⚠️ Ordered Windows: Ties Give Surprises

A running total over **customers**, ordered by `age`:

```sql
SELECT age, ROUND(charges, 0) AS charges,
       ROUND(SUM(charges) OVER (ORDER BY age), 0) AS running_total
FROM insurance
ORDER BY age, charges
LIMIT 4;
```

<!-- RESULT -->

| age | charges | running_total |
|----:|--------:|--------------:|
|  18 |  1122.0 |      488949.0 |
|  18 |  1132.0 |      488949.0 |
|  18 |  1136.0 |      488949.0 |
|  18 |  1136.0 |      488949.0 |

*(4 rows)*

<!-- /RESULT -->

- All four rows show the **same** running total: with `ORDER BY`, the default frame is `RANGE … CURRENT ROW`, which includes **every row with the same age** (69 customers are 18).
- And "the previous customer" (`LAG`) would be an arbitrary 18-year-old.

👉 Fix: make the order **unique**, usually by aggregating first to **one row per step** (next slide).

---

# 📈 Aggregate First, Then Window

One row per age → running total, moving average and change are meaningful:

```sql
SELECT age,
       COUNT(*)                                                        AS customers,
       ROUND(AVG(charges), 0)                                          AS avg_charges,
       ROUND(AVG(AVG(charges)) OVER (ORDER BY age
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 0)          AS moving_avg_3,
       ROUND(AVG(charges) - LAG(AVG(charges)) OVER (ORDER BY age), 0)  AS change_vs_prev_age,
       SUM(COUNT(*)) OVER (ORDER BY age)                               AS running_customers
FROM insurance
WHERE age BETWEEN 55 AND 64
GROUP BY age
ORDER BY age;
```

<!-- RESULT -->

| age | customers | avg_charges | moving_avg_3 | change_vs_prev_age | running_customers |
|----:|----------:|------------:|-------------:|-------------------:|------------------:|
|  55 |        26 |     16165.0 |      16165.0 |               NULL |                26 |
|  56 |        26 |     15026.0 |      15595.0 |            -1139.0 |                52 |
|  57 |        26 |     16447.0 |      15879.0 |             1422.0 |                78 |
|  58 |        25 |     13879.0 |      15117.0 |            -2568.0 |               103 |
|  59 |        25 |     18896.0 |      16407.0 |             5017.0 |               128 |
|  60 |        23 |     21979.0 |      18251.0 |             3084.0 |               151 |
|  61 |        23 |     22024.0 |      20967.0 |               45.0 |               174 |
|  62 |        23 |     19164.0 |      21056.0 |            -2861.0 |               197 |
|  63 |        23 |     19885.0 |      20358.0 |              721.0 |               220 |
|  64 |        22 |     23276.0 |      20775.0 |             3391.0 |               242 |

*(10 rows)*

<!-- /RESULT -->

- `LAG(x)` = x from the **previous** row in the window order (`LEAD(x)` = the next); the first row gets NULL.
- 💡 Single ages jump up and down (−2,568, then +5,017); the 3-age moving average climbs more smoothly, from about 16,000 at 55–57 to about 21,000 at 61–64.

---

# 📊 Pareto: Who Causes Most of the Cost?

`NTILE(10)` splits the customers, most expensive first, into 10 equal groups (deciles):

```sql
SELECT decile,
       COUNT(*)                                                         AS customers,
       ROUND(100 * SUM(charges) / SUM(SUM(charges)) OVER (), 1)         AS pct_of_charges,
       ROUND(100 * SUM(SUM(charges)) OVER (ORDER BY decile)
                 / SUM(SUM(charges)) OVER (), 1)                        AS cumulative_pct
FROM (SELECT charges, NTILE(10) OVER (ORDER BY charges DESC) AS decile
      FROM insurance)
GROUP BY decile
ORDER BY decile
LIMIT 4;
```

<!-- RESULT -->

| decile | customers | pct_of_charges | cumulative_pct |
|-------:|----------:|---------------:|---------------:|
|      1 |       134 |           32.0 |           32.0 |
|      2 |       134 |           19.7 |           51.7 |
|      3 |       134 |           12.6 |           64.3 |
|      4 |       134 |            9.4 |           73.7 |

*(4 rows)*

<!-- /RESULT -->

💡 The most expensive **10%** of customers cause **32%** of all charges, and the top **20%** cause more than **half** (51.7%).

---

# ⚠️ Common Mistakes

| Mistake | What you see | Fix |
|---|---|---|
| Forget `PARTITION BY` | every row gets the **overall** value | `OVER (PARTITION BY group)` |
| `ROW_NUMBER` on ties without a tie-breaker | a different "winner" on each run | `ORDER BY charges DESC, id` |
| `RANK` for "exactly top N" | more than N rows when there is a tie | `ROW_NUMBER` (or say "ties included") |
| Window in `WHERE` | error | `QUALIFY` or a subquery |
| Running total / `LAG` on a non-unique order | equal running totals, random "previous row" | aggregate first: one row per step |
| Share without `100 *` | 0.30 instead of 30 | `100 * x / SUM(x) OVER ()` |

---

# 🧰 Summary

| Need | Window |
|---|---|
| Overall value on every row | `AVG(x) OVER ()` |
| Group value on every row | `AVG(x) OVER (PARTITION BY g)` |
| Rank within a group | `ROW_NUMBER / RANK / DENSE_RANK() OVER (PARTITION BY g ORDER BY x DESC)` |
| Top N per group | `QUALIFY ROW_NUMBER() OVER (…) <= N` |
| Share of total | `100 * SUM(x) / SUM(SUM(x)) OVER ()` |
| Running total | `SUM(x) OVER (ORDER BY step)` (one row per step!) |
| Moving average | `AVG(x) OVER (ORDER BY step ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)` |
| Change vs previous | `x - LAG(x) OVER (ORDER BY step)` |
| Deciles | `NTILE(10) OVER (ORDER BY x DESC)` |

👉 Now: **Lab 2.1** (30 minutes). Practice notebook: `notebook_01_window_functions_practice.py`.
