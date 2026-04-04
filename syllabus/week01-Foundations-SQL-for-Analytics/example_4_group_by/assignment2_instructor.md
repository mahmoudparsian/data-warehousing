---
marp: true
theme: default
paginate: true
title: Assignment 2 — Instructor Solutions
---

# Instructor Solutions

---

# Q1 Solution

```sql
SELECT *
FROM sales
WHERE country = 'USA'
  AND sales_amount > 1000;
```

**Insight**
- Filters rows before aggregation
- Useful for transaction-level analysis

---

# Q2 Solution

```sql
SELECT product_name, SUM(sales_amount) AS total_sales
FROM sales
WHERE country = 'USA'
GROUP BY product_name;
```

**Insight**
- WHERE filters before grouping
- Shows product performance in USA

---

# Q3 Solution

```sql
SELECT product_name, SUM(sales_amount) AS total_sales
FROM sales
GROUP BY product_name
HAVING SUM(sales_amount) > 1000000;
```

**Insight**
- HAVING filters AFTER aggregation
- Identifies high-performing products

---

# Q4 Solution

```sql
SELECT country, SUM(sales_amount) AS total_sales
FROM sales
WHERE EXTRACT(YEAR FROM transaction_date) = 2025
GROUP BY country
HAVING SUM(sales_amount) > 5000000;
```

**Insight**
- WHERE filters rows (year)
- HAVING filters groups (sales threshold)

---

# Q5 Solution (Top-N)

```sql
SELECT country, product_name, total_sales
FROM (
    SELECT 
        country,
        product_name,
        SUM(sales_amount) AS total_sales,
        ROW_NUMBER() OVER (
            PARTITION BY country
            ORDER BY SUM(sales_amount) DESC
        ) AS rn
    FROM sales
    GROUP BY country, product_name
) t
WHERE rn <= 3;
```

**Insight**
- Uses window function for per-group ranking
- Essential for “Top-N per category” problems
