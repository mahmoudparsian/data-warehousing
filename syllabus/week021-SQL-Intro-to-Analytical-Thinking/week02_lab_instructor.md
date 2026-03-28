# Week 2 Lab — Instructor Version (Detailed Solutions)
## SQL, Analytical Thinking, and Window Functions

## 1) Instructor Goals

This lab is designed to reinforce three important transitions:

- from syntax to analytical thinking
- from simple aggregation to contextual analysis
- from summarizing data to ranking and comparing inside groups

Emphasize throughout the lab:

- the business question first
- the SQL pattern second
- the interpretation third

---

## 2) Dataset Reminder

Table: `insurance`

Columns:

- `age`
- `gender`
- `bmi`
- `children`
- `smoker`
- `region`
- `charges`

The most important business metric in this lab is `charges`.

---

# Part A — Review and Analytical Thinking

## Task 1 — Regional Average Charges

### SQL
```sql
SELECT
    region,
    AVG(charges) AS avg_charges
FROM insurance
GROUP BY region
ORDER BY avg_charges DESC;
```

### What we are doing
- grouping rows by region
- computing the average charge in each region
- ranking regions from highest average to lowest

### Why this matters
This gives a quick regional comparison.  
It is one of the simplest ways to identify expensive or cheap markets.

### Teaching note
Students should explain why `AVG` is better than `SUM` for this question.  
A region with more customers could have a larger sum even if the typical customer is not more expensive.

---

## Task 2 — Smoker vs Non-Smoker

### SQL
```sql
SELECT
    smoker,
    AVG(charges) AS avg_charges
FROM insurance
GROUP BY smoker
ORDER BY avg_charges DESC;
```

### What we are doing
- segmenting customers into smoker vs non-smoker
- comparing average cost between the groups
- testing a risk-based business hypothesis

### Why this matters
This is a clean example of segmentation.  
Students should see that analytical SQL often starts with a plain-English comparison question.

### Expected insight
Smokers should have much higher average charges.  
This creates a natural discussion around risk, pricing, and segmentation.

---

## Task 3 — Region + Smoker

### SQL
```sql
SELECT
    region,
    smoker,
    AVG(charges) AS avg_charges
FROM insurance
GROUP BY region, smoker
ORDER BY region, avg_charges DESC;
```

### What we are doing
- moving from one grouping variable to two
- checking whether the smoker effect is stable across regions
- introducing interaction between variables

### Why this matters
Averages for the whole population can hide subgroup differences.  
This result is more actionable because it points to region-specific patterns.

### Teaching note
Ask students whether the same global conclusion holds in every region.  
This helps them understand why multi-dimensional analysis matters.

---

# Part B — Why GROUP BY Is Not Enough

## Task 4 — Top 5 Most Expensive Customers Overall

### SQL
```sql
SELECT *
FROM insurance
ORDER BY charges DESC
LIMIT 5;
```

### What we are doing
- sorting all rows by charges
- selecting only the most expensive customers
- identifying outliers and extremes

### Why this matters
Businesses often care about extremes, not just averages.  
Top customers may drive disproportionate revenue or cost.

### Teaching note
Encourage students to inspect the returned rows and look for shared traits such as smoking or BMI.

---

## Task 5 — Top 3 Customers per Region

### SQL
```sql
SELECT *
FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY region
            ORDER BY charges DESC
        ) AS rn
    FROM insurance
) t
WHERE rn <= 3
ORDER BY region, rn;
```

### What we are doing
- dividing the dataset into region-based partitions
- ranking customers inside each partition
- keeping the top 3 in every region

### Why this matters
This is one of the most important analytical SQL patterns.  
Businesses often need “top N per segment,” not just “top N overall.”

### Why `ROW_NUMBER` is appropriate
`ROW_NUMBER` gives a strict ranking with no duplicates.  
It is ideal when the requirement is exactly three rows per region.

### Teaching note
This is the slide/lab moment where students should clearly see why `GROUP BY` cannot solve this problem correctly.

---

# Part C — Core Window Functions

## Task 6 — Add Regional Average to Every Row

### SQL
```sql
SELECT
    *,
    AVG(charges) OVER (PARTITION BY region) AS regional_avg
FROM insurance;
```

### What we are doing
- preserving every customer row
- adding the average charge for the customer’s region
- enriching rows with group context

### Why this matters
This is the conceptual breakthrough of window functions.  
Unlike `GROUP BY`, we do not lose row-level detail.

### Teaching note
Use this task to repeat:
- `GROUP BY` summarizes
- window functions enrich

---

## Task 7 — Customers Above Their Regional Average

### SQL
```sql
SELECT *
FROM (
    SELECT
        *,
        AVG(charges) OVER (PARTITION BY region) AS regional_avg
    FROM insurance
) t
WHERE charges > regional_avg
ORDER BY region, charges DESC;
```

### What we are doing
- computing a regional benchmark
- comparing each row against that benchmark
- filtering to rows that exceed the benchmark

### Why this matters
This identifies customers who are expensive relative to their peer group.  
That is often more meaningful than using one overall threshold for everyone.

### Teaching note
Ask students why “above regional average” is better than “charges > 15000” for many analytical purposes.

---

## Task 8 — Difference from Regional Average

### SQL
```sql
SELECT
    *,
    charges - AVG(charges) OVER (PARTITION BY region) AS diff_from_regional_avg
FROM insurance
ORDER BY region, diff_from_regional_avg DESC;
```

### What we are doing
- calculating a deviation score
- measuring how far each customer is from their regional norm
- creating a simple anomaly metric

### Why this matters
A distance from average is often more informative than a yes/no label.  
It helps rank unusual cases.

### Teaching note
This is a good place to discuss anomaly detection and benchmarking.

---

# Part D — Ranking Functions

## Task 9 — RANK()

### SQL
```sql
SELECT
    *,
    RANK() OVER (
        PARTITION BY region
        ORDER BY charges DESC
    ) AS rnk
FROM insurance
ORDER BY region, rnk, charges DESC;
```

### What we are doing
- ranking customers inside each region
- allowing ties to share the same rank
- preserving the meaning of tied positions

### Why this matters
If two customers have the same charge, it can be reasonable to give them the same rank.

### Important detail
If ranks tie, the next rank number may skip.  
For example: 1, 2, 2, 4.

---

## Task 10 — DENSE_RANK()

### SQL
```sql
SELECT
    *,
    DENSE_RANK() OVER (
        PARTITION BY region
        ORDER BY charges DESC
    ) AS dense_rnk
FROM insurance
ORDER BY region, dense_rnk, charges DESC;
```

### What we are doing
- ranking inside each region
- allowing ties
- avoiding skipped numbers

### Why this matters
This is often easier to explain in reporting.  
For example: 1, 2, 2, 3.

### Teaching note
Students should understand that `DENSE_RANK` is often friendlier for dashboards and presentations.

---

## Task 11 — ROW_NUMBER()

### SQL
```sql
SELECT
    *,
    ROW_NUMBER() OVER (
        PARTITION BY region
        ORDER BY charges DESC
    ) AS row_num
FROM insurance
ORDER BY region, row_num;
```

### What we are doing
- assigning a unique order to each row
- guaranteeing one unique number per row
- forcing exact Top-N output

### Why this matters
This is the best tool when the requirement is strict row selection.  
For example: exactly the top 3 rows per region.

### Teaching note
Stress that ties are broken arbitrarily unless the `ORDER BY` is expanded with additional columns.

---

## Task 12 — Compare All Three

### SQL
```sql
SELECT
    region,
    charges,
    RANK() OVER (
        PARTITION BY region
        ORDER BY charges DESC
    ) AS rnk,
    DENSE_RANK() OVER (
        PARTITION BY region
        ORDER BY charges DESC
    ) AS dense_rnk,
    ROW_NUMBER() OVER (
        PARTITION BY region
        ORDER BY charges DESC
    ) AS row_num
FROM insurance
ORDER BY region, charges DESC;
```

### What we are doing
- placing all three ranking methods side by side
- making their differences visible
- building conceptual clarity

### Why this matters
Students often memorize definitions but do not truly understand the behavioral difference.  
This query makes the difference concrete.

### Teaching note
Have students explain in plain English which function they would use for:
- dashboards
- exact top 3
- fair handling of ties

---

# Part E — Contribution and Running Analytics

## Task 13 — Contribution to Total Charges

### SQL
```sql
SELECT
    *,
    charges / SUM(charges) OVER () AS pct_total
FROM insurance
ORDER BY pct_total DESC;
```

### What we are doing
- computing the total charges across the full table
- dividing each row by that total
- measuring each customer’s contribution

### Why this matters
This supports prioritization.  
Businesses want to know which customers drive the most value or cost.

### Teaching note
This is a good place to mention Pareto thinking: a small number of rows may account for a large portion of total value.

---

## Task 14 — Running Total by Age

### SQL
```sql
SELECT
    age,
    charges,
    SUM(charges) OVER (
        ORDER BY age
    ) AS running_total
FROM insurance
ORDER BY age;
```

### What we are doing
- sorting rows by age
- accumulating charges as age increases
- building a cumulative view

### Why this matters
Running totals are widely used in dashboards, forecasting, and business monitoring.

### Teaching note
Point out that ordering matters a lot.  
Without `ORDER BY`, there is no meaningful running total.

---

## Task 15 — LAG and LEAD

### SQL
```sql
SELECT
    age,
    charges,
    LAG(charges) OVER (ORDER BY age) AS prev_charge,
    LEAD(charges) OVER (ORDER BY age) AS next_charge
FROM insurance
ORDER BY age;
```

### What we are doing
- looking backward with `LAG`
- looking forward with `LEAD`
- comparing a row to nearby rows

### Why this matters
This is a foundation for change analysis and time-style analytics.

### Teaching note
Be honest that `age` is not a true time axis.  
The function is still useful pedagogically, but in real business settings this is often done over dates.

---

# Part F — Synthesis

## Task 16 — Top 2 Above Regional Average per Region

### SQL
```sql
SELECT *
FROM (
    SELECT
        *,
        AVG(charges) OVER (PARTITION BY region) AS regional_avg,
        ROW_NUMBER() OVER (
            PARTITION BY region
            ORDER BY charges DESC
        ) AS rn
    FROM insurance
) t
WHERE charges > regional_avg
  AND rn <= 2
ORDER BY region, rn;
```

### What we are doing
- combining benchmarking and ranking
- identifying customers above their segment norm
- returning the top 2 such customers in each region

### Why this matters
This is the kind of compound analytical logic businesses actually use.  
It is much more realistic than a simple aggregate query.

### Teaching note
This is an excellent final exercise because it combines:
- `PARTITION BY`
- averages
- ranking
- filtering

---

# Part G — Final Conceptual Answers

## 1) When should you use `GROUP BY`?
Use `GROUP BY` when you want one row per group and you do not need the original detail rows.

## 2) When should you use a window function?
Use a window function when you want group-level context while keeping the original rows.

## 3) Why is `PARTITION BY` important?
It defines the groups inside which the window function works.  
Without it, calculations are done over the whole table.

## 4) What is the difference between `RANK`, `DENSE_RANK`, and `ROW_NUMBER`?
- `RANK`: ties allowed, gaps after ties
- `DENSE_RANK`: ties allowed, no gaps
- `ROW_NUMBER`: unique order, no ties

## 5) Which Week 2 idea is most important?
The biggest conceptual leap is this:

> `GROUP BY` summarizes rows.  
> Window functions keep rows and add analytical context.

---

# Final Teaching Message

Students should leave this lab understanding that:

- SQL is not just for retrieving data
- SQL is a language for structured analytical reasoning
- window functions are one of the most powerful tools in modern analytics
