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

| region | n |
|---|---|
| southeast | 88 |
| northeast | 68 |
| northwest | 61 |

---

# ⚠️ Common Error

```sql
SELECT region, AVG(charges)
FROM insurance
WHERE AVG(charges) > 13000     -- ❌ error
GROUP BY region;
```

DuckDB: *WHERE clause cannot contain aggregates!*

✅ Move the condition to `HAVING AVG(charges) > 13000`.

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

| bmi_class | n | avg_charges |
|---|---|---|
| 1 underweight | 20 | 8,852 |
| 2 normal | 225 | 10,409 |
| 3 overweight | 386 | 10,988 |
| 4 obese | 707 | 15,552 |

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

| age | gender | charges |
|---|---|---|
| 54 | female | 63,770 |
| 45 | male | 62,593 |
| 52 | male | 60,021 |

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

southeast **30.2%** · northeast 24.5 · northwest 22.7 · southwest 22.6

- The inner `SELECT` (a *subquery*) computes the grand total once
- Use `100.0` (not `100`) so the result is a decimal

---

# 🧮 Bonus: Conditional Counts with FILTER

```sql
SELECT COUNT(*) FILTER (WHERE smoker)  AS smokers,
       COUNT(*)                        AS total,
       ROUND(100.0 * COUNT(*) FILTER (WHERE smoker) / COUNT(*), 1) AS pct
FROM insurance;
```

→ 274 smokers of 1,338 = **20.5%**

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
