# Star Schema Example <br> and OLAP Queries

## Fact Table:

	Sales(store_ID, item_ID, cust_ID, date_ID, price)

## DIM Tables

	Store(store_ID, city, county, state)

	Item(item_ID, category, color)

	Customer(cust_ID, cname, gender, age)

	Dates(date_ID, date, year, month, day)

## MySQL Database: `stars_sales`

## Prepare `Dates DIM`

~~~sql
use stars_sales;

create table dates (
   `date_ID` int(11) NOT NULL AUTO_INCREMENT,
   `date` Date NOT NULL,
   `year` int(11) NOT NULL,
   `month` int(11) NOT NULL,
   `day` int(11) NOT NULL,
   primary key (dateID)
);
~~~

MySQL execution:

~~~
mysql> create table dates (
    ->    `date_ID` int(11) NOT NULL AUTO_INCREMENT,
    ->    `date` Date NOT NULL,
    ->    `year` int(11) NOT NULL,
    ->    `month` int(11) NOT NULL,
    ->    `day` int(11) NOT NULL,
    ->    primary key (dateID)
    -> );
Query OK, 0 rows affected, 4 warnings (0.09 sec)
~~~


## Describe Dates table:

~~~sql
mysql> desc dates;
+--------+------+------+-----+---------+----------------+
| Field  | Type | Null | Key | Default | Extra          |
+--------+------+------+-----+---------+----------------+
| date_ID| int  | NO   | PRI | NULL    | auto_increment |
| date   | date | NO   |     | NULL    |                |
| year   | int  | NO   |     | NULL    |                |
| month  | int  | NO   |     | NULL    |                |
| day    | int  | NO   |     | NULL    |                |
+--------+------+------+-----+---------+----------------+
5 rows in set (0.03 sec)
~~~

## Create Surrogate key in MySQL

What is a surrogate key in SQL?

	1. It holds a unique value for all records.

	2. It is generated automatically.

	3. It can't be modified by the user or the application.

	4. It can be used only in the CRUD 
	   (Create, Read, Update, Delete) operations.

### What is a stored procedure?

	A stored procedure is a prepared SQL code 
	that you can save, so the code can be reused 
	over and over again. So if you have an SQL query 
	that you write over and over again, save it as 
	a stored procedure, and then just call it to 
	execute it.
	

## Create a Stored Procedure

~~~sql
DROP PROCEDURE IF EXISTS fill_dates;
DELIMITER |
CREATE PROCEDURE fill_dates(date_Start DATE, date_End DATE)
BEGIN
  WHILE date_Start <= date_End DO
    INSERT INTO dates(date_id, date, year, month, day)
      VALUES (null,
              date_Start,
              SUBSTRING_INDEX(date_Start, '-', 1),
              SUBSTRING_INDEX(SUBSTRING_INDEX(date_Start,'-', 2), '-',-1),
              SUBSTRING_INDEX(date_Start, '-', -1)
      );
    SET date_Start = date_add(date_Start, INTERVAL 1 DAY);
  END WHILE;
END;
|
DELIMITER ;
~~~

## Populate Dates Table

~~~sql
mysql> --              date_Start    date_End
mysql> CALL fill_dates('2011-03-01','2011-03-30');
Query OK, 1 row affected (0.02 sec)

mysql> CALL fill_dates('2012-03-01','2012-03-30');
Query OK, 1 row affected (0.01 sec)
~~~

View populated Dates table:

~~~
mysql> select * from dates;
+--------+------------+------+-------+-----+
| date_ID| date       | year | month | day |
+--------+------------+------+-------+-----+
|      1 | 2011-03-01 | 2011 |     3 |   1 |
|      2 | 2011-03-02 | 2011 |     3 |   2 |
|      3 | 2011-03-03 | 2011 |     3 |   3 |
|      4 | 2011-03-04 | 2011 |     3 |   4 |
|      5 | 2011-03-05 | 2011 |     3 |   5 |
|      6 | 2011-03-06 | 2011 |     3 |   6 |
|      7 | 2011-03-07 | 2011 |     3 |   7 |
|      8 | 2011-03-08 | 2011 |     3 |   8 |
|      9 | 2011-03-09 | 2011 |     3 |   9 |
|     10 | 2011-03-10 | 2011 |     3 |  10 |
|     11 | 2011-03-11 | 2011 |     3 |  11 |
|     12 | 2011-03-12 | 2011 |     3 |  12 |
|     13 | 2011-03-13 | 2011 |     3 |  13 |
|     14 | 2011-03-14 | 2011 |     3 |  14 |
|     15 | 2011-03-15 | 2011 |     3 |  15 |
|     16 | 2011-03-16 | 2011 |     3 |  16 |
|     17 | 2011-03-17 | 2011 |     3 |  17 |
|     18 | 2011-03-18 | 2011 |     3 |  18 |
|     19 | 2011-03-19 | 2011 |     3 |  19 |
|     20 | 2011-03-20 | 2011 |     3 |  20 |
|     21 | 2011-03-21 | 2011 |     3 |  21 |
|     22 | 2011-03-22 | 2011 |     3 |  22 |
|     23 | 2011-03-23 | 2011 |     3 |  23 |
|     24 | 2011-03-24 | 2011 |     3 |  24 |
|     25 | 2011-03-25 | 2011 |     3 |  25 |
|     26 | 2011-03-26 | 2011 |     3 |  26 |
|     27 | 2011-03-27 | 2011 |     3 |  27 |
|     28 | 2011-03-28 | 2011 |     3 |  28 |
|     29 | 2011-03-29 | 2011 |     3 |  29 |
|     30 | 2011-03-30 | 2011 |     3 |  30 |
|     31 | 2012-03-01 | 2012 |     3 |   1 |
|     32 | 2012-03-02 | 2012 |     3 |   2 |
|     33 | 2012-03-03 | 2012 |     3 |   3 |
|     34 | 2012-03-04 | 2012 |     3 |   4 |
|     35 | 2012-03-05 | 2012 |     3 |   5 |
|     36 | 2012-03-06 | 2012 |     3 |   6 |
|     37 | 2012-03-07 | 2012 |     3 |   7 |
|     38 | 2012-03-08 | 2012 |     3 |   8 |
|     39 | 2012-03-09 | 2012 |     3 |   9 |
|     40 | 2012-03-10 | 2012 |     3 |  10 |
|     41 | 2012-03-11 | 2012 |     3 |  11 |
|     42 | 2012-03-12 | 2012 |     3 |  12 |
|     43 | 2012-03-13 | 2012 |     3 |  13 |
|     44 | 2012-03-14 | 2012 |     3 |  14 |
|     45 | 2012-03-15 | 2012 |     3 |  15 |
|     46 | 2012-03-16 | 2012 |     3 |  16 |
|     47 | 2012-03-17 | 2012 |     3 |  17 |
|     48 | 2012-03-18 | 2012 |     3 |  18 |
|     49 | 2012-03-19 | 2012 |     3 |  19 |
|     50 | 2012-03-20 | 2012 |     3 |  20 |
|     51 | 2012-03-21 | 2012 |     3 |  21 |
|     52 | 2012-03-22 | 2012 |     3 |  22 |
|     53 | 2012-03-23 | 2012 |     3 |  23 |
|     54 | 2012-03-24 | 2012 |     3 |  24 |
|     55 | 2012-03-25 | 2012 |     3 |  25 |
|     56 | 2012-03-26 | 2012 |     3 |  26 |
|     57 | 2012-03-27 | 2012 |     3 |  27 |
|     58 | 2012-03-28 | 2012 |     3 |  28 |
|     59 | 2012-03-29 | 2012 |     3 |  29 |
|     60 | 2012-03-30 | 2012 |     3 |  30 |
+--------+------------+------+-------+-----+
60 rows in set (0.00 sec)
~~~

## Create Store Table

~~~sql
uses stars_sales;

-- NOTE:
--      a state has a set of counties
--      a county has a set of cities

create table Store(
   store_ID int, 
   city text, 
   county text, 
   state text
);
~~~

## Populate Store table

~~~sql
insert into Store(store_ID, city, county, state)
values
(1000, 'Cupertino', 'Santa Clara', 'CA'),
(2000, 'Sunnyvale', 'Santa Clara', 'CA'),
(3000, 'Palo Alto', 'Santa Clara', 'CA'),
(4000, 'San Jose', 'San Mateo', 'CA'),
(5000, 'Redwood City', 'San Mateo', 'CA'),
(6000, 'Foster City', 'San Mateo', 'CA');
~~~

MySQL Execution:

~~~sql
mysql> insert into Store(store_ID, city, county, state)
    -> values
    -> (1000, 'Cupertino', 'Santa Clara', 'CA'),
    -> (2000, 'Sunnyvale', 'Santa Clara', 'CA'),
    -> (3000, 'Palo Alto', 'Santa Clara', 'CA'),
    -> (4000, 'San Jose', 'San Mateo', 'CA'),
    -> (5000, 'Redwood City', 'San Mateo', 'CA'),
    -> (6000, 'Foster City', 'San Mateo', 'CA');
Query OK, 6 rows affected (0.01 sec)
Records: 6  Duplicates: 0  Warnings: 0

mysql> select * from store;
+---------+--------------+-------------+-------+
| store_ID| city         | county      | state |
+---------+--------------+-------------+-------+
|    1000 | Cupertino    | Santa Clara | CA    |
|    2000 | Sunnyvale    | Santa Clara | CA    |
|    3000 | Palo Alto    | Santa Clara | CA    |
|    4000 | San Jose     | San Mateo   | CA    |
|    5000 | Redwood City | San Mateo   | CA    |
|    6000 | Foster City  | San Mateo   | CA    |
+---------+--------------+-------------+-------+
6 rows in set (0.00 sec)
~~~

## Create Item Table

~~~sql
create table  Item(
   item_ID int, 
   category text, 
   color text
);
~~~

## Populate Item Table

~~~sql
insert into Item(item_ID, category, color)
values
(100, 'shirts', 'red'),
(200, 'shirts', 'red'),
(300, 'shirts', 'red'),
(400, 'shirts', 'blue'),
(500, 'shirts', 'blue'),
(600, 'shirts', 'blue'),
(101, 'shoes', 'black'),
(201, 'shoes', 'black'),
(301, 'shoes', 'black'),
(401, 'shoes', 'blue'),
(501, 'shoes', 'blue'),
(601, 'shoes', 'blue'),
(102, 'pants', 'black'),
(202, 'pants', 'black'),
(302, 'pants', 'black'),
(402, 'pants', 'blue'),
(502, 'pants', 'blue'),
(602, 'pants', 'blue'),
(700, 'pc', 'gray'),
(701, 'laptop', 'silver'),
(702, 'laptop', 'blue');
~~~

MySQL Execution:

~~~sql
mysql> insert into Item(item_ID, category, color)
    -> values
    -> (100, 'shirts', 'red'),
    -> (200, 'shirts', 'red'),
    -> (300, 'shirts', 'red'),
    -> (400, 'shirts', 'blue'),
    -> (500, 'shirts', 'blue'),
    -> (600, 'shirts', 'blue'),
    -> (101, 'shoes', 'black'),
    -> (201, 'shoes', 'black'),
    -> (301, 'shoes', 'black'),
    -> (401, 'shoes', 'blue'),
    -> (501, 'shoes', 'blue'),
    -> (601, 'shoes', 'blue'),
    -> (102, 'pants', 'black'),
    -> (202, 'pants', 'black'),
    -> (302, 'pants', 'black'),
    -> (402, 'pants', 'blue'),
    -> (502, 'pants', 'blue'),
    -> (602, 'pants', 'blue'),
    -> (700, 'pc', 'gray'),
    -> (701, 'laptop', 'silver'),
    -> (702, 'laptop', 'blue');
Query OK, 21 rows affected (0.01 sec)
Records: 21  Duplicates: 0  Warnings: 0
~~~

## View Item table:

~~~sql
mysql> select * from Item;
+--------+----------+--------+
| item_ID| category | color  |
+--------+----------+--------+
|    100 | shirts   | red    |
|    200 | shirts   | red    |
|    300 | shirts   | red    |
|    400 | shirts   | blue   |
|    500 | shirts   | blue   |
|    600 | shirts   | blue   |
|    101 | shoes    | black  |
|    201 | shoes    | black  |
|    301 | shoes    | black  |
|    401 | shoes    | blue   |
|    501 | shoes    | blue   |
|    601 | shoes    | blue   |
|    102 | pants    | black  |
|    202 | pants    | black  |
|    302 | pants    | black  |
|    402 | pants    | blue   |
|    502 | pants    | blue   |
|    602 | pants    | blue   |
|    700 | pc       | gray   |
|    701 | laptop   | silver |
|    702 | laptop   | blue   |
+--------+----------+--------+
21 rows in set (0.01 sec)
~~~

## Create DIM table: Customer

~~~sql
create table Customer (
   cust_ID int,
   cname text, 
   gender text,
   age int
);
~~~


## Populate DIM table: Customer

~~~sql
insert into Customer(cust_ID, cname, gender, age)
values
(1, 'alex', 'M', 20),
(2, 'jane', 'F', 23),
(3, 'bob', 'M', 40),
(4, 'betty', 'F', 25),
(5, 'al', 'M', 69),
(6, 'barb', 'F', 75),
(7, 'jim', 'M', 84),
(8, 'ellie', 'F', 85),
(9, 'grant', 'M', 35),
(10, 'janet', 'F', 80),
(11, 'dave', 'M', 44),
(12, 'debra', 'F', 55),
(13, 'farshid', 'M', 50),
(14, 'fay', 'F', 48),
(15, 'dom', 'M', 73),
(16, 'susan', 'F', 25),
(17, 'zal', 'M', 44);
~~~

MySQL Execution:

~~~sql
mysql> insert into Customer(cust_ID, cname, gender, age)
    -> values
    -> (1, 'alex', 'M', 20),
    -> (2, 'jane', 'F', 23),
    -> (3, 'bob', 'M', 40),
    -> (4, 'betty', 'F', 25),
    -> (5, 'al', 'M', 69),
    -> (6, 'barb', 'F', 75),
    -> (7, 'jim', 'M', 84),
    -> (8, 'ellie', 'F', 85),
    -> (9, 'grant', 'M', 35),
    -> (10, 'janet', 'F', 80),
    -> (11, 'dave', 'M', 44),
    -> (12, 'debra', 'F', 55),
    -> (13, 'farshid', 'M', 50),
    -> (14, 'fay', 'F', 48),
    -> (15, 'dom', 'M', 73),
    -> (16, 'susan', 'F', 25),
    -> (17, 'zal', 'M', 44);
Query OK, 17 rows affected (0.00 sec)
Records: 17  Duplicates: 0  Warnings: 0
~~~

## Populate DIM table: Customer

~~~sql
mysql> select * from customer;
+--------+---------+--------+------+
| cust_ID| cname   | gender | age  |
+--------+---------+--------+------+
|      1 | alex    | M      |   20 |
|      2 | jane    | F      |   23 |
|      3 | bob     | M      |   40 |
|      4 | betty   | F      |   25 |
|      5 | al      | M      |   69 |
|      6 | barb    | F      |   75 |
|      7 | jim     | M      |   84 |
|      8 | ellie   | F      |   85 |
|      9 | grant   | M      |   35 |
|     10 | janet   | F      |   80 |
|     11 | dave    | M      |   44 |
|     12 | debra   | F      |   55 |
|     13 | farshid | M      |   50 |
|     14 | fay     | F      |   48 |
|     15 | dom     | M      |   73 |
|     16 | susan   | F      |   25 |
|     17 | zal     | M      |   44 |
+--------+---------+--------+------+
17 rows in set (0.00 sec)
~~~

## FACT Table: Sales

~~~sql
create table Sales(
   store_ID int, -- FK
   item_ID  int, -- FK
   cust_ID  int, -- FK
   date_ID  int, -- FK
   price   double
);
~~~

MySQL Execution:

~~~sql
mysql> create table Sales(
    ->    store_ID int,
    ->    item_ID  int,
    ->    cust_ID  int,
    ->    date_ID  int,
    ->    price   double
    -> );
Query OK, 0 rows affected (0.00 sec)

mysql> desc sales;
+---------+--------+------+-----+---------+-------+
| Field   | Type   | Null | Key | Default | Extra |
+---------+--------+------+-----+---------+-------+
| store_ID| int    | YES  |     | NULL    |       |
| item_ID | int    | YES  |     | NULL    |       |
| cust_ID | int    | YES  |     | NULL    |       |
| date_ID | int    | YES  |     | NULL    |       |
| price   | double | YES  |     | NULL    |       |
+---------+--------+------+-----+---------+-------+
5 rows in set (0.00 sec)
~~~

## Populate  FACT Table: Sales

~~~sql
insert into Sales(store_ID, item_ID, cust_ID, price, date_ID)
values
(2000, 200, 1, 28.00, 1),
(2000, 201, 1, 36.88, 2),
(2000, 301, 1, 22.00, 1),
(1000, 100, 1, 18.60, 2),
(1000, 100, 1, 16.60, 2),
(1000, 101, 1, 12.60, 2),
(1000, 102, 1, 19.60, 5),
(3000, 401, 1, 13.60, 1),
(3000, 102, 1, 15.60, 5),
(4000, 100, 1, 28.60, 6),
(4000, 100, 1, 28.60, 6),
(1000, 100, 1, 26.60, 1),
(1000, 101, 1, 12.60, 7),
(2000, 102, 1, 19.60, 7),
(2000, 100, 1, 13.60, 8),
(3000, 402, 1, 15.60, 9),
(3000, 501, 1, 13.60, 10),
(3000, 500, 1, 15.60, 11),
(2000, 201, 1, 28.00, 12),
(2000, 200, 1, 36.88, 2),
(2000, 300, 1, 22.00, 12),
(1000, 101, 1, 18.60, 2),
(1000, 102, 1, 16.60, 22),
(1000, 100, 1, 12.60, 2),
(1000, 102, 1, 19.60, 5),
(3000, 400, 1, 13.60, 1),
(3000, 102, 1, 15.60, 35),
(4000, 100, 1, 28.60, 36),
(4000, 100, 1, 28.60, 6),
(1000, 101, 1, 26.60, 1),
(1000, 100, 1, 12.60, 7),
(2000, 102, 1, 19.60, 7),
(2000, 100, 1, 13.60, 38),
(3000, 402, 1, 15.60, 49),
(3000, 501, 1, 13.60, 10),
(3000, 500, 1, 15.60, 11),
(1000, 100, 2, 14.60, 45),
(1000, 100, 2, 14.60, 56),
(1000, 102, 2, 55.60, 1),
(1000, 102, 2, 44.60, 5),
(3000, 201, 2, 21.60, 2),
(3000, 201, 2, 43.60, 12),
(4000, 100, 2, 28.60, 45),
(4000, 100, 2, 28.60, 44),
(1000, 100, 2, 26.60, 33),
(1000, 102, 2, 12.60, 2),
(2000, 102, 2, 19.60, 23),
(2000, 100, 2, 53.60, 10),
(3000, 402, 2, 15.60, 40),
(3000, 502, 2, 43.60, 50),
(3000, 500, 2, 15.60, 60),
(4000, 102, 2, 25.60, 2),
(4000, 102, 2, 53.60, 17),
(4000, 501, 2, 55.60, 27),
(2000, 100, 2, 14.60, 15),
(2000, 100, 2, 14.60, 36),
(2000, 102, 2, 55.60, 13),
(3000, 102, 2, 44.60, 51),
(3000, 201, 2, 21.60, 22),
(3000, 201, 2, 43.60, 42),
(4000, 100, 2, 28.60, 45),
(4000, 100, 2, 28.60, 44),
(5000, 100, 2, 26.60, 33),
(5000, 102, 2, 12.60, 20),
(4000, 102, 2, 19.60, 23),
(2000, 100, 2, 53.60, 10),
(3000, 402, 2, 15.60, 40),
(3000, 502, 2, 43.60, 50),
(3000, 500, 2, 15.60, 60),
(1000, 102, 2, 25.60, 29),
(1000, 102, 2, 53.60, 17),
(1000, 501, 2, 55.60, 27),
(1000, 600, 3, 14.60, 1),
(1000, 500, 3, 14.60, 2),
(1000, 401, 3, 55.60, 3),
(1000, 100, 3, 44.60, 4),
(3000, 101, 3, 29.60, 5),
(3000, 102, 3, 43.60, 6),
(4000, 100, 3, 28.60, 7),
(4000, 100, 3, 44.60, 8),
(1000, 100, 3, 26.60, 9),
(1000, 200, 3, 12.60, 10),
(2000, 200, 3, 19.60, 11),
(2000, 100, 3, 33.60, 12),
(3000, 401, 3, 15.60, 13),
(3000, 501, 3, 47.60, 14),
(3000, 500, 3, 15.60, 15),
(4000, 100, 3, 25.60, 16),
(4000, 200, 3, 55.60, 17),
(4000, 501, 3, 15.60, 18),
(2000, 600, 3, 14.60, 11),
(2000, 500, 3, 14.60, 21),
(1000, 401, 3, 55.60, 31),
(1000, 100, 3, 44.60, 41),
(4000, 101, 3, 29.60, 51),
(4000, 102, 3, 43.60, 16),
(4000, 100, 3, 28.60, 17),
(4000, 100, 3, 44.60, 18),
(5000, 100, 3, 26.60, 19),
(5000, 200, 3, 12.60, 20),
(2000, 200, 3, 19.60, 21),
(2000, 100, 3, 33.60, 12),
(3000, 401, 3, 15.60, 13),
(4000, 501, 3, 47.60, 24),
(3000, 500, 3, 15.60, 35),
(4000, 100, 3, 25.60, 46),
(1000, 200, 3, 55.60, 47),
(1000, 501, 3, 15.60, 18),
(2000, 601, 4, 24.60, 3),
(2000, 501, 4, 19.60, 3),
(2000, 402, 4, 51.60, 4),
(5000, 600, 4, 24.60, 5),
(5000, 500, 4, 19.60, 6),
(5000, 401, 4, 51.60, 7),
(1000, 100, 4, 43.60, 8),
(3000, 101, 4, 29.60, 9),
(3000, 102, 4, 43.60, 10),
(4000, 100, 4, 23.60, 3),
(4000, 100, 4, 44.60, 13),
(5000, 100, 4, 26.60, 13),
(5000, 200, 4, 12.60, 16),
(2000, 200, 4, 44.60, 41),
(2000, 100, 4, 33.60, 42),
(3000, 401, 4, 19.60, 45),
(3000, 501, 4, 66.60, 55),
(3000, 500, 4, 15.60, 56),
(4000, 100, 4, 77.60, 57),
(4000, 200, 4, 55.60, 58),
(5000, 501, 4, 15.60, 59),
(5000, 200, 4, 55.60, 60),
(5000, 501, 4, 35.60, 3),
(1000, 601, 4, 24.60, 13),
(1000, 501, 4, 19.60, 33),
(3000, 402, 4, 51.60, 44),
(5000, 600, 4, 24.60, 45),
(4000, 500, 4, 19.60, 26),
(5000, 401, 4, 51.60, 27),
(1000, 100, 4, 43.60, 28),
(3000, 101, 4, 29.60, 29),
(1000, 102, 4, 43.60, 10),
(4000, 100, 4, 23.60, 31),
(4000, 100, 4, 44.60, 13),
(1000, 100, 4, 26.60, 13),
(5000, 200, 4, 12.60, 16),
(2000, 200, 4, 44.60, 51),
(2000, 100, 4, 33.60, 52),
(3000, 401, 4, 19.60, 55),
(3000, 501, 4, 66.60, 55),
(3000, 500, 4, 15.60, 56),
(4000, 100, 4, 77.60, 57),
(4000, 200, 4, 55.60, 58),
(5000, 501, 4, 15.60, 59),
(5000, 200, 4, 55.60, 60),
(5000, 501, 4, 35.60, 32),
(3000, 601, 5, 24.60, 1),
(3000, 501, 5, 19.60, 3),
(3000, 402, 5, 51.60, 2),
(1000, 600, 5, 24.60, 3),
(1000, 500, 5, 19.60, 54),
(1000, 401, 5, 51.60, 55),
(5000, 100, 5, 43.60, 56),
(5000, 101, 5, 29.60, 57),
(4000, 102, 5, 43.60, 3),
(4000, 100, 5, 23.60, 8),
(4000, 100, 5, 44.60, 0),
(2000, 100, 5, 26.60, 9),
(2000, 200, 5, 12.60, 44),
(2000, 200, 5, 44.60, 45),
(2000, 100, 5, 33.60, 44),
(3000, 401, 5, 19.60, 46),
(1000, 501, 5, 66.60, 45),
(1000, 500, 5, 15.60, 16),
(4000, 100, 5, 77.60, 14),
(4000, 200, 5, 55.60, 17),
(5000, 501, 5, 15.60, 13),
(5000, 200, 5, 55.60, 17),
(5000, 501, 5, 35.60, 28),
(4000, 400, 5, 15.60, 29),
(4000, 401, 5, 55.60, 20),
(4000, 301, 5, 35.60, 21),
(1000, 601, 5, 24.60, 11),
(1000, 501, 5, 19.60, 33),
(3000, 402, 5, 51.60, 32),
(2000, 600, 5, 24.60, 33),
(2000, 500, 5, 19.60, 44),
(2000, 401, 5, 51.60, 45),
(3000, 100, 5, 43.60, 56),
(3000, 101, 5, 29.60, 57),
(3000, 102, 5, 43.60, 23),
(1000, 100, 5, 23.60, 28),
(1000, 100, 5, 44.60, 60),
(1000, 100, 5, 26.60, 49),
(2000, 200, 5, 12.60, 44),
(2000, 200, 5, 44.60, 45),
(2000, 100, 5, 33.60, 44),
(3000, 401, 5, 19.60, 46),
(5000, 501, 5, 66.60, 45),
(5000, 500, 5, 15.60, 46),
(4000, 100, 5, 77.60, 44),
(4000, 200, 5, 55.60, 47),
(5000, 501, 5, 15.60, 43),
(5000, 200, 5, 55.60, 37),
(5000, 501, 5, 35.60, 38),
(4000, 400, 5, 15.60, 39),
(4000, 401, 5, 55.60, 30),
(4000, 301, 5, 35.60, 31),
(4000, 601, 6, 24.00, 1),
(4000, 501, 6, 19.00, 2),
(4000, 402, 6, 51.00, 3),
(4000, 600, 6, 24.00, 4),
(1000, 500, 6, 19.60, 5),
(1000, 401, 6, 51.60, 6),
(1000, 100, 6, 48.00, 7),
(1000, 101, 6, 19.00, 8),
(4000, 102, 6, 33.00, 9),
(4000, 100, 6, 63.00, 10),
(4000, 100, 6, 44.60, 11),
(2000, 100, 6, 26.60, 21),
(2000, 200, 6, 12.60, 12),
(2000, 200, 6, 44.60, 31),
(2000, 100, 6, 33.60, 14),
(3000, 401, 6, 19.60, 51),
(1000, 501, 6, 66.60, 16),
(1000, 500, 6, 15.60, 11),
(4000, 100, 6, 77.60, 32),
(4000, 200, 6, 55.60, 33),
(5000, 501, 6, 15.60, 34),
(3000, 200, 6, 55.60, 35),
(3000, 501, 6, 35.60, 36),
(3000, 400, 6, 15.60, 47),
(3000, 401, 6, 55.60, 48),
(3000, 301, 6, 35.60, 49),
(1000, 101, 6, 15.60, 4),
(2000, 201, 6, 55.60, 54),
(3000, 301, 6, 35.60, 55),
(4000, 402, 6, 15.60, 55),
(4000, 502, 6, 55.60, 56),
(5000, 602, 6, 35.60, 53),
(1000, 601, 6, 24.00, 41),
(1000, 501, 6, 19.00, 42),
(1000, 402, 6, 51.00, 43),
(1000, 600, 6, 24.00, 44),
(2000, 500, 6, 19.60, 45),
(2000, 401, 6, 51.60, 46),
(2000, 100, 6, 48.00, 47),
(2000, 101, 6, 19.00, 48),
(3000, 102, 6, 33.00, 49),
(5000, 100, 6, 63.00, 50),
(6000, 100, 6, 44.60, 51),
(6000, 100, 6, 26.60, 51),
(2000, 200, 6, 12.60, 52),
(2000, 200, 6, 44.60, 51),
(2000, 100, 6, 33.60, 54),
(3000, 401, 6, 19.60, 51),
(1000, 501, 6, 66.60, 60),
(1000, 500, 6, 15.60, 11),
(4000, 100, 6, 77.60, 42),
(4000, 200, 6, 55.60, 43),
(5000, 501, 6, 15.60, 44),
(3000, 200, 6, 55.60, 35),
(3000, 501, 6, 35.60, 36),
(3000, 400, 6, 15.60, 47),
(3000, 401, 6, 55.60, 48),
(3000, 301, 6, 35.60, 49),
(1000, 101, 6, 15.60, 4),
(2000, 201, 6, 55.60, 14),
(3000, 301, 6, 35.60, 15),
(4000, 402, 6, 15.60, 15),
(4000, 502, 6, 55.60, 16),
(5000, 602, 6, 35.60, 13),
(5000, 601, 7, 24.00, 1),
(5000, 501, 7, 19.00, 2),
(5000, 402, 7, 51.00, 3),
(5000, 600, 7, 24.00, 4),
(3000, 500, 7, 19.60, 15),
(3000, 401, 7, 51.60, 16),
(1000, 100, 7, 48.00, 27),
(1000, 101, 7, 19.00, 28),
(4000, 102, 7, 33.00, 39),
(4000, 101, 7, 63.00, 42),
(4000, 102, 7, 44.60, 44),
(3000, 100, 7, 26.60, 56),
(3000, 200, 7, 12.60, 18),
(3000, 200, 7, 44.60, 14),
(3000, 100, 7, 33.60, 1),
(3000, 400, 7, 19.60, 11),
(3000, 500, 7, 66.60, 21),
(2000, 500, 7, 15.60, 31),
(2000, 100, 7, 77.60, 41),
(2000, 200, 7, 55.60, 51),
(5000, 501, 7, 15.60, 59),
(3000, 200, 7, 55.60, 60),
(3000, 501, 7, 35.60, 10),
(3000, 400, 7, 15.60, 40),
(3000, 401, 7, 55.60, 30),
(3000, 301, 7, 35.60, 40),
(1000, 101, 7, 15.60, 5),
(2000, 201, 7, 55.60, 6),
(3000, 301, 7, 35.60, 35),
(4000, 402, 7, 15.60, 31),
(4000, 501, 7, 55.60, 30),
(5000, 601, 7, 35.60, 33),
(2000, 601, 7, 24.00, 11),
(2000, 501, 7, 19.00, 12),
(2000, 402, 7, 51.00, 13),
(2000, 600, 7, 24.00, 14),
(2000, 500, 7, 19.60, 15),
(4000, 401, 7, 51.60, 16),
(1000, 100, 7, 48.00, 27),
(1000, 101, 7, 19.00, 28),
(4000, 102, 7, 33.00, 39),
(2000, 101, 7, 63.00, 42),
(2000, 102, 7, 44.60, 44),
(2000, 100, 7, 26.60, 56),
(3000, 200, 7, 12.60, 18),
(3000, 200, 7, 44.60, 14),
(3000, 100, 7, 33.60, 11),
(3000, 400, 7, 19.60, 11),
(3000, 500, 7, 66.60, 21),
(4000, 500, 7, 15.60, 31),
(4000, 100, 7, 77.60, 41),
(4000, 200, 7, 55.60, 51),
(4000, 501, 7, 15.60, 59),
(3000, 200, 7, 55.60, 60),
(3000, 501, 7, 35.60, 10),
(3000, 400, 7, 15.60, 40),
(3000, 401, 7, 55.60, 30),
(3000, 301, 7, 35.60, 40),
(1000, 101, 7, 15.60, 15),
(2000, 201, 7, 55.60, 16),
(2000, 301, 7, 35.60, 35),
(4000, 402, 7, 15.60, 31),
(2000, 501, 7, 55.60, 30),
(1000, 601, 7, 35.60, 33),
(5000, 101, 8, 24.00, 1),
(5000, 201, 8, 19.00, 11),
(5000, 302, 8, 51.00, 11),
(5000, 601, 8, 24.00, 21),
(3000, 501, 8, 19.60, 41),
(3000, 402, 8, 51.60, 22),
(1000, 101, 8, 48.00, 32),
(1000, 100, 8, 19.00, 42),
(4000, 100, 8, 33.00, 52),
(4000, 100, 8, 63.00, 40),
(4000, 101, 8, 44.60, 40),
(3000, 101, 8, 26.60, 41),
(3000, 202, 8, 12.60, 42),
(2000, 201, 8, 44.60, 58),
(2000, 100, 8, 33.60, 59),
(2000, 400, 8, 19.60, 47),
(3000, 500, 8, 66.60, 60),
(2000, 500, 8, 15.60, 60),
(2000, 100, 8, 77.60, 60),
(2000, 200, 8, 55.60, 60),
(5000, 501, 8, 15.60, 60),
(4000, 200, 8, 55.60, 17),
(4000, 501, 8, 35.60, 27),
(4000, 400, 8, 15.60, 27),
(3000, 401, 8, 55.60, 27),
(3000, 301, 8, 35.60, 27),
(1000, 101, 8, 15.60, 18),
(2000, 201, 8, 55.60, 18),
(3000, 301, 8, 35.60, 18),
(4000, 402, 8, 15.60, 39),
(4000, 501, 8, 55.60, 39),
(5000, 601, 8, 35.60, 39),
(1000, 101, 8, 24.00, 41),
(1000, 201, 8, 19.00, 51),
(1000, 302, 8, 51.00, 51),
(2000, 601, 8, 24.00, 41),
(2000, 501, 8, 19.60, 51),
(2000, 402, 8, 51.60, 42),
(3000, 101, 8, 48.00, 32),
(3000, 100, 8, 19.00, 42),
(3000, 100, 8, 33.00, 52),
(3000, 100, 8, 63.00, 40),
(3000, 101, 8, 44.60, 40),
(3000, 101, 8, 26.60, 41),
(3000, 202, 8, 12.60, 42),
(2000, 201, 8, 44.60, 58),
(2000, 100, 8, 33.60, 59),
(2000, 400, 8, 19.60, 47),
(1000, 500, 8, 66.60, 50),
(1000, 500, 8, 15.60, 50),
(2000, 100, 8, 77.60, 40),
(2000, 200, 8, 55.60, 30),
(5000, 501, 8, 15.60, 30),
(4000, 200, 8, 55.60, 27),
(4000, 501, 8, 35.60, 27),
(4000, 400, 8, 15.60, 47),
(3000, 401, 8, 55.60, 57),
(3000, 301, 8, 35.60, 27),
(1000, 101, 8, 15.60, 18),
(2000, 201, 8, 55.60, 18),
(3000, 301, 8, 35.60, 18),
(4000, 402, 8, 15.60, 39),
(4000, 501, 8, 55.60, 39),
(5000, 601, 8, 35.60, 39);
~~~

## View FACT Table: Sales

~~~sql
mysql> select count(*) from sales;
+----------+
| count(*) |
+----------+
|      398 |
+----------+
1 row in set (0.01 sec)

mysql> select * from sales limit 5;
+---------+--------+--------+--------+-------+
|store_ID |item_ID |cust_ID |date_ID | price |
+---------+--------+--------+--------+-------+
|    2000 |    200 |      1 |      1 |    28 |
|    2000 |    201 |      1 |      2 | 36.88 |
|    2000 |    301 |      1 |      1 |    22 |
|    1000 |    100 |      1 |      2 |  18.6 |
|    1000 |    100 |      1 |      2 |  16.6 |
+---------+--------+--------+--------+-------+
5 rows in set (0.00 sec)
~~~

## Star Schema Tables

~~~sql
mysql> use stars_sales;

Database changed
mysql> show tables;
+-----------------------+
| Tables_in_stars_sales |
+-----------------------+
| Customer              |
| dates                 |
| Item                  |
| Sales                 |
| Store                 |
+-----------------------+
5 rows in set (0.00 sec)
~~~

## Date Table has 2 years of data:

~~~sql
mysql> 
        select d.year, sum(s.price) 
        from dates d, 
             sales s 
        where s.dateid = d.dateid 
        group by d.year;
+------+-------------------+
| year | sum(s.price)      |
+------+-------------------+
| 2011 | 6551.760000000012 |
| 2012 | 6969.800000000017 |
+------+-------------------+
2 rows in set (0.00 sec)
~~~

# OLAP Operations: using Star Schema

## Full Star Join

	❖ An example of how to find the **full star**
	 join (or complete star join) among 5 tables 
	 (i.e., fact table + all 4 of its dimensions) 
	 in a Star Schema:
	
	 – Join on the foreign keys
	
	❖ If we join fewer than all dimensions, 
	then we have a star join.

	❖ In general, OLAP queries can be answered by 
	computing some or all of the star join, then by 
	filtering, and then by aggregating.

~~~sql
SELECT *
   FROM 
        Sales F,      -- Fact table
        Store S,      -- DIM
        Item I,       -- DIM
        Customer C,   -- DIM
        Dates D       -- DIM
      WHERE 
            F.store_ID = S.store_ID and
            F.item_ID = I.item_ID   and
            F.cust_ID = C.cust_ID   and
            F.date_ID = D.date_ID;
~~~

# OLAP Queries – Roll-up

	❖ Roll-up allows you to summarize data by:
		– changing the level of granularity of 
		  a particular dimension
		– dimension reduction
		
## OLAP Queries – Roll-up
## Roll-up Example 1 (Hierarchy)

### Roll-up Example-1:

~~~sql
SELECT store_ID, 
       item_ID, 
       cust_ID, 
       date_ID, 
       SUM(price)
FROM 
    Sales 
GROUP BY 
    store_ID, item_ID, cust_ID, date_ID;
~~~

### Roll-up Example-2:

~~~sql
SELECT county, 
       item_ID, 
       cust_ID, 
       SUM(price)
FROM 
     Sales F, 
     Store S
WHERE 
     F.storeID = S.storeID
GROUP BY 
     county, item_ID, cust_ID;
~~~

### Roll-up Example-3:

~~~sql
SELECT county, 
       item_ID, 
       gender,
       SUM(price)
FROM 
      Sales F, 
      Store S, 
      Customer C
WHERE 
      F.store_ID = S.store_ID and
      F.cust_ID = C.cust_ID
GROUP BY 
      county, item_ID, gender;
~~~


### Roll-up Example 4 (Dimension)

~~~sql
SELECT county, 
       item_ID, 
       SUM(price)
FROM 
     Sales F, 
     Store S
WHERE 
     F.store_ID = S.store_ID
GROUP BY 
     county, item_ID;
~~~

		The following are 3 complex OLAP queries 
		for your star schema that include joins, 
		ranking functions with partitions, and subqueries:

---

### Roll-up Example 5: **Top 3 Stores by Sales in Each State**

	This query ranks stores within each 
	state based on  total  sales  and 
	retrieves the top 3 for each state.
	
```sql
WITH StoreSales AS (
    SELECT s.state, 
           f.store_ID, 
           SUM(f.price) AS total_sales
    FROM Sales f
    JOIN Store s ON f.store_ID = s.store_ID
    GROUP BY 
         s.state, f.store_ID
)
SELECT state, 
       store_ID, 
       total_sales, 
       RANK() OVER (PARTITION BY state ORDER BY total_sales DESC) AS rnk
FROM 
    StoreSales
WHERE 
    rnk <= 3;
```

---

### Roll-up Example 6: **Customers with Sales Greater Than the Average in Their Gender Group**

	This query identifies customers whose total sales 
	exceed the average sales for their gender group, 
	using subqueries and partitions.

```sql
WITH CustomerSales AS (
    SELECT c.cust_ID, 
           c.gender, 
           SUM(f.price) AS total_sales
    FROM 
         Sales f
    JOIN Customer c ON f.cust_ID = c.cust_ID
    GROUP BY 
         c.cust_ID, c.gender
),
GenderAverage AS (
    SELECT gender, 
           AVG(total_sales) AS avg_sales
    FROM CustomerSales
    GROUP BY gender
)
SELECT cs.cust_ID, 
       cs.gender, 
       cs.total_sales
FROM 
     CustomerSales cs
JOIN GenderAverage ga ON cs.gender = ga.gender
WHERE 
     cs.total_sales > ga.avg_sales;
```

---

### Roll-up Example 7: **Top-Selling Category by Month**

	This query finds the top-selling item 
	category for each month using ranking 
	functions and partitions.
	
```sql
WITH MonthlySales AS (
    SELECT d.year, 
           d.month, 
           i.category, 
           SUM(f.price) AS total_sales
    FROM Sales f
    JOIN Dates d ON f.date_ID = d.date_ID
    JOIN Item i ON f.item_ID = i.item_ID
    GROUP BY 
         d.year, d.month, i.category
)
, 
RankedSales AS
 (
    SELECT year, month, category, total_sales, 
    RANK() OVER (PARTITION BY year, month ORDER BY total_sales DESC) 
      AS rnk
    FROM MonthlySales
)
SELECT year, month, category, total_sales
FROM RankedSales
WHERE rnk = 1;
```

---

## OLAP Queries – Drill-Down

	❖ Drill-down: reverse of roll-up
	– From higher level summary to 
	  lower level summary 
	  (i.e., we want more detailed data)

	– Introducing new dimensions
	
### Drill-down Example 1 (Hierarchy)

	❖ Use Drill-down on total sales by item and
	gender for each county to find total sales by
	item and gender for each city.

~~~sql	
-- by county
SELECT county, 
       item_ID, 
       gender,
       SUM(price)
FROM Sales F, 
     Store S, 
     Customer C
WHERE 
     F.store_ID = S.store_ID AND
     F.cust_ID = C.cust_ID
GROUP BY 
     county, item_ID, gender;
~~~

~~~sql
-- by city
SELECT city, 
       item_ID, 
       gender,
       SUM(price)
FROM Sales F, 
     Store S, 
     Customer C
WHERE 
     F.store_ID = S.store_ID AND
     F.cust_ID = C.cust_ID
GROUP BY 
     city, item_ID, gender;
~~~

### Drill-down Example 2 (Dimension)

	❖ Use Drill-down on total sales by item and
	county to find total sales by item and gender 
	for each county. 
	
~~~sql
SELECT county, 
       item_ID, 
       SUM(price)
FROM 
      Sales F, 
      Store S
WHERE 
      F.store_ID = S.store_ID
GROUP BY 
      county, item_ID;
~~~

~~~sql
SELECT county, 
       item_ID, 
       gender,
       SUM(price)
FROM 
     Sales F, 
     Store S, 
     Customer C
WHERE 
     F.store_ID = S.store_ID AND
     F.cust_ID = C.cust_ID
GROUP BY 
     county, item_ID, gender;
~~~

### Here are three complex **roll-down** OLAP queries for the given star schema using MySQL. These queries involve joins, ranking functions with partitions, and subqueries, all focused on breaking down data to more granular levels:

	These queries roll data down to finer details, 
	like breaking state-level sales into store-level, 
	age-based grouping for customer analysis, or 
	category-based daily sales. 
---

### Drill-down Example 3: **Monthly Sales by Store within a State**

	This query breaks down total sales by store, 
	grouped within each state, and provides the 
	ranking of stores by sales within their 
	respective states.
	
```sql
WITH StoreMonthlySales AS (
    SELECT s.state, 
           s.store_ID, 
           d.year,
           d.month,  
           SUM(f.price) AS total_sales
    FROM Sales f
    JOIN Store s ON f.store_ID = s.store_ID
    JOIN Dates d ON f.date_ID = d.date_ID
    GROUP BY s.state, s.store_ID, d.year, d.month
)
SELECT state, 
       store_ID, 
       year, 
       month, 
       total_sales,
       RANK() OVER (PARTITION BY state ORDER BY total_sales DESC) 
         AS rank_within_state
FROM StoreMonthlySales;
```

---

### Drill-down Example 4: **Customer Sales by Age Group**

	This query identifies customer sales 
	broken down by age group, ranked by 
	total sales within each group.
	
```sql
WITH CustomerSales AS (
    SELECT c.cust_ID, 
           c.age, 
           FLOOR(c.age / 10) * 10 AS age_group, 
           SUM(f.price) AS total_sales
    FROM Sales f
    JOIN Customer c ON f.cust_ID = c.cust_ID
    GROUP BY 
         c.cust_ID, c.age
)
SELECT age_group, 
       cust_ID, 
       total_sales,
       RANK() OVER (PARTITION BY age_group ORDER BY total_sales DESC) 
         AS rank_within_age_group
FROM 
     CustomerSales;
```

---

### Drill-down Example 5: **Sales by Category for Each Day**

	This query breaks down total sales by 
	item category for each day, showing 
	the ranking of categories within each day.
	
```sql
WITH DailyCategorySales AS (
    SELECT d.date, 
           i.category, 
           SUM(f.price) AS total_sales
    FROM Sales f
    JOIN Dates d ON f.date_ID = d.date_ID
    JOIN Item i ON f.item_ID = i.item_ID
    GROUP BY 
         d.date, i.category
)
SELECT date, 
       category, 
       total_sales,
       RANK() OVER (PARTITION BY date ORDER BY total_sales DESC) 
         AS rank_within_date
FROM DailyCategorySales;
```

---


## OLAP Queries – Slicing

	❖ The slice operation produces a slice 
	of the cube by picking a specific value 
	for one of the dimensions.
	
	❖ To start our example, let’s specify:
	– Total sales by item and gender for each county

~~~sql	
SELECT county, 
       item_ID, 
       gender, 
       SUM(price)
FROM 
    Sales F, 
    Store S, 
    Customer C
WHERE 
      F.store_ID = S.store_ID AND
      F.cust_ID = C.cust_ID
GROUP BY 
      county, item_ID, gender;	
~~~


### Slicing Example 1

	❖ Use Slicing on total sales by item and gender 
	for each county to find total sales by item and 
	gender for Santa Clara county.

~~~sql	
-- NO Slicing	
SELECT county, 
       item_ID, 
       gender,
       SUM(price)
FROM 
     Sales F, 
     Store S, 
     Customer C
WHERE 
      F.store_ID = S.store_ID AND
      F.cust_ID = C.cust_ID
GROUP BY 
     county, item_ID, gender;
~~~


~~~sql	
-- Proper Slicing	
SELECT item_ID, 
       gender, 
       SUM(price)
FROM 
      Sales F, 
      Store S, 
      Customer C
WHERE 
      F.store_ID = S.store_ID AND
      F.cust_ID = C.cust_ID AND
      S.county = 'Santa Clara'    <--- SLICING
GROUP BY 
      itemID, 
      gender;
~~~

### Slicing Example 2
	❖ Use Slicing on total sales by item and gender 
	for each county to find total sales by gender and 
	county for "shirts".

~~~sql
-- NO Slicing
SELECT county, itemID, gender,
SUM(price)
FROM Sales F, Store S, Customer C
WHERE F.storeID = S.storeID AND
      F.custID = C.custID
GROUP BY county, itemID, gender;
~~~

~~~sql
-- Proper Slicing	
SELECT county, gender, SUM(price)
FROM Sales F, Store S, Customer C, Item I
WHERE F.storeID = S.storeID AND
      F.custID = C.custID AND
      F.itemID = I.itemID AND
      category = 'shirts'     <--- SLICING
GROUP BY county, gender;
~~~	


### Here are three complex **slice** OLAP queries for the given star schema. Each query focuses on selecting specific slices of data using joins, ranking functions with partitions, and subqueries:

### Each query slices the data to focus on specific conditions while incorporating advanced SQL features like joins, subqueries, and ranking within partitions. 
---

### Slicing Example 3: **Sales for Electronics in California**

	This query slices data to show sales 
	for items in the "Electronics" category 
	within California.
	
```sql
SELECT f.store_ID, 
       f.item_ID, 
       f.price, 
       s.state, 
       i.category
FROM Sales f
JOIN Store s ON f.store_ID = s.store_ID
JOIN Item i ON f.item_ID = i.item_ID
WHERE 
     s.state = 'California' AND 
     i.category = 'Electronics';
```

---

### Slicing Example 4: **Customers with Top Sales in a Specific Age Group**

	This query slices data for customers in a 
	particular age group (e.g., 20–30 years) 
	and ranks them by total sales within that group.
	
```sql
WITH CustomerSales AS (
    SELECT 
           c.cust_ID, 
           c.age, 
           SUM(f.price) AS total_sales
    FROM Sales f
    JOIN Customer c ON f.cust_ID = c.cust_ID
    WHERE 
         c.age BETWEEN 20 AND 30
    GROUP BY 
         c.cust_ID, c.age
)
SELECT cust_ID, 
       age, 
       total_sales,
       RANK() OVER (PARTITION BY FLOOR(age / 10) * 10 
                    ORDER BY total_sales DESC) 
         AS rank_within_age_group
FROM CustomerSales;
```

---

### Slicing Example 5: **Daily Sales for a Specific Category**

	This query slices data for daily sales 
	in a specific item category, like 
	"Furniture," for detailed analysis.
	
```sql
WITH DailyCategorySales AS (
    SELECT d.date, 
           i.category, 
           SUM(f.price) AS total_sales
    FROM Sales f
    JOIN Dates d ON f.date_ID = d.date_ID
    JOIN Item i ON f.item_ID = i.item_ID
    WHERE 
         i.category = 'Furniture'
    GROUP BY 
         d.date, i.category
)
SELECT date, category, total_sales,
       RANK() OVER (PARTITION BY date ORDER BY total_sales DESC) 
         AS rank_within_date
FROM DailyCategorySales;
```

---



## OLAP Queries – Dicing

	❖ The dice operation produces a sub-cube by
	picking specific values for multiple dimensions.

	❖ To start our example, let’s specify:
	– Total sales by gender, item, and city

~~~sql	
SELECT city, itemID, gender, SUM(price)
FROM Sales F, Store S, Customer C
WHERE F.storeID = S.storeID AND
      F.custID = C.custID
GROUP BY city, itemID, gender;	
~~~

~~~sql
SELECT category, city, gender, SUM(price)
FROM Sales F, Store S, Customer C, Item I
WHERE F.storeID = S.storeID AND
F.custID = C.custID AND
F.itemID = I.itemID AND
color = 'red' AND state = 'CA'
GROUP BY category, city, gender;
~~~


Here are three complex **dicing** OLAP queries for the given star schema. These queries focus on analyzing subsets of data using multiple dimensions and incorporate joins, ranking functions with partitions, and subqueries:

---

### Query 1: **Sales by Category and Gender in California and New York**
This query dices the data by filtering for specific states (California and New York) and analyzes sales by category and customer gender.
```sql
SELECT s.state, i.category, c.gender, SUM(f.price) AS total_sales
FROM Sales f
JOIN Store s ON f.store_ID = s.store_ID
JOIN Item i ON f.item_ID = i.item_ID
JOIN Customer c ON f.cust_ID = c.cust_ID
WHERE s.state IN ('California', 'New York')
GROUP BY s.state, i.category, c.gender;
```

---

### Query 2: **Top-Selling Items in Specific Cities for a Given Age Range**
This query dices data to focus on sales in specific cities (e.g., San Francisco and Los Angeles) for customers aged 20–40, ranking the top-selling items.
```sql
WITH CityItemSales AS (
    SELECT s.city, i.item_ID, i.category, SUM(f.price) AS total_sales
    FROM Sales f
    JOIN Store s ON f.store_ID = s.store_ID
    JOIN Item i ON f.item_ID = i.item_ID
    JOIN Customer c ON f.cust_ID = c.cust_ID
    WHERE s.city IN ('San Francisco', 'Los Angeles') AND c.age BETWEEN 20 AND 40
    GROUP BY s.city, i.item_ID, i.category
)
SELECT city, item_ID, category, total_sales,
       RANK() OVER (PARTITION BY city ORDER BY total_sales DESC) AS rank_within_city
FROM CityItemSales
WHERE rank_within_city <= 5;
```

---

### Query 3: **Monthly Sales by Color and Age Group**
This query dices the data by filtering on item color and customer age groups, then ranks total sales by color within each month.
```sql
WITH MonthlyColorSales AS (
    SELECT d.month, d.year, i.color, FLOOR(c.age / 10) * 10 AS age_group, SUM(f.price) AS total_sales
    FROM Sales f
    JOIN Dates d ON f.date_ID = d.date_ID
    JOIN Item i ON f.item_ID = i.item_ID
    JOIN Customer c ON f.cust_ID = c.cust_ID
    WHERE i.color IN ('Red', 'Blue', 'Green')
    GROUP BY d.year, d.month, i.color, age_group
)
SELECT year, month, color, age_group, total_sales,
       RANK() OVER (PARTITION BY year, month, color ORDER BY total_sales DESC) AS rank_within_color_month
FROM MonthlyColorSales
WHERE rank_within_color_month <= 3;
```

---

Each query dices the data by using multiple filtering conditions and focuses on specific subsets of the star schema, combining advanced SQL techniques to provide insightful analyses. Let me know if you’d like further explanation or adjustments!



## Pivot Operation

* Here are three complex **pivot** OLAP queries designed for the
star schema. 

* These queries pivot data for insightful cross-dimensional analysis, incorporating joins, ranking functions with partitions, and subqueries:

* These queries pivot data to provide a multi-dimensional view of sales while incorporating advanced SQL features for better analysis. 

---

### Query 1: **Pivot Sales by Gender and Category**

	This query creates a pivot table showing 
	total sales by gender and item category.

```sql
SELECT 
    c.gender AS gender,
    SUM(CASE WHEN i.category = 'Electronics' THEN f.price ELSE 0 END) AS Electronics_Sales,
    SUM(CASE WHEN i.category = 'Clothing' THEN f.price ELSE 0 END) AS Clothing_Sales,
    SUM(CASE WHEN i.category = 'Furniture' THEN f.price ELSE 0 END) AS Furniture_Sales
FROM 
    Sales f
JOIN Customer c ON f.cust_ID = c.cust_ID
JOIN Item i ON f.item_ID = i.item_ID
GROUP BY 
     c.gender;
```

---

### Query 2: **Pivot Monthly Sales for Each Category**

	This query pivots sales data to show the 
	total sales for each item category across 
	different months.

```sql
SELECT 
    d.month AS month,
    SUM(CASE WHEN i.category = 'Electronics' THEN f.price ELSE 0 END) AS Electronics_Sales,
    SUM(CASE WHEN i.category = 'Clothing' THEN f.price ELSE 0 END) AS Clothing_Sales,
    SUM(CASE WHEN i.category = 'Furniture' THEN f.price ELSE 0 END) AS Furniture_Sales
FROM 
    Sales f
JOIN Dates d ON f.date_ID = d.date_ID
JOIN Item i ON f.item_ID = i.item_ID
GROUP BY 
     d.month
ORDER BY 
     d.month;
```

---

### Query 3: **Pivot Top Sales by State and Category**

	This query pivots the data to display the 
	top-selling category for each state by 
	ranking sales within each state and category.

```sql
WITH StateCategorySales AS (
    SELECT s.state, 
           i.category, 
           SUM(f.price) AS total_sales
    FROM Sales f
    JOIN Store s ON f.store_ID = s.store_ID
    JOIN Item i ON f.item_ID = i.item_ID
    GROUP BY 
         s.state, i.category
),
RankedSales AS (
    SELECT state, category, total_sales,
           RANK() OVER (PARTITION BY state ORDER BY total_sales DESC) 
             AS rank_within_state
    FROM StateCategorySales
)
SELECT state, category, total_sales
FROM RankedSales
WHERE rank_within_state = 1;
```

---

