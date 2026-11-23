---
marp: true
title: Week 1 — Foundations of SQL for Analytics (Ultimate Lecture)
paginate: true
theme: default
class: lead
---

# Week 1  
## Foundations of SQL for Analytics

---

# 🎯 Learning Objectives

- Understand SQL as a thinking tool, not just syntax  
- Translate business questions into structured queries  
- Interpret results to generate insights  
- Build a strong analytical mindset  

---

# 🧠 What is Data Analytics?

- Turning raw data into meaningful decisions  
- Identifying patterns and trends in data  
- Supporting business strategy with evidence  

---

# 🧠 The Analyst Journey

- Raw data is meaningless without questions  
- SQL helps transform data into patterns  
- Insights lead to better decisions  

---

# 💡 Core Philosophy

- SQL is not about memorizing syntax  
- It is about structured thinking  
- The goal is always insight, not queries  

---

# 📊 Dataset Context

- insurance.csv represents real-world customers  
- Each row = one customer  
- Columns represent risk factors and cost  

---

# 🧠 Business Context

- Insurance companies price based on risk  
- Data helps identify high-risk customers  
- Better analysis leads to better pricing  

---

# 🎯 Key Question

- What factors influence charges?  
- Which customers are expensive?  
- How can we segment customers?  

---

# 🔍 First Look

```sql
SELECT * FROM insurance;
```

- Shows full dataset  
- Helps understand structure  
- Not analytical yet  

---

# ⚠️ Exploration vs Analysis

- Exploration = looking at data  
- Analysis = answering questions  
- Always move from exploration → analysis  

---

# 🔎 Controlled Exploration

```sql
SELECT * FROM insurance LIMIT 10;
```

- Prevents overload  
- Helps inspect data quickly  
- Best practice in real systems  

---

# 🎯 Question 1

- Who are the most expensive customers?  
- What patterns do they share?  
- Can we identify risk groups?  

---

# 📊 Query

```sql
SELECT * FROM insurance ORDER BY charges DESC LIMIT 10;
```

- Sorts by highest cost  
- Identifies extreme cases  
- Helps form hypotheses  

---

# 💡 Insight

- High-cost customers often smokers  
- BMI appears correlated  
- Patterns begin to emerge  

---

# 🧠 Hypothesis

- Smoking increases cost  
- Health risks drive pricing  
- Needs validation with data  

---

# 📊 Test Hypothesis

```sql
SELECT smoker, AVG(charges) FROM insurance GROUP BY smoker;
```

- Groups by smoker status  
- Computes average cost  
- Confirms hypothesis  

---

# 💡 Result

- Smokers pay significantly more  
- Clear separation between groups  
- Strong business implication  

---

# 🧠 Business Meaning

- Pricing models use risk factors  
- Smoking is a key driver  
- Helps in segmentation  

---

# 🎯 Question 2

- Does region affect cost?  
- Are some regions more expensive?  
- What could explain differences?  

---

# 📊 Query

```sql
SELECT region, AVG(charges) FROM insurance GROUP BY region;
```

- Groups by geography  
- Calculates average cost  
- Enables comparison  

---

# 💡 Insight

- Regions vary in cost  
- External factors influence pricing  
- Geography matters  

---

# 📊 Multi-Dimensional Analysis

```sql
SELECT region, smoker, AVG(charges) FROM insurance GROUP BY region, smoker;
```

- Combines multiple variables  
- Reveals interaction effects  
- Deeper insight than single grouping  

---

# 💡 Insight

- Smoking impact varies by region  
- Some segments are extremely costly  
- Multi-factor analysis is critical  

---

# 📊 Outlier Detection

```sql
SELECT * FROM insurance WHERE charges > 20000;
```

- Identifies extreme values  
- Helps detect risk clusters  
- Useful for segmentation  

---

# 💡 Insight

- Outliers often represent high risk  
- Important for business strategy  
- Can guide pricing decisions  

---

# 📊 High Risk Segment

```sql
SELECT * FROM insurance WHERE smoker='yes' AND bmi > 30;
```

- Combines conditions  
- Identifies risky population  
- Useful for targeting  

---

# 💡 Insight

- Multiple risk factors amplify cost  
- Segmentation becomes clearer  
- Business can act on this  

---

# 📊 Aggregation Types

- COUNT measures volume  
- AVG measures typical value  
- SUM measures total impact  

---

# 📊 Example

```sql
SELECT region, COUNT(*) FROM insurance GROUP BY region;
```

- Counts customers per region  
- Shows distribution  
- Helps understand dataset  

---

# 💡 Insight

- Data distribution matters  
- More data ≠ higher cost  
- Need normalization  

---

# 📊 More Analysis

```sql
SELECT children, AVG(charges) FROM insurance GROUP BY children;
```

- Studies family size  
- Shows cost trends  
- Adds another dimension  

---

# 💡 Insight

- Family size impacts cost  
- Patterns may not be linear  
- Requires interpretation  

---

# 📊 Advanced Example

```sql
SELECT region, children, AVG(charges) FROM insurance GROUP BY region, children;
```

- Multi-variable analysis  
- Reveals hidden relationships  
- Real-world complexity  

---

# 💡 Insight

- Real data is multi-dimensional  
- Simple queries are not enough  
- Need layered analysis  

---

# ⚠️ Common SQL Error

```sql
SELECT region, charges FROM insurance;
```

- Missing aggregation  
- Produces misleading results  
- Very common mistake  

---

# ✅ Rule

- Every column must be grouped  
- Or aggregated  
- Ensures correctness  

---

# 📊 SQL Logical Flow

- SELECT defines output  
- FROM defines data source  
- WHERE filters data  
- GROUP BY aggregates  

---

# 🧠 Execution Order

- FROM runs first  
- WHERE filters  
- GROUP BY aggregates  
- SELECT finalizes  

---

# 💡 Importance

- Prevents logical mistakes  
- Explains unexpected results  
- Critical for debugging  

---

# 📊 Sorting Insight

```sql
SELECT region, AVG(charges) FROM insurance GROUP BY region ORDER BY AVG(charges) DESC;
```

- Ranks results  
- Helps decision-making  
- Identifies top segments  

---

# 💡 Insight

- Ranking simplifies analysis  
- Easier to interpret  
- Useful for business  

---

# 📊 DISTINCT Values

```sql
SELECT DISTINCT region FROM insurance;
```

- Finds unique values  
- Helps understand categories  
- Useful for exploration  

---

# 💡 Insight

- Categorical understanding  
- Simplifies dataset view  
- Helps grouping  

---

# 📊 Case Study

- Which segment should we target?  
- Who brings highest revenue?  
- Where should strategy focus?  

---

# 📊 Answer

```sql
SELECT smoker, region, AVG(charges) FROM insurance GROUP BY smoker, region ORDER BY AVG(charges) DESC;
```

- Combines segmentation  
- Ranks segments  
- Identifies targets  

---

# 💡 Insight

- High-value segments identified  
- Supports business strategy  
- Enables decision-making  

---

# 📊 Additional Example 1

```sql
SELECT gender, AVG(charges) FROM insurance GROUP BY gender;
```

- Compares genders  
- Identifies differences  
- Adds dimension  

---

# 📊 Additional Example 2

```sql
SELECT region, MAX(charges) FROM insurance GROUP BY region;
```

- Finds max cost  
- Shows extremes  
- Useful for risk  

---

# 📊 Additional Example 3

```sql
SELECT MIN(charges), MAX(charges) FROM insurance;
```

- Range of values  
- Understand spread  
- Basic statistics  

---

# 📊 Additional Example 4

```sql
SELECT COUNT(DISTINCT region) FROM insurance;
```

- Counts categories  
- Measures diversity  
- Useful summary  

---

# 📊 Additional Example 5

```sql
SELECT smoker, COUNT(*) FROM insurance GROUP BY smoker;
```

- Distribution of smokers  
- Helps contextualize results  
- Important for interpretation  

---

# 📊 Additional Example 6

```sql
SELECT region, SUM(charges) FROM insurance GROUP BY region;
```

- Total cost per region  
- Business revenue view  
- Different from AVG  

---

# 📊 Additional Example 7

```sql
SELECT bmi, COUNT(*) FROM insurance GROUP BY bmi;
```

- Frequency distribution  
- Data density insight  
- Pre-EDA step  

---

# 📊 Additional Example 8

```sql
SELECT age, COUNT(*) FROM insurance GROUP BY age;
```

- Age distribution  
- Demographic insight  
- Useful segmentation  

---

# 📊 Additional Example 9

```sql
SELECT children, COUNT(*) FROM insurance GROUP BY children;
```

- Family size distribution  
- Understand dataset  
- Supports analysis  

---

# 📊 Additional Example 10

```sql
SELECT AVG(charges) FROM insurance;
```

- Overall average cost  
- Baseline metric  
- Used for comparison  

---

# 🎯 Final Summary

- SQL = thinking tool  
- Questions drive analysis  
- Insights drive decisions  

---

# 💡 Final Thought

Better questions → better SQL → better decisions
