# Star Schema example using MySQL


• Star Schema Structure: 

	This example creates a "star" schema 
	with three dimension tables (dim_date, 
	dim_customer, dim_product) and one fact 
	table (fact_sales). Each dimension table 
	holds descriptive attributes related to 
	a specific category, while the fact table 
	stores the core transactional data with 
	foreign key references to the dimension tables. 

• Data Loading Process (ETL): 

	• Extract: You would typically extract data 
	from a source system (like a CRM or ERP) using 
	SQL queries or data extraction tools. 
	
	• Transform: Clean and transform the extracted 
	data to match the required format for the dimension 
	and fact tables. 
	
	• Load: Use INSERT statements to load the transformed 
	data into the appropriate tables in your MySQL database. 



## Create the dimension tables 

~~~sql
-- 1. Date Dimension
CREATE TABLE `dim_date` (
  `date_id` INT PRIMARY KEY,
  `full_date` DATE NOT NULL,
  `year` INT NOT NULL,
  `quarter` INT NOT NULL,
  `month` INT NOT NULL,
  `day_of_week` VARCHAR(10) NOT NULL,
  `day_of_month` INT NOT NULL
);

-- 2. Customer Dimension
CREATE TABLE `dim_customer` (
  `customer_id` INT PRIMARY KEY,
  `customer_name` VARCHAR(50) NOT NULL,
  `customer_city` VARCHAR(50) NOT NULL,
  `customer_state` VARCHAR(2) NOT NULL
);

-- 3. Product Dimension
CREATE TABLE `dim_product` (
  `product_id` INT PRIMARY KEY,
  `product_name` VARCHAR(50) NOT NULL,
  `product_category` VARCHAR(50) NOT NULL,
  `product_price` DECIMAL(10,2) NOT NULL
);
~~~

## Create the Fact Table 

~~~sql
CREATE TABLE `fact_sales` (
  `sale_id` INT PRIMARY KEY AUTO_INCREMENT,
  `date_id` INT NOT NULL,
  `customer_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  `quantity_sold` INT NOT NULL,
  `sale_amount` DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (`date_id`) REFERENCES `dim_date` (`date_id`),
  FOREIGN KEY (`customer_id`) REFERENCES `dim_customer` (`customer_id`),
  FOREIGN KEY (`product_id`) REFERENCES `dim_product` (`product_id`)
);
~~~

## Sample Data for Dimension Tables

~~~sql
INSERT INTO `dim_date` 
(date_id, full_date, year, quarter, month, day_of_week, day_of_month)
VALUES
  (1, '2023-01-01', 2023, 1, 1, 'Sunday', 1),
  (2, '2023-01-02', 2023, 1, 1, 'Monday', 2),
  (3, '2023-01-03', 2023, 1, 1, 'Tuesday', 3); 

INSERT INTO `dim_customer` 
(customer_id, customer_name, customer_city, customer_state)
VALUES
  (1, 'John Doe', 'San Francisco', 'CA'),
  (2, 'Jane Smith', 'New York', 'NY'),
  (3, 'Mike Brown', 'Chicago', 'IL');

INSERT INTO `dim_product` 
(product_id, product_name, product_category, product_price)
VALUES
  (1, 'Laptop', 'Electronics', 1000.00),
  (2, 'Smartphone', 'Electronics', 500.00),
  (3, 'Headphones', 'Electronics', 100.00); 
~~~


## Sample Data for Fact Table

~~~sql
INSERT INTO `fact_sales` 
(date_id, customer_id, product_id, quantity_sold, sale_amount)
VALUES
  (1, 1, 1, 2, 2000.00),
  (2, 2, 2, 1, 500.00),
  (3, 3, 3, 3, 300.00); 
~~~



