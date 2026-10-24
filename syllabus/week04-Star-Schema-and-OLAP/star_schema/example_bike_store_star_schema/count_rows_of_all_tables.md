# Counting Rows for All Tables

How to count rows of all tables in a given database?

You have several ways to get row counts of all tables 
in a MySQL database from the command line.

Assume database: `bike_store`

⸻

✅ Method 1 — Quick Estimated Counts (Fastest)

From MySQL CLI:

```sql
SELECT 
    table_name,
    table_rows
FROM information_schema.tables
WHERE table_schema = 'bike_store';
```

✔ Pros
	•	Very fast
	•	One query

❗ Important

table_rows is estimated for InnoDB tables.
It may not be exact.

⸻

✅ Method 2 — Exact Counts (Accurate but Slower)

Generate dynamic SQL to count rows from each table:

```sql
SELECT 
    CONCAT('SELECT ''', table_name, ''' AS table_name, COUNT(*) FROM ', table_name, ';')
FROM information_schema.tables
WHERE table_schema = 'bike_store';
```

This will output something like:

```sql
SELECT 'customers' AS table_name, COUNT(*) FROM customers;
SELECT 'sales' AS table_name, COUNT(*) FROM sales;
SELECT 'products' AS table_name, COUNT(*) FROM products;
...
```

Copy → paste → execute.

✔ 100% accurate
❗ Slower for large tables (6M+ rows)

⸻

🚀 Method 3 — Fully Automatic Exact Counts (Advanced)

Run this directly:

```sql
SET @schema = 'bike_store';

SELECT GROUP_CONCAT(
    CONCAT('SELECT ''', table_name,
           ''' AS table_name, COUNT(*) AS row_count FROM ',
           table_name)
    SEPARATOR ' UNION ALL '
)
INTO @sql
FROM information_schema.tables
WHERE table_schema = @schema;

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
```


⚡ Quick CLI Shortcut (Outside MySQL)

From Linux/macOS terminal:

```
mysql -u root -p -e "
SELECT table_name, table_rows 
FROM information_schema.tables 
WHERE table_schema='bike_store';"
```
