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

# 📊 Example — Product Analysis

```sql
SELECT product_name, SUM(amount)
FROM sales
JOIN product USING (product_id)
GROUP BY product_name;
```

- Aggregates by product  
- Identifies best sellers  
- Drives inventory decisions  

👉 Insight: Product performance  

---

# 📊 Example — Time Analysis

```sql
SELECT year, SUM(amount)
FROM sales
JOIN date USING (date_id)
GROUP BY year;
```

- Aggregates over time  
- Identifies trends  
- Supports forecasting  

👉 Insight: Time dimension is critical  

---

# 🧠 Slowly Changing Dimensions (SCD)

- Dimensions change over time  
- Must track history  
- Important for accurate reporting  

👉 Insight: Time-aware modeling  

---

# 📊 SCD Type 1

- Overwrite old value  
- No history kept  
- Simple implementation  

👉 Insight: Loses past information  

---

# 📊 SCD Type 2

- Add new row for changes  
- Preserve history  
- Most common approach  

👉 Insight: Enables historical analysis  

---

# 📊 SCD Example

```sql
customer_id, city, start_date, end_date
```

- Tracks changes over time  
- Allows time-based queries  
- Supports auditing  

👉 Insight: Temporal dimension  

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

# 🧠 OLAP Operations

- Roll-up  
- Drill-down  
- Slice  
- Dice  

👉 Insight: Multi-dimensional analysis  

---

# 📊 Roll-Up Example

- Daily → monthly sales  
- Aggregate data  
- Summary view  

👉 Insight: High-level trends  

---

# 📊 Drill-Down Example

- Monthly → daily  
- More detail  
- Investigate patterns  

👉 Insight: Root cause analysis  

---

# 📊 Slice Example

- Filter one dimension  
- Example: region = West  
- Focus analysis  

👉 Insight: Narrow scope  

---

# 📊 Dice Example

- Filter multiple dimensions  
- Example: region + product  
- Multi-condition  

👉 Insight: Complex queries  

---

# 📊 Business Use Case

- Sales by region  
- Sales by product  
- Sales by time  

👉 Insight: Multi-angle decisions  

---

# 🧠 Factless Fact Table

- No measures  
- Tracks events  
- Example: login events  

👉 Insight: Event tracking  

---

# 🧠 Conformed Dimensions

- Shared across fact tables  
- Example: date dimension  
- Ensures consistency  

👉 Insight: Unified reporting  

---

# 📊 Data Mart

- Subset of DW  
- Focus on one area  
- Example: marketing  

👉 Insight: Specialized analysis  

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

# 📊 Advanced Query Example

```sql
SELECT region, product_name, SUM(amount)
FROM sales
JOIN customer USING (customer_id)
JOIN product USING (product_id)
GROUP BY region, product_name;
```

- Multi-dimensional analysis  
- Combines dimensions  
- Rich insights  

👉 Insight: Real analytics  

---

# 🎯 Final Summary

- DW is designed for analytics  
- Star schema simplifies queries  
- Dimensions provide context  

---

# 💡 Final Thought

👉 “A well-designed data warehouse makes analysis easy  
A poorly designed one makes it impossible”


---

# 📊 Example — Customer Segmentation

```sql
SELECT customer_id, SUM(amount) AS total_spent
FROM sales
GROUP BY customer_id
ORDER BY total_spent DESC;
```

- Identifies high-value customers  
- Supports loyalty programs  
- Enables targeted marketing  

👉 Insight: Not all customers are equal  

---

# 📊 Example — Time Trend (Monthly Sales)

```sql
SELECT month, SUM(amount)
FROM sales
JOIN date USING (date_id)
GROUP BY month
ORDER BY month;
```

- Tracks performance over time  
- Identifies seasonality  
- Supports forecasting  

👉 Insight: Trends drive planning  

---

# 📊 Example — Product Category Analysis

```sql
SELECT category, SUM(amount)
FROM sales
JOIN product USING (product_id)
GROUP BY category;
```

- Aggregates by product category  
- Identifies strong/weak categories  
- Guides inventory strategy  

👉 Insight: Category performance matters  

---

# 📊 Example — Regional Performance

```sql
SELECT region, SUM(amount)
FROM sales
JOIN customer USING (customer_id)
GROUP BY region;
```

- Compares regions  
- Identifies growth areas  
- Supports expansion decisions  

👉 Insight: Geography drives strategy  

---

# 📊 Example — Average Order Value

```sql
SELECT AVG(amount) AS avg_order_value
FROM sales;
```

- Measures typical transaction  
- Key KPI for business  
- Used in benchmarking  

👉 Insight: AOV impacts profitability  

---

# 📊 Example — Multi-Dimensional Analysis

```sql
SELECT region, category, SUM(amount)
FROM sales
JOIN customer USING (customer_id)
JOIN product USING (product_id)
GROUP BY region, category;
```

- Combines multiple dimensions  
- Reveals deeper patterns  
- Enables complex decisions  

👉 Insight: Real business = multi-dimensional  

---

# 📊 Example — Top Products per Region

```sql
SELECT *
FROM (
    SELECT region, product_name, SUM(amount) AS revenue,
           ROW_NUMBER() OVER (PARTITION BY region ORDER BY SUM(amount) DESC) AS rn
    FROM sales
    JOIN product USING (product_id)
    JOIN customer USING (customer_id)
    GROUP BY region, product_name
) t
WHERE rn <= 3;
```

- Identifies top products by region  
- Supports localized strategy  
- Combines DW + window functions  

👉 Insight: Bridge between Week 2 and 3  

---

# 📊 Example — Customer Lifetime Value (CLV)

```sql
SELECT customer_id, SUM(amount) AS lifetime_value
FROM sales
GROUP BY customer_id;
```

- Measures total customer contribution  
- Used in marketing decisions  
- Supports retention strategies  

👉 Insight: Long-term value matters  

---

# 📊 Example — Daily Sales Monitoring

```sql
SELECT date, SUM(amount)
FROM sales
JOIN date USING (date_id)
GROUP BY date;
```

- Tracks daily performance  
- Detects anomalies  
- Supports operations  

👉 Insight: Monitoring is continuous  

---

# 📊 Example — Factless Event Tracking

```sql
SELECT COUNT(*)
FROM visits
WHERE event_type = 'login';
```

- Tracks events without measures  
- Useful for engagement analysis  
- Supports behavioral analytics  

👉 Insight: Not all facts are numeric  

