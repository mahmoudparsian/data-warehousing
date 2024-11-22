# Book Seller to Star Schema


# Star Schema Example

![](./star_schema_example.png)



## Sales table:

~~~sql
transaction_id   INTEGER
book_id          INTEGER, 
book_title       TEXT, 
book_genre       TEXT
date_sold        DATE
year_sold        INTEGER
month_sold       INTEGER
day_sold         INTEGER
sale_price       DOUBLE
promotion_amount DOUBLE
promotion_used   BOOLEAN {true, false}
country_sold     TEXT
city_sold        TEXT
region_sold      TEXT
hard_copy        BOOLEAN
paperback        BOOLEAN
kindle           BOOLEAN
soft_copy        BOOLEAN
~~~

## Books table:

~~~sql
author_id         INTEGER
book_id           INTEGER
book_title        TEXT
author_last_name  TEXT
author_first_name TEXT
author_web_site   TEXT
book_published    DATE
~~~

# Star Schema

### Sales table => Star Schema tables

![](./star_schema_book.png)


## 1. Book table (as DIMENSION)

	The book dimension stores the 
	name and genre of each book sold

~~~sql	
book_id           INTEGER, 
book_title        TEXT, 
book_genre        TEXT
author_id         INTEGER
author_last_name  TEXT
author_first_name TEXT
author_web_site   TEXT
book_published    DATE
~~~


## 2. Location table  (as DIMENSION)

	The location dimension stores the 
	city and region of the stores

~~~sql
location_id INTEGER 
country     TEXT
city        TEXT 
region      TEXT
~~~

## 3. `Time_dim` table (as DIMENSION)

	`Time_dim` table stores 
	the date of each sale.

~~~sql
time_id    INTEGER
date       DATE 
day        INTEGER, 
month      INTEGER, 
year       INTEGER
~~~


## 4. Type of Book DIMENSION

~~~sql
type_of_book_id  INTEGER
hard_copy        BOOLEAN
paperback        BOOLEAN
kindle           BOOLEAN
soft_copy        BOOLEAN
~~~

## 5. FACT TABLE sale

	The fact table stores facts about 
	how many of each book is sold each day.

~~~sql
book_id          INTEGER, 
location_id      INTEGER, 
date_id          INTEGER, 
sale_price       DOUBLE
promotion_used   BOOLEAN {true, false}
promotion_amount DOUBLE
type_of_book_id  INTEGER
~~~