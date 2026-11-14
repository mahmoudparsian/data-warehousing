# Demo of "Memory" & "Persistent"  Database using DuckDB

	In DuckDB, the primary difference between a memory 
	(in-memory) and a non-memory (persistent) database 
	is data durability. While both use the same high
	performance vectorized execution engine, they differ 
	in how they handle storage and startup. 

---

## Key Differences at a Glance

|Feature         |In-Memory Database (:memory:)                 | Persistent Database (file.db) |
|----------------|----------------------------------------------|------------------------------------|
|Storage         |Data exists only in RAM.                      | Data is saved to a file on disk.|
|Durability      |All data is lost when the process ends.       | Data remains available across sessions.|
|Startup Speed   |Instant; creates a fresh environment.         |  Depends on file size and metadata scanning.|
|Performance     |Can be faster for small datasets; no disk I/O.|  May be faster for large datasets due to built-in compression.|
|Memory Limit    |Bound by available system RAM.                | Can exceed RAM by spilling to disk.|

---

# Check your DuckDb environment

> Recorded in class on 2026-04-02 with DuckDB 1.5.1. Re-checked on **DuckDB 2.0.0** (2026-11-13): same results.
> Queries without `ORDER BY` (`DISTINCT`, `GROUP BY`) may list their rows in a different order on every run.

```
% type duckdb
duckdb is /opt/homebrew/bin/duckdb

% duckdb --version
v1.5.1 (Variegata) 7dbb2e646f
```

---

# Memory database

```
% duckdb
DuckDB v1.5.1 (Variegata)
Enter ".help" for usage hints.

memory D CREATE TABLE sales 
         AS SELECT * 
         FROM read_csv('https://raw.githubusercontent.com/mahmoudparsian/data-warehousing/refs/heads/main/resources/data/sales_16_records.csv');

memory D desc sales;
┌─────────────────┐
│      sales      │
│                 │
│ country varchar │
│ product varchar │
│ price   bigint  │
└─────────────────┘

memory D select count(*) from sales;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│           16 │
└──────────────┘

memory D select * from sales;
┌─────────┬──────────┬───────┐
│ country │ product  │ price │
│ varchar │ varchar  │ int64 │
├─────────┼──────────┼───────┤
│ FRANCE  │ TV       │   200 │
│ FRANCE  │ TV       │   400 │
│ FRANCE  │ BIKE     │   400 │
│ FRANCE  │ BIKE     │   600 │
│ USA     │ TV       │   200 │
│ USA     │ TV       │   180 │
│ USA     │ TV       │   240 │
│ USA     │ BIKE     │   500 │
│ USA     │ BIKE     │   700 │
│ USA     │ COMPUTER │   800 │
│ USA     │ COMPUTER │   700 │
│ USA     │ COMPUTER │   600 │
│ CANADA  │ TV       │   300 │
│ CANADA  │ TV       │   200 │
│ CANADA  │ COMPUTER │   500 │
│ CANADA  │ COMPUTER │   900 │
└─────────┴──────────┴───────┘
  16 rows          3 columns
  
memory D SELECT DISTINCT country 
         FROM sales;
┌─────────┐
│ country │
│ varchar │
├─────────┤
│ USA     │
│ FRANCE  │
│ CANADA  │
└─────────┘

memory D SELECT  country from sales;
┌─────────┐
│ country │
│ varchar │
├─────────┤
│ FRANCE  │
│ FRANCE  │
│ FRANCE  │
│ FRANCE  │
│ USA     │
│ USA     │
│ USA     │
│ USA     │
│ USA     │
│ USA     │
│ USA     │
│ USA     │
│ CANADA  │
│ CANADA  │
│ CANADA  │
│ CANADA  │
└─────────┘
  16 rows
  
memory D SELECT DISTINCT country 
         FROM sales;
┌─────────┐
│ country │
│ varchar │
├─────────┤
│ USA     │
│ FRANCE  │
│ CANADA  │
└─────────┘


memory D SELECT country, 
                SUM(price) 
         FROM sales 
         GROUP BY country;
┌─────────┬────────────┐
│ country │ sum(price) │
│ varchar │   int128   │
├─────────┼────────────┤
│ FRANCE  │       1600 │
│ CANADA  │       1900 │
│ USA     │       3920 │
└─────────┴────────────┘

memory D SELECT country, SUM(price) 
         FROM sales 
         GROUP BY country 
         HAVING SUM(price) > 1700;
┌─────────┬────────────┐
│ country │ sum(price) │
│ varchar │   int128   │
├─────────┼────────────┤
│ CANADA  │       1900 │
│ USA     │       3920 │
└─────────┴────────────┘

memory D SELECT country, SUM(price) as total_price
         FROM sales
         GROUP BY country
         HAVING total_price  > 1700;
┌─────────┬─────────────┐
│ country │ total_price │
│ varchar │   int128    │
├─────────┼─────────────┤
│ USA     │        3920 │
│ CANADA  │        1900 │
└─────────┴─────────────┘

memory D SELECT * 
         FROM sales 
         WHERE  country = 'FRANCE';
┌─────────┬─────────┬───────┐
│ country │ product │ price │
│ varchar │ varchar │ int64 │
├─────────┼─────────┼───────┤
│ FRANCE  │ TV      │   200 │
│ FRANCE  │ TV      │   400 │
│ FRANCE  │ BIKE    │   400 │
│ FRANCE  │ BIKE    │   600 │
└─────────┴─────────┴───────┘
memory D SELECT country, 
                SUM(price) as total_price
         FROM sales
         GROUP BY country;
┌─────────┬─────────────┐
│ country │ total_price │
│ varchar │   int128    │
├─────────┼─────────────┤
│ USA     │        3920 │
│ FRANCE  │        1600 │
│ CANADA  │        1900 │
└─────────┴─────────────┘

memory D SELECT country, 
                SUM(price) as total_price
         FROM sales
         GROUP BY country
         HAVING total_price > 2000;
┌─────────┬─────────────┐
│ country │ total_price │
│ varchar │   int128    │
├─────────┼─────────────┤
│ USA     │        3920 │
└─────────┴─────────────┘


memory D select MAX(price) from sales;
┌────────────┐
│ max(price) │
│   int64    │
├────────────┤
│        900 │
└────────────┘

memory D SELECT product, MAX(price)
         FROM sales
         GROUP BY product;
┌──────────┬────────────┐
│ product  │ max(price) │
│ varchar  │   int64    │
├──────────┼────────────┤
│ COMPUTER │        900 │
│ TV       │        400 │
│ BIKE     │        700 │
└──────────┴────────────┘

memory D SELECT country, MAX(price)
         FROM sales
         GROUP BY country;
┌─────────┬────────────┐
│ country │ max(price) │
│ varchar │   int64    │
├─────────┼────────────┤
│ USA     │        800 │
│ FRANCE  │        600 │
│ CANADA  │        900 │
└─────────┴────────────┘

memory D SELECT country, product, 
                MAX(price) as max_price
         FROM sales
         GROUP BY country, product;
┌─────────┬──────────┬────────────┐
│ country │ product  │ max_price  │
│ varchar │ varchar  │   int64    │
├─────────┼──────────┼────────────┤
│ FRANCE  │ TV       │        400 │
│ USA     │ COMPUTER │        800 │
│ USA     │ TV       │        240 │
│ FRANCE  │ BIKE     │        600 │
│ CANADA  │ TV       │        300 │
│ USA     │ BIKE     │        700 │
│ CANADA  │ COMPUTER │        900 │
└─────────┴──────────┴────────────┘
memory D
.exit

```

# Persistent database

```
% duckdb sales.duckdb
DuckDB v1.5.1 (Variegata)
Enter ".help" for usage hints.
sales D CREATE TABLE sales
        AS SELECT *
        FROM read_csv('https://raw.githubusercontent.com/mahmoudparsian/data-warehousing/refs/heads/main/resources/data/sales_16_records.csv');
sales D SHOW TABLES;
┌─────────┐
│  name   │
│ varchar │
├─────────┤
│ sales   │
└─────────┘
sales D SELECT COUNT(*) 
        FROM sales;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│           16 │
└──────────────┘
sales D SELECT * 
      FROM sales 
      LIMIT 2;
┌─────────┬─────────┬───────┐
│ country │ product │ price │
│ varchar │ varchar │ int64 │
├─────────┼─────────┼───────┤
│ FRANCE  │ TV      │   200 │
│ FRANCE  │ TV      │   400 │
└─────────┴─────────┴───────┘
sales D .exit
%
```

###  Your data/tables are persisted

# Verify Persistent Database

```
% duckdb sales.duckdb
DuckDB v1.5.1 (Variegata)
Enter ".help" for usage hints.
sales D SHOW TABLES;
┌─────────┐
│  name   │
│ varchar │
├─────────┤
│ sales   │
└─────────┘
sales D SELECT COUNT(*) 
        FROM sales;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│           16 │
└──────────────┘
sales D SELECT * 
      FROM sales 
      LIMIT 2;
┌─────────┬─────────┬───────┐
│ country │ product │ price │
│ varchar │ varchar │ int64 │
├─────────┼─────────┼───────┤
│ FRANCE  │ TV      │   200 │
│ FRANCE  │ TV      │   400 │
└─────────┴─────────┴───────┘
sales D .exit
```


# Persistent database is here:

```
% ls -l sales.duckdb
-rw-r--r--@ 1 max  staff  536576 Apr  2 22:33 sales.duckdb
```
