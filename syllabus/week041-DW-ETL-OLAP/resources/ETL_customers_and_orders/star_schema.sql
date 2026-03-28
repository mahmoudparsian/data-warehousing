-- ----------------------
-- Star Schema (MySQL 8+)
-- ----------------------
DROP TABLE IF EXISTS fact_orders;
DROP TABLE IF EXISTS dim_dates;
DROP TABLE IF EXISTS dim_customers;

CREATE TABLE dim_customers (
  customer_id INT PRIMARY KEY,
  country VARCHAR(20) NOT NULL,
  age INT NOT NULL,
  gender VARCHAR(12) NOT NULL,
  signup_year INT NOT NULL
);

CREATE TABLE dim_dates (
  date_id INT PRIMARY KEY,          -- YYYYMMDD
  date DATE NOT NULL,
  year SMALLINT NOT NULL,
  month TINYINT NOT NULL,
  day TINYINT NOT NULL,
  quarter TINYINT NOT NULL
);

CREATE TABLE fact_orders (
  order_id INT PRIMARY KEY,
  customer_id INT NOT NULL,
  date_id INT NOT NULL,
  order_date DATE NOT NULL,         -- optional lineage column
  channel VARCHAR(10) NOT NULL,
  order_amount DECIMAL(12,2) NOT NULL,
  tax DECIMAL(12,2) NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
  FOREIGN KEY (date_id) REFERENCES dim_dates(date_id)
);

-- Helpful indexes for OLAP
CREATE INDEX idx_fact_orders_customer ON fact_orders(customer_id);
CREATE INDEX idx_fact_orders_date ON fact_orders(date_id);
CREATE INDEX idx_fact_orders_channel ON fact_orders(channel);
