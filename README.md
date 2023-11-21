# data-warehousing

<img 
        alt="data-lakehouse" 
        src="./web_docs/data_warehouse_image.png"
        width="550" 
        height="700"
>

![](./web_docs/data_warehouse_image.png)


## 0. Git Repository


* This repository is a place for **Data Warehousing** 
  Course (MSIS-2621) at Santa Clara University.
  
  
* [MSIS 2621: Business Intelligence and Data Warehousing](https://www.scu.edu/business/graduate-degrees/ms-programs/ms-information-systems/curriculum/)
	* [Graduate School, Leavey School of Business](https://www.scu.edu/business/)
	* [Department of Information Systems & Analytics](https://www.scu.edu/business/isa/)


* Spring Quarter 2024 (January-March)
	* Class room: Lucas Hall (LH) 310
	* Office: 316U, Lucas Hall (LH)
	* Office Hours: via scheduled Zoom and by appointment


## 1. Course Information: 
	
	This course  is about  data warehousing  and  its 
	role in carrying out modern business intelligence 
	for  actionable  insight  to address new business 
	needs. A data warehouses is the central component 
	of a modern data stack (a modern data  stack is a 
	combination  of  various  software  tools used to 
	collect,  process,  and  store  data  on  a  well 
	integrated    cloud   based    data    platform). 

## 2. Class Meeting Dates & Hours

* **Class meeting dates**: 
	* Start: January 9, 2024
	* End: March 21, 2024
	* Final Exam week: March 18-21, 2024

* **Class hours**:  
	* Tuesday 5:45 PM - 7:20 PM PST
	* Thursday 5:45 PM - 7:20 PM PST

## 3.  [Instructor, Adjunct Professor: Mahmoud Parsian](https://www.scu.edu/business/isa/faculty/parsian/)

## 4.  [Prerequisite](./web_docs/prerequisite.md)

## 5.  [Course Description & Concepts](./web_docs/course_description.md)

## 6.  [Data Warehousing Class Web Site](https://github.com/mahmoudparsian/data-warehousing)

## 7.  [Glossary of Big Data, MapReduce, Spark, Data Warehousing](./slides/glossary/glossary_of_big_data_and_mapreduce.md)

## 8.  [Required Books and Papers](./web_docs/required_books.md)

## 9.  [Optional Books and References](./web_docs/optional_books.md)

## 10.  [Required Software: MapReduce & Spark/PySpark](./web_docs/required_software.md)

## 11.  [Syllabus, Winter Quarter 2024](./syllabus/2024-01-Winter/README.md)

## 12. [Grading and Class Conduct](./web_docs/grading_and_class_conduct.md)

## 13. [Python Tutorials](./web_docs/python_tutorials.md)

## 14. [SQL Tutorials](./web_docs/sql_tutorials.md)

## 15. [Office Hours](./web_docs/office_hours.md)

## 16. [Midterm Exam](./web_docs/midterm_exam.md)

## 17. [Final Exam](./web_docs/final_exam.md)

## 18. Mahmoud Parsian's Latest Books: 

-------

### Data Algorithms with Spark 

<a href="https://github.com/mahmoudparsian/data-algorithms-with-spark/blob/master/README.md">
    <img 
        alt="Data Algorithms with Spark" 
        src="images/Data_Algorithms_with_Spark_COVER_9781492082385.png"
        width="550" 
        height="600"
    >
</a>

------

### PySpark Algorithms 

<a href="https://www.amazon.com/PySpark-Algorithms-Version-Mahmoud-Parsian-ebook/dp/B07X4B2218/">
    <img 
        alt="PySpark Algorithms Book" 
        src="images/pyspark_algorithms.jpg"
        width="550" 
        height="600"
    >
</a>

-------

### Data Algorithms 

<a href="http://shop.oreilly.com/product/0636920033950.do">
    <img 
        alt="Data Algorithms Book" 
        src="images/large-image.jpg"
        width="550" 
        height="700"
    >
</a>


CMU data warehousing course:
https://api.heinz.cmu.edu/courses_api/course/syllabus/360883/
https://api.heinz.cmu.edu/courses_api/course/syllabus/360883/


TLC Trip Record Data
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Data Dictionary – Yellow Taxi Trip Records 
https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf

Working With Parquet Format
https://www.nyc.gov/assets/tlc/downloads/pdf/working_parquet_format.pdf

What is an ETL
https://docs.getdbt.com/terms/elt

https://github.com/letthedataconfess/Data-Engineering-Books/tree/main

What is Data Warehouse? Types, Definition & Example
by David Taylor: https://www.guru99.com/data-warehousing.html#general-stages-of-data-warehouse

Data Warehousing Tutorial
https://www.tutorialspoint.com/dwh/index.htm


----
Week 1:  Data ingest (ETL)
         a. [What is ELT (Extract, Load, Transform)?](https://docs.getdbt.com/terms/elt)
         b. Example of ELT using Python: read parquet and create a RDBMS Table
         c. ETL vs ELT: Differences and Similarities | Snowflake Guides
         
         To write a Pandas dataframe to MySQL, you will need to perform the following steps:
			1. Connect to the MySQL database.
			2. Create a table in the database to store the data.
			3. Convert the Pandas dataframe to a format that can be inserted into the MySQL table.
			4. Insert the data into the MySQL table.

Week 2: Transform data to Database Tables
			
		[Python MySQL Insert Into Table]
		(https://www.w3schools.com/python/python_mysql_insert.asp)
		
		[How to insert pandas dataframe via mysqldb into database?]
		(https://stackoverflow.com/questions/16476413/how-to-insert-pandas-dataframe-via-mysqldb-into-database)
		
		Write records stored in a DataFrame to a SQL database.
		[pandas.DataFrame.to_sql]
		(https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html)

        Pandas 0.20.2 to_sql() using MySQL
        https://stackoverflow.com/questions/44933704/pandas-0-20-2-to-sql-using-mysql

		2. Transform data using dbt
		a. Introduction to dbt (data build tool) from Fishtown Analytics
		b. How to build a mature dbt project from scratch (w/ Dave Connors)
		c. Excelling at dbt: Jinja & Macros for modular and cleaner SQL Queries
		d. Data Wrangling with SQL | Advanced SQL - Mode
		e. Using SQL String Functions to Clean Data | Advanced SQL - Mode

3. Maintain data quality
a. Tutorial: Using dbt to Test for Schema Changes
b. How to Manage Data Quality: A Comprehensive Guide
c. Open source interviews #14 - Maayan Salom, founder of Elementary Data
d. Compounding Quality

4. Compare data modeling strategies
Note: ignore all mentions of Data Vault
a. Babies and bathwater: Is Kimball still relevant?
b. Introducing the activity schema data modeling with a single table
c. Data Vault vs Star Schema vs Third Normal Form: Which Data Model to Use?
d. Back to the Future: Where Dimensional Modeling Enters the Modern Data Stack
e. Comparative study of data warehouses modeling approaches: Inmon, Kimball and Data Vault
f. FDE Chapter 8, pp. 291-310

5. Advanced SQL for data analytics
a. SQL Joins | Intermediate SQL - Mode
b. SQL Aggregate Functions | Intermediate SQL - Mode
c. SQL Window Functions | Advanced SQL - Mode
d. Use Common Table Expressions (CTE) to Keep Your SQL Clean | Mode
e. Back to the Basics With SQL- Date Functions

6. Data warehouse architecture
a. Databases Demystified Chapter 3 – Row Store vs. Column Store | Blog | Fivetran
b. Benchmark (computing) - Wikipedia through “Benchmarking Principles”
c. Understanding Snowflake Table Structures
d. MPP: The Transformation on Big Data Analytics | by Maggy Hu | Slalom Technology |
Medium.
e. (optional) Designing Data-Intensive Applications (available on Canvas), chapter 3, pp.
90-103, chapter 6 pp. 199-219

7. Reporting and BI
a. A Comprehensive Guide to the Grammar of Graphics for Effective Visualization of
Multi-dimensional Data | by Dipanjan (DJ) Sarkar
b. Reporting vs. Analytics: What's the Difference? | Indeed.com
c. Difference Between Business Analytics and Predictive Analytics - GeeksforGeeks
d. Reporting, Predictive Analytics, and Everything in Between (available on Canvas), pp. TBD
5


data-warehousing (main *) % python3 -m pip install pymysql
Collecting pymysql
  Obtaining dependency information for pymysql from https://files.pythonhosted.org/packages/e5/30/20467e39523d0cfc2b6227902d3687a16364307260c75e6a1cb4422b0c62/PyMySQL-1.1.0-py3-none-any.whl.metadata
  Downloading PyMySQL-1.1.0-py3-none-any.whl.metadata (4.4 kB)
Downloading PyMySQL-1.1.0-py3-none-any.whl (44 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 44.8/44.8 kB 829.6 kB/s eta 0:00:00
Installing collected packages: pymysql
Successfully installed pymysql-1.1.0

Working With Parquet Format

import pyarrow.parquet as pq
trips = pq.read_table('trips.parquet')
trips = trips.to_pandas()

engine = create_engine('mysql+mysqldb://[user]:[pass]@[host]:[port]/[schema]', echo = False)
df.to_sql(name = 'my_table', con = engine, if_exists = 'append', index = False)
Where [schema] is the database name, and in my particular case, 
:[port] is omitted with [host] being localhost.


Week 3: Introduction to RDBMS, SQL, Data Quality


----

~~~python
def f()
 a = 2
 c = '123'
~~~

CSE 414 - Introduction to Database Systems
University of Washington
https://sites.google.com/cs.washington.edu/cse414-23sp
https://sites.google.com/cs.washington.edu/cse414-23au