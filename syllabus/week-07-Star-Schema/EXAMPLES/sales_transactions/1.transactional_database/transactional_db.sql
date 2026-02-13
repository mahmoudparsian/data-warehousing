-- ### Sample Transactional Tables and Data

DROP DATABASE IF EXISTS sales_database;

CREATE DATABASE sales_database;

USE sales_database;

-- #### 1.1 Sales Table (MySQL)

CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    store_id INT,
    sale_date DATE,
    quantity INT,
    amount INT
);

INSERT INTO sales 
(sale_id, customer_id, product_id, 
store_id, sale_date, quantity, amount) 
VALUES
(1, 101, 201, 301, '2025-01-01', 2, 100),
(2, 102, 202, 302, '2025-01-02', 1, 50),
(3, 103, 203, 303, '2025-01-03', 5, 250),
(4, 101, 201, 301, '2025-01-11', 2, 100),
(5, 102, 202, 302, '2025-01-22', 1, 50),
(6, 103, 203, 303, '2025-01-13', 5, 250);


-- #### 1.2 Customers Table

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100)
);

INSERT INTO customers 
(customer_id, customer_name, customer_email) 
VALUES
(101, 'John Doe', 'john.doe@example.com'),
(102, 'Jane Smith', 'jane.smith@example.com'),
(103, 'Robert Johnson', 'robert.johnson@example.com'),
(104, 'David Foster', 'david2@example.com'),
(105, 'Bob Smith', 'bob77@example.com'),
(106, 'Robert King', 'robert.king@example.com');


-- #### 1.3 Products Table

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    product_category VARCHAR(100)
);

INSERT INTO products (product_id, product_name, product_category) 
VALUES
(201, 'Laptop', 'Electronics'),
(202, 'Smartphone', 'Electronics'),
(203, 'Tablet', 'Electronics'),
(204, 'TV', 'Electronics'),
(205, 'Pager', 'Electronics'),
(206, 'Table', 'Home');


-- #### 1.4 Stores Table

CREATE TABLE stores (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(100),
    store_location VARCHAR(100)
);

INSERT INTO stores (store_id, store_name, store_location) 
VALUES
(301, 'Store A', 'New York'),
(302, 'Store B', 'Los Angeles'),
(303, 'Store C', 'Chicago'),
(304, 'Store D', 'Sunnyvale'),
(305, 'Store E', 'Cupertino'),
(306, 'Store F', 'Chicago');


