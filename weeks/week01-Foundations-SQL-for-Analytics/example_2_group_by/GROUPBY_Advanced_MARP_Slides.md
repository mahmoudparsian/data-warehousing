---
marp: true
theme: default
paginate: true
title: Advanced Teaching GROUP BY with DuckDB
author: Mahmoud Parsian
---

# 📊 Advanced GROUP BY with DuckDB

## Learning Objectives
- Master GROUP BY patterns
- Understand aggregation deeply
- Apply business thinking
- Use ranking (window functions)

---

# 🧱 Dataset (Small but Powerful)

- Transaction-level data
- Dimensions:
  - country
  - product
- Metric:
  - price

👉 Even small data can teach big concepts

---

# 🧠 Mental Model

## GROUP BY = "Split → Apply → Combine"

1. Split data into groups  
2. Apply aggregation  
3. Combine results  

---

# ❌ Without GROUP BY

```sql
SELECT SUM(price) FROM sales;
```

👉 Only one number → no insight

---

# ✅ With GROUP BY

```sql
SELECT country, SUM(price)
FROM sales
GROUP BY country;
```

👉 Insight per country

---

# 📊 Pattern 1: One Dimension

```sql
SELECT country, SUM(price)
FROM sales
GROUP BY country;
```

### Insight
- Market comparison
- Revenue distribution

---

# 📊 Pattern 2: Another Dimension

```sql
SELECT product, SUM(price)
FROM sales
GROUP BY product;
```

### Insight
- Product performance

---

# 📊 Pattern 3: Multi-Dimensional

```sql
SELECT country, product, SUM(price)
FROM sales
GROUP BY country, product;
```

### Insight
- Product performance within each country

---

# ⚠️ Common Mistake

```sql
SELECT country, product, SUM(price)
FROM sales
GROUP BY country;
```

❌ ERROR: product not in GROUP BY

---

# ✅ Correct Version

```sql
GROUP BY country, product
```

---

# 🔢 COUNT vs SUM

```sql
SELECT country, COUNT(*) FROM sales GROUP BY country;
```

vs

```sql
SELECT country, SUM(price) FROM sales GROUP BY country;
```

👉 Volume vs Value

---

# 📈 Business Thinking

| Metric | Meaning |
|------|--------|
| COUNT | activity |
| SUM | revenue |
| AVG | pricing |
| MAX | premium |

---

# 🏆 Top-N Problem

## Question:
Top product per country?

---

# ❌ GROUP BY Alone Can't Solve It

You need ranking

---

# ✅ Window Function Solution

```sql
SELECT *
FROM (
  SELECT country, product, SUM(price),
         RANK() OVER (PARTITION BY country ORDER BY SUM(price) DESC) rnk
  FROM sales
  GROUP BY country, product
) t
WHERE rnk = 1;
```

---

# 🧠 Insight

- GROUP BY → aggregates
- Window → compares within groups

---

# 🏆 Ranking Countries

```sql
SELECT country, SUM(price),
       RANK() OVER (ORDER BY SUM(price) DESC)
FROM sales
GROUP BY country;
```

---

# ⚠️ WHERE vs HAVING

## WHERE → before grouping  
## HAVING → after grouping

---

# ✅ Example

```sql
SELECT country, SUM(price)
FROM sales
GROUP BY country
HAVING SUM(price) > 1500;
```

---

# 🧠 Teaching Insight

> WHERE filters rows  
> HAVING filters groups  

---

# 📊 Analytical Questions

- Which country is strongest?
- Which product dominates?
- Which country-product combo wins?
- Who crosses threshold?

---

# 🧩 Real-World Mapping

| Concept | Real Use |
|--------|---------|
| GROUP BY country | regional sales |
| GROUP BY product | product strategy |
| HAVING | KPI thresholds |
| RANK | leaderboards |

---

# ⚡ Medallion Connection

- Bronze → raw data  
- Silver → cleaned  
- Gold → GROUP BY tables  

👉 Dashboards use Gold

---

# 🚀 Executive Thinking

GROUP BY enables:
- KPI dashboards
- reporting
- decision making

---

# 🎯 Final Takeaway

> GROUP BY transforms raw data into business insight

---

# 🧠 Bonus Exercise

1. Top 2 products per country  
2. Avg price per product  
3. Country with highest avg price  

---

# 🙌 End
