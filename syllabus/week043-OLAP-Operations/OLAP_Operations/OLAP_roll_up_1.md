# OLAP ROLL UP

	Provide a star schema in mysql with sample 
	records for all tables and then provide 5 
	examples (simple to complex) of a "roll up" 
	opertion in sql

### **ROLLUP in MySQL – Complete Example with Sample Data and Output**

#### **1. What is ROLLUP in SQL?**
- `ROLLUP` is a SQL extension used in `GROUP BY` to **generate subtotals and grand totals** in a query result.
- It provides hierarchical aggregation **from the most detailed level to higher summary levels**.
- The `ROLLUP` operator is useful in **OLAP (Online Analytical Processing)** and **data analysis**.

---

### **2. Create Sample Data in MySQL**

#### **Creating a Sales Table**
```sql
CREATE TABLE sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    year INT,
    quarter VARCHAR(2),
    region VARCHAR(50),
    sales_amount DECIMAL(10,2)
);
```

#### **Inserting Sample Records**
```sql
INSERT INTO sales (year, quarter, region, sales_amount) 
VALUES
(2023, 'Q1', 'North', 5000.00),
(2023, 'Q1', 'South', 7000.00),
(2023, 'Q2', 'North', 6000.00),
(2023, 'Q2', 'South', 8000.00),
(2024, 'Q1', 'North', 5500.00),
(2024, 'Q1', 'South', 7500.00),
(2024, 'Q2', 'North', 6200.00),
(2024, 'Q2', 'South', 8200.00);
```

---

### **3. Using `ROLLUP` to Generate Subtotals and Grand Total**

```sql
SELECT 
    year, 
    quarter, 
    region, 
    SUM(sales_amount) AS total_sales
FROM 
    sales
GROUP BY 
    year, quarter, region WITH ROLLUP;
```

---

### **4. Expected Output**

~~~text
| year | quarter | region | total_sales|
|------|---------|--------|------------|
| 2023 | Q1      | North  | 5000.00    |
| 2023 | Q1      | South  | 7000.00    |
| 2023 | Q1      | NULL   | 12000.00   |  ⬅ **Subtotal (Q1 2023)**
| 2023 | Q2      | North  | 6000.00    |
| 2023 | Q2      | South  | 8000.00    |
| 2023 | Q2      | NULL   | 14000.00   |  ⬅ **Subtotal (Q2 2023)**
| 2023 | NULL    | NULL   | 26000.00   |  ⬅ **Total for 2023**
| 2024 | Q1      | North  | 5500.00    |
| 2024 | Q1      | South  | 7500.00    |
| 2024 | Q1      | NULL   | 13000.00   |  ⬅ **Subtotal (Q1 2024)**
| 2024 | Q2      | North  | 6200.00    |
| 2024 | Q2      | South  | 8200.00    |
| 2024 | Q2      | NULL   | 14400.00   |  ⬅ **Subtotal (Q2 2024)**
| 2024 | NULL    | NULL   | 27400.00   |  ⬅ **Total for 2024**
| NULL | NULL    | NULL   | 53400.00   |  ⬅ **Grand Total for all years**
~~~


### **5. Explanation of Output**
1. **Detailed Data**: Individual rows show sales by year, quarter, and region.
2. **Subtotal per Quarter**: When `region` is `NULL`, it represents the total for that quarter.
3. **Subtotal per Year**: When both `quarter` and `region` are `NULL`, it shows total sales per year.
4. **Grand Total**: When `year`, `quarter`, and `region` are all `NULL`, it shows the total sales across all years.

---

### **6. Modifying `ROLLUP` for Different Levels**
#### **Example: ROLLUP on `year` and `quarter` (without `region`)**
```sql
SELECT 
    year, 
    quarter, 
    SUM(sales_amount) AS total_sales
FROM 
    sales
GROUP BY 
    year, quarter WITH ROLLUP;
```

#### **Modified Output**

~~~
| year | quarter | total_sales|
|------|---------|------------|
| 2023 | Q1      | 12000.00   |
| 2023 | Q2      | 14000.00   |
| 2023 | NULL    | 26000.00   |  ⬅ **Total for 2023**  
| 2024 | Q1      | 13000.00   |
| 2024 | Q2      | 14400.00   |
| 2024 | NULL    | 27400.00   |  ⬅ **Total for 2024**  
| NULL | NULL    | 53400.00   |  ⬅ **Grand Total**  
~~~

### **7. Conclusion**
✅ `ROLLUP` helps create hierarchical summaries in OLAP analysis.  
✅ It automatically **generates subtotals and grand totals** for aggregated data.  
✅ It simplifies reporting without requiring multiple queries or UNION operations.  

------


# Another Example: Story...

	Let's start with creating a star schema in 
	MySQL. In a star schema, we typically have 
	a central fact table connected to several 
	dimension tables. Here's an example for a 
	simple sales database:

# 1. Creating the Tables

## Fact Table: sales_fact

~~~sql
CREATE TABLE sales_fact (
    sales_id INT PRIMARY KEY,
    date_id INT,
    customer_id INT,
    product_id INT,
    store_id INT,
    sales_amount DECIMAL(10, 2),
    units_sold INT
);
~~~

## Dimension Tables:

### date_dim

~~~sql
CREATE TABLE date_dim (
    date_id INT PRIMARY KEY,
    date DATE,
    year INT,
    quarter INT,
    month INT,
    day INT
);
~~~

### customer_dim

~~~sql
CREATE TABLE customer_dim (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_address VARCHAR(255)
);
~~~

### product_dim

~~~sql
CREATE TABLE product_dim (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    product_category VARCHAR(100)
);
~~~

### store_dim

~~~sql
CREATE TABLE store_dim (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(100),
    store_location VARCHAR(100)
);
~~~

# 2. Inserting Sample Records

Let's insert some sample data into these tables:

* Date Dimension

~~~sql
INSERT INTO date_dim (date_id, date, year, quarter, month, day)
VALUES 
(1, '2025-01-01', 2025, 1, 1, 1), 
(2, '2025-02-01', 2025, 1, 2, 1);
~~~

* Customer Dimension

~~~sql
INSERT INTO customer_dim (customer_id, customer_name, customer_address)
VALUES 
(1, 'John Doe', '123 Elm Street'), 
(2, 'Jane Smith', '456 Oak Avenue');
~~~

* Product Dimension

~~~sql
INSERT INTO product_dim (product_id, product_name, product_category)
VALUES 
(1, 'Product A', 'Category 1'), 
(2, 'Product B', 'Category 2');
~~~

* Store Dimension

~~~sql
INSERT INTO store_dim (store_id, store_name, store_location)
VALUES 
(1, 'Store X', 'Location 1'), 
(2, 'Store Y', 'Location 2');
~~~

* Sales Fact

~~~sql
INSERT INTO sales_fact 
(sales_id, date_id, customer_id, product_id, store_id, sales_amount, units_sold)
VALUES
(1, 1, 1, 1, 1, 100.00, 10),
(2, 2, 2, 2, 2, 200.00, 20);
~~~

# 3. Examples of "ROLL UP" Operation in SQL

### Example 2: Simple Roll-Up on a Single Dimension
	
	This will provide the total sales 
	per product category and the grand 
	total for all product categories.

~~~sql
SELECT product_category, 
       SUM(sales_amount) AS total_sales
FROM 
     sales_fact
JOIN 
     product_dim ON sales_fact.product_id = product_dim.product_id
GROUP BY 
     ROLLUP (product_category);
~~~



### Example 3: Roll-Up on Multiple Dimensions

	This will provide the total sales 
	per product category and store location, 
	including subtotals and the grand total.
	
~~~sql
SELECT product_category, 
       store_location, 
       SUM(sales_amount) AS total_sales
FROM 
    sales_fact
JOIN 
    product_dim ON sales_fact.product_id = product_dim.product_id
JOIN 
    store_dim ON sales_fact.store_id = store_dim.store_id
GROUP BY ROLLUP 
    (product_category, store_location);
~~~