# MySQL
# GROUP BY Modifiers
# WITH ROLLUP

Source: MySQL Documentation


	1. The GROUP BY clause permits a WITH ROLLUP 
	modifier  that  causes summary  output to 
	include extra rows that represent higher-level 
	(that is, super-aggregate) summary operations. 
	
	2. ROLLUP thus enables you to answer questions 
	at multiple levels of analysis with a single 
	query. 
	
	3. For example, ROLLUP can be used to provide 
	support for OLAP (Online Analytical Processing) 
	operations.

-----

	EXAMPLE: 
	    Suppose that a sales table has year, country, product, 
	    and profit columns for recording sales profitability:

~~~sql
CREATE TABLE sales
(
    year    INT,
    country VARCHAR(20),
    product VARCHAR(32),
    profit  INT
);
~~~

To summarize table:

	To summarize table contents per year, 
	use a simple `GROUP BY` like this:

~~~sql
mysql> SELECT year, SUM(profit) AS profit
       FROM sales
       GROUP BY year;
+------+--------+
| year | profit |
+------+--------+
| 2000 |   4525 |
| 2001 |   3010 |
+------+--------+
~~~

## ROLLUP 

	1. The output shows the total (aggregate) profit 
	for each year.  
	
	2. To also determine the total profit summed over 
	all years, you must add up the individual 
	values yourself or run an additional query. 
	
	3. Or you can use ROLLUP, which provides both levels 
	of analysis with a single query. Adding a WITH ROLLUP 
	modifier to the GROUP BY clause causes the query to 
	produce another (super-aggregate) row that shows the 
	grand total over all year values:

~~~sql
mysql> SELECT year, SUM(profit) AS profit
       FROM sales
       GROUP BY year WITH ROLLUP;
+------+--------+
| year | profit |
+------+--------+
| 2000 |   4525 |
| 2001 |   3010 |
| NULL |   7535 |
+------+--------+
~~~

	1. NOTE: The NULL value in the year column 
	identifies the grand total super-aggregate line.


	2. ROLLUP has a more complex effect when there 
	are multiple GROUP BY columns. In this case, each 
	time there is a change in value in any but the 
	last grouping column, the query produces an extra 
	super-aggregate summary row.

	3. For example, without ROLLUP, a summary of the 
	sales table based on year, country, and product 
	might look like this, where the output indicates 
	summary values only at the year/country/product 
	level of analysis:

~~~sql
mysql> SELECT year, country, product, SUM(profit) AS profit
       FROM sales
       GROUP BY year, country, product;
+------+---------+------------+--------+
| year | country | product    | profit |
+------+---------+------------+--------+
| 2000 | Finland | Computer   |   1500 |
| 2000 | Finland | Phone      |    100 |
| 2000 | India   | Calculator |    150 |
| 2000 | India   | Computer   |   1200 |
| 2000 | USA     | Calculator |     75 |
| 2000 | USA     | Computer   |   1500 |
| 2001 | Finland | Phone      |     10 |
| 2001 | USA     | Calculator |     50 |
| 2001 | USA     | Computer   |   2700 |
| 2001 | USA     | TV         |    250 |
+------+---------+------------+--------+
~~~

## WITH ROLLUP

With ROLLUP added, the query produces several extra rows:

~~~
mysql> SELECT year, country, product, SUM(profit) AS profit
       FROM sales
       GROUP BY year, country, product WITH ROLLUP;
+------+---------+------------+--------+
| year | country | product    | profit |
+------+---------+------------+--------+
| 2000 | Finland | Computer   |   1500 |
| 2000 | Finland | Phone      |    100 |
| 2000 | Finland | NULL       |   1600 |
| 2000 | India   | Calculator |    150 |
| 2000 | India   | Computer   |   1200 |
| 2000 | India   | NULL       |   1350 |
| 2000 | USA     | Calculator |     75 |
| 2000 | USA     | Computer   |   1500 |
| 2000 | USA     | NULL       |   1575 |
| 2000 | NULL    | NULL       |   4525 |
| 2001 | Finland | Phone      |     10 |
| 2001 | Finland | NULL       |     10 |
| 2001 | USA     | Calculator |     50 |
| 2001 | USA     | Computer   |   2700 |
| 2001 | USA     | TV         |    250 |
| 2001 | USA     | NULL       |   3000 |
| 2001 | NULL    | NULL       |   3010 |
| NULL | NULL    | NULL       |   7535 |
+------+---------+------------+--------+
~~~

	1. NOTE: Now the output includes summary 
	   information at four levels of analysis, 
	   not just one:

	2. Following each set of product rows for 
	   a given year and country, an extra 
	   super-aggregate summary row appears 
	   showing the total for all products. 
  	   These rows have the product column set 
  	   to NULL.

	3. Following each set of rows for a given 
	   year, an extra super-aggregate summary 
	   row appears showing the total for all 
	   countries and products. These rows have 
	   the country and products columns set to NULL.

	4. Finally, following all other rows, an extra 
	   super-aggregate summary row appears showing 
	   the grand total for all years, countries, 
	   and products. 
	
	5. This row has the year, country, and products 
	   columns set to NULL (all of them).

## The NULL indicators

	1. The NULL indicators in each super-aggregate 
	row are produced when the row is sent to the 
	client. The server looks at the columns named 
	in the GROUP BY clause following the leftmost one 
	that has changed value. 
	
	2. For any column in the result set with a name 
	that matches any of those names, its value is 
	set to NULL. (If you specify grouping columns 
	by column position, the server identifies which 
	columns to set to NULL by position.)

	3. Because the NULL values in the super-aggregate 
	rows are placed into the result set at such a late 
	stage in query processing, you can test them as NULL 
	values only in the select list or HAVING clause. 
	
	4. You cannot test them as NULL values in join conditions 
	or the WHERE clause to determine which rows to select. 
	
	5. For example, you cannot add WHERE product IS NULL to 
	the query to eliminate from the output all but the 
	super-aggregate rows.

	6. The NULL values do appear as NULL on the 
	client side and can be tested as such using 
	any MySQL client programming interface. However, 
	at this point, you cannot distinguish whether a 
	NULL represents a regular grouped value or a 
	super-aggregate value. In MySQL 8.0, you can 
	use the `GROUPING()`function to test the distinction.


## Other Considerations When using ROLLUP

	1. The following discussion lists some behaviors 
	specific to the MySQL implementation of ROLLUP.

	2. When you use ROLLUP, you cannot also use an 
	`ORDER BY` clause to sort the results. In other 
	words, `ROLLUP` and `ORDER BY` are mutually 
	exclusive in MySQL. 
	
	3. However, you still have some control over sort 
	order. To work around the restriction that prevents 
	using `ROLLUP` with `ORDER BY` and achieve a specific 
	sort order of grouped results, generate the grouped 
	result set as a derived table and apply ORDER BY to it. 


For example:

~~~sql
mysql> SELECT * FROM
         (
           SELECT year, SUM(profit) AS profit
             FROM sales GROUP BY year WITH ROLLUP
         ) AS dt
       ORDER BY year DESC;
+------+--------+
| year | profit |
+------+--------+
| 2001 |   3010 |
| 2000 |   4525 |
| NULL |   7535 |
+------+--------+
~~~

	1. In this case, the super-aggregate summary rows 
	sort with the rows from which they are calculated, 
	and their placement depends on sort order (at the 
	beginning for ascending sort, at the end for 
	descending sort).
	
	2. LIMIT can be used to restrict the number of rows 
	returned to the client. LIMIT is applied after 
	ROLLUP, so the limit applies against the extra 
	rows added by ROLLUP. 


For example:

~~~sql
mysql> SELECT year, country, product, SUM(profit) AS profit
       FROM sales
       GROUP BY year, country, product WITH ROLLUP
       LIMIT 5;
+------+---------+------------+--------+
| year | country | product    | profit |
+------+---------+------------+--------+
| 2000 | Finland | Computer   |   1500 |
| 2000 | Finland | Phone      |    100 |
| 2000 | Finland | NULL       |   1600 |
| 2000 | India   | Calculator |    150 |
| 2000 | India   | Computer   |   1200 |
+------+---------+------------+--------+
~~~

	1. NOTE: Using LIMIT with ROLLUP may produce 
	results that are more difficult to interpret, 
	because there is less context for understanding 
	the super-aggregate rows.
	
	2. A MySQL extension permits a column that 
	does not appear in the GROUP BY list to be 
	named in the select list. In this case, the 
	server is free to choose any value from this 
	nonaggregated column in summary rows, and this 
	includes the extra rows added by WITH ROLLUP.
	
	3. For example, in the following query, country 
	is a non-aggregated column that does not appear 
	in the GROUP BY list and values chosen for this 
	column are nondeterministic:

~~~sql
mysql> SELECT year, country, SUM(profit) AS profit
       FROM sales
       GROUP BY year WITH ROLLUP;
+------+---------+--------+
| year | country | profit |
+------+---------+--------+
| 2000 | India   |   4525 |
| 2001 | USA     |   3010 |
| NULL | USA     |   7535 |
+------+---------+--------+
~~~

	1. This behavior is permitted when the 
	ONLY_FULL_GROUP_BY SQL mode is not enabled. 
	If that mode is enabled, the server rejects 
	the query as illegal because country is not 
	listed in the GROUP BY clause. 
	
	2. With ONLY_FULL_GROUP_BY enabled, you can 
	still execute the query by using the ANY_VALUE() 
	function for nondeterministic-value columns:

~~~sql
mysql> SELECT year, 
              ANY_VALUE(country) AS country, 
              SUM(profit) AS profit
       FROM sales
       GROUP BY year WITH ROLLUP;
+------+---------+--------+
| year | country | profit |
+------+---------+--------+
| 2000 | India   |   4525 |
| 2001 | USA     |   3010 |
| NULL | USA     |   7535 |
+------+---------+--------+
~~~

----------

# MySQL 8.0: GROUPING function

	Starting with MySQL 8.0.1, the server supports 
	the SQL GROUPING function.  The GROUPING function 
	is used to distinguish between a NULL representing 
	the set of all values in a super-aggregate row  
	(produced by a ROLLUP operation) from a NULL in 
	a regular row.

## Introduction

	MySQL server has supported GROUP BY extension ROLLUP 
	for sometime now.  Here is an example of how to use 
	ROLLUP with GROUP BY.
	
~~~sql
mysql> create table t1 (a integer, b integer, c integer);
Query OK, 0 rows affected (0.05 sec)
 
mysql> insert into t1 values (111,11,11);
Query OK, 1 row affected (0.01 sec)
 
mysql> insert into t1 values (222,22,22);
Query OK, 1 row affected (0.00 sec)
 
mysql> insert into t1 values (111,12,12);
Query OK, 1 row affected (0.00 sec)
 
mysql> insert into t1 values (222,23,23);
Query OK, 1 row affected (0.01 sec)
 
mysql> select * from t1;
+------+------+------+
| a    | b    | c    |
+------+------+------+
|  111 |   11 |   11 |
|  222 |   22 |   22 |
|  111 |   12 |   12 |
|  222 |   23 |   23 |
+------+------+------+
4 rows in set (0.00 sec)

mysql> SELECT a, b, SUM(c) as SUM FROM t1 GROUP BY a,b ; 
+------+------+------+
| a    | b    | SUM  |
+------+------+------+
|  111 |   11 |   11 |
|  222 |   22 |   22 |
|  111 |   12 |   12 |
|  222 |   23 |   23 |
+------+------+------+

mysql> SELECT a, b, SUM(c) as SUM FROM t1 GROUP BY a,b WITH ROLLUP; 
+------+------+------+
| a    | b    | SUM  |
+------+------+------+
|  111 |   11 |   11 |
|  111 |   12 |   12 |
|  111 | NULL |   23 |
|  222 |   22 |   22 |
|  222 |   23 |   23 |
|  222 | NULL |   45 |
| NULL | NULL |   68 |
+------+------+------+
7 rows in set (0.00 sec)
~~~

	As we see in the above result,  
	NULL’s are added by the ROLLUP 
	modifier for every super aggregate row.


Now let us add NULL’s into the table data:

~~~sql
mysql> INSERT INTO t1 values (1111,NULL,112); 
Query OK, 1 row affected (0.00 sec)
 
mysql> INSERT INTO t1 values (NULL,112,NULL); 
Query OK, 1 row affected (0.00 sec)
 
mysql> select * from t1;
+------+------+------+
| a    | b    | c    |
+------+------+------+
|  111 |   11 |   11 |
|  222 |   22 |   22 |
|  111 |   12 |   12 |
|  222 |   23 |   23 |
| 1111 | NULL |  112 |
| NULL |  112 | NULL |
+------+------+------+
6 rows in set (0.00 sec)
~~~

	We have the following result when we 
	query the data with ROLLUP after the 
	addition of NULL’s into table data.
	
~~~sql
mysql> SELECT a, b, SUM(c) as SUM FROM t1 GROUP BY a,b WITH ROLLUP;
+------+------+------+
| a    | b    | SUM  |
+------+------+------+
| NULL |  112 | NULL |
| NULL | NULL | NULL |
|  111 |   11 |   11 |
|  111 |   12 |   12 |
|  111 | NULL |   23 |
|  222 |   22 |   22 |
|  222 |   23 |   23 |
|  222 | NULL |   45 |
| 1111 | NULL |  112 |
| 1111 | NULL |  112 |
| NULL | NULL |  180 |
+------+------+------+
11 rows in set (0.01 sec)
~~~

	As we can see in the above example, 
	it is now difficult to distinguish 
	whether a  NULL is representing a 
	regular grouped value or a super-aggregate 
	value.

## What is new in MySQL-8.0.1

	1. The GROUPING function can be used in 
	the above example to differentiate NULLs 
	produced by ROLLUP from NULLs from the 
	grouped data.  
	
	2. GROUPING function for a column returns a 
	value of 1 when the NULL generated for that 
	column is a result of ROLLUP operation. 
	Else it returns a value of 0.
	
~~~sql
mysql> SELECT a, b, SUM(c) as SUM, 
       GROUPING(a), GROUPING(b) FROM t1 
       GROUP BY a,b WITH ROLLUP;
+------+------+------+-------------+-------------+
| a    | b    | SUM  | GROUPING(a) | GROUPING(b) |
+------+------+------+-------------+-------------+
| NULL |  112 | NULL |           0 |           0 |
| NULL | NULL | NULL |           0 |           1 |
|  111 |   11 |   11 |           0 |           0 |
|  111 |   12 |   12 |           0 |           0 |
|  111 | NULL |   23 |           0 |           1 |
|  222 |   22 |   22 |           0 |           0 |
|  222 |   23 |   23 |           0 |           0 |
|  222 | NULL |   45 |           0 |           1 |
| 1111 | NULL |  112 |           0 |           0 |
| 1111 | NULL |  112 |           0 |           1 |
| NULL | NULL |  180 |           1 |           1 |
+------+------+------+-------------+-------------+
11 rows in set (0.01 sec)
~~~

	1. As we see in the above example,  GROUPING(b) 
	returns a value of 1 only for those rows which 
	have NULLs produced by a ROLLUP operation.

	2. Another way of using the GROUPING function is 
	by passing multiple columns as arguments to a 
	single GROUPING function. 
	
	3. The result of the GROUPING function would 
	then be an integer bit mask having 1’s for the 
	arguments which have GROUPING(argument) as 1.

For example:

~~~sql

mysql> SELECT a, b, SUM(c) as SUM, 
       GROUPING(a,b) FROM t1 
       GROUP BY a,b WITH ROLLUP;
+------+------+------+---------------+
| a    | b    | SUM  | GROUPING(a,b) |
+------+------+------+---------------+
| NULL |  112 | NULL |             0 |
| NULL | NULL | NULL |             1 |
|  111 |   11 |   11 |             0 |
|  111 |   12 |   12 |             0 |
|  111 | NULL |   23 |             1 |
|  222 |   22 |   22 |             0 |
|  222 |   23 |   23 |             0 |
|  222 | NULL |   45 |             1 |
| 1111 | NULL |  112 |             0 |
| 1111 | NULL |  112 |             1 |
| NULL | NULL |  180 |             3 |
+------+------+------+---------------+
11 rows in set (0.00 sec)

~~~

	As seen here, if GROUPING (a,b) returns 3, 
	it means that NULL in column “a” and NULL in 
	column “b” for that row is produce by a ROLLUP 
	operation. If result is 1, NULL in column “b” 
	alone is a result of ROLLUP operation.

------

## Other uses of GROUPING function

	We can specify GROUPING function in a select 
	list or in a having condition. When specified 
	in having condition, we can use this function 
	to retrieve only super-aggregate rows or only 
	aggregate rows like in the example below.
	
~~~sql
mysql> SELECT a, b, SUM(c) as SUM 
       FROM t1 GROUP BY a,b 
       WITH ROLLUP 
       HAVING GROUPING(a) = 1 or GROUPING(b) = 1;
+------+------+------+
| a    | b    | SUM  |
+------+------+------+
| NULL | NULL | NULL |
|  111 | NULL |   23 |
|  222 | NULL |   45 |
| 1111 | NULL |  112 |
| NULL | NULL |  180 |
+------+------+------+
5 rows in set (0.00 sec)
~~~	

	We can also use GROUPING function to 
	differentiate super aggregates from 
	aggregates in a nice way as shown below:
	
~~~sql
mysql> SELECT 
          IF(GROUPING(a)=1,'All Departments', a) as Department, 
          IF(GROUPING(b)=1, 'All Employees', b) as Employees, 
          SUM(c) as SUM 
          FROM t1 GROUP BY a,b WITH ROLLUP;
+-----------------+---------------+------+
| Department      | Employees     | SUM  |
+-----------------+---------------+------+
| NULL            | 112           | NULL |
| NULL            | All Employees | NULL |
| 111             | 11            |   11 |
| 111             | 12            |   12 |
| 111             | All Employees |   23 |
| 222             | 22            |   22 |
| 222             | 23            |   23 |
| 222             | All Employees |   45 |
| 1111            | NULL          |  112 |
| 1111            | All Employees |  112 |
| All Departments | All Employees |  180 |
+-----------------+---------------+------+
11 rows in set (0.00 sec)
~~~

# SubQuery Solutions

Create and populate an OrderItems table.

~~~sql
CREATE TABLE Order_Items(
   Order_ID INT NOT NULL, 
   Item VARCHAR(20) NOT NULL,
   Quantity SMALLINT NOT NULL,
   PRIMARY KEY(OrderID, Item)
);

INSERT INTO Order_Items (Order_ID, Item, Quantity)
  VALUES 
   (1, 'M8 Bolt', 100), 
   (2, 'M8 Nut', 100),
   (3, 'M8 Washer', 200);
~~~

## Rank items based on ordered quantity. 

	Rank items based on ordered quantity. 
	This is a workaround for the window 
	ranking function.

~~~sql
SELECT Item, 
       Quantity,
       ( SELECT COUNT(*) 
            FROM Order_Items
              AS OI2 
            WHERE OI.Quantity > OI2.Quantity
       ) + 1 AS QtyRank
FROM Order_Items AS OI;
~~~

Calculate the grand total. 

	Calculate the grand total.
	This is a workaround for a partitioned 
	window aggregate function.

~~~sql
SELECT Item, 
       Quantity,
       (SELECT SUM(Quantity) FROM Order_Items AS OI2 
        WHERE OI2.Order_ID = OI.Order_ID
       ) AS 
       TotalOrderQty
FROM Order_Items AS OI;
~~~