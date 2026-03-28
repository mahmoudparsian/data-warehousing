---
marp: true
title: Week 2 — Window Functions (Elite Deep Dive)
paginate: true
theme: default
class: lead
---

# Window Functions — Deep Dive

---

# 🎯 Learning Goals

- Master window functions conceptually  
- Apply ranking, aggregation, and comparison  
- Solve real analytical problems  

---

# 🧠 What Makes Window Functions Powerful?

- Combine row-level + aggregated insight  
- Avoid losing detail like GROUP BY  
- Enable advanced analytics in one query  

---

# 📊 Example: Global Average

```sql
SELECT *,
       AVG(charges) OVER () AS overall_avg
FROM insurance;
```

- Adds benchmark to every row  
- Enables comparison  
- Useful for performance analysis  

👉 Insight: Who is above average?

---

# 📊 Example: Regional Average

```sql
SELECT *,
       AVG(charges) OVER (PARTITION BY region) AS regional_avg
FROM insurance;
```

- Context-aware metric  
- Compares within group  
- More meaningful than global  

👉 Insight: Compare fairly within region

---

# 📊 Example: Difference from Average

```sql
SELECT *,
       charges - AVG(charges) OVER (PARTITION BY region) AS diff
FROM insurance;
```

- Measures deviation  
- Identifies anomalies  
- Useful for outlier detection  

👉 Insight: Who deviates most?

---

# 📊 Example: Percentage of Total

```sql
SELECT *,
       charges / SUM(charges) OVER () AS pct_total
FROM insurance;
```

- Shows contribution  
- Helps prioritize  
- Enables Pareto analysis  

👉 Insight: Who drives most revenue?

---

# 📊 Example: Running Total

```sql
SELECT age, charges,
       SUM(charges) OVER (ORDER BY age) AS running_total
FROM insurance;
```

- Accumulates values  
- Shows progression  
- Useful for trends  

👉 Insight: Growth over dimension

---

# 📊 Example: Moving Average

```sql
SELECT age, charges,
       AVG(charges) OVER (ORDER BY age ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg
FROM insurance;
```

- Smooths fluctuations  
- Reveals trends  
- Used in finance  

👉 Insight: Local trends matter

---

# 📊 Example: Rank by Region

```sql
SELECT *,
       RANK() OVER (PARTITION BY region ORDER BY charges DESC) AS rnk
FROM insurance;
```

- Ranking within groups  
- Identifies leaders  
- Enables segmentation  

👉 Insight: Top performers per region

---

# 📊 Example: Dense Rank

```sql
DENSE_RANK() OVER (PARTITION BY region ORDER BY charges DESC)
```

- No gaps  
- Better readability  
- Used in dashboards  

👉 Insight: Cleaner ranking

---

# 📊 Example: Row Number

```sql
ROW_NUMBER() OVER (PARTITION BY region ORDER BY charges DESC)
```

- Unique ordering  
- No ties  
- Perfect for Top-N  

👉 Insight: Strict selection

---

# 📊 Example: Top-N per Group

```sql
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY region ORDER BY charges DESC) AS rn
    FROM insurance
) t
WHERE rn <= 3;
```

- Real-world pattern  
- Segmented ranking  
- High business value  

👉 Insight: Target top customers

---

# 📊 Example: Lag Function

```sql
SELECT age, charges,
       LAG(charges) OVER (ORDER BY age) AS prev_charge
FROM insurance;
```

- Access previous row  
- Enables comparison  
- Used in time-series  

👉 Insight: Change detection

---

# 📊 Example: Lead Function

```sql
SELECT age, charges,
       LEAD(charges) OVER (ORDER BY age) AS next_charge
FROM insurance;
```

- Looks ahead  
- Predictive context  
- Useful in forecasting  

👉 Insight: Future comparison

---

# 📊 Example: Ranking + Filter

```sql
SELECT *
FROM (
    SELECT *,
           RANK() OVER (ORDER BY charges DESC) AS rnk
    FROM insurance
) t
WHERE rnk <= 10;
```

- Global ranking  
- Identifies top entities  
- Simple but powerful  

👉 Insight: Identify top performers

---

# 🧠 Key Patterns

- Compare vs average  
- Rank within groups  
- Measure contribution  
- Detect trends  

---

# 🎯 Business Applications

- Customer segmentation  
- Fraud detection  
- Pricing optimization  
- Marketing targeting  

---

# ⚠️ Common Mistakes

- Forgetting PARTITION BY  
- Using RANK instead of ROW_NUMBER  
- Misinterpreting results  

---

# 🎯 Final Summary

- Window functions = advanced analytics  
- Preserve detail + add insight  
- Essential for real-world SQL  

---

# 💡 Final Thought

👉 “Window functions turn SQL into analytics”
