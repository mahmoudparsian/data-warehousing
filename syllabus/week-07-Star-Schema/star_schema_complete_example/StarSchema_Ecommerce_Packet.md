# ⭐ Star Schema (E‑Commerce) — Teaching Packet
**Includes:** OLTP schema + sample data, Star schema, ETL (MySQL), `dim_date` generator, Customer SCD Type 2, and 15 OLAP queries (5 simple, 5 intermediate, 5 intermediate+).  
**Assumes:** MySQL 8.x

---

## 1) What a Star Schema is
A **star schema** is a dimensional model optimized for analytics.

- **Fact table (center):** numeric measures at a defined **grain**
- **Dimensions (spokes):** descriptive attributes used to filter/group facts

**Why it’s used (in one line):** fewer joins + predictable query patterns ⇒ faster aggregations and simpler BI.

---

## 2) Basic Star Schema Example (not overly detailed)
**Business process:** sales (orders)  
**Grain:** *one row per product per order line*

- **fact_sales**: quantity, sales_amount
- **dim_customer**: who bought
- **dim_product**: what they bought
- **dim_store**: where (physical store)  
- **dim_channel**: online vs in‑store  
- **dim_date**: when

---

## 3) OLTP (Operational) Schema — Solid & realistic
OLTP is **normalized** and optimized for fast inserts/updates.

We model:
- customers (with country)
- stores (physical locations)
- products
- orders (channel + optional store)
- order_items (line items)

✅ Full MySQL DDL + inserts are in: **`StarSchema_Ecommerce_Scripts.sql`**

---

## 4) How to populate OLTP (concept)
Typical teaching flow:
1. Insert **reference entities** first (customers, stores, products)
2. Insert **orders**
3. Insert **order_items** (the “lines”)

✅ A small, coherent dataset is included in the SQL file.

---

## 5) Converting OLTP → Star Schema (with solid reasoning)

### Step A — Choose the business process
We choose **Sales** because it’s the most common analytical process:
- revenue trends
- store performance
- customer behavior
- product/category performance

### Step B — Declare the grain (most important step)
**Grain = one row per product per order line**.

**Reasoning:**
- avoids double-counting revenue
- supports product/category analytics naturally
- aligns with OLTP order_items

### Step C — Identify dimensions (the “group by” subjects)
- **Customer** (with country)  
- **Store** (store geography)  
- **Channel** (ONLINE vs IN_STORE)  
- **Product** (category, name)  
- **Date** (year/month/quarter)  

### Step D — Identify measures (what you aggregate)
- quantity
- sales_amount (quantity × unit_price)

### Step E — Decide SCD strategy
Customer location/country can change over time, and you often want “as‑of” correctness.

✅ We convert **Customer** to **SCD Type 2**:
- keep full history of descriptive changes
- facts point to the correct historical customer version

### Step F — Build the star schema
In the star schema we use **surrogate keys** (`*_sk`) for dimensions.
This makes history tracking (SCD2) and integration easier.

✅ Full Star DDL is in the SQL file.

---

## 6) ETL overview (OLTP → Staging → Dimensions → Fact)

**Recommended flow each load run:**
1. Extract OLTP into **staging** (stg_* tables)
2. Load **dim_date** (one-time or incremental)
3. Load small/static dims (dim_channel)
4. Load Type 1 dims (product/store) as overwrite
5. Load **dim_customer_scd2** (expire+insert on change)
6. Load fact_sales by joining staged orders + order_items, and looking up surrogate keys

✅ Full ETL SQL blocks are in the SQL file, including SCD2 change detection.

---

# 7) OLAP Queries (Star Schema)

> **Note:** These run against the **warehouse** tables (dim_* and fact_sales).

## 7.1) 5 SIMPLE queries

### Q1) Total revenue
```sql
SELECT SUM(sales_amount) AS total_revenue
FROM fact_sales;
```

### Q2) Revenue by channel (ONLINE vs IN_STORE)
```sql
SELECT ch.channel_name, SUM(f.sales_amount) AS revenue
FROM fact_sales f
JOIN dim_channel ch ON ch.channel_sk = f.channel_sk
GROUP BY ch.channel_name
ORDER BY revenue DESC;
```

### Q3) Revenue by country (customer)
```sql
SELECT c.country, SUM(f.sales_amount) AS revenue
FROM fact_sales f
JOIN dim_customer_scd2 c ON c.customer_sk = f.customer_sk
GROUP BY c.country
ORDER BY revenue DESC;
```

### Q4) Revenue by store (physical only — excludes online NULLs)
```sql
SELECT s.store_name, SUM(f.sales_amount) AS revenue
FROM fact_sales f
JOIN dim_store s ON s.store_sk = f.store_sk
GROUP BY s.store_name
ORDER BY revenue DESC;
```

### Q5) Monthly revenue
```sql
SELECT d.year, d.month, SUM(f.sales_amount) AS revenue
FROM fact_sales f
JOIN dim_date d ON d.date_id = f.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;
```

---

## 7.2) 5 INTERMEDIATE queries

### Q6) Top 5 products by revenue
```sql
SELECT p.product_name, SUM(f.sales_amount) AS revenue
FROM fact_sales f
JOIN dim_product p ON p.product_sk = f.product_sk
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 5;
```

### Q7) Revenue by category **per country**
```sql
SELECT c.country, p.category, SUM(f.sales_amount) AS revenue
FROM fact_sales f
JOIN dim_customer_scd2 c ON c.customer_sk = f.customer_sk
JOIN dim_product p ON p.product_sk = f.product_sk
GROUP BY c.country, p.category
ORDER BY c.country, revenue DESC;
```

### Q8) Average order value (AOV) by channel
```sql
WITH order_totals AS (
  SELECT order_id, channel_sk, SUM(sales_amount) AS order_total
  FROM fact_sales
  GROUP BY order_id, channel_sk
)
SELECT ch.channel_name, AVG(order_total) AS avg_order_value
FROM order_totals ot
JOIN dim_channel ch ON ch.channel_sk = ot.channel_sk
GROUP BY ch.channel_name;
```

### Q9) Quarterly revenue by store
```sql
SELECT s.store_name, d.year, d.quarter, SUM(f.sales_amount) AS revenue
FROM fact_sales f
JOIN dim_store s ON s.store_sk = f.store_sk
JOIN dim_date d ON d.date_id = f.date_id
GROUP BY s.store_name, d.year, d.quarter
ORDER BY s.store_name, d.year, d.quarter;
```

### Q10) Top 3 customers by lifetime revenue
```sql
SELECT c.customer_id, c.full_name, SUM(f.sales_amount) AS lifetime_revenue
FROM fact_sales f
JOIN dim_customer_scd2 c ON c.customer_sk = f.customer_sk
GROUP BY c.customer_id, c.full_name
ORDER BY lifetime_revenue DESC
LIMIT 3;
```

---

## 7.3) 5 INTERMEDIATE+ queries (fully written)

### Q11) Running monthly revenue (window function)
```sql
WITH monthly AS (
  SELECT d.year, d.month, SUM(f.sales_amount) AS revenue
  FROM fact_sales f
  JOIN dim_date d ON d.date_id = f.date_id
  GROUP BY d.year, d.month
)
SELECT
  year, month, revenue,
  SUM(revenue) OVER (ORDER BY year, month) AS running_revenue
FROM monthly
ORDER BY year, month;
```

### Q12) Year-over-year revenue growth %
```sql
WITH yearly AS (
  SELECT d.year, SUM(f.sales_amount) AS revenue
  FROM fact_sales f
  JOIN dim_date d ON d.date_id = f.date_id
  GROUP BY d.year
)
SELECT
  y.year,
  y.revenue,
  LAG(y.revenue) OVER (ORDER BY y.year) AS prev_year_revenue,
  ROUND(
    (y.revenue - LAG(y.revenue) OVER (ORDER BY y.year))
    / NULLIF(LAG(y.revenue) OVER (ORDER BY y.year), 0) * 100, 2
  ) AS yoy_growth_pct
FROM yearly y
ORDER BY y.year;
```

### Q13) Revenue contribution % by channel (share of total)
```sql
WITH channel_rev AS (
  SELECT channel_sk, SUM(sales_amount) AS revenue
  FROM fact_sales
  GROUP BY channel_sk
),
total AS (
  SELECT SUM(revenue) AS total_revenue FROM channel_rev
)
SELECT
  ch.channel_name,
  cr.revenue,
  ROUND(cr.revenue / NULLIF(t.total_revenue,0) * 100, 2) AS revenue_share_pct
FROM channel_rev cr
JOIN dim_channel ch ON ch.channel_sk = cr.channel_sk
CROSS JOIN total t
ORDER BY cr.revenue DESC;
```

### Q14) Top product **per country** (RANK)
```sql
WITH country_product AS (
  SELECT
    c.country,
    p.product_name,
    SUM(f.sales_amount) AS revenue
  FROM fact_sales f
  JOIN dim_customer_scd2 c ON c.customer_sk = f.customer_sk
  JOIN dim_product p ON p.product_sk = f.product_sk
  GROUP BY c.country, p.product_name
),
ranked AS (
  SELECT
    country, product_name, revenue,
    RANK() OVER (PARTITION BY country ORDER BY revenue DESC) AS rnk
  FROM country_product
)
SELECT country, product_name, revenue
FROM ranked
WHERE rnk = 1
ORDER BY revenue DESC;
```

### Q15) Store performance percentiles (NTILE)
```sql
WITH store_rev AS (
  SELECT s.store_name, SUM(f.sales_amount) AS revenue
  FROM fact_sales f
  JOIN dim_store s ON s.store_sk = f.store_sk
  GROUP BY s.store_name
),
bucketed AS (
  SELECT
    store_name, revenue,
    NTILE(4) OVER (ORDER BY revenue) AS quartile
  FROM store_rev
)
SELECT store_name, revenue, quartile
FROM bucketed
ORDER BY revenue DESC;
```

---

## What to run next
1) Run **`StarSchema_Ecommerce_Scripts.sql`** (it creates OLTP + DW + sample data)  
2) Run the ETL blocks (also in the same SQL file)  
3) Execute the OLAP queries above

---
**Generated:** 2026-02-10
