# MySQL WITH
# Common Table Expressions

	1. A common table expression in MySQL is a 
	   temporary result whose scope is confined 
	   to a single statement. 
	
	2. You can refer this expression multiple 
	   times with in the statement.

	3. The WITH clause in MySQL is used to 
	   specify a Common Table Expression, a with 
	   clause can have one or more comms-separated 
	   subclauses.

Syntax:

Following is the syntax of the WITH clause:

~~~SQL
WITH
 name_for_summary_data AS (SELECT Statement)

SELECT columns
FROM name_for_summary_data
WHERE conditions <=> (
   SELECT column
   FROM name_for_summary_data
)[ORDER BY columns]
~~~

## Multiple CTEs

~~~sql
WITH
    cte_name1 AS (
        -- Query here
    ),
    cte_name2 AS (
        -- Query here
    )
    SELECT ... from cte_name1, cte_name2 ...
~~~


Example

	Assume we have created a table named data 
	and populated it as shown below −

~~~sql
CREATE TABLE data(
   ID INT,
   NAME CHAR(20),
   AGE INT,
   SALARY INT
);
~~~

Let's insert some records into the data table −

~~~sql
INSERT INTO data values 
(101, 'Raja', 25, 55452),
(102, 'Roja', 29, 66458),
(103, 'Roja', 35, 36944);
~~~

Following query demonstrates the usage of the WITH clause −

~~~sql
WITH CTE 
  AS (SELECT ID, NAME, AGE, SALARY FROM data)
SELECT * From CTE; 
~~~

Following is the output of the above query −

~~~sql
ID	NAME	AGE	SALARY
101	Raja	25	55452
102	Roja	29	66458
103	Roja	35	36944
~~~

## CTE from multiples tables

	You can also create a Common Table Expression 
	from multiple tables.

Example

	Suppose we have created a table with name 
	EMPLOYEE and populated data into it as shown below −

~~~sql
CREATE TABLE EMPLOYEE(
   ID INT NOT NULL,
   FIRST_NAME CHAR(20) NOT NULL,
   LAST_NAME CHAR(20),
   AGE INT,
   SEX CHAR(1),
   INCOME FLOAT,
   CONTACT INT
);
~~~

Now, let's insert two records into the Employee table −

~~~sql
INSERT INTO Employee VALUES
(101, 'Ramya', 'Rama Priya', 27, 'F', 9000, 101),
(102, 'Vinay', 'Bhattacharya', 20, 'M', 6000, 102);
~~~

And, if we have created another table and populated it as −

~~~sql
CREATE TABLE CONTACT(
   ID INT NOT NULL,
   EMAIL CHAR(20) NOT NULL,
   PHONE LONG,
   CITY CHAR(20)
);
~~~

Now, let us insert some records into the CONTACT table −

~~~sql
INSERT INTO CONTACT (ID, EMAIL, CITY) VALUES
(101, 'ramya@mymail.com', 'Hyderabad'),
(102, 'vinay@mymail.com', 'Vishakhapatnam');
~~~

	Following query create a Common Table Expression 
	from the above two tables −

~~~sql
WITH 
  exp1 AS (SELECT ID, FIRST_NAME, LAST_NAME FROM EMPLOYEE),
  exp2 AS (SELECT EMAIL, PHONE FROM CONTACT)
SELECT * FROM exp1 JOIN exp2;
~~~

Output

The above query produces the following output −

~~~sql
ID	FIRST_NAME	LAST_NAME		EMAIL				PHONE
102	Vinay		Bhattacharya	ramya@mymail.com	NULL
101	Ramya		Rama Priya		ramya@mymail.com	NULL
102	Vinay		Bhattacharya	vinay@mymail.com	NULL
101	Ramya		Rama Priya		vinay@mymail.com	NULL
~~~

------

# MySQL: Complex WITH Example

~~~sql
-- define query parameters
set reference = 1;
set filter_value = 1.2;

with gene_averages as 
(
 select gene_id, 
        subject_id, 
        avg(fold_change) as avg_fc, 
        abs(avg(fold_change)) as abs_avg_fc 
        from gene_expression
    where  
       reference = $reference AND 
       gene_id is not null AND 
       sample_id in (12345, 12346, 14135, 13735)
    group by gene_id, subject_id
) 
  select 
    gene_id, 
    count(subject_id) as s,
    sum(case WHEN abs_avg_fc >= $filter_value then 1 else 0 end) as sum,
    sum(case WHEN abs_avg_fc >= $filter_value and avg_fc > 0.0 THEN 1 ELSE 0 end) as p, 
    sum(case WHEN abs_avg_fc >= $filter_value and avg_fc < 0.0 THEN 1 ELSE 0 end) as n, 
    sum(case WHEN abs_avg_fc >= $filter_value and avg_fc = 0.0 THEN 1 ELSE 0 end) as z
  from gene_averages 
    group by gene_id;
~~~

Output

~~~sql
GENE_ID		S	SUM  P	N	Z
100289341	4	2	 0	2	0
100669346	3	2	 0	1	0
...
~~~

