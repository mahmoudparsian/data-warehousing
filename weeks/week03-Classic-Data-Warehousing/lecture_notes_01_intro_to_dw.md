---
marp: true
title: Week 3 — Classic Data Warehousing (Ultimate Lecture + Tutorial)
paginate: true
theme: default
class: lead
---
# Week 3  
## Classic Data Warehousing (DW)

---

# 🎯 Learning Objectives

- Understand why DW exists in modern analytics  
- Design star schemas (fact + dimensions)  
- Connect DW to SQL queries and business insight  

---

# 🧠 What Problem Are We Solving?

- Raw transactional systems are not designed for analytics  
- Queries become slow and complex  
- Business users cannot easily explore data  

👉 Insight: DW simplifies complexity  

---

# 💡 OLTP vs OLAP (Revisited)

- OLTP → transactions, normalized, fast inserts  
- OLAP → analytics, denormalized, fast queries  
- Different systems for different workloads  

👉 Insight: Separate systems = better performance  

---

# 📊 Business Scenario

- Retail company with millions of transactions  
- Needs daily reporting and dashboards  
- Requires fast aggregation queries  

👉 Insight: Scale demands structure  

---

# 🧠 Why Queries Become Slow

- Too many joins  
- Highly normalized schema  
- No pre-aggregation  

👉 Insight: Design impacts performance  

---

# 💡 Data Warehouse Solution

- Central analytical database  
- Structured for reporting  
- Pre-modeled for queries  

👉 Insight: DW = analytics engine  

---

# 🏛️ Two Classic Approaches: Inmon vs Kimball

| | **Bill Inmon** (top-down) | **Ralph Kimball** (bottom-up) |
|---|---|---|
| Start with | One enterprise-wide warehouse | One business process (e.g. sales) |
| Warehouse model | Normalized (3NF) | Dimensional (star schemas) |
| Data marts | Built **from** the warehouse | Together they **are** the warehouse |
| Integration via | Central model | Conformed dimensions (shared `dim_date`, `dim_customer`, …) |
| Strength | Consistency, single version of truth | Fast delivery, easy for analysts |
| Cost | Slow, big upfront design | Needs discipline to stay consistent |

👉 In this course we build **Kimball-style** star schemas (weeks 3–4, and the Gold layer in week 8)

---

# 🏛️ Inmon Model in a Picture

![w:900](../../course_information/images/README_DW_Inmon_Model.png)

- OLTP sources → ETL → **enterprise DW (3NF)** → ETL → data marts → OLAP / reports
- Kimball: OLTP sources → ETL → **star schemas (data marts)** linked by conformed dimensions

---

# 🧠 Dimensional Modeling Overview

- Fact tables store metrics  
- Dimension tables store context  
- Star schema organizes everything  

👉 Insight: Model mirrors business thinking  

---

# 📊 Fact Table Deep Dive

- Contains numeric measures (sales, revenue)  
- Contains foreign keys to dimensions  
- Very large and grows continuously  

👉 Insight: Fact = what happened  

---

# 📊 Dimension Table Deep Dive

- Contains descriptive attributes  
- Used in filtering and grouping  
- Relatively small and stable  

👉 Insight: Dimension = context  

---

# 📊 Example Star Schema

Fact: sales  
Dimensions: customer, product, date, store  

👉 Insight: One central table + context tables  

---

# 📊 Visual Thinking

- Fact table in the center  
- Dimensions around it  
- Looks like a star  

👉 Insight: Simplicity improves usability  

---

# 🧠 Grain (Critical Concept)

- Defines level of detail  
- Example: one row per transaction  
- Must be consistent  

👉 Insight: Grain determines everything  

---

# 📊 Grain Example

- One row per order line  
- Each row = one product in an order  
- Supports detailed analysis  

👉 Insight: Fine grain = flexibility  

---

# 🧠 Measures

- Quantitative values  
- Example: revenue, quantity  
- Aggregated using SUM, AVG  

👉 Insight: Measures drive KPIs  

---

# 🧠 Dimensions

- Who, what, when, where  
- Used in GROUP BY  
- Enables slicing and dicing  

👉 Insight: Dimensions enable insight  

---

# 📊 Simple DW Query

```sql
SELECT region, SUM(amount)
FROM sales
JOIN customer USING (customer_id)
GROUP BY region;
```

- Combines fact + dimension  
- Produces business metric  
- Easy to understand  

👉 Insight: DW simplifies SQL  

---

# 🧠 Why Star Schema Works

- Fewer joins  
- Denormalized structure  
- Faster queries  

👉 Insight: Built for analysts  

---

# 🧠 ETL Pipeline

- Extract from source systems  
- Transform (clean + enrich)  
- Load into DW  

👉 Insight: Data preparation is essential  

---

# 📊 ETL Example

- Extract: OLTP database  
- Transform: clean, normalize  
- Load: star schema  

👉 Insight: Pipeline ensures quality  

---

# 🧠 Data Quality Issues

- Missing values  
- Duplicates  
- Inconsistent formats  

👉 Insight: Bad data → bad decisions  

---

# 📊 Cleaning Example

```sql
SELECT LOWER(TRIM(name))
```

- Standardizes data  
- Removes noise  
- Improves accuracy  

👉 Insight: Clean data matters  

---

# 🧠 Normalization vs Denormalization

- OLTP normalized  
- DW denormalized  
- Trade-off: redundancy vs speed  

👉 Insight: Performance priority  

---

# 📊 Performance Thinking

- Indexing  
- Partitioning  
- Pre-aggregation  

👉 Insight: Optimization matters  

---

# 🎯 Final Summary

- DW is designed for analytics  
- Star schema simplifies queries  
- Dimensions provide context  

---

# 💡 Final Thought

👉 “A well-designed data warehouse makes analysis easy  
A poorly designed one makes it impossible”
