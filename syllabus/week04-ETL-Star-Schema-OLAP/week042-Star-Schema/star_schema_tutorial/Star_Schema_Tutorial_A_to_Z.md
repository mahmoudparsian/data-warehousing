# 📘 Comprehensive Tutorial: Star Schema (A--Z Guide)


------------------------------------------------------------------------

# 1️⃣ Introduction to Data Warehousing

## What is a Data Warehouse?

A **Data Warehouse (DW)** 

		is  a  centralized  repository 
		designed  to store  integrated, 
		historical, and analytical data 
		from multiple operational systems.

**Characteristics:**

- Subject-oriented 
- Integrated 
- Time-variant 
- Non-volatile

Unlike OLTP systems, a data warehouse is optimized for **analysis**, not transactions.

------------------------------------------------------------------------

# 2️⃣ What is a Star Schema?

A **Star Schema** is the most common dimensional modeling technique used
in data warehousing.

It consists of:

-   ⭐ One central **Fact Table**
-   🌟 Multiple surrounding **Dimension Tables**

It looks like a star --- hence the name.

------------------------------------------------------------------------

# 3️⃣ Core Components

## 3.1 Fact Table

A Fact Table contains:

-   Numeric measurable values (metrics)
-   Foreign keys to dimensions
-   Very large number of rows

Example measures: 

- `sales_amount`
- `quantity`
- `discount`
- `profit``

Example:

``` sql
CREATE TABLE fact_sales (
    sale_id BIGINT PRIMARY KEY,
    date_id INT,
    customer_id INT,
    product_id INT,
    store_id INT,
    quantity INT,
    sales_amount DECIMAL(10,2)
);
```

------------------------------------------------------------------------

## 3.2 Dimension Tables

Dimension tables describe the facts.

They contain: 

- Attributes for filtering 
- Textual descriptive information 
- Relatively small number of rows

Example:

``` sql
CREATE TABLE dim_product (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    brand VARCHAR(50)
);
```

------------------------------------------------------------------------

# 4️⃣ Why Star Schema is Important

Benefits:

-   Simple structure
-   Easy for business users
-   High performance for OLAP
-   Efficient aggregations
-   Compatible with BI tools
-   Clear separation of metrics and attributes

------------------------------------------------------------------------

# 5️⃣ OLTP vs Star Schema

```
OLTP                         Star Schema
---------------------------- -------------------------
Highly normalized            Denormalized
Optimized for transactions   Optimized for analytics
Many joins                   Few joins
Current data                 Historical data
```
------------------------------------------------------------------------

# 6️⃣ Concrete Example: E-Commerce OLTP

## OLTP Tables

### Customers

``` sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    country VARCHAR(50)
);
```

### Products

``` sql
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2)
);
```

### Orders

``` sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE
);
```

### Order Items

``` sql
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2)
);
```

------------------------------------------------------------------------

# 7️⃣ Designing the Star Schema

## Step 1: Define Grain

Grain = one row per product per order.

## Step 2: Identify Fact Table

Fact: sales transaction

Measures: - quantity - sales_amount

## Step 3: Identify Dimensions

-   dim_customer
-   dim_product
-   dim_date

------------------------------------------------------------------------

# 8️⃣ Star Schema Implementation

## 8.1 Date Dimension

``` sql
CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    full_date DATE,
    year INT,
    quarter INT,
    month INT,
    day INT
);
```

## 8.2 Customer Dimension

``` sql
CREATE TABLE dim_customer (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    country VARCHAR(50)
);
```

## 8.3 Product Dimension

``` sql
CREATE TABLE dim_product (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50)
);
```

## 8.4 Fact Table

``` sql
CREATE TABLE fact_sales (
    sales_id BIGINT PRIMARY KEY,
    date_id INT,
    customer_id INT,
    product_id INT,
    quantity INT,
    sales_amount DECIMAL(10,2)
);
```

------------------------------------------------------------------------

# 9️⃣ ETL: From OLTP to Star Schema

## Step 1: Load Dimensions

``` sql
INSERT INTO dim_customer
SELECT customer_id, name, country
FROM customers;
```

## Step 2: Load Fact Table

``` sql
INSERT INTO fact_sales (
  sales_id, 
  date_id, 
  customer_id, 
  product_id, 
  quantity, 
  sales_amount
)
SELECT 
    oi.order_item_id,
    DATE_FORMAT(o.order_date, '%Y%m%d'),
    o.customer_id,
    oi.product_id,
    oi.quantity,
    oi.quantity * oi.unit_price
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id;
```

------------------------------------------------------------------------

# 🔟 OLAP Queries

## Total Sales by Year

``` sql
SELECT d.year, 
       SUM(f.sales_amount)
FROM fact_sales f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year;
```

## Top 5 Products

``` sql
SELECT p.product_name, 
       SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_sales DESC
LIMIT 5;
```

------------------------------------------------------------------------

# 1️⃣1️⃣ Advanced Concepts

-   Slowly Changing Dimensions (SCD Type 1, 2, 3)
-   Degenerate Dimensions
-   Conformed Dimensions
-   Factless Fact Tables
-   Surrogate Keys
-   Role-playing Dimensions

------------------------------------------------------------------------

# 1️⃣2️⃣ When to Use Star Schema

Use Star Schema when:

-   Building BI systems
-   Creating dashboards
-   Supporting aggregation-heavy workloads
-   Designing enterprise DW

Avoid when:

-   Highly transactional workloads
-   Real-time write-intensive systems

------------------------------------------------------------------------

# 1️⃣3️⃣ Summary

Star Schema:

-   Simplifies analytics
-   Improves performance
-   Separates metrics from descriptive data
-   Is the foundation of dimensional modeling

------------------------------------------------------------------------

# 🎯 Final Takeaway

**If OLTP answers:**

"What happened to this specific order?"

**Star Schema answers:**

"How are sales trending across regions, time, and product categories?"

That is the power of dimensional modeling.

------------------------------------------------------------------------

End of Tutorial
