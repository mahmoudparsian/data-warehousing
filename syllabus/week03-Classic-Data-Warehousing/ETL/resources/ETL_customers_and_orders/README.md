# Star Schema ETL (Customers + Orders)

	This package contains two realistic-ish datasets 
	plus a Python ETL that builds a simple star schema.

## Files

### Input datasets
- `customers.csv` (5,000 rows)
- `orders.csv` (30,000 rows)

### ETL outputs
- `dim_customers.csv`
- `dim_dates.csv`  (derived from `orders.order_date`)
- `fact_orders.csv` (orders fact table + computed `tax`)

### SQL
- `schema.sql` (MySQL 8+ DDL for the star schema)
- `olap_queries.md`  (10 OLAP queries)
- `olap_queries.sql` (10 OLAP queries)

## Run the ETL

```bash
python3 etl_build_star_schema.py --customers customers.csv --orders orders.csv --outdir out
```

Outputs land in `out/`.

## Notes
- `date_id` uses the `YYYYMMDD` integer format (e.g., 20240517).
- `tax` is computed as **7%** of `order_amount`, rounded to cents.
