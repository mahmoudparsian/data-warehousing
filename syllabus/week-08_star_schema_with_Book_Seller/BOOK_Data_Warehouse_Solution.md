# Star Schema Solution for a Book Seller, REVISED

# Operational Tables 

### Sales table:

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
user_email       TEXT
user_city        TEXT
user_country     TEXT
~~~

### Books table:

~~~sql
author_id         INTEGER
book_id           INTEGER
book_title        TEXT
author_last_name  TEXT
author_first_name TEXT
author_web_site   TEXT
book_published    DATE
~~~


# Star Schema for Book Seller

### Dimension Table:  Users
~~~sql
user_id          INTEGER (PK)
user_email       TEXT
user_city        TEXT
user_country     TEXT
~~~


### Dimension Table:  Date_Sold
~~~sql
date_id          INTEGER (PK)
date_sold        DATE
year_sold        INTEGER
month_sold       INTEGER
day_sold         INTEGER
~~~

### Dimension Table:  Location
~~~sql
location_id      INTEGER (PK)
country_sold     TEXT
city_sold        TEXT
region_sold      TEXT
~~~

### Dimension Table:  Book_type

NOTE: Assumption: only ONE of them will be true

~~~sql
book_type_id      INTEGER (PK)
book_type         TEXT

Assumption: only ONE of them will be true
(1, "hard_copy")
(2, "paperback")
(3, "kindle")
(4, "soft_copy")
~~~

### Dimension Table:  Book_type

NOTE: Assumption: More than one of them can be true

~~~sql
book_type_id      INTEGER (PK)
book_type         TEXT


Assumption: only ONE of them will be true
(1, "TTTT", {"hard_copy", "paperback", "kindle", "soft_copy"} 
(2, "TTTF", {"hard_copy", "paperback", "kindle"} 
(3, "TTFT", {"hard_copy", "paperback", "soft_copy"} 
(4, "TTFF", {"hard_copy", "paperback"} 
...
(15, ...)
(16, "FFFF") -> WILL NOT Happen
~~~

### Dimension table: Books
~~~sql
book_id           INTEGER (PK)
book_genre        TEXT     <-- moved from the Sales table
book_title        TEXT
book_published    DATE
author_id         INTEGER
author_last_name  TEXT
author_first_name TEXT
author_web_site   TEXT  
~~~
    
## FACT table: Sales


	Note-1: DROPPED promotion_used   BOOLEAN {true, false} 

	Note-2: promotion_amount DOUBLE  
	        if > 0, promotion is used, 
	        if 0, promotion is NOT used 
	        

~~~sql
transaction_id   INTEGER
user_id          INTEGER (FK)
date_id          INTEGER (FK)
location_id      INTEGER (FK)
book_type_id     INTEGER (FK)
book_id          INTEGER (FK)
sale_price       DOUBLE
promotion_amount DOUBLE  
~~~


# NOTE: 

	Books dimension can be split into Books 
	and Authors tables: THEN this will be 
	a Snowflake Schema.



