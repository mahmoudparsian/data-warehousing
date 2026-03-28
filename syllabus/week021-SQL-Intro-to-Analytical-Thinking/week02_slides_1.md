---
marp: true
title: Week 2 — SQL & Analytical Thinking (Full Lecture)
paginate: true
theme: default
class: lead
---

# Week 2  
## SQL & Analytical Thinking

---

# 🎯 Learning Objectives

- Move from syntax to thinking  
- Translate business questions into SQL  
- Recognize patterns in data  
- Generate actionable insights  

---

# 🧠 What is Analytical Thinking?

- Breaking problems into components  
- Using data to validate assumptions  
- Connecting results to business decisions  

---

# 🧠 Analyst Workflow

- Start with a question  
- Use SQL to explore  
- Interpret results  
- Recommend actions  

---

# 💡 Key Principle

- SQL is a tool  
- Thinking is the skill  
- Insight is the goal  

---

# 🎯 Business Question

- Who are our most valuable customers?  
- What drives cost?  
- Where should we act?  

---

# 📊 Example Dataset

- insurance dataset  
- customer-level data  
- multiple influencing variables  

---

# 🧠 Step 1: Ask Better Questions

- What are we trying to learn?  
- Why does it matter?  
- How will it impact decisions?  

---

# 📊 Example Question

- Do smokers cost more?  
- Is this consistent across regions?  
- What does this imply?  

---

# 📊 SQL Example

```sql
SELECT smoker, AVG(charges)
FROM insurance
GROUP BY smoker;
```

---

# 💡 Insight

- Smokers cost significantly more  
- Strong segmentation signal  
- Impacts pricing strategy  

---

# 🧠 Deeper Question

- Does smoking impact equally across regions?  
- Are there interaction effects?  
- Where is the impact strongest?  

---

# 📊 SQL Example

```sql
SELECT region, smoker, AVG(charges)
FROM insurance
GROUP BY region, smoker;
```

---

# 💡 Insight

- Interaction effects visible  
- Some regions amplify risk  
- Strategy should be localized  

---

# 🧠 Analytical Pattern

- Start simple  
- Add dimensions  
- Compare results  

---

# 📊 Business Example

- Retail: which products drive revenue?  
- Banking: which customers default?  
- Healthcare: which patients cost more?  

---

# 📊 SQL Pattern

```sql
SELECT dimension, metric
FROM table
GROUP BY dimension;
```

---

# 💡 Insight

- Aggregation simplifies complexity  
- Enables comparison  
- Reveals patterns  

---

# 🧠 Thinking in Segments

- Divide customers into groups  
- Compare behavior  
- Identify outliers  

---

# 📊 Example

```sql
SELECT children, AVG(charges)
FROM insurance
GROUP BY children;
```

---

# 💡 Insight

- Family size affects cost  
- Not always linear  
- Needs deeper analysis  

---

# 🧠 Hypothesis-Driven Analysis

- Form a hypothesis  
- Test with SQL  
- Accept or reject  

---

# 📊 Example Hypothesis

- Higher BMI increases cost  
- Test using grouping  
- Validate with averages  

---

# 📊 SQL

```sql
SELECT bmi, AVG(charges)
FROM insurance
GROUP BY bmi;
```

---

# 💡 Insight

- Trends visible  
- Outliers present  
- Non-linear patterns  

---

# 🧠 Outlier Thinking

- Outliers matter  
- Identify extremes  
- Understand causes  

---

# 📊 SQL

```sql
SELECT *
FROM insurance
ORDER BY charges DESC
LIMIT 10;
```

---

# 💡 Insight

- High-cost individuals  
- Often share risk factors  
- Target for analysis  

---

# 🧠 Comparing Groups

- Always compare  
- Never analyze in isolation  
- Context matters  

---

# 📊 Example

```sql
SELECT region, AVG(charges)
FROM insurance
GROUP BY region;
```

---

# 💡 Insight

- Geography impacts cost  
- External factors matter  
- Contextual analysis needed  

---

# 🧠 Analytical Depth

- Single variable = basic insight  
- Multiple variables = deep insight  
- Context = real insight  

---

# 📊 Advanced Example

```sql
SELECT region, children, smoker, AVG(charges)
FROM insurance
GROUP BY region, children, smoker;
```

---

# 💡 Insight

- Multi-factor interaction  
- Real-world complexity  
- Strategic value  

---

# 🧠 Business Translation

- Data → insight  
- Insight → action  
- Action → value  

---

# 📊 Case Study

- Identify high-risk segments  
- Optimize pricing  
- Improve profitability  

---

# 📊 SQL

```sql
SELECT smoker, region, AVG(charges)
FROM insurance
GROUP BY smoker, region
ORDER BY AVG(charges) DESC;
```

---

# 💡 Insight

- Target high-cost segments  
- Adjust pricing  
- Focus interventions  

---

# 🧠 Common Mistake

- Writing SQL without thinking  
- Ignoring business context  
- Misinterpreting results  

---

# 💡 Fix

- Always ask “why”  
- Always interpret results  
- Always connect to business  

---

# 🎯 Summary

- SQL is a thinking tool  
- Questions drive analysis  
- Insights drive decisions  

---

# 💡 Final Thought

- Better questions → better SQL  
- Better SQL → better insights  
- Better insights → better business  


---

# 📊 Example — Revenue Segmentation

```sql
SELECT region, SUM(charges)
FROM insurance
GROUP BY region;
```

- Measures total revenue by region  
- Identifies high-value regions  
- Helps allocate resources  

👉 Business Insight: Focus marketing on high-revenue regions  

---

# 📊 Example — Customer Concentration

```sql
SELECT region, COUNT(*) 
FROM insurance 
GROUP BY region;
```

- Shows customer distribution  
- Helps identify dense markets  
- Supports expansion decisions  

👉 Business Insight: High density ≠ high revenue  

---

# 📊 Example — Risk Segmentation

```sql
SELECT smoker, COUNT(*)
FROM insurance
GROUP BY smoker;
```

- Measures population split  
- Understands risk proportions  
- Contextualizes averages  

👉 Business Insight: Small group may drive large cost  

---

# 📊 Example — Cost Distribution

```sql
SELECT MIN(charges), MAX(charges), AVG(charges)
FROM insurance;
```

- Shows full range of values  
- Identifies spread of costs  
- Establishes baseline  

👉 Business Insight: Large variance = pricing complexity  

---

# 📊 Example — High Value Segments

```sql
SELECT smoker, AVG(charges)
FROM insurance
GROUP BY smoker
ORDER BY AVG(charges) DESC;
```

- Ranks segments by value  
- Identifies top contributors  
- Enables prioritization  

👉 Business Insight: Focus on high-cost drivers  

---

# 📊 Example — Combined Risk Analysis

```sql
SELECT smoker, region, COUNT(*)
FROM insurance
GROUP BY smoker, region;
```

- Combines multiple dimensions  
- Identifies segment sizes  
- Adds context to averages  

👉 Business Insight: Large risky segments = big impact  

---

# 📊 Example — Outlier Regions

```sql
SELECT region, MAX(charges)
FROM insurance
GROUP BY region;
```

- Finds extreme values  
- Detects unusual regions  
- Helps risk management  

👉 Business Insight: Extreme cases require attention  

---

# 📊 Example — Balanced View

```sql
SELECT region, AVG(charges), COUNT(*)
FROM insurance
GROUP BY region;
```

- Combines value + volume  
- Prevents misleading insights  
- Enables better decisions  

👉 Business Insight: Always consider BOTH avg and count  

---

# 📊 Example — Customer Mix

```sql
SELECT region, smoker, COUNT(*)
FROM insurance
GROUP BY region, smoker;
```

- Shows composition of customers  
- Helps understand mix  
- Supports segmentation  

👉 Business Insight: Mix impacts profitability  

---

# 📊 Example — Trend Preparation

```sql
SELECT age, AVG(charges)
FROM insurance
GROUP BY age
ORDER BY age;
```

- Prepares data for trend analysis  
- Identifies patterns over age  
- Useful for visualization  

👉 Business Insight: Age trends guide pricing  

---

# 📊 Example — Segment Ranking

```sql
SELECT region, AVG(charges)
FROM insurance
GROUP BY region
ORDER BY AVG(charges) DESC;
```

- Ranks segments  
- Simplifies decision-making  
- Highlights top performers  

👉 Business Insight: Ranking drives prioritization  

---

# 📊 Example — Business KPI

```sql
SELECT AVG(charges) AS avg_cost
FROM insurance;
```

- Defines baseline metric  
- Used for comparisons  
- Simple but powerful  

👉 Business Insight: KPIs guide performance tracking  

---

# 📊 Example — Comparing Groups

```sql
SELECT smoker, region, AVG(charges)
FROM insurance
GROUP BY smoker, region;
```

- Enables group comparison  
- Highlights differences  
- Supports decisions  

👉 Business Insight: Comparison reveals opportunity  

---

# 📊 Example — Data Completeness

```sql
SELECT COUNT(*) FROM insurance;
```

- Measures dataset size  
- Checks completeness  
- Validates data loading  

👉 Business Insight: Data quality affects decisions  

---

# 📊 Example — Strategic Insight

```sql
SELECT region, smoker, AVG(charges)
FROM insurance
GROUP BY region, smoker
ORDER BY AVG(charges) DESC;
```

- Combines segmentation + ranking  
- Identifies high-value segments  
- Supports strategy  

👉 Business Insight: Focus on segments that maximize value  

