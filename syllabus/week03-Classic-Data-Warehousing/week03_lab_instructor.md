# Week 3 Lab — Instructor Version
## Bike Store Data Warehouse + OLAP Queries

## Teaching Goals
This lab should reinforce:
- the business reason for data warehouses
- the structure of a star schema
- the relationship between DW design and SQL simplicity
- OLAP-style thinking over fact + dimension tables

---

## Part A — Understand the Warehouse

### Task 1 — Concepts
- **Fact table**: stores measurable business events and numeric metrics
- **Dimension table**: stores descriptive business context
- **Grain**: the level of detail represented by one fact row

### Task 2 — Bike Store Warehouse
- Fact table: `fact_sales`
- Dimensions:
  - `dim_date`
  - `dim_customer`
  - `dim_store`
  - `dim_product`
  - `dim_staff`
- Grain:
  - one row per order line item

### Teaching Note
Keep repeating:
> grain first, then schema, then SQL

---

## Part B — Core Analytical Queries

### Task 3 — Total Revenue
```sql
SELECT SUM(revenue) AS total_revenue
FROM fact_sales;
```

**Insight:** This is the simplest warehouse KPI and a baseline sanity check.

---

### Task 4 — Revenue by Store
```sql
SELECT
    s.store_name,
    SUM(f.revenue) AS total_revenue
FROM fact_sales f
JOIN dim_store s
  ON f.store_id = s.store_id
GROUP BY s.store_name
ORDER BY total_revenue DESC;
```

**Insight:** Helps compare location performance and allocate resources.

---

### Task 5 — Revenue by Category
```sql
SELECT
    p.category_name,
    SUM(f.revenue) AS total_revenue
FROM fact_sales f
JOIN dim_product p
  ON f.product_id = p.product_id
GROUP BY p.category_name
ORDER BY total_revenue DESC;
```

**Insight:** Identifies which category drives the business.

---

### Task 6 — Revenue by Brand
```sql
SELECT
    p.brand_name,
    SUM(f.revenue) AS total_revenue
FROM fact_sales f
JOIN dim_product p
  ON f.product_id = p.product_id
GROUP BY p.brand_name
ORDER BY total_revenue DESC;
```

**Insight:** Supports vendor, promotion, and assortment decisions.

---

### Task 7 — Revenue by Year
```sql
SELECT
    d.year,
    SUM(f.revenue) AS total_revenue
FROM fact_sales f
JOIN dim_date d
  ON f.date_id = d.date_id
GROUP BY d.year
ORDER BY d.year;
```

**Insight:** This is a roll-up to a higher time level.

---

### Task 8 — Revenue by Year and Month
```sql
SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(f.revenue) AS total_revenue
FROM fact_sales f
JOIN dim_date d
  ON f.date_id = d.date_id
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;
```

**Insight:** This is a drill-down from year to month.

---

## Part C — OLAP Thinking

### Task 9 — Roll-Up
```sql
SELECT
    d.year,
    SUM(f.revenue) AS total_revenue
FROM fact_sales f
JOIN dim_date d
  ON f.date_id = d.date_id
GROUP BY d.year
ORDER BY d.year;
```

**Insight:** Higher-level summary for executive reporting.

---

### Task 10 — Drill-Down
```sql
SELECT
    d.year,
    d.month,
    SUM(f.revenue) AS total_revenue
FROM fact_sales f
JOIN dim_date d
  ON f.date_id = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;
```

**Insight:** More detailed view for investigation.

---

### Task 11 — Slice
```sql
SELECT
    s.store_name,
    SUM(f.revenue) AS total_revenue
FROM fact_sales f
JOIN dim_store s
  ON f.store_id = s.store_id
WHERE s.state = 'CA'
GROUP BY s.store_name
ORDER BY total_revenue DESC;
```

**Insight:** One fixed dimension value narrows the analysis.

---

### Task 12 — Dice
```sql
SELECT
    d.year,
    p.category_name,
    SUM(f.revenue) AS total_revenue
FROM fact_sales f
JOIN dim_date d
  ON f.date_id = d.date_id
JOIN dim_product p
  ON f.product_id = p.product_id
WHERE d.year = 2023
  AND p.category_name = 'Accessories'
GROUP BY d.year, p.category_name;
```

**Insight:** Multi-dimensional filtering supports targeted analysis.

---

## Part D — Business Analysis

### Task 13 — Top Customers
```sql
SELECT
    c.customer_name,
    SUM(f.revenue) AS total_revenue
FROM fact_sales f
JOIN dim_customer c
  ON f.customer_id = c.customer_id
GROUP BY c.customer_name
ORDER BY total_revenue DESC
LIMIT 5;
```

**Insight:** High-value customers support VIP and retention strategies.

---

### Task 14 — Top Products per Store
```sql
SELECT *
FROM (
    SELECT
        s.store_name,
        p.product_name,
        SUM(f.revenue) AS revenue,
        ROW_NUMBER() OVER (
            PARTITION BY s.store_name
            ORDER BY SUM(f.revenue) DESC
        ) AS rn
    FROM fact_sales f
    JOIN dim_store s
      ON f.store_id = s.store_id
    JOIN dim_product p
      ON f.product_id = p.product_id
    GROUP BY s.store_name, p.product_name
) t
WHERE rn <= 2
ORDER BY store_name, rn;
```

**Insight:** This beautifully connects Week 2 window functions to Week 3 warehouse modeling.

---

### Task 15 — Staff Performance
```sql
SELECT
    st.staff_name,
    SUM(f.revenue) AS total_revenue
FROM fact_sales f
JOIN dim_staff st
  ON f.staff_id = st.staff_id
GROUP BY st.staff_name
ORDER BY total_revenue DESC;
```

**Insight:** Supports evaluation and staffing decisions.

---

### Task 16 — Category Profitability View
```sql
SELECT
    p.category_name,
    AVG(f.revenue) AS avg_line_revenue
FROM fact_sales f
JOIN dim_product p
  ON f.product_id = p.product_id
GROUP BY p.category_name
ORDER BY avg_line_revenue DESC;
```

**Insight:** Shows per-line revenue characteristics, not just total volume.

---

## Reflection Guidance

### 1) Why is star schema easier for analytics?
Because:
- fewer joins
- more intuitive business structure
- easier SQL for analysts

### 2) Why is grain important?
Because grain defines:
- what one fact row means
- which analyses are possible
- how measures should be interpreted

### 3) Most useful business query?
Accept multiple answers if well justified, especially:
- revenue by store
- top customers
- top products per store
- time-based revenue trends

### 4) Connection to Week 2
Week 2 taught:
- ranking
- partitions
- contextual comparisons

Week 3 applies those ideas on top of:
- fact + dimension design
- star schema analytics
- OLAP-style business questions

---

## Final Teaching Message
Students should leave Week 3 understanding:

- a warehouse is not just a database
- it is a business-oriented analytical design
- good dimensional modeling makes good SQL possible
