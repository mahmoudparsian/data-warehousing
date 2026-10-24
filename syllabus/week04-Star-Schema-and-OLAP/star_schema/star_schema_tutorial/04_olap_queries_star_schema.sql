
-- ============================================================
-- OLAP Query Pack (Star Schema) — run in dw_demo
-- ============================================================

USE dw_demo;

-- 1) Revenue by year
SELECT d.year, SUM(f.sales_amount) AS revenue
FROM fact_sales f
JOIN dim_date d ON d.date_key = f.date_key
GROUP BY d.year
ORDER BY d.year;

-- 2) Revenue by month (last 12 months)
SELECT d.year, d.month, d.month_name, SUM(f.sales_amount) AS revenue
FROM fact_sales f
JOIN dim_date d ON d.date_key = f.date_key
WHERE d.full_date >= DATE_SUB(CURDATE(), INTERVAL 365 DAY)
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;

-- 3) Top 10 products by revenue
SELECT p.category, p.product_name, SUM(f.sales_amount) AS revenue
FROM fact_sales f
JOIN dim_product p ON p.product_key = f.product_key
GROUP BY p.category, p.product_name
ORDER BY revenue DESC
LIMIT 10;

-- 4) Revenue by region
SELECT s.region, SUM(f.sales_amount) AS revenue
FROM fact_sales f
JOIN dim_store s ON s.store_key = f.store_key
GROUP BY s.region
ORDER BY revenue DESC;

-- 5) Customer lifetime value (top 20)
SELECT c.customer_id, CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
       SUM(f.sales_amount) AS lifetime_value
FROM fact_sales f
JOIN dim_customer c ON c.customer_key = f.customer_key
GROUP BY c.customer_id, customer_name
ORDER BY lifetime_value DESC
LIMIT 20;

-- 6) Average order value (AOV)
SELECT AVG(order_totals.order_value) AS avg_order_value
FROM (
  SELECT order_id, SUM(sales_amount) AS order_value
  FROM fact_sales
  GROUP BY order_id
) order_totals;

-- 7) Basket size distribution (items per order)
SELECT items_per_order, COUNT(*) AS orders_count
FROM (
  SELECT order_id, COUNT(*) AS items_per_order
  FROM fact_sales
  GROUP BY order_id
) t
GROUP BY items_per_order
ORDER BY items_per_order;

-- 8) Category mix by month
SELECT d.year, d.month, p.category, SUM(f.sales_amount) AS revenue
FROM fact_sales f
JOIN dim_date d ON d.date_key = f.date_key
JOIN dim_product p ON p.product_key = f.product_key
GROUP BY d.year, d.month, p.category
ORDER BY d.year, d.month, revenue DESC;

-- 9) Repeat customers (>= 2 distinct orders)
SELECT COUNT(*) AS repeat_customers
FROM (
  SELECT customer_key
  FROM fact_sales
  GROUP BY customer_key
  HAVING COUNT(DISTINCT order_id) >= 2
) t;

-- 10) Daily revenue trend (last 30 days)
SELECT d.full_date, SUM(f.sales_amount) AS revenue
FROM fact_sales f
JOIN dim_date d ON d.date_key = f.date_key
WHERE d.full_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY d.full_date
ORDER BY d.full_date;
