# GROUP BY Tutorial using DuckDB

** before you generate anything, 
   please let me know if we have to finalize requirements*

1. Generate 4 separate files:

sales_2023.csv (100,000 records)
sales_2024.csv (200,000 records)
sales_2025.csv (400,000 records)
sales_2026.csv (300,000, for 3 months of January, February, March )


Columns are:

| column name       | Description and values |
|-------------------|------------------------|
|`transaction_id`   | transaction id         |
|`transation_date`  | as a timestamp spanning for 4 years : 2023, 2024, 2025, 2026|
|`sale_type`        | ONLINE, INSTORE
|`product_name`     | {ROBOT, TV, RADIO, TABLE, COMPUTER, BIKE, LAPTOP, WATCH, IPAD, EBIKE}|
|`price`            | as an integer, based on product|
|`quantity`         | as an integer: number of products: 1, 2, 3, 4
|`gender`           | MALE, FEMALE|
|`discount`         | this is a total discount for this transaction
|`country`          | USA, CANADA, GERMANY, INDIA, CHINA, MEXICO, ITALY, FRANCE, SPAIN|
|`age`              | 18 to 80 |
|`sales_amount`     | as an integer, sale_amount = (quantity * price) - discount

* Do not generate symmetric data, for example USA will have more sales than
any other country, 

* The number of FEMALE will be 5 to 3

* Product sales should not be even based on product name 
  some products should dominate sales

# What to do (all as  downloadable files)

1. generate the 4 files requested

2. Create meta data dictionary file as md/marp

3. Create a comprehensive EDA with business reasoning 
   and nice plots
   
4. Create a DuckDB/Notebook, which reads data (4 files), 
   4.1 What are we solving, NL query
   4.2 SQL Query in a nice format
   4.3 Nice Beautiful Plotting 
   4.4 Business insight in 2 bullet points.

   4.5  create 10 cells: using "group by" 

	Give a business insight to each query
		-- monthly sales
		-- yearly sales
		-- sale by country
		-- sale by gender
		-- sale by age group
		...
    
4.6 create 5 top-N queries
    * Give a business insight to each query
    
4.7 create 5 additional business insight queries

4.8 Add plotting for all queries




