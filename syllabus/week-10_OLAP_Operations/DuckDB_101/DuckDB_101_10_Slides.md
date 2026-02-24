
# 🦆 DuckDB 101
## A 10-Slide Introduction 

---

# Slide 1 — What is DuckDB?

DuckDB is an **in-process analytical SQL database engine**.

Think of it as:

> SQLite for Analytics

It is lightweight, fast, and designed for OLAP (analytical) workloads.

---

# Slide 2 — Why DuckDB Was Created

**Traditional databases**:

- MySQL → optimized for transactions (OLTP)
- PostgreSQL → general purpose
- Data warehouses → require servers & infrastructure

**DuckDB was created to:**

- Run analytics locally
- Be embedded in applications
- Eliminate server overhead
- Support modern data science workflows

---

# Slide 3 — Key Characteristics

- Columnar storage
- Vectorized execution engine
- Parallel query execution
- Runs inside Python, R, CLI, C++
- Zero configuration
- ACID-compliant

---

# Slide 4 — Architecture

DuckDB runs inside your application.

No client/server model required.

Application → DuckDB Engine → Database File

Advantages:
- No network latency
- No server management
- Ideal for local analytics

---

# Slide 5 — Columnar Storage

DuckDB stores data column-wise.

Example:

```sql
SELECT SUM(total_amount) FROM sales;
```

Only the `total_amount` column is scanned.

This makes aggregations extremely fast.

---

# Slide 6 — Installing DuckDB

### macOS (Homebrew)
```bash
brew install duckdb
```

### Python
```bash
pip install duckdb
```

### Start CLI
```bash
duckdb
```

---

# Slide 7 — Basic SQL Example

Create table:

```sql
CREATE TABLE sales (
    id INTEGER,
    amount DOUBLE
);
```

Insert data:

```sql
INSERT INTO sales 
VALUES 
(1, 100.0), 
(2, 200.0);
```

Query:

```sql
SELECT SUM(amount) 
FROM sales;
```

---

# Slide 8 — Direct File Querying

DuckDB can query files directly.

CSV:

```sql
SELECT * 
FROM read_csv_auto('sales.csv');
```

Parquet:

```sql
SELECT * 
FROM 'sales.parquet';
```

No import step required.

---

# Slide 9 — Advanced SQL Support

DuckDB supports:

- Window functions
- ROLLUP
- CUBE
- GROUPING SETS
- Statistical functions
- Time-series functions

It follows modern SQL standards closely.

---

# Slide 10 — When to Use DuckDB

Use DuckDB when:

- Teaching data warehousing
- Running OLAP queries
- Working with CSV/Parquet files
- Doing exploratory data analysis
- Building embedded analytics tools

DuckDB = Lightweight Analytical Engine  
Fast. Modern. Embedded.

---

# End of Slides
