# Book Seller to Star Schema
# First DEMO of Data Warehousing

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

4. What are the 3 Business Intelligence SQL 
   queries to give an insight to book sales


## Book Seller Operational/Transactional Tables

### Sales table:
~~~
  COLUMN NAME      DATA TYPE
  --------------   ----------
  transaction_id   INTEGER
  book_id          INTEGER, 
  sale_type        TEXT, -- { ONLINE, INSTORE}
  date_sold        DATE
  year_sold        INTEGER
  month_sold       INTEGER
  day_sold         INTEGER
  sale_price       DOUBLE
  discount         DOUBLE
  final_price      DOUBLE -- final_price = sale_price - discount
  country_sold     TEXT   -- 5 countries (total)
  city_sold        TEXT   -- 15 cities (total)
  hard_copy        BOOLEAN
  paperback        BOOLEAN
  soft_copy        BOOLEAN
~~~

### Books table:

~~~
  COLUMN NAME      DATA TYPE
  --------------   ----------
  book_id           INTEGER
  book_title        TEXT 
  book_genre        TEXT
  author_id         INTEGER
  author_name       TEXT
  author_web_site   TEXT
  published_date    DATE
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

## 4. Type of Book sold DIMENSION


## 5. FACT TABLE sale

```
	The fact table stores facts about 
	how many of each book is sold each day.
```

# What to do:

1. create 2 downloadable CSV files:

1.1 data does not need to be messy for the 1st iteration

1.2 sales table: 10,000 rows

1.3 books table: 100 rows

2. Show complete ETL --> Star Schema

```
You may use Python, DuckDB, Pandas, ...
as a downloadable jupyter notebook
```

## Generated the files.

```
books.csv￼

sales.csv￼

book_seller_to_star_schema_poc.ipynb￼

What I assumed for this first iteration:
	•	Clean data, as requested
	•	sales.csv has 10,000 rows
	•	books.csv has 100 rows
	•	The notebook uses Python + Pandas + DuckDB
	•	The star schema includes:
	•	   dim_book
	•	   dim_location
	•	   dim_date
	•	   dim_book_format
	•	   fact_sales

The notebook includes:
	•	loading the operational tables
	•	explaining the transactional design
	•	designing the star schema
	•	full ETL into dimensions and fact table
	•	validation checks
	•	3 BI SQL queries
	•	a few simple plots
```

