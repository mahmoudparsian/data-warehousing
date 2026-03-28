# Star Schema and Roll Up

	Provide a star schema in mysql with 
	sample records for all tables and then 
	provide 4 examples (simple to complex) 
	of a "roll up" opertion in sql

## Roll-Up Operations in SQL

		Roll-up is an OLAP (Online Analytical Processing) 
 		operation where we aggregate data at different 
  		levels of granularity.


A **Star Schema** in MySQL consists of a central **fact table** and several **dimension tables** that provide descriptive attributes. Let's create a star schema for a **Sales Analysis System**.

# What to do

### **Summary**
1. **Created a Star Schema** with a fact table and multiple dimensions.
2. **Inserted sample records** for realistic data.
3. **Demonstrated 4 roll-up operations**, from basic to complex.


---

### **1. Star Schema Design**
#### **Fact Table: `sales_fact`**
Stores transactional data.

~~~
| sale_id | date_id | product_id | customer_id | store_id | sales_amount | quantity_sold |
|---------|---------|------------|-------------|----------|--------------|---------------|
| 1       | 1       | 1          | 1           | 1        | 500.00       | 5             |
| 2       | 2       | 2          | 2           | 1        | 300.00       | 3             |
| 3       | 3       | 3          | 3           | 2        | 700.00       | 7             |
~~~

#### **Dimension Table: `date_dim`**
Stores date-related attributes.

~~~
| date_id | date       | year | quarter | month | day |
|---------|-----------|------|---------|-------|-----|
| 1       | 2024-01-01 | 2024 | Q1      | Jan   | 1   |
| 2       | 2024-02-01 | 2024 | Q1      | Feb   | 1   |
| 3       | 2024-03-01 | 2024 | Q1      | Mar   | 1   |
~~~

#### **Dimension Table: `product_dim`**
Stores product-related attributes.

~~~
| product_id | product_name | category  | price  |
|------------|-------------|-----------|--------|
| 1          | Laptop      | Electronics | 100.00 |
| 2          | Phone       | Electronics | 50.00  |
| 3          | TV          | Electronics | 150.00 |
~~~

#### **Dimension Table: `customer_dim`**
Stores customer-related attributes.

~~~
| customer_id | customer_name | region   |
|------------|--------------|---------|
| 1          | Alice        | North   |
| 2          | Bob          | South   |
| 3          | Charlie      | West    |
~~~

#### **Dimension Table: `store_dim`**
Stores store-related attributes.

~~~
| store_id | store_name | location |
|----------|-----------|----------|
| 1        | Store A   | NY       |
| 2        | Store B   | CA       |
~~~
---

### **2. Roll-Up Operations in SQL**
**Roll-up** is an OLAP (Online Analytical Processing) operation where we aggregate data at different levels of granularity.

---

#### **Example 1: Roll-Up on Time (Summing Sales by Year)**

```sql
SELECT d.year, 
       SUM(s.sales_amount) AS total_sales
FROM 
     sales_fact s
JOIN 
     date_dim d ON s.date_id = d.date_id
GROUP BY 
     d.year;
```
✅ **Explanation**: Aggregates total sales at the **yearly** level.

---

#### **Example 2: Roll-Up on Product Category**

```sql
SELECT p.category, 
       SUM(s.sales_amount) AS total_sales
FROM 
     sales_fact s
JOIN 
     product_dim p ON s.product_id = p.product_id
GROUP BY 
     p.category;
```

✅ **Explanation**: Aggregates total sales at the **product category** level.

---

#### **Example 3: Roll-Up on Store & Region**

```sql
SELECT c.region, 
       st.location, 
       SUM(s.sales_amount) AS total_sales
FROM 
    sales_fact s
JOIN 
    customer_dim c ON s.customer_id = c.customer_id
JOIN 
    store_dim st ON s.store_id = st.store_id
GROUP BY 
    c.region, st.location WITH ROLLUP;
```

✅ **Explanation**:  
- Groups by **region** and **store location**.  
- `WITH ROLLUP` generates **subtotals** and a **grand total**.

---

#### **Example 4: Multi-Level Roll-Up on Time & Product**

```sql
SELECT d.year, 
       d.quarter, 
       p.category, 
       SUM(s.sales_amount) AS total_sales
FROM 
     sales_fact s
JOIN 
     date_dim d ON s.date_id = d.date_id
JOIN 
     product_dim p ON s.product_id = p.product_id
GROUP BY 
     d.year, d.quarter, p.category WITH ROLLUP;
```

✅ **Explanation**:  
- Aggregates sales by **year → quarter → category**.  
- **ROLLUP** provides **subtotals** at each level.



