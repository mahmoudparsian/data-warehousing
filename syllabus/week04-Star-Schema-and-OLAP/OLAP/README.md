# OLAP Operations

	OLAP operations extract 
	insights from  the data  
	stored in multidimensional 
	hypercubes. 
	
	
* OLAP operations:
	* Drill Down (a.k.a Roll-Down)
	* Roll Up
	* Dice
	* Slice
	* Pivot

-----

## DuckDB (use these first)

* [OLAP on a 1M-row star schema (DuckDB)](./OLAP_by_DuckDB/): build script + [45 queries: ROLLUP, CUBE, GROUPING SETS, drill-down, …](./OLAP_by_DuckDB/OLAP_Queries_ROLLUP_CUBE_GROUPINGSETS.md) (used in Lab 4.2)
* [ROLLUP and CUBE tutorial (DuckDB)](./OLAP_basics/ROLLUP_and_CUBE_Tutorial_using_DuckDB.md)
* [Introduction to DuckDB for MySQL users](./OLAP_basics/Introduction_to_DuckDB_for_MySQL_Users.md)

## Concepts

* [OLAP basics and definitions](./OLAP_basics/): [OLAP vs OLTP](./OLAP_basics/OLAP_vs_OLTP.md), [OLAP and CUBE basics](./OLAP_basics/OLAP_and_CUBE_basics.md), [list of operations](./OLAP_basics/List_of_OLAP_Operations_Summary.md)
* [OLAP operations, one file per operation](./OLAP_Operations/): roll-down, dice, pivot, … with examples
* [OLAP design patterns](./OLAP_design_patterns/OLAP_Design_Patterns.md) and [running totals](./OLAP_design_patterns/running_total_example.md)
* [Review: GROUP BY & CUBE, OLAP operations](./review/)
* [Lecture slides from other universities](./DW_and_OLAP_lectures/) (PDF/PPT)

## Other databases (reference)

* [GROUP BY and ROLLUP in MySQL](./groupby_and_rollup_mysql/)
* [GROUP BY, ROLLUP, and CUBE in Snowflake](./groupby_and_cube_snowflake/)
* [Star schema and 20+ OLAP queries](./OLAP_sales_example/Star_Schema_and_OLAP_queries.md)
