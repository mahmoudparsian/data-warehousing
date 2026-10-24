---
marp: true
theme: default
paginate: true
title: Week 5 — Session 2 — Medallion as a Lakehouse (files + DuckDB)
---

# Week 5 — Session 2
## Medallion as a Lakehouse: Layers as Files

---

# 🏞️ Warehouse · Lake · Lakehouse

| | Data warehouse | Data lake | **Lakehouse** |
|---|---|---|---|
| Stores | tables inside a DBMS | any files in cheap storage | **open files** (Parquet) in cheap storage |
| Schema | on write (strict) | on read (anything goes) | on write **for Silver/Gold** |
| Readers | that DBMS | many tools, little trust | **many tools, trusted layers** |
| Example | MySQL, Snowflake tables | S3 bucket of CSV/JSON | S3/folders + Parquet/Delta/Iceberg + DuckDB/Spark |

👉 Medallion layers map naturally to **folders**: `bronze/`, `silver/`, `gold/`

---

# 🟫 Bronze = the files that arrived

DuckDB queries files **in place**, with no load step:

```sql
-- what is there?
SELECT COUNT(*) AS files, SUM(size) AS bytes
FROM read_blob('sales_1400_messy_records/*.csv');      -- 1 file, 132,025 bytes

-- a view = "how to read the files", not a copy
CREATE VIEW bronze_sales AS
SELECT *, filename AS _source_file                       -- lineage for free
FROM read_csv('sales_1400_messy_records/sale_records_1400_messy.csv',
              all_varchar = true, filename = true);
```

- `filename = true` adds the source file path to every row
- A glob (`*.csv`) picks up **new files automatically**

---

# 📦 CSV vs Parquet

| | CSV | Parquet |
|---|---|---|
| Layout | row by row, text | **column by column**, binary |
| Types | none (everything is text) | stored in the file |
| Size | large | typically **2–10× smaller** (compression + encoding) |
| Read 2 of 20 columns | reads everything | reads **only those 2 columns** |

👉 Bronze: keep what arrived (often CSV/JSON) · Silver & Gold: **Parquet**

---

# ⚪ Writing Silver as Partitioned Parquet

```sql
COPY (
  SELECT upper(trim(product))              AS product,
         CAST(quantity AS INT)             AS quantity,
         CAST(unit_price AS DECIMAL(10,2)) AS unit_price
  FROM bronze_sales
  WHERE product IS NOT NULL
) TO 'silver_sales' (FORMAT parquet, PARTITION_BY (product));
```

```
silver_sales/product=COMPUTER/data_0.parquet
silver_sales/product=EBIKE/data_0.parquet
silver_sales/product=IPAD/data_0.parquet
silver_sales/product=IPHONE/data_0.parquet
silver_sales/product=TV/data_0.parquet
silver_sales/product=WATCH/data_0.parquet
```

👉 The partition column lives in the **folder name** (`product=TV`), not inside the file (Hive-style)

---

# ✂️ Reading Partitions: Pruning

```sql
SELECT COUNT(*)
FROM read_parquet('silver_sales/*/*.parquet', hive_partitioning = true)
WHERE product = 'TV';                                    -- 233
```

`EXPLAIN ANALYZE` shows:

```
READ_PARQUET
File Filters: (product = 'TV')
Scanning Files: 1/6
```

- DuckDB **skips 5 of 6 files** without opening them
- Partition by what you **filter on most**: usually date (year, month)
- Don't over-partition: thousands of tiny files are slow

---

# 🟡 Gold as Files

```sql
COPY (SELECT product, SUM(quantity * unit_price) AS gross_revenue
      FROM read_parquet('silver_sales/*/*.parquet', hive_partitioning = true)
      GROUP BY product)
TO 'gold_revenue_by_product.parquet' (FORMAT parquet);

SELECT * FROM 'gold_revenue_by_product.parquet';          -- query a file like a table
SELECT name, type FROM parquet_schema('gold_revenue_by_product.parquet');
```

- One Gold file per business question / dashboard
- Tableau, Python (pandas/polars), Spark, DuckDB all read the **same** file
- Parquet is **self-describing**: names and types travel with the data

---

# 🔁 Same Medallion, Two Implementations

| | Lab 5.1: schemas in one DuckDB | Lab 5.2: folders of files |
|---|---|---|
| Bronze | `bronze.sales` table | view over raw CSVs |
| Silver | `silver.sales` table | `silver_…/year=…/*.parquet` |
| Gold | `gold.*` tables | `gold_*.parquet` |
| Good at | transactions, constraints, one file | open formats, any engine, scale, cheap storage |

👉 The **layer idea** is the same; only where the data lives changes

---

# ✅ Summary

- Lakehouse = lake storage + warehouse discipline (Medallion layers, schemas, quality)
- DuckDB reads CSV/Parquet **in place**: `read_csv`, `read_parquet`, `read_blob`, `glob`
- `COPY … (FORMAT parquet, PARTITION_BY (…))` writes a partitioned layer
- `hive_partitioning = true` + a filter → **partition pruning**

👉 Now: **Lab 5.2** (30 minutes)
