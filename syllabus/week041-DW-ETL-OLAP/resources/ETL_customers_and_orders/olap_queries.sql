-- 10 OLAP Queries (English + SQL)

-- Q1: Total revenue, tax, and number of orders by year.
SELECT d.year,
       COUNT(*)            AS order_count,
       SUM(o.order_amount) AS revenue,
       SUM(o.tax)          AS total_tax
FROM fact_orders o
JOIN dim_dates d ON o.date_id = d.date_id
GROUP BY d.year
ORDER BY d.year;

-- Q2: Monthly revenue trend per country (year, month, country).
SELECT d.year, d.month, c.country,
       SUM(o.order_amount) AS revenue
FROM fact_orders o
JOIN dim_dates d ON o.date_id = d.date_id
JOIN dim_customers c ON o.customer_id = c.customer_id
GROUP BY d.year, d.month, c.country
ORDER BY d.year, d.month, revenue DESC;

-- Q3: Quarterly revenue split by channel (Online vs In-Store).
SELECT d.year, d.quarter, o.channel,
       SUM(o.order_amount) AS revenue
FROM fact_orders o
JOIN dim_dates d ON o.date_id = d.date_id
GROUP BY d.year, d.quarter, o.channel
ORDER BY d.year, d.quarter, o.channel;

-- Q4: Top 10 customers by lifetime spend (revenue) and their country.
SELECT o.customer_id, c.country,
       SUM(o.order_amount) AS lifetime_spend,
       COUNT(*) AS orders
FROM fact_orders o
JOIN dim_customers c ON o.customer_id = c.customer_id
GROUP BY o.customer_id, c.country
ORDER BY lifetime_spend DESC
LIMIT 10;

-- Q5: Average order value (AOV) by channel and country.
SELECT c.country, o.channel,
       AVG(o.order_amount) AS avg_order_value,
       COUNT(*) AS order_count
FROM fact_orders o
JOIN dim_customers c ON o.customer_id = c.customer_id
GROUP BY c.country, o.channel
ORDER BY c.country, o.channel;

-- Q6: Year-over-year revenue growth by country.
WITH yearly AS (
  SELECT d.year, c.country, SUM(o.order_amount) AS revenue
  FROM fact_orders o
  JOIN dim_dates d ON o.date_id = d.date_id
  JOIN dim_customers c ON o.customer_id = c.customer_id
  GROUP BY d.year, c.country
)
SELECT country, year, revenue,
       LAG(revenue) OVER (PARTITION BY country ORDER BY year) AS prev_year_revenue,
       ROUND(100 * (revenue - LAG(revenue) OVER (PARTITION BY country ORDER BY year))
             / NULLIF(LAG(revenue) OVER (PARTITION BY country ORDER BY year), 0), 2) AS yoy_growth_pct
FROM yearly
ORDER BY country, year;

-- Q7: Revenue rollup by year and month (using ROLLUP).
SELECT d.year, d.month,
       SUM(o.order_amount) AS revenue
FROM fact_orders o
JOIN dim_dates d ON o.date_id = d.date_id
GROUP BY d.year, d.month WITH ROLLUP
ORDER BY d.year, d.month;

-- Q8: Customer cohort analysis: revenue by signup_year and order year.
SELECT c.signup_year,
       d.year AS order_year,
       SUM(o.order_amount) AS revenue,
       COUNT(*) AS orders
FROM fact_orders o
JOIN dim_customers c ON o.customer_id = c.customer_id
JOIN dim_dates d ON o.date_id = d.date_id
GROUP BY c.signup_year, d.year
ORDER BY c.signup_year, d.year;

-- Q9: Age band analysis: revenue and AOV by age group and country.
SELECT c.country,
       CASE
         WHEN c.age < 25 THEN 'Under 25'
         WHEN c.age BETWEEN 25 AND 34 THEN '25-34'
         WHEN c.age BETWEEN 35 AND 44 THEN '35-44'
         WHEN c.age BETWEEN 45 AND 54 THEN '45-54'
         WHEN c.age BETWEEN 55 AND 64 THEN '55-64'
         ELSE '65+'
       END AS age_band,
       SUM(o.order_amount) AS revenue,
       AVG(o.order_amount) AS aov,
       COUNT(*) AS orders
FROM fact_orders o
JOIN dim_customers c ON o.customer_id = c.customer_id
GROUP BY c.country, age_band
ORDER BY c.country, revenue DESC;

-- Q10: Top 5 countries by revenue for each year (dense_rank).
WITH yearly_country AS (
  SELECT d.year, c.country, SUM(o.order_amount) AS revenue
  FROM fact_orders o
  JOIN dim_dates d ON o.date_id = d.date_id
  JOIN dim_customers c ON o.customer_id = c.customer_id
  GROUP BY d.year, c.country
),
ranked AS (
  SELECT *,
         DENSE_RANK() OVER (PARTITION BY year ORDER BY revenue DESC) AS rnk
  FROM yearly_country
)
SELECT year, country, revenue
FROM ranked
WHERE rnk <= 5
ORDER BY year, rnk, country;
