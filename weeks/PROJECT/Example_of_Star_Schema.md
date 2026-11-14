# Star Schema for Bike Store

A small star schema in **DuckDB** syntax: four dimension tables and one fact table.
Save the first SQL block as `bike_store_schema.sql` and run `duckdb bike_store.duckdb < bike_store_schema.sql`, or paste it into a notebook cell.
(Tested with DuckDB 2.0: the test below returns one row, and a sale with an unknown `product_id` is rejected by the foreign key.)

Surrogate keys come from **sequences** (`DEFAULT nextval(...)`), so an `INSERT` without a key gets the next number
(the DuckDB way of MySQL's `AUTO_INCREMENT`). The OLAP questions for this schema are in
[`Example_of_OLAP_Queries.md`](Example_of_OLAP_Queries.md).

```sql
-- -------------------------
-- Dimension Table: stores
-- -------------------------
CREATE SEQUENCE seq_store_id START 1;
CREATE TABLE stores (
    store_id       INTEGER PRIMARY KEY DEFAULT nextval('seq_store_id'),
    store_location VARCHAR(100) NOT NULL
);

-- -------------------------
-- Dimension Table: products
-- -------------------------
CREATE SEQUENCE seq_product_id START 1;
CREATE TABLE products (
    product_id   INTEGER PRIMARY KEY DEFAULT nextval('seq_product_id'),
    product_name VARCHAR(100) NOT NULL,
    category     VARCHAR(20)  NOT NULL
);

-- --------------------------
-- Dimension Table: customers
-- --------------------------
CREATE SEQUENCE seq_customer_id START 1;
CREATE TABLE customers (
    customer_id   INTEGER PRIMARY KEY DEFAULT nextval('seq_customer_id'),
    customer_name VARCHAR(100) NOT NULL,
    gender        VARCHAR(10)  NOT NULL,  -- MALE/FEMALE
    country       VARCHAR(20)  NOT NULL,  -- USA/CANADA/MEXICO/GERMANY/FRANCE/INDIA/CHINA/TURKEY/ENGLAND/ITALY
    email         VARCHAR(40)
);

-- -------------------------
-- Dimension Table: dates
-- -------------------------
CREATE SEQUENCE seq_date_id START 1;
CREATE TABLE dates (
    date_id   INTEGER PRIMARY KEY DEFAULT nextval('seq_date_id'),
    full_date DATE    NOT NULL,
    year      INTEGER NOT NULL,
    month     INTEGER NOT NULL,
    day       INTEGER NOT NULL,
    quarter   INTEGER NOT NULL
);

-- -------------------------
-- Fact Table: sales
-- -------------------------
CREATE SEQUENCE seq_sale_id START 1;
CREATE TABLE sales (
    sale_id     INTEGER PRIMARY KEY DEFAULT nextval('seq_sale_id'),
    sale_type   VARCHAR(10)    NOT NULL,  -- IN-STORE/ON-LINE
    product_id  INTEGER        NOT NULL REFERENCES products (product_id),
    store_id    INTEGER        NOT NULL REFERENCES stores (store_id),
    customer_id INTEGER        NOT NULL REFERENCES customers (customer_id),
    date_id     INTEGER        NOT NULL REFERENCES dates (date_id),
    quantity    INTEGER        NOT NULL,
    amount      DECIMAL(10, 2) NOT NULL,  -- unit price
    sale_amount DECIMAL(10, 2) NOT NULL   -- sale_amount = quantity * amount
);
```

A quick test (one row per table, then a star join):

```sql
INSERT INTO stores (store_location)                    VALUES ('San Jose');
INSERT INTO products (product_name, category)          VALUES ('Trail 500', 'MOUNTAIN');
INSERT INTO customers (customer_name, gender, country) VALUES ('Ana Lopez', 'FEMALE', 'USA');
INSERT INTO dates (full_date, year, month, day, quarter) VALUES (DATE '2024-03-15', 2024, 3, 15, 1);
INSERT INTO sales (sale_type, product_id, store_id, customer_id, date_id, quantity, amount, sale_amount)
VALUES ('IN-STORE', 1, 1, 1, 1, 2, 450.00, 900.00);

SELECT d.year, s.store_location, p.category, SUM(f.sale_amount) AS revenue
FROM sales f
JOIN dates d     USING (date_id)
JOIN stores s    USING (store_id)
JOIN products p  USING (product_id)
GROUP BY ALL;
```
