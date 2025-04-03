### 1. Find number of employees per country:

~~~sql
SELECT country, 
       count(*) as count 
FROM  
       destination_table 
GROUP BY  
       country 
ORDER BY  
       count;
~~~

Result:

~~~
+---------+-------+
| country | count |
+---------+-------+
| USA     |     4 |
| CANADA  |     4 |
| MEXICO  |     4 |
+---------+-------+
3 rows in set (0.01 sec)
~~~

------

### 2. find top-2 slaries per country:

~~~sql
WITH Ranked_Salaries AS (
    SELECT
        country,
        name,
        salary,
        ROW_NUMBER() OVER (PARTITION BY country ORDER BY salary DESC) AS rnk
    FROM
        destination_table
)
SELECT
    country,
    name,
    salary
FROM
    Ranked_Salaries
WHERE
    rnk <= 2
ORDER BY
    country, rnk;
~~~

Result:

~~~
+---------+--------+--------+
| country | name   | salary |
+---------+--------+--------+
| CANADA  | Bob    |  60000 |
| CANADA  | Betty  |  50000 |
| MEXICO  | Jason  |  50000 |
| MEXICO  | David  |  40000 |
| USA     | Chuck  |  90000 |
| USA     | George |  80000 |
+---------+--------+--------+
6 rows in set (0.01 sec)
~~~

-----

### 3. find bottom slaries per country:

~~~sql
WITH Ranked_Salaries AS (
    SELECT
        country,
        name,
        salary,
        ROW_NUMBER() OVER (PARTITION BY country ORDER BY salary) AS rnk
    FROM
        destination_table
)
SELECT
    country,
    name,
    salary
FROM
    Ranked_Salaries
WHERE
    rnk <= 1
ORDER BY
    country, rnk;
~~~

Result:

~~~
+---------+-------+--------+
| country | name  | salary |
+---------+-------+--------+
| CANADA  | Babak |  20000 |
| MEXICO  | Jeb   |  30000 |
| USA     | Alice |  50000 |
+---------+-------+--------+
3 rows in set (0.00 sec)
~~~


### 4. find top-3 slaries for all countries:

~~~sql
SELECT
    country,
    name,
    salary
FROM
    destination_table

ORDER BY
    salary DESC
LIMIT 3;
~~~

Result:

~~~
+---------+---------+--------+
| country | name    | salary |
+---------+---------+--------+
| USA     | Chuck   |  90000 |
| USA     | George  |  80000 |
| USA     | Charlie |  70000 |
+---------+---------+--------+
3 rows in set (0.01 sec)
~~~


### 5. **Retrieve the average salary and tax by country**

	This query groups data by `country` to 
	calculate the average salary and tax:

```sql
SELECT
    country,
    AVG(salary) AS avg_salary,
    AVG(tax) AS avg_tax
FROM
    destination_table
GROUP BY
    country
ORDER BY
    avg_salary DESC;
```

Result:

~~~
+---------+------------+-----------+
| country | avg_salary | avg_tax   |
+---------+------------+-----------+
| USA     | 72500.0000 | 7250.0000 |
| CANADA  | 42500.0000 | 4250.0000 |
| MEXICO  | 40000.0000 | 4000.0000 |
+---------+------------+-----------+
3 rows in set (0.00 sec)
~~~

------

### 6. **Find employees with the highest tax-to-salary ratio in each country**

	This uses a window function to rank employees 
	by their tax-to-salary ratio within each country:

```sql
WITH Tax_Ratio_Ranked AS (
    SELECT
        id,
        name,
        country,
        salary,
        tax,
        tax * 1.0 / salary AS tax_ratio,
        RANK() OVER (PARTITION BY country ORDER BY tax * 1.0 / salary DESC) 
          AS rnk
    FROM
        destination_table
)
SELECT
    id,
    name,
    country,
    salary,
    tax,
    tax_ratio
FROM
    Tax_Ratio_Ranked
WHERE
    rnk = 1;
```

Result:

~~~
+------+---------+---------+--------+------+-----------+
| id   | name    | country | salary | tax  | tax_ratio |
+------+---------+---------+--------+------+-----------+
|    5 | Bob     | CANADA  |  60000 | 6000 |   0.10000 |
|    6 | Betty   | CANADA  |  50000 | 5000 |   0.10000 |
|    7 | Barb    | CANADA  |  40000 | 4000 |   0.10000 |
|    8 | Babak   | CANADA  |  20000 | 2000 |   0.10000 |
|    9 | Jeb     | MEXICO  |  30000 | 3000 |   0.10000 |
|   10 | Jason   | MEXICO  |  50000 | 5000 |   0.10000 |
|   11 | David   | MEXICO  |  40000 | 4000 |   0.10000 |
|   12 | Rafa    | MEXICO  |  40000 | 4000 |   0.10000 |
|    1 | Alice   | USA     |  50000 | 5000 |   0.10000 |
|    2 | George  | USA     |  80000 | 8000 |   0.10000 |
|    3 | Charlie | USA     |  70000 | 7000 |   0.10000 |
|    4 | Chuck   | USA     |  90000 | 9000 |   0.10000 |
+------+---------+---------+--------+------+-----------+
12 rows in set (0.00 sec)
~~~

---

### 7. **Identify employees with above-average salaries in their country**

	This uses a correlated subquery to 
	compare each employee's salary with 
	the average salary for their country:

```sql
SELECT
    id,
    name,
    age,
    country,
    salary
FROM
    destination_table D
WHERE
    salary > (
        SELECT
            AVG(salary)
        FROM
            destination_table
        WHERE
            country = D.country
    )
ORDER BY
    country, salary DESC;
```

Result:

~~~
+------+--------+------+---------+--------+
| id   | name   | age  | country | salary |
+------+--------+------+---------+--------+
|    5 | Bob    |   25 | CANADA  |  60000 |
|    6 | Betty  |   25 | CANADA  |  50000 |
|   10 | Jason  |   25 | MEXICO  |  50000 |
|    4 | Chuck  |   45 | USA     |  90000 |
|    2 | George |   40 | USA     |  80000 |
+------+--------+------+---------+--------+
5 rows in set (0.00 sec)
~~~

------

### 8. **Calculate the cumulative tax collected per country**

	Using a window function, this query 
	calculates the cumulative tax amount 
	per country, sorted by the employee's `id`:

```sql
SELECT
    country,
    id,
    name,
    tax,
    SUM(tax) OVER (PARTITION BY country ORDER BY id) AS cumulative_tax
FROM
    destination_table
ORDER BY
    country, id;
```

Result:

~~~
+---------+------+---------+------+----------------+
| country | id   | name    | tax  | cumulative_tax |
+---------+------+---------+------+----------------+
| CANADA  |    5 | Bob     | 6000 |           6000 |
| CANADA  |    6 | Betty   | 5000 |          11000 |
| CANADA  |    7 | Barb    | 4000 |          15000 |
| CANADA  |    8 | Babak   | 2000 |          17000 |

| MEXICO  |    9 | Jeb     | 3000 |           3000 |
| MEXICO  |   10 | Jason   | 5000 |           8000 |
| MEXICO  |   11 | David   | 4000 |          12000 |
| MEXICO  |   12 | Rafa    | 4000 |          16000 |

| USA     |    1 | Alice   | 5000 |           5000 |
| USA     |    2 | George  | 8000 |          13000 |
| USA     |    3 | Charlie | 7000 |          20000 |
| USA     |    4 | Chuck   | 9000 |          29000 |
+---------+------+---------+------+----------------+
12 rows in set (0.00 sec)
~~~

---

### 9. **Detect duplicate employees with the same name, age, and country**

	This helps identify duplicate entries 
	based on non-unique attributes:

```sql
SELECT
    name,
    age,
    country,
    COUNT(*) AS duplicate_count
FROM
    destination_table
GROUP BY
    name,
    age,
    country
HAVING
    COUNT(*) > 1
ORDER BY
    duplicate_count DESC;
```

Result:

~~~
Empty set (0.00 sec)
~~~


