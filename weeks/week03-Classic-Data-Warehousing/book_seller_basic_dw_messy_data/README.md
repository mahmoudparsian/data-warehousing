# Book Seller to Star Schema
# DEMO of Data Warehousing
# With Some Messy Data

## Purpose of This Example

The purpose of this example is to 

```
1. To understand the given operational/
   transactional database tables

2. Design a Star Schema based on operational/
   transactional database tables

3. Understand the ETL process to convert 
   transactional database tables into a Star Schema 

4. Understand the FACT table and its associated 
   Dimensional Tables

5. Define 10 Business Intelligence questions 
   in English language 

6. Express 10 Business Intelligence questions 
   in SQL using the Star Schema
```   
   
## Book Seller Story: 

A new book seller sells books everywhere in the world.

Given the following 2 operational/transactional database tables

```
    1. Sales table
    
    2. Books table
```

## We answer the following Questions:

1. What is a Star Schema

2. How would you design a Star Schema for these given tables

3. What are your ETL programs to create 
   Star Schema from these 2 operational tables

4. What are the 10 Business Intelligence SQL 
   queries to give an insight to book sales


## Book Seller Operational/Transactional Tables

### Sales table:
~~~
  COLUMN NAME      DATA TYPE
  --------------   ----------
  transaction_id   INTEGER  
  book_id          INTEGER, 
  sale_type        TEXT     -- { ONLINE, INSTORE}
  date_sold        DATE
  year_sold        INTEGER
  customer_gender  TEXT     -- { MALE, FEMALE}
  sale_price       DOUBLE
  discount         DOUBLE
  final_price      DOUBLE -- final_price = sale_price - discount
  country_sold     TEXT   -- 10 countries (total)
  city_sold        TEXT   -- 20 cities (total)
  book_format      TEXT   -- {"hard_copy", "paperback", "soft_copy"}        BOOLEAN
~~~

### Books table:

~~~
  COLUMN NAME      DATA TYPE
  --------------   ----------
  book_id           INTEGER
  book_title        TEXT 
  book_genre        TEXT -- 5 categories of books
  author_id         INTEGER
  author_name       TEXT
  author_gender     TEXT -- { MALE, FEMALE }
  author_web_site   TEXT
  published_date    DATE
  publisher         TEXT -- {Penguin, Prentice Hall, O'Reilly}
~~~

# Star Schema BOOK SELLER

## 1. Book table (as DIMENSION)

```
	The book dimension stores the 
	name and genre of each book sold
```

## 2. Location table  (as DIMENSION)

```
	The location dimension stores the 
	city and region of the stores
```

~~~sql
location_id INTEGER 
country     TEXT
city        TEXT 
~~~

## 3. `dates` table (as DIMENSION)

```
	table stores the date of each sale.
```


## 4. FACT TABLE sale

```
	The fact table stores facts about 
	how many of each book is sold each day.
```

# Files

| File | What it is |
|---|---|
| `data/books.csv` | Book table, 120 rows (with problems) |
| `data/sales.csv` | Sales table, 21,000 rows (with problems) |
| `dw_notebook.py` | Demo: Bronze → Silver → Gold (star schema) pipeline that cleans this data |

What exactly is wrong with the data? Finding out is your job in [Lab 3.2](../labs/week_03_lab_02_student.md).
