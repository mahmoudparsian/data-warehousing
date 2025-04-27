% mysql --local-infile=1 -h localhost -u root -p
Enter password: xxxxxxx

mysql> use homeworks;
Database changed

-- --------------------------------------
-- Table structure for scores
-- --------------------------------------
DROP TABLE IF EXISTS `scores`;

CREATE TABLE `scores` (
  `name` text,
  `country` text,
  `score` int
);

mysql>

SET GLOBAL local_infile = TRUE; 

LOAD DATA LOCAL INFILE "/Users/mparsian/github/data-warehousing/syllabus/week-01-1-introduction_to_databases_and_SQL/load_data_into_mysql_table/scores_records.csv"
INTO TABLE scores
COLUMNS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
