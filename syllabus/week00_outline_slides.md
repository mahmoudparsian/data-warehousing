---
author: Mahmoud Parsian  
marp: true  
theme: default  
paginate: true  
title: ISBA — Modern Data Warehousing  
class: lead  
---

# 🎯 Course Objectives

- Understand modern data warehouse architectures
- Learn analytical SQL deeply
- Build data pipelines (Bronze → Silver → Gold)
- Think like a data analyst
- Connect SQL with LLMs and AI


---

# 📅 Course Roadmap (Detailed)

- Week 1 → SQL Foundations  
- Week 2 → Analytical Thinking  
- Week 3 → Data Warehousing  
- Week 4 → ETL & OLAP  
- Week 5 → Medallion Architecture  
- Week 6 → Bronze Layer  
- Week 7 → Silver Layer  
- Week 8 → Gold Layer  
- Week 9 → Pipelines  
- Week 10 → Final Project  

---

# 📘 Week 1 — SQL Foundations

- SELECT, WHERE, GROUP BY  
- Filtering and aggregation  
- Working with real datasets  
- Building SQL intuition  

---

# 📊 Week 1 — Example

```sql
SELECT region, COUNT(*) AS num_orders
FROM sales
GROUP BY region;
```

- Count orders per region  
- Basic aggregation  
- First business insight  
- Builds SQL confidence  

👉 Business Insight:
- Which region has the most activity?
- Are some regions underperforming?

👉 Question to Students:
- If one region is low, what could that mean?

---

# 📘 Week 2 — Analytical Thinking

- Aggregations + HAVING  
- Window functions  
- Top-N queries  
- Business-driven SQL  

---

# 📊 Week 2 — Example

```sql
SELECT region, amount,
RANK() OVER (PARTITION BY region ORDER BY amount DESC) rnk
FROM sales;
```

- Top-N per region  
- Partitioning concept  
- Ranking logic  
- Real-world use case  

👉 Business Insight:
- Identify top customers/products per region
- Compare performance within groups

👉 Question to Students:
- Why not just use GROUP BY here?

---

# 📘 Week 3 — Data Warehousing

- Star schema  
- Fact vs dimension  
- Analytical modeling  
- OLAP queries  

---

# 📊 Week 3 — Example

```sql
SELECT d.region, SUM(f.sales)
FROM fact_sales f
JOIN dim_region d ON f.region_id = d.id
GROUP BY d.region;
```

- Fact + dimension join  
- Star schema query  
- Aggregation  
- Business reporting  

👉 Business Insight:
- Combine descriptive + numeric data
- Enable flexible reporting

👉 Question to Students:
- Why separate fact and dimension tables?

---

# 📘 Week 4 — ETL & OLAP

- ETL vs ELT  
- Data cleaning  
- Roll-up / drill-down  
- Pipeline thinking  

---

# 📊 Week 4 — Example

```sql
SELECT LOWER(TRIM(region)), SUM(amount)
FROM raw_sales
GROUP BY LOWER(TRIM(region));
```

- Cleaning + aggregation  
- ETL transformation  
- OLAP query  
- Data quality impact  

👉 Business Insight:
- Cleaning changes results significantly
- Poor data → wrong decisions

👉 Question to Students:
- What happens if we skip cleaning?

---

# 📘 Week 5 — Medallion Architecture

- Bronze / Silver / Gold  
- Layered architecture  
- Data lifecycle  
- Scalability  

---

# 📊 Week 5 — Example

```sql
SELECT region, SUM(amount)
FROM silver_sales
GROUP BY region;
```

- Clean → aggregate  
- Layered thinking  
- Business output  
- Reusable logic  

👉 Business Insight:
- Gold tables simplify reporting
- Consistency across dashboards

👉 Question to Students:
- Why not query Bronze directly?

---

# 📘 Week 6 — Bronze Layer

- Raw ingestion  
- Handling messy data  
- Data profiling  
- Source of truth  

---

# 📊 Week 6 — Example

```sql
SELECT * FROM bronze_sales;
```

- Raw inspection  
- Identify issues  
- Debugging stage  
- No transformation  

👉 Business Insight:
- Raw data reveals data problems early
- Critical for debugging pipelines

👉 Question to Students:
- Should business users see this data?

---

# 📘 Week 7 — Silver Layer

- Cleaning  
- Transformation  
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

👉 Business Insight:
- Trusted data leads to reliable metrics
- Cleaning decisions affect outcomes

👉 Question to Students:
- Are we losing important data here?

---

# 📘 Week 8 — Gold Layer

- Aggregations  
- KPIs  
- Reporting tables  
- Decision-ready data  

---

# 📊 Week 8 — Example

```sql
SELECT region, SUM(amount) AS revenue
FROM silver_sales
GROUP BY region;
```

- KPI generation  
- Aggregation  
- Business insight  
- Dashboard-ready  

👉 Business Insight:
- Direct input to dashboards
- Drives executive decisions

👉 Question to Students:
- What KPI would you add next?

---

# 📘 Week 9 — Pipelines

- End-to-end pipelines  
- Incremental processing  
- Monitoring  
- Performance optimization  

---

# 📊 Week 9 — Example

```sql
SELECT *
FROM sales
WHERE order_date > CURRENT_DATE - INTERVAL '1 day';
```

- Incremental load  
- Efficient processing  
- Real-world pattern  
- Performance focus  

👉 Business Insight:
- Faster updates = fresher insights
- Reduces system load

👉 Question to Students:
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

👉 Business Insight:
- Communication is as important as analysis
- Insight must lead to action

👉 Question to Students:
- What makes a story convincing?

---

# 💬 Final Thought

Data → Insight → Decision  

---

# 🙌 Let’s Begin

- Ask questions  
- Practice  
- Build systems  
