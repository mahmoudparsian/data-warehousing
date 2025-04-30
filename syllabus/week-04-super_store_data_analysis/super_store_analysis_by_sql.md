# Super Store Orders Data Analysis

### 1. Given the following table: `super_store_orders`

### 2. Provide sql queries to analyze this data.

### 3. Use sub-queries and ranking functions.

### 4. Database: MySQL 

-------

# 1. Table Definition

~~~sql
-- -------------------------
-- Table: super_store_orders
-- -------------------------
CREATE TABLE super_store_orders (
    order_id VARCHAR(255),
    order_date DATE,
    ship_date DATE,
    ship_mode VARCHAR(255),
    customer_name VARCHAR(255),
    segment VARCHAR(255),
    state VARCHAR(255),
    country VARCHAR(255),
    market VARCHAR(255),
    region VARCHAR(255),
    product_id VARCHAR(255),
    category VARCHAR(255),
    sub_category VARCHAR(255),
    product_name VARCHAR(255),
    sales DECIMAL(10, 2),
    quantity INT,
    discount DECIMAL(5, 2),
    profit DECIMAL(10, 2),
    shipping_cost DECIMAL(10, 2),
    order_priority VARCHAR(255),
    year INT
);
~~~

# 2. Load CSV into Table

~~~sql
% mysql --local-infile=1 -hlocalhost -uroot -p

-- select the database:
use homeworks;

-- Uploading the file --
LOAD DATA LOCAL INFILE '<DIR>/super_store_orders.csv'
INTO TABLE super_store_orders
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS -- Skip header row 
(order_id, @order_date, @ship_date, ship_mode, customer_name, segment, state, country, market, region, product_id, category, sub_category, product_name, sales, quantity, discount, profit, shipping_cost, order_priority, year)
SET 
    order_date = STR_TO_DATE(@order_date, '%m/%d/%Y'),
    ship_date = STR_TO_DATE(@ship_date, '%m/%d/%Y');
~~~

# 3. Load Data

~~~sql

mysql> use homeworks;

Database changed
mysql> LOAD DATA LOCAL INFILE '<DIR>/super_store_orders.csv'
    -> INTO TABLE super_store_orders
    -> FIELDS TERMINATED BY ','
    -> ENCLOSED BY '"'
    -> LINES TERMINATED BY '\n'
    -> IGNORE 1 ROWS -- Skip header row
    -> (order_id, @order_date, @ship_date, ship_mode, customer_name, segment, state, country, market, region, product_id, category, sub_category, product_name, sales, quantity, discount, profit, shipping_cost, order_priority, year)
    -> SET
    ->     order_date = STR_TO_DATE(@order_date, '%m/%d/%Y'),
    ->     ship_date = STR_TO_DATE(@ship_date, '%m/%d/%Y');

Query OK, 51290 rows affected, 22702 warnings (1.18 sec)
Records: 51290  Deleted: 0  Skipped: 0  Warnings: 22702
~~~

# 4. Examine Table

~~~sql
mysql> desc super_store_orders;
+----------------+---------------+------+-----+---------+-------+
| Field          | Type          | Null | Key | Default | Extra |
+----------------+---------------+------+-----+---------+-------+
| order_id       | varchar(255)  | YES  |     | NULL    |       |
| order_date     | date          | YES  |     | NULL    |       |
| ship_date      | date          | YES  |     | NULL    |       |
| ship_mode      | varchar(255)  | YES  |     | NULL    |       |
| customer_name  | varchar(255)  | YES  |     | NULL    |       |
| segment        | varchar(255)  | YES  |     | NULL    |       |
| state          | varchar(255)  | YES  |     | NULL    |       |
| country        | varchar(255)  | YES  |     | NULL    |       |
| market         | varchar(255)  | YES  |     | NULL    |       |
| region         | varchar(255)  | YES  |     | NULL    |       |
| product_id     | varchar(255)  | YES  |     | NULL    |       |
| category       | varchar(255)  | YES  |     | NULL    |       |
| sub_category   | varchar(255)  | YES  |     | NULL    |       |
| product_name   | varchar(255)  | YES  |     | NULL    |       |
| sales          | decimal(10,2) | YES  |     | NULL    |       |
| quantity       | int           | YES  |     | NULL    |       |
| discount       | decimal(5,2)  | YES  |     | NULL    |       |
| profit         | decimal(10,2) | YES  |     | NULL    |       |
| shipping_cost  | decimal(10,2) | YES  |     | NULL    |       |
| order_priority | varchar(255)  | YES  |     | NULL    |       |
| year           | int           | YES  |     | NULL    |       |
+----------------+---------------+------+-----+---------+-------+
21 rows in set (0.02 sec)


mysql> select count(*) from super_store_orders;
+----------+
| count(*) |
+----------+
|    51290 |
+----------+
1 row in set (0.02 sec)

mysql> select * from super_store_orders limit 4;
+-----------------+------------+------------+----------------+-----------------+-------------+-----------------+-----------+--------+---------+------------------+-----------------+--------------+-----------------------------+--------+----------+----------+--------+---------------+----------------+------+
| order_id        | order_date | ship_date  | ship_mode      | customer_name   | segment     | state           | country   | market | region  | product_id       | category        | sub_category | product_name                | sales  | quantity | discount | profit | shipping_cost | order_priority | year |
+-----------------+------------+------------+----------------+-----------------+-------------+-----------------+-----------+--------+---------+------------------+-----------------+--------------+-----------------------------+--------+----------+----------+--------+---------------+----------------+------+
| AG-2011-2040    | 2011-01-01 | 2011-01-06 | Standard Class | Toby Braunhardt | Consumer    | Constantine     | Algeria   | Africa | Africa  | OFF-TEN-10000025 | Office Supplies | Storage      | Tenex Lockers, Blue         | 408.00 |        2 |     0.00 | 106.14 |         35.46 | Medium         | 2011 |
| IN-2011-47883   | 2011-01-01 | 2011-01-08 | Standard Class | Joseph Holt     | Consumer    | New South Wales | Australia | APAC   | Oceania | OFF-SU-10000618  | Office Supplies | Supplies     | Acme Trimmer, High Speed    | 120.00 |        3 |     0.10 |  36.04 |          9.72 | Medium         | 2011 |
| HU-2011-1220    | 2011-01-01 | 2011-01-05 | Second Class   | Annie Thurman   | Consumer    | Budapest        | Hungary   | EMEA   | EMEA    | OFF-TEN-10001585 | Office Supplies | Storage      | Tenex Box, Single Width     |  66.00 |        4 |     0.00 |  29.64 |          8.17 | High           | 2011 |
| IT-2011-3647632 | 2011-01-01 | 2011-01-05 | Second Class   | Eugene Moren    | Home Office | Stockholm       | Sweden    | EU     | North   | OFF-PA-10001492  | Office Supplies | Paper        | Enermax Note Cards, Premium |  45.00 |        3 |     0.50 | -26.06 |          4.82 | High           | 2011 |
+-----------------+------------+------------+----------------+-----------------+-------------+-----------------+-----------+--------+---------+------------------+-----------------+--------------+-----------------------------+--------+----------+----------+--------+---------------+----------------+------+
4 rows in set (0.00 sec)

~~~

------

# 5. Data Analysis: SQL Queries

### Query-1: Total Sales, Profit, and Quantity

~~~
SELECT
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    SUM(quantity) AS total_quantity
FROM 
    super_store_orders;

+-------------+--------------+----------------+
| total_sales | total_profit | total_quantity |
+-------------+--------------+----------------+
| 12642905.00 |   1469034.09 |         178312 |
+-------------+--------------+----------------+
1 row in set (0.04 sec)
~~~

------

### Query-2:  Average, Minimum, and Maximum Values for Sales, Profit, and Quantity

~~~sql
SELECT
    AVG(sales) AS average_sales,
    MIN(sales) AS min_sales,
    MAX(sales) AS max_sales,
    
    AVG(profit) AS average_profit,
    MIN(profit) AS min_profit,
    MAX(profit) AS max_profit,
    
    AVG(quantity) AS average_quantity,
    MIN(quantity) AS min_quantity,
    MAX(quantity) AS max_quantity
FROM 
    super_store_orders;
    
+---------------+-----------+-----------+----------------+------------+------------+------------------+--------------+--------------+
| average_sales | min_sales | max_sales | average_profit | min_profit | max_profit | average_quantity | min_quantity | max_quantity |
+---------------+-----------+-----------+----------------+------------+------------+------------------+--------------+--------------+
|    246.498440 |      0.00 |  22638.00 |      28.641725 |   -6599.98 |    8399.98 |           3.4765 |            1 |           14 |
+---------------+-----------+-----------+----------------+------------+------------+------------------+--------------+--------------+
1 row in set (0.07 sec)
~~~

-------

### Query-3:  Temporal Analysis - Sales, Profit, and Quantity Trends by Quarter

~~~sql
SELECT
    YEAR(order_date) AS order_year,
    QUARTER(order_date) AS order_quarter,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    SUM(quantity) AS total_quantity
FROM 
    super_store_orders
GROUP BY 
    order_year, order_quarter
ORDER BY 
    order_year, order_quarter;
    
+------------+---------------+-------------+--------------+----------------+
| order_year | order_quarter | total_sales | total_profit | total_quantity |
+------------+---------------+-------------+--------------+----------------+
|       2011 |             1 |   335780.00 |     36043.19 |           4523 |
|       2011 |             2 |   478903.00 |     48501.29 |           7145 |
|       2011 |             3 |   613318.00 |     65075.52 |           8516 |
|       2011 |             4 |   831510.00 |     99320.41 |          11259 |
|       2012 |             1 |   399388.00 |     43394.57 |           5555 |
|       2012 |             2 |   625611.00 |     81650.78 |           8842 |
|       2012 |             3 |   737795.00 |     86935.60 |          10344 |
|       2012 |             4 |   914699.00 |     95434.35 |          13370 |
|       2013 |             1 |   565035.00 |     75584.39 |           7201 |
|       2013 |             2 |   834873.00 |     93435.98 |          11823 |
|       2013 |             3 |   933057.00 |     98792.92 |          13979 |
|       2013 |             4 |  1072895.00 |    140699.09 |          15133 |
|       2014 |             1 |   689225.00 |     85110.23 |           9326 |
|       2014 |             2 |   933028.00 |    101514.49 |          13903 |
|       2014 |             3 |  1196537.00 |    149558.31 |          16298 |
|       2014 |             4 |  1481251.00 |    167982.97 |          21095 |
+------------+---------------+-------------+--------------+----------------+
16 rows in set (0.07 sec)
~~~

------

### Query-4:  Identify Top Sales Quarter for Each Year

~~~sql
WITH Ranked_Quarters AS (
    SELECT
        YEAR(order_date) AS order_year,
        QUARTER(order_date) AS order_quarter,
        SUM(sales) AS total_sales,
        RANK() OVER (PARTITION BY YEAR(order_date) ORDER BY SUM(sales) DESC) AS sales_rank
    FROM super_store_orders
    GROUP BY order_year, order_quarter
)
SELECT
    order_year,
    order_quarter,
    total_sales 
FROM Ranked_Quarters
WHERE sales_rank = 1;
+------------+---------------+-------------+
| order_year | order_quarter | total_sales |
+------------+---------------+-------------+
|       2011 |             4 |  831510.00  |
|       2012 |             4 |  914699.00  |
|       2013 |             4 | 1072895.00  |
|       2014 |             4 | 1481251.00  |
+------------+---------------+-------------+
4 rows in set (0.06 sec)
~~~

------

### Query-5.1:  Top-3 Selling Categories and Sub-Categories
~~~sql
SELECT
    category,
    sub_category,
    SUM(sales) AS total_sales
FROM 
    super_store_orders
GROUP BY 
    category, sub_category
ORDER BY 
    total_sales DESC
LIMIT 3;

+------------+--------------+-------------+
| category   | sub_category | total_sales |
+------------+--------------+-------------+
| Technology | Phones       |  1706874.00 |
| Technology | Copiers      |  1509439.00 |
| Furniture  | Chairs       |  1501682.00 |
+------------+--------------+-------------+
3 rows in set (0.11 sec)
~~~

### Query-5.2:  Top-Selling Categories and Sub-Categories

~~~sql
SELECT
    category,
    sub_category,
    SUM(sales) AS total_sales
FROM 
    super_store_orders
GROUP BY 
    category, sub_category
ORDER BY 
    total_sales DESC;
    
+-----------------+--------------+-------------+
| category        | sub_category | total_sales |
+-----------------+--------------+-------------+
| Technology      | Phones       |  1706874.00 |
| Technology      | Copiers      |  1509439.00 |
| Furniture       | Chairs       |  1501682.00 |
| Furniture       | Bookcases    |  1466559.00 |
| Office Supplies | Storage      |  1127124.00 |
| Office Supplies | Appliances   |  1011081.00 |
| Technology      | Machines     |   779071.00 |
| Furniture       | Tables       |   757034.00 |
| Technology      | Accessories  |   749307.00 |
| Office Supplies | Binders      |   461952.00 |
| Furniture       | Furnishings  |   385609.00 |
| Office Supplies | Art          |   372163.00 |
| Office Supplies | Paper        |   244307.00 |
| Office Supplies | Supplies     |   243090.00 |
| Office Supplies | Envelopes    |   170926.00 |
| Office Supplies | Fasteners    |    83254.00 |
| Office Supplies | Labels       |    73433.00 |
+-----------------+--------------+-------------+
17 rows in set (0.10 sec)
~~~

------

### Query-6:  Most Profitable Categories and Sub-Categories

~~~sql
SELECT
    category,
    sub_category,
    SUM(profit) AS total_profit
FROM 
    super_store_orders
GROUP BY 
    category, sub_category
ORDER BY 
    total_profit DESC;
    
+-----------------+--------------+--------------+
| category        | sub_category | total_profit |
+-----------------+--------------+--------------+
| Technology      | Copiers      |    258567.62 |
| Technology      | Phones       |    216717.49 |
| Furniture       | Bookcases    |    161924.32 |
| Furniture       | Chairs       |    141973.78 |
| Office Supplies | Appliances   |    141680.65 |
| Technology      | Accessories  |    129626.44 |
| Office Supplies | Storage      |    108461.74 |
| Office Supplies | Binders      |     72449.60 |
| Office Supplies | Paper        |     59207.25 |
| Technology      | Machines     |     58867.70 |
| Office Supplies | Art          |     57953.92 |
| Furniture       | Furnishings  |     46967.55 |
| Office Supplies | Envelopes    |     29600.85 |
| Office Supplies | Supplies     |     22583.13 |
| Office Supplies | Labels       |     15010.35 |
| Office Supplies | Fasteners    |     11525.25 |
| Furniture       | Tables       |    -64083.55 |
+-----------------+--------------+--------------+
17 rows in set (0.08 sec)
~~~

---------

### Query-7:  Sales and Profit by Region

~~~sql
SELECT
    region,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit
FROM 
    super_store_orders
GROUP BY 
    region
ORDER BY 
    total_profit DESC;
    
+----------------+-------------+--------------+
| region         | total_sales | total_profit |
+----------------+-------------+--------------+
| Central        |  2822399.00 |    311403.75 |
| North          |  1248192.00 |    194597.41 |
| North Asia     |   848349.00 |    165578.17 |
| South          |  1600960.00 |    140355.94 |
| Central Asia   |   752839.00 |    132479.89 |
| Oceania        |  1100207.00 |    121667.17 |
| West           |   725514.00 |    108418.79 |
| East           |   678834.00 |     91522.84 |
| Africa         |   783776.00 |     88871.13 |
| EMEA           |   806184.00 |     43897.90 |
| Caribbean      |   324281.00 |     34571.35 |
| Southeast Asia |   884438.00 |     17852.36 |
| Canada         |    66932.00 |     17817.39 |
+----------------+-------------+--------------+
13 rows in set (0.07 sec)
~~~

--------


### Query-8: Most Valuable Customer Segments

~~~sql
SELECT
    segment,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit
FROM super_store_orders
GROUP BY segment
ORDER BY total_profit DESC;

+-------------+-------------+--------------+
| segment     | total_sales | total_profit |
+-------------+-------------+--------------+
| Consumer    |  6508141.00 |    749239.18 |
| Corporate   |  3824808.00 |    442785.63 |
| Home Office |  2309956.00 |    277009.28 |
+-------------+-------------+--------------+
3 rows in set (0.07 sec)
~~~

-----


### Query-9:  Most (top-10) Profitable and Top-Selling Products

~~~sql
SELECT
    product_name,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit
FROM super_store_orders
GROUP BY product_name
ORDER BY total_profit DESC, 
         total_sales DESC
LIMIT 10;

+----------------------------------------------------------+-------------+--------------+
| product_name                                             | total_sales | total_profit |
+----------------------------------------------------------+-------------+--------------+
| Canon imageCLASS 2200 Advanced Copier                    |    61600.00 |     25199.94 |
| Cisco Smart Phone, Full Size                             |    76441.00 |     17238.52 |
| Motorola Smart Phone, Full Size                          |    73159.00 |     17027.14 |
| Hoover Stove, Red                                        |    31664.00 |     11807.96 |
| Sauder Classic Bookcase, Traditional                     |    39110.00 |     10672.06 |
| Harbour Creations Executive Leather Armchair, Adjustable |    50120.00 |     10427.33 |
| Nokia Smart Phone, Full Size                             |    71904.00 |      9938.16 |
| Cisco Smart Phone, with Caller ID                        |    43124.00 |      9786.65 |
| Nokia Smart Phone, with Caller ID                        |    47880.00 |      9465.34 |
| Belkin Router, USB                                       |    23473.00 |      8955.01 |
+----------------------------------------------------------+-------------+--------------+
10 rows in set (0.09 sec)
~~~

------

### Query-10:  Impact of Discounts on Sales and Profit

~~~sql
SELECT
    discount,
    AVG(sales) AS average_sales,
    AVG(profit) AS average_profit
FROM super_store_orders
GROUP BY discount
ORDER BY discount DESC;

+----------+---------------+----------------+
| discount | average_sales | average_profit |
+----------+---------------+----------------+
|     0.85 |    398.500000 |   -1534.330000 |
|     0.80 |     64.753165 |    -122.203513 |
|     0.70 |     78.258679 |    -104.339955 |
|     0.65 |    387.058824 |    -365.998824 |
|     0.60 |     93.426811 |     -83.223356 |
|     0.57 |    678.666667 |    -526.129167 |
|     0.55 |    630.800000 |    -315.068000 |
|     0.50 |    198.496632 |     -97.141451 |
|     0.47 |    115.078621 |     -42.982400 |
|     0.45 |    102.131498 |     -41.611437 |
|     0.40 |    180.827187 |     -47.296236 |
|     0.37 |    427.229730 |     -78.461892 |
|     0.35 |    784.459016 |    -116.144754 |
|     0.32 |    536.703704 |     -88.561481 |
|     0.30 |    555.626471 |     -57.899735 |
|     0.27 |    230.286082 |      -4.317268 |
|     0.25 |    444.762626 |       4.043687 |
|     0.20 |    242.125025 |      23.243018 |
|     0.17 |    336.604082 |      38.317184 |
|     0.15 |    565.687616 |      50.602736 |
|     0.10 |    388.303343 |      64.071433 |
|     0.07 |    810.800000 |     140.990133 |
|     0.00 |    246.153003 |      62.051992 |
+----------+---------------+----------------+
23 rows in set (0.06 sec)
~~~

------


### Query-11:  Shipping Costs and Their Impact on Profit

~~~sql
SELECT
    ship_mode,
    AVG(shipping_cost) AS avg_shipping_cost,
    AVG(profit) AS average_profit
FROM super_store_orders
GROUP BY ship_mode
ORDER BY avg_shipping_cost DESC;

+----------------+-------------------+----------------+
| ship_mode      | avg_shipping_cost | average_profit |
+----------------+-------------------+----------------+
| Same Day       |         42.937453 |      28.201862 |
| First Class    |         41.053065 |      27.728798 |
| Second Class   |         30.469747 |      28.534334 |
| Standard Class |         19.971755 |      28.938937 |
+----------------+-------------------+----------------+
4 rows in set (0.08 sec)
~~~

-----

### Query-12:  Distribution of Order Priorities

~~~sql
SELECT
    order_priority,
    AVG(sales) AS avg_sales,
    AVG(profit) AS avg_profit,
    COUNT(distinct order_id) AS order_count
FROM super_store_orders
GROUP BY order_priority
ORDER BY order_priority;

+----------------+------------+------------+-------------+
| order_priority | avg_sales  | avg_profit | order_count |
+----------------+------------+------------+-------------+
| Critical       | 250.828586 |  31.994351 |        1967 |
| High           | 245.642152 |  27.119087 |        7767 |
| Low            | 234.258663 |  24.197970 |        1212 |
| Medium         | 247.378962 |  29.361718 |       14484 |
+----------------+------------+------------+-------------+
4 rows in set (0.17 sec)
~~~

-----


### Query-13:  Top-10 Customers Based on Total Sales

~~~sql
SELECT
    customer_name,
    SUM(sales) AS total_sales
FROM super_store_orders
GROUP BY customer_name
ORDER BY total_sales DESC
LIMIT 10; 

+--------------------+-------------+
| customer_name      | total_sales |
+--------------------+-------------+
| Tom Ashbrook       |    40489.00 |
| Tamara Chand       |    37453.00 |
| Greg Tran          |    35552.00 |
| Christopher Conant |    35187.00 |
| Sean Miller        |    35170.00 |
| Bart Watters       |    32315.00 |
| Natalie Fritzler   |    31778.00 |
| Fred Hopkins       |    30404.00 |
| Jane Waco          |    30288.00 |
| Hunter Lopez       |    30246.00 |
+--------------------+-------------+
10 rows in set (0.06 sec)
~~~

-----

### Query-14:  Top-10 Customers Based on Total Profit


~~~sql
SELECT
    customer_name,
    SUM(profit) AS total_profit
FROM super_store_orders
GROUP BY customer_name
ORDER BY total_profit DESC
LIMIT 10; 
-- Adjust the limit as needed

+-----------------+--------------+
| customer_name   | total_profit |
+-----------------+--------------+
| Tamara Chand    |      8672.90 |
| Raymond Buch    |      8453.05 |
| Sanjit Chand    |      8205.37 |
| Hunter Lopez    |      7816.57 |
| Bill Eplett     |      7410.01 |
| Harry Marie     |      6958.26 |
| Susan Pistek    |      6484.41 |
| Mike Gockenbach |      6458.64 |
| Adrian Barton   |      6417.27 |
| Tom Ashbrook    |      6312.01 |
+-----------------+--------------+
10 rows in set (0.07 sec)
~~~

-----


### Query-15:  Analyze Customer Buying Patterns

~~~sql
SELECT
    customer_name,
    COUNT(DISTINCT order_id) AS total_orders,
    AVG(sales) AS average_sales_per_order
FROM super_store_orders
GROUP BY customer_name
ORDER BY total_orders DESC
LIMIT 10;

+------------------+--------------+-------------------------+
| customer_name    | total_orders | average_sales_per_order |
+------------------+--------------+-------------------------+
| Frank Olsen      |           47 |              209.117647 |
| Anna Andreadi    |           47 |              190.241758 |
| Michael Paige    |           47 |              189.319149 |
| Laura Armstrong  |           46 |              324.000000 |
| Kristen Hastings |           46 |              225.636364 |
| Sara Luxemburg   |           46 |              205.207317 |
| Anthony Rawles   |           45 |              240.819444 |
| Eric Murdock     |           45 |              280.850000 |
| Gary Hansen      |           45 |              200.907895 |
| Bart Watters     |           45 |              336.614583 |
+------------------+--------------+-------------------------+
10 rows in set (0.11 sec)
~~~

-----


### Query-16:  Calculating RFM: top-10 by SUM(sales)

~~~sql
--
-- RFM analysis, or Recency, Frequency, Monetary value analysis
--
SELECT
    customer_name,
    DATEDIFF('2015-01-30', MAX(order_date)) AS recency,
    COUNT(DISTINCT order_id) AS frequency,
    SUM(sales) AS monetary_value
FROM
    super_store_orders
GROUP BY
    customer_name
ORDER BY 
    monetary_value DESC
LIMIT 10;

+--------------------+---------+-----------+----------------+
| customer_name      | recency | frequency | monetary_value |
+--------------------+---------+-----------+----------------+
| Tom Ashbrook       |      38 |        30 |       40489.00 |
| Tamara Chand       |      57 |        36 |       37453.00 |
| Greg Tran          |      38 |        34 |       35552.00 |
| Christopher Conant |      36 |        39 |       35187.00 |
| Sean Miller        |      51 |        28 |       35170.00 |
| Bart Watters       |      84 |        45 |       32315.00 |
| Natalie Fritzler   |      31 |        43 |       31778.00 |
| Fred Hopkins       |      31 |        39 |       30404.00 |
| Jane Waco          |      42 |        40 |       30288.00 |
| Hunter Lopez       |      60 |        24 |       30246.00 |
+--------------------+---------+-----------+----------------+
10 rows in set (0.11 sec)
~~~

-----

### Query-17:  Use NTILE() function   

~~~sql
SELECT
    customer_name,
    NTILE(4) OVER (ORDER BY DATEDIFF('2015-01-30', MAX(order_date))) AS rfm_recency,
    NTILE(4) OVER (ORDER BY COUNT(DISTINCT order_id)) AS rfm_frequency,
    NTILE(4) OVER (ORDER BY SUM(sales)) AS rfm_monetary
FROM
    super_store_orders
GROUP BY
    customer_name;
~~~
    

### Query-18: Top 5 products by total sales

Use a subquery + `ROW_NUMBER()` to grab the top 5 overall products.  

~~~sql
   WITH product_sales AS (
     SELECT
       product_id,
       product_name,
       SUM(sales) AS total_sales
     FROM super_store_orders
     GROUP BY product_id, product_name
   )
   SELECT product_id, product_name, total_sales
   FROM (
     SELECT
       ps.*,
       ROW_NUMBER() OVER (ORDER BY total_sales DESC) AS rn
     FROM product_sales ps
   ) t
   WHERE rn <= 5;
 
   
+-----------------+-----------------------------------------------------------------------------+-------------+
| product_id      | product_name                                                                | total_sales |
+-----------------+-----------------------------------------------------------------------------+-------------+
| TEC-CO-10004722 | Canon imageCLASS 2200 Advanced Copier                                       |    61600.00 |
| TEC-PH-10004664 | Nokia Smart Phone, with Caller ID                                           |    30042.00 |
| OFF-BI-10003527 | Fellowes PB500 Electric Punch Plastic Comb Binding Machine with Manual Bind |    27454.00 |
| TEC-MA-10002412 | Cisco TelePresence System EX90 Videoconferencing Unit                       |    22638.00 |
| TEC-PH-10004823 | Nokia Smart Phone, Full Size                                                |    22261.00 |
+-----------------+-----------------------------------------------------------------------------+-------------+
5 rows in set (0.13 sec)
~~~

-----


### Query-19: Top 3 products per category
   Partition by category and pick top 3 in each.  

~~~sql
   SELECT *
   FROM (
     SELECT
       product_id, product_name, category,
       SUM(sales) AS cat_sales,
       ROW_NUMBER() OVER (PARTITION BY category ORDER BY SUM(sales) DESC) AS rn
     FROM super_store_orders
     GROUP BY category, product_id, product_name
   ) x
   WHERE rn <= 3;
   
+-----------------+-----------------------------------------------------------------------------+-----------------+-----------+----+
| product_id      | product_name                                                                | category        | cat_sales | rn |
+-----------------+-----------------------------------------------------------------------------+-----------------+-----------+----+
| FUR-CH-10002024 | HON 5400 Series Task Chairs for Big and Tall                                | Furniture       |  21870.00 |  1 |
| FUR-CH-10000027 | SAFCO Executive Leather Armchair, Black                                     | Furniture       |  21329.00 |  2 |
| FUR-BO-10004679 | Safco Library with Doors, Pine                                              | Furniture       |  17433.00 |  3 |
| OFF-BI-10003527 | Fellowes PB500 Electric Punch Plastic Comb Binding Machine with Manual Bind | Office Supplies |  27454.00 |  1 |
| OFF-AP-10004512 | Hoover Stove, Red                                                           | Office Supplies |  21148.00 |  2 |
| OFF-BI-10001359 | GBC DocuBind TL300 Electric Binding System                                  | Office Supplies |  19824.00 |  3 |
| TEC-CO-10004722 | Canon imageCLASS 2200 Advanced Copier                                       | Technology      |  61600.00 |  1 |
| TEC-PH-10004664 | Nokia Smart Phone, with Caller ID                                           | Technology      |  30042.00 |  2 |
| TEC-MA-10002412 | Cisco TelePresence System EX90 Videoconferencing Unit                       | Technology      |  22638.00 |  3 |
+-----------------+-----------------------------------------------------------------------------+-----------------+-----------+----+
9 rows in set (0.14 sec)
~~~

#### Rewrite as a sub-query:

~~~sql
with ranked as
(   SELECT
       product_id, product_name, category,
       SUM(sales) AS cat_sales,
       ROW_NUMBER() OVER (PARTITION BY category ORDER BY SUM(sales) DESC) AS rn
     FROM super_store_orders
     GROUP BY product_id, product_name, category
)
SELECT *
   FROM ranked
   WHERE rn <= 3;

+-----------------+-----------------------------------------------------------------------------+-----------------+-----------+----+
| product_id      | product_name                                                                | category        | cat_sales | rn |
+-----------------+-----------------------------------------------------------------------------+-----------------+-----------+----+
| FUR-CH-10002024 | HON 5400 Series Task Chairs for Big and Tall                                | Furniture       |  21870.00 |  1 |
| FUR-CH-10000027 | SAFCO Executive Leather Armchair, Black                                     | Furniture       |  21329.00 |  2 |
| FUR-BO-10004679 | Safco Library with Doors, Pine                                              | Furniture       |  17433.00 |  3 |
| OFF-BI-10003527 | Fellowes PB500 Electric Punch Plastic Comb Binding Machine with Manual Bind | Office Supplies |  27454.00 |  1 |
| OFF-AP-10004512 | Hoover Stove, Red                                                           | Office Supplies |  21148.00 |  2 |
| OFF-BI-10001359 | GBC DocuBind TL300 Electric Binding System                                  | Office Supplies |  19824.00 |  3 |
| TEC-CO-10004722 | Canon imageCLASS 2200 Advanced Copier                                       | Technology      |  61600.00 |  1 |
| TEC-PH-10004664 | Nokia Smart Phone, with Caller ID                                           | Technology      |  30042.00 |  2 |
| TEC-MA-10002412 | Cisco TelePresence System EX90 Videoconferencing Unit                       | Technology      |  22638.00 |  3 |
+-----------------+-----------------------------------------------------------------------------+-----------------+-----------+----+
9 rows in set (0.19 sec)

~~~
------


### Query-20: Rank states by total profit, showing only top 10**  

~~~sql
   SELECT state, total_profit
   FROM (
     SELECT
       state,
       SUM(profit) AS total_profit,
       RANK() OVER (ORDER BY SUM(profit) DESC) AS profit_rank
     FROM super_store_orders
     GROUP BY state
   ) s
   WHERE profit_rank <= 10;
   
+------------------------+--------------+
| state                  | total_profit |
+------------------------+--------------+
| England                |     99907.60 |
| California             |     76381.60 |
| New York               |     74038.64 |
| New South Wales        |     45273.70 |
| Ile-de-France          |     44056.03 |
| North Rhine-Westphalia |     42347.93 |
| San Salvador           |     35883.38 |
| Washington             |     33402.70 |
| Michigan               |     24463.15 |
| São Paulo              |     21878.02 |
+------------------------+--------------+
10 rows in set (0.07 sec)
~~~

-----

### Query-21: Quartiles of customers by total sales**  

~~~sql
   SELECT customer_name, 
          total_sales,
          NTILE(4) OVER (ORDER BY total_sales DESC) AS sales_quartile
   FROM (
     SELECT customer_name, 
            SUM(sales) AS total_sales
     FROM super_store_orders
     GROUP BY customer_name
   ) c;
   
+------------------------+-------------+----------------+
| customer_name          | total_sales | sales_quartile |
+------------------------+-------------+----------------+
| Tom Ashbrook           |    40489.00 |              1 |
| Tamara Chand           |    37453.00 |              1 |
| Greg Tran              |    35552.00 |              1 |
| Christopher Conant     |    35187.00 |              1 |
| Sean Miller            |    35170.00 |              1 |
...
| Karen Seio             |     5325.00 |              4 |
| Catherine Glotzbach    |     4116.00 |              4 |
| Vivian Mathis          |     3891.00 |              4 |
+------------------------+-------------+----------------+
795 rows in set (0.07 sec)
~~~

-----


### Query-22: Second-highest single order sale amount**  

~~~sql
   SELECT DISTINCT order_id, order_sale
   FROM (
     SELECT
       order_id,
       SUM(sales) AS order_sale,
       DENSE_RANK() OVER (ORDER BY SUM(sales) DESC) AS dr
     FROM super_store_orders
     GROUP BY order_id
   ) t
   WHERE dr = 2;
   
+----------------+------------+
| order_id       | order_sale |
+----------------+------------+
| CA-2013-118689 |   18336.00 |
+----------------+------------+
1 row in set (0.13 sec)
~~~

-----

### Query-23: Top-10 Orders above average quantity per sub-category**  

~~~sql
with averages as
(
  SELECT sub_category,
         AVG(quantity) as avg_quantity
     FROM super_store_orders
     GROUP BY sub_category
)
SELECT *
FROM super_store_orders s,
     averages a
WHERE s.sub_category = a.sub_category AND
      s.quantity > a.avg_quantity
ORDER BY s.quantity
LIMIT 10;

+-----------------+------------+------------+----------------+------------------+-------------+--------------+----------------+--------+---------+------------------+-----------------+--------------+----------------------------------------------+--------+----------+----------+--------+---------------+----------------+------+--------------+--------------+
| order_id        | order_date | ship_date  | ship_mode      | customer_name    | segment     | state        | country        | market | region  | product_id       | category        | sub_category | product_name                                 | sales  | quantity | discount | profit | shipping_cost | order_priority | year | sub_category | avg_quantity |
+-----------------+------------+------------+----------------+------------------+-------------+--------------+----------------+--------+---------+------------------+-----------------+--------------+----------------------------------------------+--------+----------+----------+--------+---------------+----------------+------+--------------+--------------+
| IT-2014-4273010 | 2014-09-27 | 2014-09-29 | First Class    | Katrina Bavinger | Home Office | Dublin       | Ireland        | EU     | North   | OFF-EN-10001202  | Office Supplies | Envelopes    | Kraft Clasp Envelope, with clear poly window |  25.00 |        4 |     0.50 |  -1.08 |          6.17 | Critical       | 2014 | Envelopes    |       3.4415 |
| IN-2013-22109   | 2013-03-04 | 2013-03-08 | Standard Class | David Wiener     | Corporate   | Queensland   | Australia      | APAC   | Oceania | OFF-EN-10000615  | Office Supplies | Envelopes    | Jiffy Mailers, Security-Tint                 | 142.00 |        4 |     0.10 |   3.13 |         24.65 | High           | 2013 | Envelopes    |       3.4415 |
| MX-2014-165841  | 2014-01-30 | 2014-02-04 | Standard Class | Toby Gnade       | Consumer    | San Salvador | El Salvador    | LATAM  | Central | OFF-EN-10000532  | Office Supplies | Envelopes    | Cameo Clasp Envelope, Set of 50              |  25.00 |        4 |     0.00 |  12.16 |          2.32 | Medium         | 2014 | Envelopes    |       3.4415 |
| ES-2014-2349858 | 2014-02-01 | 2014-02-06 | Standard Class | Lynn Smith       | Consumer    | England      | United Kingdom | EU     | North   | OFF-EN-10000271  | Office Supplies | Envelopes    | Kraft Peel and Seal, with clear poly window  |  96.00 |        4 |     0.00 |  25.92 |          2.13 | Medium         | 2014 | Envelopes    |       3.4415 |
| PL-2014-3190    | 2014-02-23 | 2014-02-25 | First Class    | Karl Braun       | Consumer    | Silesia      | Poland         | EMEA   | EMEA    | OFF-CAM-10004271 | Office Supplies | Envelopes    | Cameo Mailers, Recycled                      | 148.00 |        4 |     0.00 |  33.96 |         54.45 | Critical       | 2014 | Envelopes    |       3.4415 |
| ID-2014-80300   | 2014-02-24 | 2014-02-25 | First Class    | Katrina Edelman  | Corporate   | Queensland   | Australia      | APAC   | Oceania | OFF-EN-10003176  | Office Supplies | Envelopes    | Cameo Manila Envelope, Set of 50             |  65.00 |        4 |     0.40 |  -6.48 |         29.04 | Critical       | 2014 | Envelopes    |       3.4415 |
| ES-2014-1833179 | 2014-02-25 | 2014-03-02 | Standard Class | Phillip Breyer   | Corporate   | England      | United Kingdom | EU     | North   | OFF-EN-10004150  | Office Supplies | Envelopes    | GlobeWeis Business Envelopes, Recycled       |  65.00 |        4 |     0.00 |  28.32 |          6.55 | High           | 2014 | Envelopes    |       3.4415 |
| KZ-2014-660     | 2014-03-03 | 2014-03-05 | First Class    | Stefania Perrino | Corporate   | Almaty City  | Kazakhstan     | EMEA   | EMEA    | OFF-JIF-10004450 | Office Supplies | Envelopes    | Jiffy Mailers, Recycled                      |  43.00 |        4 |     0.70 | -72.04 |          9.64 | Medium         | 2014 | Envelopes    |       3.4415 |
| MX-2014-146955  | 2014-03-04 | 2014-03-04 | Same Day       | Jennifer Braxton | Corporate   | Coahuila     | Mexico         | LATAM  | North   | OFF-EN-10002122  | Office Supplies | Envelopes    | Jiffy Mailers, with clear poly window        | 109.00 |        4 |     0.00 |  24.96 |         45.22 | Critical       | 2014 | Envelopes    |       3.4415 |
| CA-2014-161046  | 2014-03-06 | 2014-03-06 | Same Day       | Claudia Bergmann | Corporate   | Mississippi  | United States  | US     | South   | OFF-EN-10003862  | Office Supplies | Envelopes    | Laser & Ink Jet Business Envelopes           |  43.00 |        4 |     0.00 |  19.63 |          5.54 | Medium         | 2014 | Envelopes    |       3.4415 |
+-----------------+------------+------------+----------------+------------------+-------------+--------------+----------------+--------+---------+------------------+-----------------+--------------+----------------------------------------------+--------+----------+----------+--------+---------------+----------------+------+--------------+--------------+
10 rows in set (0.38 sec)
~~~

-----


### Query-24: Cumulative sales by month within each year**  

~~~sql
   SELECT
     year,
     DATE_FORMAT(order_date, '%Y-%m')  AS ym,
     SUM(sales) AS month_sales,
     SUM(SUM(sales)) OVER (PARTITION BY year ORDER BY DATE_FORMAT(order_date, '%Y-%m')) AS cum_sales
   FROM super_store_orders
   GROUP BY year, DATE_FORMAT(order_date, '%Y-%m')
   ORDER BY year, ym;
   
+------+---------+-------------+------------+
| year | ym      | month_sales | cum_sales  |
+------+---------+-------------+------------+
| 2011 | 2011-01 |    98902.00 |   98902.00 |
| 2011 | 2011-02 |    91152.00 |  190054.00 |
| 2011 | 2011-03 |   145726.00 |  335780.00 |
| 2011 | 2011-04 |   116927.00 |  452707.00 |
| 2011 | 2011-05 |   146762.00 |  599469.00 |
| 2011 | 2011-06 |   215214.00 |  814683.00 |
| 2011 | 2011-07 |   115518.00 |  930201.00 |
| 2011 | 2011-08 |   207570.00 | 1137771.00 |
| 2011 | 2011-09 |   290230.00 | 1428001.00 |
| 2011 | 2011-10 |   199070.00 | 1627071.00 |
| 2011 | 2011-11 |   298499.00 | 1925570.00 |
| 2011 | 2011-12 |   333941.00 | 2259511.00 |
| 2012 | 2012-01 |   135775.00 |  135775.00 |
| 2012 | 2012-02 |   100521.00 |  236296.00 |
| 2012 | 2012-03 |   163092.00 |  399388.00 |
| 2012 | 2012-04 |   161060.00 |  560448.00 |
| 2012 | 2012-05 |   208370.00 |  768818.00 |
| 2012 | 2012-06 |   256181.00 | 1024999.00 |
| 2012 | 2012-07 |   145247.00 | 1170246.00 |
| 2012 | 2012-08 |   303158.00 | 1473404.00 |
| 2012 | 2012-09 |   289390.00 | 1762794.00 |
| 2012 | 2012-10 |   252942.00 | 2015736.00 |
| 2012 | 2012-11 |   323512.00 | 2339248.00 |
| 2012 | 2012-12 |   338245.00 | 2677493.00 |
| 2013 | 2013-01 |   199197.00 |  199197.00 |
| 2013 | 2013-02 |   167247.00 |  366444.00 |
| 2013 | 2013-03 |   198591.00 |  565035.00 |
| 2013 | 2013-04 |   177835.00 |  742870.00 |
| 2013 | 2013-05 |   260525.00 | 1003395.00 |
| 2013 | 2013-06 |   396513.00 | 1399908.00 |
| 2013 | 2013-07 |   229940.00 | 1629848.00 |
| 2013 | 2013-08 |   326491.00 | 1956339.00 |
| 2013 | 2013-09 |   376626.00 | 2332965.00 |
| 2013 | 2013-10 |   293423.00 | 2626388.00 |
| 2013 | 2013-11 |   373996.00 | 3000384.00 |
| 2013 | 2013-12 |   405476.00 | 3405860.00 |
| 2014 | 2014-01 |   241267.00 |  241267.00 |
| 2014 | 2014-02 |   184848.00 |  426115.00 |
| 2014 | 2014-03 |   263110.00 |  689225.00 |
| 2014 | 2014-04 |   242781.00 |  932006.00 |
| 2014 | 2014-05 |   288404.00 | 1220410.00 |
| 2014 | 2014-06 |   401843.00 | 1622253.00 |
| 2014 | 2014-07 |   258718.00 | 1880971.00 |
| 2014 | 2014-08 |   456633.00 | 2337604.00 |
| 2014 | 2014-09 |   481186.00 | 2818790.00 |
| 2014 | 2014-10 |   422785.00 | 3241575.00 |
| 2014 | 2014-11 |   555312.00 | 3796887.00 |
| 2014 | 2014-12 |   503154.00 | 4300041.00 |
+------+---------+-------------+------------+
48 rows in set (0.08 sec)
~~~

-----

### Query-25: Top-2 shipping modes by average shipping_cost**  

~~~sql
   SELECT ship_mode, 
          avg_cost
   FROM (
     SELECT
       ship_mode,
       AVG(shipping_cost) AS avg_cost,
       ROW_NUMBER() OVER (ORDER BY AVG(shipping_cost) DESC) AS rn
     FROM super_store_orders
     GROUP BY ship_mode
   ) t
   WHERE rn <= 2;
   
+-------------+-----------+
| ship_mode   | avg_cost  |
+-------------+-----------+
| Same Day    | 42.937453 |
| First Class | 41.053065 |
+-------------+-----------+
2 rows in set (0.06 sec)

~~~

-----

### Query-26: Top 5 customers per region by sales**  

~~~sql
   SELECT region, 
          customer_name, 
          cust_sales
   FROM (
     SELECT
       region, 
       customer_name,
       SUM(sales) AS cust_sales,
       ROW_NUMBER() OVER (PARTITION BY region ORDER BY SUM(sales) DESC) AS rn
     FROM super_store_orders
     GROUP BY region, customer_name
   ) x
   WHERE rn <= 5;
  
+----------------+--------------------+------------+
| region         | customer_name      | cust_sales |
+----------------+--------------------+------------+
| Africa         | Barry Weirich      |    8957.00 |
| Africa         | Liz Thompson       |    7853.00 |
| Africa         | Phillina Ober      |    7799.00 |
| Africa         | Jennifer Ferguson  |    6470.00 |
| Africa         | Jane Waco          |    6173.00 |
| Canada         | Stuart Van         |    4009.00 |
| Canada         | Dianna Wilson      |    2469.00 |
| Canada         | Jim Karlsson       |    2264.00 |
| Canada         | Bart Folk          |    2183.00 |
| Canada         | Dan Campbell       |    2091.00 |
| Caribbean      | Frank Merwin       |    4656.00 |
| Caribbean      | Dorothy Wardle     |    4252.00 |
| Caribbean      | Larry Hughes       |    4016.00 |
| Caribbean      | Art Ferguson       |    3980.00 |
| Caribbean      | Jason Fortune-     |    3923.00 |
| Central        | Tamara Chand       |   27345.00 |
| Central        | Sanjit Chand       |   15673.00 |
| Central        | Adrian Barton      |   14258.00 |
| Central        | Harry Greene       |   14207.00 |
| Central        | Becky Martin       |   13353.00 |
| Central Asia   | Cynthia Arntzen    |   10462.00 |
| Central Asia   | Vivek Grady        |   10058.00 |
| Central Asia   | Barry Franz        |    9365.00 |
| Central Asia   | Stefania Perrino   |    7894.00 |
| Central Asia   | Laurel Beltran     |    7798.00 |
| East           | Tom Ashbrook       |   13724.00 |
| East           | Hunter Lopez       |   10523.00 |
| East           | Bill Shonely       |   10022.00 |
| East           | Greg Tran          |    9384.00 |
| East           | Seth Vernon        |    9217.00 |
| EMEA           | Sally Hughsby      |    7537.00 |
| EMEA           | Michael Dominguez  |    6855.00 |
| EMEA           | Pauline Johnson    |    5990.00 |
| EMEA           | Christopher Conant |    5544.00 |
| EMEA           | Tim Brockman       |    5314.00 |
| North          | Fred Hopkins       |   11122.00 |
| North          | James Galang       |    9772.00 |
| North          | Eric Murdock       |    9023.00 |
| North          | Bart Watters       |    8437.00 |
| North          | Greg Tran          |    8033.00 |
| North Asia     | Carol Adams        |    9055.00 |
| North Asia     | Dean percer        |    8976.00 |
| North Asia     | Cari Sayre         |    8936.00 |
| North Asia     | Paul Lucas         |    7919.00 |
| North Asia     | Phillip Breyer     |    7436.00 |
| Oceania        | Dave Poirier       |   11865.00 |
| Oceania        | Eric Murdock       |    8464.00 |
| Oceania        | Sean Christensen   |    8328.00 |
| Oceania        | George Bell        |    7661.00 |
| Oceania        | Peter Fuller       |    7650.00 |
| South          | Sean Miller        |   23778.00 |
| South          | Sanjit Engle       |   12783.00 |
| South          | Maria Etezadi      |   10145.00 |
| South          | Patrick Jones      |    9681.00 |
| South          | Saphhira Shifley   |    9543.00 |
| Southeast Asia | Steve Chapman      |    7991.00 |
| Southeast Asia | Evan Minnotte      |    7194.00 |
| Southeast Asia | Anne McFarland     |    7116.00 |
| Southeast Asia | Dorris liebe       |    6786.00 |
| Southeast Asia | Joe Kamberova      |    6784.00 |
| West           | Raymond Buch       |   14345.00 |
| West           | Ken Lonsdale       |    8473.00 |
| West           | Edward Hooks       |    7448.00 |
| West           | Jane Waco          |    7393.00 |
| West           | Karen Ferguson     |    7183.00 |
+----------------+--------------------+------------+
65 rows in set (0.11 sec)
~~~

------

### Query-27: Customers in the top 10% by sales**  

~~~sql
    SELECT customer_name, 
           total_sales
    FROM (
      SELECT
        customer_name,
        SUM(sales) AS total_sales,
        CUME_DIST() OVER (ORDER BY SUM(sales)) AS cd
      FROM super_store_orders
      GROUP BY customer_name
    ) t
    WHERE cd >= 0.90;
   
+--------------------+-------------+
| customer_name      | total_sales |
+--------------------+-------------+
| Jason Fortune-     |    22817.00 |
| Dean percer        |    22833.00 |
| Randy Bradley      |    22898.00 |
| Lena Radford       |    22903.00 |
| Jennifer Ferguson  |    22947.00 |
| Ralph Arnett       |    23044.00 |
| Mitch Webber       |    23070.00 |
| Emily Grady        |    23114.00 |
| Juliana Krohn      |    23136.00 |
| Ben Ferrer         |    23219.00 |
| Mike Gockenbach    |    23378.00 |
| Steve Chapman      |    23401.00 |
| Eugene Moren       |    23411.00 |
| Dianna Wilson      |    23456.00 |
| Bill Shonely       |    23511.00 |
| Justin Deggeller   |    23618.00 |
| Jill Fjeld         |    23621.00 |
| Saphhira Shifley   |    23632.00 |
| Seth Vernon        |    23640.00 |
| Alan Hwang         |    23641.00 |
| David Philippe     |    23730.00 |
| Vivek Grady        |    23767.00 |
| Justin Hirsh       |    23918.00 |
| Theone Pippenger   |    23965.00 |
| Carol Adams        |    23993.00 |
| Joy Bell-          |    24011.00 |
| Karen Daniels      |    24018.00 |
| Patrick O'Donnell  |    24025.00 |
| Barry Franz        |    24082.00 |
| Ken Lonsdale       |    24127.00 |
| Mike Pelletier     |    24216.00 |
| Harry Greene       |    24217.00 |
| Phillip Breyer     |    24269.00 |
| Nathan Mautz       |    24278.00 |
| Tom Boeckenhauer   |    24480.00 |
| Gary Hwang         |    24629.00 |
| Aaron Bergman      |    24646.00 |
| Gary Zandusky      |    24700.00 |
| Rick Wilson        |    25125.00 |
| Adrian Barton      |    25125.00 |
| Christine Phan     |    25157.00 |
| Anne McFarland     |    25522.00 |
| Dave Brooks        |    25550.00 |
| Steven Ward        |    25669.00 |
| Dave Poirier       |    25901.00 |
| John Huston        |    25947.00 |
| John Lee           |    25979.00 |
| Brad Norvell       |    26200.00 |
| Maria Etezadi      |    26252.00 |
| Laurel Beltran     |    26387.00 |
| Keith Dawkins      |    26451.00 |
| Sanjit Chand       |    26524.00 |
| Joe Kamberova      |    26689.00 |
| Patrick O'Brill    |    26712.00 |
| Becky Martin       |    27173.00 |
| Todd Sumrall       |    27775.00 |
| Laura Armstrong    |    27864.00 |
| Daniel Raglin      |    27932.00 |
| Eric Murdock       |    28085.00 |
| Brosina Hoffman    |    28120.00 |
| Art Ferguson       |    28183.00 |
| Harry Marie        |    28477.00 |
| Bill Eplett        |    28480.00 |
| Zuschuss Carroll   |    28485.00 |
| Susan Pistek       |    29020.00 |
| Raymond Buch       |    29601.00 |
| Muhammed Yedwab    |    29644.00 |
| Peter Fuller       |    29876.00 |
| Penelope Sewall    |    30083.00 |
| Sanjit Engle       |    30143.00 |
| Hunter Lopez       |    30246.00 |
| Jane Waco          |    30288.00 |
| Fred Hopkins       |    30404.00 |
| Natalie Fritzler   |    31778.00 |
| Bart Watters       |    32315.00 |
| Sean Miller        |    35170.00 |
| Christopher Conant |    35187.00 |
| Greg Tran          |    35552.00 |
| Tamara Chand       |    37453.00 |
| Tom Ashbrook       |    40489.00 |
+--------------------+-------------+
80 rows in set (0.08 sec)
~~~

-----

### Query-28: Find each order’s rank (top-5-rank) within its year by profit**  

~~~sql
with order_profit_by_year as
(
      SELECT order_id, 
             year, 
             SUM(profit) AS order_profit
      FROM super_store_orders
      GROUP BY order_id, year
),
ranked as
(
    SELECT  order_id, 
            year, 
            order_profit,
            RANK() OVER (PARTITION BY year ORDER BY order_profit DESC) AS profit_rank
    FROM order_profit_by_year
)
SELECT order_id, 
       year, 
       order_profit,
       profit_rank
FROM ranked
WHERE profit_rank <= 5;

+-----------------+------+--------------+-------------+
| order_id        | year | order_profit | profit_rank |
+-----------------+------+--------------+-------------+
| CA-2011-116904  | 2011 |      4668.70 |           1 |
| ID-2011-64599   | 2011 |      3033.99 |           2 |
| ES-2011-3248922 | 2011 |      2552.53 |           3 |
| IT-2011-3911927 | 2011 |      2304.63 |           4 |
| CA-2011-164973  | 2011 |      2242.84 |           5 |
| CA-2012-145352  | 2012 |      3192.08 |           1 |
| CA-2012-114811  | 2012 |      2509.08 |           2 |
| ES-2012-5671193 | 2012 |      2461.32 |           3 |
| US-2012-128587  | 2012 |      2306.75 |           4 |
| ES-2012-5113958 | 2012 |      2194.83 |           5 |
| CA-2013-118689  | 2013 |      8762.39 |           1 |
| CA-2013-117121  | 2013 |      4946.37 |           2 |
| CA-2013-158841  | 2013 |      2825.28 |           3 |
| IN-2013-50809   | 2013 |      2817.99 |           4 |
| US-2013-140158  | 2013 |      2640.48 |           5 |
| CA-2014-140151  | 2014 |      6734.47 |           1 |
| CA-2014-166709  | 2014 |      5039.99 |           2 |
| CA-2014-127180  | 2014 |      4597.17 |           3 |
| ES-2014-1651774 | 2014 |      4046.58 |           4 |
| MO-2014-2000    | 2014 |      2625.24 |           5 |
+-----------------+------+--------------+-------------+
20 rows in set (0.13 sec)
~~~

-----


### Query-29: Identify duplicate product_name entries and their row numbers**  

~~~sql
    SELECT *
    FROM (
      SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY product_name ORDER BY order_date) AS rn
      FROM super_store_orders
    ) t
    WHERE rn > 1;

+-----------------+------------+------------+----------------+------------------------+-------------+--------------------------------------+----------------------------------+--------+----------------+------------------+-----------------+--------------+---------------------------------------------------------------------------------------------------------------------------------+----------+----------+----------+----------+---------------+----------------+------+-----+
| order_id        | order_date | ship_date  | ship_mode      | customer_name          | segment     | state                                | country                          | market | region         | product_id       | category        | sub_category | product_name                                                                                                                    | sales    | quantity | discount | profit   | shipping_cost | order_priority | year | rn  |
+-----------------+------------+------------+----------------+------------------------+-------------+--------------------------------------+----------------------------------+--------+----------------+------------------+-----------------+--------------+---------------------------------------------------------------------------------------------------------------------------------+----------+----------+----------+----------+---------------+----------------+------+-----+
| CA-2014-123491  | 2014-10-31 | 2014-11-06 | Standard Class | Jamie Kunitz           | Consumer    | California                           | United States                    | US     | West           | OFF-PA-10003424  | Office Supplies | Paper        | "While you Were Out" Message Book, One Form per Page                                                                            |     7.00 |        2 |     0.00 |     3.71 |          0.84 | Medium         | 2014 |   2 |
| CA-2014-165204  | 2014-11-14 | 2014-11-17 | Second Class   | Michael Nguyen         | Consumer    | Tennessee                            | United States                    | US     | South          | OFF-PA-10003424  | Office Supplies | Paper        | "While you Were Out" Message Book, One Form per Page                                                                            |     9.00 |        3 |     0.20 |     3.34 |          1.56 | High           | 2014 |   3 |
| CA-2013-137848  | 2013-01-15 | 2013-01-21 | Standard Class | William Brown          | Consumer    | New York                             | United States                    | US     | East           | OFF-EN-10001137  | Office Supplies | Envelopes    | #10 Gummed Flap White Envelopes, 100/Box                                                                                        |    17.00 |        4 |     0.00 |     7.60 |          0.69 | Medium         | 2013 |   2 |
| CA-2013-138520  | 2013-04-09 | 2013-04-14 | Standard Class | Jeremy Lonsdale        | Consumer    | New York                             | United States                    | US     | East           | OFF-EN-10001137  | Office Supplies | Envelopes    | #10 Gummed Flap White Envelopes, 100/Box                                                                                        |     8.00 |        2 |     0.00 |     3.80 |          0.69 | Medium         | 2013 |   3 |
| CA-2014-117114  | 2014-11-01 | 2014-11-06 | Standard Class | Craig Yedwab           | Corporate   | Illinois                             | United States                    | US     | Central        | OFF-EN-10001137  | Office Supplies | Envelopes    | #10 Gummed Flap White Envelopes, 100/Box                                                                                        |    10.00 |        3 |     0.20 |     3.22 |          0.63 | Medium         | 2014 |   4 |
| CA-2013-102162  | 2013-09-12 | 2013-09-17 | Standard Class | Jill Fjeld             | Consumer    | Virginia                             | United States                    | US     | South          | OFF-EN-10002312  | Office Supplies | Envelopes    | #10 Self-Seal White Envelopes                                                                                                   |    11.00 |        1 |     0.00 |     5.43 |          0.63 | Medium         | 2013 |   2 |
| CA-2013-142097  | 2013-10-16 | 2013-10-21 | Standard Class | Quincy Jones           | Corporate   | Virginia                             | United States                    | US     | South          | OFF-EN-10002312  | Office Supplies | Envelopes    | #10 Self-Seal White Envelopes
...
...
...
~~~

------

### Query-30: Top 3 sub-categories per category by profit**  

~~~sql
    SELECT category, 
           sub_category, 
           sub_profit
    FROM (
      SELECT
        category,
        sub_category,
        SUM(profit) AS sub_profit,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY SUM(profit) DESC) AS rn
      FROM super_store_orders
      GROUP BY category, sub_category
    ) x
    WHERE rn <= 3;
    
+-----------------+--------------+------------+
| category        | sub_category | sub_profit |
+-----------------+--------------+------------+
| Furniture       | Bookcases    |  161924.32 |
| Furniture       | Chairs       |  141973.78 |
| Furniture       | Furnishings  |   46967.55 |
| Office Supplies | Appliances   |  141680.65 |
| Office Supplies | Storage      |  108461.74 |
| Office Supplies | Binders      |   72449.60 |
| Technology      | Copiers      |  258567.62 |
| Technology      | Phones       |  216717.49 |
| Technology      | Accessories  |  129626.44 |
+-----------------+--------------+------------+
9 rows in set (0.08 sec)
~~~

------

### Query-31: Orders in top 10 shipping costs within each ship_mode**  

~~~sql
    SELECT ship_mode, 
           order_id, 
           ship_cost
    FROM (
      SELECT
        ship_mode,
        order_id,
        SUM(shipping_cost) AS ship_cost,
        ROW_NUMBER() OVER (PARTITION BY ship_mode ORDER BY SUM(shipping_cost) DESC) AS rn
      FROM super_store_orders
      GROUP BY ship_mode, order_id
    ) t
    WHERE rn <= 10;
   
+----------------+-----------------+-----------+
| ship_mode      | order_id        | ship_cost |
+----------------+-----------------+-----------+
| First Class    | IN-2011-10286   |   2076.62 |
| First Class    | IN-2011-44803   |   1167.44 |
| First Class    | IT-2013-3376681 |   1131.02 |
| First Class    | MX-2014-113845  |   1029.09 |
| First Class    | IN-2013-71249   |    996.36 |
| First Class    | IT-2011-3183678 |    934.18 |
| First Class    | MX-2014-124744  |    912.04 |
| First Class    | ES-2012-5870268 |    911.60 |
| First Class    | ES-2013-1579342 |    910.16 |
| First Class    | IN-2011-81826   |    904.83 |
| Same Day       | CA-2012-124891  |   1288.99 |
| Same Day       | ES-2014-1972860 |   1046.48 |
| Same Day       | CA-2011-160766  |    984.43 |
| Same Day       | ES-2012-2510515 |    972.42 |
| Same Day       | IN-2014-35983   |    926.85 |
| Same Day       | SG-2013-4320    |    903.04 |
| Same Day       | IT-2013-3085011 |    894.32 |
| Same Day       | IN-2013-48184   |    832.04 |
| Same Day       | MX-2014-154907  |    830.00 |
| Same Day       | MX-2012-130015  |    818.27 |
| Second Class   | SA-2011-1830    |   1314.72 |
| Second Class   | IN-2012-48240   |   1207.60 |
| Second Class   | IN-2013-42360   |   1146.05 |
| Second Class   | IN-2011-28087   |   1064.89 |
| Second Class   | IN-2013-77878   |   1041.10 |
| Second Class   | CA-2014-143567  |   1035.86 |
| Second Class   | ES-2013-2757712 |    947.82 |
| Second Class   | IN-2014-76016   |    927.74 |
| Second Class   | ES-2014-4673578 |    917.03 |
| Second Class   | ES-2013-2860574 |    913.75 |
| Standard Class | IN-2014-37320   |   1224.97 |
| Standard Class | ES-2014-1651774 |    919.31 |
| Standard Class | CA-2014-135909  |    894.81 |
| Standard Class | IN-2012-86369   |    878.38 |
| Standard Class | IN-2011-86278   |    771.98 |
| Standard Class | ES-2012-5877219 |    758.21 |
| Standard Class | ES-2012-2212320 |    731.48 |
| Standard Class | IN-2014-78900   |    724.08 |
| Standard Class | SF-2014-3260    |    699.12 |
| Standard Class | CA-2011-116904  |    698.91 |
+----------------+-----------------+-----------+
40 rows in set (0.15 sec)
~~~

------

### Query-32: Second-highest discount per category**  

~~~sql
    SELECT distinct category, discount
    FROM (
      SELECT
        category,
        discount,
        DENSE_RANK() OVER (PARTITION BY category ORDER BY discount DESC) AS dr
      FROM super_store_orders
    ) x
    WHERE dr = 2;
   
+-----------------+----------+
| category        | discount |
+-----------------+----------+
| Furniture       |     0.80 |
| Office Supplies |     0.70 |
| Technology      |     0.65 |
+-----------------+----------+
3 rows in set (0.12 sec)
~~~

---

### Query-33: Top-10 Total Sales by country per year

~~~sql
SELECT year,
       country,
       SUM(sales) as total_sales
FROM 
       super_store_orders
GROUP BY 
       year,
       country
ORDER by 3 DESC
LIMIT 10; 
  
+------+---------------+-------------+
| year | country       | total_sales |
+------+---------------+-------------+
| 2014 | United States |   734016.00 |
| 2013 | United States |   608523.00 |
| 2011 | United States |   484255.00 |
| 2012 | United States |   470560.00 |
| 2014 | Australia     |   314741.00 |
| 2014 | France        |   308437.00 |
| 2013 | Australia     |   268970.00 |
| 2013 | France        |   230113.00 |
| 2014 | China         |   218975.00 |
| 2014 | Germany       |   216533.00 |
+------+---------------+-------------+
10 rows in set (0.07 sec)
~~~
    