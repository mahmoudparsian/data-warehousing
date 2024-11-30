% mysql --verbose --help | grep my.cnf
/etc/my.cnf /etc/mysql/my.cnf /usr/local/etc/my.cnf ~/.my.cnf

MySQL conf file:
/usr/local/etc/my.cnf

-- full path: DID NOT WORK
LOAD DATA INFILE "/Users/mparsian/max/github/data-warehousing-and-business-intelligence/resources/ETL/ETL_Electric_Vehicle_Example/Electric_Vehicle_Population_Data.csv"
INTO TABLE ev_imported_from_csv
COLUMNS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES; 

LOAD DATA LOCAL INFILE "Electric_Vehicle_Population_Data.csv"
INTO TABLE ev_imported_from_csv
COLUMNS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES; 

% pwd
/Users/mparsian/max/github/data-warehousing-and-business-intelligence/resources/ETL/ETL_Electric_Vehicle_Example

% mysql --local-infile=1 -h localhost -u root -p
Enter password: xxxxxxx

mysql> use test;
Database changed

-- --------------------------------------
-- Table structure for ev_table_from_csv
-- --------------------------------------
DROP TABLE IF EXISTS `ev_imported_from_csv`;
CREATE TABLE `ev_imported_from_csv` (
  `VIN` text,
  `County` text,
  `City` text,
  `State` text,
  `Postal_Code` double DEFAULT NULL,
  `Model_Year` bigint DEFAULT NULL,
  `Make` text,
  `Model` text,
  `Electric_Vehicle_Type` text,
  `Electric_Range` bigint DEFAULT NULL,
  `Base_MSRP` bigint DEFAULT NULL,
  `Legislative_District` double DEFAULT NULL,
  `DOL_Vehicle_ID` bigint DEFAULT NULL,
  `Electric_Utility` text,
  `Census_Tract_2020` double DEFAULT NULL
);

mysql> LOAD DATA LOCAL INFILE "Electric_Vehicle_Population_Data.csv"
    -> INTO TABLE ev_imported_from_csv
    -> COLUMNS TERMINATED BY ','
    -> OPTIONALLY ENCLOSED BY '"'
    -> ESCAPED BY '"'
    -> LINES TERMINATED BY '\n'
    -> IGNORE 1 LINES;
Query OK, 124716 rows affected, 301 warnings (1.46 sec)
Records: 124716  Deleted: 0  Skipped: 0  Warnings: 301

mysql> select count(*) from ev_imported_from_csv;
+----------+
| count(*) |
+----------+
|   124716 |
+----------+
1 row in set (0.02 sec)

mysql> select * from ev_imported_from_csv limit 3;
+------------+-----------+-----------+-------+-------------+------------+-------+---------+----------------------------------------+----------------+-----------+----------------------+----------------+------------------+-------------------+
| VIN        | County    | City      | State | Postal_Code | Model_Year | Make  | Model   | Electric_Vehicle_Type                  | Electric_Range | Base_MSRP | Legislative_District | DOL_Vehicle_ID | Electric_Utility | Census_Tract_2020 |
+------------+-----------+-----------+-------+-------------+------------+-------+---------+----------------------------------------+----------------+-----------+----------------------+----------------+------------------+-------------------+
| 5YJ3E1EB4L | Yakima    | Yakima    | WA    |       98908 |       2020 | TESLA | MODEL 3 | Battery Electric Vehicle (BEV)         |            322 |         0 |                   14 |      127175366 | PACIFICORP       |       53077000904 |
| 5YJ3E1EA7K | San Diego | San Diego | CA    |       92101 |       2019 | TESLA | MODEL 3 | Battery Electric Vehicle (BEV)         |            220 |         0 |                    0 |      266614659 |                  |        6073005102 |
| 7JRBR0FL9M | Lane      | Eugene    | OR    |       97404 |       2021 | VOLVO | S60     | Plug-in Hybrid Electric Vehicle (PHEV) |             22 |         0 |                    0 |      144502018 |                  |       41039002401 |
+------------+-----------+-----------+-------+-------------+------------+-------+---------+----------------------------------------+----------------+-----------+----------------------+----------------+------------------+-------------------+
3 rows in set (0.00 sec)

mysql>