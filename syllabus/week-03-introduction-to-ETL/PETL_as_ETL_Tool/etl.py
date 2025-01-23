"""
We can install PETL by running the following command:

pip install petl

"""

import sys
import petl as etl


# DEFINE your INPUT PATH
# sales_data_as_csv = "sales_data.csv"
sales_data_as_csv = sys.argv[1]


# STEP-1: Load the data from CSV file
table = etl.fromcsv(sales_data_as_csv)
table = etl.convert(table, 'quantity', int)
table = etl.convert(table, 'price', int)
print("table=\n", table)

# STEP-2: Filter out rows with quantity <= 0
filtered_table = etl.select(table, lambda rec: rec.quantity > 0)
print("filtered_table=\n", filtered_table)
print("len(filtered_table)=", len(filtered_table))

# STEP-3: Calculate the total sales amount for each product
aggregated_table = etl.addfield(filtered_table, 'total_sales', lambda row: row.price * row.quantity) 
#aggregated_table = etl.aggregate(table3, key='product', aggregation={'total_sales': sum}, value='price')
print("aggregated_table=\n", aggregated_table)


# STEP-4: Sort the data based on total sales amount
sorted_table = etl.sort(aggregated_table, key='total_sales', reverse=True)
#print("sorted_table=\n", sorted_table)

# STEP-5: Save the transformed data to a new CSV file
etl.tocsv(sorted_table, 'transformed_sales_data.csv')
