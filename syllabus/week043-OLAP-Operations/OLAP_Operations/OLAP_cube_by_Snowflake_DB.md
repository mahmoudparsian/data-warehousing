# GROUP BY CUBE (in snowflake.com)

	GROUP BY CUBE is an extension of the 
	GROUP BY clause similar to GROUP BY ROLLUP. 
	In addition to producing all the rows of 
	a GROUP BY ROLLUP, GROUP BY CUBE adds 
	all the “cross-tabulations” rows. 
	Sub-total rows are rows that further 
	aggregate whose values are derived by 
	computing the same aggregate functions 
	that were used to produce the grouped rows.


	A CUBE grouping is equivalent to a series 
	of grouping sets and is essentially a shorter 
	specification. 
	
	The N elements of a CUBE specification 
	correspond to 2^N GROUPING SETS.

# Table definition

~~~
create table sales_table(
   country text, 
   city text, 
   year int, 
   sales int
);
~~~

# Table Population

~~~sql
insert into sales_table(country, city, year, sales) 
values
('USA', 'Sunnyvale', 2020, 2000),
('USA', 'Sunnyvale', 2020, 3000),
('USA', 'Sunnyvale', 2024, 1000),
('USA', 'Sunnyvale', 2024, 2000),
('USA', 'Sunnyvale', 2024, 4000),

('USA', 'Cupertino', 2020, 6000),
('USA', 'Cupertino', 2020, 5000),
('USA', 'Cupertino', 2020, 7000),
('USA', 'Cupertino', 2024, 6000),
('USA', 'Cupertino', 2024, 8000),
('USA', 'Cupertino', 2024, 9000),

('CANADA', 'Toronto', 2020, 800),
('CANADA', 'Toronto', 2020, 700),
('CANADA', 'Toronto', 2024, 500),
('CANADA', 'Toronto', 2024, 600),
('CANADA', 'Toronto', 2024, 800),

('CANADA', 'Ottawa', 2020, 1000),
('CANADA', 'Ottawa', 2020, 2000),
('CANADA', 'Ottawa', 2020, 3000),
('CANADA', 'Ottawa', 2024, 4000),
('CANADA', 'Ottawa', 2024, 5000),
('CANADA', 'Ottawa', 2024, 6000);
~~~


# SELECT All Rows

~~~sql
select * from sales_table;

COUNTRY   CITY        YEAR   SALES
USA       Sunnyvale   2020   2000
USA       Sunnyvale   2020   3000
USA       Sunnyvale   2024   1000
USA       Sunnyvale   2024   2000
USA       Sunnyvale   2024   4000
USA       Cupertino   2020   6000
USA       Cupertino   2020   5000
USA       Cupertino   2020   7000
USA       Cupertino   2024   6000
USA       Cupertino   2024   8000
USA       Cupertino   2024   9000
CANADA    Toronto     2020    800
CANADA    Toronto     2020    700
CANADA    Toronto     2024    500
CANADA    Toronto     2024    600
CANADA    Toronto     2024    800
CANADA    Ottawa      2020   1000
CANADA    Ottawa      2020   2000
CANADA    Ottawa      2020   3000
CANADA    Ottawa      2024   4000
CANADA    Ottawa      2024   5000
CANADA    Ottawa      2024   6000
~~~

# GROUP BY ROLLUP (country, year)
~~~sql
SELECT country, 
       year, 
       sum(sales) as sum_of_sales
FROM 
     sales_table 
GROUP BY 
     ROLLUP (country, year)
ORDER BY 
     country, year 
NULLS LAST;

~~~

# GROUP BY ROLLUP (country, year) Result Set
~~~sql
COUNTRY    YEAR   SUM_OF_SALES
-------    -----  ------------
CANADA     2020   7500
CANADA     2024  16900
CANADA     NULL  24400 ⬅ **Subtotal**
USA        2020  23000
USA        2024  30000
USA        NULL  53000 ⬅ **Subtotal**
NULL       NULL  77400 ⬅ **Total**
~~~

-------
-------

# GROUP BY CUBE (country, year)

~~~sql
SELECT country, 
       city, 
       year, 
       sum(sales) as sum_of_sales
FROM 
     sales_table 
GROUP BY 
     CUBE (country, city, year)
ORDER BY 
     country, city, year 
NULLS LAST;
~~~

# GROUP BY CUBE (country, year) Result Set
~~~sql
COUNTRY   YEAR   SUM_OF_SALES
-------   ----   ------------
CANADA    2020   7500
CANADA    2024  16900
CANADA    NULL  24400  ⬅ **Subtotal**
USA       2020  23000
USA       2024  30000
USA       NULL  53000  ⬅ **Subtotal**
NULL      2020  30500  ⬅ **Subtotal**
NULL      2024  46900  ⬅ **Subtotal**
NULL      NULL  77400  ⬅ **Total**
~~~

------
------

# GROUP BY CUBE (country, city, year)

~~~sql
SELECT country, 
       city, 
       year, 
       sum(sales) as sum_of_sales
FROM 
     sales_table 
GROUP BY 
     CUBE (country, city, year)
ORDER BY 
     country, city, year 
NULLS LAST;
~~~

# GROUP BY CUBE (country, city, year) Result Set
~~~sql
COUNTRY   CITY       YEAR   SUM_OF_SALES
-------   ----       -----  ------------
CANADA    Ottawa     2020    6000
CANADA    Ottawa     2024   15000
CANADA    Ottawa     NULL   21000  ⬅ **Subtotal**
CANADA    Toronto    2020    1500
CANADA    Toronto    2024    1900
CANADA    Toronto    NULL    3400  ⬅ **Subtotal**
CANADA    NULL       2020    7500  ⬅ **Subtotal**
CANADA    NULL       2024   16900  ⬅ **Subtotal**
CANADA    NULL       NULL   24400  ⬅ **Subtotal**
USA       Cupertino  2020   18000
USA       Cupertino  2024   23000
USA       Cupertino  NULL   41000  ⬅ **Subtotal**
USA       Sunnyvale  2020    5000
USA       Sunnyvale  2024    7000
USA       Sunnyvale  NULL   12000  ⬅ **Subtotal**
USA       NULL       2020   23000  ⬅ **Subtotal**
USA       NULL       2024   30000  ⬅ **Subtotal**
USA       NULL       NULL   53000  ⬅ **Subtotal**
NULL      Cupertino  2020   18000  ⬅ **Subtotal**
NULL      Cupertino  2024   23000  ⬅ **Subtotal**
NULL      Cupertino  NULL   41000  ⬅ **Subtotal**
NULL      Ottawa     2020    6000  ⬅ **Subtotal**
NULL      Ottawa     2024   15000  ⬅ **Subtotal**
NULL      Ottawa     NULL   21000  ⬅ **Subtotal**
NULL      Sunnyvale  2020    5000  ⬅ **Subtotal**
NULL      Sunnyvale  2024    7000  ⬅ **Subtotal**
NULL      Sunnyvale  NULL   12000  ⬅ **Subtotal**
NULL      Toronto    2020    1500  ⬅ **Subtotal**
NULL      Toronto    2024    1900  ⬅ **Subtotal**
NULL      Toronto    NULL    3400  ⬅ **Subtotal**
NULL      NULL       2020    30500 ⬅ **Subtotal**
NULL      NULL       2024    46900 ⬅ **Subtotal**
NULL      NULL       NULL    77400 ⬅ **Total**
~~~