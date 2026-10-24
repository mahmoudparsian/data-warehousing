
# 🦆 Introduction to DuckDB
## For MySQL Users (With Live Demo Schema)

---

# Slide 1 — What is DuckDB?

DuckDB is an **in-process analytical SQL database**.

Think of it as:

> SQLite for Analytics

Designed for:

- OLAP workloads
- Columnar execution
- Large aggregations
- Data science integration

---

# Slide 2 — DuckDB vs MySQL

| Feature | MySQL | DuckDB |
|----------|--------|--------|
| Designed for | OLTP | OLAP |
| Storage | Row-based | Columnar |
| Server required | Yes | No |
| CUBE support | No | Yes |
| GROUPING SETS | No | Yes |
| Embedded | No | Yes |

---

# Slide 3 — Architecture Difference

## MySQL
Client → Server → Storage Engine

## DuckDB
Application → DuckDB Engine (embedded)

No server required.

---

# Slide 4 — Demo Schema (Star-Style Mini Model)

We will use a small sales table for OLAP demo.

```sql
CREATE TABLE sales (
    product VARCHAR,
    quarter VARCHAR,
    region  VARCHAR,
    sales   INTEGER
);
```

---

# Slide 5 — Insert Sample Rows

```sql
INSERT INTO sales VALUES
('A','Q1','Europe',10),
('A','Q1','America',20),
('A','Q2','Europe',20),
('A','Q2','America',50),
('A','Q3','America',20),
('A','Q4','Europe',10),
('A','Q4','America',30),
('B','Q1','Europe',40),
('B','Q1','America',60),
('B','Q2','Europe',20),
('B','Q2','America',10),
('B','Q3','America',20),
('B','Q4','Europe',10),
('B','Q4','America',40),
('C','Q1','Europe',50),
('C','Q1','America',60),
('C','Q2','Europe',35),
('C','Q2','America',45);
```

---

# Slide 6 — Verify Data

```sql
SELECT * 
FROM sales;

┌─────────┬─────────┬─────────┬───────┐
│ product │ quarter │ region  │ sales │
│ varchar │ varchar │ varchar │ int32 │
├─────────┼─────────┼─────────┼───────┤
│ A       │ Q1      │ Europe  │    10 │
│ A       │ Q1      │ America │    20 │
│ A       │ Q2      │ Europe  │    20 │
│ A       │ Q2      │ America │    50 │
│ A       │ Q3      │ America │    20 │
│ A       │ Q4      │ Europe  │    10 │
│ A       │ Q4      │ America │    30 │
│ B       │ Q1      │ Europe  │    40 │
│ B       │ Q1      │ America │    60 │
│ B       │ Q2      │ Europe  │    20 │
│ B       │ Q2      │ America │    10 │
│ B       │ Q3      │ America │    20 │
│ B       │ Q4      │ Europe  │    10 │
│ B       │ Q4      │ America │    40 │
│ C       │ Q1      │ Europe  │    50 │
│ C       │ Q1      │ America │    60 │
│ C       │ Q2      │ Europe  │    35 │
│ C       │ Q2      │ America │    45 │
├─────────┴─────────┴─────────┴───────┤
│ 18 rows                   4 columns │
└─────────────────────────────────────┘
```

---

# Slide 7 — Basic Aggregation

```sql
SELECT product, 
       SUM(sales) AS total_sales
FROM sales
GROUP BY product
ORDER BY product;

┌─────────┬─────────────┐
│ product │ total_sales │
│ varchar │   int128    │
├─────────┼─────────────┤
│ A       │         160 │
│ B       │         200 │
│ C       │         190 │
└─────────┴─────────────┘
```

---

# Slide 8 — ROLLUP Example

```sql
SELECT product, quarter, 
       SUM(sales) AS total_sales
FROM sales
GROUP BY ROLLUP(product, quarter)
ORDER BY product, quarter;

┌─────────┬─────────┬─────────────┐
│ product │ quarter │ total_sales │
│ varchar │ varchar │   int128    │
├─────────┼─────────┼─────────────┤
│ A       │ Q1      │          30 │
│ A       │ Q2      │          70 │
│ A       │ Q3      │          20 │
│ A       │ Q4      │          40 │
│ A       │ NULL    │         160 │
│ B       │ Q1      │         100 │
│ B       │ Q2      │          30 │
│ B       │ Q3      │          20 │
│ B       │ Q4      │          50 │
│ B       │ NULL    │         200 │
│ C       │ Q1      │         110 │
│ C       │ Q2      │          80 │
│ C       │ NULL    │         190 │
│ NULL    │ NULL    │         550 │
├─────────┴─────────┴─────────────┤
│ 14 rows               3 columns │
└─────────────────────────────────┘
```

ROLLUP generates:

- (product, quarter)
- (product subtotal)
- (grand total)

---

# Slide 9 — CUBE Example

```sql
.maxrows 1000
SELECT product, quarter, region,
       SUM(sales) AS total_sales
FROM sales
GROUP BY CUBE(product, quarter, region)
ORDER BY product, quarter, region;

┌─────────┬─────────┬─────────┬─────────────┐
│ product │ quarter │ region  │ total_sales │
│ varchar │ varchar │ varchar │   int128    │
├─────────┼─────────┼─────────┼─────────────┤
│ A       │ Q1      │ America │          20 │
│ A       │ Q1      │ Europe  │          10 │
│ A       │ Q1      │ NULL    │          30 │
│ A       │ Q2      │ America │          50 │
│ A       │ Q2      │ Europe  │          20 │
│ A       │ Q2      │ NULL    │          70 │
│ A       │ Q3      │ America │          20 │
│ A       │ Q3      │ NULL    │          20 │
│ A       │ Q4      │ America │          30 │
│ A       │ Q4      │ Europe  │          10 │
│ A       │ Q4      │ NULL    │          40 │
│ A       │ NULL    │ America │         120 │
│ A       │ NULL    │ Europe  │          40 │
│ A       │ NULL    │ NULL    │         160 │
│ B       │ Q1      │ America │          60 │
│ B       │ Q1      │ Europe  │          40 │
│ B       │ Q1      │ NULL    │         100 │
│ B       │ Q2      │ America │          10 │
│ B       │ Q2      │ Europe  │          20 │
│ B       │ Q2      │ NULL    │          30 │
│ B       │ Q3      │ America │          20 │
│ B       │ Q3      │ NULL    │          20 │
│ B       │ Q4      │ America │          40 │
│ B       │ Q4      │ Europe  │          10 │
│ B       │ Q4      │ NULL    │          50 │
│ B       │ NULL    │ America │         130 │
│ B       │ NULL    │ Europe  │          70 │
│ B       │ NULL    │ NULL    │         200 │
│ C       │ Q1      │ America │          60 │
│ C       │ Q1      │ Europe  │          50 │
│ C       │ Q1      │ NULL    │         110 │
│ C       │ Q2      │ America │          45 │
│ C       │ Q2      │ Europe  │          35 │
│ C       │ Q2      │ NULL    │          80 │
│ C       │ NULL    │ America │         105 │
│ C       │ NULL    │ Europe  │          85 │
│ C       │ NULL    │ NULL    │         190 │
│ NULL    │ Q1      │ America │         140 │
│ NULL    │ Q1      │ Europe  │         100 │
│ NULL    │ Q1      │ NULL    │         240 │
│ NULL    │ Q2      │ America │         105 │
│ NULL    │ Q2      │ Europe  │          75 │
│ NULL    │ Q2      │ NULL    │         180 │
│ NULL    │ Q3      │ America │          40 │
│ NULL    │ Q3      │ NULL    │          40 │
│ NULL    │ Q4      │ America │          70 │
│ NULL    │ Q4      │ Europe  │          20 │
│ NULL    │ Q4      │ NULL    │          90 │
│ NULL    │ NULL    │ America │         355 │
│ NULL    │ NULL    │ Europe  │         195 │
│ NULL    │ NULL    │ NULL    │         550 │
├─────────┴─────────┴─────────┴─────────────┤
│ 51 rows                         4 columns │
└───────────────────────────────────────────┘
```

CUBE generates all 2³ combinations automatically.

---

# Slide 10 — GROUPING() Indicator

```sql
SELECT product,
       quarter,
       region,
       SUM(sales) AS total_sales,
       GROUPING(product) AS g_product,
       GROUPING(quarter) AS g_quarter,
       GROUPING(region)  AS g_region
FROM sales
GROUP BY CUBE(product, quarter, region);

┌─────────┬─────────┬─────────┬─────────────┬───────────┬───────────┬──────────┐
│ product │ quarter │ region  │ total_sales │ g_product │ g_quarter │ g_region │
│ varchar │ varchar │ varchar │   int128    │   int64   │   int64   │  int64   │
├─────────┼─────────┼─────────┼─────────────┼───────────┼───────────┼──────────┤
│ A       │ Q4      │ America │          30 │         0 │         0 │        0 │
│ NULL    │ Q3      │ America │          40 │         1 │         0 │        0 │
│ C       │ NULL    │ America │         105 │         0 │         1 │        0 │
│ NULL    │ Q1      │ America │         140 │         1 │         0 │        0 │
│ NULL    │ NULL    │ America │         355 │         1 │         1 │        0 │
│ NULL    │ Q4      │ America │          70 │         1 │         0 │        0 │
│ NULL    │ Q2      │ America │         105 │         1 │         0 │        0 │
│ NULL    │ NULL    │ Europe  │         195 │         1 │         1 │        0 │
│ C       │ Q2      │ NULL    │          80 │         0 │         0 │        1 │
│ B       │ Q4      │ America │          40 │         0 │         0 │        0 │
│ C       │ Q1      │ America │          60 │         0 │         0 │        0 │
│ A       │ Q3      │ America │          20 │         0 │         0 │        0 │
│ C       │ NULL    │ Europe  │          85 │         0 │         1 │        0 │
│ A       │ NULL    │ America │         120 │         0 │         1 │        0 │
│ NULL    │ Q1      │ Europe  │         100 │         1 │         0 │        0 │
│ A       │ Q3      │ NULL    │          20 │         0 │         0 │        1 │
│ C       │ Q1      │ NULL    │         110 │         0 │         0 │        1 │
│ A       │ Q4      │ Europe  │          10 │         0 │         0 │        0 │
│ C       │ NULL    │ NULL    │         190 │         0 │         1 │        1 │
│ B       │ Q3      │ NULL    │          20 │         0 │         0 │        1 │
│ A       │ Q1      │ America │          20 │         0 │         0 │        0 │
│ B       │ Q2      │ Europe  │          20 │         0 │         0 │        0 │
│ A       │ NULL    │ Europe  │          40 │         0 │         1 │        0 │
│ NULL    │ Q2      │ Europe  │          75 │         1 │         0 │        0 │
│ B       │ NULL    │ NULL    │         200 │         0 │         1 │        1 │
│ B       │ Q1      │ NULL    │         100 │         0 │         0 │        1 │
│ A       │ Q2      │ Europe  │          20 │         0 │         0 │        0 │
│ B       │ Q1      │ Europe  │          40 │         0 │         0 │        0 │
│ C       │ Q2      │ America │          45 │         0 │         0 │        0 │
│ NULL    │ Q2      │ NULL    │         180 │         1 │         0 │        1 │
│ NULL    │ Q4      │ NULL    │          90 │         1 │         0 │        1 │
│ NULL    │ Q1      │ NULL    │         240 │         1 │         0 │        1 │
│ NULL    │ NULL    │ NULL    │         550 │         1 │         1 │        1 │
│ B       │ Q2      │ NULL    │          30 │         0 │         0 │        1 │
│ B       │ Q4      │ NULL    │          50 │         0 │         0 │        1 │
│ A       │ Q1      │ Europe  │          10 │         0 │         0 │        0 │
│ B       │ NULL    │ America │         130 │         0 │         1 │        0 │
│ A       │ NULL    │ NULL    │         160 │         0 │         1 │        1 │
│ A       │ Q2      │ NULL    │          70 │         0 │         0 │        1 │
│ A       │ Q4      │ NULL    │          40 │         0 │         0 │        1 │
│ B       │ Q4      │ Europe  │          10 │         0 │         0 │        0 │
│ C       │ Q1      │ Europe  │          50 │         0 │         0 │        0 │
│ A       │ Q1      │ NULL    │          30 │         0 │         0 │        1 │
│ B       │ Q2      │ America │          10 │         0 │         0 │        0 │
│ A       │ Q2      │ America │          50 │         0 │         0 │        0 │
│ B       │ Q1      │ America │          60 │         0 │         0 │        0 │
│ B       │ Q3      │ America │          20 │         0 │         0 │        0 │
│ C       │ Q2      │ Europe  │          35 │         0 │         0 │        0 │
│ NULL    │ Q3      │ NULL    │          40 │         1 │         0 │        1 │
│ B       │ NULL    │ Europe  │          70 │         0 │         1 │        0 │
│ NULL    │ Q4      │ Europe  │          20 │         1 │         0 │        0 │
├─────────┴─────────┴─────────┴─────────────┴───────────┴───────────┴──────────┤
│ 51 rows                                                            7 columns │
└──────────────────────────────────────────────────────────────────────────────┘
```

GROUPING() identifies subtotal rows.

---

# Slide 11 — GROUPING SETS

```sql
SELECT product, quarter, region,
       SUM(sales) AS total_sales
FROM sales
GROUP BY GROUPING SETS (
    (product, quarter, region),
    (product, quarter),
    (product),
    ()
);

┌─────────┬─────────┬─────────┬─────────────┐
│ product │ quarter │ region  │ total_sales │
│ varchar │ varchar │ varchar │   int128    │
├─────────┼─────────┼─────────┼─────────────┤
│ A       │ Q2      │ Europe  │          20 │
│ B       │ Q1      │ Europe  │          40 │
│ C       │ Q2      │ America │          45 │
│ A       │ Q1      │ NULL    │          30 │
│ B       │ Q4      │ America │          40 │
│ C       │ Q1      │ America │          60 │
│ B       │ Q1      │ NULL    │         100 │
│ C       │ NULL    │ NULL    │         190 │
│ B       │ Q2      │ NULL    │          30 │
│ B       │ Q4      │ NULL    │          50 │
│ B       │ Q3      │ NULL    │          20 │
│ NULL    │ NULL    │ NULL    │         550 │
│ B       │ Q2      │ America │          10 │
│ A       │ Q1      │ America │          20 │
│ A       │ Q3      │ America │          20 │
│ B       │ Q4      │ Europe  │          10 │
│ C       │ Q1      │ Europe  │          50 │
│ A       │ Q4      │ Europe  │          10 │
│ A       │ Q2      │ NULL    │          70 │
│ A       │ Q4      │ NULL    │          40 │
│ C       │ Q2      │ NULL    │          80 │
│ A       │ NULL    │ NULL    │         160 │
│ B       │ NULL    │ NULL    │         200 │
│ A       │ Q4      │ America │          30 │
│ A       │ Q2      │ America │          50 │
│ B       │ Q1      │ America │          60 │
│ B       │ Q3      │ America │          20 │
│ C       │ Q2      │ Europe  │          35 │
│ A       │ Q1      │ Europe  │          10 │
│ B       │ Q2      │ Europe  │          20 │
│ A       │ Q3      │ NULL    │          20 │
│ C       │ Q1      │ NULL    │         110 │
├─────────┴─────────┴─────────┴─────────────┤
│ 32 rows                         4 columns │
└───────────────────────────────────────────┘
```

Explicit control over aggregation combinations.

---

# Slide 12 — Columnar Advantage Demo

Aggregation example:

```sql
SELECT SUM(sales) 
FROM sales;
```

DuckDB reads only one column (sales).

Columnar design → Faster OLAP.

---

# Slide 13 — Querying CSV Directly

```sql
SELECT *
FROM read_csv_auto('sales.csv');
```

No import step required.

---

# Slide 14 — When to Use DuckDB

- OLAP teaching
- Analytics
- Window functions
- CUBE / GROUPING SETS
- Local BI experiments

---

# Slide 15 — Final Teaching Message

MySQL = Transactional database 
 
DuckDB = Analytical engine  

They complement each other.

---

# ✅ End of Extended Slides
