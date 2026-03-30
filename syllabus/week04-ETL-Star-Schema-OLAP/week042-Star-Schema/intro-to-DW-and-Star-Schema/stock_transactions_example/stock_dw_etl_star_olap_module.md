# Stock Trading DW Module (MySQL): 

ETL Grain → Star Schema → ETL SQL → OLAP Queries

This document assumes you already created 
and loaded the **OLTP** schema:

```
users
accounts 
exchanges 
symbols
orders
executions
```

> **MySQL version:** The SQL below is written for **MySQL 8+** 
(uses CTEs and window functions).

---

## 1) 🎯 Define the ETL Grain Precisely

### Fact grain decision (execution-level)
**Grain:** **1 row in the fact table = 1 execution fill** 
(one partial/full fill of an order).

**Why this grain is correct for analytics:**
- Captures partial fills (an order may have multiple executions).
- Supports accurate revenue/fees/volume reporting.
- Enables intraday analysis (execution timestamp).
- Supports slippage analysis later (order requested price vs executed price).

### Measures at this grain
At execution grain, typical measures include:
- `execution_quantity`
- `execution_price`
- `execution_fee`
- `trade_value = execution_price * execution_quantity`

---

## 2) 🏗 Design the Star Schema

### Star Schema Overview (denormalized dimensions)
We design a **true star**: dimensions connect only to the fact (no dimension-to-dimension joins).

**Core tables**
- **Fact:** `fact_trades` (1 row per execution)
- **Dimensions:** `dim_date`, `dim_symbol`, `dim_account`, `dim_order_type`, `dim_order_status`, `dim_side`

### 2.1 Create a dedicated DW database (optional)
```sql
CREATE DATABASE IF NOT EXISTS stock_dw;
USE stock_dw;
```

> If your OLTP tables are in another database (e.g., `stock_oltp`), you can reference them with `stock_oltp.table_name` in ETL SQL.

---

## 2.2 Dimension Tables (DDL)

### dim_date
```sql
CREATE TABLE IF NOT EXISTS dim_date (
  date_id INT AUTO_INCREMENT PRIMARY KEY,
  full_date DATE NOT NULL,
  year INT NOT NULL,
  quarter INT NOT NULL,
  month INT NOT NULL,
  day INT NOT NULL,
  day_name VARCHAR(10) NOT NULL,
  month_name VARCHAR(10) NOT NULL,
  is_weekend TINYINT NOT NULL,
  UNIQUE KEY uk_dim_date_full_date (full_date)
);
```

### dim_symbol (denormalized: includes exchange attributes)
```sql
CREATE TABLE IF NOT EXISTS dim_symbol (
  symbol_key INT AUTO_INCREMENT PRIMARY KEY,
  symbol_id INT NOT NULL,                 -- business key from OLTP
  symbol VARCHAR(16) NOT NULL,
  company_name VARCHAR(255),
  sector VARCHAR(100),
  industry VARCHAR(100),
  exchange_name VARCHAR(100),
  exchange_country VARCHAR(50),
  exchange_timezone VARCHAR(50),
  date_added DATE,
  UNIQUE KEY uk_dim_symbol_symbol_id (symbol_id)
);
```

### dim_account (denormalized: account + user attributes)
```sql
CREATE TABLE IF NOT EXISTS dim_account (
  account_key INT AUTO_INCREMENT PRIMARY KEY,
  account_id INT NOT NULL,                -- business key from OLTP
  user_id INT NOT NULL,                   -- business key from OLTP
  account_type VARCHAR(20),
  account_status VARCHAR(20),
  user_gender VARCHAR(10),
  user_first_name VARCHAR(155),
  user_last_name VARCHAR(155),
  user_email VARCHAR(155),
  user_country VARCHAR(25),
  user_city VARCHAR(155),
  user_date_joined DATE,
  account_created_at DATE,
  UNIQUE KEY uk_dim_account_account_id (account_id)
);
```

### dim_side (buy/sell)
```sql
CREATE TABLE IF NOT EXISTS dim_side (
  side_key INT AUTO_INCREMENT PRIMARY KEY,
  side_code VARCHAR(10) NOT NULL,         -- 'buy' or 'sell'
  UNIQUE KEY uk_dim_side_code (side_code)
);
```

### dim_order_type (Market/Limit/Stop)
```sql
CREATE TABLE IF NOT EXISTS dim_order_type (
  order_type_key INT AUTO_INCREMENT PRIMARY KEY,
  order_type VARCHAR(20) NOT NULL,
  UNIQUE KEY uk_dim_order_type (order_type)
);
```

### dim_order_status (executed/cancelled/pending)
```sql
CREATE TABLE IF NOT EXISTS dim_order_status (
  order_status_key INT AUTO_INCREMENT PRIMARY KEY,
  order_status VARCHAR(20) NOT NULL,
  UNIQUE KEY uk_dim_order_status (order_status)
);
```

---

## 2.3 Fact Table (DDL)

### fact_trades (1 row per execution)
```sql
CREATE TABLE IF NOT EXISTS fact_trades (
  trade_key BIGINT AUTO_INCREMENT PRIMARY KEY,

  -- Dimension foreign keys (surrogate keys)
  date_id INT NOT NULL,
  symbol_key INT NOT NULL,
  account_key INT NOT NULL,
  side_key INT NOT NULL,
  order_type_key INT NOT NULL,
  order_status_key INT NOT NULL,

  -- Degenerate dimensions / identifiers (kept for traceability)
  order_id INT NOT NULL,
  execution_id INT NOT NULL,

  -- Measures
  execution_price DOUBLE NOT NULL,
  execution_quantity INT NOT NULL,
  execution_fee DOUBLE NOT NULL,
  trade_value DOUBLE NOT NULL,

  -- Optional timestamp (kept in fact for intraday analytics)
  execution_time TIMESTAMP NOT NULL,

  KEY idx_fact_date (date_id),
  KEY idx_fact_symbol (symbol_key),
  KEY idx_fact_account (account_key),
  KEY idx_fact_order (order_id),
  UNIQUE KEY uk_fact_execution (execution_id)
);
```

---

## 3) 🔄 Write Transformation SQL (ETL)

### ETL Strategy (simple and teachable)
1. Populate small “code” dimensions (`dim_side`, `dim_order_type`, `dim_order_status`).
2. Populate `dim_date` for a date range used by orders/executions.
3. Populate `dim_symbol` from OLTP `symbols + exchanges` (flattened).
4. Populate `dim_account` from OLTP `accounts + users` (flattened).
5. Populate `fact_trades` from OLTP `executions + orders` plus dimension lookups.

> In teaching, it’s useful to do ETL in **repeatable steps** (truncate + reload) first, then discuss incremental loads.

---

### 3.1 Code Dimensions

```sql
INSERT IGNORE INTO dim_side (side_code) VALUES ('buy'), ('sell');

INSERT IGNORE INTO dim_order_type (order_type)
SELECT DISTINCT order_type FROM stock_oltp.orders;

INSERT IGNORE INTO dim_order_status (order_status)
SELECT DISTINCT order_status FROM stock_oltp.orders;
```

---

### 3.2 dim_date population (2018–2024 example)

#### Option A (recommended): recursive CTE (MySQL 8+)
```sql
WITH RECURSIVE dates AS (
  SELECT DATE('2018-01-01') AS d
  UNION ALL
  SELECT DATE_ADD(d, INTERVAL 1 DAY) FROM dates
  WHERE d < DATE('2024-12-31')
)
INSERT IGNORE INTO dim_date
(full_date, year, quarter, month, day, day_name, month_name, is_weekend)
SELECT
  d AS full_date,
  YEAR(d) AS year,
  QUARTER(d) AS quarter,
  MONTH(d) AS month,
  DAY(d) AS day,
  DAYNAME(d) AS day_name,
  MONTHNAME(d) AS month_name,
  CASE WHEN DAYOFWEEK(d) IN (1,7) THEN 1 ELSE 0 END AS is_weekend
FROM dates;
```

---

### 3.3 dim_symbol load (flatten symbols + exchanges)
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
  e.country AS exchange_country,
  e.timezone AS exchange_timezone,
  s.date_added
FROM stock_oltp.symbols s
JOIN stock_oltp.exchanges e
  ON s.exchange_id = e.exchange_id
ON DUPLICATE KEY UPDATE
  symbol = VALUES(symbol),
  company_name = VALUES(company_name),
  sector = VALUES(sector),
  industry = VALUES(industry),
  exchange_name = VALUES(exchange_name),
  exchange_country = VALUES(exchange_country),
  exchange_timezone = VALUES(exchange_timezone),
  date_added = VALUES(date_added);
```

---

### 3.4 dim_account load (flatten accounts + users)
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
ON DUPLICATE KEY UPDATE
  user_id = VALUES(user_id),
  account_type = VALUES(account_type),
  account_status = VALUES(account_status),
  user_gender = VALUES(user_gender),
  user_first_name = VALUES(user_first_name),
  user_last_name = VALUES(user_last_name),
  user_email = VALUES(user_email),
  user_country = VALUES(user_country),
  user_city = VALUES(user_city),
  user_date_joined = VALUES(user_date_joined),
  account_created_at = VALUES(account_created_at);
```

---

### 3.5 fact_trades load (executions + orders + dimension lookups)

**Key mapping rules**
- `date_id` comes from `DATE(execution_time)` (or `orders.order_date` if you prefer day-grain by order date).
- `symbol_key` from `dim_symbol` via `orders.symbol_id`
- `account_key` from `dim_account` via `orders.account_id`
- `side_key` from `dim_side` via `orders.buy_or_sell`
- `order_type_key` from `dim_order_type` via `orders.order_type`
- `order_status_key` from `dim_order_status` via `orders.order_status`

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

ON DUPLICATE KEY UPDATE
  execution_price = VALUES(execution_price),
  execution_quantity = VALUES(execution_quantity),
  execution_fee = VALUES(execution_fee),
  trade_value = VALUES(trade_value),
  execution_time = VALUES(execution_time);
```

> Teaching note: With 300k executions, add indexes on OLTP keys (`orders.order_id`, `executions.order_id`) and on DW business keys (`dim_symbol.symbol_id`, `dim_account.account_id`, `dim_date.full_date`).

---

## 4) 📊 Teaching-Grade OLAP Queries (Star Schema)

Below are **12 realistic OLAP queries** using aggregation, CTEs, window functions, and rollups.
Assume you’re querying the DW tables in `stock_dw`.

---

### Q1) Total trade value (all time)
```sql
SELECT SUM(trade_value) AS total_trade_value
FROM fact_trades;
```

### Q2) Total fees by year
```sql
SELECT d.year, SUM(f.execution_fee) AS total_fees
FROM fact_trades f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year
ORDER BY d.year;
```

### Q3) Top 10 symbols by total trade value
```sql
SELECT s.symbol, SUM(f.trade_value) AS total_value
FROM fact_trades f
JOIN dim_symbol s ON f.symbol_key = s.symbol_key
GROUP BY s.symbol
ORDER BY total_value DESC
LIMIT 10;
```

### Q4) Top 5 countries by total trade value
```sql
SELECT a.user_country, SUM(f.trade_value) AS total_value
FROM fact_trades f
JOIN dim_account a ON f.account_key = a.account_key
GROUP BY a.user_country
ORDER BY total_value DESC
LIMIT 5;
```

### Q5) Buy vs Sell volume (shares) by month
```sql
SELECT
  d.year, d.month,
  side.side_code,
  SUM(f.execution_quantity) AS total_shares
FROM fact_trades f
JOIN dim_date d ON f.date_id = d.date_id
JOIN dim_side side ON f.side_key = side.side_key
GROUP BY d.year, d.month, side.side_code
ORDER BY d.year, d.month, side.side_code;
```

### Q6) Average execution price by sector (with a minimum trade count)
```sql
SELECT
  s.sector,
  AVG(f.execution_price) AS avg_exec_price,
  COUNT(*) AS trade_count
FROM fact_trades f
JOIN dim_symbol s ON f.symbol_key = s.symbol_key
GROUP BY s.sector
HAVING COUNT(*) >= 1000
ORDER BY avg_exec_price DESC;
```

### Q7) Daily trade value trend (last 30 days in the dimension range)
```sql
WITH daily AS (
  SELECT d.full_date, SUM(f.trade_value) AS total_value
  FROM fact_trades f
  JOIN dim_date d ON f.date_id = d.date_id
  GROUP BY d.full_date
)
SELECT *
FROM daily
ORDER BY full_date DESC
LIMIT 30;
```

### Q8) Top 3 symbols per country (window function)
```sql
WITH country_symbol AS (
  SELECT
    a.user_country,
    s.symbol,
    SUM(f.trade_value) AS total_value
  FROM fact_trades f
  JOIN dim_account a ON f.account_key = a.account_key
  JOIN dim_symbol s ON f.symbol_key = s.symbol_key
  GROUP BY a.user_country, s.symbol
),
ranked AS (
  SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY user_country ORDER BY total_value DESC) AS rn
  FROM country_symbol
)
SELECT user_country, symbol, total_value
FROM ranked
WHERE rn <= 3
ORDER BY user_country, total_value DESC;
```

### Q9) Order type mix by year (percent contribution)
```sql
WITH yearly AS (
  SELECT
    d.year,
    ot.order_type,
    COUNT(*) AS cnt
  FROM fact_trades f
  JOIN dim_date d ON f.date_id = d.date_id
  JOIN dim_order_type ot ON f.order_type_key = ot.order_type_key
  GROUP BY d.year, ot.order_type
),
totals AS (
  SELECT year, SUM(cnt) AS year_total
  FROM yearly
  GROUP BY year
)
SELECT
  y.year,
  y.order_type,
  y.cnt,
  ROUND(100.0 * y.cnt / t.year_total, 2) AS pct_of_year
FROM yearly y
JOIN totals t ON y.year = t.year
ORDER BY y.year, pct_of_year DESC;
```

### Q10) Revenue rollup by (country → city → grand total)
```sql
SELECT
  a.user_country,
  a.user_city,
  SUM(f.trade_value) AS total_value
FROM fact_trades f
JOIN dim_account a ON f.account_key = a.account_key
GROUP BY a.user_country, a.user_city WITH ROLLUP;
```

### Q11) Identify high-fee accounts (top 20 by total fees)
```sql
SELECT
  a.account_id,
  a.user_email,
  SUM(f.execution_fee) AS total_fees
FROM fact_trades f
JOIN dim_account a ON f.account_key = a.account_key
GROUP BY a.account_id, a.user_email
ORDER BY total_fees DESC
LIMIT 20;
```

### Q12) Detect potential “execution fragmentation” (orders with many fills)
```sql
SELECT
  f.order_id,
  COUNT(*) AS num_executions,
  SUM(f.execution_quantity) AS total_shares,
  SUM(f.trade_value) AS total_value
FROM fact_trades f
GROUP BY f.order_id
HAVING COUNT(*) >= 10
ORDER BY num_executions DESC, total_value DESC
LIMIT 50;
```

---

## Appendix: Recommended Indexes (DW)

```sql
-- Dimension business key lookup indexes
CREATE INDEX idx_dim_date_full_date ON dim_date(full_date);
CREATE INDEX idx_dim_symbol_symbol_id ON dim_symbol(symbol_id);
CREATE INDEX idx_dim_account_account_id ON dim_account(account_id);

-- Fact foreign-key / query acceleration indexes
CREATE INDEX idx_fact_trades_date_id ON fact_trades(date_id);
CREATE INDEX idx_fact_trades_symbol_key ON fact_trades(symbol_key);
CREATE INDEX idx_fact_trades_account_key ON fact_trades(account_key);
CREATE INDEX idx_fact_trades_side_key ON fact_trades(side_key);
```

---

## What you can teach from this module

- **Grain** (why execution-level is correct)
- **Star schema** design and denormalization choices
- **ETL patterns** (code dimensions, date dimension, dimension lookups)
- **OLAP queries** (CTEs, window functions, rollup, percent-of-total)
- **Performance** (indexes, lookup keys, large fact loading)

