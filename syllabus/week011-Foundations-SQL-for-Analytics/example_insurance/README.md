This is to be prepared for Week 1 
of a Data Warehousing class: SQL Foundations

consider the following dataset: insurance.csv

 % ls -l insurance.csv
-rw-r--r--@ 1 max  staff  55631 Mar 29 11:41 insurance.csv
week011-Foundations-SQL-for-Analytics (main) % wc -l insurance.csv
    1339 insurance.csv
week011-Foundations-SQL-for-Analytics (main) % head insurance.csv
age,gender,bmi,children,smoker,region,charges
19,female,27.9,0,yes,southwest,16884.924
18,male,33.77,1,no,southeast,1725.5523
28,male,33,3,no,southeast,4449.462
33,male,22.705,0,no,northwest,21984.47061
32,male,28.88,0,no,northwest,3866.8552
31,female,25.74,0,no,southeast,3756.6216
46,female,33.44,1,no,southeast,8240.5896
37,female,27.74,3,no,northwest,7281.5056
37,male,29.83,2,no,northeast,6406.4107

1. Provide Metadata Description:
Give a description of every column as a bullet item

deliver this as insurance_metadata_description.md file

2. Use DuckDB and Jupyter Notebook to deliver "SQL Foundations":

Provide 10 basic, 10 intermediate, and 5 advanced queries

For each query:

a. Define the query: what problem this query is going to solve
b. provide a solution in a nicely formatted SQL
c. provide explanation of SQL solution
d. give a business insight for the query/solution
e. if possible provide a nice plot and explain the plot from business point of view

