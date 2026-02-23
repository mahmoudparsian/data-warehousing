
# 🦆 What is DuckDB? <br> Graduate-Level Tutorial
#### Comparison with MySQL from an Analytics Perspective

---

# Slide 1 — What is DuckDB?

DuckDB is an **in-process analytical SQL database engine**.

Think of it as:

> SQLite for Analytics

It is designed for:

- OLAP workloads
- Columnar storage
- Large aggregations
- Data science integration
- Embedded analytics

It runs inside your application (no server required).

---

# Slide 2 — DuckDB Architecture

## MySQL (Traditional RDBMS)
Client → Server → Storage Engine (InnoDB)

## DuckDB
Application → DuckDB Engine (embedded)

Key differences:

- No server process
- No network overhead
- Runs inside Python, R, CLI, C++
- Ideal for local analytics

---

# Slide 3 — OLTP vs OLAP Design Philosophy

| Feature | MySQL | DuckDB |
|----------|--------|--------|
| Primary Use | OLTP | OLAP |
| Data Layout | Row-based | Columnar |
| Write-heavy workloads | Excellent | Moderate |
| Large scans | Slower | Very Fast |
| Embedded usage | No | Yes |

DuckDB is optimized for **analytical queries**, not high-concurrency transactions.

---

# Slide 4 — Columnar Storage Advantage

DuckDB stores data column-wise.

Example:

```sql
SELECT SUM(total_amount) 
FROM sales;
```

* DuckDB reads only the `total_amount` column.

* MySQL reads entire rows.

* Columnar = fewer I/O operations = faster aggregation.

---

# Slide 5 — Analytical SQL Capabilities

DuckDB supports:

- CUBE
- ROLLUP
- GROUPING SETS
- Advanced window functions
- Statistical functions (STDDEV, VARIANCE)
- Direct Parquet/CSV querying

MySQL:

- Supports ROLLUP
- No native CUBE
- Limited GROUPING SETS support

DuckDB follows modern SQL analytics standards more closely.

---

# Slide 6 — Data Integration & Files

DuckDB can query files directly:

```sql
SELECT *
FROM 'sales.parquet';
```

Or:

```sql
SELECT *
FROM read_csv_auto('sales.csv');
```

No import step required.

MySQL requires explicit data loading into tables.

---

# Slide 7 — Performance Model

DuckDB uses:

- Vectorized execution
- Parallel query processing
- Late materialization
- Automatic compression

MySQL focuses on:

- Index lookups
- Transaction consistency
- Row-based updates

DuckDB excels at full-table scans and aggregations.

---

# Slide 8 — Use Cases Comparison

### Use MySQL When:
- Building web applications
- High concurrency writes
- ACID transactional systems
- Operational systems

### Use DuckDB When:
- Running analytical workloads
- Teaching data warehousing
- Prototyping star schemas
- Local BI / data science experiments

They complement each other.

---

# Slide 9 — Example: CUBE Comparison

## DuckDB
```sql
SELECT year, category, SUM(total_amount)
FROM sales
GROUP BY CUBE(year, category);
```

## MySQL
Requires manual UNION ALL simulation.

DuckDB provides richer multidimensional analytics out-of-the-box.

---

# Slide 10 — Final Takeaways (Graduate-Level Perspective)

DuckDB is:

- A modern analytical engine
- Columnar and vectorized
- Embedded and lightweight
- Ideal for OLAP and teaching

MySQL is:

- Mature transactional RDBMS
- Excellent for OLTP
- Less optimized for heavy analytical workloads

Conclusion:

> MySQL = Operational Database  
> DuckDB = Analytical Engine  

For advanced analytics education, DuckDB provides a powerful and modern SQL platform.

---

# End of Slides
