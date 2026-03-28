# Complete Working Example of an ETL in Python

## Database Configurations

Update the content of the following files accordingly.

* `db_config_source.json` (for source table)

* `db_config_target.json` (for destination table)


* source  database configuration:

```
% cat db_config_source.json
{
    "user": "root",
    "password": "mp22pass",
    "host": "localhost",
    "database": "scu_homeworks"
}
```

* target database configuration:

```
% cat db_config_target.json
{
    "user": "root",
    "password": "mp22pass",
    "host": "localhost",
    "database": "scu2_homeworks"
}
```

## What This ETL Does

✅ Extracts data from "source_table" and "continents" tables

✅ Transforms:
* 1.   Fills NULL age with 25

* 2. Fills NULL salary with 40000

* 3. Computes tax = salary * 10%

* 4. Creates "continent" column by (country, continent) look up table

✅ Loads data into destination_table


## ETL Summary

	Provide a complete working example of an ETL 
	in python, which reads mysql table (include 
	sample records), does some useful transformations 
	and then loads into another mysql table.

	Here’s a complete working ETL (Extract, Transform, Load) 
	pipeline in Python using MySQL. The example covers:

    	1.    Extract: Reads data from a MySQL table (source_table).
    
    	2.    Transform: Cleans data and performs some transformations.
    
    	3.    Load: Inserts transformed data into another MySQL table 
                (destination_table).

You’ll need:
    •    mysql-connector-python (pip install mysql-connector-python)
    •    A running MySQL server

------


## 1. MySQL Setup

	Before running the script, create the 
	source and destination tables in MySQL:

~~~sql
CREATE DATABASE scu_homeworks;


USE scu_homeworks;

CREATE TABLE source_table (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    age INT,
    country VARCHAR(20),
    salary INT
);

INSERT INTO source_table (name, age, country, salary) 
VALUES 
('Alice', 30,  'USA', 50000),
('George', 40,  'USA', 80000),
('Charlie', 35, 'USA', 70000),
('Chuck', 45, 'USA', 90000),
('Bob', NULL, 'CANADA', 60000),
('Betty', NULL, 'CANADA', 50000),
('Barb', 50, 'CANADA', 40000),
('Babak', 45, 'CANADA', 20000),
('Jeb', NULL, 'MEXICO', 30000),
('Jason', NULL, 'MEXICO', 50000),
('David', 28, 'MEXICO', NULL),
('Rafa', 38, 'MEXICO', NULL);

mysql> select * from source_table;
+----+---------+------+---------+--------+
| id | name    | age  | country | salary |
+----+---------+------+---------+--------+
|  1 | Alice   |   30 | USA     |  50000 |
|  2 | George  |   40 | USA     |  80000 |
|  3 | Charlie |   35 | USA     |  70000 |
|  4 | Chuck   |   45 | USA     |  90000 |
|  5 | Bob     | NULL | CANADA  |  60000 |
|  6 | Betty   | NULL | CANADA  |  50000 |
|  7 | Barb    |   50 | CANADA  |  40000 |
|  8 | Babak   |   45 | CANADA  |  20000 |
|  9 | Jeb     | NULL | MEXICO  |  30000 |
| 10 | Jason   | NULL | MEXICO  |  50000 |
| 11 | David   |   28 | MEXICO  |   NULL |
| 12 | Rafa    |   38 | MEXICO  |   NULL |
+----+---------+------+---------+--------+
12 rows in set (0.00 sec)

USE scu_homeworks;

CREATE TABLE continents (
    continent VARCHAR(30),
    country   VARCHAR(20),
    PRIMARY KEY (country)
);

INSERT INTO continents (continent, country) VALUES
('North America', 'USA'),
('North America', 'CANADA'),
('North America', 'MEXICO'),
('Asia', 'INDIA');


SELECT * FROM continents;
+---------------+---------+
| continent     | country |
+---------------+---------+
| North America | USA     |
| North America | CANADA  |
| North America | MEXICO  |
| Asis          | INDIA   |
+---------------+---------+
~~~

## Create Destination database and table definitions

~~~
CREATE DATABASE scu2_homeworks;

USE scu2_homeworks;

CREATE TABLE destination_table (
    id INT,
    name VARCHAR(50),
    age INT,
    country VARCHAR(20),
    salary INT,
    tax INT,
    continent VARCHAR(20)
);
~~~



# 2. Python ETL Script


-----

# 3. Running the ETL

Run the script:

~~~sh
python3 etl.py db_config_source.json db_config_target.json
~~~

# 4. Expected Output in destination_table

~~~
mysql> SELECT * FROM destination_table;

mysql> SELECT * FROM destination_table;
+------+---------+------+---------+--------+------+--------------+
| id   | name    | age  | country | salary | tax  | continent    |
+------+---------+------+---------+--------+------+--------------+
|    1 | Alice   |   30 | USA     |  50000 | 5000 | North America|
...

~~~
What will be Expiatory Data Analysis for the following table:

target_table (id: INT, name: String, age: INT, country: String, salary: INT, continent: String)

Use Python and show graphs for important EDA elements.

 



