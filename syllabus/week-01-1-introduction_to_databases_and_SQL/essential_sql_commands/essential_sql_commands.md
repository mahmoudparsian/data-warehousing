# Essential SQL Commands

* Here are 24 essential SQL commands, arranged from simple to more complex, with examples to guide you

* These examples progress from simple commands like creating databases and tables to more advanced operations like `JOIN` and `SUBQUERY`. Let me know if you'd like further clarification or help building your SQL expertise!

* How to learn: practice!

---

### 1. **CREATE DATABASE**
   ```sql
   -- create a database
   CREATE DATABASE company_db;
   
   -- make it your default database
   use company_db
   ```

### 2. **CREATE TABLE**
   ```sql
   CREATE TABLE employees (
       id INT,
       name VARCHAR(50),
       position VARCHAR(50),
       salary INT,
       age INT,
       country VARCHAR(50),
       dept_id INT
   );   ```

### 3. **INSERT INTO**  
   ```sql
INSERT INTO employees (id, name, position, salary, age, country, dept_id)
VALUES 
(1, 'Alice', 'CEO', 150000, 61, 'USA', 3),
(2, 'Bob', 'CTO', 140000, 45, 'USA', 3),
(3, 'Charlie', 'HR Manager', 75000, 32, 'USA', 3),
(4, 'Alex', 'Software Engineering', 140000, 55, 'USA', 5),
(5, 'Bobby', 'Software Engineering', 110000, 32, 'USA', 5),
(6, 'Charles', 'Sales', 75000, 44, 'USA', 1),
(7, 'Chuck', 'Marketing', 75000, 37, 'USA', 2),
(8, 'Candy', 'Marketing', 95000, 56, 'USA', 2),
(9, 'Dave', 'Marketing', 50000, 44, 'USA', 4),
(10, 'Rafa', 'Marketing', 90000, 33, 'USA', 4),

(11, 'Al', 'CEO', 120000, 41, 'CANADA', 3),
(12, 'Babak', 'CTO', 130000, 67, 'CANADA', 3),
(13, 'Chad', 'HR Manager', 70000, 60, 'CANADA', 3),
(14, 'Alosh', 'Software Engineering', 120000, 55, 'CANADA', 5),
(15, 'Mahin', 'Software Engineering', 100000, 32, 'CANADA', 5),
(16, 'Shahin', 'Sales', 70000, 40, 'CANADA', 1),
(17, 'Terry', 'Marketing', 100000, 31, 'CANADA', 4),
(18, 'Taba', 'Marketing', 90000, 37, 'CANADA', 4),

(19, 'Rafael', 'CEO', 130000, 65, 'MEXICO', 3),
(20, 'Gonzalez', 'Software Engineering', 110000, 55, 'MEXICO', 5),
(21, 'Casa', 'Software Engineering', 90000, 32, 'MEXICO', 5),
(22, 'Pedro', 'Sales', 80000, 40, 'MEXICO', 1),
(23, 'Barbara', 'Software Engineering', 120000, 32, 'MEXICO', 5),
(24, 'Samir', 'Sales', 40000, 40, 'MEXICO', 1);

   ```

### 4. **SELECT**  

   Retrieve all columns and rows:

   ```sql
   SELECT * 
   FROM employees;
   
   mysql> select * from employees;
+------+----------+----------------------+--------+------+---------+---------+
| id   | name     | position             | salary | age  | country | dept_id |
+------+----------+----------------------+--------+------+---------+---------+
|    1 | Alice    | CEO                  | 150000 |   61 | USA     |       3 |
|    2 | Bob      | CTO                  | 140000 |   45 | USA     |       3 |
|    3 | Charlie  | HR Manager           |  75000 |   32 | USA     |       3 |
|    4 | Alex     | Software Engineering | 140000 |   55 | USA     |       5 |
|    5 | Bobby    | Software Engineering | 110000 |   32 | USA     |       5 |
|    6 | Charles  | Sales                |  75000 |   44 | USA     |       1 |
|    7 | Chuck    | Marketing            |  75000 |   37 | USA     |       2 |
|    8 | Candy    | Marketing            |  95000 |   56 | USA     |       2 |
|    9 | Dave     | Marketing            |  50000 |   44 | USA     |       4 |
|   10 | Rafa     | Marketing            |  90000 |   33 | USA     |       4 |
|   11 | Al       | CEO                  | 120000 |   41 | CANADA  |       3 |
|   12 | Babak    | CTO                  | 130000 |   67 | CANADA  |       3 |
|   13 | Chad     | HR Manager           |  70000 |   60 | CANADA  |       3 |
|   14 | Alosh    | Software Engineering | 120000 |   55 | CANADA  |       5 |
|   15 | Mahin    | Software Engineering | 100000 |   32 | CANADA  |       5 |
|   16 | Shahin   | Sales                |  70000 |   40 | CANADA  |       1 |
|   17 | Terry    | Marketing            | 100000 |   31 | CANADA  |       4 |
|   18 | Taba     | Marketing            |  90000 |   37 | CANADA  |       4 |
|   19 | Rafael   | CEO                  | 130000 |   65 | MEXICO  |       3 |
|   20 | Gonzalez | Software Engineering | 110000 |   55 | MEXICO  |       5 |
|   21 | Casa     | Software Engineering |  90000 |   32 | MEXICO  |       5 |
|   22 | Pedro    | Sales                |  80000 |   40 | MEXICO  |       1 |
|   23 | Barbara  | Software Engineering | 120000 |   32 | MEXICO  |       5 |
|   24 | Samir    | Sales                |  40000 |   40 | MEXICO  |       1 |
+------+----------+----------------------+--------+------+---------+---------+
24 rows in set (0.00 sec)

   ```
   Retrieve specific columns:
   
   ```sql
   SELECT Name, Position 
   FROM employees;
   ```

### 5. **WHERE**  
   Filter results based on a condition:
   
   ```sql
   SELECT * 
   FROM employees 
   WHERE Salary > 100000;
   
   mysql> SELECT *
    ->    FROM employees
    ->    WHERE Salary > 100000;
+------+----------+----------------------+--------+------+---------+---------+
| id   | name     | position             | salary | age  | country | dept_id |
+------+----------+----------------------+--------+------+---------+---------+
|    1 | Alice    | CEO                  | 150000 |   61 | USA     |       3 |
|    2 | Bob      | CTO                  | 140000 |   45 | USA     |       3 |
|    4 | Alex     | Software Engineering | 140000 |   55 | USA     |       5 |
|    5 | Bobby    | Software Engineering | 110000 |   32 | USA     |       5 |
|   11 | Al       | CEO                  | 120000 |   41 | CANADA  |       3 |
|   12 | Babak    | CTO                  | 130000 |   67 | CANADA  |       3 |
|   14 | Alosh    | Software Engineering | 120000 |   55 | CANADA  |       5 |
|   19 | Rafael   | CEO                  | 130000 |   65 | MEXICO  |       3 |
|   20 | Gonzalez | Software Engineering | 110000 |   55 | MEXICO  |       5 |
|   23 | Barbara  | Software Engineering | 120000 |   32 | MEXICO  |       5 |
+------+----------+----------------------+--------+------+---------+---------+
10 rows in set (0.00 sec)
   ```

### 6. **UPDATE**  
   Modify existing data:
   
   ```sql
   UPDATE employees
   SET position = 'Chief Operating Officer'
   WHERE id = 1;
   ```

### 7. **DELETE**
   Remove rows from the table:
   
   ```sql
   DELETE FROM employees 
   WHERE id = 3;
   ```

### 8. **ALTER TABLE**  

Add or modify table structure:

* Add a column to an existing table:
   
```sql
     ALTER TABLE employees
     ADD bonus INT;
```

* Modify an existing column data type:
   
```sql
     ALTER TABLE employees
     MODIFY salary DECIMAL(12, 2);
```

### 9. **JOIN**  
   Combine rows from two tables. Example with a second table:
   
   ```sql
INSERT INTO departments (dept_id, dept_name)
VALUES 
(1, 'Sales'),
(2, 'Technical'),
(3, 'Management'),
(4, 'Marketing'),
(5, 'Software'),
(6, 'Top-Secret'),
(7, 'Classified');

mysql> select * from departments;
+---------+------------+
| dept_id | dept_name  |
+---------+------------+
|       1 | Sales      |
|       2 | Technical  |
|       3 | Management |
|       4 | Marketing  |
|       5 | Software   |
|       6 | Top-Secret |
|       7 | Classified |
+---------+------------+
7 rows in set (0.00 sec)

   
SELECT E.name, E.salary, D.dept_name
FROM employees E
JOIN departments D
ON E.dept_id = D.dept_id
WHERE E.salary > 120000;

+--------+--------+------------+
| name   | salary | dept_name  |
+--------+--------+------------+
| Alice  | 150000 | Management |
| Bob    | 140000 | Management |
| Alex   | 140000 | Software   |
| Babak  | 130000 | Management |
| Rafael | 130000 | Management |
+--------+--------+------------+
5 rows in set (0.00 sec)

   ```

### 10. **GROUP BY**  
   - Aggregate data: find average salary per department:
   
```sql
   SELECT dept_id, 
          AVG(Salary) AS average_salary
   FROM employees
   GROUP BY dept_id;
   
+---------+----------------+
| dept_id | average_salary |
+---------+----------------+
|       3 |    116428.5714 |
|       5 |    112857.1429 |
|       1 |     66250.0000 |
|       2 |     85000.0000 |
|       4 |     82500.0000 |
+---------+----------------+
5 rows in set (0.00 sec)
   
```
   
- Aggregate data: find number of employees per department:
   
```sql
   SELECT dept_id, 
          count(*) AS number_of_employees
   FROM employees
   GROUP BY dept_id;
   
+---------+---------------------+
| dept_id | number_of_employees |
+---------+---------------------+
|       3 |                   7 |
|       5 |                   7 |
|       1 |                   4 |
|       2 |                   2 |
|       4 |                   4 |
+---------+---------------------+
5 rows in set (0.00 sec)


SELECT    E.dept_id, 
          D.dept_name,
          count(*) AS number_of_employees
FROM employees E,
     departments D
WHERE E.dept_id = D.dept_id
GROUP BY E.dept_id;

+---------+------------+---------------------+
| dept_id | dept_name  | number_of_employees |
+---------+------------+---------------------+
|       3 | Management |                   7 |
|       5 | Software   |                   7 |
|       1 | Sales      |                   4 |
|       2 | Technical  |                   2 |
|       4 | Marketing  |                   4 |
+---------+------------+---------------------+
5 rows in set (0.00 sec)

```


### 11. **HAVING**  
   
Apply conditions to grouped data:
   
```sql
   SELECT dept_id, 
          AVG(salary) AS average_salary
   FROM employees
   GROUP BY dept_id
   HAVING AVG(salary) > 90000;
   
+---------+----------------+
| dept_id | average_salary |
+---------+----------------+
|       3 |    116428.5714 |
|       5 |    112857.1429 |
+---------+----------------+
2 rows in set (0.00 sec)

```

### 12. **SUBQUERY**  
   Use a query inside another query:
   
   ```sql
   SELECT * FROM employees
   WHERE salary > (
                   SELECT AVG(salary) FROM employees
                  );
+------+----------+----------------------+--------+------+---------+---------+
| id   | name     | position             | salary | age  | country | dept_id |
+------+----------+----------------------+--------+------+---------+---------+
|    1 | Alice    | CEO                  | 150000 |   61 | USA     |       3 |
|    2 | Bob      | CTO                  | 140000 |   45 | USA     |       3 |
|    4 | Alex     | Software Engineering | 140000 |   55 | USA     |       5 |
|    5 | Bobby    | Software Engineering | 110000 |   32 | USA     |       5 |
|   11 | Al       | CEO                  | 120000 |   41 | CANADA  |       3 |
|   12 | Babak    | CTO                  | 130000 |   67 | CANADA  |       3 |
|   14 | Alosh    | Software Engineering | 120000 |   55 | CANADA  |       5 |
|   15 | Mahin    | Software Engineering | 100000 |   32 | CANADA  |       5 |
|   17 | Terry    | Marketing            | 100000 |   31 | CANADA  |       4 |
|   19 | Rafael   | CEO                  | 130000 |   65 | MEXICO  |       3 |
|   20 | Gonzalez | Software Engineering | 110000 |   55 | MEXICO  |       5 |
|   23 | Barbara  | Software Engineering | 120000 |   32 | MEXICO  |       5 |
+------+----------+----------------------+--------+------+---------+---------+
12 rows in set (0.00 sec)
   ```

---

# subqueries and ranking functions


---

### **13. Subquery with `WHERE` Clause**
Find employees whose salary is above the average salary:

```sql
SELECT name, salary
FROM employees
WHERE salary > (
                 SELECT AVG(salary) 
                 FROM employees
               );
+----------+--------+
| name     | salary |
+----------+--------+
| Alice    | 150000 |
| Bob      | 140000 |
| Alex     | 140000 |
| Bobby    | 110000 |
| Al       | 120000 |
| Babak    | 130000 |
| Alosh    | 120000 |
| Mahin    | 100000 |
| Terry    | 100000 |
| Rafael   | 130000 |
| Gonzalez | 110000 |
| Barbara  | 120000 |
+----------+--------+
12 rows in set (0.00 sec)
```

---

### **14. Subquery with `IN`**
Get employees who work in specific departments by using a subquery:

```sql
SELECT name, position
FROM employees
WHERE dept_id IN (
                   SELECT dept_id 
                   FROM Departments 
                   WHERE dept_name = 'Marketing'
                 );

+-------+-----------+
| name  | position  |
+-------+-----------+
| Dave  | Marketing |
| Rafa  | Marketing |
| Terry | Marketing |
| Taba  | Marketing |
+-------+-----------+
4 rows in set (0.00 sec)
```

---

### **15. using LIMIT**
Find 3 highest salaried employees:

```sql
SELECT name, salary
FROM employees
ORDER BY salary DESC
LIMIT 3;

+-------+--------+
| name  | salary |
+-------+--------+
| Alice | 150000 |
| Bob   | 140000 |
| Alex  | 140000 |
+-------+--------+
3 rows in set (0.00 sec)

```

---

### **16. Ranking with `ROW_NUMBER()`**
Assign a unique rank to each employee based on their salary:

```sql
SELECT name, 
       salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) AS rnk
FROM employees;

+----------+--------+-----+
| name     | salary | rnk |
+----------+--------+-----+
| Alice    | 150000 |   1 |
| Bob      | 140000 |   2 |
| Alex     | 140000 |   3 |
| Babak    | 130000 |   4 |
| Rafael   | 130000 |   5 |
| Al       | 120000 |   6 |
| Alosh    | 120000 |   7 |
| Barbara  | 120000 |   8 |
| Bobby    | 110000 |   9 |
| Gonzalez | 110000 |  10 |
| Mahin    | 100000 |  11 |
| Terry    | 100000 |  12 |
| Candy    |  95000 |  13 |
| Rafa     |  90000 |  14 |
| Taba     |  90000 |  15 |
| Casa     |  90000 |  16 |
| Pedro    |  80000 |  17 |
| Charlie  |  75000 |  18 |
| Charles  |  75000 |  19 |
| Chuck    |  75000 |  20 |
| Chad     |  70000 |  21 |
| Shahin   |  70000 |  22 |
| Dave     |  50000 |  23 |
| Samir    |  40000 |  24 |
+----------+--------+-----+
24 rows in set (0.00 sec)
```

---

### **17. Ranking with `RANK()`**
Rank employees based on their salary, allowing ties to share the same rank:

```sql
SELECT name, 
       salary,
       RANK() OVER (ORDER BY salary DESC) AS rnk
FROM employees;

+----------+--------+-----+
| name     | salary | rnk |
+----------+--------+-----+
| Alice    | 150000 |   1 |
| Bob      | 140000 |   2 |
| Alex     | 140000 |   2 |
| Babak    | 130000 |   4 |
| Rafael   | 130000 |   4 |
| Al       | 120000 |   6 |
| Alosh    | 120000 |   6 |
| Barbara  | 120000 |   6 |
| Bobby    | 110000 |   9 |
| Gonzalez | 110000 |   9 |
| Mahin    | 100000 |  11 |
| Terry    | 100000 |  11 |
| Candy    |  95000 |  13 |
| Rafa     |  90000 |  14 |
| Taba     |  90000 |  14 |
| Casa     |  90000 |  14 |
| Pedro    |  80000 |  17 |
| Charlie  |  75000 |  18 |
| Charles  |  75000 |  18 |
| Chuck    |  75000 |  18 |
| Chad     |  70000 |  21 |
| Shahin   |  70000 |  21 |
| Dave     |  50000 |  23 |
| Samir    |  40000 |  24 |
+----------+--------+-----+
24 rows in set (0.00 sec)
```

---

### **18. Ranking with `DENSE_RANK()`**
Rank employees based on their salary without skipping ranks for ties:

```sql
SELECT name, 
       salary,
       DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
FROM employees;

+----------+--------+-----+
| name     | salary | rnk |
+----------+--------+-----+
| Alice    | 150000 |   1 |
| Bob      | 140000 |   2 |
| Alex     | 140000 |   2 |
| Babak    | 130000 |   3 |
| Rafael   | 130000 |   3 |
| Al       | 120000 |   4 |
| Alosh    | 120000 |   4 |
| Barbara  | 120000 |   4 |
| Bobby    | 110000 |   5 |
| Gonzalez | 110000 |   5 |
| Mahin    | 100000 |   6 |
| Terry    | 100000 |   6 |
| Candy    |  95000 |   7 |
| Rafa     |  90000 |   8 |
| Taba     |  90000 |   8 |
| Casa     |  90000 |   8 |
| Pedro    |  80000 |   9 |
| Charlie  |  75000 |  10 |
| Charles  |  75000 |  10 |
| Chuck    |  75000 |  10 |
| Chad     |  70000 |  11 |
| Shahin   |  70000 |  11 |
| Dave     |  50000 |  12 |
| Samir    |  40000 |  13 |
+----------+--------+-----+
24 rows in set (0.00 sec)

```

---


### **19. Subquery with `JOIN` and Ranking with `ROW_NUMBER()`**
Get the top 3 employees with the highest salaries in each country:

```sql
with ranked_emps as 
(
SELECT dept_id, 
      name, 
      country,
      salary, 
      ROW_NUMBER() OVER (PARTITION BY country ORDER BY salary DESC)
       AS rnk
FROM Employees
)
SELECT dept_id, 
   name,
   country, 
   salary, 
   rnk
FROM ranked_emps
WHERE rnk <= 3
ORDER BY country DESC;

+---------+----------+---------+--------+-----+
| dept_id | name     | country | salary | rnk |
+---------+----------+---------+--------+-----+
|       3 | Alice    | USA     | 150000 |   1 |
|       3 | Bob      | USA     | 140000 |   2 |
|       5 | Alex     | USA     | 140000 |   3 |
|       3 | Rafael   | MEXICO  | 130000 |   1 |
|       5 | Barbara  | MEXICO  | 120000 |   2 |
|       5 | Gonzalez | MEXICO  | 110000 |   3 |
|       3 | Babak    | CANADA  | 130000 |   1 |
|       3 | Al       | CANADA  | 120000 |   2 |
|       5 | Alosh    | CANADA  | 120000 |   3 |
+---------+----------+---------+--------+-----+
9 rows in set (0.00 sec)
```

---

### **20. Subquery with Aggregation and Ranking with `RANK()`**
Rank departments by their average salaries:

```sql
SELECT dept_id, 
       AVG(salary) AS average_salary,
       RANK() OVER (ORDER BY AVG(salary) DESC) AS department_rank
FROM employees
GROUP BY dept_id;

+---------+----------------+-----------------+
| dept_id | average_salary | department_rank |
+---------+----------------+-----------------+
|       3 |    116428.5714 |               1 |
|       5 |    112857.1429 |               2 |
|       2 |     85000.0000 |               3 |
|       4 |     82500.0000 |               4 |
|       1 |     66250.0000 |               5 |
+---------+----------------+-----------------+
5 rows in set (0.00 sec)

```

---

### **21. Subquery with `HAVING` Clause**
Find employees with salaries above the department average:

```sql
SELECT name, 
       salary, 
       dept_id
FROM employees
WHERE salary > (
    SELECT AVG(salary)
    FROM employees e
    WHERE e.dept_id = Employees.dept_id
);

+---------+--------+---------+
| name    | salary | dept_id |
+---------+--------+---------+
| Alice   | 150000 |       3 |
| Bob     | 140000 |       3 |
| Alex    | 140000 |       5 |
| Charles |  75000 |       1 |
| Candy   |  95000 |       2 |
| Rafa    |  90000 |       4 |
| Al      | 120000 |       3 |
| Babak   | 130000 |       3 |
| Alosh   | 120000 |       5 |
| Shahin  |  70000 |       1 |
| Terry   | 100000 |       4 |
| Taba    |  90000 |       4 |
| Rafael  | 130000 |       3 |
| Pedro   |  80000 |       1 |
| Barbara | 120000 |       5 |
+---------+--------+---------+
15 rows in set (0.00 sec)

```

---

### **22. Correlated Subquery with `DENSE_RANK()`**
Rank employees by salary within each department, handling ties with `DENSE_RANK()`:

```sql
SELECT name, 
       salary, 
       dept_id,
       DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) 
        AS rnk
FROM employees
ORDER BY dept_id;

+----------+--------+---------+-----+
| name     | salary | dept_id | rnk |
+----------+--------+---------+-----+
| Pedro    |  80000 |       1 |   1 |
| Charles  |  75000 |       1 |   2 |
| Shahin   |  70000 |       1 |   3 |
| Samir    |  40000 |       1 |   4 |
| Candy    |  95000 |       2 |   1 |
| Chuck    |  75000 |       2 |   2 |
| Alice    | 150000 |       3 |   1 |
| Bob      | 140000 |       3 |   2 |
| Babak    | 130000 |       3 |   3 |
| Rafael   | 130000 |       3 |   3 |
| Al       | 120000 |       3 |   4 |
| Charlie  |  75000 |       3 |   5 |
| Chad     |  70000 |       3 |   6 |
| Terry    | 100000 |       4 |   1 |
| Rafa     |  90000 |       4 |   2 |
| Taba     |  90000 |       4 |   2 |
| Dave     |  50000 |       4 |   3 |
| Alex     | 140000 |       5 |   1 |
| Alosh    | 120000 |       5 |   2 |
| Barbara  | 120000 |       5 |   2 |
| Bobby    | 110000 |       5 |   3 |
| Gonzalez | 110000 |       5 |   3 |
| Mahin    | 100000 |       5 |   4 |
| Casa     |  90000 |       5 |   5 |
+----------+--------+---------+-----+
24 rows in set (0.00 sec)
```

---

### **23. Subquery with Aggregation and Ranking Functions**
Find the highest-paid employee in each department:

```sql
SELECT name, 
       salary, 
       dept_id
FROM employees
WHERE salary = (
    SELECT MAX(salary)
    FROM employees e
    WHERE e.dept_id = employees.dept_id
);

+-------+--------+---------+
| name  | salary | dept_id |
+-------+--------+---------+
| Alice | 150000 |       3 |
| Alex  | 140000 |       5 |
| Candy |  95000 |       2 |
| Terry | 100000 |       4 |
| Pedro |  80000 |       1 |
+-------+--------+---------+
5 rows in set (0.01 sec)
```

---

### **24. Left-Join**
List department who have no employees:

* Iteration-1:

```sql
SELECT D.dept_id, 
       D.dept_name, 
       E.dept_id
FROM departments D
LEFT JOIN employees E
on D.dept_id = E.dept_id;

+---------+------------+---------+
| dept_id | dept_name  | dept_id |
+---------+------------+---------+
|       1 | Sales      |       1 |
|       1 | Sales      |       1 |
|       1 | Sales      |       1 |
|       1 | Sales      |       1 |
|       2 | Technical  |       2 |
|       2 | Technical  |       2 |
|       3 | Management |       3 |
|       3 | Management |       3 |
|       3 | Management |       3 |
|       3 | Management |       3 |
|       3 | Management |       3 |
|       3 | Management |       3 |
|       3 | Management |       3 |
|       4 | Marketing  |       4 |
|       4 | Marketing  |       4 |
|       4 | Marketing  |       4 |
|       4 | Marketing  |       4 |
|       5 | Software   |       5 |
|       5 | Software   |       5 |
|       5 | Software   |       5 |
|       5 | Software   |       5 |
|       5 | Software   |       5 |
|       5 | Software   |       5 |
|       5 | Software   |       5 |
|       6 | Top-Secret |    NULL |
|       7 | Classified |    NULL |
+---------+------------+---------+
26 rows in set (0.00 sec)
```

* Iteration-2:

~~~sql
SELECT D.dept_id, 
       D.dept_name, 
       E.dept_id
FROM departments D
LEFT JOIN employees E
on D.dept_id = E.dept_id
WHERE E.dept_id is NULL;

+---------+------------+---------+
| dept_id | dept_name  | dept_id |
+---------+------------+---------+
|       6 | Top-Secret |    NULL |
|       7 | Classified |    NULL |
+---------+------------+---------+
2 rows in set (0.00 sec)
~~~

* Iteration-3:

~~~sql
SELECT D.dept_id, 
       D.dept_name
FROM departments D
LEFT JOIN employees E
on D.dept_id = E.dept_id
WHERE E.dept_id is NULL;

+---------+------------+
| dept_id | dept_name  |
+---------+------------+
|       6 | Top-Secret |
|       7 | Classified |
+---------+------------+
2 rows in set (0.00 sec)

~~~

---

# References

### 1. [10 Essential SQL Commands](https://medium.com/@thallyscostalat/10-essential-sql-commands-every-data-professional-should-know-49cecd79bb0b)


### 2. [The Most Important SQL Commands](https://learnsql.com/blog/sql-commands/)