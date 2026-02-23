# DuckDB: Create Star Schema and Load CSV Files (Step-by-Step)

This guide assumes the following files exist in the same folder:
- `star_schema_duckdb.sql`
- `csv/` directory containing: customers.csv, products.csv, stores.csv, dates.csv, sales.csv

## 1) Create/Open DuckDB database
```bash
duckdb online_sales.duckdb
```

## 2) Create tables
Inside DuckDB:
```sql
.read star_schema_duckdb.sql
```

## 3) Speed settings (recommended)
```sql
PRAGMA threads=8;
PRAGMA memory_limit='2GB';
```

## 4) Load dimensions first
```sql
COPY customers FROM 'csv/customers.csv' (AUTO_DETECT TRUE);
COPY products  FROM 'csv/products.csv'  (AUTO_DETECT TRUE);
COPY stores    FROM 'csv/stores.csv'    (AUTO_DETECT TRUE);
COPY dates     FROM 'csv/dates.csv'     (AUTO_DETECT TRUE);
```

## 5) Load fact table
```sql
COPY sales FROM 'csv/sales.csv' (AUTO_DETECT TRUE);
```

## 6) Build statistics
```sql
ANALYZE;
```

## 7) Validate
```sql
SELECT 'customers' AS t, COUNT(*) AS n FROM customers
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'stores', COUNT(*) FROM stores
UNION ALL SELECT 'dates', COUNT(*) FROM dates
UNION ALL SELECT 'sales', COUNT(*) FROM sales;
```

Example OLAP query:
```sql
SELECT p.category, SUM(s.total_amount) AS total_sales_amount
FROM sales s
JOIN dates d    ON s.date_key = d.date_key
JOIN products p ON s.product_key = p.product_key
WHERE d.year = 2024 AND d.month_of_year = 1
GROUP BY p.category
ORDER BY total_sales_amount DESC;
```
