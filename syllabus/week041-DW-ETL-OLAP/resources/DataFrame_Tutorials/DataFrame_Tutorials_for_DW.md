# Pandas DataFrame Tutorial for ETL in Data Warehousing

	1. A DataFrame in Python's Pandas Library

	2. When using Python as an ETL programming, 
	   a DataFrame in Python's Pandas Library 
	   is the key ingrediant for the ETL process.
	
	3. A Pandas DataFrame is a two-dimensional, 
	   size-mutable, and potentially heterogeneous 
	   tabular data structure with labeled axes 
	   (rows and columns).
	
	
![](./pandas_dataframe_example.png)



## 0. This tutorial

This tutorial explains how **Pandas DataFrames** 
are used to implement **ETL pipelines** for 
**data warehousing**, with realistic examples 
and best practices.

---

## 1. Role of Pandas in ETL

Pandas is commonly used for:

- Prototyping ETL logic
- Batch ETL pipelines
- Small–medium data volumes
- Pre-processing before Spark / DW load

```text
Source Data → Pandas ETL → Data Warehouse
```

---

## 2. Typical ETL Workflow in Pandas

1. **Extract** data from files or databases  
2. **Transform** data (clean, join, enrich)  
3. **Load** data into a data warehouse  

---

## 3. Setup

```python
import pandas as pd
import numpy as np
```

---

## 4. Extract Phase

### 4.1 Read CSV Files

```python
customers = pd.read_csv("customers.csv")
orders = pd.read_csv("orders.csv")
```

```python
customers.head()
orders.head()
```

---

### 4.2 Read from Database (Optional)

```python
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://user:password@localhost/source_db")
df = pd.read_sql("SELECT * FROM orders", engine)
```

---

## 5. Transform Phase – Data Cleaning

### 5.1 Handle Missing Values

```python
orders.isnull().sum()
```

```python
orders = orders.dropna(subset=["order_amount"])
```

---

### 5.2 Filter Invalid Records

```python
orders = orders[orders["order_amount"] > 0]
```

---

## 6. Transform Phase – Enrichment

### 6.1 Add Derived Columns

```python
orders["tax"] = orders["order_amount"] * 0.07
orders["tax"] = orders["tax"].round(2)
```

---

### 6.2 Convert Data Types

```python
orders["order_date"] = pd.to_datetime(orders["order_date"])
```

---

## 7. Dimension Tables

### 7.1 Customer Dimension

```python
dim_customers = customers[[
    "customer_id",
    "country",
    "age",
    "gender",
    "signup_year"
]]
```

---

### 7.2 Date Dimension

```python
dim_dates = orders[["order_date"]].drop_duplicates()

dim_dates["date_id"] = dim_dates["order_date"].dt.strftime("%Y%m%d").astype(int)
dim_dates["year"] = dim_dates["order_date"].dt.year
dim_dates["month"] = dim_dates["order_date"].dt.month
dim_dates["day"] = dim_dates["order_date"].dt.day
dim_dates["quarter"] = dim_dates["order_date"].dt.quarter
```

---

## 8. Fact Table Construction

```python
fact_orders = orders.merge(
    dim_dates,
    on="order_date",
    how="left"
)

fact_orders = fact_orders[[
    "order_id",
    "customer_id",
    "date_id",
    "order_amount",
    "tax"
]]
```

---

## 9. Aggregations for OLAP

### Revenue by Country

```python
orders.merge(customers, on="customer_id") \
      .groupby("country")["order_amount"] \
      .sum()
```

---

## 10. Incremental ETL Pattern

```python
last_run = "2024-01-01"

new_orders = orders[orders["order_date"] > last_run]
```

---

## 11. Data Quality Checks

```python
assert fact_orders["customer_id"].isnull().sum() == 0
assert (fact_orders["order_amount"] > 0).all()
```

---

## 12. Load Phase

### 12.1 Load to CSV (Staging)

```python
fact_orders.to_csv("fact_orders.csv", index=False)
dim_customers.to_csv("dim_customers.csv", index=False)
dim_dates.to_csv("dim_dates.csv", index=False)
```

---

### 12.2 Load to MySQL

```python
engine = create_engine("mysql+pymysql://user:password@localhost/dw")

fact_orders.to_sql(
    "fact_orders",
    engine,
    if_exists="append",
    index=False
)
```

---

## 13. Performance Considerations

- Avoid row-by-row loops
- Use vectorized operations
- Chunk large files

```python
pd.read_csv("large.csv", chunksize=100_000)
```

---

## 14. Pandas vs Spark

| Pandas | Spark |
|------|------|
| Single-node | Distributed |
| Easy to use | Scales big |
| Prototyping | Production-scale |

---

## 15. Best Practices

✔ Keep raw data immutable  
✔ Separate extract / transform / load  
✔ Log ETL runs  
✔ Validate data before loading  

---

## 16. Summary

- Pandas is ideal for **ETL prototyping**
- Supports full DW workflows
- Integrates well with SQL databases
- Forms the foundation for Spark-based ETL

---

## 17. References and Tutorials

#### 1. [Python pandas Tutorial: The Ultimate Guide for Beginners]()

#### 2. [Pandas Tutorial: DataFrames in Python](https://www.datacamp.com/tutorial/pandas-tutorial-dataframe-python)

#### 3. [Pandas DataFrames: from w3schools](https://www.w3schools.com/python/pandas/pandas_dataframes.asp)

#### 4. [The pandas DataFrame](https://realpython.com/pandas-dataframe/)

#### 5. [Pandas Getting started tutorials](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html)

#### 6. [Python Pandas - DataFrame](https://www.tutorialspoint.com/python_pandas/python_pandas_dataframe.htm)


