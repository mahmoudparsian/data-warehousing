# OLAP Pivot Operation

	Provide a star schema in mysql with 
	sample records for all tables and then 
	provide 4 examples (simple to complex) 
	of a "pivot" operation in sql

### **What is a Pivot Operation?**
- A **Pivot operation transforms row-based data into columns**.
- It allows you to **summarize and compare different values** efficiently.


![](./images/olap-pivot-2.png)

### **1. Star Schema in MySQL (Retail Sales Analysis System)**  

A **Star Schema** consists of a **central fact table** and **multiple dimension tables** to store structured sales data.

---

### **Fact Table: `sales_fact`**
Stores transactional sales data.

| sale_id | date_id | product_id | customer_id | store_id | sales_amount | quantity_sold |
|---------|---------|------------|-------------|----------|--------------|---------------|
| 1       | 1       | 1          | 1           | 1        | 500.00       | 5             |
| 2       | 2       | 2          | 2           | 1        | 300.00       | 3             |
| 3       | 3       | 3          | 3           | 2        | 700.00       | 7             |
| 4       | 4       | 1          | 4           | 2        | 900.00       | 9             |
| 5       | 5       | 2          | 5           | 3        | 250.00       | 2             |

---

### **Dimension Table: `date_dim`**
Stores date-related attributes.

| date_id | date       | year | quarter | month | day |
|---------|-----------|------|---------|-------|-----|
| 1       | 2024-01-01 | 2024 | Q1      | Jan   | 1   |
| 2       | 2024-02-01 | 2024 | Q1      | Feb   | 1   |
| 3       | 2024-03-01 | 2024 | Q1      | Mar   | 1   |
| 4       | 2024-04-01 | 2024 | Q2      | Apr   | 1   |
| 5       | 2024-05-01 | 2024 | Q2      | May   | 1   |

---

### **Dimension Table: `product_dim`**
Stores product-related attributes.

| product_id | product_name | category  | price  |
|------------|-------------|-----------|--------|
| 1          | Laptop      | Electronics | 100.00 |
| 2          | Phone       | Electronics | 50.00  |
| 3          | TV          | Electronics | 150.00 |

---

### **Dimension Table: `customer_dim`**
Stores customer-related attributes.

| customer_id | customer_name | region   |
|------------|--------------|---------|
| 1          | Alice        | North   |
| 2          | Bob          | South   |
| 3          | Charlie      | West    |
| 4          | David        | East    |
| 5          | Emily        | North   |

---

### **Dimension Table: `store_dim`**
Stores store-related attributes.

| store_id | store_name | location |
|----------|-----------|----------|
| 1        | Store A   | NY       |
| 2        | Store B   | CA       |
| 3        | Store C   | TX       |

---

## **2. Pivot Operations in SQL**
### **What is a Pivot Operation?**
- A **Pivot operation transforms row-based data into columns**.
- It allows you to **summarize and compare different values** efficiently.

---

### **Example 1: Pivot by Quarter (Sales per Quarter)**
```sql
SELECT 
    year,
    SUM(CASE WHEN quarter = 'Q1' THEN sales_amount ELSE 0 END) AS Q1_sales,
    SUM(CASE WHEN quarter = 'Q2' THEN sales_amount ELSE 0 END) AS Q2_sales
FROM sales_fact s
JOIN date_dim d ON s.date_id = d.date_id
GROUP BY year;
```
✅ **Explanation**:
- Transforms **quarterly sales into separate columns** (`Q1_sales`, `Q2_sales`).
- Groups by **year**.


| **Example** | **Pivot Condition** | **Query Purpose** |
|------------|---------------------|-------------------|
| **1** | `SUM(CASE WHEN quarter = 'Q1' THEN sales_amount ELSE 0 END)` <br> `AS Q1_sales` <br> `SUM(CASE WHEN quarter = 'Q2' THEN sales_amount ELSE 0 END)` <br> `AS Q2_sales` | Converts **sales by quarter into columns** |

---

### **Example 2: Pivot by Product (Sales per Product in Q1 2024)**
```sql
SELECT 
    product_name,
    SUM(CASE WHEN quarter = 'Q1' THEN sales_amount ELSE 0 END) AS Q1_sales
FROM sales_fact s
JOIN date_dim d ON s.date_id = d.date_id
JOIN product_dim p ON s.product_id = p.product_id
WHERE d.year = 2024
GROUP BY product_name;
```
✅ **Explanation**:
- Converts **sales per product into columns by quarter**.
- Filters for **2024 sales**.



| **Example** | **Pivot Condition** | **Query Purpose** |
|------------|---------------------|-------------------|
| **2** | `SUM(CASE WHEN quarter = 'Q1' THEN sales_amount ELSE 0 END)` | Converts **sales by product for Q1 2024 into columns** |

---

### **Example 3: Pivot by Region (Sales by Customer Region in 2024)**
```sql
SELECT 
    region,
    SUM(CASE WHEN quarter = 'Q1' THEN sales_amount ELSE 0 END) AS Q1_sales,
    SUM(CASE WHEN quarter = 'Q2' THEN sales_amount ELSE 0 END) AS Q2_sales
FROM sales_fact s
JOIN date_dim d ON s.date_id = d.date_id
JOIN customer_dim c ON s.customer_id = c.customer_id
WHERE d.year = 2024
GROUP BY region;
```
✅ **Explanation**:
- Groups sales **by customer region**.
- Displays **Q1 and Q2 sales as columns**.


| **Example** | **Pivot Condition** | **Query Purpose** |
|------------|---------------------|-------------------|
| **3** | `SUM(CASE WHEN quarter = 'Q1' THEN sales_amount ELSE 0 END),` <br> `SUM(CASE WHEN quarter = 'Q2' THEN sales_amount ELSE 0 END)` | Converts **sales by customer region into columns** |

---

### **Example 4: Pivot by Store and Quarter (Sales per Store per Quarter)**
```sql
SELECT 
    store_name,
    SUM(CASE WHEN quarter = 'Q1' THEN sales_amount ELSE 0 END) AS Q1_sales,
    SUM(CASE WHEN quarter = 'Q2' THEN sales_amount ELSE 0 END) AS Q2_sales
FROM sales_fact s
JOIN date_dim d ON s.date_id = d.date_id
JOIN store_dim st ON s.store_id = st.store_id
WHERE d.year = 2024
GROUP BY store_name;
```
✅ **Explanation**:
- Converts **quarterly sales into separate columns per store**.
- Groups by **store name**.

---

## **Summary**

| **Example** | **Pivot Condition** | **Query Purpose** |
|------------|---------------------|-------------------|
| **1** | `SUM(CASE WHEN quarter = 'Q1' THEN sales_amount ELSE 0 END)` | Converts **sales by quarter into columns** |
| **2** | `SUM(CASE WHEN quarter = 'Q1' THEN sales_amount ELSE 0 END)` | Converts **sales by product for Q1 2024 into columns** |
| **3** | `SUM(CASE WHEN quarter = 'Q1' THEN sales_amount ELSE 0 END), SUM(CASE WHEN quarter = 'Q2' THEN sales_amount ELSE 0 END)` | Converts **sales by customer region into columns** |
| **4** | `SUM(CASE WHEN quarter = 'Q1' THEN sales_amount ELSE 0 END), SUM(CASE WHEN quarter = 'Q2' THEN sales_amount ELSE 0 END)` | Converts **sales per store per quarter into columns** |

