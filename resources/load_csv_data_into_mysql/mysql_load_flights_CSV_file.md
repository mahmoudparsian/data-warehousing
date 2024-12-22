# Load CSV Data into MySQL

Data:  flights-small.with.header.csv

Number of records for flight data: 1,148,675

# Method-1: Load Data using  MySQL workbench

* Using MySQL workbench, Right click on database name, 
  then use import wizard

* Performance: VERY SLOW

# Method-2: Load Data using Command Line

* Performance: VERY FAST

```sql
create database homeworks;

use homeworks;

create table FLIGHTS
        (fid int, 
         year int, 
         month_id int, 
         day_of_month int, 
         day_of_week_id int, 
         carrier_id varchar(3), 
         flight_num int,
         origin_city varchar(34), 
         origin_state varchar(47), 
         dest_city varchar(34), 
         dest_state varchar(46), 
         departure_delay double, 
         taxi_out double, 
         arrival_delay double,
         canceled int, 
         actual_time double, 
         distance double, 
         capacity int, 
         price double);
```
## Steps:

```
-- Step 1:
-- cd to directory where you CSV data resides 
cd /Users/mparsian/max/github/data-warehousing/resources/data/flights_small/

-- Step 2:
% mysql --local-infile=1 -h localhost -uroot -p

-- Step 3:
use homeworks;

-- Step 4:
create table FLIGHTS
        (fid int, 
         year int, 
         month_id int, 
         day_of_month int, 
         day_of_week_id int, 
         carrier_id varchar(3), 
         flight_num int,
         origin_city varchar(34), 
         origin_state varchar(47), 
         dest_city varchar(34), 
         dest_state varchar(46), 
         departure_delay double, 
         taxi_out double, 
         arrival_delay double,
         canceled int, 
         actual_time double, 
         distance double, 
         capacity int, 
         price double);
 
-- Step 5:
LOAD DATA LOCAL INFILE 'flights-small.with.header.csv' 
  INTO TABLE FLIGHTS
  FIELDS TERMINATED BY ',' 
  IGNORE 1 LINES;
  
mysql> LOAD DATA LOCAL INFILE 'flights-small.with.header.csv'
    ->   INTO TABLE FLIGHTS
    ->   FIELDS TERMINATED BY ','
    ->   IGNORE 1 LINES;
Query OK, 1148675 rows affected, 65535 warnings (9.49 sec)
Records: 1148675  Deleted: 0  Skipped: 0  Warnings: 74279

select count(*) from FLIGHTS;

mysql> select count(*) from FLIGHTS;
+----------+
| count(*) |
+----------+
|  1148675 |
+----------+
1 row in set (0.11 sec)

select * from FLIGHTS limit 5;
mysql> select * from FLIGHTS limit 5;
+------+------+----------+--------------+----------------+------------+------------+-------------+--------------+----------------+------------+-----------------+----------+---------------+----------+-------------+----------+----------+--------+
| fid  | year | month_id | day_of_month | day_of_week_id | carrier_id | flight_num | origin_city | origin_state | dest_city      | dest_state | departure_delay | taxi_out | arrival_delay | canceled | actual_time | distance | capacity | price  |
+------+------+----------+--------------+----------------+------------+------------+-------------+--------------+----------------+------------+-----------------+----------+---------------+----------+-------------+----------+----------+--------+
|    1 | 2005 |        7 |            1 |              5 | AA         |          1 | New York NY | New York     | Los Angeles CA | California |              -4 |       29 |             9 |        0 |         360 |     2475 |       10 | 480.95 |
|    2 | 2005 |        7 |            2 |              6 | AA         |          1 | New York NY | New York     | Los Angeles CA | California |              -7 |       13 |           -10 |        0 |         344 |     2475 |       11 | 817.49 |
|    3 | 2005 |        7 |            3 |              7 | AA         |          1 | New York NY | New York     | Los Angeles CA | California |              -1 |       17 |            -4 |        0 |         344 |     2475 |       14 | 789.78 |
|    4 | 2005 |        7 |            4 |              1 | AA         |          1 | New York NY | New York     | Los Angeles CA | California |              -9 |       20 |            17 |        0 |         373 |     2475 |        3 | 523.12 |
|    5 | 2005 |        7 |            5 |              2 | AA         |          1 | New York NY | New York     | Los Angeles CA | California |              -6 |       32 |            12 |        0 |         365 |     2475 |        8 | 606.44 |
+------+------+----------+--------------+----------------+------------+------------+-------------+--------------+----------------+------------+-----------------+----------+---------------+----------+-------------+----------+----------+--------+
5 rows in set (0.00 sec)
```
