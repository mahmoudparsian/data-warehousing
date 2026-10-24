# OLAP Slice Operation

	Provide a star schema in mysql with 
	sample records for all tables and then 
	provide 4 examples (simple to complex) 
	of a "slice" operation in sql
	
	Let's start by defining a simple star schema 
	in MySQL. A star schema consists of a central 
	fact table connected to multiple dimension tables. 
	Here's an example involving a retail store scenario:

# Star Schema

### Fact Table: Sales

~~~
sale_id	date	product_id	store_id	customer_id	quantity	total_amount
1	2025-02-20	1001	200	3000	2	40.00
2	2025-02-21	1002	201	3001	1	25.00
~~~

### Dimension Table: Products

~~~
product_id	product_name	category	price
1001	Widget A	Widgets	20.00
1002	Widget B	Widgets	25.00
~~~

### Dimension Table: Stores

~~~
store_id	store_name	location
200	Store A	Downtown
201	Store B	Uptown
~~~

### Dimension Table: Customers

customer_id	customer_name	membership_level
3000	John Doe	Gold
3001	Jane Smith	Silver

# Slice Operation Examples

### Simple Slice - Sales on a specific date
* This query retrieves all sales data for February 20, 2025.

~~~sql
SELECT * FROM Sales
WHERE date = '2025-02-20';
~~~

### Slice - Sales of a specific product
* This query retrieves all sales data for "Widget A".

~~~sql
SELECT * FROM Sales
WHERE product_id = 1001;
~~~


### Slice - Sales from a specific store and product category

* This query retrieves all sales data from "Store A" for products in the "Widgets" category.

~~~sql
SELECT s.*
FROM Sales s
JOIN Products p ON s.product_id = p.product_id
JOIN Stores t ON s.store_id = t.store_id
WHERE t.store_name = 'Store A' AND 
      p.category = 'Widgets';
~~~

### Slice - Sales for a specific customer with a certain membership level

* This query retrieves all sales data for customers with the "Gold" membership level.

~~~sql
SELECT s.*
FROM Sales s
JOIN Customers c ON s.customer_id = c.customer_id
WHERE c.membership_level = 'Gold';
~~~

