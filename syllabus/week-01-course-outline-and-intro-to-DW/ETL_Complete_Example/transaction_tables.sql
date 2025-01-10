-- ---------------------
-- Create Database 
-- ---------------------
CREATE DATABASE IF NOT EXISTS sales_db;
USE sales_db;

-- ---------------------------
-- Create transactional tables
-- ---------------------------


-- ---------------------------
-- customers table
-- ---------------------------
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT  PRIMARY KEY,
    customer_name VARCHAR(50),
    age INT,
    gender VARCHAR(10)
);

INSERT INTO customers (customer_id, customer_name, age, gender) 
VALUES
(10, 'Alice', 17, 'Female'),
(11, 'Bob', 18, 'Male'),
(12, 'Charlie', 19, 'Male'),
(13, 'Jane', 30, 'Female'),
(14, 'Dave', 45, 'Male'),
(15, 'Max', 36, 'Male'),
(16, 'Mary', 32, 'Female'),
(17, 'Rafa', 38, 'Male'),
(18, 'Mark', 42, 'Male'),
(19, 'Jen', 40, 'Female'),
(20, 'Betty', 48, 'Female'),
(21, 'Barb', 58, 'Female'),
(22, 'Farid', 38, 'Male'),
(23, 'Farah', 68, 'Female'),
(24, 'Bo', 60, 'Male'),
(25, 'Coco', 28, 'Female'),
(26, 'Farzad', 25, 'Male'),
(27, 'Bedford', 70, 'Male'),
(28, 'Jennifer', 33, 'Female'),
(29, 'Martina', 37, 'Female');


-- ---------------------------
-- products table
-- ---------------------------
CREATE TABLE IF NOT EXISTS products (
    product_id INT  PRIMARY KEY,
    product_name VARCHAR(50),
    category VARCHAR(50),
    price INT
);

INSERT INTO products (product_id, product_name, category, price) 
VALUES
(100, 'Laptop', 'Electronics', 900),
(200, 'Smartphone', 'Electronics', 450),
(300, 'Tablet', 'Electronics', 280),
(400, 'Ipad', 'Electronics', 700),
(500, 'Modem', 'Electronics', 200),
(600, 'TV', 'Electronics', 820),
(650, 'Charger', 'Electronics', 55),
(700, 'Ladder', 'Home', 120),
(800, 'Cooler', 'Home', 300),
(900, 'Cooker', 'Home', 50),
(950, 'Chair', 'Home', 40),
(960, 'Table', 'Home', 170),
(965, 'Sofa', 'Home', 770),
(967, 'Bed', 'Home', 970),
(970, 'T-Shirt', 'Clothing', 18),
(975, 'Jacket', 'Clothing', 68),
(980, 'Socks', 'Clothing', 12),
(985, 'Coat', 'Clothing', 190),
(986, 'Short', 'Clothing', 35),
(987, 'Hat', 'Clothing', 30),
(988, 'Pants', 'Clothing', 55);


-- ---------------------------
-- locations table
-- ---------------------------
CREATE TABLE IF NOT EXISTS locations (
    location_id INT  PRIMARY KEY,
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50)
);

INSERT INTO locations (location_id, city, state, country) VALUES
(1000, 'New York', 'NY', 'USA'),
(1001, 'San Francisco', 'CA', 'USA'),
(1002, 'New Jersey', 'NJ', 'USA'),
(1003, 'Cupertino', 'CA', 'USA'),
(1004, 'Sunnyvale', 'CA', 'USA'),
(1005, 'Chicago', 'IL', 'USA'),
(1006, 'Troy', 'MI', 'USA'),
(1007, 'Detroit', 'MI', 'USA'),
(1008, 'Toronto', 'Ontario', 'CANADA'),
(1009, 'Montreal', 'Quebec', 'CANADA'),
(1010, 'Calgary', 'Alberta', 'CANADA'),
(1011, 'Paris', 'France', 'FRANCE'),
(1012, 'Lyon', 'France', 'FRANCE'),
(1013, 'Colmar', 'France', 'FRANCE');


-- ---------------------------
-- sales_transactions table
-- ---------------------------
CREATE TABLE IF NOT EXISTS sales_transactions (
    sale_id INT  PRIMARY KEY,
    product_id INT,
    customer_id INT,
    location_id INT,
    sale_date DATE,
    quantity INT,
    total_amount INT
);


