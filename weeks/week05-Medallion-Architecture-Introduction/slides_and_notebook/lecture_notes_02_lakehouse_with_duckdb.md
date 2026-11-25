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

# 🟫 Bronze = the Files That Arrived

In a lakehouse, Bronze **is** the folder of raw files: nothing is copied or changed. DuckDB reads them **in place**:

```sql
-- what is there? (metadata only, no parsing)
SELECT COUNT(*) AS files, SUM(size) AS bytes
FROM read_blob('sales_1400_messy_records/*.csv');                -- 1 file, 132,025 bytes

-- a view = "how to read the raw files as text", not a copy
CREATE VIEW bronze_sales AS
SELECT *, filename AS _source_file                                -- lineage for free
FROM read_csv('sales_1400_messy_records/*.csv', all_varchar = true, filename = true);
```

- Same Bronze rules as in Session 1: **as received**, all text, never fixed. New files are **added** to the folder.
- A glob (`*.csv`) picks up next month's file automatically; `filename = true` says which file each row came from.

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

# ⚪ Silver = the Rules' Output, Written as Parquet

Silver applies **the same business rules** as Session 1 and Lab 5.1 (dedup → quarantine → flag cancelled → fix discount → price).
Only the **storage** changes: the result goes to files.

```sql
-- silver.sales and silver.rejected built exactly as in Lab 5.1, then:
COPY (SELECT * FROM silver.sales)                         -- valid + flagged (is_cancelled)
TO 'silver_sales' (FORMAT parquet, PARTITION_BY (product));

COPY (SELECT * FROM silver.rejected)                      -- quarantine, with reject_reason
TO 'silver_rejected.parquet' (FORMAT parquet);
```

```
silver_sales/product=COMPUTER/data_0.parquet      silver_sales/product=IPHONE/data_0.parquet
silver_sales/product=EBIKE/data_0.parquet         silver_sales/product=TV/data_0.parquet
silver_sales/product=IPAD/data_0.parquet          silver_sales/product=WATCH/data_0.parquet
```

- The partition column lives in the **folder name** (`product=TV`), not inside the file (Hive-style).
- The rejected rows are written too: a lakehouse keeps every fate, exactly like the schemas did. **1,400 = 31 + 78 + 33 + 1,258** still holds.
- `COPY` creates only the **last** folder: `'lake/silver/sales'` fails unless `lake/silver/` exists.

---

# ✂️ Reading Partitions: Pruning

```sql
SELECT COUNT(*)
FROM read_parquet('silver_sales/*/*.parquet', hive_partitioning = true)
WHERE product = 'TV';                                    -- 214 (212 valid + 2 cancelled)
```

`EXPLAIN ANALYZE` shows:

```
READ_PARQUET
File Filters: product = 'TV'
Scanning Files: 1/6
```

- DuckDB **skips 5 of 6 files** without opening them.
- Partition by what you **filter on most**: usually a date (year, month).
- Don't over-partition: thousands of tiny files are slow.

---

# 🟡 Gold as Files

```sql
COPY (SELECT product,
             COUNT(*)              AS sales,
             SUM(final_sale_price) AS revenue           -- after discounts (rule 8)
      FROM read_parquet('silver_sales/*/*.parquet', hive_partitioning = true)
      WHERE NOT is_cancelled                            -- Gold uses the flag explicitly
      GROUP BY product
      ORDER BY revenue DESC)
TO 'gold_revenue_by_product.parquet' (FORMAT parquet);

SELECT * FROM 'gold_revenue_by_product.parquet';         -- IPHONE 352 sales, 562,276.00 … WATCH 143, 92,142.50
SELECT name, type FROM parquet_schema('gold_revenue_by_product.parquet');
```

- The same numbers as Lab 5.1's `gold.revenue_by_product`: only the storage changed.
- One Gold file per business question / dashboard; Tableau, pandas, Spark and DuckDB all read the **same** file.
- Parquet is **self-describing**: column names and types travel with the data.

---

# 🔁 Same Medallion, Two Implementations

| | Lab 5.1: schemas in one DuckDB | Lab 5.2: folders of files |
|---|---|---|
| Bronze | `bronze.sales_raw` table (all text + lineage) | the raw CSV folder + a view (`filename` = lineage) |
| Silver | `silver.sales`, `silver.rejected` tables | `silver_sales/product=…/*.parquet`, `silver_rejected.parquet` |
| Gold | `gold.*` tables | `gold_*.parquet` |
| Good at | transactions, constraints, one file | open formats, any engine, scale, cheap storage |

👉 The **layers, rules, fates and reconciliation** are the same; only where the data lives changes.

---

# ✅ Summary

- Lakehouse = lake storage (open files) + warehouse discipline (Medallion layers, rules, reconciliation)
- DuckDB reads CSV/Parquet **in place**: `read_csv`, `read_parquet`, `read_blob`, `glob`
- `COPY … (FORMAT parquet, PARTITION_BY (…))` writes a partitioned layer
- `hive_partitioning = true` + a filter → **partition pruning**

👉 Now: **Lab 5.2** (30 minutes)
