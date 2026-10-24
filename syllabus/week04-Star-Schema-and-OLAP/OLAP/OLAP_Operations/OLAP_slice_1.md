# OLAP Slice

	Provide a star schema in mysql with 
	sample records for all tables and then 
	provide 4 examples (simple to complex) 
	of a "slice" operation in sql
	
### **What is a Slice Operation?**
- A **Slice** operation **filters the data on one dimension**, keeping all other dimensions unchanged.
- It helps to analyze a **subset** of the dataset.


## **1. Star Schema in MySQL (Sales Analysis System)**  

A **Star Schema** consists of a **central fact table** and **multiple dimension tables** to efficiently analyze sales data.

---

### **Fact Table: `sales_fact`**
Stores transactional sales data.

~~~
| sale_id | date_id | product_id | customer_id | store_id | sales_amount | quantity_sold |
|---------|---------|------------|-------------|----------|--------------|---------------|
| 1       | 1       | 1          | 1           | 1        | 500.00       | 5             |
| 2       | 2       | 2          | 2           | 1        | 300.00       | 3             |
| 3       | 3       | 3          | 3           | 2        | 700.00       | 7             |
| 4       | 4       | 1          | 4           | 2        | 900.00       | 9             |
| 5       | 5       | 2          | 5           | 3        | 250.00       | 2             |
~~~
---

### **Dimension Table: `date_dim`**
Stores date-related attributes.

~~~
| date_id | date       | year | quarter | month | day |
|---------|-----------|------|---------|-------|-----|
| 1       | 2024-01-01 | 2024 | Q1      | Jan   | 1   |
| 2       | 2024-02-01 | 2024 | Q1      | Feb   | 1   |
| 3       | 2024-03-01 | 2024 | Q1      | Mar   | 1   |
| 4       | 2024-04-01 | 2024 | Q2      | Apr   | 1   |
| 5       | 2024-05-01 | 2024 | Q2      | May   | 1   |
~~~

---

### **Dimension Table: `product_dim`**
Stores product-related attributes.

~~~
| product_id | product_name | category  | price  |
|------------|-------------|-----------|--------|
| 1          | Laptop      | Electronics | 100.00 |
| 2          | Phone       | Electronics | 50.00  |
| 3          | TV          | Electronics | 150.00 |
~~~
---

### **Dimension Table: `customer_dim`**
Stores customer-related attributes.

~~~
| customer_id | customer_name | region   |
|------------|--------------|---------|
| 1          | Alice        | North   |
| 2          | Bob          | South   |
| 3          | Charlie      | West    |
| 4          | David        | East    |
| 5          | Emily        | North   |
~~~
---

### **Dimension Table: `store_dim`**
Stores store-related attributes.

~~~
| store_id | store_name | location |
|----------|-----------|----------|
| 1        | Store A   | NY       |
| 2        | Store B   | CA       |
| 3        | Store C   | TX       |
~~~
---

## **2. Slice Operations in SQL**
### **What is a Slice Operation?**
- A **Slice** operation **filters the data on one dimension**, keeping all other dimensions unchanged.
- It helps to analyze a **subset** of the dataset.

---

### **Example 1: Slice on Time (Filter Sales for Q1 2024)**

```sql
SELECT d.year, 
       d.quarter, 
       SUM(s.sales_amount) AS total_sales
FROM 
     sales_fact s
JOIN 
     date_dim d ON s.date_id = d.date_id
WHERE 
     d.quarter = 'Q1' AND 
     d.year = 2024
GROUP BY 
     d.year, d.quarter;
```

✅ **Explanation**:
- Filters sales **only for Q1 2024**.
- Groups by **year and quarter**.

---

### **Example 2: Slice on Product Category (Electronics Only)**

```sql
SELECT p.category, 
       p.product_name, 
       SUM(s.sales_amount) AS total_sales
FROM 
     sales_fact s
JOIN 
     product_dim p ON s.product_id = p.product_id
WHERE 
     p.category = 'Electronics'
GROUP BY 
     p.category, p.product_name;
```

✅ **Explanation**:
- Filters **only Electronics** sales.
- Groups by **category and product name**.

---

### **Example 3: Slice on Store Location (Sales in NY Only)**

```sql
SELECT st.store_name, 
       st.location, 
       SUM(s.sales_amount) AS total_sales
FROM 
     sales_fact s
JOIN 
     store_dim st ON s.store_id = st.store_id
WHERE 
     st.location = 'NY'
GROUP BY 
     st.store_name, st.location;
```

✅ **Explanation**:
- Filters **only sales from NY stores**.
- Groups by **store and location**.

---

### **Example 4: Slice on Customer Region (North Region Sales in Q1 2024)**

```sql
SELECT c.region, 
       c.customer_name, 
       SUM(s.sales_amount) AS total_sales
FROM 
     sales_fact s
JOIN 
     customer_dim c ON s.customer_id = c.customer_id
JOIN 
     date_dim d ON s.date_id = d.date_id
WHERE 
     c.region = 'North' AND 
     d.quarter = 'Q1'   AND 
     d.year = 2024
GROUP 
     BY c.region, c.customer_name;
```

✅ **Explanation**:
- Filters **only North region customers**.
- Filters **only Q1 2024 sales**.
- Groups by **region and customer**.

---

## **Summary**
| **Example** | **Slice Condition** | **Query Purpose** |
|------------|---------------------|-------------------|
| **1** | `WHERE d.quarter = 'Q1' AND d.year = 2024` | Filters **Q1 2024** sales |
| **2** | `WHERE p.category = 'Electronics'` | Filters **only Electronics** sales |
| **3** | `WHERE st.location = 'NY'` | Filters **only NY** store sales |
| **4** | `WHERE c.region = 'North' AND d.quarter = 'Q1'` | Filters **North region sales in Q1 2024** |

