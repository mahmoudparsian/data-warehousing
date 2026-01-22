# Cat Tricks Lab: ROW_NUMBER(), RANK(), DENSE_RANK()

	Consider the following table called cat_tricks 
	with 2 columns: 

			cat_name, num_tricks

	and assume the following 10 records:


			master  2
			gray    3
			pepper  4
			salt    5
			aster   6
			june    6
			pishi   6
			farmer  9
			july    9
			manim   9

## Activities:

	1. create a schema in MySQL

	2. populate table by SQL INSERT

	3. Provide 3 English/SQL queries to teach ROW_NUMBER()

	4. Provide 3 English/SQL queries to teach RANK()

	5. Provide 3 English/SQL queries to teach DENSE_RANK()


## 1. Schema

```sql
CREATE TABLE cat_tricks (
    cat_name VARCHAR(50) PRIMARY KEY,
    num_tricks INT
);

mysql> desc cat_tricks;
+------------+-------------+------+-----+---------+-------+
| Field      | Type        | Null | Key | Default | Extra |
+------------+-------------+------+-----+---------+-------+
| cat_name   | varchar(50) | NO   | PRI | NULL    |       |
| num_tricks | int         | YES  |     | NULL    |       |
+------------+-------------+------+-----+---------+-------+
2 rows in set (0.00 sec)

```

## 2. Populate with Sample Data

```sql
INSERT INTO cat_tricks (cat_name, num_tricks) VALUES
('master', 2),
('gray', 3),
('pepper', 4),
('salt', 5),
('aster', 6),
('june', 6),
('pishi', 6),
('farmer', 9),
('july', 9),
('manim', 9);

mysql> select * from cat_tricks;
+----------+------------+
| cat_name | num_tricks |
+----------+------------+
| aster    |          6 |
| farmer   |          9 |
| gray     |          3 |
| july     |          9 |
| june     |          6 |
| manim    |          9 |
| master   |          2 |
| pepper   |          4 |
| pishi    |          6 |
| salt     |          5 |
+----------+------------+
10 rows in set (0.00 sec)
```

---

## 3. Teaching ROW_NUMBER()

		
		Definition: Assigns a unique, sequential integer 
		to each row within its partition, starting from 1.

		Behavior with ties: It treats each row as distinct, 
		even if the values in the ordering columns are identical. 
		Therefore, it assigns a unique number to every row, 
		regardless of ties.

		Example: If two rows have the same value in the ORDER BY column, 
		ROW_NUMBER() will assign them consecutive, different numbers.


### Query 1 – Assign a unique row number to all cats, ordered by tricks descending
```sql
SELECT cat_name, num_tricks,
       ROW_NUMBER() OVER (ORDER BY num_tricks DESC) AS row_num
FROM cat_tricks;

+----------+------------+---------+
| cat_name | num_tricks | row_num |
+----------+------------+---------+
| farmer   |          9 |       1 |
| july     |          9 |       2 |
| manim    |          9 |       3 |
| aster    |          6 |       4 |
| june     |          6 |       5 |
| pishi    |          6 |       6 |
| salt     |          5 |       7 |
| pepper   |          4 |       8 |
| gray     |          3 |       9 |
| master   |          2 |      10 |
+----------+------------+---------+
10 rows in set (0.00 sec)
```

### Query 2 – Row numbers partitioned by trick count
```sql
SELECT cat_name, num_tricks,
       ROW_NUMBER() OVER (PARTITION BY num_tricks ORDER BY cat_name) AS row_num
FROM cat_tricks
ORDER BY num_tricks, row_num;

+----------+------------+---------+
| cat_name | num_tricks | row_num |
+----------+------------+---------+
| master   |          2 |       1 |
| gray     |          3 |       1 |
| pepper   |          4 |       1 |
| salt     |          5 |       1 |
| aster    |          6 |       1 |
| june     |          6 |       2 |
| pishi    |          6 |       3 |
| farmer   |          9 |       1 |
| july     |          9 |       2 |
| manim    |          9 |       3 |
+----------+------------+---------+
10 rows in set (0.00 sec)
```

### Query 3 – Top 3 cats by number of tricks
```sql
WITH ranked AS (
  SELECT cat_name, 
         num_tricks,
         ROW_NUMBER() OVER (ORDER BY num_tricks DESC) AS row_num
  FROM cat_tricks
)
SELECT * FROM ranked 
WHERE row_num <= 3;

+----------+------------+---------+
| cat_name | num_tricks | row_num |
+----------+------------+---------+
| farmer   |          9 |       1 |
| july     |          9 |       2 |
| manim    |          9 |       3 |
+----------+------------+---------+
3 rows in set (0.00 sec)
```

---

## 4. Teaching RANK()

		Definition: Assigns a rank to each row within 
		its partition. Rows with identical values in 
		the ORDER BY columns receive the same rank.

		Behavior with ties: If there are ties, RANK() 
		assigns the same rank to all tied rows. It then 
		skips the subsequent rank numbers, creating gaps 
		in the ranking sequence.

		Example: If two rows are tied for rank 1, the next 
		distinct rank will be 3 (skipping rank 2).

### Query 1 – Rank cats by number of tricks (ties get same rank, with gaps)
```sql
SELECT cat_name, 
       num_tricks,
       RANK() OVER (ORDER BY num_tricks DESC) AS rnk
FROM cat_tricks;

+----------+------------+-----+
| cat_name | num_tricks | rnk |
+----------+------------+-----+
| farmer   |          9 |   1 |
| july     |          9 |   1 |
| manim    |          9 |   1 |
| aster    |          6 |   4 |
| june     |          6 |   4 |
| pishi    |          6 |   4 |
| salt     |          5 |   7 |
| pepper   |          4 |   8 |
| gray     |          3 |   9 |
| master   |          2 |  10 |
+----------+------------+-----+
10 rows in set (0.00 sec)
```

### Query 2 – Rank within cats grouped by trick count
```sql
SELECT cat_name, 
       num_tricks,
       RANK() OVER (PARTITION BY num_tricks ORDER BY cat_name) AS rnk
FROM cat_tricks
ORDER BY num_tricks, rnk;

+----------+------------+-----+
| cat_name | num_tricks | rnk |
+----------+------------+-----+
| master   |          2 |   1 |
| gray     |          3 |   1 |
| pepper   |          4 |   1 |
| salt     |          5 |   1 |
| aster    |          6 |   1 |
| june     |          6 |   2 |
| pishi    |          6 |   3 |
| farmer   |          9 |   1 |
| july     |          9 |   2 |
| manim    |          9 |   3 |
+----------+------------+-----+
10 rows in set (0.00 sec)
```

### Query 3 – Top 2 ranks only
```sql
WITH ranked AS (
  SELECT cat_name, 
         num_tricks,
         RANK() OVER (ORDER BY num_tricks DESC) AS rnk
  FROM cat_tricks
)
SELECT * FROM ranked 
WHERE rnk <= 2;

+----------+------------+-----+
| cat_name | num_tricks | rnk |
+----------+------------+-----+
| farmer   |          9 |   1 |
| july     |          9 |   1 |
| manim    |          9 |   1 |
+----------+------------+-----+
3 rows in set (0.00 sec)

```

---

## 5. Teaching DENSE_RANK() -- (no gaps in ranking)

		Definition: Assigns a rank to each row within 
		its partition, similar to RANK(), where rows 
		with identical values in the ORDER BY columns 
		receive the same rank.

		Behavior with ties: Unlike RANK(), DENSE_RANK() 
		does not skip rank numbers after ties. It assigns 
		the next consecutive rank number to the next distinct value.

		Example: If two rows are tied for rank 1, the next 
		distinct rank will be 2 (no gap).


### Query 1 – Dense rank cats by number of tricks (no gaps in ranking)
```sql
SELECT cat_name, 
       num_tricks,
       DENSE_RANK() OVER (ORDER BY num_tricks DESC) AS dense_rnk
FROM cat_tricks;

+----------+------------+-----------+
| cat_name | num_tricks | dense_rnk |
+----------+------------+-----------+
| farmer   |          9 |         1 |
| july     |          9 |         1 |
| manim    |          9 |         1 |
| aster    |          6 |         2 |
| june     |          6 |         2 |
| pishi    |          6 |         2 |
| salt     |          5 |         3 |
| pepper   |          4 |         4 |
| gray     |          3 |         5 |
| master   |          2 |         6 |
+----------+------------+-----------+
10 rows in set (0.00 sec)
```

### Query 2 – Dense rank partitioned by trick count -- (no gaps in ranking)
```sql
SELECT cat_name, 
       num_tricks,
       DENSE_RANK() OVER (PARTITION BY num_tricks ORDER BY cat_name) AS dense_rnk
FROM cat_tricks
ORDER BY num_tricks, dense_rnk;

+----------+------------+-----------+
| cat_name | num_tricks | dense_rnk |
+----------+------------+-----------+
| master   |          2 |         1 |
| gray     |          3 |         1 |
| pepper   |          4 |         1 |
| salt     |          5 |         1 |
| aster    |          6 |         1 |
| june     |          6 |         2 |
| pishi    |          6 |         3 |
| farmer   |          9 |         1 |
| july     |          9 |         2 |
| manim    |          9 |         3 |
+----------+------------+-----------+
10 rows in set (0.00 sec)
```

### Query 3 – Find cats in the top 2 dense ranks -- (no gaps in ranking)
```sql
WITH ranked AS (
  SELECT cat_name, 
         num_tricks,
         DENSE_RANK() OVER (ORDER BY num_tricks DESC) AS dense_rnk
  FROM cat_tricks
)
SELECT * 
FROM ranked 
WHERE dense_rnk <= 2;

+----------+------------+-----------+
| cat_name | num_tricks | dense_rnk |
+----------+------------+-----------+
| farmer   |          9 |         1 |
| july     |          9 |         1 |
| manim    |          9 |         1 |
| aster    |          6 |         2 |
| june     |          6 |         2 |
| pishi    |          6 |         2 |
+----------+------------+-----------+
6 rows in set (0.00 sec)
```

# One More Example on Ranking Function

-- Create the scores table

~~~sql
CREATE TABLE scores (
    student_id INT,
    subject VARCHAR(50),
    score INT
);
~~~

-- Insert data into the scores table

~~~sql
INSERT INTO scores (student_id, subject, score) VALUES
(1, 'Math', 95),
(2, 'Math', 85),
(3, 'Math', 95),
(4, 'Math', 75),
(1, 'Science', 90),
(2, 'Science', 88),
(3, 'Science', 90);

mysql> select * from scores;
+------------+---------+-------+
| student_id | subject | score |
+------------+---------+-------+
|          1 | Math    |    95 |
|          2 | Math    |    85 |
|          3 | Math    |    95 |
|          4 | Math    |    75 |
|          1 | Science |    90 |
|          2 | Science |    88 |
|          3 | Science |    90 |
+------------+---------+-------+
7 rows in set (0.00 sec)
~~~

## Query Example

	To assign ranks to students based on their 
	scores in each subject, you could use:

~~~sql
SELECT 
    student_id,
    subject,
    score,
    RANK() OVER (PARTITION BY subject ORDER BY score DESC) AS ranking,
    DENSE_RANK() OVER (PARTITION BY subject ORDER BY score DESC) AS denseRank,
    ROW_NUMBER() OVER (PARTITION BY subject ORDER BY score DESC) AS rowNumber
FROM 
    scores;
    
+------------+---------+-------+---------+-----------+-----------+
| student_id | subject | score | ranking | denseRank | rowNumber |
+------------+---------+-------+---------+-----------+-----------+
|          1 | Math    |    95 |       1 |         1 |         1 |
|          3 | Math    |    95 |       1 |         1 |         2 |
|          2 | Math    |    85 |       3 |         2 |         3 |
|          4 | Math    |    75 |       4 |         3 |         4 |
|          1 | Science |    90 |       1 |         1 |         1 |
|          3 | Science |    90 |       1 |         1 |         2 |
|          2 | Science |    88 |       3 |         2 |         3 |
+------------+---------+-------+---------+-----------+-----------+
7 rows in set (0.01 sec)
~~~