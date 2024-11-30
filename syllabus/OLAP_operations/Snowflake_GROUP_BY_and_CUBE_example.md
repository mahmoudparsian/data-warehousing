# Snowflake GROUP BY

source: [Snowflake Documentation](https://docs.snowflake.com/en/sql-reference/constructs/group-by)

## GROUP BY

	Groups rows with the same group-by-item expressions 
	and computes aggregate functions for the resulting group. 
	A GROUP BY expression can be:

* A column name.

* A number referencing a position in the SELECT list.

* A general expression.

* Extensions:
	* GROUP BY CUBE , 
	* GROUP BY ROLLUP
	* GROUP BY GROUPING SETS , 



## GROUP BY CUBE

	GROUP BY CUBE is an extension of the GROUP BY 
	clause similar to GROUP BY ROLLUP. In addition
	to producing all the rows of a GROUP BY ROLLUP, 
	GROUP BY CUBE adds all the “cross-tabulations” rows. 
	
	Sub-total rows are rows that further aggregate whose 
	values are derived by computing the same aggregate 
	functions that were used to produce the grouped rows.


	A CUBE grouping is equivalent to a series of grouping 
	sets and is essentially a shorter specification. The 
	N elements of a CUBE specification correspond to 2^N 
	GROUPING SETS.


Example -- Create some tables and insert some rows.

~~~sql
CREATE TABLE products (
   product_ID INTEGER, 
   wholesale_price REAL
);

INSERT INTO products (product_ID, wholesale_price) VALUES 
    (1, 1.00),
    (2, 2.00);

CREATE TABLE sales (
   product_ID INTEGER, 
   retail_price REAL, 
   quantity INTEGER, 
   city VARCHAR, 
   state VARCHAR
);

INSERT INTO sales 
  (product_id, retail_price, quantity, city, state) VALUES 
    (1, 2.00,  1, 'SF', 'CA'),
    (1, 2.00,  2, 'SJ', 'CA'),
    (2, 5.00,  4, 'SF', 'CA'),
    (2, 5.00,  8, 'SJ', 'CA'),
    (2, 5.00, 16, 'Miami', 'FL'),
    (2, 5.00, 32, 'Orlando', 'FL'),
    (2, 5.00, 64, 'SJ', 'PR');
~~~

### Using CUBE

~~~sql   
SELECT state, city, 
       SUM((s.retail_price - p.wholesale_price) * s.quantity) AS profit 
 FROM products AS p, sales AS s
 WHERE s.product_ID = p.product_ID
 GROUP BY CUBE (state, city)
 ORDER BY state, city NULLS LAST
 ;
+-------+---------+--------+
| STATE | CITY    | PROFIT |
|-------+---------+--------|
| CA    | SF      |     13 |
| CA    | SJ      |     26 |
| CA    | NULL    |     39 |
| FL    | Miami   |     48 |
| FL    | Orlando |     96 |
| FL    | NULL    |    144 |
| PR    | SJ      |    192 |
| PR    | NULL    |    192 |
| NULL  | Miami   |     48 |
| NULL  | Orlando |     96 |
| NULL  | SF      |     13 |
| NULL  | SJ      |    218 |
| NULL  | NULL    |    375 |
+-------+---------+--------+
~~~

### GROUP BY ROLLUP

	1. GROUP BY ROLLUP is an extension of the GROUP BY 
	clause that produces sub-total rows (in addition 
	to the grouped rows). Sub-total rows are rows that 
	further aggregate whose values are derived by 
	computing the same aggregate functions that were 
	used to produce the grouped rows.

	2. You can think of rollup as generating multiple 
	result sets, each of which (after the first) is the 
	aggregate of the previous result set. So, for example, 
	if you own a chain of retail stores, you might want 
	to see the profit for:

		Each store.

		Each city (large cities might have multiple stores).

		Each state.

		Everything (all stores in all states).


	NOTE: You could create separate reports to get 
	      that information, but it is more efficient 
	      to scan the data once.

			If you are familiar with the concept of 
			grouping sets (GROUP BY GROUPING SETS) you 
			can think of a ROLLUP grouping as equivalent 
			to a series of grouping sets, and which is 
			essentially a shorter specification. 
			The N elements of a ROLLUP specification 
			correspond to N+1 GROUPING SETS.


Example -- Create some tables and insert some rows.

~~~sql
CREATE TABLE products (
   product_ID INTEGER, 
   wholesale_price REAL
);

INSERT INTO products 
  (product_ID, wholesale_price) VALUES 
    (1, 1.00),
    (2, 2.00);
~~~

~~~sql 
CREATE TABLE sales (
   product_ID INTEGER, 
   retail_price REAL, 
   quantity INTEGER, 
   city VARCHAR, 
   state VARCHAR);
   
INSERT INTO sales 
  (product_id, retail_price, quantity, city, state) VALUES 
    (1, 2.00,  1, 'SF', 'CA'),
    (1, 2.00,  2, 'SJ', 'CA'),
    (2, 5.00,  4, 'SF', 'CA'),
    (2, 5.00,  8, 'SJ', 'CA'),
    (2, 5.00, 16, 'Miami', 'FL'),
    (2, 5.00, 32, 'Orlando', 'FL'),
    (2, 5.00, 64, 'SJ', 'PR');
~~~
   
	ROLL UP Query:
	--------------
	Run a rollup query that shows profit by 
	city, state, and total across all states.

	The example below shows a query that has three “levels”:

			Each city.

			Each state.

			All revenue combined.


	This example uses ORDER BY state, 
	city NULLS LAST to ensure that each 
	state’s rollup comes immediately after 
	all of the cities in that state, and 
	that the final rollup appears at the 
	end of the output.

~~~sql
SELECT state, city, 
  SUM((s.retail_price - p.wholesale_price) * s.quantity) AS profit 
 FROM products AS p, sales AS s
 WHERE s.product_ID = p.product_ID
 GROUP BY ROLLUP (state, city)
 ORDER BY state, city NULLS LAST
 ;
+-------+---------+--------+
| STATE | CITY    | PROFIT |
|-------+---------+--------|
| CA    | SF      |     13 |
| CA    | SJ      |     26 |
| CA    | NULL    |     39 |
| FL    | Miami   |     48 |
| FL    | Orlando |     96 |
| FL    | NULL    |    144 |
| PR    | SJ      |    192 |
| PR    | NULL    |    192 |
| NULL  | NULL    |    375 |
+-------+---------+--------+
~~~

	Some rollup rows contain NULL values. 
	For example, the last row in the table 
	contains a NULL value for the city and a 
	NULL value for the state because the data 
	is for all cities and states, not a specific 
	city and state.

## GROUP BY GROUPING SETS

	GROUP BY GROUPING SETS is a powerful extension 
	of the GROUP BY clause that computes multiple 
	group-by clauses in a single statement. The 
	group set is a set of dimension columns.

	NOTE:
	-----
	GROUP BY GROUPING SETS is equivalent to 
	   the UNION of two or more GROUP BY operations 
	   in the same result set:

		GROUP BY GROUPING SETS(a) is equivalent to the 
		single grouping set operation GROUP BY a.

		GROUP BY GROUPING SETS(a,b) is equivalent to 
		GROUP BY a UNION ALL GROUP BY b.

Examples

	These examples use a table of information 
	about nurses who are trained to assist in 
	disasters. 
	
	All of these nurses have a license as nurses 
	(e.g. an RN has a license as a “Registered Nurse”), 
	and an additional license in a disaster-related 
	specialty, such as search and rescue, radio 
	communications, etc. 
	
	This example simplifies and uses just two 
	categories of licenses:

		Nursing: RN (Registered Nurse) and 
		         LVN (Licensed Vocational Nurse).

		Amateur (“ham”) Radio: 
		Ham radio licenses include 
			“Technician”, 
			“General”, and 
			“Amateur Extra”.

Here are the commands to create and load the table:

~~~sql
CREATE or replace TABLE nurses (
  ID INTEGER,
  full_name VARCHAR,
  medical_license VARCHAR,   -- LVN, RN, etc.
  radio_license VARCHAR      -- Technician, General, Amateur Extra
);

INSERT INTO nurses
    (ID, full_name, medical_license, radio_license)
  VALUES
    (201, 'Thomas Leonard Vicente', 'LVN', 'Technician'),
    (202, 'Tamara Lolita VanZant', 'LVN', 'Technician'),
    (341, 'Georgeann Linda Vente', 'LVN', 'General'),
    (471, 'Andrea Renee Nouveau', 'RN', 'Amateur Extra')
    ;
~~~
    
### This query uses GROUP BY GROUPING SETS:

~~~sql
SELECT COUNT(*), medical_license, radio_license
  FROM nurses
  GROUP BY GROUPING SETS (medical_license, radio_license);
~~~

Output:

	The first two rows show the count of RNs and LVNs 
	(two types of nursing licenses). The NULL values 
	in the RADIO_LICENSE column for those two rows are 
	deliberate; the query grouped all of the LVNs together 
	(and all the RNs together) regardless of their radio 
	license, so the results can’t show one value in the 
	RADIO_LICENSE column for each row that necessarily 
	applies to all the LVNs or RNs grouped in that row.

	The next three rows show the number of nurses with 
	each type of ham radio license (“Technician”, “General”, 
	and “Amateur Extra”). The NULL value for MEDICAL_LICENSE 
	in each of those three rows is deliberate because no single 
	medical license necessarily applies to all members of each 
	of those rows.

~~~sql
+----------+-----------------+---------------+
| COUNT(*) | MEDICAL_LICENSE | RADIO_LICENSE |
|----------+-----------------+---------------|
|        3 | LVN             | NULL          |
|        1 | RN              | NULL          |
|        2 | NULL            | Technician    |
|        1 | NULL            | General       |
|        1 | NULL            | Amateur Extra |
+----------+-----------------+---------------+
~~~

	The next example shows what happens when some 
	columns contain NULL values. Start by adding 
	three new nurses who don’t yet have ham radio licenses.

~~~sql
INSERT INTO nurses
    (ID, full_name, medical_license, radio_license)
  VALUES
    (101, 'Lily Vine', 'LVN', NULL),
    (102, 'Larry Vancouver', 'LVN', NULL),
    (172, 'Rhonda Nova', 'RN', NULL)
    ;
~~~

Then run the same query as before:

~~~sql
SELECT COUNT(*), medical_license, radio_license
  FROM nurses
  GROUP BY GROUPING SETS (medical_license, radio_license);
~~~

Output:

	The first 5 lines are the same as in the previous query.

	The last line might be confusing at first – 
	why is there a line that has NULL in both 
	columns? And if all the values are NULL, 
	why is the COUNT(*) equal to 3?

	The answer is:
	--------------
	The answer is that the NULL in the RADIO_LICENSE 
	column of that row occurs because three nurses 
	don’t have any radio license. 
	(“SELECT DISTINCT RADIO_LICENSE FROM nurses” now 
	returns four distinct values: “Technician”, 
	“General”, “Amateur Extra”, and “NULL”.)

	The NULL in the MEDICAL_LICENSES column occurs for 
	the same reason that NULL values occur in the earlier 
	query results: the nurses counted in this row have 
	different MEDICAL_LICENSES, so no one value (“RN” or “LVN”) 
	necessarily applies to all of the nurses counted in this row.

~~~sql
+----------+-----------------+---------------+
| COUNT(*) | MEDICAL_LICENSE | RADIO_LICENSE |
|----------+-----------------+---------------|
|        5 | LVN             | NULL          |
|        2 | RN              | NULL          |
|        2 | NULL            | Technician    |
|        1 | NULL            | General       |
|        1 | NULL            | Amateur Extra |
|        3 | NULL            | NULL          |
+----------+-----------------+---------------+
~~~

	If you’d like, you can compare this output 
	to the output of a GROUP BY without the 
	GROUPING SETS clause:

~~~sql
SELECT COUNT(*), medical_license, radio_license
  FROM nurses
  GROUP BY medical_license, radio_license;
~~~

Output:

~~~sql
+----------+-----------------+---------------+
| COUNT(*) | MEDICAL_LICENSE | RADIO_LICENSE |
|----------+-----------------+---------------|
|        2 | LVN             | Technician    |
|        1 | LVN             | General       |
|        1 | RN              | Amateur Extra |
|        2 | LVN             | NULL          |
|        1 | RN              | NULL          |
+----------+-----------------+---------------+
~~~  