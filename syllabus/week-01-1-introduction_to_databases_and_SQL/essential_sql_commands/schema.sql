CREATE DATABASE company_db;

use company_db;

CREATE TABLE employees (
       id INT,
       name VARCHAR(50),
       position VARCHAR(50),
       salary INT,
       age INT,
       country VARCHAR(50),
       dept_id INT
   );

CREATE TABLE departments (
       dept_id INT PRIMARY KEY,
       dept_name VARCHAR(50)
);
   
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
   