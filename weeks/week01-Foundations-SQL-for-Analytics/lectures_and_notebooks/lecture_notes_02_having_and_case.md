---
marp: true
title: Week 1 — Session 2 — GROUP BY in Depth (HAVING, CASE, Top-N, % of Total)
paginate: true
theme: default
class: lead
---

# Week 1 — Session 2
## GROUP BY in Depth: HAVING · CASE · Top-N · % of Total

---

# 🎯 Today

- `WHERE` vs `HAVING`: filter **rows** vs filter **groups**
- `CASE`: build your own segments
- `ORDER BY … LIMIT`: top-N questions
- Percent of total: "what share comes from …?"

👉 Then: **Lab 1.2** on 400,000 sales transactions

---

# 🔧 Setup: the Same Table as Session 1

```sql
CREATE OR REPLACE TABLE insurance AS
SELECT * FROM read_csv('../example_1_insurance/insurance.csv');
```

Reminder: `smoker` is **BOOLEAN** (`true` / `false`), so `WHERE smoker` means "smokers only".

---

# 🧠 Full Execution Order

1. `FROM`: pick the table
2. `WHERE`: keep some **rows**
3. `GROUP BY`: make groups
4. `HAVING`: keep some **groups**
5. `SELECT`: compute output columns
6. `ORDER BY` → `LIMIT`

👉 `WHERE` runs **before** groups exist, so it cannot use `AVG()`, `COUNT()`, …

---

# 📊 WHERE + HAVING Together

**Question:** Which regions have more than 60 customers with charges above 20,000?

```sql
SELECT region, COUNT(*) AS n
FROM insurance
WHERE charges > 20000        -- rows
GROUP BY region
HAVING COUNT(*) > 60         -- groups
ORDER BY n DESC;
```

<!-- RESULT -->

| region    |  n |
|-----------|---:|
| southeast | 88 |
| northeast | 68 |
| northwest | 61 |

*(3 rows)*

<!-- /RESULT -->

👉 The southwest's 56 such customers passed `WHERE`, but its group was removed by `HAVING` (56 is not > 60).

---

# ⚠️ Common Error

```sql
SELECT region, AVG(charges)
FROM insurance
WHERE AVG(charges) > 13000     -- ❌ error
GROUP BY region;
```

<!-- ERROR -->

```text
Binder Error: WHERE clause cannot contain aggregates!

LINE 3: WHERE AVG(charges) > 13000     -- ❌ error
              ^^^^^^^^^^^^
```

<!-- /ERROR -->

✅ Move the condition to `HAVING AVG(charges) > 13000`: `WHERE` runs **before** the groups exist.

---

# 🧩 CASE: Build Segments

**Question:** Does BMI class change cost?

```sql
SELECT CASE WHEN bmi < 18.5 THEN '1 underweight'
            WHEN bmi < 25   THEN '2 normal'
            WHEN bmi < 30   THEN '3 overweight'
            ELSE                 '4 obese'
       END                       AS bmi_class,
       COUNT(*)                  AS n,
       ROUND(AVG(charges), 0)    AS avg_charges
FROM insurance
GROUP BY bmi_class
ORDER BY bmi_class;
```

---

# 💡 CASE: Result

<!-- RESULT -->

| bmi_class     |   n | avg_charges |
|---------------|----:|------------:|
| 1 underweight |  20 |      8852.0 |
| 2 normal      | 225 |     10409.0 |
| 3 overweight  | 386 |     10988.0 |
| 4 obese       | 707 |     15552.0 |

*(4 rows)*

<!-- /RESULT -->

- `CASE` conditions are checked **top to bottom**; the first match wins
- Number prefixes (`1 …`, `2 …`) make `ORDER BY` sort in a sensible order
- Insight: the big jump is at **obese** (+42% vs overweight)

---

# 🏆 Top-N

**Question:** Who are the 3 most expensive customers?

```sql
SELECT age, gender, ROUND(charges, 0) AS charges
FROM insurance
ORDER BY charges DESC
LIMIT 3;
```

<!-- RESULT -->

| age | gender | charges |
|----:|--------|--------:|
|  54 | female | 63770.0 |
|  45 | male   | 62593.0 |
|  52 | male   | 60021.0 |

*(3 rows)*

<!-- /RESULT -->

👉 Top-N **per group** ("top product per country") needs window functions: **week 2**.

---

# 📊 Percent of Total

**Question:** What share of total charges comes from each region?

```sql
SELECT region,
       ROUND(100.0 * SUM(charges)
             / (SELECT SUM(charges) FROM insurance), 1) AS pct_of_total
FROM insurance
GROUP BY region
ORDER BY pct_of_total DESC;
```

<!-- RESULT -->

| region    | pct_of_total |
|-----------|-------------:|
| southeast |         30.2 |
| northeast |         24.5 |
| northwest |         22.7 |
| southwest |         22.6 |

*(4 rows)*

<!-- /RESULT -->

- The inner `SELECT` (a *subquery*) computes the grand total once
- Write `100.0`, not `100`: in PostgreSQL or SQL Server, an integer divided by an integer drops the decimals (DuckDB's `/` always keeps them)

---

# 🧮 Bonus: Conditional Counts with FILTER

```sql
SELECT COUNT(*) FILTER (WHERE smoker)  AS smokers,
       COUNT(*)                        AS total,
       ROUND(100.0 * COUNT(*) FILTER (WHERE smoker) / COUNT(*), 1) AS pct
FROM insurance;
```

<!-- RESULT -->

| smokers | total |  pct |
|--------:|------:|-----:|
|     274 |  1338 | 20.5 |

*(1 row)*

<!-- /RESULT -->

👉 Same as `SUM(CASE WHEN smoker THEN 1 ELSE 0 END)`, but shorter.

---

# ✅ Summary

| Need | Tool |
|---|---|
| Filter rows | `WHERE` |
| Filter groups | `HAVING` |
| Make your own categories | `CASE WHEN … END` |
| Best / worst N | `ORDER BY … LIMIT N` |
| Share of the whole | `100.0 * part / (SELECT total)` |

👉 Now: **Lab 1.2** (30 minutes)
