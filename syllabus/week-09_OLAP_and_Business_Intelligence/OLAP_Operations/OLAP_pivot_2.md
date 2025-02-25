can you provide a star schema in mysql with sample records for all tables and then provide 4 examples (simple to complex) of a "pivot" operation in sql

Absolutely! Let's start by creating a star schema in MySQL with sample records for all tables. I'll use a simple e-commerce example.

### Star Schema Example

**Fact Table:** `sales`
- `sale_id` (Primary Key)
- `date_id` (Foreign Key to `dim_date`)
- `product_id` (Foreign Key to `dim_product`)
- `customer_id` (Foreign Key to `dim_customer`)
- `quantity`
- `sales_amount`

**Dimension Tables:**

**1. `dim_date`**
- `date_id` (Primary Key)
- `date`
- `month`
- `year`

**2. `dim_product`**
- `product_id` (Primary Key)
- `product_name`
- `category`

**3. `dim_customer`**
- `customer_id` (Primary Key)
- `customer_name`
- `customer_location`

### Creating Tables in MySQL with Sample Records

```sql
-- Create dimension tables
CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    date DATE,
    month VARCHAR(20),
    year INT
);

CREATE TABLE dim_product (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(100)
);

CREATE TABLE dim_customer (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_location VARCHAR(100)
);

-- Create fact table
CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    date_id INT,
    product_id INT,
    customer_id INT,
    quantity INT,
    sales_amount DECIMAL(10, 2),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id)
);

-- Insert sample records into dimension tables
INSERT INTO dim_date (date_id, date, month, year) VALUES
(1, '2025-01-01', 'January', 2025),
(2, '2025-02-01', 'February', 2025);

INSERT INTO dim_product (product_id, product_name, category) VALUES
(1, 'Laptop', 'Electronics'),
(2, 'Chair', 'Furniture');

INSERT INTO dim_customer (customer_id, customer_name, customer_location) VALUES
(1, 'Alice', 'New York'),
(2, 'Bob', 'Los Angeles');

-- Insert sample records into fact table
INSERT INTO sales (sale_id, date_id, product_id, customer_id, quantity, sales_amount) VALUES
(1, 1, 1, 1, 2, 2000.00),
(2, 2, 2, 2, 1, 150.00);
```

### Pivot Table Examples in SQL

#### 1. Simple Pivot Table: Aggregate Sales Amount by Month
```sql
SELECT
    month,
    SUM(sales_amount) AS total_sales_amount
FROM sales
JOIN dim_date ON sales.date_id = dim_date.date_id
GROUP BY month;
```

#### 2. Pivot Table: Sales Amount by Product and Month
```sql
SELECT
    product_name,
    SUM(CASE WHEN month = 'January' THEN sales_amount ELSE 0 END) AS January_Sales,
    SUM(CASE WHEN month = 'February' THEN sales_amount ELSE 0 END) AS February_Sales
FROM sales
JOIN dim_date ON sales.date_id = dim_date.date_id
JOIN dim_product ON sales.product_id = dim_product.product_id
GROUP BY product_name;
```

#### 3. Pivot Table: Sales Amount by Customer and Product
```sql
SELECT
    customer_name,
    SUM(CASE WHEN product_name = 'Laptop' THEN sales_amount ELSE 0 END) AS Laptop_Sales,
    SUM(CASE WHEN product_name = 'Chair' THEN sales_amount ELSE 0 END) AS Chair_Sales
FROM sales
JOIN dim_product ON sales.product_id = dim_product.product_id
JOIN dim_customer ON sales.customer_id = dim_customer.customer_id
GROUP BY customer_name;
```

#### 4. Complex Pivot Table: Quantity Sold by Product and Month
```sql
SELECT
    product_name,
    SUM(CASE WHEN month = 'January' THEN quantity ELSE 0 END) AS January_Quantity,
    SUM(CASE WHEN month = 'February' THEN quantity ELSE 0 END) AS February_Quantity
FROM sales
JOIN dim_date ON sales.date_id = dim_date.date_id
JOIN dim_product ON sales.product_id = dim_product.product_id
GROUP BY product_name;
```

I hope this helps! Let me know if you have any questions or if there's anything else you'd like to explore.
