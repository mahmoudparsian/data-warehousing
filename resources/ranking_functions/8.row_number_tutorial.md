# MySQL Tutorial: Using ROW_NUMBER()

This is a self-contained guide for MySQL 8.x.

## 1. Introduction

### ✅ 1.1 Description:

	1. ROW_NUMBER() is a window function that 
	assigns sequential numbers...
	
	2. Why do we call it a "window" function?
	
		ROW_NUMBER() is a window function because 
		it operates on a set of rows related to the 
		current row, known as a "window," rather than
		aggregating all rows in a table into a single 
		result or operating on a single row at a time.

	3. The ROW_NUMBER() function in MySQL assigns 
	a unique, sequential number to each row within 
	a result set or a partition of a result set. 
	
	4. This function was introduced in MySQL 8.0 as 
	part of its window functions capabilities.
	
### ✅ 1.2 Syntax

	ROW_NUMBER() OVER (
	                   [PARTITION BY expression [, ...]] 
	                   ORDER BY expression [ASC|DESC] 
	                   [, ...]
	                  )

Explanation:

* `ROW_NUMBER()`: The function itself, which assigns the row number.

* `OVER()`: This clause is mandatory for all window functions and defines the "window" or set of rows over which the function operates.

* `PARTITION BY expression [, ...]` (Optional): This clause divides the result set into partitions (groups) based on the specified column(s). The `ROW_NUMBER()` function will reset its numbering to 1 for each new partition. If omitted, the entire result set is treated as a single partition.
 
* `ORDER BY expression [ASC|DESC] [, ...]`: This clause defines the order of rows within each partition (or the entire result set if no PARTITION BY is used). The `ROW_NUMBER()` is assigned based on this specified order.

### 1.3 ✅ Example Usage:

☑️ **Assigning row numbers to an entire result set:**

		This query assigns a sequential 
		row number to each row in `your_table`, 
		ordered by `column1` in ascending order. 

```sql
		SELECT
		    column1,
		    column2,
		    ROW_NUMBER() OVER (ORDER BY column1 ASC) 
		      AS row_num
		FROM
		    your_table;
```



☑️ **Assigning row numbers within partitions:**

		This query assigns a rank to products within 
		each category, ordered by price in descending 
		order. The product_rank_in_category will reset 
		to 1 for each new category.
		
```sql

    SELECT
        category,
        product_name,
        price,
        ROW_NUMBER() OVER (PARTITION BY category 
                           ORDER BY price DESC) 
          AS product_rank_in_category
    FROM
        products;
```



## 2. Dataset: 2 Tables: employees & logs

### 2.1 employees Table:

```sql
DROP TABLE IF EXISTS employees;
CREATE TABLE employees (
  emp_id INT PRIMARY KEY,
  name VARCHAR(50),
  department VARCHAR(30),
  salary INT,
  hire_date DATE
);
INSERT INTO employees VALUES
(101,'Alice','AI',175000,'2021-02-10'),
(102,'Bob','IT',120000,'2022-04-01'),
(103,'Carol','AI',180000,'2023-05-15'),
(104,'David','Sales',90000,'2020-08-10'),
(105,'Eve','IT',135000,'2021-11-12'),
(106,'Frank','Sales',95000,'2022-01-05'),
(107,'Grace','AI',150000,'2024-01-01');
```

### 2.1 logs Table:

```sql
DROP TABLE IF EXISTS logs;
CREATE TABLE logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    event VARCHAR(30) NOT NULL,
    event_time DATETIME NOT NULL
);

INSERT INTO logs (user_id, event, event_time) VALUES
(1, 'login',  '2024-01-01 10:00'),
(1, 'login',  '2024-01-01 10:00'),
(1, 'login',  '2024-01-01 10:01'),
(2, 'logout', '2024-02-10 17:00'),
(2, 'logout', '2024-02-10 17:00');
```

## 3. Basic Usage

```sql
SELECT emp_id,
       name,
       salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) 
         AS salary_rank
FROM employees;
```

## 4. Partition Example

```sql
SELECT name,
       department,
       salary,
       ROW_NUMBER() OVER (PARTITION BY department 
                          ORDER BY salary DESC) 
         AS dept_rank
FROM employees;
```

## 5. Top-1 per Department

```sql
WITH ranked AS (
 SELECT emp_id,
        name,
        department,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department 
                           ORDER BY salary DESC) 
          AS rn
 FROM employees
)
SELECT * 
FROM ranked 
WHERE rn=1;
```

## 6. Top-N per Department

```sql
WITH ranked AS (
 SELECT emp_id,
        name,
        department,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department 
                           ORDER BY salary DESC) 
          AS rn
 FROM employees
)
SELECT * 
FROM ranked 
WHERE rn <= 2 
ORDER BY  department, rn;
```

## 7. Latest Record per Department

```sql
WITH ranked AS (
 SELECT emp_id,
        name,
        department,
        hire_date,
        ROW_NUMBER() OVER (PARTITION BY department 
                           ORDER BY hire_date DESC) 
          AS rn
 FROM employees
)
SELECT * 
FROM ranked 
WHERE rn=1;
```

## 8. Deduplication with ROW_NUMBER

```sql
WITH ranked AS (
 SELECT *, 
        ROW_NUMBER() OVER (PARTITION BY user_id,event,event_time 
                           ORDER BY id) AS rn
 FROM logs
)
SELECT * 
FROM ranked 
WHERE rn=1;
```

## 9. Detecting Duplicates

```sql
WITH ranked AS (
 SELECT *, 
        ROW_NUMBER() OVER (PARTITION BY user_id,event,event_time 
                           ORDER BY id) 
          AS rn
 FROM logs
)
SELECT * 
FROM ranked 
WHERE rn > 1;
```

## 10. Pagination Example

```sql
WITH ranked AS (
   SELECT *, 
          ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn
   FROM employees
)
SELECT * 
FROM ranked 
WHERE rn BETWEEN 6 AND 10;
```

## 11. Best Practices
- Always specify ORDER BY.
- Use PARTITION BY to group rankings.
- Use CTEs to filter by row numbers.

------
## 12. Example

The `ROW_NUMBER()` function is useful when creating tables. 
The following example is using a dataset, customers, with 
entries for `first_name`, `last_name`, and `city` (where they live).

```
first_name  last_name   city
Sarah       Myer        Houston
Susan       Davidson    Dallas
Mary        Greene      Raleigh
Joseph      Chang       Raleigh
Eric        Gustav      Louisville
Chris       Blake       Manchester
Tyler       Hunter      Houston
Matthew     Rivera      Louisville
Samantha    Daniels     Dallas
Emily       Pugh        Manchester
```
Using the following statement, the above information 
is pulled from the dataset customers. It is ordered 
alphabetically by their first name, then each row is 
assigned an integer starting with `1`.

```sql
SELECT
  ROW_NUMBER() OVER (
  ORDER BY first_name
  ) AS row_num,
  first_name,
  last_name,
  city
FROM
  customers;
```

Output:

```
row_num   first_name    last_name    city
1         Chris         Blake        Manchester
2         Emily         Pugh         Manchester
3         Eric          Gustav       Louisville
4         Joseph        Chang        Raleigh
5         Mary          Greene       Raleigh
6         Matthew       Rivera       Louisville
7         Samantha      Daniels      Dallas
8         Sarah         Myer         Houston
9         Susan         Davidson     Dallas
10        Tyler         Hunter       Houston
```

### 12.1 Pagination Example

		For pagination, the function 
		would be changed like so to only 
		show the first 5 entries:

```sql
WITH customers_ranked AS (
  SELECT
    ROW_NUMBER() OVER (
      ORDER BY
        first_name
      ) row_num,
      first_name,
      last_name,
      city
  FROM
    customers
) 
SELECT
  row_num,
  first_name,
  last_name,
  city
FROM
  customers_ranked
WHERE
  row_num > 0 AND
  row_num <= 5;
```

Output:

```
row_num   first_name    last_name    city
1         Chris         Blake        Manchester
2         Emily         Pugh         Manchester
3         Eric          Gustav       Louisville
4         Joseph        Chang        Raleigh
5         Mary          Greene       Raleigh
```

### 12.2 Using Partitions

	The ROW_NUMBER() function above could instead 
	be modified like so to include partitions:

```sql
SELECT
  ROW_NUMBER() OVER (
   PARTITION BY city
   ORDER BY first_name
  ) row_num,
    first_name,
    last_name,
    city
FROM
  customers
ORDER BY
  city;
```

Output:

```
row_num   first_name   last_name  city
1         Samantha     Daniels    Dallas
2         Susan        Davidson   Dallas
1         Sarah        Myer       Houston
2         Tyler        Hunter     Houston
1         Eric         Gustav     Louisville
2         Matthew      Rivera     Louisville
1         Chris        Blake      Manchester
2         Emily        Pugh       Manchester
1         Joseph       Chang      Raleigh
2         Mary         Greene     Raleigh
```

## 13. Removing duplicate rows

	You can use the ROW_NUMBER() to turn non-unique 
	rows into unique rows and then delete the duplicate 
	rows. 
	
Consider the following example.

✅  First, create a table with some duplicate values:

```sql
CREATE TABLE t (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(10) NOT NULL
);

INSERT INTO t(name) 
VALUES('A'),
      ('B'),
      ('B'),
      ('C'),
      ('C'),
      ('C'),
      ('D');
```

View Table:

```sql
SELECT * 
FROM t;
```

Output:

```
+----+------+
| id | name |
+----+------+
|  1 | A    |
|  2 | B    |
|  3 | B    |
|  4 | C    |
|  5 | C    |
|  6 | C    |
|  7 | D    |
+----+------+
7 rows in set (0.00 sec)
```


✅  Second, use the `ROW_NUMBER()` function to divide the rows into partitions by all columns. The row number will restart for each unique set of rows.

```sql
SELECT 
  id, 
  name, 
  ROW_NUMBER() OVER (
    PARTITION BY name
    ORDER BY id
  ) AS row_num 
FROM 
  t;
```


Output:

```
+----+------+---------+
| id | name | row_num |
+----+------+---------+
|  1 | A    |       1 |
|  2 | B    |       1 |
|  3 | B    |       2 |
|  4 | C    |       1 |
|  5 | C    |       2 |
|  6 | C    |       3 |
|  7 | D    |       1 |
+----+------+---------+
7 rows in set (0.00 sec)
```

The output indicates that the unique rows are the ones with the row number 1.

✅  Third, you can use the common table expression (CTE) 
to return the duplicate rows and the DELETE statement to remove them:

```sql
WITH dups AS (
  SELECT 
    id,
    name,
    ROW_NUMBER() OVER (
      PARTITION BY name 
      ORDER BY id
    ) AS row_num
  FROM t
)
DELETE FROM t
WHERE id IN (
  SELECT id
  FROM dups
  WHERE row_num > 1
);
```

✅ 🧠 Explanation
	•	The CTE (dups) ranks rows by name and id.
	•	The inner SELECT finds all IDs where row_num > 1 (i.e., duplicates).
	•	The outer DELETE removes those IDs directly from the base table t.
	

✅ Finally, select data from the t table to check for duplicates:

```sql
 select * 
 from t;
```

Output:

```
+----+------+
| id | name |
+----+------+
|  1 | A    |
|  2 | B    |
|  4 | C    |
|  7 | D    |
+----+------+
4 rows in set (0.00 sec)
```

