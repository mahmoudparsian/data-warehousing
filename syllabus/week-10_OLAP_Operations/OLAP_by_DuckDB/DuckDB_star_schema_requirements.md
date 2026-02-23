STEP-1 : first validate the schema (no data generation yet)
         Give me your suggestions, but I do not want to expand too much

STEP-2: then given suggestions on the number of records  per table:
        I want a small db in DuckDB

STEP-3: best way to load data into duckdb tables


Let's Build a Star Schema: SQL Examples

Let's get our hands dirty with some SQL. 
Here's how to implement our online sales 
star schema using standard SQL syntax. 

Below represents a standard SQL approach. 

Step 1: Create the Dimension Tables
Let's start with defining the tables that provide context:

-- Dimension Table for Dates
CREATE TABLE dates (
    date_key INT PRIMARY KEY, -- Example: 20240424
    full_date DATE NOT NULL,
    day_of_month INT NOT NULL,
    day_of_week VARCHAR(10) NOT NULL,
    month_of_year INT NOT NULL,
    month_name VARCHAR(10) NOT NULL,
    quarter INT NOT NULL,
    year INT NOT NULL,
    is_weekend BOOLEAN NOT NULL
);

-- Sequence for Dim customers Primary Key
CREATE SEQUENCE customer_key_seq START 1;

-- Dimension Table for Customers
CREATE TABLE customers (
    customer_key INTEGER PRIMARY KEY DEFAULT nextval('customer_key_seq'), -- Auto-incrementing key via sequence
    customer_id VARCHAR(50) UNIQUE, -- Business key from source system
    customer_name VARCHAR(255) NOT NULL,
    gender VARCHAR(10) CHECK (gender IN ('MALE','FEMALE')), 
    email VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    segment VARCHAR(50) -- e.g., 'Retail', 'Wholesale'
);

-- Sequence for Dim products Primary Key
CREATE SEQUENCE product_key_seq START 1;

-- Dimension Table for Products
CREATE TABLE products (
    product_key INTEGER PRIMARY KEY DEFAULT nextval('product_key_seq'), -- Auto-incrementing key via sequence
    product_id VARCHAR(50) UNIQUE, -- Business key from source system
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    brand VARCHAR(100),
    color VARCHAR(50),
    cost DECIMAL(10, 2) -- Cost price might live here
);

-- Sequence for Dim stores Primary Key
CREATE SEQUENCE store_key_seq START 1;

-- Dimension Table for Stores (Optional, if relevant)
CREATE TABLE stores (
    store_key INTEGER PRIMARY KEY DEFAULT nextval('store_key_seq'), -- Auto-incrementing key via sequence  
    store_id VARCHAR(50) UNIQUE, -- Business key from source system
    store_name VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100)
);

Step 2: Create the Fact Table
Now for the central table that links everything together and holds our metrics:


-- Sequence for FactSales Primary Key
CREATE SEQUENCE sales_key_seq START 1;

-- Fact Table for Sales
CREATE TABLE sales (
    sales_key BIGINT  PRIMARY KEY DEFAULT nextval('sales_key_seq'), -- Unique key for the fact row itself, auto-generated via sequence
    date_key INT NOT NULL,
    customer_key INT NOT NULL,
    product_key INT NOT NULL,
    store_key INT NOT NULL, -- Use a placeholder key if not applicable, e.g., -1 for 'Online'
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_amount DECIMAL(12, 2) NOT NULL, -- calculated as quantity * unit_price

    -- Foreign Key Constraints
    FOREIGN KEY (date_key) REFERENCES dates(date_key),
    FOREIGN KEY (customer_key) REFERENCES customers(customer_key),
    FOREIGN KEY (product_key) REFERENCES products(product_key),
    FOREIGN KEY (store_key) REFERENCES stores(store_key)
);

-- Optional: Create indexes on foreign keys for better join performance
CREATE INDEX idx_sales_date ON sales(date_key);
CREATE INDEX idx_sales_customer ON sales(customer_key);
CREATE INDEX idx_sales_product ON sales(product_key);
CREATE INDEX idx_sales_store ON sales(store_key);

Sample: Querying the Star Schema
Let's write a query to answer a business question: 
"What were the total sales amounts for 
 each product category in January 2024?"

SELECT
    dp.category,
    SUM(s.total_amount) AS total_sales_amount
FROM
    sales s
JOIN
    dates d ON s.date_key = d.date_key
JOIN
    products p ON s.product_key = p.product_key
WHERE
    d.Year = 2024
    AND d.month_of_year = 1 -- January
GROUP BY
    p.category
ORDER BY
    total_sales_amount DESC;


Data Population:

1. Create 5000 customers (2000 MALE, 3000 FEMALE)

2. Create 200 products 

3. Create 10 stores  

4. Create 10,000,000 sales records for 3 years: 
   2023, 2024, 2025 (do not create symmetric data)

5. Create dates table from the sales table

