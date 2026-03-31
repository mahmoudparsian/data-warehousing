
---
marp: true

paginate: true

theme: default

title: DuckDB Tutorial — Reading CSV & Creating Tables
style: |
  section { font-size: 26px; }
  h1 { color: #0b5394; }
  code { background: #f6f8fa; }
---

# 🦆 DuckDB Tutorial

## Reading CSV Files & Creating Tables

Audience: Business / Data Analytics Students

---

# 🎯 Learning Objectives

• Read CSV files directly  
• Create tables from CSV  
• Handle messy data  
• Perform SQL analytics  

---

# 📂 General Pattern — Reading CSV

```sql
SELECT *
FROM 'file.csv';
```

---

# 📌 Using read_csv_auto

```sql
SELECT *
FROM read_csv_auto('file.csv');
```

---

# 📥 Example — Simple Read

```sql
SELECT *
FROM 'customers.csv'
LIMIT 5;
```

---

# 📊 Aggregation Example

```sql
SELECT
    country,
    COUNT(*) AS total_customers
FROM 'customers.csv'
GROUP BY country;
```

---

# 🔗 Join Example

```sql
SELECT
    o.order_id,
    c.customer_name
FROM 'orders.csv' o
JOIN 'customers.csv' c
ON o.customer_id = c.customer_id;
```

---

# 🧱 Create Table

```sql
CREATE TABLE customers AS
SELECT *
FROM 'customers.csv';
```

---

# 🆚 View vs Table

View:
```sql
CREATE VIEW v_customers AS
SELECT * FROM 'customers.csv';
```

Table:
```sql
CREATE TABLE customers AS
SELECT * FROM 'customers.csv';
```

---

# ⚠️ Handling Messy CSV

```sql
SELECT *
FROM read_csv_auto(
    'retail_data.csv',
    encoding='latin1',
    ignore_errors=true
);
```

---

# 🔄 Transform While Loading

```sql
CREATE TABLE sales AS
SELECT
    order_id,
    quantity,
    quantity * price AS revenue
FROM 'order_items.csv';
```

---

# 📤 Export

```sql
COPY customers TO 'customers_export.csv' (HEADER);
```

---

# 🧑‍💻 Python Example

```python
import duckdb
con = duckdb.connect()

df = con.execute("""
SELECT *
FROM 'customers.csv'
LIMIT 10
""").df()

df.head()
```

---
# Example: read a CSV file and Create a Table

* inspect CSV file

```
% ls -l insurance.csv

-rw-r--r--@ 1 max  staff  55631 Mar 20 19:53 insurance.csv

% wc -l insurance.csv
    1339 insurance.csv
    
% head -5 insurance.csv
age,gender,bmi,children,smoker,region,charges
19,female,27.9,0,yes,southwest,16884.924
18,male,33.77,1,no,southeast,1725.5523
28,male,33,3,no,southeast,4449.462
33,male,22.705,0,no,northwest,21984.47061
```

* Create a Table from CSV file

```
% duckdb
DuckDB v1.5.1 (Variegata)

memory D CREATE TABLE insurance AS SELECT * FROM 'insurance.csv';

memory D desc insurance;
┌──────────────────┐
│    insurance     │
│                  │
│ age      bigint  │
│ gender   varchar │
│ bmi      double  │
│ children bigint  │
│ smoker   boolean │
│ region   varchar │
│ charges  double  │
└──────────────────┘

memory D select count(*) from insurance;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│         1338 │
└──────────────┘

memory D select * from insurance limit 5;
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int64 │ varchar │ double │  int64   │ boolean │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    19 │ female  │   27.9 │        0 │ true    │ southwest │   16884.924 │
│    18 │ male    │  33.77 │        1 │ false   │ southeast │   1725.5523 │
│    28 │ male    │   33.0 │        3 │ false   │ southeast │    4449.462 │
│    33 │ male    │ 22.705 │        0 │ false   │ northwest │ 21984.47061 │
│    32 │ male    │  28.88 │        0 │ false   │ northwest │   3866.8552 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘
```

---

# 🎓 Summary

DuckDB = SQL directly on files

---

# 🧪 Exercises

1. Count customers per country  
2. Join orders and customers  
3. Create revenue table  
