
# 📊 Teaching ROLLUP and CUBE in MySQL
## Complete Tutorial with Table, Data, Queries & Stored Procedure
(MySQL 8+/9 Compatible)

---

# 1️⃣ Create Teaching Table

```sql
DROP TABLE IF EXISTS sales;
CREATE TABLE sales (
    product  VARCHAR(10),
    quarter  VARCHAR(5),
    region   VARCHAR(20),
    sales    INT
);
```

---

# 2️⃣ Populate Data

```sql
INSERT INTO sales VALUES
('A','Q1','Europe',10),
('A','Q1','America',20),
('A','Q2','Europe',20),
('A','Q2','America',50),
('A','Q3','America',20),
('A','Q4','Europe',10),
('A','Q4','America',30),
('B','Q1','Europe',40),
('B','Q1','America',60),
('B','Q2','Europe',20),
('B','Q2','America',10),
('B','Q3','America',20),
('B','Q4','Europe',10),
('B','Q4','America',40),
('C','Q1','Europe',50),
('C','Q1','America',60),
('C','Q2','Europe',35),
('C','Q2','America',45);
```

# View Data
```sql
mysql> select * from sales;
+---------+---------+---------+-------+
| product | quarter | region  | sales |
+---------+---------+---------+-------+
| A       | Q1      | Europe  |    10 |
| A       | Q1      | America |    20 |
| A       | Q2      | Europe  |    20 |
| A       | Q2      | America |    50 |
| A       | Q3      | America |    20 |
| A       | Q4      | Europe  |    10 |
| A       | Q4      | America |    30 |
| B       | Q1      | Europe  |    40 |
| B       | Q1      | America |    60 |
| B       | Q2      | Europe  |    20 |
| B       | Q2      | America |    10 |
| B       | Q3      | America |    20 |
| B       | Q4      | Europe  |    10 |
| B       | Q4      | America |    40 |
| C       | Q1      | Europe  |    50 |
| C       | Q1      | America |    60 |
| C       | Q2      | Europe  |    35 |
| C       | Q2      | America |    45 |
+---------+---------+---------+-------+
18 rows in set (0.000 sec)
```
---

# 3️⃣ Basic GROUP BY

```sql
SELECT product, 
       SUM(sales) AS total_sales
FROM sales
GROUP BY product
ORDER BY product;

+---------+-------------+
| product | total_sales |
+---------+-------------+
| A       |         160 |
| B       |         200 |
| C       |         190 |
+---------+-------------+
3 rows in set (0.001 sec)
```

---

# 4️⃣ ROLLUP Examples

## 4.1 ROLLUP by PRODUCT

```sql
SELECT product, 
       SUM(sales) AS total_sales
FROM sales
GROUP BY product WITH ROLLUP
ORDER BY product;

+---------+-------------+
| product | total_sales |
+---------+-------------+
| NULL    |         550 |
| A       |         160 |
| B       |         200 |
| C       |         190 |
+---------+-------------+
4 rows in set (0.001 sec)
```

## 4.2 ROLLUP by (PRODUCT, QUARTER)

```sql
SELECT 
       product, quarter, 
       SUM(sales) AS total_sales
FROM 
       sales
GROUP BY 
       product, quarter WITH ROLLUP
ORDER BY
       product, quarter;
       
+---------+---------+-------------+
| product | quarter | total_sales |
+---------+---------+-------------+
| NULL    | NULL    |         550 |

| A       | NULL    |         160 |
| A       | Q1      |          30 |
| A       | Q2      |          70 |
| A       | Q3      |          20 |
| A       | Q4      |          40 |

| B       | NULL    |         200 |
| B       | Q1      |         100 |
| B       | Q2      |          30 |
| B       | Q3      |          20 |
| B       | Q4      |          50 |

| C       | NULL    |         190 |
| C       | Q1      |         110 |
| C       | Q2      |          80 |
+---------+---------+-------------+
14 rows in set (0.001 sec)
```

## 4.3 ROLLUP by (QUARTER, REGION)

```sql
SELECT 
       quarter, region, 
       SUM(sales) AS total_sales
FROM 
       sales
GROUP BY 
       quarter, region WITH ROLLUP
ORDER BY
       quarter, region;

+---------+---------+-------------+
| quarter | region  | total_sales |
+---------+---------+-------------+
| NULL    | NULL    |         550 |

| Q1      | NULL    |         240 |
| Q1      | America |         140 |
| Q1      | Europe  |         100 |

| Q2      | NULL    |         180 |
| Q2      | America |         105 |
| Q2      | Europe  |          75 |

| Q3      | NULL    |          40 |
| Q3      | America |          40 |

| Q4      | NULL    |          90 |
| Q4      | America |          70 |
| Q4      | Europe  |          20 |
+---------+---------+-------------+
12 rows in set (0.001 sec)

```

## 4.4 ROLLUP by (PRODUCT, QUARTER, REGION)

```sql
SELECT product, quarter, region, 
       SUM(sales) AS total_sales
FROM sales
GROUP BY product, quarter, region WITH ROLLUP
ORDER BY product, quarter, region;

+---------+---------+---------+-------------+
| product | quarter | region  | total_sales |
+---------+---------+---------+-------------+
| NULL    | NULL    | NULL    |         550 |
| A       | NULL    | NULL    |         160 |
| A       | Q1      | NULL    |          30 |
| A       | Q1      | America |          20 |
| A       | Q1      | Europe  |          10 |
| A       | Q2      | NULL    |          70 |
| A       | Q2      | America |          50 |
| A       | Q2      | Europe  |          20 |
| A       | Q3      | NULL    |          20 |
| A       | Q3      | America |          20 |
| A       | Q4      | NULL    |          40 |
| A       | Q4      | America |          30 |
| A       | Q4      | Europe  |          10 |
| B       | NULL    | NULL    |         200 |
| B       | Q1      | NULL    |         100 |
| B       | Q1      | America |          60 |
| B       | Q1      | Europe  |          40 |
| B       | Q2      | NULL    |          30 |
| B       | Q2      | America |          10 |
| B       | Q2      | Europe  |          20 |
| B       | Q3      | NULL    |          20 |
| B       | Q3      | America |          20 |
| B       | Q4      | NULL    |          50 |
| B       | Q4      | America |          40 |
| B       | Q4      | Europe  |          10 |
| C       | NULL    | NULL    |         190 |
| C       | Q1      | NULL    |         110 |
| C       | Q1      | America |          60 |
| C       | Q1      | Europe  |          50 |
| C       | Q2      | NULL    |          80 |
| C       | Q2      | America |          45 |
| C       | Q2      | Europe  |          35 |
+---------+---------+---------+-------------+
32 rows in set (0.001 sec)
```

---

# 5️⃣ What Is CUBE?

CUBE generates ALL combinations of dimensions.

For (product, quarter, region):

- (product, quarter, region)
- (product, quarter)
- (product, region)
- (quarter, region)
- (product)
- (quarter)
- (region)
- (grand total)

⚠ MySQL does NOT support CUBE directly.

---

# 6️⃣ Simulating CUBE Using UNION ALL

```sql
SELECT product, quarter, region, SUM(sales) AS total_sales
FROM sales
GROUP BY product, quarter, region

UNION ALL

SELECT product, quarter, NULL, SUM(sales)
FROM sales
GROUP BY product, quarter

UNION ALL

SELECT product, NULL, region, SUM(sales)
FROM sales
GROUP BY product, region

UNION ALL

SELECT NULL, quarter, region, SUM(sales)
FROM sales
GROUP BY quarter, region

UNION ALL

SELECT product, NULL, NULL, SUM(sales)
FROM sales
GROUP BY product

UNION ALL

SELECT NULL, quarter, NULL, SUM(sales)
FROM sales
GROUP BY quarter

UNION ALL

SELECT NULL, NULL, region, SUM(sales)
FROM sales
GROUP BY region

UNION ALL

SELECT NULL, NULL, NULL, SUM(sales)
FROM sales;
```

output:

```sql
+---------+---------+---------+-------------+
| product | quarter | region  | total_sales |
+---------+---------+---------+-------------+
| A       | Q1      | Europe  |          10 |
| A       | Q1      | America |          20 |
| A       | Q2      | Europe  |          20 |
| A       | Q2      | America |          50 |
| A       | Q3      | America |          20 |
| A       | Q4      | Europe  |          10 |
| A       | Q4      | America |          30 |
| B       | Q1      | Europe  |          40 |
| B       | Q1      | America |          60 |
| B       | Q2      | Europe  |          20 |
| B       | Q2      | America |          10 |
| B       | Q3      | America |          20 |
| B       | Q4      | Europe  |          10 |
| B       | Q4      | America |          40 |
| C       | Q1      | Europe  |          50 |
| C       | Q1      | America |          60 |
| C       | Q2      | Europe  |          35 |
| C       | Q2      | America |          45 |
| A       | Q1      | NULL    |          30 |
| A       | Q2      | NULL    |          70 |
| A       | Q3      | NULL    |          20 |
| A       | Q4      | NULL    |          40 |
| B       | Q1      | NULL    |         100 |
| B       | Q2      | NULL    |          30 |
| B       | Q3      | NULL    |          20 |
| B       | Q4      | NULL    |          50 |
| C       | Q1      | NULL    |         110 |
| C       | Q2      | NULL    |          80 |
| A       | NULL    | Europe  |          40 |
| A       | NULL    | America |         120 |
| B       | NULL    | Europe  |          70 |
| B       | NULL    | America |         130 |
| C       | NULL    | Europe  |          85 |
| C       | NULL    | America |         105 |
| NULL    | Q1      | Europe  |         100 |
| NULL    | Q1      | America |         140 |
| NULL    | Q2      | Europe  |          75 |
| NULL    | Q2      | America |         105 |
| NULL    | Q3      | America |          40 |
| NULL    | Q4      | Europe  |          20 |
| NULL    | Q4      | America |          70 |
| A       | NULL    | NULL    |         160 |
| B       | NULL    | NULL    |         200 |
| C       | NULL    | NULL    |         190 |
| NULL    | Q1      | NULL    |         240 |
| NULL    | Q2      | NULL    |         180 |
| NULL    | Q3      | NULL    |          40 |
| NULL    | Q4      | NULL    |          90 |
| NULL    | NULL    | Europe  |         195 |
| NULL    | NULL    | America |         355 |
| NULL    | NULL    | NULL    |         550 |
+---------+---------+---------+-------------+
51 rows in set (0.001 sec)
```
---

# 7️⃣ Stored Procedure for CUBE

```sql
DELIMITER $$

CREATE PROCEDURE cube_sales()
BEGIN
    SELECT product, quarter, region, SUM(sales) AS total_sales
    FROM sales
    GROUP BY product, quarter, region

    UNION ALL

    SELECT product, quarter, NULL, SUM(sales)
    FROM sales
    GROUP BY product, quarter

    UNION ALL

    SELECT product, NULL, region, SUM(sales)
    FROM sales
    GROUP BY product, region

    UNION ALL

    SELECT NULL, quarter, region, SUM(sales)
    FROM sales
    GROUP BY quarter, region

    UNION ALL

    SELECT product, NULL, NULL, SUM(sales)
    FROM sales
    GROUP BY product

    UNION ALL

    SELECT NULL, quarter, NULL, SUM(sales)
    FROM sales
    GROUP BY quarter

    UNION ALL

    SELECT NULL, NULL, region, SUM(sales)
    FROM sales
    GROUP BY region

    UNION ALL

    SELECT NULL, NULL, NULL, SUM(sales)
    FROM sales;
END$$

DELIMITER ;
```

Call:

```sql
CALL cube_sales();
```

---

# 8️⃣ Key Teaching Points

- ROLLUP = hierarchical aggregation
- CUBE = all dimension combinations
- CUBE grows exponentially (2^n)
- MySQL supports ROLLUP but not CUBE
- CUBE can be simulated via UNION ALL

---

# ✅ End of Tutorial
