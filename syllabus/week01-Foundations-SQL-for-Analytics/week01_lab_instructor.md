# Week 1 Lab — Instructor Version (Detailed Solutions)

## 🎯 Teaching Notes
Focus on:
- Question → SQL → Insight
- Always ask students: “Why does this matter?”

---

## Part 1 — Exploration

### Solution 1
```sql
SELECT * FROM insurance LIMIT 10;
```

👉 Explanation:
Previewing data helps understand structure before analysis.

---

### Solution 2
```sql
SELECT age, region, charges FROM insurance;
```

👉 Explanation:
Selecting only needed columns improves clarity and performance.

---

## Part 2 — Filtering

### Solution 3
```sql
SELECT * FROM insurance WHERE smoker = 'yes';
```

👉 Insight:
Smokers represent higher-risk individuals.

---

### Solution 4
```sql
SELECT * FROM insurance WHERE charges > 15000;
```

👉 Insight:
Identifies high-cost customers (important for pricing).

---

## Part 3 — Aggregation

### Solution 5
```sql
SELECT region, AVG(charges)
FROM insurance
GROUP BY region;
```

👉 Insight:
Compare cost across regions.

---

### Solution 6
```sql
SELECT smoker, AVG(charges)
FROM insurance
GROUP BY smoker;
```

👉 Insight:
Smokers clearly cost more → strong business signal.

---

### Solution 7
```sql
SELECT region, COUNT(*)
FROM insurance
GROUP BY region;
```

👉 Insight:
Distribution matters — more data ≠ higher cost.

---

## Part 4 — Multi-Dimensional Analysis

### Solution 8
```sql
SELECT region, smoker, AVG(charges)
FROM insurance
GROUP BY region, smoker;
```

👉 Insight:
Combining variables reveals deeper patterns.

---

## Part 5 — Challenge

### Solution 9
```sql
SELECT *
FROM insurance
WHERE smoker = 'yes' AND bmi > 30;
```

👉 Insight:
High BMI + smoking = high-risk segment.

---

## 🧠 Instructor Tips

- Always ask “Why?”
- Push students beyond syntax
- Focus on interpretation

---

## 🎯 Key Takeaway

SQL is not about queries  
👉 It is about thinking and decision-making
