# 1. Tutorial

[Overview of SQL RANK functions](https://www.sqlshack.com/overview-of-sql-rank-functions/)

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

