# Database Normalization

## 1. What is a Database Normalization

	Database normalization is the process 
	of organizing  data in a  database to 
	eliminate  redundancy, improve  data 
	integrity, and make the database more 
	flexible: 

	1. Eliminate redundancy: 
		Redundant data wastes disk space 
		and creates maintenance problems. 

	2. Improve data integrity: 
		Normalized relations mirror real-world 
		concepts and their interrelationships. 

	3. Make the database more flexible: 
		A fully normalized database can be 
		extended to accommodate  new  types 
		of data without changing existing 
		structure too much. 

	4. Benefits of database normalization: 
		1. Simplifies the query process 
		2. Improves workflow 
		3. Increases security 
		4. Lessens costs

	5. Normalization is commonly used when dealing 
		with large datasets. It involves breaking 
		down a large, complex  table into  smaller 
		and  simpler tables while  maintaining data 
		relationships. 

## 2. Normal Forms in DBMS

	Normalization is the process of minimizing 
	redundancy from a relation or set of relations. 
	Redundancy in relation  may  cause  insertion, 
	deletion, and update anomalies. So, it helps to 
	minimize the redundancy in relations. Normal 
	forms are used to eliminate or reduce 
	redundancy in database tables.

	Normalization of DBMS:
	
	In database management systems (DBMS), normal 
	forms are a series of guidelines that help to 
	ensure that  the  design of  a  database  is 
	efficient, organized,  and  free  from  data 
	anomalies.   There  are  several levels  of 
	normalization, each  with  its  own set  of 
	guidelines, known as normal forms.

	Important Points Regarding Normal Forms in DBMS:
	
	* First Normal Form (1NF): 
	
		This is the most basic level of normalization. 
		In 1NF, each table cell should contain only a 
		single value,  and each  column  should  have 
		a unique name. The first normal form helps to 
		eliminate duplicate data and simplify queries.
		
	* Second Normal Form (2NF): 
	
		2NF eliminates redundant data by requiring 
		that each non-key attribute be dependent on 
		the primary key. This means that each column 
		should be directly related to the primary key, 
		and not to other columns.
		
	* Third Normal Form (3NF): 
	
		3NF  builds on 2NF by requiring  that  all 
		non-key attributes are independent of each 
		other. This means that each column should 
		be  directly related  to the  primary key, 
		and not to any other columns in the same 
		table.
		
	* Boyce-Codd Normal Form (BCNF): 
	
		BCNF is a stricter form of 3NF that ensures 
		that each determinant in a table is a candidate 
		key. In other words, BCNF ensures  that  each 
		non-key attribute is dependent only on the 
		candidate key.


## 3. Tutorials

The following are some tutorials for Database Normalization
 
1. [Normal Forms in DBMS](https://www.geeksforgeeks.org/normal-forms-in-dbms/)

2. [Why Normalization in DBMS is Essential for Databases](https://www.simplilearn.com/tutorials/sql-tutorial/what-is-normalization-in-sql)

3. [DBMS - Normalization](https://www.tutorialspoint.com/dbms/database_normalization.htm)

