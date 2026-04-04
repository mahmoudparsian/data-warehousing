# Understanding `GROUP BY` in SQL/DuckDB

		The GROUP BY clause in SQL is used to group 
		rows that have the same values in specified 
		columns into a summary row. 
		
		This clause is typically used in conjunction 
		with aggregate functions (like COUNT(), SUM(), 
		AVG(), MIN(), MAX()) to perform calculations on 
		each group of rows, rather than on the entire 
		result set.

		How it works:
		
			**Grouping**: The GROUP BY clause divides the 
			rows of a table into groups based on the 
			values in one or more specified columns. 
			All rows with  identical  values  in  the 
			GROUP BY columns will belong to the same 
			group.

			**Aggregation**: Once the groups are formed, 
			aggregate functions can be applied to each 
			group. These functions then return a single 
			summary value for each group. For example, 
			SUM() will calculate the total for each group, 
			AVG() will calculate the average for each group, 
			and so on.

## 1. Introduction

* There are 3 countries (`USA`, `CANADA`, `GERMANY`).

* There are 2 teams: `RED` and `BLUE`.

* Consider the following table (called `scores`) representing the 
scores for `RED` and `BLUE` teams.

## 2. Database `test.duckdb`

Create a database called `test.duckdb `.

```
duckdb test.duckdb
```

If you have already created this database, then no action is required.

## 3. Table Definition

Use a database called: `test.duckdb`:

```sql
% duckdb test.duckdb
DuckDB v1.5.1 (Variegata)
Enter ".help" for usage hints.

test D CREATE TABLE scores (
          country VARCHAR(20),
          team    VARCHAR(20),
          score   INT
       );

test D desc table scores;
┌─────────────────┐
│     scores      │
│                 │
│ country varchar │
│ team    varchar │
│ score   integer │
└─────────────────┘
```

## 4. Table Population

```sql
test D INSERT INTO scores(country, team, score) VALUES
       ('USA', 'RED', 10),
       ('USA', 'RED', 20),
       ('USA', 'RED', 30),
       ('USA', 'BLUE', 20),
       ('USA', 'BLUE', 40),
       ('USA', 'BLUE', 70),
       ('CANADA', 'RED', 30),
       ('CANADA', 'RED', 60),
       ('CANADA', 'RED', 80),
       ('CANADA', 'BLUE', 10),
       ('CANADA', 'BLUE', 40),
       ('CANADA', 'BLUE', 90),
       ('GERMANY', 'RED', 20),
       ('GERMANY', 'RED', 40),
       ('GERMANY', 'BLUE', 30),
       ('GERMANY', 'BLUE', 70);
test D select count(*) from scores;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│           16 │
└──────────────┘


test D select * from scores;
┌─────────┬─────────┬───────┐
│ country │  team   │ score │
│ varchar │ varchar │ int32 │
├─────────┼─────────┼───────┤
│ USA     │ RED     │    10 │
│ USA     │ RED     │    20 │
│ USA     │ RED     │    30 │
│ USA     │ BLUE    │    20 │
│ USA     │ BLUE    │    40 │
│ USA     │ BLUE    │    70 │
│ CANADA  │ RED     │    30 │
│ CANADA  │ RED     │    60 │
│ CANADA  │ RED     │    80 │
│ CANADA  │ BLUE    │    10 │
│ CANADA  │ BLUE    │    40 │
│ CANADA  │ BLUE    │    90 │
│ GERMANY │ RED     │    20 │
│ GERMANY │ RED     │    40 │
│ GERMANY │ BLUE    │    30 │
│ GERMANY │ BLUE    │    70 │
└─────────┴─────────┴───────┘
  16 rows         3 columns

```

## 5. The `GROUP_CONCAT()` function 

		To understand the GROUP BY in SQL, we 
		will use the GROUP_CONCAT() function.

		The GROUP_CONCAT() function  is an 
		aggregate function that concatenates strings 
		from a group of rows into a single string. 
		This function is particularly useful when 
		you need to combine related data from multiple 
		rows into a more concise format. 

## 6. SQL Queries using GROUP BY 


**1. Find the total score per country and order by total score**

```sql
test D SELECT country,
              SUM(score) AS total_score
       FROM scores
       GROUP BY country
       ORDER BY total_score;
       
┌─────────┬─────────────┐
│ country │ total_score │
│ varchar │   int128    │
├─────────┼─────────────┤
│ GERMANY │         160 │
│ USA     │         190 │
│ CANADA  │         310 │
└─────────┴─────────────┘
```

**2. Find the total score per country (sorted by total score) and show the grouped scores**

```sql
test D SELECT country,
              SUM(score) AS total_score,
              GROUP_CONCAT(score)
       FROM scores
       GROUP BY country
       ORDER BY total_score;
       
┌─────────┬─────────────┬─────────────────────┐
│ country │ total_score │ group_concat(score) │
│ varchar │   int128    │       varchar       │
├─────────┼─────────────┼─────────────────────┤
│ GERMANY │         160 │ 20,40,30,70         │
│ USA     │         190 │ 10,20,30,20,40,70   │
│ CANADA  │         310 │ 30,60,80,10,40,90   │
└─────────┴─────────────┴─────────────────────┘
```


**3. Find the average score per team**

```sql
test D SELECT team,
              AVG(score) AS avg_score
       FROM scores
       GROUP BY team;
       
┌─────────┬───────────┐
│  team   │ avg_score │
│ varchar │  double   │
├─────────┼───────────┤
│ BLUE    │     46.25 │
│ RED     │     36.25 │
└─────────┴───────────┘

```

**4. Find the rounded average score per team**

```sql
test D SELECT team,
              ROUND(AVG(score)) AS avg_score
       FROM scores
       GROUP BY team;
       
┌─────────┬───────────┐
│  team   │ avg_score │
│ varchar │  double   │
├─────────┼───────────┤
│ BLUE    │      46.0 │
│ RED     │      36.0 │
└─────────┴───────────┘
```

**5. Find the rounded average score per team and list of scored grouped**

```sql
test D SELECT team,
              ROUND(AVG(score)) AS avg_score,
              GROUP_CONCAT(score) AS list_of_scores
       FROM scores
       GROUP BY team;
       
┌─────────┬───────────┬─────────────────────────┐
│  team   │ avg_score │     list_of_scores      │
│ varchar │  double   │         varchar         │
├─────────┼───────────┼─────────────────────────┤
│ BLUE    │      46.0 │ 20,40,70,10,40,90,30,70 │
│ RED     │      36.0 │ 10,20,30,30,60,80,20,40 │
└─────────┴───────────┴─────────────────────────┘
```

------

**6. Count the number of games (rows) per country and team**

```sql
test D SELECT country,
              team,
              COUNT(*) AS games
       FROM
              scores
       GROUP BY
              country,
              team;
              
┌─────────┬─────────┬───────┐
│ country │  team   │ games │
│ varchar │ varchar │ int64 │
├─────────┼─────────┼───────┤
│ CANADA  │ BLUE    │     3 │
│ CANADA  │ RED     │     3 │
│ USA     │ BLUE    │     3 │
│ GERMANY │ RED     │     2 │
│ USA     │ RED     │     3 │
│ GERMANY │ BLUE    │     2 │
└─────────┴─────────┴───────┘
```


**7. Find the highest score recorded per country**

```sql
test D SELECT country,
              MAX(score) AS max_score,
              GROUP_CONCAT(score) AS list_of_scores
       FROM scores
       GROUP BY country;
       
┌─────────┬───────────┬───────────────────┐
│ country │ max_score │  list_of_scores   │
│ varchar │   int32   │      varchar      │
├─────────┼───────────┼───────────────────┤
│ USA     │        70 │ 10,20,30,20,40,70 │
│ CANADA  │        90 │ 30,60,80,10,40,90 │
│ GERMANY │        70 │ 20,40,30,70       │
└─────────┴───────────┴───────────────────┘
```

**8. Find the highest score recorded per country and make sure the highest score is more than 80.**

```sql
test D SELECT country,
              MAX(score) AS max_score,
              GROUP_CONCAT(score) AS list_of_scores
       FROM scores
       GROUP BY country
       HAVING max_score > 80;
       
┌─────────┬───────────┬───────────────────┐
│ country │ max_score │  list_of_scores   │
│ varchar │   int32   │      varchar      │
├─────────┼───────────┼───────────────────┤
│ CANADA  │        90 │ 30,60,80,10,40,90 │
└─────────┴───────────┴───────────────────┘
```


**9. Find the lowest score recorded per team**

```sql
test D SELECT team,
              MIN(score) AS min_score
       FROM scores
       GROUP BY team;
       
┌─────────┬───────────┐
│  team   │ min_score │
│ varchar │   int32   │
├─────────┼───────────┤
│ BLUE    │        10 │
│ RED     │        10 │
└─────────┴───────────┘
```

**10. Find the total scores grouped by country and team**

```sql
test D SELECT country, team,
              SUM(score) AS total_score,
              GROUP_CONCAT(score) AS list_of_scores
       FROM scores
       GROUP BY country, team;
       
┌─────────┬─────────┬─────────────┬────────────────┐
│ country │  team   │ total_score │ list_of_scores │
│ varchar │ varchar │   int128    │    varchar     │
├─────────┼─────────┼─────────────┼────────────────┤
│ CANADA  │ RED     │         170 │ 30,60,80       │
│ CANADA  │ BLUE    │         140 │ 10,40,90       │
│ USA     │ RED     │          60 │ 10,20,30       │
│ GERMANY │ BLUE    │         100 │ 30,70          │
│ USA     │ BLUE    │         130 │ 20,40,70       │
│ GERMANY │ RED     │          60 │ 20,40          │
└─────────┴─────────┴─────────────┴────────────────┘
```


**11. Find the average score grouped by country and team**

```sql
test D SELECT country, team,
              AVG(score) AS avg_score
       FROM scores
       GROUP BY country, team;
       
┌─────────┬─────────┬────────────────────┐
│ country │  team   │     avg_score      │
│ varchar │ varchar │       double       │
├─────────┼─────────┼────────────────────┤
│ CANADA  │ BLUE    │ 46.666666666666664 │
│ USA     │ RED     │               20.0 │
│ GERMANY │ BLUE    │               50.0 │
│ CANADA  │ RED     │ 56.666666666666664 │
│ USA     │ BLUE    │ 43.333333333333336 │
│ GERMANY │ RED     │               30.0 │
└─────────┴─────────┴────────────────────┘
```


**12. Find the ROUNDED average score grouped by country and team**

```sql
test D SELECT country, team,
              ROUND(AVG(score)) AS avg_score
       FROM scores
       GROUP BY country, team;
       
┌─────────┬─────────┬───────────┐
│ country │  team   │ avg_score │
│ varchar │ varchar │  double   │
├─────────┼─────────┼───────────┤
│ CANADA  │ RED     │      57.0 │
│ USA     │ RED     │      20.0 │
│ GERMANY │ BLUE    │      50.0 │
│ CANADA  │ BLUE    │      47.0 │
│ USA     │ BLUE    │      43.0 │
│ GERMANY │ RED     │      30.0 │
└─────────┴─────────┴───────────┘
```


**13. Count how many scores are greater than 50 per country**

```sql
test D SELECT country,
              COUNT(*) AS scores_above_50
       FROM scores
       WHERE score > 50
       GROUP BY country;
       
┌─────────┬─────────────────┐
│ country │ scores_above_50 │
│ varchar │      int64      │
├─────────┼─────────────────┤
│ USA     │               1 │
│ CANADA  │               3 │
│ GERMANY │               1 │
└─────────┴─────────────────┘
```

**14. Count how many scores are greater than 50 per country and make sure the number of scores are greater than 2 (per country).**

```sql
test D SELECT country,
              COUNT(*) AS scores_above_50
       FROM scores
       WHERE score > 50
       GROUP BY country
       HAVING scores_above_50 > 2;
       
┌─────────┬─────────────────┐
│ country │ scores_above_50 │
│ varchar │      int64      │
├─────────┼─────────────────┤
│ CANADA  │               3 │
└─────────┴─────────────────┘
```


**15. Find the country with the maximum average score**

```sql
test D SELECT country,
              AVG(score) AS avg_score
       FROM scores
       GROUP BY country
       ORDER BY avg_score DESC
       LIMIT 1;
       
┌─────────┬────────────────────┐
│ country │     avg_score      │
│ varchar │       double       │
├─────────┼────────────────────┤
│ CANADA  │ 51.666666666666664 │
└─────────┴────────────────────┘
```


**16. Compare RED vs BLUE average scores per country**

```sql
test D test D SELECT country,
                     team,
                     ROUND(AVG(score)) AS avg_score
              FROM scores
              GROUP BY
                    country,
                    team;
                    
┌─────────┬─────────┬───────────┐
│ country │  team   │ avg_score │
│ varchar │ varchar │  double   │
├─────────┼─────────┼───────────┤
│ USA     │ RED     │      20.0 │
│ GERMANY │ BLUE    │      50.0 │
│ CANADA  │ RED     │      57.0 │
│ USA     │ BLUE    │      43.0 │
│ GERMANY │ RED     │      30.0 │
│ CANADA  │ BLUE    │      47.0 │
└─────────┴─────────┴───────────┘
```


**17. Compare RED vs BLUE average scores (ROUNDED) per country**

```sql
test D SELECT country, team,
              ROUND(AVG(score)) AS avg_score
       FROM scores
       GROUP BY country, team;
       
┌─────────┬─────────┬───────────┐
│ country │  team   │ avg_score │
│ varchar │ varchar │  double   │
├─────────┼─────────┼───────────┤
│ CANADA  │ BLUE    │      47.0 │
│ CANADA  │ RED     │      57.0 │
│ USA     │ RED     │      20.0 │
│ GERMANY │ BLUE    │      50.0 │
│ USA     │ BLUE    │      43.0 │
│ GERMANY │ RED     │      30.0 │
└─────────┴─────────┴───────────┘
```

**18. Compare RED vs BLUE average scores (ROUNDED) per country and list all scores per country and team**

```sql
test D SELECT country,
              team,
              ROUND(AVG(score)) AS avg_score,
              GROUP_CONCAT(score) AS list_of_scores
       FROM scores
       GROUP BY country,
                team;
                
┌─────────┬─────────┬───────────┬────────────────┐
│ country │  team   │ avg_score │ list_of_scores │
│ varchar │ varchar │  double   │    varchar     │
├─────────┼─────────┼───────────┼────────────────┤
│ CANADA  │ BLUE    │      47.0 │ 10,40,90       │
│ USA     │ RED     │      20.0 │ 10,20,30       │
│ GERMANY │ BLUE    │      50.0 │ 30,70          │
│ USA     │ BLUE    │      43.0 │ 20,40,70       │
│ GERMANY │ RED     │      30.0 │ 20,40          │
│ CANADA  │ RED     │      57.0 │ 30,60,80       │
└─────────┴─────────┴───────────┴────────────────┘
```


---

## Advanced Queries using WITH + Ranking Functions

**19. Find the highest score per country (using ROW_NUMBER)**

```sql
WITH ranked AS 
(
  SELECT country, team, score,
         ROW_NUMBER() OVER (
            PARTITION BY country 
            ORDER BY score DESC) 
         AS row_num
  FROM scores
)
SELECT * 
FROM ranked 
WHERE row_num = 1;

┌─────────┬─────────┬───────┬─────────┐
│ country │  team   │ score │ row_num │
│ varchar │ varchar │ int32 │  int64  │
├─────────┼─────────┼───────┼─────────┤
│ USA     │ BLUE    │    70 │       1 │
│ CANADA  │ BLUE    │    90 │       1 │
│ GERMANY │ BLUE    │    70 │       1 │
└─────────┴─────────┴───────┴─────────┘

```



**20. Find the top 2 scores per country**

```sql
WITH ranked AS 
(
  SELECT country, 
         score,
         RANK() OVER (
           PARTITION BY country
           ORDER BY score DESC) 
         AS rnk
  FROM scores
)
SELECT * 
FROM ranked 
WHERE rnk <= 2;

┌─────────┬───────┬───────┐
│ country │ score │  rnk  │
│ varchar │ int32 │ int64 │
├─────────┼───────┼───────┤
│ GERMANY │    70 │     1 │
│ GERMANY │    40 │     2 │
│ USA     │    70 │     1 │
│ USA     │    40 │     2 │
│ CANADA  │    90 │     1 │
│ CANADA  │    80 │     2 │
└─────────┴───────┴───────┘

```

**21. Compare RED vs BLUE average (rounded) per country with ranking**

```sql
WITH avg_scores AS 
(
  SELECT country, 
         team, 
         ROUND(AVG(score)) AS avg_score
  FROM scores
  GROUP BY country, team
)
SELECT country, team, avg_score,
       RANK() OVER (
          PARTITION BY country 
          ORDER BY avg_score DESC) 
       AS rnk
FROM avg_scores;

┌─────────┬─────────┬───────────┬───────┐
│ country │  team   │ avg_score │  rnk  │
│ varchar │ varchar │  double   │ int64 │
├─────────┼─────────┼───────────┼───────┤
│ CANADA  │ RED     │      57.0 │     1 │
│ CANADA  │ BLUE    │      47.0 │     2 │
│ GERMANY │ BLUE    │      50.0 │     1 │
│ GERMANY │ RED     │      30.0 │     2 │
│ USA     │ BLUE    │      43.0 │     1 │
│ USA     │ RED     │      20.0 │     2 │
└─────────┴─────────┴───────────┴───────┘
```


**22. Rank countries by their total scores**

```sql
WITH totals AS 
(
  SELECT country, SUM(score) AS total_score
  FROM scores
  GROUP BY country
)
SELECT country, total_score,
       DENSE_RANK() OVER (ORDER BY total_score DESC) 
         AS country_rank
FROM totals;

┌─────────┬─────────────┬──────────────┐
│ country │ total_score │ country_rank │
│ varchar │   int128    │    int64     │
├─────────┼─────────────┼──────────────┤
│ CANADA  │         310 │            1 │
│ USA     │         190 │            2 │
│ GERMANY │         160 │            3 │
└─────────┴─────────────┴──────────────┘
```



**23. Find the best performing team overall**

```sql
WITH team_totals AS (
  SELECT team, SUM(score) AS total_score
  FROM scores
  GROUP BY team
)
SELECT team, total_score,
       RANK() OVER (ORDER BY total_score DESC) 
         AS rank_overall
FROM team_totals;

┌─────────┬─────────────┬──────────────┐
│  team   │ total_score │ rank_overall │
│ varchar │   int128    │    int64     │
├─────────┼─────────────┼──────────────┤
│ BLUE    │         370 │            1 │
│ RED     │         290 │            2 │
└─────────┴─────────────┴──────────────┘

```
---
