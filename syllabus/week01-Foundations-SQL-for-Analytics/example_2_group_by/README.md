# Teaching GROUP BY

1. Provide a notebook, which asnswers 14 questions listed below:
for each NL query, write an associated SQL, 
explain SQL query, and tell what is the business insight 
from the query. If you can plot the result plot it
using DuckDB plotting (simple plotting) and explain the result.

2. If you can add more queries to help "GROUP BY",
then please add it.

3. as a downloadable file

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
### 1. Display all records from sales table

### 2. Find total sales for all products for USA

### 3. Find total sales for all products for all countries

### 4. Find the list of unique countries

### 5. Find the list of unique products

### 6. Find total product sales per country
  
### 7. Find total product sales per product

### 8. Find total product sales per country and product

### 9. Find the number of sales per country

### 10. write a sql query to find top selling product per country
	
### 11. write a sql query to find top selling country overall

### 12. Show Full Ranking of all Countries (based on sale of products)

### 13. Find list countries, which they have sold products more than $1500

### 14. Find highest price product sold per country
