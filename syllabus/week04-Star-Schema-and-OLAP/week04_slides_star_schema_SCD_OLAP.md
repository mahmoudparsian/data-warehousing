---
marp: true
title: Week 4 — Star Schema in Depth, SCD and OLAP
paginate: true
theme: default
class: lead
---

# Week 4  
## Star Schema in Depth · SCD · OLAP

*(These slides were part of the original week 3 deck.)*

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

---

# 🧮 Session 2 — Subtotals in ONE Query

Roll-up by hand needs one query per level.
DuckDB (and most warehouses) can return **all levels at once**:

| Clause | Returns |
|---|---|
| `GROUP BY ROLLUP (a, b)` | (a, b) · (a) · () = drill **path** subtotals |
| `GROUP BY CUBE (a, b)` | (a, b) · (a) · (b) · () = **all** combinations |
| `GROUP BY GROUPING SETS ((a), (b), ())` | exactly the groups you list |

Examples use the online-sales star (`OLAP/OLAP_by_DuckDB/`), revenue in $M.

---

# 🔼 ROLLUP

```sql
SELECT c.segment, c.gender, ROUND(SUM(s.total_amount)/1e6, 2) AS revenue_m
FROM sales s JOIN customers c USING (customer_key)
GROUP BY ROLLUP (c.segment, c.gender)
ORDER BY c.segment NULLS LAST, c.gender NULLS LAST;
```

| segment | gender | revenue_m |
|---|---|---|
| Retail | FEMALE | 11.82 |
| Retail | MALE | 106.56 |
| Retail | NULL | **118.38** |
| Wholesale | FEMALE | 11.62 |
| Wholesale | MALE | 105.92 |
| Wholesale | NULL | **117.53** |
| NULL | NULL | **235.91** |

👉 `NULL` here means **"all"**: a subtotal row, not missing data

---

# 🧊 CUBE

```sql
GROUP BY CUBE (c.segment, c.gender)
```

Same as ROLLUP **plus** the totals for each gender across segments:

| segment | gender | revenue_m |
|---|---|---|
| NULL | FEMALE | 23.44 |
| NULL | MALE | 212.47 |

- 2 dimensions → 4 grouping levels; 3 dimensions → 8 levels
- Order of columns matters for ROLLUP, **not** for CUBE

---

# 🏷️ GROUPING(): Label the Subtotals

```sql
SELECT CASE WHEN GROUPING(c.segment) = 1 THEN 'ALL'
            ELSE c.segment END                AS segment,
       ROUND(SUM(s.total_amount)/1e6, 2)      AS revenue_m
FROM sales s JOIN customers c USING (customer_key)
GROUP BY ROLLUP (c.segment)
ORDER BY GROUPING(c.segment), segment;
```

| segment | revenue_m |
|---|---|
| Retail | 118.38 |
| Wholesale | 117.53 |
| ALL | 235.91 |

👉 `GROUPING(col)` = 1 on rows where `col` was rolled up

---

# 🔄 PIVOT: Rows → Columns

```sql
PIVOT (SELECT c.segment, c.gender, s.total_amount
       FROM sales s JOIN customers c USING (customer_key))
ON gender
USING SUM(total_amount);
```

| segment | FEMALE | MALE |
|---|---|---|
| Retail | 11.82 M | 106.56 M |
| Wholesale | 11.62 M | 105.92 M |

👉 The crosstab managers expect, and exactly what a **Tableau** text table shows

---

# 📊 From SQL to Tableau

1. Build the summary in SQL (Gold-style table)
2. `COPY (SELECT …) TO 'result.csv' (HEADER);`
3. Tableau: **Connect → Text file** → drag dimensions to Columns/Rows/Color, measures to Rows
4. Tableau does roll-up / drill-down / slice / dice **interactively** (hierarchies, filters)

👉 Lab 4.2: your first Tableau line chart
👉 Tableau decks: [`resources/Tableau/`](../../resources/Tableau/)
