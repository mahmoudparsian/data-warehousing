-- --------------------
-- Star Schema Database
-- --------------------

-- --------------------
-- Table Definitions
-- --------------------

-- ---------------
-- create database
-- ---------------
CREATE DATABASE bike_store;

-- ---------------
-- select database
-- ---------------
USE bike_store; 

-- -------------------------
-- Dimension Table: Products
-- -------------------------
CREATE TABLE Products (
    Product_ID INT PRIMARY KEY AUTO_INCREMENT,
    Product_Name VARCHAR(100) NOT NULL,
    Category VARCHAR(20) NOT NULL
);

-- --------------------------
-- Dimension Table: Customers
-- --------------------------
CREATE TABLE Customers (
    Customer_ID INT PRIMARY KEY AUTO_INCREMENT,
    Customer_Name VARCHAR(100) NOT NULL
);

-- -------------------------
-- Dimension Table: Dates
-- -------------------------
CREATE TABLE Dates (
    Date_ID INT PRIMARY KEY AUTO_INCREMENT,
    Date DATE NOT NULL,
    Year INT NOT NULL,
    Month INT NOT NULL
);

-- -------------------------
-- Fact Table: SalesFact
-- -------------------------
CREATE TABLE SalesFact (
    Sale_ID INT PRIMARY KEY AUTO_INCREMENT,
    Product_ID INT NOT NULL,
    Customer_ID INT NOT NULL,
    Date_ID INT NOT NULL,
    Quantity INT NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (Product_ID) REFERENCES Products(Product_ID),
    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID),
    FOREIGN KEY (Date_ID) REFERENCES Dates(Date_ID)
);


-- -----------------
-- Table Populations
-- -----------------

-- ---------------------------------------
-- Populate the table with sample values:
-- ---------------------------------------

-- ------------------
-- Products Table
-- ------------------
INSERT INTO Products (Product_Name, Category)
VALUES 
('Mountain Bike - Tera A', 'Mountain'),    -- Product_ID = 1
('Mountain Bike - Tera B', 'Mountain'),    -- Product_ID = 2
('Mountain Bike - Tera C', 'Hybrid'),      -- Product_ID = 3
('Bike Helmet - SafeHelmets', 'Simple'),   -- Product_ID = 4
('Bike Lock - SecuLock', 'MISC'),          -- Product_ID = 5
('Fixed gear bike - SlowRoad', 'Regular'), -- Product_ID = 6
('Fixed gear bike - Road', 'Regular'),     -- Product_ID = 7
('Fixed gear bike - FastRoad', 'Regular'), -- Product_ID = 8
('Hybrid bike - SlowRoad', 'Hybrid'),      -- Product_ID = 9
('E-bike - Type 1'),                       -- Product_ID = 10
('E-bike - Type 2'),                       -- Product_ID = 11
('E-bike - Type 3'),                       -- Product_ID = 12
('E-bike - Type 4'),                       -- Product_ID = 13
('E-bike - Type 5'),                       -- Product_ID = 14
('E-bike - Type 6'),                       -- Product_ID = 15
('Advanced E-bike - Type 1'),              -- Product_ID = 16
('Advanced E-bike - Type 2'),              -- Product_ID = 17
('Advanced E-bike - Type 3'),              -- Product_ID = 18
('Advanced E-bike - Type 4'),              -- Product_ID = 19
('Advanced E-bike - Type 5'),              -- Product_ID = 20
('Advanced E-bike - Type 6');              -- Product_ID = 21


-- ------------------
-- Customers Table
-- ------------------
INSERT INTO Customers (Customer_Name)
VALUES 
('Megan Johnson'),  -- Customer_ID = 1
('David Chen'),     -- Customer_ID = 2
('Maria Thompson'), -- Customer_ID = 3
('Betty Ford'),     -- Customer_ID = 4
('David Taylor'),   -- Customer_ID = 5
('Maria Bush'),     -- Customer_ID = 6
('Rafa Jaan'),      -- Customer_ID = 7
('David Bentley'),  -- Customer_ID = 8
('Maria Shriver'),  -- Customer_ID = 9
('Pat Rafter'),     -- Customer_ID = 10
('Megan Kelley'),   -- Customer_ID = 11
('Frank Morris'),   -- Customer_ID = 12
('Vahik Mina'),     -- Customer_ID = 13
('Dave Soltan'),    -- Customer_ID = 14
('Mary Paul'),      -- Customer_ID = 15
('Pat Ford'),       -- Customer_ID = 16
('Al Kelley'),      -- Customer_ID = 17
('Frank Ford'),     -- Customer_ID = 18
('Tommy Davidson'), -- Customer_ID = 19
('Carlos Alcaraz'); -- Customer_ID = 20

-- ------------------
-- Dates Table
-- ------------------
INSERT INTO Dates (Date, Year, Month)
VALUES 
('2024-01-01', 2024, 1),
('2025-10-02', 2025, 10),
('2025-03-07', 1025, 3),
('2025-08-10', 2025, 8),
('2025-12-04', 2025, 12),
('2025-12-05', 2025, 12),
('2025-12-06', 2025, 12),
('2025-02-13', 2025, 2),
('2025-02-14', 2025, 2),
('2025-02-15', 2025, 2),
('2024-03-17', 2024, 3),
('2024-03-18', 2024, 3),
('2024-03-19', 2024, 3);

-- ------------------
-- SalesFact Table
-- ------------------
INSERT INTO SalesFact (Product_ID, Customer_ID, Date_ID, Quantity, Amount)
VALUES 
(3, 2, 1, 1, 100.00),
(1, 1, 1, 2, 850.00),
(2, 1, 3, 1, 45.00),
(4, 3, 2, 1, 1200.00),
(5, 1, 5, 1, 450.00),
(6, 3, 6, 3, 1000.00),
(7, 4, 5, 1, 850.00),
(8, 6, 5, 2, 1400.00),
(6, 6, 7, 1, 650.00),
(9, 8, 8, 1, 1100.00),
(9, 3, 8, 1, 600.00);

-- -----------
-- verify data
-- -----------
SELECT * FROM Products;
SELECT * FROM Customers;
SELECT * FROM Dates;
SELECT * FROM SalesFact;

