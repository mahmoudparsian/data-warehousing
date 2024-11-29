# 1. Tutorial: MySQL Ranking Functions

[Overview of SQL RANK functions](https://www.sqlshack.com/overview-of-sql-rank-functions/)


	MySQL offers several powerful ranking 
	functions that allow you to assign ranks 
	to rows within a result set, based on 
	specific criteria. 
	
	These functions are invaluable for tasks 
	like leaderboards, top-N analysis, and more.
	
## Practical Use Cases
* Leaderboards: Rank players or teams based on their performance.

* Top-N Analysis: Identify the top-performing products, customers, or employees.

* Sales Analysis: Rank sales representatives by their sales volume.

* Customer Segmentation: Rank customers based on their purchase frequency or total spending.

* Performance Evaluation: Rank employees based on their performance metrics.


## Key Ranking Functions

##  RANK()
* Assigns a rank to each row within a partition, with gaps for ties.
* Syntax: 

~~~sql
RANK() OVER (PARTITION BY partition_column ORDER BY order_column ASC/DESC)
~~~

* Example:

~~~sql
SELECT product_name, 
       sales_amount,
       RANK() OVER (ORDER BY sales_amount DESC) 
         AS product_rank
FROM products;
~~~


## DENSE_RANK()
* Assigns a rank to each row within a partition, without gaps for ties.
* Syntax: 

~~~sql
DENSE_RANK() OVER (PARTITION BY partition_column ORDER BY order_column ASC/DESC)
~~~

* Example:

~~~sql
SELECT
employee_name,
salary,
DENSE_RANK() OVER (ORDER BY salary DESC) AS salary_rank
FROM employees;
~~~

## ROW_NUMBER()
* Assigns a sequential number to each row within a partition, starting from 1.
* Syntax: 

~~~sql
ROW_NUMBER() OVER (PARTITION BY partition_column ORDER BY order_column ASC/DESC)
~~~

* Example:

~~~sql
SELECT
order_id,
order_date,
ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date ASC) AS order_number
FROM
orders;
~~~

## PERCENT_RANK()
* Calculates the percentile rank of each row within a partition.
* Syntax: 

~~~sql
PERCENT_RANK() OVER (PARTITION BY partition_column ORDER BY order_column ASC/DESC)
~~~

* Example:


~~~sql
SELECT
student_name,
score,
PERCENT_RANK() OVER (ORDER BY score DESC) AS percentile_rank
FROM
students;
~~~


## Additional Considerations

* Partitioning: Use the PARTITION BY clause to divide the result set into smaller groups, applying the ranking function to each group independently.

* Ordering: Use the ORDER BY clause to specify the sorting order of the rows within each partition.

* Ties: Consider how you want to handle ties in the ranking. The RANK() function leaves gaps for ties, while DENSE_RANK() assigns consecutive ranks to tied rows.
By mastering these ranking functions, you can gain deeper insights from your data and make more informed decisions.

# 2. Example

~~~sql
create table sales (
  id int, 
  month  varchar(10),
  amount  int
);

insert into sales(id, month, amount)
values
     (1,'Jan',450),
     (2,'Jan',350),
     (3,'Jan',250),
     (4,'Feb',150),
     (5,'Feb',450),
     (6,'Feb',500),
     (7,'Mar',350),
     (8,'Mar',450),
     (9,'Mar',250),
     (10,'Mar',150);
~~~

Test table:

~~~sql
mysql> select * from sales;
+------+-------+--------+
| id   | month | amount |
+------+-------+--------+
|    1 | Jan   |    450 |
|    2 | Jan   |    350 |
|    3 | Jan   |    250 |
|    4 | Feb   |    150 |
|    5 | Feb   |    450 |
|    6 | Feb   |    500 |
|    7 | Mar   |    350 |
|    8 | Mar   |    450 |
|    9 | Mar   |    250 |
|   10 | Mar   |    150 |
+------+-------+--------+
~~~

Ranking:

	Here’s the query to assign rank to each row 
	of the table, without using any PARTITION BY clause.

~~~sql
SELECT
     id, month, amount, 
     RANK() OVER (PARTITION BY Month ORDER BY amount desc) as rank
FROM sales;

+------+-------+--------+--------+
| id   | month | amount |  rank  |
+------+-------+--------+--------+
|    6 | Feb   |    500 |     1  |
|    5 | Feb   |    450 |     2  |
|    4 | Feb   |    150 |     3  |
|    1 | Jan   |    450 |     1  |
|    2 | Jan   |    350 |     2  |
|    3 | Jan   |    250 |     3  |
|    8 | Mar   |    450 |     1  |
|    7 | Mar   |    350 |     2  |
|    9 | Mar   |    250 |     3  |
|   10 | Mar   |    150 |     4  |
+------+-------+--------+--------+
~~~

	In the above query, we partition the table 
	by month name, and then rank each row within 
	each partition in descending order of amount.

