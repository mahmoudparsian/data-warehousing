# Star Schema

#### Fact Table: `fact_sales`
- `sale_id` (PK)
- `customer_id` (FK)
- `product_id` (FK)
- `store_id` (FK)
- `date_key` (FK)
- `quantity`
- `amount`

#### Dimension Tables:
1. `dim_customers`
   - `customer_id` (PK)
   - `customer_name`
   - `customer_email`

2. `dim_products`
   - `product_id` (PK)
   - `product_name`
   - `product_category`

3. `dim_stores`
   - `store_id` (PK)
   - `store_name`
   - `store_location`

4. `dim_dates`
   - `date_key` (PK)
   - `date`
   - `year`
   - `month`
   - `day`
   - `quarter`
   - `week`

-------

# The `lag()` function in MySQL

		The `LAG()` function in MySQL is a window 
		function that provides access to a row at 
		a given physical offset before the current 
		row within the result set. 
		
		This function can be quite useful for tasks 
		like comparing a current row with a previous 
		one, computing differences over time, and more.
		
		The term "lag" is used because it retrieves 
		data that "lags behind" the current row, allowing 
		you to perform comparisons or calculations based 
		on previous rows.

Here's the basic syntax:

```sql
LAG(column_name, offset, default_value) 
   OVER (PARTITION BY partition_clause ORDER BY order_clause)
```
- `column_name`: The column from which you want to 
  retrieve the lagged value.
  
- `offset`: The number of rows behind the current row 
  from which to retrieve the value (default is 1).
  
- `default_value`: The value to return if the offset goes 
  out of the bounds of the partition (default is `NULL`).

## Concrete example:

Suppose we have a sales table that looks like this:

| sale_id | sale_date | sales_amount |
|---------|-----------|--------------|
| 1       | 2025-01-01| 1000         |
| 2       | 2025-01-02| 1500         |
| 3       | 2025-01-03| 1200         |
| 4       | 2025-01-04| 1300         |
| 5       | 2025-01-05| 1100         |

We want to compare the `sales_amount` of each day with the previous day.

Here’s how we’d use the `LAG()` function to do this:

```sql
SELECT 
    sale_id, 
    sale_date, 
    sales_amount, 
    LAG(sales_amount, 1) 
      OVER (ORDER BY sale_date) AS prev_day_sales
FROM 
    sales;
```

The result set will be:

~~~text
| sale_id | sale_date | sales_amount | prev_day_sales |
|---------|-----------|--------------|----------------|
| 1       | 2025-01-01| 1000         | NULL           |
| 2       | 2025-01-02| 1500         | 1000           |
| 3       | 2025-01-03| 1200         | 1500           |
| 4       | 2025-01-04| 1300         | 1200           |
| 5       | 2025-01-05| 1100         | 1300           |
~~~


In this example, the `LAG()` function is used to retrieve the `sales_amount` from the previous day, so you can see the `prev_day_sales` column shows the sales amount for the day before.



-------

#  OLAP SQL Queries

------

### Query 1: Total Sales by Product
```sql
SELECT p.product_name, 
       SUM(f.quantity) AS total_quantity, 
       SUM(f.amount) AS total_amount
FROM 
    fact_sales f
JOIN 
    dim_products p ON f.product_id = p.product_id
GROUP BY 
    p.product_name;
```

-----

### Query 2: Sales by Month

```sql
SELECT d.year, 
       d.month, 
       SUM(f.amount) AS total_amount
FROM 
    fact_sales f
JOIN 
    dim_dates d ON f.date_key = d.date_key
GROUP BY 
    d.year, d.month;
```

-----

### Query 3: Top 5 Customers by Sales Amount

```sql
SELECT c.customer_name, 
       SUM(f.amount) AS total_amount
FROM 
    fact_sales f
JOIN 
    dim_customers c ON f.customer_id = c.customer_id
GROUP BY 
    c.customer_name
ORDER BY 
    total_amount DESC
LIMIT 
    5;
```

------

### Query 4: Sales Distribution by Store Location

```sql
SELECT s.store_location, 
       SUM(f.amount) AS total_amount
FROM 
    fact_sales f
JOIN 
    dim_stores s ON f.store_id = s.store_id
GROUP BY 
    s.store_location;
```

------

### Query 5: Average Sales per Day

```sql
SELECT d.date, 
       AVG(f.amount) AS avg_amount
FROM 
    fact_sales f
JOIN 
    dim_dates d ON f.date_key = d.date_key
GROUP BY 
    d.date;
```

------

### Query 6: Monthly Sales Growth Rate

```sql
SELECT d.year, 
       d.month, 
       SUM(f.amount) AS total_amount,
       LAG(SUM(f.amount)) 
         OVER (ORDER BY d.year, d.month) AS prev_month_amount,
       
       (SUM(f.amount) - LAG(SUM(f.amount)) 
         OVER (ORDER BY d.year, d.month)) / 
         LAG(SUM(f.amount)) OVER (ORDER BY d.year, d.month) * 100 
           AS growth_rate
FROM 
    fact_sales f
JOIN 
    dim_dates d ON f.date_key = d.date_key
GROUP BY 
    d.year, d.month;
```

------

### Query 7: Sales Rank by Customer

```sql
SELECT c.customer_name, 
       SUM(f.amount) AS total_amount,
       RANK() OVER (ORDER BY SUM(f.amount) DESC) AS sales_rank
FROM 
    fact_sales f
JOIN 
    dim_customers c ON f.customer_id = c.customer_id
GROUP BY 
    c.customer_name;
   
```


### Query 7.1: Sales Rank by Customer ONLY Top-3

```sql
WITH ranked_data AS
(
  SELECT c.customer_name, 
         SUM(f.amount) AS total_amount,
         RANK() OVER (ORDER BY SUM(f.amount) DESC) AS sales_rank
  FROM 
      fact_sales f
  JOIN 
      dim_customers c ON f.customer_id = c.customer_id
  GROUP BY 
      c.customer_name
)
SELECT customer_name, 
       total_amount,
       sales_rank
FROM 
      ranked_data 
WHERE 
      sales_rank <= 3;
```

------

### Query 8: Total Sales by Product Category

```sql
SELECT p.product_category, 
       SUM(f.amount) AS total_amount
FROM 
    fact_sales f
JOIN 
    dim_products p ON f.product_id = p.product_id
GROUP BY 
    p.product_category;
```

------

### Query 9: Sales Amount for Specific Date Range

```sql
SELECT d.date,
       SUM(f.amount) AS total_amount
FROM 
    fact_sales f
JOIN 
    dim_dates d ON f.date_key = d.date_key
WHERE 
    d.date BETWEEN '2025-01-01' AND '2025-12-31'
GROUP BY 
    d.date;
```

-------

### Query 10: Customers with Multiple Purchases

#### Solution with HAVING clause

```sql
SELECT  c.customer_name, 
        COUNT(f.sale_id) AS purchase_count
FROM 
    fact_sales f
JOIN 
    dim_customers c ON f.customer_id = c.customer_id
GROUP BY 
    c.customer_name
HAVING 
    COUNT(f.sale_id) > 1;
```

#### Solution without HAVING clause

```sql
WITH grouped_data AS
(
  SELECT  c.customer_name, 
          COUNT(f.sale_id) AS purchase_count
  FROM 
      fact_sales f
  JOIN 
      dim_customers c ON f.customer_id = c.customer_id
  GROUP BY 
    c.customer_name
)
SELECT  customer_name, 
        purchase_count
FROM 
      grouped_data 
WHERE  
    purchase_count > 1;
```



------

### Query 11. Total Sales per Customer in Each Store

```sql
SELECT 
    c.customer_name,
    s.store_name,
    SUM(f.amount) AS total_sales
FROM 
    fact_sales f
JOIN 
    dim_customers c ON f.customer_id = c.customer_id
JOIN 
    dim_stores s ON f.store_id = s.store_id
GROUP BY 
    c.customer_name, s.store_name;
```

------

### Query 12. Top 3 Selling Products by Amount in Each Category
```sql
SELECT 
    p.product_category,
    p.product_name,
    SUM(f.amount) AS total_sales,
    RANK() OVER (PARTITION BY p.product_category ORDER BY SUM(f.amount) DESC) as rank
FROM 
    fact_sales f
JOIN 
    dim_products p ON f.product_id = p.product_id
GROUP BY 
    p.product_category, p.product_name
HAVING 
    RANK() <= 3;
```

-------

### Query 13. Monthly Sales Trend for Each Store
```sql
SELECT 
    s.store_name,
    d.year,
    d.month,
    SUM(f.amount) AS total_sales
FROM 
    fact_sales f
JOIN 
    dim_stores s ON f.store_id = s.store_id
JOIN 
    dim_dates d ON f.date_key = d.date_key
GROUP BY 
    s.store_name, d.year, d.month
ORDER BY 
    s.store_name, d.year, d.month;
```

------

### Query 14. Customer with Highest Spending in Each Store
```sql
SELECT 
    s.store_name,
    c.customer_name,
    SUM(f.amount) AS total_spending
FROM 
    fact_sales f
JOIN 
    dim_customers c ON f.customer_id = c.customer_id
JOIN 
    dim_stores s ON f.store_id = s.store_id
GROUP BY 
    s.store_name, c.customer_name
ORDER BY 
    s.store_name, total_spending DESC;
```

-------

### Query 15. Average Sales Amount per Day in Each Month
```sql
SELECT 
    d.year,
    d.month,
    d.day,
    AVG(f.amount) AS avg_sales
FROM 
    fact_sales f
JOIN 
    dim_dates d ON f.date_key = d.date_key
GROUP BY 
    d.year, d.month, d.day
ORDER BY 
    d.year, d.month, d.day;
```

------

### Query 16. Total Quantity Sold of Each Product in Each Store
```sql
SELECT 
    p.product_name,
    s.store_name,
    SUM(f.quantity) AS total_quantity
FROM 
    fact_sales f
JOIN 
    dim_products p ON f.product_id = p.product_id
JOIN 
    dim_stores s ON f.store_id = s.store_id
GROUP BY 
    p.product_name, s.store_name;
```

------

### Query 17. Year-over-Year Sales Growth for Each Store
```sql
SELECT 
    s.store_name,
    d.year,
    SUM(f.amount) AS total_sales,
    LAG(SUM(f.amount)) 
      OVER (PARTITION BY s.store_name ORDER BY d.year) 
      AS prev_year_sales,
    ((SUM(f.amount) - LAG(SUM(f.amount)) 
      OVER (PARTITION BY s.store_name ORDER BY d.year)) / 
      LAG(SUM(f.amount)) OVER (PARTITION BY s.store_name ORDER BY d.year)) * 100 
      AS sales_growth
FROM 
    fact_sales f
JOIN 
    dim_stores s ON f.store_id = s.store_id
JOIN 
    dim_dates d ON f.date_key = d.date_key
GROUP BY 
    s.store_name, d.year;
```

------

### Query 18. Total Sales by Product Category and Customer
```sql
SELECT 
    p.product_category,
    c.customer_name,
    SUM(f.amount) AS total_sales
FROM 
    fact_sales f
JOIN 
    dim_products p ON f.product_id = p.product_id
JOIN 
    dim_customers c ON f.customer_id = c.customer_id
GROUP BY 
    p.product_category, c.customer_name
ORDER BY 
    p.product_category, total_sales DESC;
```

------

### Query 19. Top 5 Customers by Sales Amount in Each Month

#### Solution using HAVING clause

```sql
SELECT 
    d.year,
    d.month,
    c.customer_name,
    SUM(f.amount) AS total_sales,
    RANK() OVER (PARTITION BY d.year, d.month ORDER BY SUM(f.amount) DESC) as rank
FROM 
    fact_sales f
JOIN 
    dim_dates d ON f.date_key = d.date_key
JOIN 
    dim_customers c ON f.customer_id = c.customer_id
GROUP BY 
    d.year, d.month, c.customer_name
HAVING 
    RANK() <= 5;
```

#### Solution without using HAVING clause

```sql
WITH ranked_data AS 
(
  SELECT 
     d.year,
     d.month,
     c.customer_name,
    SUM(f.amount) AS total_sales,
     RANK() OVER (PARTITION BY d.year, d.month ORDER BY SUM(f.amount) DESC) as rnk
  FROM 
      fact_sales f
  JOIN 
      dim_dates d ON f.date_key = d.date_key
  JOIN 
      dim_customers c ON f.customer_id = c.customer_id
  GROUP BY 
      d.year, d.month, c.customer_name
)
SELECT 
     year,
     month,
     customer_name,
     total_sales,
     rnk
FROM 
      ranked_data 
WHERE 
    rnk <= 5;
```



-----

### Query 20. Weekly Sales Distribution for Each Product Category

```sql
SELECT 
    p.product_category,
    d.year,
    d.week,
    SUM(f.amount) AS total_sales
FROM 
    fact_sales f
JOIN 
    dim_products p ON f.product_id = p.product_id
JOIN 
    dim_dates d ON f.date_key = d.date_key
GROUP BY 
    p.product_category, d.year, DATEPART(WEEK, d.date)
ORDER BY 
    p.product_category, d.year, d.week;
```


