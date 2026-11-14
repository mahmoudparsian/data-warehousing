# Star Schema & OLAP Operations 

Provide a star schema in mysql with a fat table and 3 dimensions (provide with sample records). Then provide 3 rollup, 3 roll down, 3 slide, 3 dice , and 3 pivot olap operations with IO.

Here is a complete example of a **Star Schema in MySQL** using a **Fact Table** and **3 Dimension Tables**, followed by **sample OLAP operations** (Roll-Up, Roll-Down, Slice, Dice, and Pivot) with example inputs and outputs.

---

## ✅ 1. Star Schema in MySQL

### 📦 Fact Table: `sales_fact`

```sql
CREATE TABLE sales_fact (
    sale_id INT PRIMARY KEY,
    date_id INT,
    product_id INT,
    store_id INT,
    revenue DECIMAL(10,2),
    quantity_sold INT
);
```

### 📅 Dimension: `date_dim`

```sql
CREATE TABLE date_dim (
    date_id INT PRIMARY KEY,
    date DATE,
    month VARCHAR(20),
    quarter VARCHAR(10),
    year INT
);
```

### 📦 Dimension: `product_dim`

```sql
CREATE TABLE product_dim (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    brand VARCHAR(50)
);
```

### 🏬 Dimension: `store_dim`

```sql
CREATE TABLE store_dim (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(100),
    region VARCHAR(50),
    city VARCHAR(50)
);
```

---

## 📄 Sample Data

### `date_dim`

```sql
INSERT INTO date_dim 
VALUES
(1, '2025-01-10', 'January', 'Q1', 2025),
(2, '2025-02-15', 'February', 'Q1', 2025),
(3, '2025-04-12', 'April', 'Q2', 2025);
```

### `product_dim`

```sql
INSERT INTO product_dim 
VALUES
(1, 'Laptop X1', 'Electronics', 'BrandA'),
(2, 'Phone Z5', 'Electronics', 'BrandB'),
(3, 'Desk Chair', 'Furniture', 'BrandC');
```

### `store_dim`

```sql
INSERT INTO store_dim 
VALUES
(1, 'Store North', 'North', 'Chicago'),
(2, 'Store East', 'East', 'New York'),
(3, 'Store South', 'South', 'Houston');
```

### `sales_fact`

```sql
INSERT INTO sales_fact 
VALUES
(1, 1, 1, 1, 1500.00, 3),
(2, 2, 2, 2, 1200.00, 4),
(3, 3, 3, 3, 800.00, 2);
```

---

## 🔍 OLAP Operations

	OLAP (Online Analytical Processing) operations 
	allow users to explore data within a data cube 
	through various manipulations. These operations 
	include roll-up, drill-down, slice, dice, and 
	pivot, enabling analysts to view data at different 
	levels of granularity and from various perspectives. 
	
### Key OLAP Operations:

#### Roll-up:
		Aggregates data from lower levels to higher 
		levels of a dimension hierarchy. For example,
		summarizing  daily  sales  to  monthly or 
		quarterly sales.
		
		Roll-up example: You might roll up from daily 
		sales to weekly or monthly sales by aggregating 
		the data for each week or month.
		 
#### Drill-down:
		Moves from a higher level of aggregation to a 
		lower level of a dimension hierarchy. For instance,
	 	viewing annual sales data and then drilling down 
	 	to monthly sales. 
	 	
	 	Drill-down example: You can drill down from total 
	 	sales to sales by region, then to sales by city, 
	 	and finally to sales by specific product.

#### Slice:
		Selects a single value from one dimension, 
		creating a sub-cube. For example, focusing 
		on sales data for a specific product category. 
		
		Slice example: You might slice the cube to view 
		only sales for the "Electronics" product category.

#### Dice:
		Selects multiple values from one or more dimensions,
		creating a sub-cube. For example, examining sales 
		data for specific products in a particular region
		during a given period. 
		
		Dice example: You could dice the cube to view 
		sales for  "Electronics"  in  "Western Europe" 
		during the "Q2" quarter.

#### Pivot:
		Rotates the data cube by moving a dimension from 
		the row to the column, or vice versa, to view data 
		from a different angle. 

		Pivot example: You could pivot the cube to view sales 
		by time on the rows and product on the columns.


------

## 1️⃣ **Roll-Up (less detail)**

#### Example: Roll-up from **month** to **quarter**

```sql
SELECT d.year,
       d.quarter, 
       SUM(f.revenue) AS total_revenue
FROM 
     sales_fact f
JOIN 
     date_dim d ON f.date_id = d.date_id
GROUP BY 
     d.year,
     d.quarter;
```

OR

```sql
SELECT d.year,
       d.quarter, 
       SUM(f.revenue) AS total_revenue
FROM 
     sales_fact f,
     date_dim d
WHERE 
      f.date_id = d.date_id
GROUP BY 
     d.year,
     d.quarter;
```



#### IO:

| year  |quarter | total\_revenue |
| ----- |------- | -------------- |
| 2025  |Q1      | 2700.00        |
| 2025  |Q2      | 800.00         |

---

## 2️⃣ **Roll-Down (more detail)**

#### Example: Roll-down from **quarter** to **month**

```sql
SELECT d.year, 
       d.month, 
       SUM(f.revenue) AS total_revenue
FROM 
     sales_fact f
JOIN 
     date_dim d ON f.date_id = d.date_id
GROUP BY 
     d.year,
     d.month;
```

#### IO:

| year | month    | total\_revenue |
| ---- |-------- | -------------- |
| 2025 |January  | 1500.00        |
| 2025 |February | 1200.00        |
| 2025 |April    | 800.00         |

---

## 3️⃣ **Slice**

#### Example: Get data for **January only**

```sql
SELECT 
      f.sale_id, 
      f.revenue, 
      f.quantity_sold
FROM 
     sales_fact f
JOIN 
     date_dim d ON f.date_id = d.date_id
WHERE 
     d.month = 'January';
```

#### IO:

| sale\_id | revenue | quantity\_sold |
| -------- | ------- | -------------- |
| 1        | 1500.00 | 3              |

---

## 4️⃣ **Dice**

#### Example: Data for **Electronics** category in **Q1**

```sql
SELECT p.category, 
       d.year,
       d.quarter, 
       SUM(f.revenue) AS total
FROM 
     sales_fact f
JOIN 
     product_dim p ON f.product_id = p.product_id
JOIN 
     date_dim d ON f.date_id = d.date_id
WHERE 
     p.category = 'Electronics' AND 
     d.quarter = 'Q1'
GROUP BY 
     p.category, 
     d.year,
     d.quarter;
```

OR

```sql
SELECT p.category, 
       d.year,
       d.quarter, 
       SUM(f.revenue) AS total
FROM 
     sales_fact f,
     product_dim p, 
     date_dim d

WHERE 
     f.product_id = p.product_id AND
     f.date_id = d.date_id       AND
     p.category = 'Electronics'  AND 
     d.quarter = 'Q1'
GROUP BY 
     p.category, 
     d.year,
     d.quarter;
```



#### IO:

| category    | year  |quarter | total   |
| ----------- | ----  |------- | ------- |
| Electronics | 2025  | Q1     | 2700.00 |

---

### 5️⃣ **Pivot (cross-tab)**

#### Example: Revenue by **region** and **month**

```sql
SELECT
    s.region,
    SUM(CASE WHEN d.month = 'January' THEN f.revenue ELSE 0 END) AS January,
    SUM(CASE WHEN d.month = 'February' THEN f.revenue ELSE 0 END) AS February,
    SUM(CASE WHEN d.month = 'April' THEN f.revenue ELSE 0 END) AS April
FROM sales_fact f
JOIN date_dim d ON f.date_id = d.date_id
JOIN store_dim s ON f.store_id = s.store_id
GROUP BY s.region;
```

#### IO:

| region | January | February | April  |
| ------ | ------- | -------- | ------ |
| North  | 1500.00 | 0.00     | 0.00   |
| East   | 0.00    | 1200.00  | 0.00   |
| South  | 0.00    | 0.00     | 800.00 |

---

### More OLAP Examples:

#### ✅ Roll-Up: Region → All Regions

```sql
SELECT 
     SUM(f.revenue) AS total_revenue
FROM 
     sales_fact f
JOIN 
     store_dim s ON f.store_id = s.store_id;
```

#### ✅ Roll-Down: Region → City

```sql
SELECT 
     s.city, 
     SUM(f.revenue) AS total_revenue
FROM 
     sales_fact f
JOIN 
     store_dim s ON f.store_id = s.store_id
GROUP BY 
     s.city;
```

#### ✅ Slice: Only BrandB Products

```sql
SELECT 
     f.sale_id, 
     f.revenue
FROM 
     sales_fact f
JOIN 
     product_dim p ON f.product_id = p.product_id
WHERE 
     p.brand = 'BrandB';
```

#### ✅ Dice: Electronics in North or South region

```sql
SELECT 
     f.sale_id, 
     f.revenue
FROM 
     sales_fact f
JOIN 
     product_dim p ON f.product_id = p.product_id
JOIN 
     store_dim s ON f.store_id = s.store_id
WHERE 
      p.category = 'Electronics' AND 
      s.region IN ('North', 'South');
```

#### ✅ Pivot: Quantity sold by product and month

```sql
SELECT
    p.product_name,
    SUM(CASE WHEN d.month = 'January' THEN f.quantity_sold ELSE 0 END) AS Jan_Qty,
    SUM(CASE WHEN d.month = 'February' THEN f.quantity_sold ELSE 0 END) AS Feb_Qty,
    SUM(CASE WHEN d.month = 'April' THEN f.quantity_sold ELSE 0 END) AS Apr_Qty
FROM sales_fact f
JOIN product_dim p ON f.product_id = p.product_id
JOIN date_dim d ON f.date_id = d.date_id
GROUP BY p.product_name;
```

---

# References

1. [What is OLAP?](https://www.datacamp.com/tutorial/what-is-olap)

2. [Data Warehousing - OLAP](https://www.tutorialspoint.com/dwh/dwh_olap.htm)

3. [OLAP Operations](https://cci.drexel.edu/faculty/song/courses/info%20607/tutorial_OLAP/operations.htm)