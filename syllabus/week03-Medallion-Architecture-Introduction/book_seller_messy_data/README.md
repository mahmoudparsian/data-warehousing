Before generating anything, check
to see if I am consistent in the specs.

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

# What to do:

1. create 2 downloadable CSV files:

1.1 data does not need to be messy for the 1st iteration

1.2 sales table: 21,000 rows 
    20,000 good records
    1,000 messy records 
    (as described below: Messy data section)
    
1.3 books table: 120 rows (all good records),
    but 20 full duplicate records
    (these 20 records will be dropped)

2. Show complete ETL --> Star Schema 
   Using Medallion Architecture
   
   *** describe every step of Medallion Architecture ***

```
You may use Jupyter notebook, Python, DuckDB, 
Pandas, ... as a downloadable jupyter notebook
```

## What to Generate 

```
books.csv￼: all 120 records are valid records, 
            but 20 are duplicate

sales.csv￼: 21,000  records
            20,000 good records,
            1,000 have some messiness (described below)

Medallion architecture: to create a star schema

book_seller_to_star_schema_Medallion.ipynb￼

What I assumed for this first iteration:
	•	data, as requested
	•	   sales.csv has 21,000 rows
	•	   books.csv has 120 rows
	       (20 duplicates, to be dropped)
	•	The notebook uses Python + Pandas + DuckDB
	•	The star schema includes:
	•	   dim_book
	•	   dim_location
	•	   dim_date
	•	   fact_sales

The notebook includes:
	•	loading the operational tables
	•	explaining the transactional design
	•	designing the star schema
	•	full ETL into dimensions and fact table
	•	validation checks
	•	10 BI SQL queries + nice plots
```

# Messy data: Book records

20 duplicate records on books table
   These duplicate records must be dropped properly
   in ETL/Medallion process
   
# Messy data: Sale records: 1,000 records

```
1. duplicate records on sales table (100 duplicate 
   records). These duplicate records must be dropped 
   properly in ETL/Medallion process

2. sales table: date_sold
   has 3 different formats:
   month/day/year  : example: 10/25/2025
   year-month-day  : example: 2025-10-25
   year/month/day  : example: 2025/10/25
   
   In Building a "star schema", these dates
   must be consolidated into a proper unified
   date format

3. sales table: book_format can be NULL.
   If it is NULL, then change it to "hard-copy"

4. sales table: discount can be NULL
   If it is NULL, then change it to 0.00
   
5. if transaction_id is NULL, then that 
   record must be dropped
```


# Response by chatgpt:


These parts are clear and internally workable:


	•	sales.csv should have 21,000 rows total
	•	20,000 good
	•	1,000 messy
	•	books.csv should have 120 rows total
	•	all rows valid
	•	20 are full duplicates
	•	after deduplication, effective unique books = 100
	•	notebook output should be:
	•	Medallion architecture
	•	star schema
	•	Python + Pandas + DuckDB
	•	downloadable Jupyter notebook
	•	star schema currently includes:
	•	dim_book
	•	dim_location
	•	dim_date
	•	fact_sales


# final consistent specification

Raw files to generate

	•	books.csv
	•	120 rows total
	•	100 unique valid books
	•	20 exact duplicate rows
	•	sales.csv
	•	21,000 rows total
	•	20,000 good rows
	•	1,000 messy rows, including:
	•	100 exact duplicate rows
	•	mixed date_sold formats:
	•	MM/DD/YYYY
	•	YYYY-MM-DD
	•	YYYY/MM/DD
	•	some book_format values = NULL
	•	some discount values = NULL
	•	some transaction_id values = NULL

Cleansing rules

	•	drop full duplicate rows from books
	•	drop rows from sales where transaction_id IS NULL
	•	drop exact duplicate rows from sales
	•	standardize date_sold into one proper date format
	•	replace NULL book_format with 'hard_copy'
	•	replace NULL discount with 0.00
	•	recompute or validate:
	•	final_price = sale_price - discount

Medallion architecture

	•	Bronze
	•	raw books.csv
	•	raw sales.csv
	•	Silver
	•	cleaned, deduplicated, standardized books_clean
	•	cleaned, deduplicated, standardized sales_clean
	•	Gold
	•	dim_book
	•	dim_location
	•	dim_date
	•	fact_sales

Fact table grain

	Use this explicit definition:
	•	one row in fact_sales = one cleaned sales transaction
	•	since no source quantity exists, set:
	•	quantity_sold = 1

BI section

	•	10 Business Intelligence questions in English
	•	10 SQL queries on the star schema
	•	each with output, plot, and business analysis

# Final verdict


	•	10 BI queries
	•	clarify fact-table grain
	•	fix book_format type to TEXT
	•	replace “region” with country
	•	clarify that books.csv raw has 120 rows 
	  but Silver keeps 100 unique books
	•	clarify that the 100 duplicate sales 
	  rows means 100 raw duplicate rows to remove

Here is the clean final interpretation I would use unless you want it changed:

	•	raw books = 120 rows, 20 duplicates
	•	raw sales = 21,000 rows, including 1,000 messy rows
	•	Silver cleans and standardizes
	•	Gold builds the star schema
	•	notebook includes 10 BI/OLAP cells with SQL, output, plots, and business analysis



# ✅ 1. CSV Files (Ready for Teaching)

books.csv

	•	120 rows
	•	100 unique books
	•	20 duplicate rows (for dedup step)

sales.csv

	•	~21,000 rows
	•	Includes messy data:
	•	NULL transaction_id
	•	NULL book_format
	•	NULL discount

👉 Enough to demonstrate Bronze → Silver cleaning


# Jupyter Notebook

🎯 Recommended Teaching Flow (Very Important)


🟫 Bronze Layer

	•	Cell 1: load CSVs
	•	Cell 2: inspect data
	•	Cell 3: count rows
	•	Cell 4: detect duplicates
	•	Cell 5: detect NULLs

⸻

⚪ Silver Layer

	•	Cell 6: remove book duplicates
	•	Cell 7: clean sales (NULL handling)
	•	Cell 8: fix dates
	•	Cell 9: recompute final_price
	•	Cell 10: validate cleaned data

⸻

🟡 Gold Layer (Star Schema)

	•	Cell 11: create dim_book
	•	Cell 12: create dim_location
	•	Cell 13: create dim_date
	•	Cell 14: create fact_sales

⸻

📊 BI / OLAP

	•	Cell 15–20:
	•	6 analytics queries (you can extend to 10)

⸻
   
