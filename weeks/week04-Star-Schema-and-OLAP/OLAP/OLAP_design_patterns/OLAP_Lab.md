# OLAP Lab: Intermediate + Advanced

## Retail Star Schema Analytics Lab

### Hands-On SQL Exercises

# 🎓 Lab Objectives

Students should learn:

-   Multi-dimensional aggregation
-   Hierarchical rollups
-   Window functions
-   Ranking within partitions
-   Running totals
-   Percent-of-total calculations
-   Time intelligence (YoY)
-   Pivot transformations
-   Advanced filtering

------------------------------------------------------------------------

# ⭐ Star Schema Used in This Lab

## fact_sales

-   `sales_key`
-   `date_key`
-   `customer_key`
-   `product_key`
-   `store_key`
-   `channel_key`
-   `quantity`
-   `sales_amount`

## Dimensions

-   `dim_date(date_key, full_date, year, quarter, month, day)`
-   `dim_product(product_key, product_name, category, brand)`
-   `dim_customer(customer_key, city, state, country)`
-   `dim_store(store_key, store_name, state, country)`
-   `dim_channel(channel_key, channel_name)`

Grain: **One row per product sold per order line**

------------------------------------------------------------------------

# 🔹 Part 1: Intermediate OLAP Exercises

------------------------------------------------------------------------

## Exercise 1 --- Multi-Dimensional Aggregation

### Task (English)

Find total sales by year and product category.

### Expected Concepts

-   GROUP BY
-   Dimension joins

``` sql
SELECT
    d.year,
    p.category,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY d.year, p.category
ORDER BY d.year, total_sales DESC;
```

------------------------------------------------------------------------

## Exercise 2 --- Top-N per Dimension

### Task

Find top 5 products by total revenue.

``` sql
SELECT p.product_name, 
       SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.product_name
ORDER BY total_sales DESC
LIMIT 5;
```

------------------------------------------------------------------------

## Exercise 3 --- Slice + Dice

### Task

Compute total online sales in California during 2025.

``` sql
SELECT SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_customer c ON f.customer_key = c.customer_key
JOIN dim_channel ch ON f.channel_key = ch.channel_key
WHERE d.year = 2025
AND   c.state = 'CA'
AND   ch.channel_name = 'Online';
```

------------------------------------------------------------------------

## Exercise 4 --- Rollup

### Task

Generate sales by year and month including subtotals.

``` sql
SELECT d.year, 
       d.month, 
       SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month WITH ROLLUP;
```

------------------------------------------------------------------------

# 🔸 Part 2: Advanced OLAP Exercises

------------------------------------------------------------------------

## Exercise 5 --- Ranking per Partition

### Task

Find top 3 products per year.

``` sql
SELECT *
FROM (
    SELECT
        d.year,
        p.product_name,
        SUM(f.sales_amount) AS total_sales,
        RANK() OVER (PARTITION BY d.year ORDER BY SUM(f.sales_amount) DESC) AS rnk
    FROM fact_sales f
    JOIN dim_date d ON f.date_key = d.date_key
    JOIN dim_product p ON f.product_key = p.product_key
    GROUP BY d.year, p.product_name
) t
WHERE rnk <= 3;
```

OR

```sql
WITH ranked AS (
    SELECT
        d.year,
        p.product_name,
        SUM(f.sales_amount) AS total_sales,
        RANK() OVER (PARTITION BY d.year 
                     ORDER BY SUM(f.sales_amount) DESC) 
         AS rnk
    FROM fact_sales f
    JOIN dim_date d ON f.date_key = d.date_key
    JOIN dim_product p ON f.product_key = p.product_key
    GROUP BY d.year, p.product_name
) 
SELECT *
FROM ranked
WHERE rnk <= 3;
```

------------------------------------------------------------------------

## Exercise 6 --- Running Total

### CONCEPT: [Running Total Example](./running_total_example.md)

### Task: Compute cumulative sales by year.

``` sql
SELECT
    d.year,
    SUM(f.sales_amount) AS yearly_sales,
    SUM(SUM(f.sales_amount)) OVER (ORDER BY d.year) 
       AS running_total
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year;
```

------------------------------------------------------------------------

## Exercise 7 --- Percent Contribution

### Task

Find percentage contribution of each category to total revenue.

``` sql
SELECT
    p.category,
    SUM(f.sales_amount) AS total_sales,
    SUM(f.sales_amount) / SUM(SUM(f.sales_amount)) OVER () AS pct_total
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.category;
```

------------------------------------------------------------------------

## Exercise 8 --- Pivot Analysis

### Task

Pivot sales by channel per year.

``` sql
SELECT
    d.year,
    SUM(CASE WHEN ch.channel_name = 'Online' 
        THEN f.sales_amount END) 
      AS online_sales,
    SUM(CASE WHEN ch.channel_name = 'In-Store' 
        THEN f.sales_amount END) AS store_sales
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_channel ch ON f.channel_key = ch.channel_key
GROUP BY d.year;
```

------------------------------------------------------------------------

## Exercise 9 --- Multi-Level Drill-Down with Window Function

### Task

Within each state, rank stores by revenue and return top 2.

``` sql
SELECT *
FROM (
    SELECT
        c.state,
        s.store_name,
        SUM(f.sales_amount) AS total_sales,
        RANK() OVER (PARTITION BY c.state 
                     ORDER BY SUM(f.sales_amount) DESC) AS rnk
    FROM fact_sales f
    JOIN dim_customer c ON f.customer_key = c.customer_key
    JOIN dim_store s ON f.store_key = s.store_key
    GROUP BY c.state, s.store_name
) t
WHERE rnk <= 2;
```

OR

```sql
WITH ranked AS (
    SELECT
        c.state,
        s.store_name,
        SUM(f.sales_amount) AS total_sales,
        RANK() OVER (PARTITION BY c.state 
                     ORDER BY SUM(f.sales_amount) DESC) AS rnk
    FROM fact_sales f
    JOIN dim_customer c ON f.customer_key = c.customer_key
    JOIN dim_store s ON f.store_key = s.store_key
    GROUP BY c.state, s.store_name
) 
SELECT *
FROM ranked
WHERE rnk <= 2;
```


------------------------------------------------------------------------

## Exercise 10 --- Time Intelligence (Year-over-Year Growth)

### Task

Compute year-over-year growth percentage.

``` sql
SELECT
    year,
    yearly_sales,
    LAG(yearly_sales) OVER (ORDER BY year) AS prev_year,
    (yearly_sales - LAG(yearly_sales) OVER (ORDER BY year))
        / LAG(yearly_sales) OVER (ORDER BY year) AS yoy_growth
FROM (
    SELECT
        d.year,
        SUM(f.sales_amount) AS yearly_sales
    FROM fact_sales f
    JOIN dim_date d ON f.date_key = d.date_key
    GROUP BY d.year
) t;
```

OR

``` sql


WITH yearly_sales_table (
    SELECT
        d.year,
        SUM(f.sales_amount) AS yearly_sales
    FROM fact_sales f
    JOIN dim_date d ON f.date_key = d.date_key
    GROUP BY d.year
) 
SELECT
    year,
    yearly_sales,
    LAG(yearly_sales) OVER (ORDER BY year) AS prev_year,
    (yearly_sales - LAG(yearly_sales) OVER (ORDER BY year))
        / LAG(yearly_sales) OVER (ORDER BY year) AS yoy_growth
FROM yearly_sales_table;
```
