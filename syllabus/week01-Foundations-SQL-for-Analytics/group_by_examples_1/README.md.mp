# Data

```
% cat sales.csv
country,product,price
FRANCE,TV,200
FRANCE,TV,400
FRANCE,BIKE,400
FRANCE,BIKE,600
USA,TV,200
USA,TV,180
USA,TV,240
USA,BIKE,500
USA,BIKE,700
USA,COMPUTER,800
USA,COMPUTER,700
USA,COMPUTER,600
CANADA,TV,300
CANADA,TV,200
CANADA,COMPUTER,500
CANADA,COMPUTER,900
```

# Size of Data: Number of bytes
      
```
% ls -l sales.csv
-rw-r--r--@ 1 max  staff  260 Apr  1 00:44 sales.csv
```

# Number of records

```
% wc -l sales.csv
      17 sales.csv
```

# GROUP BY Examples using DuckDB

```sql
% duckdb
DuckDB v1.5.1 (Variegata)
Enter ".help" for usage hints.

memory D create table sales 
            as SELECT * from 'sales.csv';
            
memory D desc sales;
┌─────────────────┐
│      sales      │
│                 │
│ country varchar │
│ product varchar │
│ price   bigint  │
└─────────────────┘
```
### 1. Find total sales for all products

### 2. Select/Display all rows from the sales table

### 3. Find total product sales per country
  
### 4. Find total product sales per product

### 5. Find total product sales per country and product

### 6. Find the number of sales per country

### 7. write a sql query to find top selling product per country

```sql
SELECT *
FROM (
    SELECT 
        country,
        product,
        SUM(price) AS total_sales,
        RANK() OVER (
            PARTITION BY country
            ORDER BY SUM(price) DESC
        ) AS rnk
    FROM sales
    GROUP BY country, product
) t
WHERE rnk = 1;
```

##### OR

```sql
-- step-1: create ranks
WITH ranked_sales AS (
    SELECT 
        country,
        product,
        SUM(price) AS total_sales,
        RANK() OVER (
            PARTITION BY country
            ORDER BY SUM(price) DESC
        ) AS rnk
    FROM sales
    GROUP BY country, product
) 
-- step-2: filter by created ranks
SELECT country,
        product,
        total_sales,
        rnk
FROM ranked_sales
WHERE rnk = 1;
```


🧠 Explanation

	•	GROUP BY country, product 
	   → total sales per product per country
	    
	•	RANK() OVER (PARTITION BY country ...) 
		→ rank within each country
		
	•	WHERE rnk = 1 → top product per country
	
	
### 8. write a sql query to find top selling country overall

	👉 Interpretation:
		“Which country has the highest total sales 
		across all products?”

```sql
SELECT 
    country,
    SUM(price) AS total_sales
FROM sales
GROUP BY country
ORDER BY total_sales DESC
LIMIT 1;
```

Explanation

	•	Aggregate total sales per country
	•	Sort descending
	•	Take the top one

	
### 9. Show Full Ranking of all Countries

```sql
SELECT 
    country,
    SUM(price) AS total_sales,
    RANK() OVER (ORDER BY SUM(price) DESC) AS rnk
FROM sales
GROUP BY country;
```

1. GROUP BY

			👉 aggregation per dimension

2. Window Functions

			👉 ranking within partitions

### 10. Filtering Grouped Data (HAVING)

	Use the HAVING clause to filter the results 
	after they have been grouped. 

```sql
SELECT country, 
       SUM(price) as sum_per_country
FROM sales
GROUP BY country
HAVING sum_per_country > 1000;
```

### 11. Find the list of unique countries

### 12. Find the list of unique products


# One-Liner to Tell Students

* GROUP BY aggregates 

* window functions compare
