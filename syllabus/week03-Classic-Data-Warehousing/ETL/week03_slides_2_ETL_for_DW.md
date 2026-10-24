
# ETL for Data Warehousing


---

## Slide 1 — What is ETL?

**ETL (Extract, Transform, Load)** is the backbone of data warehousing.

```text
Source Systems → ETL → Data Warehouse → Analytics / BI
```

![](./images/etl_01.png)

![](./images/etl_02.jpg)

![](./images/etl_03.png)
---

## Slide 2 — Why ETL is Critical

Operational systems (OLTP):

- Optimized for transactions
- Normalized
- Write-heavy

Data warehouses (OLAP):
- Optimized for analytics
- Denormalized
- Read-heavy

---

## Slide 3 — ETL vs ELT

| ETL | ELT |
|---|---|
| Transform before load | Load raw data first |
| Traditional DW | Cloud DW |
| Controlled schema | Flexible schema |

![](./images/ETL_vs_ELT.png)
---

## Slide 4 — Extract Phase

Sources:

- Databases
- Files (CSV, JSON)
- APIs

Key concerns:

- Incremental extraction
- Source system impact

---

## Slide 5 — Python: Extract Example

```python
import pandas as pd

customers = pd.read_csv("customers.csv")
orders = pd.read_csv("orders.csv")
```

---

## Slide 6 — Transform Phase

Transformations:

- Cleansing
- Filtering
- Aggregations
- Business rules

---

## Slide 7 — Python: Transform Example

```python
orders = orders[orders["amount"] > 0]
orders["tax"] = orders["amount"] * 0.07
```

---

## Slide 8 — Dimensions

Dimensions provide context:

- Customer
- Date
- Product

Low cardinality, descriptive attributes.

---

## Slide 9 — Python: Date Dimension

```python
orders["order_date"] = pd.to_datetime(orders["order_date"])

dates = orders["order_date"].drop_duplicates().to_frame()
dates["year"] = dates["order_date"].dt.year
dates["month"] = dates["order_date"].dt.month
dates["date_id"] = dates["order_date"].dt.strftime("%Y%m%d").astype(int)
```

---

## Slide 10 — Fact Tables

Facts store measurable events:

- Sales
- Transactions

Contain foreign keys + measures.

---

## Slide 11 — Python: Fact Example

```python
fact_orders = orders.merge(
    dates[["date_id", "order_date"]],
    on="order_date"
)
```

---

## Slide 12 — Load Phase

Load into:

- MySQL
- Postgres
- Snowflake
- BigQuery

Bulk loading preferred.

---

## Slide 13 — Python: Load Example

```python
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://user:pwd@localhost/dw")

fact_orders.to_sql("fact_orders", engine, if_exists="append", index=False)
```

---

## Slide 14 — Incremental ETL

Avoid full reloads:
```sql
WHERE updated_at > last_run
```

---

## Slide 15 — Data Quality Checks

- Null checks
- Range checks
- Referential integrity

---

## Slide 16 — Error Handling

- Logging
- Retry logic
- Dead-letter records

---

## Slide 17 — Performance

- Batch processing
- Partitioning
- Parallelism

---

## Slide 18 — ETL Tools

| Type | Examples |
|---|---|
| Open-source | Airflow, Spark |
| Commercial | Informatica |
| Cloud | Glue |

---

## Slide 19 — Modern ETL Architecture

```text
Sources → Data Lake → ELT → Cloud DW → BI
```

---

## Slide 20 — Summary

✔ ETL enables analytics  
✔ Python is flexible  
✔ Dimensions + facts power OLAP  
✔ Data quality matters  

---

## End
