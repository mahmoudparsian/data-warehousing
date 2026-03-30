# Week 2 Lab — Student Version (Detailed)
## SQL, Analytical Thinking, and Window Functions

## 1) Lab Purpose

This lab helps you move from basic SQL syntax to analytical reasoning.

By the end of this lab, you should be able to:

- explain why a business question comes before a SQL query
- choose between `GROUP BY` and window functions
- use `PARTITION BY` to analyze data inside segments
- solve Top-N per group problems
- interpret results in business terms

---

## 2) Dataset

We use the `insurance` table built from `insurance.csv`.

Columns:

- `age`
- `gender`
- `bmi`
- `children`
- `smoker`
- `region`
- `charges`

Think of each row as one customer and `charges` as the business outcome we want to understand.

---

## 3) Big Idea for This Week

Last week, you learned that:

- `SELECT` asks questions
- `WHERE` filters
- `GROUP BY` summarizes

This week, you will learn a more advanced idea:

> Sometimes we want to **keep the original rows** and still add group-level insight.

That is exactly why window functions matter.

---

## 4) Before You Start

For each task:

1. Read the business question carefully.
2. Think about whether you need:
   - filtering
   - grouping
   - ranking
   - comparison to an average
3. Write your SQL.
4. Interpret the result in plain English.

Do not stop at “the query runs.”  
The real goal is: **What does the result mean?**

---

# Part A — Review and Analytical Thinking

## Task 1 — Regional Average Charges

### Business Question
Which regions have higher average insurance charges?

### Why this matters
A business often wants to compare geographic markets.  
Average charges can help identify expensive regions.

### Your task
Write a query to compute the average `charges` for each `region`.

### Hint
Use:

- `AVG(charges)`
- `GROUP BY region`

### Reflection
After you run the query, answer:

- Which region is highest?
- Which region is lowest?
- Why might geography matter?

---

## Task 2 — Smoker vs Non-Smoker

### Business Question
Do smokers cost more than non-smokers?

### Why this matters
This is a classic risk segmentation question.

### Your task
Write a query to compute average charges by `smoker`.

### Reflection
After you run the query, answer:

- Is the difference large or small?
- What might this imply for pricing?
- Why is this a useful segmentation variable?

---

## Task 3 — Region + Smoker

### Business Question
Does the smoker effect look the same in every region?

### Why this matters
Averages across the whole dataset can hide local patterns.  
A business may need region-specific strategy.

### Your task
Write a query to calculate average charges by both:

- `region`
- `smoker`

### Reflection
After you run the query, answer:

- Is the smoker effect visible in every region?
- Are some region/smoker combinations much more expensive?
- What action could a business take?

---

# Part B — Why GROUP BY Is Not Enough

## Task 4 — Find the Top 5 Most Expensive Customers Overall

### Business Question
Who are the highest-cost customers in the whole dataset?

### Why this matters
Businesses often want to identify:

- extreme cases
- premium customers
- costly risk segments

### Your task
Write a query to return the top 5 customers by `charges`.

### Hint
Use:

- `ORDER BY charges DESC`
- `LIMIT 5`

### Reflection
After you run the query, answer:

- Do the top customers seem to share patterns?
- Do you notice smoking or BMI patterns?
- Why are outliers important?

---

## Task 5 — The Real Problem: Top 3 Customers per Region

### Business Question
Who are the top 3 most expensive customers **inside each region**?

### Why this matters
This is a real analytical pattern.  
The business does not just want the top customers overall.  
It wants the top customers **within each segment**.

### Why `GROUP BY` is not enough
`GROUP BY` collapses rows.  
But here, you need to keep individual customer rows and still rank them.

### Your task
Use a window function to assign a row number within each region and keep only the top 3.

### Hint
You will need:

- `ROW_NUMBER()`
- `OVER (...)`
- `PARTITION BY region`
- `ORDER BY charges DESC`

### Reflection
After you run the query, answer:

- Why is `ROW_NUMBER()` appropriate here?
- Why would `GROUP BY` be the wrong tool?
- How could a company use this result?

---

# Part C — Core Window Functions

## Task 6 — Add the Regional Average to Every Row

### Business Question
How does each customer compare with the average customer in their region?

### Why this matters
A business often wants to compare a specific customer against the normal level of their group.

### Your task
Write a query that returns all rows and adds a new column:

- `regional_avg`

This column should contain the average `charges` for that customer’s region.

### Hint
Use:

```sql
AVG(charges) OVER (PARTITION BY region)
```

### Reflection
After you run the query, answer:

- Why is this more informative than a plain `GROUP BY` query?
- What new comparison can you now make?
- Why is keeping row-level detail valuable?

---

## Task 7 — Customers Above Their Regional Average

### Business Question
Which customers are more expensive than the average customer in their own region?

### Why this matters
This identifies customers who are above normal for their group.

### Your task
Using a subquery or CTE, return only rows where:

- `charges > regional_avg`

### Reflection
After you run the query, answer:

- Which regions have many above-average customers?
- What kinds of customers appear in this result?
- Why is “above average” more meaningful than just “high”?

---

## Task 8 — Difference from Regional Average

### Business Question
How far above or below average is each customer in their region?

### Why this matters
It is useful to measure distance from a benchmark, not just whether someone is above it.

### Your task
Create a calculated column like:

```sql
charges - AVG(charges) OVER (PARTITION BY region)
```

Call it something like `diff_from_regional_avg`.

### Reflection
After you run the query, answer:

- Who is far above average?
- Who is far below average?
- Why is this useful in anomaly detection?

---

# Part D — Ranking Functions

## Task 9 — Use RANK()

### Business Question
What is each customer’s rank by charges inside their region?

### Why this matters
Rank tells us position within a segment.

### Your task
Use:

- `RANK() OVER (PARTITION BY region ORDER BY charges DESC)`

### Reflection
After you run the query, answer:

- What happens when there are ties?
- Why can ranks skip numbers?
- When is this acceptable?

---

## Task 10 — Use DENSE_RANK()

### Business Question
How is `DENSE_RANK()` different from `RANK()`?

### Why this matters
Students often confuse these two functions.

### Your task
Write a query using:

- `DENSE_RANK() OVER (PARTITION BY region ORDER BY charges DESC)`

### Reflection
After you run the query, answer:

- How is the numbering different?
- Why might a dashboard prefer `DENSE_RANK()`?
- When is this easier to explain to users?

---

## Task 11 — Use ROW_NUMBER()

### Business Question
How is `ROW_NUMBER()` different from both `RANK()` and `DENSE_RANK()`?

### Why this matters
This is often the best function for exact Top-N tasks.

### Your task
Write a query using:

- `ROW_NUMBER() OVER (PARTITION BY region ORDER BY charges DESC)`

### Reflection
After you run the query, answer:

- Why does it produce unique numbers?
- Why is this useful for exact Top-N selection?
- When is tie handling less important than strict row selection?

---

## Task 12 — Compare All Three

### Business Question
What is the practical difference between:

- `RANK()`
- `DENSE_RANK()`
- `ROW_NUMBER()`

### Your task
Write one query that shows all three ranking columns side by side.

### Reflection
After you run the query, answer:

- Which function is best for reporting?
- Which is best for exact selection?
- Which is easiest to explain to a manager?

---

# Part E — Contribution and Running Analytics

## Task 13 — Contribution to Total Charges

### Business Question
How much does each customer contribute to the total charges of the whole dataset?

### Why this matters
Businesses often want to know who contributes most to revenue or cost.

### Your task
Create a column like:

```sql
charges / SUM(charges) OVER ()
```

Name it `pct_total`.

### Reflection
After you run the query, answer:

- Which customers contribute the most?
- Is contribution spread evenly or concentrated?
- Why is this useful in prioritization?

---

## Task 14 — Running Total by Age

### Business Question
How do charges accumulate as age increases?

### Why this matters
Running totals help analysts understand accumulation and progression.

### Your task
Use:

```sql
SUM(charges) OVER (ORDER BY age)
```

### Reflection
After you run the query, answer:

- What does a running total show that a simple total does not?
- Why might sorting matter here?
- In what business situations are running totals helpful?

---

## Task 15 — LAG and LEAD

### Business Question
How can we compare a row to the previous or next row?

### Why this matters
In many analytical settings, comparing neighboring rows helps identify local changes.

### Your task
Use:

- `LAG(charges) OVER (ORDER BY age)`
- `LEAD(charges) OVER (ORDER BY age)`

### Reflection
After you run the query, answer:

- What do the previous and next values tell you?
- Why are these functions important in time-series analysis?
- What caution should you use when ordering by age instead of time?

---

# Part F — Synthesis

## Task 16 — Full Analytical Question

### Business Question
Find the top 2 customers in each region whose charges are above their regional average.

### Why this matters
This combines several Week 2 ideas:

- regional context
- above-average comparison
- ranking within groups

### Your task
Build a query that:

1. computes the regional average
2. filters to customers above that average
3. ranks them by region
4. returns the top 2 per region

### Reflection
After you run the query, answer:

- Why is this query more realistic than a simple aggregate?
- What business action might follow?
- What did window functions make possible here?

---

# Part G — Final Reflection

Write short answers for the following:

1. When should you use `GROUP BY`?
2. When should you use a window function?
3. Why is `PARTITION BY` so important?
4. What is the difference between `RANK`, `DENSE_RANK`, and `ROW_NUMBER`?
5. Which Week 2 query felt most useful from a business perspective, and why?

---

# Deliverables

Submit:

- your SQL queries
- your result screenshots or outputs
- your written reflections

Remember:

> The goal is not just to produce SQL.  
> The goal is to explain what the SQL means.
