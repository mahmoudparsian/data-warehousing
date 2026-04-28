# Medallion Data Warehouse <br> 10 Rows Case Study

	🟫 Bronze → ⚪ Silver → 🟡 Gold

	This project demonstrates a complete Medallion 
	Data Architecture (Bronze → Silver → Gold) using 
	a small 10-rows transactional dataset. 
	
	Starting from raw, messy data (missing values, 
	invalid  dates,  duplicates),  the  pipeline 
	progressively cleans, validates, and transforms 
	the data into a trusted analytical model. 
	
	The Silver layer enforces business rules (rejecting 
	bad data and identifying cancelled transactions), 
	while the  Gold layer builds a  star  schema with 
	dimension tables (`customer`, `product`, `date`) and 
	a fact table for analytics. 
	
	This compact example is designed for teaching and 
	clearly illustrates how raw data becomes reliable 
	business insights.

![](./medallion_architecture.webp)

# Files in this folder

| File                   | Description               |
|------------------------|---------------------------|
|[`README.md`](./README.md)             | this file you are reading |
|[`sales_data_10_rows.csv`](./sales_data_10_rows.csv)| sales data set: 10 rows
|[`medallion_running_case_study_10_rows.md`](./medallion_running_case_study_10_rows.md) | medallion architecture: step-by-step |
|[`case_study_sql_commands.sql`](./case_study_sql_commands.sql) | SQL commands in proper order |
|[`case_study_sql_commands.sql.output.txt`](./case_study_sql_commands.sql.output.txt) | Output of SQL commands |
|[`medallion_architecture.webp`](./medallion_architecture.webp) | medallion architecture image|


# How to Run SQL Commands (command line)

```
db="sales_data_10_rows.duckdb"
sql_commands="case_study_sql_commands.sql"
output_of_sql="case_study_sql_commands.sql.output.txt"
#
duckdb ${db} < ${sql_commands} > ${output_of_sql}
```
