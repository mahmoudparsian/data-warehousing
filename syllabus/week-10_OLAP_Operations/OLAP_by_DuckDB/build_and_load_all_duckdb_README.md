Here is your single one-shot SQL script:

👉 Download build_and_load_all_duckdb.sql￼

⸻

How to Use

Place this file in the same directory as your csv/ folder, then run:

duckdb online_sales.duckdb < build_and_load_all_duckdb.sql

OR

duckdb online_sales.duckdb
.read build_and_load_all_duckdb.sql

It will:
	1.	Drop existing tables
	2.	Create full star schema
	3.	Load all CSV files
	4.	Run ANALYZE
	5.	Validate row counts
	6.	Run a sample OLAP query

⸻

You now have a fully automated star schema build in one file.

Next step: 🔥 OLAP (ROLLUP, CUBE, GROUPING SETS, advanced analytics). ￼
