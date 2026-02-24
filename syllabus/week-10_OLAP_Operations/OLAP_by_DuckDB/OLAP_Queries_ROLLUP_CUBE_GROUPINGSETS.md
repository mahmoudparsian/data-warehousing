# 📊 Online Sales Star Schema — Meaningful OLAP Queries (DuckDB)
**Format:** English question + SQL (DuckDB)  

**Schema:** 

	* FACT table: `sales`, 
	* DIMs : `dates`, `customers`, `products`, `stores` 
**Measures:** `quantity`, `unit_price`, `total_amount`  

**Channel hint:** 
Online rows have `stores.store_id = 'ONLINE'` (and store_name = 'Online')

---

## 0) Quick reference joins (used throughout)

```sql
-- Fact to dimensions
-- sales s
--   JOIN dates d      ON s.date_key     = d.date_key
--   JOIN customers c  ON s.customer_key = c.customer_key
--   JOIN products p   ON s.product_key  = p.product_key
--   JOIN stores st    ON s.store_key    = st.store_key
```

---

# (1) 5 Basic OLAP Queries (Foundation)

### 1.1 Total revenue by year (simple time aggregation)
```sql
SELECT d.year, 
       SUM(s.total_amount) AS revenue
FROM sales s
JOIN dates d ON s.date_key = d.date_key
GROUP BY d.year
ORDER BY d.year;
```

### 1.2 Total revenue by product category
```sql
SELECT p.category, 
       SUM(s.total_amount) AS revenue
FROM sales s
JOIN products p ON s.product_key = p.product_key
GROUP BY p.category
ORDER BY revenue DESC;
```

### 1.3 Revenue by store (includes Online as a “store”)
```sql
SELECT st.store_name, 
       SUM(s.total_amount) AS revenue
FROM sales s
JOIN stores st ON s.store_key = st.store_key
GROUP BY st.store_name
ORDER BY revenue DESC;
```

### 1.4 Average order line value (average total_amount per line item) by year
```sql
SELECT d.year, 
       AVG(s.total_amount) AS avg_line_value
FROM sales s
JOIN dates d ON s.date_key = d.date_key
GROUP BY d.year
ORDER BY d.year;
```

### 1.5 Top categories in January 2024 (basic filter + group)
```sql
SELECT p.category, 
       SUM(s.total_amount) AS total_sales_amount
FROM sales s
JOIN dates d    ON s.date_key = d.date_key
JOIN products p ON s.product_key = p.product_key
WHERE d.year = 2024 AND 
      d.month_of_year = 1
GROUP BY p.category
ORDER BY total_sales_amount DESC;
```

---

# (2) 5 Top-5 Queries Using WITH + Ranking Functions

> Each query returns **Top-5** using `WITH` + `DENSE_RANK()` / `ROW_NUMBER()`.

### 2.1 Top-5 products by revenue in 2024
```sql
WITH product_rev AS (
  SELECT p.product_id, p.product_name, 
         SUM(s.total_amount) AS revenue
  FROM sales s
  JOIN dates d    ON s.date_key = d.date_key
  JOIN products p ON s.product_key = p.product_key
  WHERE d.year = 2024
  GROUP BY p.product_id, p.product_name
),
ranked AS (
  SELECT *,
         DENSE_RANK() OVER (ORDER BY revenue DESC) AS rnk
  FROM product_rev
)
SELECT *
FROM ranked
WHERE rnk <= 5
ORDER BY revenue DESC;
```

### 2.2 Top-5 customers by total spend (lifetime)
```sql
WITH cust_spend AS (
  SELECT c.customer_id, c.customer_name, 
         SUM(s.total_amount) AS spend
  FROM sales s
  JOIN customers c ON s.customer_key = c.customer_key
  GROUP BY c.customer_id, c.customer_name
),
ranked AS (
  SELECT *,
         DENSE_RANK() OVER (ORDER BY spend DESC) AS rnk
  FROM cust_spend
)
SELECT *
FROM ranked
WHERE rnk <= 5
ORDER BY spend DESC;
```

### 2.3 Top-5 categories per year (Top-5 **within each year**)
```sql
WITH cat_year AS (
  SELECT d.year, p.category, 
         SUM(s.total_amount) AS revenue
  FROM sales s
  JOIN dates d    ON s.date_key = d.date_key
  JOIN products p ON s.product_key = p.product_key
  GROUP BY d.year, p.category
),
ranked AS (
  SELECT *,
         DENSE_RANK() OVER (PARTITION BY year ORDER BY revenue DESC) AS rnk
  FROM cat_year
)
SELECT *
FROM ranked
WHERE rnk <= 5
ORDER BY year, revenue DESC;
```

### 2.4 Top-5 stores by revenue in each quarter of 2024
```sql
WITH store_quarter AS (
  SELECT d.quarter, st.store_name, 
         SUM(s.total_amount) AS revenue
  FROM sales s
  JOIN dates d   ON s.date_key = d.date_key
  JOIN stores st ON s.store_key = st.store_key
  WHERE d.year = 2024
  GROUP BY d.quarter, st.store_name
),
ranked AS (
  SELECT *,
         ROW_NUMBER() OVER 
            (PARTITION BY quarter 
             ORDER BY revenue DESC) AS rn
  FROM store_quarter
)
SELECT quarter, store_name, revenue
FROM ranked
WHERE rn <= 5
ORDER BY quarter, revenue DESC;
```

### 2.5 Top-5 customers per segment (Retail/Wholesale) by spend
```sql
WITH segment_spend AS (
  SELECT c.segment, c.customer_id, c.customer_name,
         SUM(s.total_amount) AS spend
  FROM sales s
  JOIN customers c ON s.customer_key = c.customer_key
  GROUP BY c.segment, c.customer_id, c.customer_name
),
ranked AS (
  SELECT *,
         ROW_NUMBER() OVER 
           (PARTITION BY segment ORDER BY spend DESC) 
          AS rn
  FROM segment_spend
)
SELECT segment, customer_id, customer_name, spend
FROM ranked
WHERE rn <= 5
ORDER BY segment, spend DESC;
```

---

# (3) 5 CUBE Queries

> DuckDB supports `GROUP BY CUBE(...)` directly.

### 3.1 Revenue across all combinations of (year, category, channel)
```sql
SELECT
  d.year,
  p.category,
  CASE 
      WHEN st.store_id = 'ONLINE' 
           THEN 'Online' 
           ELSE 'Physical' 
      END AS channel,
  SUM(s.total_amount) AS revenue
FROM sales s
JOIN dates d    ON s.date_key = d.date_key
JOIN products p ON s.product_key = p.product_key
JOIN stores st  ON s.store_key = st.store_key
GROUP BY CUBE(d.year, p.category, channel)
ORDER BY d.year NULLS LAST, 
         p.category NULLS LAST, 
         channel NULLS LAST;
```

### 3.2 Revenue cube for (quarter, store_country, category)
```sql
SELECT
  d.quarter,
  st.country AS store_country,
  p.category,
  SUM(s.total_amount) AS revenue
FROM sales s
JOIN dates d    ON s.date_key = d.date_key
JOIN stores st  ON s.store_key = st.store_key
JOIN products p ON s.product_key = p.product_key
GROUP BY CUBE(d.quarter, st.country, p.category)
ORDER BY d.quarter NULLS LAST, 
         store_country NULLS LAST, 
         p.category NULLS LAST;
```

### 3.3 Quantity cube for (year, brand, color)
```sql
SELECT
  d.year,
  p.brand,
  p.color,
  SUM(s.quantity) AS units
FROM sales s
JOIN dates d    ON s.date_key = d.date_key
JOIN products p ON s.product_key = p.product_key
GROUP BY CUBE(d.year, p.brand, p.color)
ORDER BY 
         d.year NULLS LAST, 
         brand NULLS LAST, 
         color NULLS LAST;
```

### 3.4 Revenue cube for (customer_country, store_country, year)
```sql
SELECT
  c.country AS customer_country,
  st.country AS store_country,
  d.year,
  SUM(s.total_amount) AS revenue
FROM sales s
JOIN customers c ON s.customer_key = c.customer_key
JOIN stores st   ON s.store_key = st.store_key
JOIN dates d     ON s.date_key = d.date_key
GROUP BY CUBE(customer_country, store_country, d.year)
ORDER BY 
        customer_country NULLS LAST, 
        store_country NULLS LAST, 
        d.year NULLS LAST;
```

### 3.5 CUBE + GROUPING() indicators to label subtotal rows
```sql
SELECT
  d.year,
  p.category,
  st.store_name,
  SUM(s.total_amount) AS revenue,
  GROUPING(d.year)        AS g_year,
  GROUPING(p.category)    AS g_category,
  GROUPING(st.store_name) AS g_store
FROM sales s
JOIN dates d    ON s.date_key = d.date_key
JOIN products p ON s.product_key = p.product_key
JOIN stores st  ON s.store_key = st.store_key
GROUP BY CUBE(d.year, p.category, st.store_name)
ORDER BY 
         g_year, 
         g_category, 
         g_store,
         d.year NULLS LAST, 
         p.category NULLS LAST, 
         st.store_name NULLS LAST;
```

---

# (4) 5 ROLLUP Queries

> ROLLUP is hierarchical subtotaling (left-to-right order matters).

### 4.1 Revenue rollup: (year → quarter → month)
```sql
SELECT d.year, d.quarter, d.month_of_year, SUM(s.total_amount) AS revenue
FROM sales s
JOIN dates d ON s.date_key = d.date_key
GROUP BY ROLLUP(d.year, d.quarter, d.month_of_year)
ORDER BY d.year NULLS LAST, d.quarter NULLS LAST, d.month_of_year NULLS LAST;
```

### 4.2 Revenue rollup: (category → brand)
```sql
SELECT p.category, p.brand, SUM(s.total_amount) AS revenue
FROM sales s
JOIN products p ON s.product_key = p.product_key
GROUP BY ROLLUP(p.category, p.brand)
ORDER BY p.category NULLS LAST, p.brand NULLS LAST;
```

### 4.3 Units rollup: (channel → store_name)
```sql
SELECT
  CASE WHEN st.store_id='ONLINE' THEN 'Online' ELSE 'Physical' END AS channel,
  st.store_name,
  SUM(s.quantity) AS units
FROM sales s
JOIN stores st ON s.store_key = st.store_key
GROUP BY ROLLUP(channel, st.store_name)
ORDER BY channel NULLS LAST, st.store_name NULLS LAST;
```

### 4.4 Revenue rollup: (customer_country → segment)
```sql
SELECT c.country, c.segment, SUM(s.total_amount) AS revenue
FROM sales s
JOIN customers c ON s.customer_key = c.customer_key
GROUP BY ROLLUP(c.country, c.segment)
ORDER BY c.country NULLS LAST, c.segment NULLS LAST;
```

### 4.5 Revenue rollup: (year → category → product_name)
```sql
SELECT d.year, p.category, p.product_name, SUM(s.total_amount) AS revenue
FROM sales s
JOIN dates d    ON s.date_key = d.date_key
JOIN products p ON s.product_key = p.product_key
GROUP BY ROLLUP(d.year, p.category, p.product_name)
ORDER BY d.year NULLS LAST, p.category NULLS LAST, p.product_name NULLS LAST;
```

---

# (5) 5 Roll-Down (Drill-Down) Queries

> “Roll-down” here means: start from a summary, then drill into more detail.

### 5.1 Drill down: from year totals → month totals for 2024
```sql
-- Summary: year totals
SELECT d.year, SUM(s.total_amount) AS revenue
FROM sales s JOIN dates d ON s.date_key = d.date_key
GROUP BY d.year
ORDER BY d.year;

-- Drill-down: months within 2024
SELECT d.month_of_year, SUM(s.total_amount) AS revenue
FROM sales s JOIN dates d ON s.date_key = d.date_key
WHERE d.year = 2024
GROUP BY d.month_of_year
ORDER BY d.month_of_year;
```

### 5.2 Drill down: top category in 2024 → top products within that category
```sql
WITH top_cat AS (
  SELECT p.category, SUM(s.total_amount) AS revenue
  FROM sales s
  JOIN dates d    ON s.date_key = d.date_key
  JOIN products p ON s.product_key = p.product_key
  WHERE d.year = 2024
  GROUP BY p.category
  ORDER BY revenue DESC
  LIMIT 1
)
SELECT p.category, p.product_name, SUM(s.total_amount) AS revenue
FROM sales s
JOIN dates d    ON s.date_key = d.date_key
JOIN products p ON s.product_key = p.product_key
JOIN top_cat tc ON p.category = tc.category
WHERE d.year = 2024
GROUP BY p.category, p.product_name
ORDER BY revenue DESC
LIMIT 10;
```

### 5.3 Drill down: online vs physical → which physical stores drive revenue?
```sql
-- Channel summary
SELECT
  CASE WHEN st.store_id='ONLINE' THEN 'Online' ELSE 'Physical' END AS channel,
  SUM(s.total_amount) AS revenue
FROM sales s JOIN stores st ON s.store_key = st.store_key
GROUP BY channel
ORDER BY revenue DESC;

-- Drill-down: physical stores only
SELECT st.store_name, SUM(s.total_amount) AS revenue
FROM sales s JOIN stores st ON s.store_key = st.store_key
WHERE st.store_id <> 'ONLINE'
GROUP BY st.store_name
ORDER BY revenue DESC;
```

### 5.4 Drill down: customer country → segments within a chosen country (example: USA)
```sql
-- Country summary
SELECT c.country, SUM(s.total_amount) AS revenue
FROM sales s JOIN customers c ON s.customer_key = c.customer_key
GROUP BY c.country
ORDER BY revenue DESC;

-- Drill-down: segments within USA
SELECT c.segment, SUM(s.total_amount) AS revenue
FROM sales s JOIN customers c ON s.customer_key = c.customer_key
WHERE c.country = 'USA'
GROUP BY c.segment
ORDER BY revenue DESC;
```

### 5.5 Drill down: brand summary → colors within a brand (pick top brand in 2024)
```sql
WITH top_brand AS (
  SELECT p.brand, SUM(s.total_amount) AS revenue
  FROM sales s
  JOIN dates d    ON s.date_key = d.date_key
  JOIN products p ON s.product_key = p.product_key
  WHERE d.year = 2024
  GROUP BY p.brand
  ORDER BY revenue DESC
  LIMIT 1
)
SELECT p.brand, p.color, SUM(s.total_amount) AS revenue
FROM sales s
JOIN dates d     ON s.date_key = d.date_key
JOIN products p  ON s.product_key = p.product_key
JOIN top_brand b ON p.brand = b.brand
WHERE d.year = 2024
GROUP BY p.brand, p.color
ORDER BY revenue DESC;
```

---

# (6) 5 Slice Queries (Fix one dimension value)

> Slice = fix one dimension (e.g., year=2024) and analyze the rest.

### 6.1 Slice year=2024: revenue by category
```sql
SELECT p.category, SUM(s.total_amount) AS revenue
FROM sales s
JOIN dates d    ON s.date_key = d.date_key
JOIN products p ON s.product_key = p.product_key
WHERE d.year = 2024
GROUP BY p.category
ORDER BY revenue DESC;
```

### 6.2 Slice category='Electronics': revenue by year
```sql
SELECT d.year, SUM(s.total_amount) AS revenue
FROM sales s
JOIN dates d    ON s.date_key = d.date_key
JOIN products p ON s.product_key = p.product_key
WHERE p.category = 'Electronics'
GROUP BY d.year
ORDER BY d.year;
```

### 6.3 Slice store='Online': monthly revenue trend (2024)
```sql
SELECT d.month_of_year, SUM(s.total_amount) AS revenue
FROM sales s
JOIN dates d   ON s.date_key = d.date_key
JOIN stores st ON s.store_key = st.store_key
WHERE d.year = 2024 AND st.store_id = 'ONLINE'
GROUP BY d.month_of_year
ORDER BY d.month_of_year;
```

### 6.4 Slice segment='Retail': top brands (2024)
```sql
SELECT p.brand, SUM(s.total_amount) AS revenue
FROM sales s
JOIN dates d     ON s.date_key = d.date_key
JOIN customers c ON s.customer_key = c.customer_key
JOIN products p  ON s.product_key = p.product_key
WHERE d.year = 2024 AND c.segment = 'Retail'
GROUP BY p.brand
ORDER BY revenue DESC
LIMIT 10;
```

### 6.5 Slice customer_country='CANADA': revenue by channel
```sql
SELECT
  CASE WHEN st.store_id='ONLINE' THEN 'Online' ELSE 'Physical' END AS channel,
  SUM(s.total_amount) AS revenue
FROM sales s
JOIN customers c ON s.customer_key = c.customer_key
JOIN stores st   ON s.store_key = st.store_key
WHERE c.country = 'CANADA'
GROUP BY channel
ORDER BY revenue DESC;
```

---

# (7) 5 Dice Queries (Multiple dimension filters)

> Dice = filter on multiple dimensions (e.g., year=2024 AND category IN (...) AND country='USA').

### 7.1 Dice: 2024, categories Electronics/Home, channel=Online
```sql
SELECT p.category, SUM(s.total_amount) AS revenue
FROM sales s
JOIN dates d    ON s.date_key = d.date_key
JOIN products p ON s.product_key = p.product_key
JOIN stores st  ON s.store_key = st.store_key
WHERE d.year = 2024
  AND p.category IN ('Electronics','Home')
  AND st.store_id = 'ONLINE'
GROUP BY p.category
ORDER BY revenue DESC;
```

### 7.2 Dice: USA customers, 2023–2024, Physical stores only
```sql
SELECT d.year, SUM(s.total_amount) AS revenue
FROM sales s
JOIN dates d     ON s.date_key = d.date_key
JOIN customers c ON s.customer_key = c.customer_key
JOIN stores st   ON s.store_key = st.store_key
WHERE c.country = 'USA'
  AND d.year IN (2023, 2024)
  AND st.store_id <> 'ONLINE'
GROUP BY d.year
ORDER BY d.year;
```

### 7.3 Dice: Q4 only, Fashion category, top 10 products by revenue
```sql
SELECT p.product_name, SUM(s.total_amount) AS revenue
FROM sales s
JOIN dates d    ON s.date_key = d.date_key
JOIN products p ON s.product_key = p.product_key
WHERE d.quarter = 4 AND p.category = 'Fashion'
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 10;
```

### 7.4 Dice: Segment=Wholesale, brand='Acme', year=2025
```sql
SELECT p.category, SUM(s.total_amount) AS revenue
FROM sales s
JOIN dates d     ON s.date_key = d.date_key
JOIN customers c ON s.customer_key = c.customer_key
JOIN products p  ON s.product_key = p.product_key
WHERE d.year = 2025
  AND c.segment = 'Wholesale'
  AND p.brand = 'Acme'
GROUP BY p.category
ORDER BY revenue DESC;
```

### 7.5 Dice: Non-USA physical stores, 2024, by month
```sql
SELECT d.month_of_year, SUM(s.total_amount) AS revenue
FROM sales s
JOIN dates d   ON s.date_key = d.date_key
JOIN stores st ON s.store_key = st.store_key
WHERE d.year = 2024
  AND st.country <> 'USA'
  AND st.store_id <> 'ONLINE'
GROUP BY d.month_of_year
ORDER BY d.month_of_year;
```

---

# (8) 5 Pivot Queries (Simple → Intermediate)

> Pivot in SQL is commonly done with conditional aggregation (`SUM(CASE WHEN ... THEN ... END)`).

### 8.1 Pivot revenue by year into columns (2023/2024/2025) per category
```sql
SELECT
  p.category,
  SUM(CASE WHEN d.year=2023 THEN s.total_amount ELSE 0 END) AS rev_2023,
  SUM(CASE WHEN d.year=2024 THEN s.total_amount ELSE 0 END) AS rev_2024,
  SUM(CASE WHEN d.year=2025 THEN s.total_amount ELSE 0 END) AS rev_2025
FROM sales s
JOIN dates d    ON s.date_key = d.date_key
JOIN products p ON s.product_key = p.product_key
GROUP BY p.category
ORDER BY rev_2024 DESC;
```

### 8.2 Pivot: Online vs Physical revenue per month (2024)
```sql
SELECT
  d.month_of_year AS month,
  SUM(CASE WHEN st.store_id='ONLINE' THEN s.total_amount ELSE 0 END) AS online_rev,
  SUM(CASE WHEN st.store_id<>'ONLINE' THEN s.total_amount ELSE 0 END) AS physical_rev
FROM sales s
JOIN dates d   ON s.date_key = d.date_key
JOIN stores st ON s.store_key = st.store_key
WHERE d.year = 2024
GROUP BY d.month_of_year
ORDER BY month;
```

### 8.3 Pivot: Revenue by quarter across categories (selected categories)
```sql
SELECT
  d.quarter,
  SUM(CASE WHEN p.category='Electronics' THEN s.total_amount ELSE 0 END) AS electronics_rev,
  SUM(CASE WHEN p.category='Home'        THEN s.total_amount ELSE 0 END) AS home_rev,
  SUM(CASE WHEN p.category='Fashion'     THEN s.total_amount ELSE 0 END) AS fashion_rev
FROM sales s
JOIN dates d    ON s.date_key = d.date_key
JOIN products p ON s.product_key = p.product_key
WHERE d.year = 2024
GROUP BY d.quarter
ORDER BY d.quarter;
```

### 8.4 Pivot: Customer segment × channel revenue matrix (2024)
```sql
SELECT
  c.segment,
  SUM(CASE WHEN st.store_id='ONLINE' THEN s.total_amount ELSE 0 END) AS online_rev,
  SUM(CASE WHEN st.store_id<>'ONLINE' THEN s.total_amount ELSE 0 END) AS physical_rev
FROM sales s
JOIN dates d     ON s.date_key = d.date_key
JOIN customers c ON s.customer_key = c.customer_key
JOIN stores st   ON s.store_key = st.store_key
WHERE d.year = 2024
GROUP BY c.segment
ORDER BY online_rev DESC;
```

### 8.5 Pivot (intermediate): Top 5 brands, revenue by quarter (2024)
```sql
WITH brand_rev AS (
  SELECT p.brand, SUM(s.total_amount) AS revenue
  FROM sales s
  JOIN dates d    ON s.date_key = d.date_key
  JOIN products p ON s.product_key = p.product_key
  WHERE d.year = 2024
  GROUP BY p.brand
),
top5 AS (
  SELECT brand
  FROM brand_rev
  ORDER BY revenue DESC
  LIMIT 5
)
SELECT
  p.brand,
  SUM(CASE WHEN d.quarter=1 THEN s.total_amount ELSE 0 END) AS q1_rev,
  SUM(CASE WHEN d.quarter=2 THEN s.total_amount ELSE 0 END) AS q2_rev,
  SUM(CASE WHEN d.quarter=3 THEN s.total_amount ELSE 0 END) AS q3_rev,
  SUM(CASE WHEN d.quarter=4 THEN s.total_amount ELSE 0 END) AS q4_rev
FROM sales s
JOIN dates d    ON s.date_key = d.date_key
JOIN products p ON s.product_key = p.product_key
JOIN top5 t     ON p.brand = t.brand
WHERE d.year = 2024
GROUP BY p.brand
ORDER BY q4_rev DESC;
```

---

# (9) 5 Advanced Analytics Queries (AI Expert Picks)

### 9.1 Pareto: What % of revenue comes from top 20% of products?
```sql
WITH product_rev AS (
  SELECT p.product_key, SUM(s.total_amount) AS revenue
  FROM sales s
  JOIN products p ON s.product_key = p.product_key
  GROUP BY p.product_key
),
ranked AS (
  SELECT
    product_key,
    revenue,
    ROW_NUMBER() OVER (ORDER BY revenue DESC) AS rn,
    COUNT(*) OVER () AS n_products,
    SUM(revenue) OVER () AS total_revenue
  FROM product_rev
),
top20 AS (
  SELECT *
  FROM ranked
  WHERE rn <= CAST(n_products * 0.20 AS BIGINT)
)
SELECT
  ROUND(100 * SUM(revenue) / MAX(total_revenue), 2) AS pct_revenue_from_top_20pct_products
FROM top20;
```

### 9.2 Customer “RFM-lite”: Recency, Frequency, Monetary
```sql
WITH cust_metrics AS (
  SELECT
    c.customer_id,
    MAX(d.full_date) AS last_purchase_date,
    COUNT(*) AS frequency_lines,
    SUM(s.total_amount) AS monetary_spend
  FROM sales s
  JOIN customers c ON s.customer_key = c.customer_key
  JOIN dates d     ON s.date_key = d.date_key
  GROUP BY c.customer_id
)
SELECT *
FROM cust_metrics
ORDER BY monetary_spend DESC
LIMIT 20;
```

### 9.3 Cohort analysis: revenue by cohort year (first purchase year) and activity year
```sql
WITH first_year AS (
  SELECT s.customer_key, MIN(d.year) AS cohort_year
  FROM sales s
  JOIN dates d ON s.date_key = d.date_key
  GROUP BY s.customer_key
),
cohort_rev AS (
  SELECT
    fy.cohort_year,
    d.year AS activity_year,
    SUM(s.total_amount) AS revenue
  FROM sales s
  JOIN dates d       ON s.date_key = d.date_key
  JOIN first_year fy ON s.customer_key = fy.customer_key
  GROUP BY fy.cohort_year, d.year
)
SELECT *
FROM cohort_rev
ORDER BY cohort_year, activity_year;
```

### 9.4 Price dispersion by category (detect categories with high price variability)
```sql
SELECT
  p.category,
  AVG(s.unit_price) AS avg_price,
  STDDEV_SAMP(s.unit_price) AS std_price,
  ROUND(STDDEV_SAMP(s.unit_price) / NULLIF(AVG(s.unit_price),0), 3) AS coeff_var
FROM sales s
JOIN products p ON s.product_key = p.product_key
GROUP BY p.category
ORDER BY coeff_var DESC;
```

### 9.5 “Anomaly” months: revenue > mean + 2 std dev (2024)
```sql
WITH monthly AS (
  SELECT d.month_of_year AS month, SUM(s.total_amount) AS revenue
  FROM sales s
  JOIN dates d ON s.date_key = d.date_key
  WHERE d.year = 2024
  GROUP BY d.month_of_year
),
stats AS (
  SELECT AVG(revenue) AS avg_rev, STDDEV_SAMP(revenue) AS std_rev
  FROM monthly
)
SELECT m.month, m.revenue
FROM monthly m
CROSS JOIN stats s
WHERE m.revenue > s.avg_rev + 2*s.std_rev
ORDER BY m.revenue DESC;
```

---

## Notes for DuckDB CLI demos
- If output truncates (e.g., “40 shown”), run:
  ```sql
  .maxrows 200
  ```
- Export any query result:
  ```sql
  COPY (SELECT ...) TO 'result.csv' (HEADER, DELIMITER ',');
  ```

---

✅ **Total queries provided:** 45  
(5 basic + 40 intermediate/advanced across the requested OLAP patterns)
