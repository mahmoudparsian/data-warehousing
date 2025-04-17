# Transactional Database --> ETL --> Star Schema --> OLAP Queries

		The goal of this exercise is to show a 
		complete story of creating a "star schema" 
		from a transactional database by using a 
		Python ETL. 
		
		Once a "star schema" is created, then we can
		write our Business Intelligence SQL queries.


# 1. Database configurations
Database configurations are defined as JSON files:

* Transactional (Source) Database:
	* [`db_config_source.json`](./step_2_etl_to_star_schema/db_config_source.json) 

* Star Schema (Target) Database:
	* [`db_config_target.json`](./step_2_etl_to_star_schema/db_config_target.json) 


# 2. Transactional Database

The Transactional Database has 3 tables (which will be created).

* movies

* users

* ratings

------

# 3. Creating  Transactional Database

1. The `movies` table will be created from the following:

		IMDB_Movies_2000_2020.csv
				
2. The Python program `generate_users_as_csv_file.py`
   generates users data as CSV file

3. The Python program `generate_ratings_as_csv_file.py`
   generates ratings data as CSV file   

-------
# 3.0 Create Transactional Database:

~~~sql
CREATE DATABASE movies2
 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
~~~

# 3.1 Create `movies` table:

~~~sql
CREATE TABLE movies (
    imdm_title_id VARCHAR(255),
    title VARCHAR(255),
    original_title VARCHAR(255),
    year int,
    date_published VARCHAR(255),
    genre VARCHAR(255),
    duration INT,
    country  VARCHAR(255),
    language_1  VARCHAR(255),
    language_2  VARCHAR(255),
    language_3  VARCHAR(255),
    director  VARCHAR(255),
    writer  VARCHAR(255),
    actors  VARCHAR(955),
    actors_1  VARCHAR(955),
    actors_f2  VARCHAR(955),
    description  VARCHAR(255),
    desc35  VARCHAR(255),
    avg_vote DOUBLE,
    votes INT,
    budget INT,
    usa_gross_income INT,
    worlwide_gross_income INT,
    reviews_from_users INT
) CHARACTER SET utf8 COLLATE utf8_general_ci;
~~~

# 3.2 Load Data into `movies` Table

~~~
LOAD DATA LOCAL INFILE "/Users/mparsian/github/data-warehousing/syllabus/week-03-introduction-to-ETL/movies_to_star_schema/step_1_build_transacational_db/IMDB_Movies_2000_2020.csv"
INTO TABLE movies
COLUMNS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
~~~

## More work

~~~

mysql> select * from movies limit 4;
+---------------+----------------------+------------------+------+----------------+--------------------------+----------+------------------+------------+--------------+------------+--------------------+------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------+----------+--------+----------+------------------+-----------------------+--------------------+
| imdm_title_id | title                | original_title   | year | date_published | genre                    | duration | country          | language_1 | language_2   | language_3 | director           | writer                       | actors                                                                                                                                                                                                                            | actors_1        | actors_f2                          | description                                                                                                                                                                                           | desc35                                    | avg_vote | votes  | budget   | usa_gross_income | worlwide_gross_income | reviews_from_users |
+---------------+----------------------+------------------+------+----------------+--------------------------+----------+------------------+------------+--------------+------------+--------------------+------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------+----------+--------+----------+------------------+-----------------------+--------------------+
| tt0035423     | Kate & Leopold       | Kate & Leopold   | 2001 | 01/03/2002     | Comedy, Fantasy, Romance |      118 | USA              | English    | French       |            | James Mangold      | Steven Rogers, James Mangold | Meg Ryan, Hugh Jackman, Liev Schreiber, Breckin Meyer, Natasha Lyonne, Bradley Whitford, Paxton Whitehead, Spalding Gray, Josh Stamberg, Matthew Sussman, Charlotte Ayanna, Philip Bosco, Andrew Jack, Stan Tracy, Kristen Schaal | Meg Ryan        | Meg Ryan, Hugh Jackman             | An English Duke from 1876 is inadvertedly dragged to modern day New York where he falls for a plucky advertising executive.                                                                           | An English Duke from 1876 is inadvertedly |      6.4 |  77852 | 48000000 |         47121859 |              76019048 |                341 |
| tt0118589     | Glitter              | Glitter          | 2001 | 30/11/2001     | Drama, Music, Romance    |      104 | USA              | English    |              |            | Vondie Curtis-Hall | Cheryl L. West, Kate Lanier  | Mariah Carey, Max Beesley, Da Brat, Tia Texada, Valarie Pettiford, Ann Magnuson, Terrence Howard, Dorian Harewood, Grant Nickalls, Eric Benét, Padma Lakshmi, Don Ackerman, Ed Sahely, Carmen Wong, James Allodi                  | Mariah Carey    | Mariah Carey, Max Beesley          | A young singer dates a disc jockey who helps her get into the music business, but their relationship become complicated as she ascends to super stardom.                                              | A young singer dates a disc jockey        |      2.2 |  21298 | 22000000 |          4274407 |               5271666 |                319 |
| tt0118694     | In the Mood for Love | Fa yeung nin wah | 2000 | 27/10/2000     | Drama, Romance           |       98 | Hong Kong, China | Cantonese  | Shanghainese | French     | Kar-Wai Wong       | Kar-Wai Wong                 | Maggie Cheung, Tony Chiu-Wai Leung, Ping Lam Siu, Tung Cho 'Joe' Cheung, Rebecca Pan, Kelly Lai Chen, Man-Lei Chan, Kam-Wah Koo, Szu-Ying Chien, Paulyn Sun, Roy Cheung, Po-chun Chow, Hsien Yu                                   | Maggie Cheung   | Maggie Cheung, Tony Chiu-Wai Leung | Two neighbors, a woman and a man, form a strong bond after both suspect extramarital activities of their spouses. However, they agree to keep their bond platonic so as not to commit similar wrongs. | Two neighbors, a woman and a man,         |      8.1 | 119171 |        0 |          2738980 |              12854953 |                422 |
| tt0120202     | Hollywood, Vermont   | State and Main   | 2000 | 31/05/2002     | Comedy, Drama            |      105 | France, USA      | English    | Italian      |            | David Mamet        | David Mamet                  | Michael Higgins, Michael Bradshaw, Morris Lamore, Allen Soule, Clark Gregg, Rebecca Pidgeon, Ricky Jay, Julia Stiles, Matt Malloy, Charles Durning, Tony V., Tony Mamet, Jack Wallace, Michael James O'Boyle, Charlotte Potok     | Michael Higgins | Michael Higgins, Michael Bradshaw  | A movie crew invades a small town whose residents are all too ready to give up their values for showbiz glitz.                                                                                        | A movie crew invades a small town         |      6.7 |  20220 |        0 |          6944471 |               9206279 |                175 |
+---------------+----------------------+------------------+------+----------------+--------------------------+----------+------------------+------------+--------------+------------+--------------------+------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------+----------+--------+----------+------------------+-----------------------+--------------------+
4 rows in set (0.00 sec)


mysql> # Add a new column date_published_2 as a DATE format:

mysql> ALTER TABLE movies 
       ADD COLUMN date_published_2 DATE;

mysql> UPDATE movies
       SET date_published_2 = STR_TO_DATE(date_published, '%d/%m/%Y');

mysql> select date_published, date_published_2 from movies;
+----------------+------------------+
| date_published | date_published_2 |
+----------------+------------------+
| 01/03/2002     | 2002-03-01       |
| 30/11/2001     | 2001-11-30       |
| 27/10/2000     | 2000-10-27       |
...

I have a mysql table, how can I add a new column  
and set the values from 1, 2, 3, ...
You can achieve this by following these steps:

Add the new column to the table: 
Use the ALTER TABLE statement to create the new column:

mysql>
ALTER TABLE movies
ADD COLUMN movie_id INT;

Update the column with sequential values: 
You can populate the new column using the UPDATE 
statement along with a user-defined variable to 
create sequential numbers:

mysql>
SET @counter = 0;
UPDATE movies
SET movie_id = (@counter := @counter + 1);

mysql> select movie_id, imdm_title_id from movies;
+----------+---------------+
| movie_id | imdm_title_id |
+----------+---------------+
|        1 | tt0035423     |
|        2 | tt0118589     |
|        3 | tt0118694     |
|        4 | tt0120202     |
...
|     5485 | tt9806192     |
|     5486 | tt9860728     |
|     5487 | tt9898858     |
+----------+---------------+
5487 rows in set (0.01 sec)

mysql> select * from movies limit 4;
+---------------+----------------------+------------------+------+----------------+--------------------------+----------+------------------+------------+--------------+------------+--------------------+------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------+----------+--------+----------+------------------+-----------------------+--------------------+------------------+-------+
| imdm_title_id | title                | original_title   | year | date_published | genre                    | duration | country          | language_1 | language_2   | language_3 | director           | writer                       | actors                                                                                                                                                                                                                            | actors_1        | actors_f2                          | description                                                                                                                                                                                           | desc35                                    | avg_vote | votes  | budget   | usa_gross_income | worlwide_gross_income | reviews_from_users | date_published_2 | mpvie_id |
+---------------+----------------------+------------------+------+----------------+--------------------------+----------+------------------+------------+--------------+------------+--------------------+------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------+----------+--------+----------+------------------+-----------------------+--------------------+------------------+-------+
| tt0035423     | Kate & Leopold       | Kate & Leopold   | 2001 | 01/03/2002     | Comedy, Fantasy, Romance |      118 | USA              | English    | French       |            | James Mangold      | Steven Rogers, James Mangold | Meg Ryan, Hugh Jackman, Liev Schreiber, Breckin Meyer, Natasha Lyonne, Bradley Whitford, Paxton Whitehead, Spalding Gray, Josh Stamberg, Matthew Sussman, Charlotte Ayanna, Philip Bosco, Andrew Jack, Stan Tracy, Kristen Schaal | Meg Ryan        | Meg Ryan, Hugh Jackman             | An English Duke from 1876 is inadvertedly dragged to modern day New York where he falls for a plucky advertising executive.                                                                           | An English Duke from 1876 is inadvertedly |      6.4 |  77852 | 48000000 |         47121859 |              76019048 |                341 | 2002-03-01       |     1 |
| tt0118589     | Glitter              | Glitter          | 2001 | 30/11/2001     | Drama, Music, Romance    |      104 | USA              | English    |              |            | Vondie Curtis-Hall | Cheryl L. West, Kate Lanier  | Mariah Carey, Max Beesley, Da Brat, Tia Texada, Valarie Pettiford, Ann Magnuson, Terrence Howard, Dorian Harewood, Grant Nickalls, Eric Benét, Padma Lakshmi, Don Ackerman, Ed Sahely, Carmen Wong, James Allodi                  | Mariah Carey    | Mariah Carey, Max Beesley          | A young singer dates a disc jockey who helps her get into the music business, but their relationship become complicated as she ascends to super stardom.                                              | A young singer dates a disc jockey        |      2.2 |  21298 | 22000000 |          4274407 |               5271666 |                319 | 2001-11-30       |     2 |
| tt0118694     | In the Mood for Love | Fa yeung nin wah | 2000 | 27/10/2000     | Drama, Romance           |       98 | Hong Kong, China | Cantonese  | Shanghainese | French     | Kar-Wai Wong       | Kar-Wai Wong                 | Maggie Cheung, Tony Chiu-Wai Leung, Ping Lam Siu, Tung Cho 'Joe' Cheung, Rebecca Pan, Kelly Lai Chen, Man-Lei Chan, Kam-Wah Koo, Szu-Ying Chien, Paulyn Sun, Roy Cheung, Po-chun Chow, Hsien Yu                                   | Maggie Cheung   | Maggie Cheung, Tony Chiu-Wai Leung | Two neighbors, a woman and a man, form a strong bond after both suspect extramarital activities of their spouses. However, they agree to keep their bond platonic so as not to commit similar wrongs. | Two neighbors, a woman and a man,         |      8.1 | 119171 |        0 |          2738980 |              12854953 |                422 | 2000-10-27       |     3 |
| tt0120202     | Hollywood, Vermont   | State and Main   | 2000 | 31/05/2002     | Comedy, Drama            |      105 | France, USA      | English    | Italian      |            | David Mamet        | David Mamet                  | Michael Higgins, Michael Bradshaw, Morris Lamore, Allen Soule, Clark Gregg, Rebecca Pidgeon, Ricky Jay, Julia Stiles, Matt Malloy, Charles Durning, Tony V., Tony Mamet, Jack Wallace, Michael James O'Boyle, Charlotte Potok     | Michael Higgins | Michael Higgins, Michael Bradshaw  | A movie crew invades a small town whose residents are all too ready to give up their values for showbiz glitz.                                                                                        | A movie crew invades a small town         |      6.7 |  20220 |        0 |          6944471 |               9206279 |                175 | 2002-05-31       |     4 |
+---------------+----------------------+------------------+------+----------------+--------------------------+----------+------------------+------------+--------------+------------+--------------------+------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------+------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------+----------+--------+----------+------------------+-----------------------+--------------------+------------------+-------+
4 rows in set (0.00 sec)

mysql> select movie_id from movies limit 5;
+----------+
| movie_id |
+----------+
|        1 |
|        2 |
|        3 |
|        4 |
|        5 |
+----------+
5 rows in set (0.00 sec)

mysql> ALTER TABLE movies
       CHANGE year release_year INT;

Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0
~~~

# Load `ratings` table

~~~
create table ratings(
    rating_id INT,
    movie_id INT,
    user_id INT,
    rating INT, -- 1, 2, 3, ..., 10
    rating_date Date
);

LOAD DATA LOCAL INFILE "/Users/mparsian/github/data-warehousing/syllabus/week-03-introduction-to-ETL/movies_to_star_schema/step_1_build_transacational_db/ratings.csv"
INTO TABLE ratings
COLUMNS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

mysql> select count(*) from ratings;
+----------+
| count(*) |
+----------+
|  2000000 |
+----------+
1 row in set (0.06 sec)

mysql> select * from ratings limit 5;
+-----------+----------+---------+--------+-------------+
| rating_id | movie_id | user_id | rating | rating_date |
+-----------+----------+---------+--------+-------------+
|         1 |      527 |   89631 |     10 | 2022-10-23  |
|         2 |     3677 |   70546 |     10 | 2021-04-03  |
|         3 |     3318 |   68106 |      3 | 2021-02-03  |
|         4 |     1797 |   46927 |      2 | 2020-02-16  |
|         5 |     1574 |   99078 |      8 | 2021-11-11  |
+-----------+----------+---------+--------+-------------+
5 rows in set (0.00 sec)

~~~

# Load `users` table

~~~
-- #### Table: `users`
create table users(
    user_id INT,
    user_name VARCHAR(60)      
);

LOAD DATA LOCAL INFILE "/Users/mparsian/github/data-warehousing/syllabus/week-03-introduction-to-ETL/movies_to_star_schema/step_1_build_transacational_db/users.csv"
INTO TABLE ratings
COLUMNS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

mysql> select count(*) from users;

~~~
--------

# 4. ETL

## 4.1 [ETL --> Star Schema](./etl.py)


## 4.2 To run ETL:


~~~sh
ETL="et.py"
SOURCE_DB="db_config_source.json"
TARGET_DB="db_config_target.json"
#                sys.argv[1]   sys.argv[2]
python3  ${ETL}  ${SOURCE_DB}  ${TARGET_DB}
~~~
-------

# 5. Star Schema

![](./star_schema.drawio.png)

-------


1. **Create a transactional database** with movies and user ratings.
2. **Python ETL script** to transform the transactional database into a **star schema**.
3. **OLAP SQL queries** using the star schema.

---


# Star Schema Design

#### Fact Table: `fact_ratings`

~~~
| rating_id | movie_id | user_id | rating | rating_date  |
~~~

#### Dimension Tables:

~~~
1. `dim_movies`
   | movie_id | movie_title | genre | release_year |

2. `dim_users`
   | user_id | user_name |

3. `dim_date`
   | date_id | rating_date | year | month | day |

~~~
---

### Python ETL Script

`etl.py`

---

