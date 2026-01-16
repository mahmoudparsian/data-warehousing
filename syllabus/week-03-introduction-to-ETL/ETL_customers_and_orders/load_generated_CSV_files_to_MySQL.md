Below are clean, copy-pasteable command-line instructions to load

	•	dim_customers.csv
	•	dim_dates.csv
	•	fact_orders.csv

into MySQL tables using the MySQL CLI, following best practices for OLAP / star schemas.

⸻

0️⃣ Prerequisites (once)

0.1 Verify MySQL allows CSV loading

You must enable LOCAL INFILE.

mysql --version

Then connect with:

mysql --local-infile=1 -u your_user -p

Inside MySQL, confirm:

SHOW VARIABLES LIKE 'local_infile';

You should see:

local_infile | ON


⸻

1️⃣ Create the database

CREATE DATABASE IF NOT EXISTS retail_dw;
USE retail_dw;


⸻

2️⃣ Create tables (Star Schema)

2.1 Dimension: Customers

DROP TABLE IF EXISTS dim_customers;

CREATE TABLE dim_customers (
  customer_id INT PRIMARY KEY,
  country VARCHAR(20),
  age INT,
  gender VARCHAR(12),
  signup_year INT
);


⸻

2.2 Dimension: Dates

DROP TABLE IF EXISTS dim_dates;

CREATE TABLE dim_dates (
  date_id INT PRIMARY KEY,     -- YYYYMMDD
  date DATE,
  year INT,
  month INT,
  day INT,
  quarter INT
);


⸻

2.3 Fact: Orders

DROP TABLE IF EXISTS fact_orders;

CREATE TABLE fact_orders (
  order_id INT PRIMARY KEY,
  customer_id INT,
  date_id INT,
  order_date DATE,
  channel VARCHAR(10),
  order_amount DECIMAL(12,2),
  tax DECIMAL(12,2),

  FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
  FOREIGN KEY (date_id) REFERENCES dim_dates(date_id)
);


⸻

3️⃣ Load CSV files (Command Line)

Assume your CSV files are in
/path/to/data/

3.1 Load dim_customers.csv

LOAD DATA LOCAL INFILE '/path/to/data/dim_customers.csv'
INTO TABLE dim_customers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(customer_id, country, age, gender, signup_year);


⸻

3.2 Load dim_dates.csv

LOAD DATA LOCAL INFILE '/path/to/data/dim_dates.csv'
INTO TABLE dim_dates
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(date_id, date, year, month, day, quarter);


⸻

3.3 Load fact_orders.csv

LOAD DATA LOCAL INFILE '/path/to/data/fact_orders.csv'
INTO TABLE fact_orders
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(order_id, customer_id, date_id, order_date, channel, order_amount, tax);


⸻

4️⃣ Validate the Load

SELECT COUNT(*) FROM dim_customers;
SELECT COUNT(*) FROM dim_dates;
SELECT COUNT(*) FROM fact_orders;

Expected:
	•	dim_customers ≈ 5,000
	•	fact_orders ≈ 30,000
	•	dim_dates ≈ number of unique order dates

⸻

5️⃣ Recommended OLAP Indexes (Important)

CREATE INDEX idx_fact_customer ON fact_orders(customer_id);
CREATE INDEX idx_fact_date ON fact_orders(date_id);
CREATE INDEX idx_fact_channel ON fact_orders(channel);
CREATE INDEX idx_dates_year_month ON dim_dates(year, month);


⸻

6️⃣ Common Troubleshooting

❌ ERROR 3948 (LOCAL INFILE disabled)

Fix:

mysql --local-infile=1 -u your_user -p

Or in my.cnf:

[mysqld]
local_infile=1


⸻

❌ Windows path issue

Use double backslashes:

'C:\\data\\fact_orders.csv'


⸻

✅ Result

Now, we have a fully loaded MySQL star schema ready for:
	•	OLAP queries
	•	BI tools
	•	Window functions
	•	Roll-ups and cube-style analytics
