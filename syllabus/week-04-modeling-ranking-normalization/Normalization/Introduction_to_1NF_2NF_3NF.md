# Database Normalization

	✅ Database normalization is a process 
	   of organizing data within a relational 
	   database to 
	   
			1. reduce data redundancy 
			
			and 
		
			2. improve data integrity. 
	
	✅  It involves breaking down large tables 
	    into smaller, more manageable tables 
	    while maintaining data relationships. 
	
	✅  This process helps minimize data anomalies, 
	    making it easier to manage and maintain the 
	    database. 

------

# Some Definitions about CK, PK, FK

* CK = Candidate Key
* PK = Primary Key
* FK = Foreign Key

## Primary Key (PK)

A **primary key** (PK) is a column <br>
(or set of columns) in a table that <br>
**uniquely identifies each row** in <br> 
that table.

**Characteristics:**

- Must contain unique values
- Cannot contain NULL values
- A table can have only one primary key

**Example:**

```sql
-- --------------------------------------
-- Here,  customer_id  is the primary key 
-- that uniquely identifies each customer.
-- --------------------------------------
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100)
);
```



## Foreign Key (FK)

A **foreign key** (FK) is a column (or set of columns)  <br>
in one table that references the primary key in another <br>
table, establishing a relationship (link) between the   <br>
two tables.

**Characteristics:**

- Ensures referential integrity
- Can contain duplicate values (unless constrained otherwise)
- Can contain NULL values (unless constrained otherwise)

**Example:**

```sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    order_date DATE,
    customer_id INT,
    
    FOREIGN KEY (customer_id) 
    REFERENCES customers(customer_id)
);
```

Here, `customer_id ` in the `orders` table is a foreign key (FK) that references the `customer_id ` primary key (PK) in the `customers` table, linking each order to a specific customer.

## Combined Example of PK and FK

```sql
-- Parent table with PK
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL
);

-- Child table with FK
CREATE TABLE Employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50) NOT NULL,
    dept_id INT,
    
    FOREIGN KEY (dept_id) 
    REFERENCES departments(dept_id)
);
```

In this example:

- `dept_id ` is the primary key (PK) in `departments` table
- `dept_id ` in `employees` table is a foreign key (FK) 
  referencing `departments` table
- This establishes a relationship/link where each employee belongs to a department

## Candidate Key (CK)
A **candidate key** (CK) in a database is a set of one or 
more columns (attributes) that can uniquely identify a record 
in a table. A table may have multiple candidate keys, but each 
of them must satisfy two conditions:

1. **Uniqueness**: No two rows in the table can have the same value(s) in the candidate key column(s).

2. **Minimality**: It cannot include any extra column(s) that are not necessary for uniqueness.

A **primary key (PK)**, on the other hand, is a **specific candidate key**
chosen by the database designer to uniquely identify rows in the table. 
It has a few additional constraints:

- **Only one primary key** can exist per table.
- A primary key cannot contain `NULL` values (it must be non-nullable).
- Primary keys are often used to create relationships between tables, like in foreign key references.

In summary:

- **Candidate Key**: A potential key that could uniquely identify rows (can have multiple per table).
- **Primary Key**: The chosen candidate key that uniquely identifies rows and is subject to stricter rules (one per table).

## Example:
Here's an example of a table called **students** 
that has multiple candidate keys, with one designated 
as the primary key:

| **student_id** | **email**           | **SSN**         | **Name**       | **DOB**        |
|---------------|---------------------|-----------------|----------------|----------------|
| 1001          | alice@email.com     | 123-45-6789     | Alice Johnson  | 1995-01-12     |
| 1002          | bob@email.com       | 987-65-4321     | Bob Smith      | 1997-03-22     |

### Explanation:
- **Candidate Keys:** 
  - `student_id`: Uniquely identifies each student.
  - `email`: Every student's email address is unique.
  - `SSN`: Social Security Numbers are unique to each individual.
  
  All these columns satisfy the **uniqueness** and **minimality** criteria of candidate keys.

- **Primary Key (PK):**
  - If we choose `student_id` as the primary key, it becomes the designated unique identifier for the table. This means `student_id` will also be non-nullable and used for relationships with other tables.

In this example, `email` and `SSN` remain as alternate candidate keys. 


--------

![](./images/types_of_normal_forms.webp)

# Normal Forms Definitions

| Normal Forms | Description of Normal Forms |
|--------------|-----------------------------|
| First Normal Form (1NF)        | A relation is in first normal form if every attribute in that relation is single-valued attribute.       |
| Second Normal Form (2NF)        | A relation that is in First Normal Form and every non-primary-key attribute is fully functionally dependent on the primary key, then the relation is in Second Normal Form (2NF).       |
| Third Normal Form (3NF)        | Third Normal Form (3NF) in database normalization means a table is in 2NF and all non-key attributes are directly (not transitively) dependent on the candidate key(s). This eliminates transitive dependencies, where a non-key attribute depends on another non-key attribute instead of the key.        |



# Introduction

		📊 Database  normalization  is  the  process 
		of  organizing  data  in a  database  by 
		structuring it into tables and establishing 
		relationships between them, with the goal of 
		
		  ✅ 1. Minimizing data redundancy, 
		
		  ✅ 2. Preventing data inconsistencies, and 
		
		  ✅ 3. Improving data integrity by eliminating 
		   unnecessary repetition across multiple tables

-----

# 1. What is a Database Normalization

	Database normalization is the process 
	of organizing  data in a database to 
	
		1. Eliminate  redundancy, 
		2. Improve  data integrity, and 
		3. Make the database more flexible: 

### 1.1 Eliminate redundancy: 
		Redundant data wastes disk space 
		and creates maintenance problems. 

### 1.2. Improve data integrity: 
		Normalized relations mirror real-world 
		concepts and their interrelationships. 

### 1.3. Make the database more flexible: 
		A fully normalized database can be 
		extended to accommodate  new  types 
		of data without changing existing 
		structure too much. 

### 1.4. Benefits of database normalization: 
		1. Simplifies the query process 
		2. Improves workflow 
		3. Increases security 
		4. Lessens costs

### 1.5. Normalization is commonly used when dealing 
		with large datasets. It involves breaking 
		down a large, complex  table into  smaller 
		and  simpler tables while  maintaining data 
		relationships. 
		
		
# 2. Problems with the Non-Normalized Table

The following table is a Non-Normalized Table:

| Student_ID | Name       | Courses                 |
|------------|------------|-------------------------|
| 1          | John Doe   | Math, Science, History  |
| 2          | Jane Smith | English, Art            |


The following table is in 1NF:

| Student_ID | first_Name | last_name | Course  |
|------------|------------|-----------|---------|
| 1          | John       |  Doe      | Math    |             | 1          | John       |  Doe      | Science |  
| 1          | John       |  Doe      | History | 
| 2          | Jane       |  Smith    | English |
| 2          | Jane       |  Smith    | Art     | 

Problem-1. **you can not ADD a new course without a student** 

Problem-2. **you can not ADD a new student without a course** 

Problem-3. **If you want to ADD a new course for a student,** 

then 

	* 1.1 read the record
	* 1.2 update the courses field
	* 1.3 update the database

Problem-4. **If you want to DROP an existing course for a student,**

then 

	* 2.1 read the record
	* 2.2 update the courses field (drop the course)
	* 2.3 update the database
	
Problem 5. **If you want to change the last name of a student**

then 

	* 3.1 read the record
	* 3.2 update the Name field
	* 3.3 update the database
	
### → Eliminate Problems by a Normalized Table(s):

NOTE: the `Name` column is not atomic: converted to 
two atomic columns:  `First_Name` and `Last_Name`.

**Students:**

| Student_ID | First_Name | Last_Name  |
|------------|------------|------------|
| 1          | John       | Doe        |
| 2          | Jane       | Smith      |

**Courses:**

| Course_ID  | Course_Name|
|------------|------------|
| 100        | Math       |
| 101        | Science    |
| 102        | History    |
| 103        | English    |
| 104        | Art        |

**Students_Courses:**

| Student_ID | Courses_ID |
|------------|------------|
| 1          | 100        | 
| 1          | 101        | 
| 1          | 102        |
| 2          | 103        | 
| 2          | 104        |

------


# 3. Normal Forms in DBMS

![](./images/normal_forms.png)


	1️⃣ Normalization is the process of 
	    minimizing  redundancy  from a 
	    relation or set of relations. 
	
	2️⃣ Redundancy  in  relation  may  
	    cause insertion, deletion, and 
	    update anomalies.  So, it helps 
	    to minimize the redundancy 
	    in relations. 
	
	3️⃣ Normal forms are used to eliminate 
	    or reduce redundancy in database 
	    tables.

## 3.1 Anomalies

**a·nom·a·ly** → something that deviates from what is standard, normal, or expected.

### 1. [Insertion Anomaly](./anomaly_insertion.md)

### 2. [Update Anomaly](./anomaly_update.md)

### 3. [Deletion Anomaly](./anomaly_delete.md)


-----


## 3.2 Normalization of DBMS:
	
	In database management systems (DBMS), normal 
	forms are a series of guidelines that help to 
	ensure that  the  design of  a  database  is 
	efficient, organized,  and  free  from  data 
	anomalies.   There  are  several levels  of 
	normalization, each  with  its  own set  of 
	guidelines, known as normal forms.
	
![](images/image_normalization_levels.png)



## 3.3 Normal Forms in DBMS:
	
### First Normal Form (1NF): 
	
		This is the most basic level of normalization. 
		In 1NF, each table cell should contain only a 
		single value,  and each  column  should  have 
		a unique name. The first normal form helps to 
		eliminate duplicate data and simplify queries.
		
### Second Normal Form (2NF): 
	
		2NF eliminates redundant data by requiring 
		that each non-key attribute be dependent on 
		the primary key. This means that each column 
		should be directly related to the primary key, 
		and not to other columns.
		
### Third Normal Form (3NF): 
	
		3NF  builds on 2NF by requiring  that  all 
		non-key attributes are independent of each 
		other. This means that each column should 
		be  directly related  to the  primary key, 
		and not to any other columns in the same 
		table.
		
### Boyce-Codd Normal Form (BCNF): 
	
		BCNF is a stricter form of 3NF that ensures 
		that each determinant in a table is a candidate 
		key. In other words, BCNF ensures  that  each 
		non-key attribute is dependent only on the 
		candidate key.

------

# 4. Dependency & Partial Dependency

### What is a Dependency?

* In database normalization, a **dependency** refers to  <br>
a relationship between attributes (columns) in a table.  <br>
<br>
* Specifically, it describes how one attribute determines <br>
the value of another attribute. The most common type of   <br>
dependency is a **functional dependency**, where the value <br> 
of one attribute (or set of attributes) uniquely determines <br>
the value of another attribute.

#### Notation:
- If attribute **X** determines attribute **Y**, 
we write it as **X → Y**.

- Example: In a table of "employees," the `employee_id` 
  determines the `employee_name`.
-  If you know the `employee_id` , you can find the exact `employee_name`.
-  `employee_id` → `employee_name`

---

### What is a Partial Dependency?

* A **partial dependency** occurs when a non-prime 
attribute (an attribute that is not part of the 
primary key) depends on only a part of a composite 
primary key, rather than the entire primary key. 

* Partial dependencies are problematic in database 
design because they violate the rules of **Second 
Normal Form (2NF)**.

#### Example of Partial Dependency:
- Suppose a table has a composite primary key **(A, B)**.

- If a non-prime attribute **C** depends only on
  **A** (i.e., **A → C**), this is a partial dependency.

- If a non-prime attribute **D** depends only on 
  **B** (i.e., **B → D**), this is a partial dependency.

---

### Examples of Dependencies:

#### Example 1: Functional Dependency

**Table: Employees**

| Employee_ID | Employee_Name | Department_ID |
|-------------|---------------|---------------|
| 101         | Alice         | D01           |
| 102         | Bob           | D02           |

- **Dependency:** `Employee_ID → Employee_Name`
  - The `Employee_ID` uniquely determines the `Employee_Name`.

#### Example 2: Functional Dependency

**Table: Orders**

| Order_ID | Product_ID | Quantity |
|----------|------------|----------|
| 1001     | P101       | 2        |
| 1002     | P102       | 1        |

- **Dependency:** 
	- `Order_ID, Product_ID → Quantity`
	-  The combination of `Order_ID` and `Product_ID` uniquely determines the `Quantity`.


#### Example 3: Functional Dependency

**Table: Students**

| Student_ID | Course_ID | Grade |
|------------|-----------|-------|
| 1          | C101      | A     |
| 2          | C102      | B     |

- **Dependency:** `Student_ID, Course_ID → Grade`
  - The combination of `Student_ID` and `Course_ID` 
    uniquely determines the `Grade`.

---

### Examples of Partial Dependencies:

#### Example 1: Partial Dependency
**Table: Orders**

| Order_ID | Product_ID | Product_Name | Quantity |
|----------|------------|--------------|----------|
| 1001     | P101       | Laptop       | 2        |
| 1002     | P102       | Phone        | 1        |

- **Composite Primary Key:** `(Order_ID, Product_ID)`
- **Partial Dependency:** `Product_ID → Product_Name`
  - The `Product_Name` depends only on `Product_ID`, 
    which is part of the composite primary key.

#### Example 2: Partial Dependency
**Table: Enrollments**

| Student_ID | Course_ID | Course_Name | Enrollment_Date |
|------------|-----------|-------------|-----------------|
| 1          | C101      | Math        | 2023-01-01      |
| 2          | C102      | Science     | 2023-02-01      |

- **Composite Primary Key:** `(Student_ID, Course_ID)`
- **Partial Dependency:** `Course_ID → Course_Name`
  - The `Course_Name` depends only on `Course_ID`, which 
    is part of the composite primary key.

#### Example 3: Partial Dependency
**Table: Sales**

| Salesperson_ID | Region_ID | Region_Name | Sales_Amount |
|----------------|-----------|-------------|--------------|
| 101            | R01       | North       | 5000         |
| 102            | R02       | South       | 3000         |

- **Composite Primary Key:** `(Salesperson_ID, Region_ID)`
- **Partial Dependency:** `Region_ID → Region_Name`
  - The `Region_Name` depends only on `Region_ID`, which 
    is part of the composite primary key.

---

### Key Differences:
- **Dependency:** A general relationship where one 
  attribute determines another.
- **Partial Dependency:** A specific type of dependency 
  where a non-prime attribute depends on only part of 
  a composite primary key.

By resolving partial dependencies, you can achieve 
**Second Normal Form (2NF)** and improve the structure 
of your database.

------

# First Normal Form: 1NF

### What is First Normal Form (1NF)?

* First Normal Form (1NF) is the most basic level 
  of database normalization. 
* A table is in 1NF if it satisfies the following 
  conditions:

1. **Atomic Values**: Each column (attribute) contains 
   only atomic (indivisible) values. This means no repeating 
   groups or arrays are allowed in a single cell.
2. **Unique Column Names**: Each column has a unique name, 
   and the order of columns does not matter.
3. **Unique Rows**: Each row in the table must be unique. 
   This is typically ensured by having a primary key.
4. **Order Independence**: The order of rows and columns 
   does not affect the data's meaning.

		In simpler terms:
				1NF ensures that the table is "flat" 
				and does not contain any nested or 
				repeating structures.
		 
		 First Normal Form (1NF):
				A table is in 1NF if each cell contains 
				only a single value.  In  other  words, 
				there are no repeating groups or arrays 
				within a single row.



---

### Examples of Converting a Table into 1NF

#### Example 1: Repeating Groups in a Single Column

**Original Table (Not in 1NF):**

| Student_ID | Name       | Courses                 |
|------------|------------|-------------------------|
| 1          | John Doe   | Math, Science, History  |
| 2          | Jane Smith | English, Art            |

**Problem**: The "Courses" column contains multiple values separated by commas, violating the atomicity rule.

**Converted Table (1NF):**

* NOTE: the `Name` column is not atomic: converted to 
  two atomic columns:  `First_Name` and `Last_Name`.
* Every attribute is atomic
* No duplicate rows
* No duplicate column names


| Student_ID | First_Name | Last_Name| Course   |
|------------|------------|----------|----------|
| 1          | John       | Doe      | Math     |
| 1          | John       | Doe      | Science  |
| 1          | John       | Doe      | History  |
| 2          | Jane       | Smith    | English  |
| 2          | Jane       | Smith    | Art      |



**Explanation**: Each course is now in a separate row, 
ensuring atomicity.

---

#### Example 2: Multiple Columns for Repeating Data

**Original Table (Not in 1NF):**

| Employee_ID | Last_Name  | Skill_1 | Skill_2 | Skill_3 |
|-------------|------------|---------|---------|---------|
| 101         | Brown      | Python  | Java    | SQL     |
| 102         | Green      | C++     | NULL    | NULL    |
| 103         | Smith      | Java    | NULL    | SQL     |

**Problem**: The table uses multiple columns to store similar 
data (skills), which is not scalable and violates 1NF.

**Converted Table (1NF):**

| Employee_ID | last_Name   | Skill  |
|-------------|-------------|--------|
| 101         | Brown       | Python |
| 101         | Brown       | Java   |
| 101         | Brown       | SQL    |
| 102         | Green       | C++    |
| 103         | Smith       | Java   |
| 103         | Smith       | SQL    |

**Explanation**: Each skill is now in a separate row, 
eliminating the need for multiple columns.

---

#### Example 3: Nested Data in a Single Column

**Original Table (Not in 1NF):**

| Order_ID | Customer_Name | Products_Ordered                     |
|----------|---------------|--------------------------------------|
| 1001     | John Smith    | {Product: Laptop, Quantity: 1}, {Product: Mouse, Quantity: 2} |
| 1002     | Mary Johnson  | {Product: Keyboard, Quantity: 1}     |

**Problem**: The "Products_Ordered" column contains nested data (a list of products with quantities), which violates atomicity.

**Converted Table (1NF):**

NOTE: the `Customer_Name` column is not atomic: converted 
to two atomic columns:  `First_Name` and `Last_Name`.

| Order_ID | First_Name | Last_Name|Product   | Quantity |
|----------|------------|----------|----------|----------|
| 1001     | John       | Smith    | Laptop   | 1        |
| 1001     | John       | Smith    | Mouse    | 2        |
| 1002     | Mary       | Johnson  | Keyboard | 1        |

**Explanation**: Each product and its quantity are now in 
separate rows, ensuring atomicity.

---

### **First Normal Form (1NF)**
A table is in **First Normal Form (1NF)** if:  
1. All columns contain **atomic (indivisible) values**.  
2. There are **no repeating groups or arrays**.  
3. Each column contains values of **a single type**.  

---

### **Example 4: Breaking Multi-Valued Columns into Rows**
#### **Unnormalized Table (UNF)**
| student_id | student_name| subjects       |
|------------|-------------|----------------|
| 1          | Alice       | Math, Science  |
| 2          | Bob         | English, Math  |
| 3          | Charlie     | History        |

- The **"subjects"** column contains multiple values, violating 1NF.

#### **Converted to 1NF**
| student_id | student_name | subject  |
|------------|-------------|---------|
| 1          | Alice       | Math    |
| 1          | Alice       | Science |
| 2          | Bob         | English |
| 2          | Bob         | Math    |
| 3          | Charlie     | History |

✅ Now, all values are **atomic**, and there are **no multi-valued attributes**.

---

### **Example 5: Removing Repeating Groups**
#### **Unnormalized Table (UNF)**
| order_id | customer_name | product_1  | product_2  | product_3  |
|----------|--------------|------------|------------|------------|
| 101      | John Doe     | Laptop     | Mouse      | Keyboard   |
| 102      | Jane Smith   | Tablet     | Charger    | NULL       |

- The **product columns** are repeating groups, violating 1NF.

#### **Converted to 1NF**

NOTE: the `customer_name` column is not atomic: converted to 
two atomic columns:  `first_fame` and `last_name`.


| order_id | first_name   | last_name | product   |
|----------|--------------|-----------|-----------|
| 101      | John         | Doe       | Laptop    |
| 101      | John         | Doe       | Mouse     |
| 101      | John         | Doe       | Keyboard  |
| 102      | Jane         | Smith     | Tablet    |
| 102      | Jane         | Smith     | Charger   |

✅ Now, there are **no repeating groups**, and each column holds **atomic values**.

These transformations help normalize data for better consistency and query efficiency. 


### **Example 6: Repeating Groups Across Columns**

**Original Table (Not in 1NF):**

| Order_ID | Customer_Name | Product_1 | Quantity_1 | Product_2 | Quantity_2 |
|----------|---------------|-----------|------------|-----------|------------|
| 1001     | Alice Brown   | Laptop    | 1          | Mouse     | 2          |
| 1002     | Bob Green     | Monitor   | 1          | Keyboard  | 1          |
| 1003     | Rafa Smith    | PC        | 5          | NULL      | NULL       |

**Problem:** The table has repeating groups of columns 
(`Product_1`, `Quantity_1`), and (`Product_2`, `Quantity_2`), 
which violates 1NF.

**Converted Table (1NF):**

NOTE: the `Customer_Name` column is not atomic: converted to 
two atomic columns:  `First_Name` and `Last_Name`.

| Order_ID | First_Name | Last_Name | Product  | Quantity |
|----------|------------|-----------|----------|----------|
| 1001     | Alice      |Brown      | Laptop   | 1        |
| 1001     | Alice      |Brown      | Mouse    | 2        |
| 1002     | Bob        |Green      | Monitor  | 1        |
| 1002     | Bob        |Green      | Keyboard | 1        |
| 1003     | Rafa       |Smith      | PC       | 5        |

**Explanation:** The repeating groups are eliminated 
by creating separate rows for each product and its 
corresponding quantity.

### **Example 7:

#### Before 1NF (Violates 1NF):

| CustomerID | Name   | Phone Numbers   |
| :--------- | :----- | :-------------- |
| 1          | Alice  | 123-456-7890, 987-654-3210 |
| 2          | Bob    | 555-123-4567    |

#### After 1NF:

| CustomerID | Name  | Phone Number   |
| :--------- | :---- | :------------- |
| 1          | Alice | 123-456-7890   |
| 1          | Alice | 987-654-3210   |
| 2          | Bob   | 555-123-4567   |

### **Example 8:

#### Before 1NF (Violates 1NF):

| OrderID | Product1 | Quantity1 | Product2 | Quantity2 |
| :------ | :------- | :-------- | :------- | :-------- |
| 101     | Laptop   | 1         | Mouse    | 2         |
| 102     | Laptop   | 4         | NULL     | NULL      |

#### After 1NF:

| OrderID | Product  | Quantity |
| :------ | :------- | :------- |
| 101     | Laptop   | 1        |
| 101     | Mouse    | 2        |
| 102     | Laptop   | 4        |


### **Example 9: A Table Already in 1NF:

| Employee_ID | Name    | Department |
| :---------- | :------ | :--------- |
| 10          | Charlie | Sales      |
| 20          | Diana   | Marketing  |
| 30          | Eve     | Sales      |

### Summary

* 1NF ensures that a table is structured in a way that 
  each cell contains a single, indivisible value, and 
  there are no repeating groups or nested structures. 
  
* By converting tables into 1NF, you create a solid 
  foundation for further normalization and efficient 
  database design.

-------

# Second Normal Form: 2NF

### What is Second Normal Form (2NF)?

The **Second Normal Form (2NF)** is a level of database 
normalization that builds on the **First Normal Form (1NF)**. 

✅ A table is in 2NF if:

1. It is in **1NF** (all attributes are atomic, 
   and each row is unique).
2. It has **no partial dependency**, meaning no 
   non-prime attribute (an attribute that is not 
   part of any candidate key) is dependent on a 
   proper subset of any candidate key.
   
✅ A table is in 2NF if it meets the following two conditions:

	1. It is in 1NF.

	2. All non-key attributes are fully 
	   functionally dependent on the entire 
	   primary key. This means that every attribute 
	   that is not part of the primary key must 
	   depend on all parts of the primary key (if 
	   the primary key is composite, meaning it has 
	   more than one attribute).

✅ In simpler terms, 2NF ensures that every non-key 
attribute in a table is fully functionally dependent 
on the **entire primary key**, not just part of it. 
This is particularly relevant for tables with composite 
primary keys (primary keys made up of multiple columns).

---

### Steps to Achieve 2NF

1. **Ensure the table is in 1NF**: The table must 
   already satisfy the rules of 1NF.
2. **Identify the primary key**: Determine the 
   primary key (or composite key) of the table.
3. **Check for partial dependencies**: If any 
   non-key attribute depends on only part of 
   the primary key, it violates 2NF.
4. **Decompose the table**: Split the table into 
   smaller tables to eliminate partial dependencies.

---

### Examples of Conversion to 2NF

#### Example 1: Student Course Enrollment

**Original Table (Not in 2NF):**

| **Student_ID** | **Course_ID** | **Student_Name** | **Course_Name** | **Grade** |
|----------------|---------------|------------------|-----------------|-----------|
| 1              | 101           | John             | Math            | A         |
| 2              | 101           | Alice            | Math            | B         |
| 1              | 102           | John             | Science         | C         |

**Problem**: 

* The table has a composite primary key: `(Student_ID, Course_ID)`. 

* However, `Student_Name` depends only on `Student_ID`, 
  and  `Course_Name` depends only on `Course_ID`. 
  This is a partial dependency.

**Solution**: Decompose the table into three tables:

1. **Students Table**:

   | **Student_ID** | **Student_Name** |
   |----------------|------------------|
   | 1              | John             |
   | 2              | Alice            |

2. **Courses Table**:

   | **Course_ID** | **Course_Name** |
   |---------------|-----------------|
   | 101           | Math            |
   | 102           | Science         |

3. **Enrollments Table**:

   | **Student_ID** | **Course_ID** | **Grade** |
   |----------------|---------------|-----------|
   | 1              | 101           | A         |
   | 2              | 101           | B         |
   | 1              | 102           | C         |

Now, all tables are in 2NF.

---

#### Example 2: Employee Project Assignment

**Original Table (Not in 2NF):**

| **Employee_ID** | **Project_ID** | **Employee_Name** | **Project_Name** | **Hours_Worked** |
|-----------------|----------------|-------------------|------------------|------------------|
| 101             | 1              | Alice             | Project X        | 20               |
| 102             | 1              | Bob               | Project X        | 15               |
| 101             | 2              | Alice             | Project Y        | 10               |

**Problem**: 

* The composite primary key is `(Employee_ID, Project_ID)`. 

* However, `Employee_Name` depends only on `Employee_ID`, and 
  `Project_Name` depends only on `Project_ID`. 
  This is a partial dependency.

**Solution**: Decompose the table into three tables:

1. **Employees Table**:

   | **Employee_ID** | **Employee_Name** |
   |-----------------|-------------------|
   | 101             | Alice             |
   | 102             | Bob               |

2. **Projects Table**:

   | **Project_ID** | **Project_Name** |
   |----------------|------------------|
   | 1              | Project X        |
   | 2              | Project Y        |

3. **Assignments Table**:

   | **Employee_ID** | **Project_ID** | **Hours_Worked** |
   |-----------------|----------------|------------------|
   | 101             | 1              | 20               |
   | 102             | 1              | 15               |
   | 101             | 2              | 10               |

Now, all tables are in 2NF.

---

#### Example 3: Order Details

**Original Table (Not in 2NF):**

| **Order_ID** | **Product_ID** | **Customer_Name** | **Product_Name** | **Quantity** |
|--------------|----------------|-------------------|------------------|--------------|
| 1001         | 1              | John              | Laptop           | 2            |
| 1001         | 2              | John              | Mouse            | 5            |
| 1002         | 1              | Alice             | Laptop           | 1            |

**Problem**: 

* The composite primary key is `(Order_ID, Product_ID)`. 

* However, `Customer_Name` depends only on `Order_ID`, 
  and `Product_Name` depends only on `Product_ID`. 
  This is a partial dependency.

**Solution**: Decompose the table into three tables:

1. **Orders Table**:

   | **Order_ID** | **Customer_Name** |
   |--------------|-------------------|
   | 1001         | John              |
   | 1002         | Alice             |

2. **Products Table**:

   | **Product_ID** | **Product_Name** |
   |----------------|------------------|
   | 1              | Laptop           |
   | 2              | Mouse            |

3. **Order_Details Table**:

   | **Order_ID** | **Product_ID** | **Quantity** |
   |--------------|----------------|--------------|
   | 1001         | 1              | 2            |
   | 1001         | 2              | 5            |
   | 1002         | 1              | 1            |

Now, all tables are in 2NF.


#### Example 4: Examples of 2NF:

✅ Before 2NF (Violates 2NF):

| OrderID | ProductID | ProductName | OrderDate  |
| :------ | :-------- | :---------- | :--------- |
| 1       | P1        | Laptop      | 2025-04-21 |
| 1       | P2        | Mouse       | 2025-04-21 |
| 2       | P1        | Laptop      | 2025-04-20 |

* Primary Key: (OrderID, ProductID)
* ProductName depends only on ProductID, not the entire primary key.

✅ After 2NF (Decomposed into two tables):

Orders Table:

| OrderID | ProductID | OrderDate  |
| :------ | :-------- | :--------- |
| 1       | P1        | 2025-04-21 |
| 1       | P2        | 2025-04-21 |
| 2       | P1        | 2025-04-20 |

Products Table:

| ProductID | ProductName |
| :-------- | :---------- |
| P1        | Laptop      |
| P2        | Mouse       |

#### Example 5: Examples of 2NF:

✅ Another Before 2NF (Violates 2NF):

| EmployeeID | ProjectID | EmployeeName | ProjectName |
| :--------- | :-------- | :----------- | :---------- |
| 101        | A         | Alice        | Alpha       |
| 102        | B         | Bob          | Beta        |
| 101        | B         | Alice        | Beta        |

* Primary Key: (EmployeeID, ProjectID)
* EmployeeName depends only on EmployeeID.
* ProjectName depends only on ProjectID.

✅ Another After 2NF (Decomposed into two tables):

EmployeeProjects Table:

| EmployeeID | ProjectID |
| :--------- | :-------- |
| 101        | A         |
| 102        | B         |
| 101        | B         |

Employees Table:

| EmployeeID | EmployeeName |
| :--------- | :----------- |
| 101        | Alice        |
| 102        | Bob          |

Projects Table:

| ProjectID | ProjectName |
| :-------- | :---------- |
| A         | Alpha       |
| B         | Beta        |

#### Example 6: Examples of 2NF:
✅ A Table Already in 2NF (assuming a single-attribute primary key):

| CustomerID | Name    | City     |
| :--------- | :------ | :------- |
| 1          | Charlie | New York |
| 2          | Diana   | London   |


---

### Summary

- **2NF** eliminates partial dependencies by 
  ensuring that non-key attributes depend on 
  the **entire primary key**.
- To achieve 2NF, decompose tables with composite  
  keys into smaller tables, separating attributes 
  that depend on only part of the key.
- The examples above demonstrate how to identify 
  and resolve partial dependencies to achieve 2NF.


### **Second Normal Form (2NF)**
A table is in **Second Normal Form (2NF)** if:  
1. **It is in 1NF** (First Normal Form).  
2. **There are no partial dependencies**, meaning:  
   - Every **non-key column** must be **fully dependent** 
     on the **entire** primary key, not just a part of it.  

---

### **Example 7: Eliminating Partial Dependency in a Composite Key Table**
#### **1NF Table (Violating 2NF)**
| order_id | product_id| product_name | customer_id| customer_name|
|----------|-----------|--------------|------------|--------------|
| 101      | P1        | Laptop       | C1         | Alice        |
| 101      | P2        | Mouse        | C1         | Alice        |
| 102      | P3        | Keyboard     | C2         | Bob          |

**Issue:**  
- The **primary key** is **(`order_id`, `product_id`)** (composite key).  
- **`product_name`** depends **only** on **`product_id`**, not on the full key.  
- **`customer_name`** depends **only** on **`customer_id`**, not on the full key.  

#### **Converted to 2NF**
**Orders Table (Now in 2NF)**

| order_id | customer_id |
|----------|------------|
| 101      | C1         |
| 102      | C2         |

**Customers Table**

| customer_id | customer_name |
|------------|--------------|
| C1         | Alice        |
| C2         | Bob          |

**Products Table**

| product_id | product_name |
|-----------|--------------|
| P1        | Laptop       |
| P2        | Mouse        |
| P3        | Keyboard     |

**Order Details Table (Bridging Orders and Products)**

| order_id | product_id |
|----------|-----------|
| 101      | P1        |
| 101      | P2        |
| 102      | P3        |

✅ Now, **all non-key attributes fully depend on the primary key**, 
eliminating partial dependencies.

---

### **Example 8: Removing Partial Dependency in a Student Enrollment Table**
#### **1NF Table (Violating 2NF)**

| student_id | course_id | course_name  | student_name|
|------------|-----------|--------------|-------------|
| S1         | C101      | Math         | Alice       |
| S2         | C102      | Science      | Bob         |
| S1         | C102      | Science      | Alice       |

**Issue:**  
- The **primary key** is **(`student_id`, `course_id`)** (composite key).  
- **`course_name`** depends **only** on **`course_id`**, not on the full key.  
- **`student_name`** depends **only** on **`student_id`**, not on the full key.  

#### **Converted to 2NF**
**Students Table**

| student_id | student_name|
|------------|-------------|
| S1         | Alice       |
| S2         | Bob         |

**Courses Table**

| course_id | course_name|
|----------|-------------|
| C101     | Math        |
| C102     | Science     |

**Enrollments Table (Bridging Students and Courses)**

| student_id | course_id|
|------------|----------|
| S1         | C101     |
| S2         | C102     |
| S1         | C102     |

✅ Now, **all non-key attributes fully depend on the primary key**, 
making the table **2NF compliant**.

---

### **Summary**
To convert to **2NF**, we:
- Identified **partial dependencies**.
- Split **data into separate tables** to ensure all 
  columns depend **only on the full primary key**.


## 2NF Summarized

### **What is 2NF (Second Normal Form)?**
Second Normal Form (2NF) is a level of database normalization aimed at eliminating **partial dependencies**. A table is in 2NF if:

1. It is already in **First Normal Form (1NF)**—meaning all columns contain atomic (indivisible) values, and there are no repeating groups.

2. **Every non-prime attribute** (attributes not part of the primary key) is fully functionally dependent on the **entire primary key** (not just part of it, in the case of composite keys).

### **Examples of Converting a Table to 2NF**
#### **Example 1: Student Enrollment**

*Initial Table:*  

| **Student_ID** | **Course_ID** | **Student_Name** | **Course_Name** | **Instructor** |  
|------------------|------------------|------------------|------------------|------------------|  
| 1               | 101            | Alice            | Math 101        | Prof. Smith     |  
| 2               | 102            | Bob              | Physics 102     | Prof. Johnson   |  

Here, the composite key is `Student_ID + Course_ID`. However:

- `Student_Name` depends only on `Student_ID`, not the full composite key.

- `Course_Name` and `Instructor` depend only on `Course_ID`.

### To Convert to 2NF:

We separate the data into two tables to remove partial dependencies:

1. **Students Table:**  

| Student_ID | Student_Name |  
|------------------|------------------|  
| 1               | Alice            |  
| 2               | Bob              |  

2. **Courses Table:** 
 
| Course_ID | Course_Name | Instructor |  
|------------------|------------------|------------------|  
| 101            | Math 101        | Prof. Smith     |  
| 102            | Physics 102     | Prof. Johnson   |  

3. **Enrollment Table:** 
 
| Student_ID | Course_ID|  
|------------------|------------------|  
| 1               | 101            |  
| 2               | 102            |  

---

#### **Example 2: Sales Records**

*Initial Table:*  

| **Order_ID** | **Product_ID** | **Order_Date** | **Product_Name** | **Price** |  
|--------------|----------------|----------------|------------------|-----------|  
| 5001         | P100           | 2025-04-01     | Widget A         | 20.00     |  
| 5002         | P101           | 2025-04-02     | Widget B         | 30.00     |  

Here, the composite key is `Order_ID` + `Product_ID`, but:

- `Order_Date` depends only on `Order_ID`.

- `Product_Name` and `Price` depend only on `Product_ID`.

### To Convert to 2NF:

We separate the data into multiple tables:

1. **Orders Table:**  

| **Order_ID** | **Order_Date** |  
|--------------|----------------|  
| 5001         | 2025-04-01     |  
| 5002         | 2025-04-02     |  


2. **Products Table:**  

| **Product_ID** | **Product_Name** | **Price** |  
|----------------|------------------|-----------|  
| P100           | Widget A         | 20.00     |  
| P101           | Widget B         | 30.00     |  


3. **Order Details Table:**  

| **Order_ID** | **Product_ID** |  
|--------------|----------------|  
| 5001         | P100           |  
| 5002         | P101           |  

These steps ensure all non-prime attributes are fully dependent on the whole primary key, making the tables compliant with 2NF.



------

# Third Normal Form: 3NF

### What is Third Normal Form (3NF)?

Third Normal Form (3NF) is a level of database 
normalization used to reduce redundancy and improve 
data integrity in relational databases. 

✅ A table is in 3NF if it satisfies the following conditions:

1. **It is in Second Normal Form (2NF):**
   - The table must already be in 2NF, meaning it 
     should have no partial dependencies (every 
     non-prime attribute must be fully functionally 
     dependent on the primary key).

2. **No Transitive Dependencies:**
   - There should be no transitive dependencies, 
     meaning no non-prime attribute should depend 
     on another non-prime attribute. All non-prime 
     attributes must depend only on the primary key.

In simpler terms, 3NF ensures that each column in a 
table is directly related to the primary key and not 
to other columns.


![](./images/transitive_dependency.png)


✅ Third Normal Form (3NF)

		A table is in 3NF if it meets the 
		following two conditions:

			1. It is in 2NF.

			2. No non-key attribute is transitively dependent 
			   on the primary key. This means that non-key attributes 
			   should not depend on other non-key attributes.
			   They should only depend directly on the primary key. 
---

### Steps to Convert a Table into 3NF:

1. Ensure the table is in 2NF.
2. Identify and remove transitive dependencies 
   by creating separate tables for attributes 
   that depend on other non-prime attributes.

---

### Examples of Conversion to 3NF:

#### Example 1: Student Table

**Original Table (Not in 3NF):**

| Student_ID | Student_Name | Course_ID | Course_Name | Instructor_Name |
|------------|--------------|-----------|-------------|-----------------|
| 1          | John         | C101      | Math        | Dr. Smith       |
| 2          | Jane         | C102      | Science     | Dr. Brown       |
| 3          | John         | C103      | History     | Dr. Lee         |

**Problem:**
- `Course_Name` and `Instructor_Name` depend on `Course_ID`, 
  not directly on `Student_ID` (transitive dependency).

**Solution:**
- Split the table into two tables: `Students` and `Courses`.

**Tables in 3NF:**

1. **Students:**

   | Student_ID | Student_Name | Course_ID |
   |------------|--------------|-----------|
   | 1          | John         | C101      |
   | 2          | Jane         | C102      |
   | 3          | John         | C103      |

2. **Courses:**

   | Course_ID | Course_Name | Instructor_Name |
   |-----------|-------------|-----------------|
   | C101      | Math        | Dr. Smith       |
   | C102      | Science     | Dr. Brown       |
   | C103      | History     | Dr. Lee         |

---

#### Example 2: Employee Table

**Original Table (Not in 3NF):**

| Employee_ID | Employee_Name | Department_ID | Department_Name | Manager_ID |
|-------------|---------------|---------------|-----------------|------------|
| 101         | Alice         | D01           | HR              | 201        |
| 102         | Bob           | D02           | IT              | 202        |
| 103         | Charlie       | D01           | HR              | 201        |

**Problem:**
- `Department_Name` depends on `Department_ID`, 
  not directly on `Employee_ID` (transitive dependency).

**Solution:**
- Split the table into two tables: `Employees` and `Departments`.

**Tables in 3NF:**

1. **Employees:**

   | Employee_ID | Employee_Name | Department_ID | Manager_ID |
   |-------------|---------------|---------------|------------|
   | 101         | Alice         | D01           | 201        |
   | 102         | Bob           | D02           | 202        |
   | 103         | Charlie       | D01           | 201        |

2. **Departments:**

   | Department_ID | Department_Name |
   |---------------|-----------------|
   | D01           | HR              |
   | D02           | IT              |

---

### Example 3: Order Table

**Original Table (Not in 3NF):**

| Order_ID | Customer_ID | Customer_Name | Product_ID | Product_Name | Quantity |
|----------|-------------|---------------|------------|--------------|----------|
| 1001     | C001        | John          | P101       | Laptop       | 1        |
| 1002     | C002        | Jane          | P102       | Phone        | 2        |
| 1003     | C001        | John          | P103       | Tablet       | 1        |

**Problem:**

- `Customer_Name` depends on `Customer_ID`, and 
- `Product_Name` depends on `Product_ID` (transitive dependencies).

**Solution:**
- Split the table into three tables: `Orders`, `Customers`, and `Products`.

**Tables in 3NF:**

1. **Orders:**

   | Order_ID | Customer_ID | Product_ID | Quantity |
   |----------|-------------|------------|----------|
   | 1001     | C001        | P101       | 1        |
   | 1002     | C002        | P102       | 2        |
   | 1003     | C001        | P103       | 1        |

2. **Customers:**

   | Customer_ID | Customer_Name |
   |-------------|---------------|
   | C001        | John          |
   | C002        | Jane          |

3. **Products:**

   | Product_ID | Product_Name |
   |------------|--------------|
   | P101       | Laptop       |
   | P102       | Phone        |
   | P103       | Tablet       |

### Example 4:

✅ Before 3NF (Violates 3NF):

| EmployeeID | Name    | ZipCode | City        |
| :--------- | :------ | :------ | :---------- |
| 1          | Alice   | 94043   | Mountain View |
| 2          | Bob     | 10001   | New York    |

* Primary Key: EmployeeID
* City depends on ZipCode, which is a non-key attribute. This creates a transitive dependency:

		 EmployeeID -> ZipCode -> City
		 
✅ After 3NF (Decomposed into two tables):

Employees Table:

| EmployeeID | Name    | ZipCode |
| :--------- | :------ | :------ |
| 1          | Alice   | 94043   |
| 2          | Bob     | 10001   |

ZipCodes Table:

| ZipCode | City        |
| :------ | :---------- |
| 94043   | Mountain View |
| 10001   | New York    |

### Example 5:

✅  Before 3NF (Violates 3NF):

| OrderID | CustomerID | CustomerName | SalesRepID | SalesRepName |
| :------ | :--------- | :----------- | :--------- | :----------- |
| 101     | C1         | Carol        | S1         | Sam          |
| 102     | C2         | David        | S2         | Sarah        |

* Primary Key: OrderID
* CustomerName depends on CustomerID.
* SalesRepName depends on SalesRepID.

✅ After 3NF (Decomposed into three tables):

Orders Table:

| OrderID | CustomerID | SalesRepID |
| :------ | :--------- | :--------- |
| 101     | C1         | S1         |
| 102     | C2         | S2         |

Customers Table:

| CustomerID | CustomerName |
| :--------- | :----------- |
| C1         | Carol        |
| C2         | David        |

SalesReps Table:

| SalesRepID | SalesRepName |
| :--------- | :----------- |
| S1         | Sam          |
| S2         | Sarah        |

### Example 6:

✅  A Table Already in 3NF:

| ProductID | ProductName | Category    | Price |
| :-------- | :---------- | :---------- | :---- |
| P1        | Keyboard    | Electronics | 75    |
| P2        | Notebook    | Stationery  | 5     |
| P3        | T-shirt     | Apparel     | 20    |

---

### Summary:
- 3NF ensures that each table has no transitive dependencies.
- It improves data integrity and reduces redundancy by organizing 
  data into smaller, related tables.
- The examples demonstrate how to identify and resolve transitive 
  dependencies to achieve 3NF.


### **Third Normal Form (3NF)**
A table is in **Third Normal Form (3NF)** if:  
1. **It is in 2NF** (Second Normal Form).  
2. **There are no transitive dependencies**, meaning:  
   - **Non-key columns** must depend **only on the primary key**, 
     **not on other non-key columns**.  

---

### **Example 7: Removing Transitive Dependency in an Employee Table**
#### **2NF Table (Violating 3NF)**

| employee_id| employee_name| department_id| department_name|
|------------|--------------|--------------|----------------|
| E1         | Alice        | D101         | HR             |
| E2         | Bob          | D102         | IT             |
| E3         | Charlie      | D101         | HR             |

**Issue:**  
- **`department_name`** depends **on `department_id`**, 
  not on **`employee_id`**.  
- This creates a **transitive dependency** 
  (`employee_id → department_id → department_name`).  

#### **Converted to 3NF**
**Employees Table**

| employee_id| employee_name| department_id|
|------------|--------------|--------------|
| E1         | Alice        | D101         |
| E2         | Bob          | D102         |
| E3         | Charlie      | D101         |

**Departments Table**

| department_id| department_name|
|--------------|----------------|
| D101         | HR             |
| D102         | IT             |

✅ Now, **each non-key attribute depends only on the primary key**, 
and transitive dependency is removed.

---

### **Example 8: Removing Transitive Dependency in a Customer Orders Table**
#### **2NF Table (Violating 3NF)**

| order_id | customer_id | customer_name | customer_address|
|----------|-------------|---------------|-----------------|
| 201      | C1          | John Doe      | 123 Main St     |
| 202      | C2          | Jane Smith    | 456 Elm St      |
| 203      | C1          | John Doe      | 123 Main St     |

**Issue:**  

- **`customer_name`** and **`customer_address`** depend on **`customer_id`**, not **`order_id`**.

- This creates a **transitive dependency** (`order_id → customer_id → customer_name, customer_address`).  

#### **Converted to 3NF**
**Orders Table**

| order_id | customer_id|
|----------|------------|
| 201      | C1         |
| 202      | C2         |
| 203      | C1         |

**Customers Table**

| `customer_id`| `cust_first_name` | `cust_first_name` | `customer_address` |
|--------------|-------------------|-------------------|--------------------|
| C1           | John              | Doe               | 123 Main St        |
| C2           | Jane              | Smith             | 456 Elm St         |

✅ Now, **all non-key attributes depend only on the primary key**, 
eliminating transitive dependency.

---

### Example 9: Transitive Dependency

Let's walk through an example of a **transitive 
dependency** in a relational database and how it 
can be resolved by normalizing the table to Third 
Normal Form (3NF).

Consider the following table `employees_departments` 
which contains information about employees, their 
departments, and the locations of those departments:

| employee_id | employee_name | department_id | department_name | department_location |
|-------------|---------------|---------------|-----------------|---------------------|
| 1           | Alice         | 10            | HR              | New York            |
| 2           | Bob           | 20            | IT              | San Francisco       |
| 3           | Charlie       | 10            | HR              | New York            |
| 4           | David         | 30            | Marketing       | Chicago             |
| 5           | Eve           | 20            | IT              | San Francisco       |

### Problems with the Initial Table

- The table is in Second Normal Form (2NF) but not in Third Normal Form (3NF).
- There is a transitive dependency: `department_location` depends on `department_id`, which in turn depends on `employee_id`.

### Transitive Dependency

- **Direct Dependency**: `department_id` directly depends on `employee_id`.
- **Transitive Dependency**: `department_location` depends on `department_id`, which depends on `employee_id`.

### Conversion to Third Normal Form (3NF)

To convert the table into 3NF, we need to remove the transitive dependencies by creating separate tables for employees, departments, and department locations.

### Step 1: Create Separate Tables

1. **Employees Table**:
    - Contains employee-specific information.
    - `employee_id` is the primary key.

2. **Departments Table**:
    - Contains department-specific information.
    - `department_id` is the primary key.

3. **Department Locations Table**:
    - Contains location-specific information.
    - `department_id` is the primary key.

### Final Tables in Third Normal Form (3NF)

#### Employees Table

| employee_id | employee_name | department_id |
|-------------|---------------|---------------|
| 1           | Alice         | 10            |
| 2           | Bob           | 20            |
| 3           | Charlie       | 10            |
| 4           | David         | 30            |
| 5           | Eve           | 20            |

#### Departments Table

| department_id | department_name |
|---------------|-----------------|
| 10            | HR              |
| 20            | IT              |
| 30            | Marketing       |

#### Department Locations Table

| department_id | department_location |
|---------------|---------------------|
| 10            | New York            |
| 20            | San Francisco       |
| 30            | Chicago             |

### Explanation

1. **Employees Table**: Contains unique employee 
   records with a foreign key reference to the 
   `departments` table.
2. **Departments Table**: Contains unique 
   department records.
3. **Department Locations Table**: Contains unique 
   department location records with a foreign key 
   reference to the `departments` table.

		By normalizing the table and removing 
		transitive dependencies, we ensure that 
		each piece of information is stored ONLY
		ONCE, eliminating redundancy and maintaining 
		data integrity. 
		
		This approach helps in achieving Third Normal 
		Form (3NF), ensuring that non-key attributes 
		are only dependent on the primary key.


### **Summary**

To convert a table to **3NF**, we:

1. **Identified transitive dependencies**.

2. **Moved dependent attributes** to a separate table 
   where they directly depend on a primary key.


--------

# References & Tutorials

The following are some tutorials for Database Normalization
 
1. [Normal Forms in DBMS](https://www.geeksforgeeks.org/normal-forms-in-dbms/)

2. [Why Normalization in DBMS is Essential for Databases](https://www.simplilearn.com/tutorials/sql-tutorial/what-is-normalization-in-sql)

3. [DBMS - Normalization](https://www.tutorialspoint.com/dbms/database_normalization.htm)
