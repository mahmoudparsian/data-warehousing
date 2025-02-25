# OLAP: Dice operation

	Provide a star schema in mysql with 
	sample records for all tables and 
	then provide 4 examples (simple to 
	complex) of a "dice" operation in sql

 ### **What is a Dice Operation?**
- **Dice filters on multiple dimensions at the same time**.
	
![](./images/olap-dice-2.png)

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

## **2. Dice Operations in SQL**
### **What is a Dice Operation?**
- **Dice filters on multiple dimensions at the same time**.
- It extracts a **subset of data** by applying multiple **conditions on different dimensions**.

---

### **Example 1: Dice on Time and Product (Q1 2024 & Electronics)**
```sql
SELECT d.year, d.quarter, p.category, p.product_name, SUM(s.sales_amount) AS total_sales
FROM sales_fact s
JOIN date_dim d ON s.date_id = d.date_id
JOIN product_dim p ON s.product_id = p.product_id
WHERE d.year = 2024 AND d.quarter = 'Q1'
AND p.category = 'Electronics'
GROUP BY d.year, d.quarter, p.category, p.product_name;
```
✅ **Explanation**:
- Filters for **Q1 2024 sales**.
- Filters for **Electronics category**.
- Groups by **time (year & quarter) and product details**.



| **Example** | **Dice Conditions** | **Query Purpose** |
|------------|---------------------|-------------------|
| **1** | `WHERE d.year = 2024 AND d.quarter = 'Q1'` <br> `AND p.category = 'Electronics'` | Filters **Q1 2024 Electronics sales** |

---

### **Example 2: Dice on Store and Customer Region (Sales in NY & North Region Customers)**
```sql
SELECT st.store_name, st.location, c.region, SUM(s.sales_amount) AS total_sales
FROM sales_fact s
JOIN store_dim st ON s.store_id = st.store_id
JOIN customer_dim c ON s.customer_id = c.customer_id
WHERE 
     st.location = 'NY' AND 
     c.region = 'North'
GROUP BY st.store_name, st.location, c.region;
```
✅ **Explanation**:
- Filters sales for **stores in NY**.
- Filters **customers from the North region**.
- Groups by **store and customer region**.



| **Example** | **Dice Conditions** | **Query Purpose** |
|------------|---------------------|-------------------|
| **2** | `WHERE st.location = 'NY'` <br> `AND c.region = 'North'` | Filters **NY store sales & North region customers** |



---

### **Example 3: Dice on Time, Product, and Store (Q2 2024, Laptops, Store B in CA)**
```sql
SELECT d.year, d.quarter, p.product_name, st.store_name, st.location, SUM(s.sales_amount) AS total_sales
FROM sales_fact s
JOIN date_dim d ON s.date_id = d.date_id
JOIN product_dim p ON s.product_id = p.product_id
JOIN store_dim st ON s.store_id = st.store_id
WHERE d.year = 2024 AND d.quarter = 'Q2'
AND p.product_name = 'Laptop'
AND st.location = 'CA'
GROUP BY d.year, d.quarter, p.product_name, st.store_name, st.location;
```
✅ **Explanation**:
- Filters for **Q2 2024**.
- Filters for **Laptop sales**.
- Filters for **Store B in California**.


| **Example** | **Dice Conditions** | **Query Purpose** |
|------------|---------------------|-------------------|
| **3** | `WHERE d.year = 2024 AND` <br> `d.quarter = 'Q2' AND` <br> `p.product_name = 'Laptop' AND st.location = 'CA'` | Filters **Q2 2024 Laptop sales in CA** |

---

### **Example 4: Dice on Time, Product, Store, and Customer (Q1 2024, Phones, Store A in NY, South Region Customers)**
```sql
SELECT d.year, d.quarter, p.product_name, st.store_name, st.location, c.region, SUM(s.sales_amount) AS total_sales
FROM sales_fact s
JOIN date_dim d ON s.date_id = d.date_id
JOIN product_dim p ON s.product_id = p.product_id
JOIN store_dim st ON s.store_id = st.store_id
JOIN customer_dim c ON s.customer_id = c.customer_id
WHERE 
     d.year = 2024 AND 
     d.quarter = 'Q1' AND 
     p.product_name = 'Phone' AND 
     st.location = 'NY' AND 
     c.region = 'South'
GROUP BY d.year, d.quarter, p.product_name, st.store_name, st.location, c.region;
```
✅ **Explanation**:
- Filters for **Q1 2024 sales**.
- Filters for **Phone sales**.
- Filters for **Store A in NY**.
- Filters for **Customers from the South region**.

---

## **Summary**

| **Example** | **Dice Conditions** | **Query Purpose** |
|------------|---------------------|-------------------|
| **1** | `WHERE d.year = 2024 AND d.quarter = 'Q1' AND p.category = 'Electronics'` | Filters **Q1 2024 Electronics sales** |
| **2** | `WHERE st.location = 'NY' AND c.region = 'North'` | Filters **NY store sales & North region customers** |
| **3** | `WHERE d.year = 2024 AND d.quarter = 'Q2' AND p.product_name = 'Laptop' AND st.location = 'CA'` | Filters **Q2 2024 Laptop sales in CA** |
| **4** | `WHERE d.year = 2024 AND d.quarter = 'Q1' AND p.product_name = 'Phone' AND st.location = 'NY' AND c.region = 'South'` | Filters **Q1 2024 Phone sales in NY for South region customers** |

---


