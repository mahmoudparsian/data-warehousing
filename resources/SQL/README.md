# SQL: Structured Query Language

<img src="./sql_image.jpeg" alt="sql" width="400" height="270">

		Structured Query Language (SQL) is 
		a programming language for storing 
		and  processing  information  in a 
		relational database.

1. [The SQL Tutorial for Data Analysis](https://mode.com/sql-tutorial/introduction-to-sql)

2. [Introduction to SQL by Larry Snyder](./introduction_to_SQL_by_Larry_Snyder.pdf)

3. [Introduction to SQL by Phil Spector](./introduction_to_SQL_by_Phil_Spector.pdf)

4. [SQL for DW by Michael Bohlen (slides: 65 pages)](./sql_for_DW_by_Michael_Bohlen_slides_65_pages.pdf)

5. [SQL Joins 101](./SQL_Joins_101.pdf)

6. [DuckDB SQL documentation](https://duckdb.org/docs/sql/introduction)

---------

# Surrogate Keys

1. [Surrogate Keys in Data Warehouse Pros and Cons](./Surrogate_Keys_in_Data_Warehouse_Pros_and_Cons.pdf)

2. [Surrogate Key in SQL – Definition and Examples](https://blog.devart.com/surrogate-key-in-sql.html#:~:text=A%20surrogate%20key%20is%20defined,object%20generates%20this%20key%20itself.)

3. [When (and How) to Use Surrogate Keys](https://www.sisense.com/blog/when-and-how-to-use-surrogate-keys/)

## Surrogate Keys Example

* In this example, we create a dimension table 
for a date (`DATE`) column.

* We use MySQL's `UNIX_TIMESTAMP()` function to 
  create unique Surrogate Keys as integers.

~~~sql
-- using UNIX_TIMESTAMP() function

-- ------------------------------------
-- Create a dimension table for a date
-- date_id : a Surrogate Key
-- ------------------------------------
create table dim_dates_table (
   date_id int(11) NOT NULL, 
   date Date NOT NULL,
   year int(11) NOT NULL,
   month int(11) NOT NULL,
   day int(11) NOT NULL,
   primary key (date_id)
);

-- ---------------------------------
-- Create a Stored Procedure to fill 
-- the table with Surrogate Keys
-- ----------------------------------
DROP PROCEDURE IF EXISTS fill_dates_with_UNIX_TIMESTAMP;

DELIMITER |
CREATE PROCEDURE fill_dates_with_UNIX_TIMESTAMP(dateStart DATE, dateEnd DATE)
BEGIN
  WHILE dateStart <= dateEnd DO
    INSERT INTO dim_dates_table(date_id, date, year, month, day) 
      VALUES (UNIX_TIMESTAMP(dateStart),
              dateStart, 
              SUBSTRING_INDEX(dateStart, '-', 1),
              SUBSTRING_INDEX(SUBSTRING_INDEX(dateStart,'-', 2), '-',-1),
              SUBSTRING_INDEX(dateStart, '-', -1)
      );
    SET dateStart = date_add(dateStart, INTERVAL 1 DAY);
  END WHILE;
END;
|
DELIMITER ;



mysql> CALL fill_dates_with_UNIX_TIMESTAMP('2011-01-25','2011-02-10');
Query OK, 1 row affected (0.01 sec)

mysql> select * from dim_dates_table;
+------------+------------+------+-------+-----+
| date_id    | date       | year | month | day |
+------------+------------+------+-------+-----+
| 1295942400 | 2011-01-25 | 2011 |     1 |  25 |
| 1296028800 | 2011-01-26 | 2011 |     1 |  26 |
| 1296115200 | 2011-01-27 | 2011 |     1 |  27 |
| 1296201600 | 2011-01-28 | 2011 |     1 |  28 |
| 1296288000 | 2011-01-29 | 2011 |     1 |  29 |
| 1296374400 | 2011-01-30 | 2011 |     1 |  30 |
| 1296460800 | 2011-01-31 | 2011 |     1 |  31 |
| 1296547200 | 2011-02-01 | 2011 |     2 |   1 |
| 1296633600 | 2011-02-02 | 2011 |     2 |   2 |
| 1296720000 | 2011-02-03 | 2011 |     2 |   3 |
| 1296806400 | 2011-02-04 | 2011 |     2 |   4 |
| 1296892800 | 2011-02-05 | 2011 |     2 |   5 |
| 1296979200 | 2011-02-06 | 2011 |     2 |   6 |
| 1297065600 | 2011-02-07 | 2011 |     2 |   7 |
| 1297152000 | 2011-02-08 | 2011 |     2 |   8 |
| 1297238400 | 2011-02-09 | 2011 |     2 |   9 |
| 1297324800 | 2011-02-10 | 2011 |     2 |  10 |
| 1706153631 | 2011-01-25 | 2011 |     1 |  25 |
+------------+------------+------+-------+-----+
18 rows in set (0.00 sec)

~~~