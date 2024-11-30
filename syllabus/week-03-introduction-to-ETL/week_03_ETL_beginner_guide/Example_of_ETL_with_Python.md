# Very simple example. 

	In a real-world ETL pipeline, you would:
	Extract data from a variety of sources: 
	Databases, APIs, cloud storage, etc.

	Perform more complex transformations: 
	Data cleaning, filtering, aggregation, etc.

	Load data into a data warehouse or other 
	storage: For analysis and reporting.

# Example in Python

~~~python
# import required libraries
import pandas as pd

# 1. Extract
sales_data = pd.read_csv('sales_data.csv')
customer_data = pd.read_csv('customer_data.csv')

# 2. Transform
sales_data['sale_date'] = pd.to_datetime(sales_data['sale_date'])
sales_data['total_price'] = sales_data['quantity'] * sales_data['price']

# Merge
merged_data = pd.merge(sales_data, customer_data, on='customer_id')

# 3. Load
merged_data.to_csv('sales_customer_data.csv', index=False)
~~~

# Explanation:

	1. Extract: We read sales and customer 
	   data from CSV files.

	2. Transform: We convert the 'sale_date' column 
	   to a datetime object and calculate the 
	   'total_price' column.

	3. Load: We merge the two dataframes on the 
	   'customer_id' column and save the 
	   result to a new CSV file.

