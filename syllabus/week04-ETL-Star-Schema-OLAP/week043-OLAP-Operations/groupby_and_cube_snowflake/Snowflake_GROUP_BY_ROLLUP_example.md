# GROUP BY ROLLUP

source: https://docs.snowflake.com/en/sql-reference/constructs/group-by-rollup

**GROUP BY ROLLUP** is an extension of the **GROUP BY**
clause that produces sub-total rows (in addition 
to the grouped rows). Sub-total rows are rows that 
further aggregate whose values are derived by computing 
the same aggregate functions that were used to produce 
the grouped rows.

You can think of rollup as generating multiple result sets, 
each of which (after the first) is the aggregate of the 
previous result set. So, for example, if you own a chain 
of retail stores, you might want to see the profit for:

* Each store.

* Each city (large cities might have multiple stores).

* Each state.

* Everything (all stores in all states).


You could create separate reports to get that information, 
but it is more efficient to scan the data once.

# Examples
Start by creating and loading a table with information 
about sales from a chain store that has branches in 
different cities and states/territories.

~~~sql
-- Create some tables and insert some rows.
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

Run a rollup query that shows profit by 
city, state, and total across all states.

The example below shows a query that has three “levels”:

* Each city.

* Each state.

* All revenue combined.

This example uses ORDER BY state, city NULLS LAST 
to ensure that each state’s rollup comes immediately 
after all of the cities in that state, and that the 
final rollup appears at the end of the output.

~~~sql
SELECT 
   state, 
   city, 
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
