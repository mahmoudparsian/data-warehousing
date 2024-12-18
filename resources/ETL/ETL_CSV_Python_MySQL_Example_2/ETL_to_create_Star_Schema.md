# ETL to Create "Star Schema"

	To demonstrate a Python-based ETL process 
	for creating a star schema, a simplified 
	example using the pandas library will be 
	presented. This example focuses on 
	
	1. extracting data from CSV files, 
	
	2. transforming it, and 
	
	3. loading it into a star schema structure. 
	
	
Scenario 

	Consider a sales dataset with information about:
	1. transactions, 
	2. products, 
	3. customers, and 
	4. dates. 

	The goal is to create a star schema with a central 
	fact table for sales and dimension tables for 
	products, customers, and dates. 

# 1. Extract 

Assume the data is stored in three CSV files: 

* `sales_data.csv`: 

Contains transaction details:
		
		transaction_id, 
		product_id,
		customer_id, 
		date_id, 
		quantity,
		price 

* `product_data.csv`: 

Contains product information:

	product_id, 
	product_name,
	category

*  `customer_data.csv`: 

Contains customer information:

	customer_id, 
	customer_name, 
	city 


* `date_data.csv`: 

Contains date information:

	date_id, 
	date, 
	month, 
	year 

	date examples: '2023-01-15', '2023-04-20'
	
	
	
~~~python
# required libraries: The pandas library 
# can be used to read these CSV files 
# into DataFrames: 

import pandas as pd

# extract data
sales_df = pd.read_csv("sales_data.csv")
product_df = pd.read_csv("product_data.csv")
customer_df = pd.read_csv("customer_data.csv")
date_df = pd.read_csv("date_data.csv")
~~~

# 2. Transform
 
	The data might require transformations 
	such as: 
	
	1. Selecting relevant columns, 
	2. Renaming columns for consistency, 
	3. Handling missing values, 
	4. Converting data types, and 
	5. Creating new calculated columns. 

	
For this example, assume the following transformations: 

* Transformation-1: Sales data: 

		Calculate `total_sales` as `quantity * price`. 

* Transformation-2: Date data: 

		Ensure date is in the correct format. 

* Transformation-3: 

		Create a new column `quarter` from a `date` column


~~~python
# Apply 3 transformations:

# Transformation-1:
sales_df["total_sales"] = sales_df["quantity"] * sales_df["price"]

# Transformation-2:
date_df["date"] = pd.to_datetime(date_df["date"])

# Transformation-3:
# Create the quarter column
date_df['quarter'] = date_df['date'].dt.quarter

# date            quarter
# 2023-01-15        1
# 2023-04-20        2
# 2023-07-01        3
# 2023-10-30        4
~~~

# 3. Load 

	The transformed data needs to be loaded 
	into the star schema. This involves: 

	1. Creating the dimension tables by loading 
	   the transformed data from created dataframes:
	   
	   product_df 
	   customer_df
	   date_df
	   
	2. Creating the FACT table by loading the 
	   transformed data from sales_df. 


	3. For simplicity, this example will demonstrate 
	   loading the data back into CSV files, representing
	   the tables in the star schema. 


~~~python
# Load transformed data into CSV files
product_df.to_csv("dim_product.csv", index=False)
customer_df.to_csv("dim_customer.csv", index=False)
date_df.to_csv("dim_date.csv", index=False)
sales_df.to_csv("fact_sales.csv", index=False)
~~~
	   
	4. In a real-world scenario, this would involve 
	   loading the data into a database. 

~~~python
# Load transformed data into Database Tables
# Create FACT table and DIMENSION tables
~~~

# 4. Star Schema Structure 

The resulting files represent the following star schema: 

* Fact Table: `fact_sales.csv`

		transaction_id, 
		product_id, 
		customer_id, 
		date_id, 
		quantity, 
		price, 
		total_sales
		 
* Dimension Tables: 

	• `dim_product.csv (product_id, product_name, category)` 
	
	• `dim_customer.csv (customer_id, customer_name, city)`
	
	• `dim_date.csv (date_id, date, month, year, quarter)` 



# 5. Note: 

	This is a basic example. 
	
	A full implementation would include 
	
	1. Error Handling, 
	2. Data Validation, and 
	3. Loading into a Database. 

	It would also address the selection 
	of appropriate surrogate keys for 
	dimension tables. 


