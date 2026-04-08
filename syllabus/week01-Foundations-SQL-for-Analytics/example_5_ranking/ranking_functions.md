# Ranking Functions in DuckDB

* @Author: Mahmoud Parsian
* Last updated date: April 7, 2026


## 1. Introduction to Ranking Functions

DuckDB provides comprehensive window-based ranking 
functions (`rank`, `dense_rank`, `row_number`, 
and `percent_rank`) to order and rank data within 
partitions. 

For faster top-N analysis, DuckDB allows passing an 
integer to `max(column, n)` to return a list of the 
top values. These are used with 

		OVER (PARTITION BY ... ORDER BY ...)

# 2. Key Ranking Window Functions
These functions are used with an OVER clause: 

* `row_number()`: Assigns a unique sequential integer (1, 2, 3, ...) to rows within a partition.

* `rank()`: Ranks rows, allowing gaps (e.g., 1, 2, 2, 4).

* `dense_rank()`: Ranks rows without gaps (e.g., 1, 2, 2, 3).

* `percent_rank()`: Calculates the relative rank: 

# 3. Example 1

## Data

```
% cat players.csv
alex,100
bob,100
jane,100
dave,90
charlie,90
daria,80
dara,80
max,50
frank,40
sasha,30
robert,10
```

# DuckDB in Action

```
% duckdb
DuckDB v1.5.1 (Variegata)
Enter ".help" for usage hints.
memory D create table players as select * from 'players.csv';

memory D select * from players;
┌─────────┬─────────┐
│ column0 │ column1 │
│ varchar │  int64  │
├─────────┼─────────┤
│ alex    │     100 │
│ bob     │     100 │
│ jane    │     100 │
│ dave    │      90 │
│ charlie │      90 │
│ daria   │      80 │
│ dara    │      80 │
│ max     │      50 │
│ frank   │      40 │
│ sasha   │      30 │
│ robert  │      10 │
└─────────┴─────────┘
       11 rows
```

## Rename Column Names

```
memory D ALTER TABLE players RENAME COLUMN column0 to player;

memory D ALTER TABLE players RENAME COLUMN column1 to score;

memory D desc players;
┌────────────────┐
│    players     │
│                │
│ player varchar │
│ score  bigint  │
└────────────────┘

memory D select * from players;
┌─────────┬───────┐
│ player  │ score │
│ varchar │ int64 │
├─────────┼───────┤
│ alex    │   100 │
│ bob     │   100 │
│ jane    │   100 │
│ dave    │    90 │
│ charlie │    90 │
│ daria   │    80 │
│ dara    │    80 │
│ max     │    50 │
│ frank   │    40 │
│ sasha   │    30 │
│ robert  │    10 │
└─────────┴───────┘
      11 rows
```

## Rank (using `rank()`) Players by Score

```
memory D SELECT player, 
                score, 
                RANK() OVER (ORDER BY score DESC) AS rnk 
          FROM players;
┌─────────┬───────┬───────┐
│ player  │ score │  rnk  │
│ varchar │ int64 │ int64 │
├─────────┼───────┼───────┤
│ alex    │   100 │     1 │
│ bob     │   100 │     1 │
│ jane    │   100 │     1 │
│ dave    │    90 │     4 │
│ charlie │    90 │     4 │
│ daria   │    80 │     6 │
│ dara    │    80 │     6 │
│ max     │    50 │     8 │
│ frank   │    40 │     9 │
│ sasha   │    30 │    10 │
│ robert  │    10 │    11 │
└─────────┴───────┴───────┘
  11 rows       3 columns
```

## Rank (using `rank()` and `dense_rank()`) Players by Score

```
memory D SELECT player, 
                score,
                RANK() OVER (ORDER BY score DESC) AS rnk,
                DENSE_RANK() OVER (ORDER BY score DESC) AS rnk2
         FROM players;
┌─────────┬───────┬───────┬───────┐
│ player  │ score │  rnk  │ rnk2  │
│ varchar │ int64 │ int64 │ int64 │
├─────────┼───────┼───────┼───────┤
│ alex    │   100 │     1 │     1 │
│ bob     │   100 │     1 │     1 │
│ jane    │   100 │     1 │     1 │
│ dave    │    90 │     4 │     2 │
│ charlie │    90 │     4 │     2 │
│ daria   │    80 │     6 │     3 │
│ dara    │    80 │     6 │     3 │
│ max     │    50 │     8 │     4 │
│ frank   │    40 │     9 │     5 │
│ sasha   │    30 │    10 │     6 │
│ robert  │    10 │    11 │     7 │
└─────────┴───────┴───────┴───────┘
  11 rows               4 columns
```

## Using `row_number()`

```
memory D select player, score,
         RANK() OVER (ORDER BY score DESC) AS rnk,
         DENSE_RANK() OVER (ORDER BY score DESC) AS rnk2,
         ROW_NUMBER() OVER (ORDER BY score DESC) AS row_num
         FROM players;
┌─────────┬───────┬───────┬───────┬─────────┐
│ player  │ score │  rnk  │ rnk2  │ row_num │
│ varchar │ int64 │ int64 │ int64 │  int64  │
├─────────┼───────┼───────┼───────┼─────────┤
│ alex    │   100 │     1 │     1 │       1 │
│ bob     │   100 │     1 │     1 │       2 │
│ jane    │   100 │     1 │     1 │       3 │
│ dave    │    90 │     4 │     2 │       4 │
│ charlie │    90 │     4 │     2 │       5 │
│ daria   │    80 │     6 │     3 │       6 │
│ dara    │    80 │     6 │     3 │       7 │
│ max     │    50 │     8 │     4 │       8 │
│ frank   │    40 │     9 │     5 │       9 │
│ sasha   │    30 │    10 │     6 │      10 │
│ robert  │    10 │    11 │     7 │      11 │
└─────────┴───────┴───────┴───────┴─────────┘
  11 rows                         5 columns
  
memory D select player, score,
         RANK() OVER (ORDER BY score DESC) AS rnk,
         DENSE_RANK() OVER (ORDER BY score DESC) AS rnk2,
         ROW_NUMBER() OVER (ORDER BY score ASC) AS row_num
         FROM players;
┌─────────┬───────┬───────┬───────┬─────────┐
│ player  │ score │  rnk  │ rnk2  │ row_num │
│ varchar │ int64 │ int64 │ int64 │  int64  │
├─────────┼───────┼───────┼───────┼─────────┤
│ robert  │    10 │    11 │     7 │       1 │
│ sasha   │    30 │    10 │     6 │       2 │
│ frank   │    40 │     9 │     5 │       3 │
│ max     │    50 │     8 │     4 │       4 │
│ daria   │    80 │     6 │     3 │       5 │
│ dara    │    80 │     6 │     3 │       6 │
│ dave    │    90 │     4 │     2 │       7 │
│ charlie │    90 │     4 │     2 │       8 │
│ alex    │   100 │     1 │     1 │       9 │
│ bob     │   100 │     1 │     1 │      10 │
│ jane    │   100 │     1 │     1 │      11 │
└─────────┴───────┴───────┴───────┴─────────┘
  11 rows                         5 columns

memory D select player, score,
         RANK() OVER (ORDER BY score DESC) AS rnk,
         DENSE_RANK() OVER (ORDER BY score DESC) AS rnk2,
         ROW_NUMBER() OVER (ORDER BY score DESC) AS row_num
         FROM players;
┌─────────┬───────┬───────┬───────┬─────────┐
│ player  │ score │  rnk  │ rnk2  │ row_num │
│ varchar │ int64 │ int64 │ int64 │  int64  │
├─────────┼───────┼───────┼───────┼─────────┤
│ alex    │   100 │     1 │     1 │       1 │
│ bob     │   100 │     1 │     1 │       2 │
│ jane    │   100 │     1 │     1 │       3 │
│ dave    │    90 │     4 │     2 │       4 │
│ charlie │    90 │     4 │     2 │       5 │
│ daria   │    80 │     6 │     3 │       6 │
│ dara    │    80 │     6 │     3 │       7 │
│ max     │    50 │     8 │     4 │       8 │
│ frank   │    40 │     9 │     5 │       9 │
│ sasha   │    30 │    10 │     6 │      10 │
│ robert  │    10 │    11 │     7 │      11 │
└─────────┴───────┴───────┴───────┴─────────┘
  11 rows                         5 columns

memory D select player, score,
         RANK() OVER (ORDER BY score) AS rnk,
         DENSE_RANK() OVER (ORDER BY score) AS rnk2,
         ROW_NUMBER() OVER (ORDER BY score) AS row_num
         FROM players;
┌─────────┬───────┬───────┬───────┬─────────┐
│ player  │ score │  rnk  │ rnk2  │ row_num │
│ varchar │ int64 │ int64 │ int64 │  int64  │
├─────────┼───────┼───────┼───────┼─────────┤
│ robert  │    10 │     1 │     1 │       1 │
│ sasha   │    30 │     2 │     2 │       2 │
│ frank   │    40 │     3 │     3 │       3 │
│ max     │    50 │     4 │     4 │       4 │
│ daria   │    80 │     5 │     5 │       5 │
│ dara    │    80 │     5 │     5 │       6 │
│ dave    │    90 │     7 │     6 │       7 │
│ charlie │    90 │     7 │     6 │       8 │
│ alex    │   100 │     9 │     7 │       9 │
│ bob     │   100 │     9 │     7 │      10 │
│ jane    │   100 │     9 │     7 │      11 │
└─────────┴───────┴───────┴───────┴─────────┘
  11 rows                         5 columns
```

## Using `row_number()`

```
memory D select * from players;
┌─────────┬───────┐
│ player  │ score │
│ varchar │ int64 │
├─────────┼───────┤
│ alex    │   100 │
│ bob     │   100 │
│ jane    │   100 │
│ dave    │    90 │
│ charlie │    90 │
│ daria   │    80 │
│ dara    │    80 │
│ max     │    50 │
│ frank   │    40 │
│ sasha   │    30 │
│ robert  │    10 │
└─────────┴───────┘
      11 rows
      
memory D SELECT row_number() OVER ()
         FROM players;
┌──────────────────────┐
│ row_number() OVER () │
│        int64         │
├──────────────────────┤
│                    1 │
│                    2 │
│                    3 │
│                    4 │
│                    5 │
│                    6 │
│                    7 │
│                    8 │
│                    9 │
│                   10 │
│                   11 │
└──────────────────────┘
        11 rows
        
memory D SELECT row_number() OVER (ORDER BY score)
         FROM players;
┌────────────────────────────────────┐
│ row_number() OVER (ORDER BY score) │
│               int64                │
├────────────────────────────────────┤
│                                  1 │
│                                  2 │
│                                  3 │
│                                  4 │
│                                  5 │
│                                  6 │
│                                  7 │
│                                  8 │
│                                  9 │
│                                 10 │
│                                 11 │
└────────────────────────────────────┘
               11 rows

memory D SELECT player, 
                score, 
                row_number()  OVER (ORDER BY score) as rn 
         FROM players;
┌─────────┬───────┬───────┐
│ player  │ score │  rn   │
│ varchar │ int64 │ int64 │
├─────────┼───────┼───────┤
│ robert  │    10 │     1 │
│ sasha   │    30 │     2 │
│ frank   │    40 │     3 │
│ max     │    50 │     4 │
│ daria   │    80 │     5 │
│ dara    │    80 │     6 │
│ dave    │    90 │     7 │
│ charlie │    90 │     8 │
│ alex    │   100 │     9 │
│ bob     │   100 │    10 │
│ jane    │   100 │    11 │
└─────────┴───────┴───────┘
  11 rows       3 columns
  
memory D SELECT player, 
                score, 
                row_number()  OVER (ORDER BY score DESC) as rn
         FROM players;
┌─────────┬───────┬───────┐
│ player  │ score │  rn   │
│ varchar │ int64 │ int64 │
├─────────┼───────┼───────┤
│ alex    │   100 │     1 │
│ bob     │   100 │     2 │
│ jane    │   100 │     3 │
│ dave    │    90 │     4 │
│ charlie │    90 │     5 │
│ daria   │    80 │     6 │
│ dara    │    80 │     7 │
│ max     │    50 │     8 │
│ frank   │    40 │     9 │
│ sasha   │    30 │    10 │
│ robert  │    10 │    11 │
└─────────┴───────┴───────┘
  11 rows       3 columns

memory D .exit
```

# 4. Partition and Ranking

## Data

```
% cat players_with_countries.csv
player,country,score
alex,USA,100
bob,USA,100
max,USA,90
ted,USA,80
frank,USA,40
sasha,USA,30
jane,CANADA,95
joseph,CANADA,95
dave,CANADA,90
ali,CANADA,60
charlie,JAPAN,90
daria,JAPAN,80
dara,JAPAN,80
robert,JAPAN,10
```

## DuckDB in Action

```
% duckdb
DuckDB v1.5.1 (Variegata)
Enter ".help" for usage hints.
memory D CREATE TABLE players 
         as SELECT * from 'players_with_countries.csv';
         
memory D select * from players;
┌─────────┬─────────┬───────┐
│ player  │ country │ score │
│ varchar │ varchar │ int64 │
├─────────┼─────────┼───────┤
│ alex    │ USA     │   100 │
│ bob     │ USA     │   100 │
│ max     │ USA     │    90 │
│ ted     │ USA     │    80 │
│ frank   │ USA     │    40 │
│ sasha   │ USA     │    30 │
│ jane    │ CANADA  │    95 │
│ joseph  │ CANADA  │    95 │
│ dave    │ CANADA  │    90 │
│ ali     │ CANADA  │    60 │
│ charlie │ JAPAN   │    90 │
│ daria   │ JAPAN   │    80 │
│ dara    │ JAPAN   │    80 │
│ robert  │ JAPAN   │    10 │
└─────────┴─────────┴───────┘
  14 rows         3 columns
```

## Rank All Rows based on Score

```                                                 ^
memory D SELECT player,
                country,
                score,
                rank() over (ORDER BY score DESC) as rn
         FROM players;
┌─────────┬─────────┬───────┬───────┐
│ player  │ country │ score │  rn   │
│ varchar │ varchar │ int64 │ int64 │
├─────────┼─────────┼───────┼───────┤
│ alex    │ USA     │   100 │     1 │
│ bob     │ USA     │   100 │     1 │
│ jane    │ CANADA  │    95 │     3 │
│ joseph  │ CANADA  │    95 │     3 │
│ max     │ USA     │    90 │     5 │
│ dave    │ CANADA  │    90 │     5 │
│ charlie │ JAPAN   │    90 │     5 │
│ ted     │ USA     │    80 │     8 │
│ daria   │ JAPAN   │    80 │     8 │
│ dara    │ JAPAN   │    80 │     8 │
│ ali     │ CANADA  │    60 │    11 │
│ frank   │ USA     │    40 │    12 │
│ sasha   │ USA     │    30 │    13 │
│ robert  │ JAPAN   │    10 │    14 │
└─────────┴─────────┴───────┴───────┘
  14 rows                 4 columns
```

## Partition and Rank

```
memory D SELECT player,
                country,
                score,
                rank() over (
                    PARTITION BY country 
                    ORDER BY score DESC) 
                 as rn
         FROM players;
┌─────────┬─────────┬───────┬───────┐
│ player  │ country │ score │  rn   │
│ varchar │ varchar │ int64 │ int64 │
├─────────┼─────────┼───────┼───────┤
│ alex    │ USA     │   100 │     1 │
│ bob     │ USA     │   100 │     1 │
│ max     │ USA     │    90 │     3 │
│ ted     │ USA     │    80 │     4 │
│ frank   │ USA     │    40 │     5 │
│ sasha   │ USA     │    30 │     6 │

│ charlie │ JAPAN   │    90 │     1 │
│ daria   │ JAPAN   │    80 │     2 │
│ dara    │ JAPAN   │    80 │     2 │
│ robert  │ JAPAN   │    10 │     4 │

│ jane    │ CANADA  │    95 │     1 │
│ joseph  │ CANADA  │    95 │     1 │
│ dave    │ CANADA  │    90 │     3 │
│ ali     │ CANADA  │    60 │     4 │
└─────────┴─────────┴───────┴───────┘
  14 rows                 4 columns
```

## Find Top Players From Each Country

```
memory D WITH ranked as (
  SELECT player,
         country,
         score,
         rank() over (
              PARTITION BY country 
              ORDER BY score DESC
         ) as rn
  FROM players
)
SELECT player,
       country,
       score, 
       rn
FROM ranked 
WHERE rn < 2;

┌─────────┬─────────┬───────┬───────┐
│ player  │ country │ score │  rn   │
│ varchar │ varchar │ int64 │ int64 │
├─────────┼─────────┼───────┼───────┤
│ charlie │ JAPAN   │    90 │     1 │
│ jane    │ CANADA  │    95 │     1 │
│ joseph  │ CANADA  │    95 │     1 │
│ alex    │ USA     │   100 │     1 │
│ bob     │ USA     │   100 │     1 │
└─────────┴─────────┴───────┴───────┘
```

## Row Number wit Partition

```
memory D SELECT player,
                country,
                score,
                row_number() over (
                   PARTITION BY country 
                   ORDER BY score DESC
                ) as rn
         FROM players;
┌─────────┬─────────┬───────┬───────┐
│ player  │ country │ score │  rn   │
│ varchar │ varchar │ int64 │ int64 │
├─────────┼─────────┼───────┼───────┤
│ alex    │ USA     │   100 │     1 │
│ bob     │ USA     │   100 │     2 │
│ max     │ USA     │    90 │     3 │
│ ted     │ USA     │    80 │     4 │
│ frank   │ USA     │    40 │     5 │
│ sasha   │ USA     │    30 │     6 │

│ charlie │ JAPAN   │    90 │     1 │
│ daria   │ JAPAN   │    80 │     2 │
│ dara    │ JAPAN   │    80 │     3 │
│ robert  │ JAPAN   │    10 │     4 │

│ jane    │ CANADA  │    95 │     1 │
│ joseph  │ CANADA  │    95 │     2 │
│ dave    │ CANADA  │    90 │     3 │
│ ali     │ CANADA  │    60 │     4 │
└─────────┴─────────┴───────┴───────┘
  14 rows                 4 columns
```

