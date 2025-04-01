# Complete Working Example of an ETL in Python

What This ETL Does

✅ Extracts data from source_table

✅ Transforms:
*    Fills NULL age with 25

* Fills NULL salary with 40000

* Computes tax = salary * 10%

✅ Loads data into destination_table



	Provide a complete working example of an ETL 
	in python, which reads mysql table (include 
	sample records), does some useful transformations 
	and then loads into another mysql table.

	Here’s a complete working ETL (Extract, Transform, Load) 
	pipeline in Python using MySQL. The example covers:

    	1.    Extract: Reads data from a MySQL table (source_table).
    
    	2.    Transform: Cleans data and performs some transformations.
    
    	3.    Load: Inserts transformed data into another MySQL table 
                (destination_table).

You’ll need:
    •    mysql-connector-python (pip install mysql-connector-python)
    •    A running MySQL server

------


# 1. MySQL Setup

	Before running the script, create the 
	source and destination tables in MySQL:

~~~sql
CREATE DATABASE homeworks;
USE homeworks;

CREATE DATABASE homeworks;
USE homeworks;

CREATE TABLE source_table (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    age INT,
    salary INT
);

INSERT INTO source_table (name, age, salary) 
VALUES 
('Alice', 30, 50000),
('Charlie', 35, 70000),
('Bob', NULL, 60000),
('Jason', NULL, 70000),
('David', 28, NULL),
('Rafa', 38, NULL);


CREATE TABLE destination_table (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(50),
    age INT,
    salary INT,
    tax INT
);
~~~



# 2. Python ETL Script


~~~python

import mysql.connector

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "your_username",
    "password": "your_password",
    "database": "etl_demo"
}

# ETL Functions
def extract_data():
    """Extract data from source_table in MySQL."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM source_table")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records

def transform_data(records):
    """Perform transformations: 
    - Handle NULL values by replacing them with defaults.
    - Calculate a new tax field (10% of salary).
    """
    transformed = []
    for record in records:
        name = record["name"]
        age = record["age"] if record["age"] is not None else 25  # Default age = 25
        salary = record["salary"] if record["salary"] is not None else 40000  # Default salary = 40K
        tax = round(salary * 0.10, 2)  # 10% tax on salary
        
        transformed.append((name, age, salary, tax))
    
    return transformed

def load_data(transformed_records):
    """Load transformed data into destination_table."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    query = "INSERT INTO destination_table (full_name, age, salary, tax) VALUES (%s, %s, %s, %s)"
    
    cursor.executemany(query, transformed_records)
    conn.commit()
    
    print(f"{cursor.rowcount} records inserted successfully into destination_table.")
    
    cursor.close()
    conn.close()

#-----------------------
# ETL Pipeline Execution
#-----------------------

# 1    
extracted_data = extract_data()

# 2
transformed_data = transform_data(extracted_data)
    
    
# 3. 
load_data(transformed_data)

~~~

-----

# 3. Running the ETL

Run the script:

~~~sh
python3 etl.py db_config_source.json db_config_target.json
~~~

# 4. Expected Output in destination_table

~~~
mysql> select * from destination_table;
+----+-----------+------+--------+------+
| id | full_name | age  | salary | tax  |
+----+-----------+------+--------+------+
|  1 | Alice     |   30 |  50000 | 5000 |
|  2 | Charlie   |   35 |  70000 | 7000 |
|  3 | Bob       |   25 |  60000 | 6000 |
|  4 | Jason     |   25 |  70000 | 7000 |
|  5 | David     |   28 |  40000 | 4000 |
|  6 | Rafa      |   38 |  40000 | 4000 |
+----+-----------+------+--------+------+
6 rows in set (0.00 sec)
~~~





