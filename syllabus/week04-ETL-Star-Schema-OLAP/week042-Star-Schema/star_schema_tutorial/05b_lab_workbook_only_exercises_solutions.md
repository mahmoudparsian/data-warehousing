# Student Lab Workbook — Star Schema (OLTP → ETL → OLAP)

This workbook includes **exercises + solutions**.

## Files
- 01_oltp_100k_data_generator_mysql.sql
- 02_dw_star_schema_mysql.sql
- 03_etl_oltp_to_dw_mysql.sql
- 04_olap_queries_star_schema.sql

---

# Lab 1 — OLTP Data Generation (100K orders)

## Exercise
Run the generator script and confirm counts.

## Solution
```sql
USE oltp_demo;
SELECT 'customers', COUNT(*) FROM customers
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'stores', COUNT(*) FROM stores
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'order_items', COUNT(*) FROM order_items;
```

---

# Lab 2 — Design (Grain + Facts + Dimensions)

## Exercise
Define the grain of your fact table and list dimensions/measures.

## Solution (Example)
- Grain: 1 row per order_item
- Dimensions: date, customer, product, store
- Measures: quantity, unit_price, sales_amount

---

# Lab 3 — Create DW Schema

## Exercise
Create `dw_demo` and run the DW schema script.

## Solution
```sql
USE dw_demo;
SHOW TABLES;
```

---

# Lab 4 — Run ETL

## Exercise
Load dimensions then facts.

## Solution
Run: `03_etl_oltp_to_dw_mysql.sql`

---

# Lab 5 — OLAP Queries

## Exercise
Write 10 OLAP queries (revenue by year, top products, AOV, etc.)

## Solution
Run: `04_olap_queries_star_schema.sql`

---

# Lab 6 — SCD Type 2 Simulation

## Exercise
Simulate a customer country change and keep history in dim_customer.

## Solution (Pattern)
```sql
-- expire current row
UPDATE dim_customer
SET expiry_date = CURDATE() - INTERVAL 1 DAY,
    is_current = FALSE
WHERE customer_id = 101 AND is_current = TRUE;

-- insert new version
INSERT INTO dim_customer (customer_id, first_name, last_name, email, country, effective_date, expiry_date, is_current)
SELECT customer_id, first_name, last_name, email, country, CURDATE(), '9999-12-31', TRUE
FROM oltp_demo.customers
WHERE customer_id = 101;
```

---

## Bonus: Historically correct joins
Join facts to customers using date ranges:
- fact_date BETWEEN effective_date AND expiry_date
