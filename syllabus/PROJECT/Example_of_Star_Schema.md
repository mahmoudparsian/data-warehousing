# Star Schema for Bike Store

```sql
CREATE DATABASE bike_store;
USE bike_store; 

-- -------------------------
-- Dimension Table: stores
-- -------------------------
CREATE TABLE stores (
    store_id INT PRIMARY KEY AUTO_INCREMENT,
    store_location VARCHAR(100) NOT NULL
);

-- -------------------------
-- Dimension Table: Products
-- -------------------------
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(20) NOT NULL
);

-- --------------------------
-- Dimension Table: customers
-- --------------------------
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL,  -- MALE/FEMALE
    country VARCHAR(20) NOT NULL, -- USA/CANADA/MEXICO/GERMANY/FRANCE/INDIA/CHINA/TURKEY/ENGLAND/ITALY
    email VARCHAR(40)
);

-- -------------------------
-- Dimension Table: dates
-- -------------------------
CREATE TABLE dates (
    date_id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,
    quarter INT NOT NULL
);

-- -------------------------
-- Fact Table: sales
-- -------------------------
CREATE TABLE sales (
    sale_id INT PRIMARY KEY AUTO_INCREMENT,
    sale_type VARCHAR(10) NOT NULL, -- IN-STORE/ON-LINE
    product_id INT NOT NULL,
    store_id INT NOT NULL,
    customer_id INT NOT NULL,
    date_id INT NOT NULL,
    quantity INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    sale_amount DECIMAL(10, 2) NOT NULL, -- sale_amount = quantity * amount
    
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (store_id) REFERENCES stores(store_id),
    FOREIGN KEY (date_id) REFERENCES Dates(date_id)
);
```