# GROUP BY ROLLUP in MySQL — Tutorial

	This tutorial teaches **`GROUP BY ROLLUP`** 
	in MySQL using **simple, realistic tables**, 
	step-by-step examples, and clear result 
	explanations.

---

## 1. What is GROUP BY ROLLUP?

	1. `ROLLUP` is an **OLAP extension** to 
	   `GROUP BY` that automatically adds 
	   **subtotal and grand total rows**.

	2. Instead of writing multiple queries 
	   for totals, MySQL computes them 
	   **in one pass**.

---

## 2. Sample Schema (Sales Star-Style)

### 2.1 Create Table

```sql
CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    country VARCHAR(20),
    city VARCHAR(30),
    year INT,
    amount DECIMAL(10,2)
);
```

---

### 2.2 Sample Data

```sql
INSERT INTO sales VALUES
(1,  'USA', 'New York', 2023, 1200),
(2,  'USA', 'New York', 2023, 800),
(3,  'USA', 'Boston', 2023, 600),
(4,  'USA', 'Boston', 2024, 700),
(5,  'Canada', 'Toronto', 2023, 900),
(6,  'Canada', 'Toronto', 2024, 1100),
(7,  'Canada', 'Vancouver', 2024, 500),
(8,  'Canada', 'Vancouver', 2024, 1100),
(9,  'France', 'Paris', 2023, 700),
(10, 'France', 'Paris', 2024, 900);

mysql> select * from sales;
+---------+---------+-----------+------+---------+
| sale_id | country | city      | year | amount  |
+---------+---------+-----------+------+---------+
|       1 | USA     | New York  | 2023 | 1200.00 |
|       2 | USA     | New York  | 2023 |  800.00 |
|       3 | USA     | Boston    | 2023 |  600.00 |
|       4 | USA     | Boston    | 2024 |  700.00 |
|       5 | Canada  | Toronto   | 2023 |  900.00 |
|       6 | Canada  | Toronto   | 2024 | 1100.00 |
|       7 | Canada  | Vancouver | 2024 |  500.00 |
|       8 | Canada  | Vancouver | 2024 | 1100.00 |
|       9 | France  | Paris     | 2023 |  700.00 |
|      10 | France  | Paris     | 2024 |  900.00 |
+---------+---------+-----------+------+---------+
10 rows in set (0.001 sec)
```
---

## 3. Basic GROUP BY (No ROLLUP)

### Revenue by Country

```sql
SELECT country, 
       SUM(amount) AS revenue
FROM sales
GROUP BY country
ORDER BY country;

+---------+---------+
| country | revenue |
+---------+---------+
| Canada  | 3600.00 |
| France  | 1600.00 |
| USA     | 3300.00 |
+---------+---------+
3 rows in set (0.001 sec)
```

---

## 4. GROUP BY ROLLUP (Country Level)

```sql
SELECT country, 
       SUM(amount) AS revenue
FROM sales
GROUP BY country WITH ROLLUP
ORDER BY country;

+---------+---------+
| country | revenue |
+---------+---------+
| NULL    | 8500.00 |  <-- 8500 = 3600 + 1600 + 3300
| Canada  | 3600.00 |
| France  | 1600.00 |
| USA     | 3300.00 |
+---------+---------+
4 rows in set (0.001 sec)
```

---

## 5. Multi-Level ROLLUP

### Country → City

```sql
SELECT country, city, 
       SUM(amount) AS revenue
FROM sales
GROUP BY country, city WITH ROLLUP
ORDER BY country;

+---------+-----------+---------+
| country | city      | revenue |
+---------+-----------+---------+
| NULL    | NULL      | 8500.00 |  <-- 8500 = 3600 + 1600 + 3300

| Canada  | Toronto   | 2000.00 |
| Canada  | Vancouver | 1600.00 |
| Canada  | NULL      | 3600.00 |  <-- 3600 = 2000 + 1600

| France  | Paris     | 1600.00 |
| France  | NULL      | 1600.00 |  <-- 1600 = 1600

| USA     | Boston    | 1300.00 |
| USA     | New York  | 2000.00 |
| USA     | NULL      | 3300.00 |  <-- 3300 = 1300 + 2000
+---------+-----------+---------+
9 rows in set (0.001 sec)

```

### save rolled up table

```sql
CREATE TABLE rolledup_table as 
SELECT country, city, 
       SUM(amount) AS revenue
FROM sales
GROUP BY country, city WITH ROLLUP
ORDER BY country;

mysql> select * from rolledup_table;
+---------+-----------+---------+
| country | city      | revenue |
+---------+-----------+---------+
| NULL    | NULL      | 8500.00 |
| Canada  | Toronto   | 2000.00 |
| Canada  | Vancouver | 1600.00 |
| Canada  | NULL      | 3600.00 |
| France  | Paris     | 1600.00 |
| France  | NULL      | 1600.00 |
| USA     | Boston    | 1300.00 |
| USA     | New York  | 2000.00 |
| USA     | NULL      | 3300.00 |
+---------+-----------+---------+
9 rows in set (0.000 sec)
```

####  find grand total

```sql
SELECT revenue as grand_total
FROM rolledup_table
WHERE country IS NULL AND
      city IS NULL;
+-------------+
| grand_total |
+-------------+
|     8500.00 |
+-------------+
1 row in set (0.000 sec)
```

#### find sub total for USA

```sql
SELECT country, city, revenue as sub_total
FROM rolledup_table
WHERE country = 'USA' AND
      city IS NULL;
+---------+------+-----------+
| country | city | sub_total |
+---------+------+-----------+
| USA     | NULL |   3300.00 |
+---------+------+-----------+
1 row in set (0.000 sec)
```

---

## 6. Understanding NULLs in ROLLUP

- `city = NULL` → subtotal per country
- `country = NULL` → grand total

---

## 7. Label Totals with COALESCE

```sql
SELECT
  COALESCE(country, 'ALL COUNTRIES') AS country,
  COALESCE(city, 'ALL CITIES') AS city,
  SUM(amount) AS revenue
FROM sales
GROUP BY country, city WITH ROLLUP
ORDER BY country;

+---------------+------------+---------+
| country       | city       | revenue |
+---------------+------------+---------+
| ALL COUNTRIES | ALL CITIES | 8500.00 |

| Canada        | Toronto    | 2000.00 |
| Canada        | Vancouver  | 1600.00 |
| Canada        | ALL CITIES | 3600.00 |

| France        | Paris      | 1600.00 |
| France        | ALL CITIES | 1600.00 |

| USA           | Boston     | 1300.00 |
| USA           | New York   | 2000.00 |
| USA           | ALL CITIES | 3300.00 |
+---------------+------------+---------+
9 rows in set, 2 warnings (0.001 sec)
```

---

## 8. Filtering Totals Only

```sql
SELECT country, SUM(amount) AS revenue
FROM sales
GROUP BY country, city WITH ROLLUP
HAVING city IS NULL;

+---------+---------+
| country | revenue |
+---------+---------+
| Canada  | 3600.00 |
| France  | 1600.00 |
| USA     | 3300.00 |
| NULL    | 8500.00 |
+---------+---------+
4 rows in set (0.001 sec)
```

---

## 9. Best Practices

- Order columns from **high → low granularity**
- Use `COALESCE()` for readability
- Avoid using `WHERE` with rollups

---

## 10. Summary

`ROLLUP` simplifies OLAP queries by generating:

- Detail rows
- Subtotals
- Grand totals

in **one SQL query**.


## 11. Example: GROUP BY vs GROUP BY ROLLUP 

	This tutorial demonstrates the difference 
	between **`GROUP BY`** and **`GROUP BY ROLLUP`** 
	using a simple **employees** table.

---

## 1️⃣ Create Employees Table


```sql
CREATE TABLE employees (
  emp_id INT,
  country VARCHAR(20),
  state VARCHAR(20),
  salary INT
);
```

---

## 2️⃣ Populate Sample Data

```sql
INSERT INTO employees VALUES
(1, 'USA', 'CA', 120000),
(2, 'USA', 'CA', 110000),
(3, 'USA', 'NY', 100000),
(4, 'USA', 'NY', 105000),
(5, 'Canada', 'ON', 90000),
(6, 'Canada', 'ON', 95000),
(7, 'Canada', 'BC', 85000),
(8, 'Germany', 'BW', 98000);
```

---

# PART A — One Column: COUNTRY

## 3️⃣ GROUP BY country

```sql
SELECT country, 
       COUNT(*) AS emp_count, 
       SUM(salary) AS total_salary
FROM employees
GROUP BY country;
```

### Output

| country | emp_count | total_salary |
|---------|-----------|--------------|
| USA     | 4         | 435000       |
| Canada  | 3         | 270000       |
| Germany | 1         | 98000        |

---

## 4️⃣ GROUP BY country WITH ROLLUP

```sql
SELECT country, 
       COUNT(*) AS emp_count, 
       SUM(salary) AS total_salary
FROM employees
GROUP BY country WITH ROLLUP;
```

### Output

| country | emp_count | total_salary |
|---------|-----------|--------------|
| USA     | 4         |  435000      |
| Canada  | 3         |  270000      |
| Germany | 1         |   98000      |
| NULL    | 8         |  803000      | ← Grand Total

---

# PART B — Two Columns: COUNTRY + STATE

## 5️⃣ GROUP BY country, state

```sql
SELECT country, 
       state, 
       COUNT(*) AS emp_count, 
       SUM(salary) AS total_salary
FROM employees
GROUP BY country, state;
```

### Output

| country | state | emp_count | total_salary |
|---------|-------|-----------|--------------|
| USA     | CA    | 2         | 230000       |
| USA     | NY    | 2         | 205000       |
| Canada  | ON    | 2         | 185000       |
| Canada  | BC    | 1         |  85000       |
| Germany | BW    | 1         |  98000       |

---

## 6️⃣ GROUP BY country, state WITH ROLLUP

```sql
SELECT country, state, 
       COUNT(*) AS emp_count, 
       SUM(salary) AS total_salary
FROM employees
GROUP BY country, state WITH ROLLUP;
```

### Output


| country | state | emp_count | total_salary |
|---------|-------|-----------|--------------|
| USA     | CA    | 2         | 230000       |
| USA     | NY    | 2         | 205000       |
| USA     | NULL  | 4         | 435000       |
| Canada  | ON    | 2         | 185000       |
| Canada  | BC    | 1         | 85000        |
| Canada  | NULL  | 3         | 270000       |
| Germany | BW    | 1         | 98000        |
| Germany | NULL  | 1         | 98000        |
| NULL    | NULL  | 8         | 803000       |

---

## 7️⃣ Key Observations

- `GROUP BY` → detail rows only
- `ROLLUP` → detail + subtotals + grand total
- `NULL` means **ALL**
- Column order matters: `country → state`

---

## 8️⃣ Summary

```text
GROUP BY:
  country, state → detail rows

GROUP BY ROLLUP:
  country, state → details
  country, ALL   → subtotals
  ALL, ALL       → grand total
```

---

✅ End of tutorial.
