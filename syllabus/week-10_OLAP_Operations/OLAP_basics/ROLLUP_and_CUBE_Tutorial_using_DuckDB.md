
# 📊 Teaching CUBE and ROLLUP in DuckDB
## Complete OLAP Teaching Module

	DuckDB can be used with Cube in two main ways: 
	by leveraging DuckDB's built-in CUBE and ROLLUP 
	SQL clauses for multi-dimensional aggregation, 
	or by integrating DuckDB as the primary data source 
	within the Cube semantic layer framework. 

---

# Why Use DuckDB for Teaching CUBE?

DuckDB is ideal for OLAP instruction because it supports:

- ✅ ROLLUP
- ✅ CUBE
- ✅ GROUPING SETS
- ✅ GROUPING() function
- ✅ Standard SQL syntax
- ✅ In-memory execution (zero setup)

---

# Feature Comparison

| Feature | MySQL | DuckDB |
|----------|--------|--------|
| ROLLUP | ✅ | ✅ |
| CUBE | ❌ | ✅ |
| GROUPING SETS | ❌ | ✅ |
| GROUPING() | ❌ | ✅ |
| OLAP-focused | ❌ | ✅ |
| Setup friction | Medium | Zero |

---

# 1️⃣ Create Table

```sql
CREATE TABLE sales (
    product VARCHAR,
    quarter VARCHAR,
    region  VARCHAR,
    sales   INTEGER
);
```

---

# 2️⃣ Insert Data

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

```sql
OLAP_basics (main) % duckdb
DuckDB v1.4.4 (Andium) 6ddac802ff
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
D CREATE TABLE sales (
      product VARCHAR,
      quarter VARCHAR,
      region  VARCHAR,
      sales   INTEGER
  );
D desc sales;
┌─────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│ column_name │ column_type │  null   │   key   │ default │  extra  │
│   varchar   │   varchar   │ varchar │ varchar │ varchar │ varchar │
├─────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ product     │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ quarter     │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ region      │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ sales       │ INTEGER     │ YES     │ NULL    │ NULL    │ NULL    │
└─────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘
```

View Data:

```sql
D select * from sales;
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

# 3️⃣ Basic GROUP BY

```sql
SELECT product, 
       SUM(sales) AS total_sales
FROM sales
GROUP BY product
ORDER BY product;

D SELECT product,
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

# 4️⃣ ROLLUP in DuckDB

```sql
SELECT product, quarter, 
       SUM(sales) AS total_sales
FROM sales
GROUP BY ROLLUP(product, quarter)
ORDER BY product, quarter;

D SELECT product, quarter,
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

ROLLUP produces:

- (product, quarter)
- (product subtotal)
- (grand total)

Hierarchical aggregation (left → right).

---

# 5️⃣ CUBE in DuckDB

```sql
SELECT product, quarter, region,
       SUM(sales) AS total_sales
FROM sales
GROUP BY CUBE(product, quarter, region)
ORDER BY product, quarter, region;
```

CUBE generates ALL combinations:

For 3 columns → 2³ = 8 grouping levels:

- (product, quarter, region)
- (product, quarter)
- (product, region)
- (quarter, region)
- (product)
- (quarter)
- (region)
- (grand total)


```sql
SELECT product, quarter, region,
       SUM(sales) AS total_sales
FROM sales
GROUP BY CUBE(product, quarter, region)
ORDER BY product, quarter, region;

D .mod box
D SELECT product, quarter, region,
         SUM(sales) AS total_sales
  FROM sales
  GROUP BY CUBE(product, quarter, region)
  ORDER BY product, quarter, region;
┌─────────┬─────────┬─────────┬─────────────┐
│ product │ quarter │ region  │ total_sales │
├─────────┼─────────┼─────────┼─────────────┤
│ A       │ Q1      │ America │ 20          │
│ A       │ Q1      │ Europe  │ 10          │
│ A       │ Q1      │ NULL    │ 30          │
│ A       │ Q2      │ America │ 50          │
│ A       │ Q2      │ Europe  │ 20          │
│ A       │ Q2      │ NULL    │ 70          │
│ A       │ Q3      │ America │ 20          │
│ A       │ Q3      │ NULL    │ 20          │
│ A       │ Q4      │ America │ 30          │
│ A       │ Q4      │ Europe  │ 10          │
│ A       │ Q4      │ NULL    │ 40          │
│ A       │ NULL    │ America │ 120         │
│ A       │ NULL    │ Europe  │ 40          │
│ A       │ NULL    │ NULL    │ 160         │
│ B       │ Q1      │ America │ 60          │
│ B       │ Q1      │ Europe  │ 40          │
│ B       │ Q1      │ NULL    │ 100         │
│ B       │ Q2      │ America │ 10          │
│ B       │ Q2      │ Europe  │ 20          │
│ B       │ Q2      │ NULL    │ 30          │
│ B       │ Q3      │ America │ 20          │
│ B       │ Q3      │ NULL    │ 20          │
│ B       │ Q4      │ America │ 40          │
│ B       │ Q4      │ Europe  │ 10          │
│ B       │ Q4      │ NULL    │ 50          │
│ B       │ NULL    │ America │ 130         │
│ B       │ NULL    │ Europe  │ 70          │
│ B       │ NULL    │ NULL    │ 200         │
│ C       │ Q1      │ America │ 60          │
│ C       │ Q1      │ Europe  │ 50          │
│ C       │ Q1      │ NULL    │ 110         │
│ C       │ Q2      │ America │ 45          │
│ C       │ Q2      │ Europe  │ 35          │
│ C       │ Q2      │ NULL    │ 80          │
│ C       │ NULL    │ America │ 105         │
│ C       │ NULL    │ Europe  │ 85          │
│ C       │ NULL    │ NULL    │ 190         │
│ NULL    │ Q1      │ America │ 140         │
│ NULL    │ Q1      │ Europe  │ 100         │
│ NULL    │ Q1      │ NULL    │ 240         │
│ NULL    │ Q2      │ America │ 105         │
│ NULL    │ Q2      │ Europe  │ 75          │
│ NULL    │ Q2      │ NULL    │ 180         │
│ NULL    │ Q3      │ America │ 40          │
│ NULL    │ Q3      │ NULL    │ 40          │
│ NULL    │ Q4      │ America │ 70          │
│ NULL    │ Q4      │ Europe  │ 20          │
│ NULL    │ Q4      │ NULL    │ 90          │
│ NULL    │ NULL    │ America │ 355         │
│ NULL    │ NULL    │ Europe  │ 195         │
│ NULL    │ NULL    │ NULL    │ 550         │
└─────────┴─────────┴─────────┴─────────────┘
```

---

# 6️⃣ Using GROUPING()

```sql
SELECT product,
       quarter,
       region,
       SUM(sales) AS total_sales,
       GROUPING(product) AS g_product,
       GROUPING(quarter) AS g_quarter,
       GROUPING(region)  AS g_region
FROM sales
GROUP BY CUBE(product, quarter, region)
ORDER BY product, quarter, region;
```

GROUPING(column):

- 0 → Column is present
- 1 → Column was aggregated (NULL introduced)

Very important for identifying subtotal rows.

```sql
SELECT product,
       quarter,
       region,
       SUM(sales) AS total_sales,
       GROUPING(product) AS g_product,
       GROUPING(quarter) AS g_quarter,
       GROUPING(region)  AS g_region
FROM sales
GROUP BY CUBE(product, quarter, region)
ORDER BY product, quarter, region;

┌─────────┬─────────┬─────────┬─────────────┬───────────┬───────────┬──────────┐
│ product │ quarter │ region  │ total_sales │ g_product │ g_quarter │ g_region │
├─────────┼─────────┼─────────┼─────────────┼───────────┼───────────┼──────────┤
│ A       │ Q1      │ America │ 20          │ 0         │ 0         │ 0        │
│ A       │ Q1      │ Europe  │ 10          │ 0         │ 0         │ 0        │
│ A       │ Q1      │ NULL    │ 30          │ 0         │ 0         │ 1        │
│ A       │ Q2      │ America │ 50          │ 0         │ 0         │ 0        │
│ A       │ Q2      │ Europe  │ 20          │ 0         │ 0         │ 0        │
│ A       │ Q2      │ NULL    │ 70          │ 0         │ 0         │ 1        │
│ A       │ Q3      │ America │ 20          │ 0         │ 0         │ 0        │
│ A       │ Q3      │ NULL    │ 20          │ 0         │ 0         │ 1        │
│ A       │ Q4      │ America │ 30          │ 0         │ 0         │ 0        │
│ A       │ Q4      │ Europe  │ 10          │ 0         │ 0         │ 0        │
│ A       │ Q4      │ NULL    │ 40          │ 0         │ 0         │ 1        │
│ A       │ NULL    │ America │ 120         │ 0         │ 1         │ 0        │
│ A       │ NULL    │ Europe  │ 40          │ 0         │ 1         │ 0        │
│ A       │ NULL    │ NULL    │ 160         │ 0         │ 1         │ 1        │
│ B       │ Q1      │ America │ 60          │ 0         │ 0         │ 0        │
│ B       │ Q1      │ Europe  │ 40          │ 0         │ 0         │ 0        │
│ B       │ Q1      │ NULL    │ 100         │ 0         │ 0         │ 1        │
│ B       │ Q2      │ America │ 10          │ 0         │ 0         │ 0        │
│ B       │ Q2      │ Europe  │ 20          │ 0         │ 0         │ 0        │
│ B       │ Q2      │ NULL    │ 30          │ 0         │ 0         │ 1        │
│ B       │ Q3      │ America │ 20          │ 0         │ 0         │ 0        │
│ B       │ Q3      │ NULL    │ 20          │ 0         │ 0         │ 1        │
│ B       │ Q4      │ America │ 40          │ 0         │ 0         │ 0        │
│ B       │ Q4      │ Europe  │ 10          │ 0         │ 0         │ 0        │
│ B       │ Q4      │ NULL    │ 50          │ 0         │ 0         │ 1        │
│ B       │ NULL    │ America │ 130         │ 0         │ 1         │ 0        │
│ B       │ NULL    │ Europe  │ 70          │ 0         │ 1         │ 0        │
│ B       │ NULL    │ NULL    │ 200         │ 0         │ 1         │ 1        │
│ C       │ Q1      │ America │ 60          │ 0         │ 0         │ 0        │
│ C       │ Q1      │ Europe  │ 50          │ 0         │ 0         │ 0        │
│ C       │ Q1      │ NULL    │ 110         │ 0         │ 0         │ 1        │
│ C       │ Q2      │ America │ 45          │ 0         │ 0         │ 0        │
│ C       │ Q2      │ Europe  │ 35          │ 0         │ 0         │ 0        │
│ C       │ Q2      │ NULL    │ 80          │ 0         │ 0         │ 1        │
│ C       │ NULL    │ America │ 105         │ 0         │ 1         │ 0        │
│ C       │ NULL    │ Europe  │ 85          │ 0         │ 1         │ 0        │
│ C       │ NULL    │ NULL    │ 190         │ 0         │ 1         │ 1        │
│ NULL    │ Q1      │ America │ 140         │ 1         │ 0         │ 0        │
│ NULL    │ Q1      │ Europe  │ 100         │ 1         │ 0         │ 0        │
│ NULL    │ Q1      │ NULL    │ 240         │ 1         │ 0         │ 1        │
│ NULL    │ Q2      │ America │ 105         │ 1         │ 0         │ 0        │
│ NULL    │ Q2      │ Europe  │ 75          │ 1         │ 0         │ 0        │
│ NULL    │ Q2      │ NULL    │ 180         │ 1         │ 0         │ 1        │
│ NULL    │ Q3      │ America │ 40          │ 1         │ 0         │ 0        │
│ NULL    │ Q3      │ NULL    │ 40          │ 1         │ 0         │ 1        │
│ NULL    │ Q4      │ America │ 70          │ 1         │ 0         │ 0        │
│ NULL    │ Q4      │ Europe  │ 20          │ 1         │ 0         │ 0        │
│ NULL    │ Q4      │ NULL    │ 90          │ 1         │ 0         │ 1        │
│ NULL    │ NULL    │ America │ 355         │ 1         │ 1         │ 0        │
│ NULL    │ NULL    │ Europe  │ 195         │ 1         │ 1         │ 0        │
│ NULL    │ NULL    │ NULL    │ 550         │ 1         │ 1         │ 1        │
└─────────┴─────────┴─────────┴─────────────┴───────────┴───────────┴──────────┘
```


---

# 7️⃣ GROUPING SETS

Explicitly define aggregation combinations:

```sql
SELECT product, quarter, region,
       SUM(sales) AS total_sales
FROM sales
GROUP BY GROUPING SETS (
    (product, quarter, region),
    (product, quarter),
    (product, region),
    (quarter, region),
    (product),
    (quarter),
    (region),
    ()
);
```

GROUPING SETS = Controlled CUBE.

```sql
SELECT product, quarter, region,
       SUM(sales) AS total_sales
FROM sales
GROUP BY GROUPING SETS (
    (product, quarter, region),
    (product, quarter),
    (product, region),
    (quarter, region),
    (product),
    (quarter),
    (region),
    ()
);

┌─────────┬─────────┬─────────┬─────────────┐
│ product │ quarter │ region  │ total_sales │
├─────────┼─────────┼─────────┼─────────────┤
│ B       │ Q2      │ America │ 10          │
│ B       │ Q4      │ America │ 40          │
│ C       │ Q1      │ America │ 60          │
│ A       │ Q2      │ NULL    │ 70          │
│ A       │ Q4      │ NULL    │ 40          │
│ NULL    │ Q2      │ America │ 105         │
│ B       │ Q4      │ Europe  │ 10          │
│ C       │ Q1      │ Europe  │ 50          │
│ B       │ Q3      │ NULL    │ 20          │
│ C       │ NULL    │ America │ 105         │
│ NULL    │ Q2      │ NULL    │ 180         │
│ NULL    │ Q4      │ NULL    │ 90          │
│ B       │ NULL    │ Europe  │ 70          │
│ NULL    │ Q1      │ NULL    │ 240         │
│ A       │ Q3      │ America │ 20          │
│ A       │ Q1      │ Europe  │ 10          │
│ NULL    │ Q1      │ America │ 140         │
│ NULL    │ NULL    │ America │ 355         │
│ B       │ Q1      │ NULL    │ 100         │
│ NULL    │ Q1      │ Europe  │ 100         │
│ C       │ NULL    │ NULL    │ 190         │
│ NULL    │ Q3      │ NULL    │ 40          │
│ NULL    │ NULL    │ Europe  │ 195         │
│ A       │ NULL    │ Europe  │ 40          │
│ NULL    │ Q3      │ America │ 40          │
│ A       │ Q4      │ Europe  │ 10          │
│ B       │ NULL    │ NULL    │ 200         │
│ A       │ Q1      │ America │ 20          │
│ A       │ Q3      │ NULL    │ 20          │
│ C       │ Q1      │ NULL    │ 110         │
│ B       │ NULL    │ America │ 130         │
│ A       │ Q4      │ America │ 30          │
│ A       │ Q2      │ America │ 50          │
│ B       │ Q1      │ America │ 60          │
│ B       │ Q3      │ America │ 20          │
│ C       │ Q2      │ Europe  │ 35          │
│ B       │ Q2      │ Europe  │ 20          │
│ A       │ Q1      │ NULL    │ 30          │
│ C       │ NULL    │ Europe  │ 85          │
│ NULL    │ Q4      │ Europe  │ 20          │
│ A       │ Q2      │ Europe  │ 20          │
│ B       │ Q1      │ Europe  │ 40          │
│ C       │ Q2      │ America │ 45          │
│ NULL    │ Q4      │ America │ 70          │
│ NULL    │ NULL    │ NULL    │ 550         │
│ C       │ Q2      │ NULL    │ 80          │
│ NULL    │ Q2      │ Europe  │ 75          │
│ A       │ NULL    │ America │ 120         │
│ A       │ NULL    │ NULL    │ 160         │
│ B       │ Q2      │ NULL    │ 30          │
│ B       │ Q4      │ NULL    │ 50          │
└─────────┴─────────┴─────────┴─────────────┘
```


---

# Teaching Strategy

Recommended lecture flow:

1. Start with GROUP BY
2. Introduce ROLLUP (hierarchical)
3. Show limitations of ROLLUP
4. Introduce CUBE
5. Explain 2ⁿ explosion
6. Introduce GROUPING()
7. Introduce GROUPING SETS
8. Compare with MySQL limitations

---

# Key Insight

ROLLUP = Hierarchical subtotaling  
CUBE = Full multidimensional subtotaling  

DuckDB fully supports modern OLAP SQL.  
MySQL supports ROLLUP but not CUBE.

---

# ✅ End of DuckDB CUBE Tutorial
