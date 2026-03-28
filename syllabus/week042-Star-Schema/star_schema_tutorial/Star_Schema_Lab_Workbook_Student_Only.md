
# 📘 Student Lab Workbook — Star Schema (Student Version)

⚠️ This version contains **NO solutions**.  
You are expected to design, write, and validate all SQL yourself.

---

# Lab Environment Setup

You will use:

- MySQL 8+
- Two databases:
  - `oltp_demo`
  - `dw_demo`

Provided files (from instructor):

```
01_oltp_100k_data_generator_mysql.sql
02_dw_star_schema_mysql.sql
03_etl_oltp_to_dw_mysql.sql
04_olap_queries_star_schema.sql
```
---

# Lab 1 — Generate OLTP Dataset (100K Orders)

## Objectives
1. Create the `oltp_demo` database.
2. Run the data generator SQL script.
3. Verify row counts for:
   - customers
   - products
   - stores
   - orders
   - order_items

## Deliverable
Provide SQL queries and screenshots of row counts.

---

# Lab 2 — Dimensional Modeling Design

## Objectives
1. Define the **grain** of your fact table.
2. Identify:
   - Fact table name
   - Measures
   - Dimension tables
3. Decide which dimensions are:
   - Type 1
   - Type 2 (SCD2)

## Questions
- Why must grain be defined first?
- What problems occur if grain changes later?

## Deliverable
Submit a 1–2 page design document explaining your model.

---

# Lab 3 — Create the Star Schema (DW)

## Objectives
1. Create `dw_demo` database.
2. Create dimension tables.
3. Create fact table.
4. Add appropriate indexes.

## Deliverable
Submit your full DDL script.

---

# Lab 4 — ETL: Load Dimensions and Facts

## Objectives
1. Populate `dim_date`.
2. Populate product and store dimensions.
3. Implement initial load for customer dimension.
4. Load `fact_sales` using surrogate key lookups.

## Validation
- Row counts in fact table.
- No NULL foreign keys.

## Deliverable
Submit your ETL SQL and validation queries.

---

# Lab 5 — OLAP Query Practice

Write SQL queries for:

1) Revenue by year  
2) Revenue by month (last 12 months)  
3) Top 10 products by revenue  
4) Revenue by region  
5) Customer lifetime value (Top 20)  
6) Average order value  
7) Basket size distribution  
8) Category mix by month  
9) Repeat customers (>= 2 orders)  
10) Daily revenue (last 30 days)  

## Deliverable
Submit SQL scripts and results.

---

# Lab 6 — Slowly Changing Dimension (Type 2)

## Scenario
A customer changes country.

## Objectives
1. Update OLTP customer record.
2. Expire existing DW dimension row.
3. Insert new current row.
4. Validate two versions exist for that customer.

## Bonus Challenge
Modify your fact-to-dimension join so that facts map to the correct historical customer version using date ranges.

## Deliverable
Submit SQL scripts and validation queries.

---

# Grading Rubric

| Component | Weight |
|-----------|--------|
| OLTP Setup | 10% |
| Dimensional Design | 20% |
| DW Schema | 20% |
| ETL Implementation | 20% |
| OLAP Queries | 20% |
| SCD2 Implementation | 10% |

---

# Expected Learning Outcomes

By completing this lab, you should be able to:

- Design a proper star schema
- Define grain correctly
- Implement ETL from OLTP to DW
- Write OLAP queries
- Implement SCD Type 2
- Validate dimensional integrity

---

End of Student Workbook
