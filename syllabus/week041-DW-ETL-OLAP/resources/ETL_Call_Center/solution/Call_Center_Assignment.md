# Call Center ETL

You are to write and execute a simple ETL and 
finally write and execute some SQL queries. 

1. read Call_Center.csv

https://github.com/mahmoudparsian/data-warehousing/blob/main/syllabus/week-05_ETL_detailed/CALL_CENTER/Call_Center.csv

2. Transformations:

2.1 From `call_timestamp` create a `call_date` 
as a DATE data type.

2.2 from `call_date` column, create a new 
column/field as day of a month `day_of_month` 
(the values will be in range of 1, 2, ..., 31)

2.3 Create a `day_of_week` field/column from `call_date` 
(values will be Saturday, Sunday, Monday, Tuesday, Wednesday, Friday)

2.4 The `csat_score` has to be greater than 0.
If any value is less than or equal to zero, then 
set it to NULL.

2.5 rename a column:
rename `call duration in minutes` column to  `call_duration_minutes`

3. load revised/transformed data into MySQL

4. Run the following queries:
4.1 show SQL Query in a very readable text format
4.2 show SQL query output as a readable text table 
(properly formatted).

1. Using SQL query, Create the following table:


  Feature        | Unique Count   
 --------------  | -------------- 
 `sentiment`     | `<value>`        
 `reason`        | `<value>`        
 `channel`       | `<value>`       
 `response_time` | `<value>`        
 `call_center`   | `<value>`    
 
 
 2. Which day has the most of the calls 
 and which day has the least number of calls
 

 3. Find, minimum, maximum, and average 
 call duration in minutes per day
 
 4. Find Average Call Duration and Response Time 
 by State and Sentiment
 
 5. Find daily Distribution of Calls by Call Center

 6. Find average CSAT score for each customer 
and channel, and ranks them within each channel.


File `Call_Center.csv` columns:

~~~
id,
customer_name,
sentiment,
csat_score,
call_timestamp,
reason,
city,
state,
channel,
response_time,
call duration in minutes, => CONVERT TO: call_duration_minutes
call_center
~~~

ETL Generated Table:

~~~sql
CREATE TABLE calls (
	id VARCHAR(50),
	customer_name VARCHAR(50),
	sentiment VARCHAR(20),
	csat_score INT,
	call_timestamp VARCHAR(10),
	call_date DATE,              -- added
	quarter INT,                 -- added
	day_of_week VARCHAR(10),     -- added
	day_of_month INT,            -- added
	reason VARCHAR(20),
	city VARCHAR(50),
	state VARCHAR(20),
	channel VARCHAR(24),
	response_time VARCHAR(24),
	call_duration_minutes INT,   -- renamed
	call_center VARCHAR (20)
);~~~


