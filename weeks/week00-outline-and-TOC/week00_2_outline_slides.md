---
author: Mahmoud Parsian  
marp: true  
theme: default  
paginate: true  
title:  Modern Data Warehousing  
class: lead  
---

# 🎯 Course Objectives

- Understand modern data warehouse architectures
 
- Learn analytical SQL deeply

- Build data pipelines (Bronze → Silver → Gold)

- Think like a data analyst

- Present findings with Tableau and Python charts

- (Bonus) Connect SQL with LLMs and AI


---

# 📅 Course Roadmap (Detailed)

| Block | Weeks | Topic |
|---|---|---|
| A | 1–2 | SQL analytics review: foundations · analytical thinking & EDA |
| B | 3–4 | Classic data warehousing & ETL · star schema & OLAP |
| C | 5–8 | Medallion: introduction · Bronze · Silver · Gold & star schema |
| D | 9–10 | End-to-end pipeline & project workshop · final project & storytelling |

---

# 📘 Week 1 — SQL Foundations

- `SELECT`, `WHERE`, `GROUP BY`  

- Filtering and aggregation  

- Working with real datasets  

- Building SQL intuition  

---

# 📊 Week 1 — Example

```sql
SELECT region, 
       COUNT(*) AS num_orders
FROM sales
GROUP BY region;
```

- Count orders per region  
- Basic aggregation  
- First business insight  
- Builds SQL confidence  

**👉 Business Insight:** 

- Which region has the most activity?

- Are some regions underperforming?

**👉 Question to Students:** 

- If one region is low, what could that mean?

---

# 📘 Week 2 — Analytical Thinking & EDA

- Aggregations + `HAVING`  

- Window functions 
	- `ROW_NUMBER`, `RANK`, `DENSE_RANK`, ...
	 
- Top-N queries  

- Exploratory data analysis (EDA) with SQL  

- Business-driven SQL  

---

# 📊 Week 2 — Example

```sql
SELECT region, 
       amount,
       RANK() OVER (
           PARTITION BY region 
           ORDER BY amount DESC
       ) AS rnk
FROM sales;
```

- Top-N per region  

- Partitioning concept  

- Ranking logic  

- Real-world use case  

### 👉 Business Insight:
- Identify top customers/products per region
- Compare performance within groups

### 👉 Question to Students:
- Why not just use `GROUP BY` here?

---

# 📘 Week 3 — Classic Data Warehousing & ETL

- OLTP vs OLAP; Inmon vs Kimball  

- ETL vs ELT  

- Data cleaning  

- Pipeline thinking  

---

# 📊 Week 3 — Example

```sql
SELECT LOWER(TRIM(region)), 
       SUM(amount)
FROM raw_sales
GROUP BY LOWER(TRIM(region));
```

- Cleaning + aggregation  

- ETL transformation  

- Reporting query  

- Data quality impact  

### 👉 Business Insight:
- Cleaning changes results significantly
- Poor data → wrong decisions

### 👉 Question to Students:
- What happens if we skip cleaning?

---

# 📘 Week 4 — Star Schema & OLAP

- Star schema 
 
- Fact vs Dimension
 
- Analytical modeling  

- OLAP: roll-up, drill-down, slice, dice  

- Slowly changing dimensions (Type 1 / Type 2)  

- First Tableau chart  

---

# 📊 Week 4 — Example

```sql
SELECT d.region, 
       SUM(f.sales)
FROM fact_sales f
JOIN dim_region d ON f.region_id = d.id
GROUP BY d.region;
```

- Fact + dimension join  

- Star schema query  

- Aggregation  

- Business reporting  

### 👉 Business Insight:
- Combine descriptive + numeric data
- Enable flexible reporting

### 👉 Question to Students:
- Why separate fact and dimension tables?

---

# 📘 Week 5 — Medallion Architecture

- Bronze / Silver / Gold  

- Layered architecture  

- Data lifecycle  

- Scalability  

---

# 📊 Week 5 — Example

```sql
SELECT region, 
       SUM(amount)
FROM silver_sales
GROUP BY region;
```

- Clean → aggregate  

- Layered thinking  

- Business output 
 
- Reusable logic  

### 👉 Business Insight:
- Gold tables simplify reporting
- Consistency across dashboards

### 👉 Question to Students:
- Why not query Bronze directly?

---

# 📘 Week 6 — Bronze in Depth & Silver Cleaning

- Raw ingestion, lineage, new files arriving  

- Load errors and bad encodings (`store_rejects`)  

- Keys that collide across batches  

- Data profiling  

- Silver cleaning: nulls, standardization, outliers, dedup  

---

# 📊 Week 6 — Example

```sql
SELECT * 
FROM bronze_sales;
```

- Raw inspection  

- Identify issues 
 
- Debugging stage  

- No transformation  

### 👉 Business Insight:
- Raw data reveals data problems early
- Critical for debugging pipelines

### 👉 Question to Students:
- Should business users see this data?

---

# 📘 Week 7 — Silver: Conformance & Integration

- Combining several sources  

- Conforming codes, names and keys  

- Validation  

- Trusted datasets  

---

# 📊 Week 7 — Example

```sql
SELECT TRY_CAST(amount AS DOUBLE) AS amount
FROM bronze_sales
WHERE TRY_CAST(amount AS DOUBLE) IS NOT NULL;
```

- Clean numeric values  

- Remove bad rows  

- Validation  

- Trust building  

### 👉 Business Insight:
- Trusted data leads to reliable metrics
- Cleaning decisions affect outcomes

### 👉 Question to Students:
- Are we losing important data here?

---

# 📘 Week 8 — Gold Layer & Star Schema

- Aggregations
  
- KPIs  

- Star schema (facts + dimensions) in Gold  

- Decision-ready data  

---

# 📊 Week 8 — Example

```sql
SELECT region, 
       SUM(amount) AS revenue
FROM silver_sales
GROUP BY region;
```

- KPI generation  

- Aggregation  

- Business insight  

- Dashboard-ready  

### 👉 Business Insight:
- Direct input to dashboards
- Drives executive decisions

### 👉 Question to Students:
- What KPI would you add next?

---

# 📘 Week 9 — End-to-End Pipeline & Project Workshop

- End-to-end pipelines  

- Incremental processing  

- Monitoring  

- Project workshop: build your own pipeline  

---

# 📊 Week 9 — Example

#### orders placed “since yesterday at midnight”

```sql
SELECT *
FROM sales
WHERE order_date > CURRENT_DATE - INTERVAL '1 day';
```

#### orders placed in “last 24 hours”
```sql
SELECT *
FROM sales
WHERE order_date > CURRENT_TIMESTAMP - INTERVAL '1 day';
```

Requirement      | Correct Expression
-----------------|-------------------
Yesterday + today| `CURRENT_DATE - INTERVAL '1 day'`
Last 24 hours    | `CURRENT_TIMESTAMP - INTERVAL '1 day'`


- Incremental load  

- Efficient processing 
 
- Real-world pattern  

- Performance focus  

### 👉 Business Insight:
- Faster updates = fresher insights
- Reduces system load

### 👉 Question to Students:
- Why not reload all data every time?

---

# 📘 Week 10 — Final Project

- End-to-end solution  

- Visualization  

- Data storytelling  

- Business presentation  

---

# 📊 Week 10 — Example

- Combine SQL + Python + visualization  

- Build pipeline  

- Present insights  

- Explain decisions  

### 👉 Business Insight:
- Communication is as important as analysis
- Insight must lead to action

### 👉 Question to Students:
- What makes a story convincing?

---

# 💬 Final Thought

## Data → Insight → Decision  

---

# 🙌 Let’s Begin

- Ask questions
  
- Practice  

- Build systems  
