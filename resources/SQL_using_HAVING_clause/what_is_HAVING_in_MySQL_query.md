# What is HAVING by in MySQL?

	The MySQL HAVING clause allows filtering 
	of aggregated  results produced by  the 
	MySQL GROUP BY clause. In the same way 
	you used MySQL WHERE clause to restrict 
	rows, you use the MySQL HAVING clause 
	to restrict groups.
	
	What is HAVING clause in SQL with example?
	The HAVING clause allows for filtering based 
	on multiple aggregate values. For example, 
	you can filter groups based on both the 
	sum and average of a column, like 
	
		HAVING SUM(column) > [value1] AND 
		AVG(column) > [value2]
		
# Syntax

The `HAVING` clause was introduced in SQL to allow 
the filtering of query results based on aggregate 
functions and groupings. Unlike the `WHERE` clause, 
which filters individual rows before any grouping 
occurs, the `HAVING` clause works on **groups of data**
 that have been aggregated using functions like `SUM()`, 
 `AVG()`, `COUNT()`, and others.

In this article, we will learn the concept of the HAVING clause, and its syntax, and provide several practical examples

## What is the SQL HAVING Clause?

The `HAVING` clause is used to filter the result 
of  `GROUP BY` based on the specified condition. 
The conditions are Boolean type i.e. use of logical 
operators  (AND, OR). This clause was included in 
SQL as the WHERE keyword failed when we used it with 
aggregate expressions. Having is a very generally 
used clause in SQL. Similar to WHERE it helps to 
apply conditions, but HAVING works with groups. If 
you wish to filter a group, the HAVING clause comes 
into action.

Some important points:

* `HAVING` clause is used to filter data according 
   to the conditions provided.
* `HAVING` a clause is generally used in reports of large data.  
* `HAVING` clause is only used with the SELECT clause.
* The expression in the syntax can only have constants.
* In the query, ORDER BY  is to be placed after the `HAVING` clause, if any.
* `HAVING` Clause is implemented in column operation.
* `HAVING` clause is generally used after GROUP BY.       

Syntax:

```sql
SELECT col_1, col_2, function_name(col_3)

FROM table_name

GROUP BY col_1, col_2

HAVING Condition
```

## SQL HAVING Clause Examples
Here first we create a database name as “Company”, 
then we will create a table named “Employee” in 
the database. After creating a table we will 
execute the query.

Creating a table

```sql
-- Create the Employee table with appropriate data types
CREATE TABLE Employee (
  EmployeeId int,
  Name varchar(50),
  Gender varchar(10),
  Salary int,
  Department varchar(20),
  Experience int -- Changed to int for years of experience
);
```

Populating a table

```sql
-- Insert multiple rows into the Employee table in a single query
INSERT INTO Employee (EmployeeId, Name, Gender, Salary, Department, Experience)
VALUES 
  (5, 'Priya Sharma', 'Female', 45000, 'IT', 2),
  (6, 'Rahul Patel', 'Male', 65000, 'Sales', 5),
  (7, 'Nisha Gupta', 'Female', 55000, 'Marketing', 4),
  (8, 'Vikram Singh', 'Male', 75000, 'Finance', 7),
  (9, 'Aarti Desai', 'Female', 50000, 'IT', 3);
```

The final table is:

```sql

mysql> select * from Employee;
+------------+--------------+--------+--------+------------+------------+
| EmployeeId | Name         | Gender | Salary | Department | Experience |
+------------+--------------+--------+--------+------------+------------+
|          5 | Priya Sharma | Female |  45000 | IT         |          2 |
|          6 | Rahul Patel  | Male   |  65000 | Sales      |          5 |
|          7 | Nisha Gupta  | Female |  55000 | Marketing  |          4 |
|          8 | Vikram Singh | Male   |  75000 | Finance    |          7 |
|          9 | Aarti Desai  | Female |  50000 | IT         |          3 |
+------------+--------------+--------+--------+------------+------------+
5 rows in set (0.00 sec)
```

## Example 1 : Using HAVING to Filter Aggregated Results

	This employee table will help us understand 
	the HAVING Clause. It contains employee IDs, 
	Name, Gender, department, and salary. To Know 
	the sum of salaries, we will write the query:

```sql
SELECT Department, sum(Salary) as Sum_Salary
FROM Employee
GROUP BY department;
```

output:

```sql
mysql> SELECT Department, sum(Salary) as Sum_Salary
    -> FROM Employee
    -> GROUP BY department;
+------------+------------+
| Department | Sum_Salary |
+------------+------------+
| IT         |      95000 |
| Sales      |      65000 |
| Marketing  |      55000 |
| Finance    |      75000 |
+------------+------------+
4 rows in set (0.00 sec)
```

## Apply HAVING:

	Now if we need to display the departments 
	where the sum of salaries is 50,000 or more. 
	In this condition, we will use the HAVING Clause.

~~~sql
SELECT Department, SUM(Salary) as Sum_Salary
FROM Employee
GROUP BY department
HAVING Sum_Salary >= 70000;  
~~~

output:

```sql
mysql> SELECT Department, SUM(Salary) as Sum_Salary
    -> FROM Employee
    -> GROUP BY department
    -> HAVING Sum_Salary >= 70000;
+------------+------------+
| Department | Sum_Salary |
+------------+------------+
| IT         |      95000 |
| Finance    |      75000 |
+------------+------------+
2 rows in set (0.00 sec)
```

## Example 2: Using HAVING with Multiple Conditions

	If we want to find the departments where the 
	total salary is greater than or equal to $50,000, 
	and the average salary is greater than $55,000. 
	We can use the HAVING clause to apply both conditions.

Without HAVING clause:

~~~sql
mysql> SELECT Department,
    ->        SUM(Salary) AS Total_Salary,
    ->        AVG(Salary) AS Average_Salary
    -> FROM Employee
    -> GROUP BY Department;
+------------+--------------+----------------+
| Department | Total_Salary | Average_Salary |
+------------+--------------+----------------+
| IT         |        95000 |     47500.0000 |
| Sales      |        65000 |     65000.0000 |
| Marketing  |        55000 |     55000.0000 |
| Finance    |        75000 |     75000.0000 |
+------------+--------------+----------------+
4 rows in set (0.00 sec)
~~~

With HAVING clause:

~~~sql
SELECT Department, 
       SUM(Salary) AS Total_Salary, 
       AVG(Salary) AS Average_Salary
FROM Employee
GROUP BY Department
HAVING Total_Salary >= 50000 AND Average_Salary > 55000;

mysql> SELECT Department,
    ->        SUM(Salary) AS Total_Salary,
    ->        AVG(Salary) AS Average_Salary
    -> FROM Employee
    -> GROUP BY Department
    -> HAVING Total_Salary >= 50000 AND Average_Salary > 55000;
+------------+--------------+----------------+
| Department | Total_Salary | Average_Salary |
+------------+--------------+----------------+
| Sales      |        65000 |     65000.0000 |
| Finance    |        75000 |     75000.0000 |
+------------+--------------+----------------+
2 rows in set (0.00 sec)
~~~

## Example 3: Using HAVING with COUNT()

	If we want to find departments where there 
	are more than two employees. For this, we can 
	use the COUNT() aggregate function along with 
	the HAVING clause.

Query:

```sql
SELECT Department, COUNT(EmployeeId) AS Emp_Count
FROM Employee
GROUP BY Department;

mysql> SELECT Department, COUNT(EmployeeId) AS Emp_Count
    -> FROM Employee
    -> GROUP BY Department;
+------------+-----------+
| Department | Emp_Count |
+------------+-----------+
| IT         |         2 |
| Sales      |         1 |
| Marketing  |         1 |
| Finance    |         1 |
+------------+-----------+
4 rows in set (0.01 sec)
```

Use HAVING clause:

```sql
SELECT Department, COUNT(EmployeeId) AS Emp_Count
FROM Employee
GROUP BY Department
HAVING Emp_Count >= 2;

mysql> SELECT Department, COUNT(EmployeeId) AS Emp_Count
    -> FROM Employee
    -> GROUP BY Department
    -> HAVING Emp_Count >= 2;
+------------+-----------+
| Department | Emp_Count |
+------------+-----------+
| IT         |         2 |
+------------+-----------+
1 row in set (0.00 sec)
```

## Example 4: Using HAVING with AVG()

	Let’s find out the average salary for each 
	department and use the HAVING clause to 
	display only those departments where the 
	average salary is greater than $50,000.

Query:

```sql
SELECT Department, AVG(Salary) AS Avg_Salary
FROM Employee
GROUP BY Department

mysql> SELECT Department, AVG(Salary) AS Avg_Salary
    -> FROM Employee
    -> GROUP BY Department;
+------------+------------+
| Department | Avg_Salary |
+------------+------------+
| IT         | 47500.0000 |
| Sales      | 65000.0000 |
| Marketing  | 55000.0000 |
| Finance    | 75000.0000 |
+------------+------------+
4 rows in set (0.01 sec)
```

Apply HAVING clause:

```sql
SELECT Department, AVG(Salary) AS Avg_Salary
FROM Employee
GROUP BY Department
HAVING Avg_Salary > 50000;

mysql> SELECT Department, AVG(Salary) AS Avg_Salary
    -> FROM Employee
    -> GROUP BY Department
    -> HAVING Avg_Salary > 50000;
+------------+------------+
| Department | Avg_Salary |
+------------+------------+
| Sales      | 65000.0000 |
| Marketing  | 55000.0000 |
| Finance    | 75000.0000 |
+------------+------------+
3 rows in set (0.00 sec)
```

## Conclusion

	The HAVING clause is an essential tool in 
	SQL for filtering results based on **aggregated 
	data**. Unlike the WHERE clause, which applies 
	conditions to individual rows, HAVING works on 
	**groups of data** that have been aggregated 
	using functions like SUM(), AVG(), and COUNT(). 
	
	Understanding how and when to use the HAVING 
	clause allows you to perform more complex data 
	analysis and generate meaningful insights from 
	your datasets.

