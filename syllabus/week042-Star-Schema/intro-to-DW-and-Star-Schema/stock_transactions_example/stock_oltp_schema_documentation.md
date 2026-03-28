# Stock Trading OLTP System -- Full Schema Documentation

## Overview

This document describes the transactional (OLTP) schema for a stock
trading system. The system models users, trading accounts, stock
exchanges, stock symbols, orders, and executions (trade fills).

The schema follows a normalized 3NF structure suitable for transactional
workloads.

------------------------------------------------------------------------

# 1. users

Represents customers using the trading platform.

``` sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    gender VARCHAR(10),              -- MALE / FEMALE
    first_name VARCHAR(155),
    last_name VARCHAR(155),
    email VARCHAR(155),
    country VARCHAR(25),
    city VARCHAR(155),
    date_joined DATE
);
```

### Description

-   One row per customer.
-   A user may open multiple trading accounts.

Relationship:

    users (1) → (many) accounts

------------------------------------------------------------------------

# 2. accounts

Represents trading accounts owned by users.

``` sql
CREATE TABLE accounts (
    account_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    account_type VARCHAR(20),        -- Individual / Joint / IRA
    account_status VARCHAR(20),      -- Active / Suspended
    balance DOUBLE,
    created_at DATE
);
```

### Description

-   One row per trading account.
-   Each account belongs to one user.
-   A user may have multiple accounts.

Foreign Key:

    accounts.user_id → users.user_id

------------------------------------------------------------------------

# 3. exchanges

Represents stock exchanges where securities are listed.

``` sql
CREATE TABLE exchanges (
    exchange_id INTEGER PRIMARY KEY,
    exchange_name VARCHAR(100),      -- NYSE / NASDAQ / etc.
    country VARCHAR(50),
    timezone VARCHAR(50)
);
```

### Description

-   One exchange lists many stock symbols.

Relationship:

    exchanges (1) → (many) symbols

------------------------------------------------------------------------

# 4. symbols

Represents tradable stock instruments.

``` sql
CREATE TABLE symbols (
    symbol_id INTEGER PRIMARY KEY,
    symbol VARCHAR(16),              -- AAPL, MSFT, etc.
    company_name VARCHAR(255),
    sector VARCHAR(100),
    industry VARCHAR(100),
    date_added DATE,
    exchange_id INTEGER
);
```

### Description

-   One row per stock/security.
-   Each symbol belongs to one exchange.

Foreign Key:

    symbols.exchange_id → exchanges.exchange_id

------------------------------------------------------------------------

# 5. orders

Represents trading requests submitted by accounts.

``` sql
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    account_id INTEGER,
    symbol_id INTEGER,
    order_type VARCHAR(20),          -- Market / Limit / Stop
    price DOUBLE,                    -- Requested price
    quantity INTEGER,                -- Requested quantity
    order_date DATE,
    buy_or_sell VARCHAR(10),         -- buy / sell
    order_status VARCHAR(20)         -- executed / cancelled / pending
);
```

### Description

-   One row per order request.
-   Represents customer intent.
-   An order may execute partially or fully.

Foreign Keys:

    orders.account_id → accounts.account_id
    orders.symbol_id  → symbols.symbol_id

Relationships:

    accounts (1) → (many) orders
    symbols  (1) → (many) orders

------------------------------------------------------------------------

# 6. executions

Represents actual market trade fills.

``` sql
CREATE TABLE executions (
    execution_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    execution_price DOUBLE,
    execution_quantity INTEGER,
    execution_time TIMESTAMP,
    execution_fee DOUBLE
);
```

### Description

-   One row per actual trade execution.
-   An order may generate multiple executions (partial fills).
-   This table represents real financial events.

Foreign Key:

    executions.order_id → orders.order_id

Relationship:

    orders (1) → (many) executions

------------------------------------------------------------------------

# Complete Relationship Overview

    users
       ↓
    accounts
       ↓
    orders
       ↓
    executions

    symbols
       ↑
    exchanges

Full Relationship Map:

    users (1) --------< accounts (1) --------< orders (1) --------< executions
                                                                   \------> symbols (1) ------< exchanges

------------------------------------------------------------------------

# Key Business Concepts

-   Users place orders through accounts.
-   Orders represent intent.
-   Executions represent actual trades.
-   Revenue, volume, and P&L are calculated from executions.
-   Symbols belong to exchanges.

------------------------------------------------------------------------

# Normalization Level

The OLTP schema is:

-   In 3NF
-   Fully normalized
-   Optimized for transactional integrity
-   Designed for high-frequency trading inserts

------------------------------------------------------------------------

# Next Step

This OLTP model will be used to:

1.  Build staging tables
2.  Design ETL transformations
3.  Create a Star Schema (Data Warehouse)
4.  Support analytical queries (OLAP)
