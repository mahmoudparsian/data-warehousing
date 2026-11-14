# The Importance of Denormalization in Data Warehousing

## 1. Introduction

* In transactional systems (OLTP), normalization is preferred to reduce
redundancy and maintain data integrity. 

* However, in Data Warehousing
(OLAP) environments, **denormalization is often preferred** to improve
query performance and simplify analytics.

This document explains:

-   Why denormalization improves performance
-   How it reduces query complexity
-   When it is preferred in data warehousing
-   Practical SQL examples
-   Performance comparison reasoning

------------------------------------------------------------------------

## 2. Normalization vs Denormalization

### Normalization (OLTP Style)

-   Many small tables
-   Foreign keys and multiple joins
-   Optimized for INSERT / UPDATE / DELETE
-   Minimizes redundancy

### Denormalization (OLAP Style)

-   Fewer, wider tables
-   Reduced joins
-   Optimized for SELECT queries
-   Improves aggregation speed

------------------------------------------------------------------------

## 3. Example Scenario: Retail Sales

### Normalized Design (OLTP)

Tables:

-   `customers(customer_id, name, city_id)`
-   `cities(city_id, city_name, state_id)`
-   `states(state_id, state_name)`
-   `products(product_id, product_name, category_id)`
-   `categories(category_id, category_name)`
-   `sales(sale_id, customer_id, product_id, sale_date, amount)`

### Query: Total Sales by State and Product Category

``` sql
SELECT st.state_name,
       c.category_name,
       SUM(s.amount) AS total_sales
FROM sales s
JOIN customers cu ON s.customer_id = cu.customer_id
JOIN cities ci ON cu.city_id = ci.city_id
JOIN states st ON ci.state_id = st.state_id
JOIN products p ON s.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
GROUP BY st.state_name, c.category_name;
```

Problems: 

- 5 JOIN operations 
- Expensive shuffle in distributed systems 
- Complex execution plan 
- Slower performance on billions of rows

------------------------------------------------------------------------

## 4. Denormalized Star Schema (Data Warehouse)

### Dimension Tables

-   `dim_customer(customer_key, name, city, state)`
-   `dim_product(product_key, product_name, category)`

### Fact Table

-   `fact_sales(sale_key, customer_key, product_key, sale_date, amount)`

Now the query becomes:

``` sql
SELECT dc.state,
       dp.category,
       SUM(fs.amount) AS total_sales
FROM fact_sales fs
JOIN dim_customer dc ON fs.customer_key = dc.customer_key
JOIN dim_product dp ON fs.product_key = dp.product_key
GROUP BY dc.state, dp.category;
```

Benefits: 

- Only 2 joins instead of 5 
- No hierarchical join chain 
- Better indexing 
- Better partition pruning 
- Simpler execution plan

------------------------------------------------------------------------

## 5. Why Denormalization Improves Performance

### 1. Fewer Joins

Joins are expensive in large-scale systems (Spark, Snowflake, BigQuery).
Reducing joins reduces:

-   Network shuffling
-   CPU overhead
-   Disk I/O

------------------------------------------------------------------------

### 2. Faster Aggregations

Fact tables are optimized for aggregation:

-   Columnar storage (Parquet, ORC)
-   Compression
-   Partitioning by date
-   Predicate pushdown

Example:

``` sql
SELECT sale_date, SUM(amount)
FROM fact_sales
WHERE sale_date BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY sale_date;
```

This scans only required partitions.

------------------------------------------------------------------------

### 3. Simpler Query Logic

Business users and BI tools prefer:

-   Fewer joins
-   Clear relationships
-   Predictable schema

Denormalization enables: 

- Power BI 
- Tableau 
- Looker 
- Direct SQL dashboards

------------------------------------------------------------------------

### 4. Better Star Join Optimization

Modern query engines optimize star schemas:

-   Broadcast dimension tables
-   Push filters early
-   Efficient hash joins

Small dimension tables are easily cached in memory.

------------------------------------------------------------------------

## 6. Real Performance Consideration

Assume:

-   2 billion rows in fact_sales
-   10 million rows in customers
-   500 thousand rows in products

Normalized system: 

- Multiple chained joins 
- More shuffle 
- More intermediate data


Denormalized star schema: 

- Small dimensions 
- Optimized joins 
- Reduced execution time

In distributed systems (Apache Spark): 
Reducing 5 joins to 2 joins can reduce
execution time dramatically.

------------------------------------------------------------------------

## 7. Trade-Offs of Denormalization

Denormalization increases:

-   Data redundancy
-   Storage usage
-   ETL complexity

However, 

* Storage is cheap. 
* Query performance is expensive.

In analytics workloads: READ performance \>\> WRITE performance

------------------------------------------------------------------------

## 8. When Denormalization Is Preferred

Denormalization is ideal when:

-   Data is mostly read-only
-   Queries involve heavy aggregation
-   BI dashboards require fast response
-   Data volume is large (millions/billions of rows)

------------------------------------------------------------------------

## 9. Summary


| Feature      | Normalized (OLTP)    | Denormalized (OLAP) |
|--------------|----------------------|---------------------|
| Joins        | Many                 | Few                 |
| Redundancy   | Low                  | Higher              |
| Query Speed  | Slower for analytics | Faster              |
| Insert Speed | Fast                 | Slower              |
| Use Case     | Transactions         | Analytics           |


Denormalization is preferred in data warehousing because:

-   It reduces join complexity
-   It improves aggregation performance
-   It enables star schema optimization
-   It scales better for analytical workloads

------------------------------------------------------------------------

## Final Takeaway

* Normalization is best for transactional integrity. 
* Denormalization is best for analytical performance.

Data Warehousing prioritizes fast queries over minimal redundancy ---
which is why denormalization is the standard design principle.
