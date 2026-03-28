# Incremental ETL Guide
## Loading New OLTP Records into an Existing Star Schema (MySQL)

This document explains how to:

1. Insert NEW OLTP records (realistic examples)
2. Incrementally update dimension tables
3. Incrementally load fact table (execution-level grain)
4. Maintain referential integrity
5. Validate the load

Assumption:
- OLTP database: stock_oltp
- DW database: stock_dw
- Fact grain: 1 row per execution
- SCD Type 1 strategy (overwrite changes)

---

# STEP 1 — Insert New OLTP Records (Example)

Switch to OLTP:

```sql
USE stock_oltp;
```

## 1.1 New User

```sql
INSERT INTO users VALUES
(9999, 'MALE', 'John', 'Investor', 'john.investor@email.com',
 'USA', 'Chicago', '2024-11-01');
```

## 1.2 New Account

```sql
INSERT INTO accounts VALUES
(8888, 9999, 'Individual', 'Active', 150000.00, '2024-11-02');
```

## 1.3 New Order

```sql
INSERT INTO orders VALUES
(777777, 8888, 10, 'Market', 250.00, 100,
 '2024-11-15', 'buy', 'executed');
```

## 1.4 New Execution (partial fill)

```sql
INSERT INTO executions VALUES
(5555555, 777777, 249.75, 100,
 '2024-11-15 10:15:00', 4.95);
```

---

# STEP 2 — Incremental Dimension Updates

Switch to DW:

```sql
USE stock_dw;
```

## 2.1 Update dim_account (SCD Type 1)

```sql
INSERT INTO dim_account (
  account_id, user_id, account_type, account_status,
  user_gender, user_first_name, user_last_name, user_email,
  user_country, user_city, user_date_joined, account_created_at
)
SELECT
  a.account_id,
  a.user_id,
  a.account_type,
  a.account_status,
  u.gender,
  u.first_name,
  u.last_name,
  u.email,
  u.country,
  u.city,
  u.date_joined,
  a.created_at
FROM stock_oltp.accounts a
JOIN stock_oltp.users u
  ON a.user_id = u.user_id
WHERE a.account_id = 8888
ON DUPLICATE KEY UPDATE
  account_status = VALUES(account_status),
  user_city = VALUES(user_city);
```

---

## 2.2 Update dim_symbol (if new symbol was inserted)

```sql
INSERT INTO dim_symbol (
  symbol_id, symbol, company_name, sector, industry,
  exchange_name, exchange_country, exchange_timezone, date_added
)
SELECT
  s.symbol_id,
  s.symbol,
  s.company_name,
  s.sector,
  s.industry,
  e.exchange_name,
  e.country,
  e.timezone,
  s.date_added
FROM stock_oltp.symbols s
JOIN stock_oltp.exchanges e
  ON s.exchange_id = e.exchange_id
WHERE s.symbol_id = 10
ON DUPLICATE KEY UPDATE
  company_name = VALUES(company_name);
```

---

# STEP 3 — Incremental Fact Load

Only load NEW executions not already in fact table.

```sql
INSERT INTO fact_trades (
  date_id, symbol_key, account_key, side_key, order_type_key, order_status_key,
  order_id, execution_id,
  execution_price, execution_quantity, execution_fee, trade_value,
  execution_time
)
SELECT
  dd.date_id,
  ds.symbol_key,
  da.account_key,
  dside.side_key,
  dot.order_type_key,
  dos.order_status_key,

  o.order_id,
  ex.execution_id,

  ex.execution_price,
  ex.execution_quantity,
  ex.execution_fee,
  (ex.execution_price * ex.execution_quantity) AS trade_value,

  ex.execution_time
FROM stock_oltp.executions ex
JOIN stock_oltp.orders o
  ON ex.order_id = o.order_id

JOIN dim_date dd
  ON dd.full_date = DATE(ex.execution_time)

JOIN dim_symbol ds
  ON ds.symbol_id = o.symbol_id

JOIN dim_account da
  ON da.account_id = o.account_id

JOIN dim_side dside
  ON dside.side_code = o.buy_or_sell

JOIN dim_order_type dot
  ON dot.order_type = o.order_type

JOIN dim_order_status dos
  ON dos.order_status = o.order_status

LEFT JOIN fact_trades f
  ON f.execution_id = ex.execution_id

WHERE f.execution_id IS NULL;
```

This ensures:
- No duplicate execution loads
- Idempotent ETL runs

---

# STEP 4 — Validation Queries

## Validate new execution loaded

```sql
SELECT *
FROM fact_trades
WHERE execution_id = 5555555;
```

## Validate total row counts

```sql
SELECT COUNT(*) FROM stock_oltp.executions;
SELECT COUNT(*) FROM stock_dw.fact_trades;
```

Counts should match.

---

# STEP 5 — Optional: Create ETL Metadata Table

```sql
CREATE TABLE etl_metadata (
  last_execution_id BIGINT,
  last_run_time TIMESTAMP
);
```

Use this to track incremental loads instead of full scans.

---

# Teaching Concepts Covered

- Incremental ETL
- SCD Type 1 dimensions
- Surrogate keys vs business keys
- Idempotent fact loading
- Data validation
- Production-safe loading patterns

---

# Recommended Production Enhancements

- Use batch processing
- Add transaction control (BEGIN / COMMIT)
- Log ETL row counts
- Add error handling
- Implement SCD Type 2 for dim_account (advanced topic)

---

END OF GUIDE
