Given the following table for call center 
by customers, can you suggest some OLAP 
sql queries: 

OLAP (Online Analytical Processing) 
queries are useful for  performing 
multi-dimensional analysis on data. 
Here are some OLAP SQL queries for 
the `calls` table to analyze various 
aspects of call center data:


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
);
-------------------------------------
-- find response time frequency per call center
SELECT call_center, 
       response_time, 
       COUNT(*) AS count
FROM calls 
GROUP BY 1,2 
ORDER BY 1,3 DESC;

mysql> SELECT call_center,
    ->        response_time,
    ->        COUNT(*) AS count
    -> FROM calls
    -> GROUP BY 1,2
    -> ORDER BY 1,3 DESC;
+----------------+---------------+-------+
| call_center    | response_time | count |
+----------------+---------------+-------+
| Baltimore/MD   | Within SLA    |  6855 |
| Baltimore/MD   | Below SLA     |  2768 |
| Baltimore/MD   | Above SLA     |  1389 |
| Chicago/IL     | Within SLA    |  3361 |
| Chicago/IL     | Below SLA     |  1361 |
| Chicago/IL     | Above SLA     |   697 |
| Denver/CO      | Within SLA    |  1741 |
| Denver/CO      | Below SLA     |   692 |
| Denver/CO      | Above SLA     |   343 |
| Los Angeles/CA | Within SLA    |  8668 |
| Los Angeles/CA | Below SLA     |  3327 |
| Los Angeles/CA | Above SLA     |  1739 |
+----------------+---------------+-------+
12 rows in set (0.06 sec)
---------------------------------------

-- find average call duration per call center (in descending order)
SELECT call_center, 
       AVG(call_duration_minutes) as avg_call_duration
FROM calls 
GROUP BY 1 
ORDER BY 2 DESC;

mysql> SELECT call_center,
    ->        AVG(call_duration_minutes) as avg_call_duration
    -> FROM calls
    -> GROUP BY 1
    -> ORDER BY 2 DESC;
+----------------+-------------------+
| call_center    | avg_call_duration |
+----------------+-------------------+
| Chicago/IL     |           25.0626 |
| Los Angeles/CA |           25.0532 |
| Denver/CO      |           25.0166 |
| Baltimore/MD   |           24.9620 |
+----------------+-------------------+
4 rows in set (0.04 sec)
---------------------------------------
SELECT channel, 
       count(*) as channel_count, 
       ROUND((COUNT(*) / (SELECT COUNT(*) FROM calls)) * 100, 2) AS percentage
FROM calls 
GROUP BY channel 
ORDER BY percentage DESC;

mysql> SELECT channel,
    ->        count(*) as channel_count,
    ->        ROUND((COUNT(*) / (SELECT COUNT(*) FROM calls)) * 100, 2) AS percentage
    -> FROM calls
    -> GROUP BY channel
    -> ORDER BY percentage DESC;
+-------------+---------------+------------+
| channel     | channel_count | percentage |
+-------------+---------------+------------+
| Call-Center |         10639 |      32.30 |
| Chatbot     |          8256 |      25.06 |
| Email       |          7470 |      22.68 |
| Web         |          6576 |      19.96 |
+-------------+---------------+------------+
4 rows in set (0.03 sec)


-----------------------------------------
-- find top-5 date with highest durations
SELECT 
    call_timestamp, 
    MAX(call_duration_minutes) AS max_call_duration
FROM  calls
GROUP BY call_timestamp
ORDER BY max_call_duration DESC
LIMIT 5;

mysql> SELECT
    ->     call_timestamp,
    ->     MAX(call_duration_minutes) AS max_call_duration
    -> FROM  calls
    -> GROUP BY call_timestamp
    -> ORDER BY max_call_duration DESC
    -> LIMIT 5;
+----------------+-------------------+
| call_timestamp | max_call_duration |
+----------------+-------------------+
| 10/29/2020     |                45 |
| 10/05/2020     |                45 |
| 10/04/2020     |                45 |
| 10/17/2020     |                45 |
| 10/28/2020     |                45 |
+----------------+-------------------+
5 rows in set (0.03 sec)
-------------------------------------------

SELECT MIN(call_duration_minutes) AS min_call_duration, 
       MAX(call_duration_minutes) AS max_call_duration, 
       AVG(call_duration_minutes) AS avg_call_duration 
FROM calls;
+-------------------+-------------------+-------------------+
| min_call_duration | max_call_duration | avg_call_duration |
+-------------------+-------------------+-------------------+
|                 5 |                45 |           25.0212 |
+-------------------+-------------------+-------------------+
1 row in set (0.02 sec)

-------------------------------------------

SELECT call_center, 
       AVG(call_duration_minutes)  avg_call_duration_in_minutes
FROM calls GROUP BY 1 
ORDER BY 2 DESC;
+----------------+------------------------------+
| call_center    | avg_call_duration_in_minutes |
+----------------+------------------------------+
| Chicago/IL     |                      25.0626 |
| Los Angeles/CA |                      25.0532 |
| Denver/CO      |                      25.0166 |
| Baltimore/MD   |                      24.9620 |
+----------------+------------------------------+
4 rows in set (0.04 sec)

---------------------------------------------
-- find top-5 sentiment for all states.

SELECT state, sentiment , COUNT(*) as count 
FROM calls 
GROUP BY 1,2 
ORDER BY 3 DESC
LIMIT 5;

mysql> SELECT state, sentiment , COUNT(*) as count
    -> FROM calls
    -> GROUP BY 1,2
    -> ORDER BY 3 DESC
    -> LIMIT 5;
+------------+-----------+-------+
| state      | sentiment | count |
+------------+-----------+-------+
| California | Negative  |  1255 |
| Texas      | Negative  |  1245 |
| California | Neutral   |   963 |
| Texas      | Neutral   |   934 |
| Florida    | Negative  |   920 |
+------------+-----------+-------+
5 rows in set (0.05 sec)

---------------------------------------------------
-- find top-2 sentiment per state.

WITH Ranked AS (
    SELECT
       state,
       sentiment,
       COUNT(*) as count,
       ROW_NUMBER() OVER (PARTITION BY state ORDER BY count(*) DESC) AS rnk
       FROM calls
       GROUP BY state, sentiment
)
SELECT  state, sentiment, count, rnk
FROM Ranked
WHERE rnk <= 2
ORDER BY state, count DESC;

mysql> WITH Ranked AS (
    ->     SELECT
    ->        state,
    ->        sentiment,
    ->        COUNT(*) as count,
    ->        ROW_NUMBER() OVER (PARTITION BY state ORDER BY count(*) DESC) AS rnk
    ->        FROM calls
    ->        GROUP BY state, sentiment
    -> )
    -> SELECT  state, sentiment, count, rnk
    -> FROM Ranked
    -> WHERE rnk <= 2
    -> ORDER BY state, count DESC;
+----------------------+---------------+-------+-----+
| state                | sentiment     | count | rnk |
+----------------------+---------------+-------+-----+
| Alabama              | Negative      |   265 |   1 |
| Alabama              | Neutral       |   200 |   2 |
| Alaska               | Negative      |    45 |   1 |
| Alaska               | Neutral       |    32 |   2 |
| Arizona              | Negative      |   235 |   1 |
| Arizona              | Neutral       |   204 |   2 |
| Arkansas             | Negative      |    73 |   1 |
| Arkansas             | Neutral       |    50 |   2 |
| California           | Negative      |  1255 |   1 |
| California           | Neutral       |   963 |   2 |
| Colorado             | Negative      |   253 |   1 |
| Colorado             | Neutral       |   181 |   2 |
| Connecticut          | Negative      |   138 |   1 |
| Connecticut          | Neutral       |   105 |   2 |
| Delaware             | Negative      |    46 |   1 |
| Delaware             | Very Negative |    27 |   2 |
| District of Columbia | Negative      |   395 |   1 |
| District of Columbia | Neutral       |   290 |   2 |
| Florida              | Negative      |   920 |   1 |
| Florida              | Neutral       |   750 |   2 |
| Georgia              | Negative      |   304 |   1 |
| Georgia              | Neutral       |   238 |   2 |
| Hawaii               | Neutral       |    50 |   1 |
| Hawaii               | Negative      |    48 |   2 |
| Idaho                | Negative      |    55 |   1 |
| Idaho                | Neutral       |    47 |   2 |
| Illinois             | Negative      |   286 |   1 |
| Illinois             | Neutral       |   223 |   2 |
| Indiana              | Negative      |   256 |   1 |
| Indiana              | Neutral       |   198 |   2 |
| Iowa                 | Negative      |   114 |   1 |
| Iowa                 | Neutral       |    97 |   2 |
| Kansas               | Neutral       |   149 |   1 |
| Kansas               | Negative      |   132 |   2 |
| Kentucky             | Negative      |   118 |   1 |
| Kentucky             | Neutral       |   112 |   2 |
| Louisiana            | Negative      |   199 |   1 |
| Louisiana            | Neutral       |   174 |   2 |
| Maine                | Neutral       |     8 |   1 |
| Maine                | Negative      |     4 |   2 |
| Maryland             | Negative      |   136 |   1 |
| Maryland             | Neutral       |   114 |   2 |
| Massachusetts        | Negative      |   146 |   1 |
| Massachusetts        | Neutral       |   135 |   2 |
| Michigan             | Negative      |   203 |   1 |
| Michigan             | Neutral       |   144 |   2 |
| Minnesota            | Negative      |   269 |   1 |
| Minnesota            | Neutral       |   186 |   2 |
| Mississippi          | Negative      |    62 |   1 |
| Mississippi          | Neutral       |    40 |   2 |
| Missouri             | Negative      |   222 |   1 |
| Missouri             | Neutral       |   182 |   2 |
| Montana              | Negative      |    28 |   1 |
| Montana              | Neutral       |    24 |   2 |
| Nebraska             | Negative      |    88 |   1 |
| Nebraska             | Neutral       |    62 |   2 |
| Nevada               | Negative      |   131 |   1 |
| Nevada               | Neutral       |   125 |   2 |
| New Hampshire        | Neutral       |    19 |   1 |
| New Hampshire        | Negative      |    18 |   2 |
| New Jersey           | Negative      |    99 |   1 |
| New Jersey           | Neutral       |    79 |   2 |
| New Mexico           | Negative      |    62 |   1 |
| New Mexico           | Neutral       |    54 |   2 |
| New York             | Negative      |   601 |   1 |
| New York             | Neutral       |   487 |   2 |
| North Carolina       | Negative      |   267 |   1 |
| North Carolina       | Neutral       |   190 |   2 |
| North Dakota         | Negative      |    34 |   1 |
| North Dakota         | Neutral       |    17 |   2 |
| Ohio                 | Negative      |   408 |   1 |
| Ohio                 | Neutral       |   304 |   2 |
| Oklahoma             | Negative      |   192 |   1 |
| Oklahoma             | Neutral       |   146 |   2 |
| Oregon               | Negative      |    79 |   1 |
| Oregon               | Neutral       |    76 |   2 |
| Pennsylvania         | Negative      |   330 |   1 |
| Pennsylvania         | Neutral       |   289 |   2 |
| Rhode Island         | Neutral       |    14 |   1 |
| Rhode Island         | Negative      |    10 |   2 |
| South Carolina       | Negative      |    95 |   1 |
| South Carolina       | Neutral       |    88 |   2 |
| South Dakota         | Negative      |    36 |   1 |
| South Dakota         | Neutral       |    24 |   2 |
| Tennessee            | Negative      |   235 |   1 |
| Tennessee            | Neutral       |   190 |   2 |
| Texas                | Negative      |  1245 |   1 |
| Texas                | Neutral       |   934 |   2 |
| Utah                 | Negative      |    99 |   1 |
| Utah                 | Neutral       |    71 |   2 |
| Vermont              | Neutral       |     5 |   1 |
| Vermont              | Negative      |     4 |   2 |
| Virginia             | Negative      |   366 |   1 |
| Virginia             | Neutral       |   314 |   2 |
| Washington           | Negative      |   245 |   1 |
| Washington           | Neutral       |   161 |   2 |
| West Virginia        | Neutral       |    98 |   1 |
| West Virginia        | Negative      |    85 |   2 |
| Wisconsin            | Negative      |   119 |   1 |
| Wisconsin            | Neutral       |    82 |   2 |
| Wyoming              | Negative      |     8 |   1 |
| Wyoming              | Neutral       |     3 |   2 |
+----------------------+---------------+-------+-----+
102 rows in set (0.04 sec)
---------------------------------------------------
-- find average call duration per sentiment
SELECT sentiment, 
       AVG(call_duration_minutes) as avg_call_duration
FROM calls 
GROUP BY 1 
ORDER BY 2 DESC;

mysql> SELECT sentiment,
    ->        AVG(call_duration_minutes) as avg_call_duration
    -> FROM calls
    -> GROUP BY 1
    -> ORDER BY 2 DESC;
+---------------+-------------------+
| sentiment     | avg_call_duration |
+---------------+-------------------+
| Negative      |           25.2618 |
| Neutral       |           24.9398 |
| Very Negative |           24.9391 |
| Positive      |           24.8620 |
| Very Positive |           24.7593 |
+---------------+-------------------+
5 rows in set (0.04 sec)

-----------------------------------------------------

### 1. Total Number of Calls per Call Center

```sql
SELECT call_center, 
       COUNT(*) AS total_calls
FROM calls
GROUP BY call_center;
```

mysql> SELECT call_center,
    ->        COUNT(*) AS total_calls
    -> FROM calls
    -> GROUP BY call_center;
+----------------+-------------+
| call_center    | total_calls |
+----------------+-------------+
| Los Angeles/CA |       13734 |
| Baltimore/MD   |       11012 |
| Denver/CO      |        2776 |
| Chicago/IL     |        5419 |
+----------------+-------------+
4 rows in set (0.04 sec)

### 1.5 Fnd the call center, which has handled
        the most of the calls
        

```sql
SELECT call_center, 
       COUNT(*) AS total_calls
FROM calls
GROUP BY call_center
ORDER by total_calls DESC
limit 1;

```

mysql> SELECT call_center,
    ->        COUNT(*) AS total_calls
    -> FROM calls
    -> GROUP BY call_center
    -> ORDER by total_calls DESC
    -> limit 1;
+----------------+-------------+
| call_center    | total_calls |
+----------------+-------------+
| Los Angeles/CA |       13734 |
+----------------+-------------+
1 row in set (0.04 sec)


### 1.5 Fnd two call centers, which have handled
        the most and least number of the calls
        
-- Find the call center with the highest total call duration
SELECT call_center, call_indicator, total_calls
FROM (
    SELECT call_center,
           'MOST CALLS' as call_indicator,
           COUNT(*) AS total_calls
    FROM calls
    GROUP BY call_center
    ORDER BY total_calls DESC
    LIMIT 1
) AS highest_duration

UNION ALL

-- Find the call center with the lowest total call duration
SELECT call_center, call_indicator, total_calls
FROM (
    SELECT call_center, 
          'LEAST CALLS' as call_indicator,
           COUNT(*) AS total_calls
    FROM calls
    GROUP BY call_center
    ORDER BY total_calls ASC
    LIMIT 1
) AS lowest_duration;

mysql> SELECT call_center, call_indicator, total_calls
    -> FROM (
    ->     SELECT call_center,
    ->            'MOST CALLS' as call_indicator,
    ->            COUNT(*) AS total_calls
    ->     FROM calls
    ->     GROUP BY call_center
    ->     ORDER BY total_calls DESC
    ->     LIMIT 1
    -> ) AS highest_duration
    ->
    -> UNION ALL
    ->
    -> -- Find the call center with the lowest total call duration
    -> SELECT call_center, call_indicator, total_calls
    -> FROM (
    ->     SELECT call_center,
    ->           'LEAST CALLS' as call_indicator,
    ->            COUNT(*) AS total_calls
    ->     FROM calls
    ->     GROUP BY call_center
    ->     ORDER BY total_calls ASC
    ->     LIMIT 1
    -> ) AS lowest_duration;
+----------------+----------------+-------------+
| call_center    | call_indicator | total_calls |
+----------------+----------------+-------------+
| Los Angeles/CA | MOST CALLS     |       13734 |
| Denver/CO      | LEAST CALLS    |        2776 |
+----------------+----------------+-------------+
2 rows in set (0.07 sec)



### 2. Average CSAT Score by Call Center and Channel

```sql
SELECT call_center, 
       channel, 
       AVG(csat_score) AS average_csat_score
FROM calls
GROUP BY call_center, channel;
```

mysql> SELECT call_center,
    ->        channel,
    ->        AVG(csat_score) AS average_csat_score
    -> FROM calls
    -> GROUP BY call_center, channel;
+----------------+-------------+--------------------+
| call_center    | channel     | average_csat_score |
+----------------+-------------+--------------------+
| Los Angeles/CA | Call-Center |             5.5844 |
| Baltimore/MD   | Chatbot     |             5.5268 |
| Los Angeles/CA | Chatbot     |             5.5195 |
| Baltimore/MD   | Call-Center |             5.5505 |
| Baltimore/MD   | Email       |             5.5935 |
| Los Angeles/CA | Web         |             5.5877 |
| Denver/CO      | Chatbot     |             5.4291 |
| Baltimore/MD   | Web         |             5.5776 |
| Chicago/IL     | Call-Center |             5.7291 |
| Chicago/IL     | Chatbot     |             5.3904 |
| Los Angeles/CA | Email       |             5.5119 |
| Chicago/IL     | Email       |             5.1837 |
| Denver/CO      | Web         |             5.8434 |
| Denver/CO      | Email       |             5.4406 |
| Denver/CO      | Call-Center |             5.7815 |
| Chicago/IL     | Web         |             5.5039 |
+----------------+-------------+--------------------+
16 rows in set (0.04 sec)


### 3. Total Call Duration by Customer and Call Center
       Which 10 customers have made most calls by minutes

```sql
SELECT customer_name, 
       call_center, 
       SUM(call_duration_minutes) AS total_call_duration
FROM calls
GROUP BY customer_name, call_center
ORDER BY total_call_duration DESC
LIMIT 10;
```

mysql> SELECT customer_name,
    ->        call_center,
    ->        SUM(call_duration_minutes) AS total_call_duration
    -> FROM calls
    -> GROUP BY customer_name, call_center
    -> ORDER BY total_call_duration DESC
    -> LIMIT 10;
+-------------------+----------------+---------------------+
| customer_name     | call_center    | total_call_duration |
+-------------------+----------------+---------------------+
| Nicoline Iskowitz | Chicago/IL     |                  45 |
| Merell Jacobi     | Chicago/IL     |                  45 |
| Averill Brundrett | Los Angeles/CA |                  45 |
| Claretta Blincow  | Baltimore/MD   |                  45 |
| Andreana Cayet    | Los Angeles/CA |                  45 |
| Bethina Fazzioli  | Denver/CO      |                  45 |
| Amargo Eplate     | Baltimore/MD   |                  45 |
| Harwilll Farlow   | Chicago/IL     |                  45 |
| Taddeusz Badcock  | Los Angeles/CA |                  45 |
| Jessamine Guillou | Chicago/IL     |                  45 |
+-------------------+----------------+---------------------+
10 rows in set (0.08 sec)



### 4. Number of Calls exceeding 700 by State and Sentiment

```sql
SELECT state, 
       sentiment, 
       COUNT(*) AS number_of_calls
FROM calls
GROUP BY state, sentiment
HAVING number_of_calls > 700;
```

mysql> SELECT state,
    ->        sentiment,
    ->        COUNT(*) AS number_of_calls
    -> FROM calls
    -> GROUP BY state, sentiment
    -> HAVING number_of_calls > 700;
+------------+-----------+-----------------+
| state      | sentiment | number_of_calls |
+------------+-----------+-----------------+
| Florida    | Negative  |             920 |
| Texas      | Neutral   |             934 |
| California | Negative  |            1255 |
| Texas      | Negative  |            1245 |
| California | Neutral   |             963 |
| Florida    | Neutral   |             750 |
+------------+-----------+-----------------+
6 rows in set (0.05 sec)

### 5. Average Response Time by City and Call Center

```sql
SELECT city, 
       call_center, 
       AVG(response_time) AS average_response_time
FROM calls
GROUP BY city, call_center;
```

### 6. Number of Calls by Reason and Channel

```sql
SELECT reason, 
       channel, 
       COUNT(*) AS number_of_calls
FROM calls
GROUP BY reason, channel;
```

mysql> SELECT reason,
    ->        channel,
    ->        COUNT(*) AS number_of_calls
    -> FROM calls
    -> GROUP BY reason, channel;
+------------------+-------------+-----------------+
| reason           | channel     | number_of_calls |
+------------------+-------------+-----------------+
| Billing Question | Call-Center |            5890 |
| Service Outage   | Chatbot     |            2355 |
| Billing Question | Chatbot     |            5901 |
| Payments         | Call-Center |            4749 |
| Billing Question | Email       |            5901 |
| Billing Question | Web         |            5770 |
| Service Outage   | Email       |            1569 |
| Service Outage   | Web         |             806 |
+------------------+-------------+-----------------+
8 rows in set (0.04 sec)


### 7. Total Calls and Average Call Duration by Call Center and State

```sql
SELECT call_center, 
       state, 
       COUNT(*) AS total_calls, 
       AVG(call_duration_minutes) AS average_call_duration
FROM calls
GROUP BY call_center, state;
```

### 8. CSAT Score Distribution by Call Center

```sql
SELECT call_center, 
       csat_score, 
       COUNT(*) AS count_of_scores
FROM calls
GROUP BY call_center, csat_score
ORDER BY call_center, csat_score;
```

### 9. Total Calls by Day (Assuming `call_timestamp` includes date information)

```sql
SELECT call_timestamp, 
       COUNT(*) AS total_calls
FROM calls
GROUP BY call_timestamp
ORDER BY call_timestamp;
```

### 10. Calls by Sentiment and Call Center

```sql
SELECT call_center, 
       sentiment, 
       COUNT(*) AS number_of_calls
FROM calls
GROUP BY call_center, sentiment;
```

### 11. Average Call Duration by Reason and Sentiment

```sql
SELECT reason, 
       sentiment, 
       AVG(call_duration_minutes) AS average_call_duration
FROM calls
GROUP BY reason, sentiment;
```

### 12. Total Calls and Average CSAT Score by City and State

```sql
SELECT city, 
       state, 
       COUNT(*) AS total_calls, 
       AVG(csat_score) AS average_csat_score
FROM calls
GROUP BY city, state;
```

### 13. Rolling 7-Day Average CSAT Score by Call Center
This query calculates the rolling 7-day average 
CSAT score for each call center.

```sql
SELECT 
    call_center, 
    call_timestamp, 
    AVG(csat_score) OVER (PARTITION BY call_center ORDER BY call_timestamp ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS rolling_7_day_avg_csat
FROM 
    calls
ORDER BY 
    call_center, call_timestamp;
```

### 14. Monthly CSAT Score Trend by Call Center and Channel
This query shows the monthly trend of 
CSAT scores by call center and channel.

```sql
SELECT 
    call_center, 
    channel, 
    day_of_month, 
    AVG(csat_score) AS avg_csat_score
FROM 
    calls
GROUP BY 
    call_center, channel, day_of_month
ORDER BY 
    call_center, channel, day_of_month;
```

mysql> SELECT
    ->     call_center,
    ->     channel,
    ->     day_of_month,
    ->     AVG(csat_score) AS avg_csat_score
    -> FROM
    ->     calls
    -> GROUP BY
    ->     call_center, channel, day_of_month
    -> ORDER BY
    ->     call_center, channel, day_of_month;
+----------------+-------------+--------------+----------------+
| call_center    | channel     | day_of_month | avg_csat_score |
+----------------+-------------+--------------+----------------+
| Baltimore/MD   | Call-Center |            1 |         5.2143 |
| Baltimore/MD   | Call-Center |            2 |         5.2821 |
| Baltimore/MD   | Call-Center |            3 |         5.3261 |
...
| Los Angeles/CA | Web         |           28 |         5.8065 |
| Los Angeles/CA | Web         |           29 |         5.2308 |
| Los Angeles/CA | Web         |           30 |         5.6216 |
+----------------+-------------+--------------+----------------+
481 rows in set (0.06 sec)

### 15. Average Call Duration and Response Time by State and Sentiment
        for states of 'California', 'Iowa', and 'Wyoming'
This query provides the average call duration and 
response time for each state, grouped by sentiment.

```sql
SELECT 
    state, 
    sentiment, 
    AVG(call_duration_minutes) AS avg_call_duration, 
    AVG(CAST(response_time AS UNSIGNED)) AS avg_response_time
FROM 
    calls
WHERE state in ('California', 'Iowa', 'Wyoming')
GROUP BY 
    state, sentiment
ORDER BY 
    state, sentiment;
```

mysql> SELECT
    ->     state,
    ->     sentiment,
    ->     AVG(call_duration_minutes) AS avg_call_duration,
    ->     AVG(CAST(response_time AS UNSIGNED)) AS avg_response_time
    -> FROM
    ->     calls
    -> WHERE state in ('California', 'Iowa', 'Wyoming')
    -> GROUP BY
    ->     state, sentiment
    -> ORDER BY
    ->     state, sentiment;
+------------+---------------+-------------------+-------------------+
| state      | sentiment     | avg_call_duration | avg_response_time |
+------------+---------------+-------------------+-------------------+
| California | Negative      |           25.8430 |            0.0000 |
| California | Neutral       |           24.5472 |            0.0000 |
| California | Positive      |           25.2370 |            0.0000 |
| California | Very Negative |           24.3254 |            0.0000 |
| California | Very Positive |           24.7950 |            0.0000 |
| Iowa       | Negative      |           24.8070 |            0.0000 |
| Iowa       | Neutral       |           24.8351 |            0.0000 |
| Iowa       | Positive      |           27.0000 |            0.0000 |
| Iowa       | Very Negative |           26.0857 |            0.0000 |
| Iowa       | Very Positive |           25.2222 |            0.0000 |
| Wyoming    | Negative      |           25.6250 |            0.0000 |
| Wyoming    | Neutral       |           19.6667 |            0.0000 |
+------------+---------------+-------------------+-------------------+
12 rows in set, 4008 warnings (0.03 sec)

### 16. Top 5 Reasons for Calls by Call Center and Sentiment
This query identifies the top 5 reasons for calls 
for each call center and sentiment.

```sql
SELECT 
    call_center, 
    sentiment, 
    reason, 
    COUNT(*) AS call_count
FROM 
    calls
GROUP BY 
    call_center, sentiment, reason
ORDER BY 
    call_center, sentiment, call_count DESC
LIMIT 5;
```

mysql> SELECT
    ->     call_center,
    ->     sentiment,
    ->     reason,
    ->     COUNT(*) AS call_count
    -> FROM
    ->     calls
    -> GROUP BY
    ->     call_center, sentiment, reason
    -> ORDER BY
    ->     call_center, sentiment, call_count DESC
    -> LIMIT 5;
+--------------+-----------+------------------+------------+
| call_center  | sentiment | reason           | call_count |
+--------------+-----------+------------------+------------+
| Baltimore/MD | Negative  | Billing Question |       2633 |
| Baltimore/MD | Negative  | Payments         |        553 |
| Baltimore/MD | Negative  | Service Outage   |        525 |
| Baltimore/MD | Neutral   | Billing Question |       2077 |
| Baltimore/MD | Neutral   | Service Outage   |        451 |
+--------------+-----------+------------------+------------+
5 rows in set (0.06 sec)

### 17. Day of Week Distribution of Calls by Call Center
This query provides the Day of Week distribution of 
calls for each call center.

```sql
SELECT 
    call_center, 
    day_of_week, 
    COUNT(*) AS call_count
FROM 
    calls
GROUP BY 
    call_center, day_of_week
ORDER BY 
    call_center, day_of_week;
```

mysql> SELECT
    ->     call_center,
    ->     day_of_week,
    ->     COUNT(*) AS call_count
    -> FROM
    ->     calls
    -> GROUP BY
    ->     call_center, day_of_week
    -> ORDER BY
    ->     call_center, day_of_week;
+----------------+-------------+------------+
| call_center    | day_of_week | call_count |
+----------------+-------------+------------+
| Baltimore/MD   | Friday      |       1829 |
| Baltimore/MD   | Monday      |       1420 |
| Baltimore/MD   | Saturday    |       1517 |
| Baltimore/MD   | Sunday      |       1383 |
| Baltimore/MD   | Thursday    |       1845 |
| Baltimore/MD   | Tuesday     |       1472 |
| Baltimore/MD   | Wednesday   |       1546 |
| Chicago/IL     | Friday      |        902 |
| Chicago/IL     | Monday      |        715 |
| Chicago/IL     | Saturday    |        702 |
| Chicago/IL     | Sunday      |        745 |
| Chicago/IL     | Thursday    |        899 |
| Chicago/IL     | Tuesday     |        749 |
| Chicago/IL     | Wednesday   |        707 |
| Denver/CO      | Friday      |        482 |
| Denver/CO      | Monday      |        357 |
| Denver/CO      | Saturday    |        388 |
| Denver/CO      | Sunday      |        350 |
| Denver/CO      | Thursday    |        477 |
| Denver/CO      | Tuesday     |        378 |
| Denver/CO      | Wednesday   |        344 |
| Los Angeles/CA | Friday      |       2357 |
| Los Angeles/CA | Monday      |       1842 |
| Los Angeles/CA | Saturday    |       1796 |
| Los Angeles/CA | Sunday      |       1818 |
| Los Angeles/CA | Thursday    |       2260 |
| Los Angeles/CA | Tuesday     |       1809 |
| Los Angeles/CA | Wednesday   |       1852 |
+----------------+-------------+------------+
28 rows in set (0.05 sec)

### 18. Average CSAT Score by Customer and Channel with  Top-2 Ranking 
This query calculates the average CSAT score for each customer 
and channel, and ranks them within each channel.

```sql
WITH CustomerCSAT AS (
    SELECT 
        customer_name, 
        channel, 
        AVG(csat_score) AS avg_csat_score,
        RANK() OVER (PARTITION BY channel ORDER BY AVG(csat_score) DESC) AS rnk
    FROM 
        calls
    WHERE channel = 'Web'
    GROUP BY 
        customer_name, channel
)
SELECT 
    customer_name, 
    channel, 
    avg_csat_score, 
    rnk
FROM 
    CustomerCSAT
    where rnk < 2
ORDER BY 
    channel, rnk;
```
    
mysql> WITH CustomerCSAT AS (
    ->     SELECT
    ->         customer_name,
    ->         channel,
    ->         AVG(csat_score) AS avg_csat_score,
    ->         RANK() OVER (PARTITION BY channel ORDER BY AVG(csat_score) DESC) AS rnk
    ->     FROM
    ->         calls
    ->     WHERE channel = 'Web'
    ->     GROUP BY
    ->         customer_name, channel
    -> )
    -> SELECT
    ->     customer_name,
    ->     channel,
    ->     avg_csat_score,
    ->     rnk
    -> FROM
    ->     CustomerCSAT
    ->     where rnk < 2
    -> ORDER BY
    ->     channel, rnk;
+----------------------+---------+----------------+-----+
| customer_name        | channel | avg_csat_score | rnk |
+----------------------+---------+----------------+-----+
| Pierson Showte       | Web     |        10.0000 |   1 |
| Berkly Biscomb       | Web     |        10.0000 |   1 |
| Kiri Errichiello     | Web     |        10.0000 |   1 |
...
| Lelah Pipkin         | Web     |        10.0000 |   1 |
| Cristobal Wear       | Web     |        10.0000 |   1 |
| Colin Pierse         | Web     |        10.0000 |   1 |
+----------------------+---------+----------------+-----+
103 rows in set (0.04 sec)

### 19. Top-5 Call Duration Percentage Contribution by Call Center and City
This query shows the Top-5 percentage contribution of call durations by each city within a call center.

```sql
SELECT 
    call_center, 
    city, 
    SUM(call_duration_minutes) AS total_call_duration, 
    SUM(call_duration_minutes) * 100.0 / SUM(SUM(call_duration_minutes)) OVER (PARTITION BY call_center) AS percent_contribution
FROM 
    calls
GROUP BY 
    call_center, city
ORDER BY 
    call_center, percent_contribution DESC
    LIMIT 5;
```

mysql> SELECT
    ->     call_center,
    ->     city,
    ->     SUM(call_duration_minutes) AS total_call_duration,
    ->     SUM(call_duration_minutes) * 100.0 / SUM(SUM(call_duration_minutes)) OVER (PARTITION BY call_center) AS percent_contribution
    -> FROM
    ->     calls
    -> GROUP BY
    ->     call_center, city
    -> ORDER BY
    ->     call_center, percent_contribution DESC
    ->     LIMIT 5;
+--------------+---------------+---------------------+----------------------+
| call_center  | city          | total_call_duration | percent_contribution |
+--------------+---------------+---------------------+----------------------+
| Baltimore/MD | Washington    |                8903 |              3.23886 |
| Baltimore/MD | Houston       |                5466 |              1.98850 |
| Baltimore/MD | New York City |                4869 |              1.77131 |
| Baltimore/MD | El Paso       |                4737 |              1.72329 |
| Baltimore/MD | Dallas        |                3594 |              1.30747 |
+--------------+---------------+---------------------+----------------------+
5 rows in set (0.07 sec)

### Explanation of Queries:
1. **Total Number of Calls by Call Center**: Counts the number of calls handled by each call center.
2. **Average CSAT Score by Call Center and Channel**: Calculates the average Customer Satisfaction (CSAT) score for each call center and channel.
3. **Total Call Duration by Customer and Call Center**: Sums up the total call duration for each customer per call center.
4. **Number of Calls by State and Sentiment**: Counts the number of calls from each state, categorized by sentiment.
5. **Average Response Time by City and Call Center**: Calculates the average response time for each city and call center.
6. **Number of Calls by Reason and Channel**: Counts the number of calls for each reason and channel.
7. **Total Calls and Average Call Duration by Call Center and State**: Provides the total number of calls and the average call duration for each call center and state.
8. **CSAT Score Distribution by Call Center**: Shows the distribution of CSAT scores for each call center.
9. **Total Calls by Day**: Counts the number of calls per day.
10. **Calls by Sentiment and Call Center**: Counts the number of calls per sentiment for each call center.
11. **Average Call Duration by Reason and Sentiment**: Calculates the average call duration for each reason and sentiment.
12. **Total Calls and Average CSAT Score by City and State**: Provides the total number of calls and the average CSAT score for each city and state.
13. **Rolling 7-Day Average CSAT Score by Call Center**: Calculates the rolling average CSAT score over the past 7 days for each call center.
14. **Monthly CSAT Score Trend by Call Center and Channel**: Displays the trend in average CSAT scores on a monthly basis, grouped by call center and channel.
15. **Average Call Duration and Response Time by State and Sentiment**: Provides the average call duration and response time for each state, segmented by sentiment.
16. **Top 5 Reasons for Calls by Call Center and Sentiment**: Identifies the top 5 reasons for calls for each call center and sentiment.
17. **Hourly Distribution of Calls by Call Center**: Shows how call volumes vary by hour for each call center.
18. **Average CSAT Score by Customer and Channel with Ranking**: Ranks customers within each channel based on their average CSAT scores.
19. **Call Duration Percentage Contribution by Call Center and City**: Calculates the percentage contribution of call durations from each city within a call center.


