# Star Schema & OLAP Queries

Given the following star schema tables:

* dimension tables: movies_dim, users_dim, dates_dim

* fact table: ratings_fact.

~~~sql
CREATE TABLE  movies_dim (
    movie_id INTEGER PRIMARY KEY,
    movie_title TEXT,
    genre TEXT,
    release_year INTEGER
);


CREATE TABLE users_dim (
    user_id INTEGER PRIMARY KEY,
    user_name TEXT
);


CREATE TABLE  dates_dim (
    date_id INTEGER PRIMARY KEY,
    rating_date DATE,
    year INTEGER,
    month INTEGER,
    day INTEGER
);


CREATE TABLE  ratings_fact (
    rating_id INTEGER PRIMARY KEY,
    movie_id INTEGER,
    user_id INTEGER,
    rating REAL,
    date_id INTEGER,
    FOREIGN KEY (movie_id) REFERENCES movies_dim(movie_id),
    FOREIGN KEY (user_id) REFERENCES users_dim(user_id),
    FOREIGN KEY (date_id) REFERENCES dates_dim(date_id)
);
~~~


Below are some example OLAP queries involving joins, 
subqueries, ranks with partitions, and top-5 results 
using the provided star schema tables: `movies_dim`, 
`users_dim`, `dates_dim`, and `ratings_fact`.


# OLAP SQL Queries Using Star Schema**

### Query 1: Top 5 Movies by Average Rating
```sql
SELECT
    dm.movie_title,
    AVG(fr.rating) AS avg_rating,
    RANK() OVER (ORDER BY AVG(fr.rating) DESC) AS rating_rank
FROM
    ratings_fact fr
JOIN
    movies_dim dm ON fr.movie_id = dm.movie_id
GROUP BY
    dm.movie_title
ORDER BY
    avg_rating DESC
LIMIT 5;
```

#### Output:
~~~
+--------------------------+------------+-------------+
| movie_title              | avg_rating | rating_rank |
+--------------------------+------------+-------------+
| The Lord of the Rings    |     6.8333 |           1 |
| The Truman Show          |     6.6757 |           2 |
| Iron Man                 |     6.6667 |           3 |
| The Shawshank Redemption |     6.5303 |           4 |
| Finding Nemo             |     6.4839 |           5 |
+--------------------------+------------+-------------+
5 rows in set (0.01 sec)
~~~


---

### Query 2: Top 5 Users by Number of Ratings
```sql
SELECT
    du.user_name,
    COUNT(fr.rating) AS num_ratings,
    RANK() OVER (ORDER BY COUNT(fr.rating) DESC) AS num_ratings_rank
FROM
    ratings_fact fr
JOIN
    users_dim du ON fr.user_id = du.user_id
GROUP BY
    du.user_name
ORDER BY
    num_ratings DESC
LIMIT 5;
```

#### Output:
~~~
+---------------+-------------+------------------+
| user_name     | num_ratings | num_ratings_rank |
+---------------+-------------+------------------+
| Alex Batman   |         179 |                1 |
| Barb Taylor   |         169 |                2 |
| John Doe      |         168 |                3 |
| Jane Williams |         167 |                4 |
| Kun Walter    |         165 |                5 |
+---------------+-------------+------------------+
5 rows in set (0.01 sec)
~~~

---

### Query 3: Top 5 Movies by Total Ratings in 2023
```sql
SELECT
    dm.movie_title,
    COUNT(fr.rating) AS total_ratings,
    RANK() OVER (ORDER BY COUNT(fr.rating) DESC) AS total_ratings_rank
FROM
    ratings_fact fr
JOIN
    movies_dim dm ON fr.movie_id = dm.movie_id
JOIN
    dates_dim dd ON fr.date_id = dd.date_id
WHERE
    dd.year = 2023
GROUP BY
    dm.movie_title
ORDER BY
    total_ratings DESC
LIMIT 5;
```

#### Output:
~~~
+-------------------------+---------------+--------------------+
| movie_title             | total_ratings | total_ratings_rank |
+-------------------------+---------------+--------------------+
| Tangled                 |            47 |                  1 |
| Guardians of the Galaxy |            41 |                  2 |
| Toy Story               |            40 |                  3 |
| Kung Fu Panda           |            39 |                  4 |
| American History X      |            39 |                  4 |
+-------------------------+---------------+--------------------+
5 rows in set (0.04 sec)
~~~
---

### Query 4: Top 3 Movies by Highest Single Rating
```sql
SELECT
    dm.movie_title,
    MAX(fr.rating) AS highest_rating,
    RANK() OVER (ORDER BY MAX(fr.rating) DESC) AS highest_rating_rank
FROM
    ratings_fact fr
JOIN
    movies_dim dm ON fr.movie_id = dm.movie_id
GROUP BY
    dm.movie_title
ORDER BY
    highest_rating DESC
LIMIT 3;
```

#### Output:
~~~
+------------------+----------------+---------------------+
| movie_title      | highest_rating | highest_rating_rank |
+------------------+----------------+---------------------+
| Schindler's List |             10 |                   1 |
| Casablanca       |             10 |                   1 |
| Joker            |             10 |                   1 |
+------------------+----------------+---------------------+
3 rows in set (0.01 sec)
~~~

---



### Query-5. Top-5 Movies by Average Rating per Genre

This query finds the top-5 movies by average rating for each genre.

1. **Top-5 Movies by Average Rating per Genre**:
    - Joins `ratings_fact` and `movies_dim`.
    - Calculates the average rating for each movie.
    - Ranks movies by average rating within each genre.
    - Filters to include only the top-5 movies per genre.

```sql
WITH RankedMovies AS (
    SELECT 
        m.movie_id,
        m.movie_title,
        m.genre,
        AVG(r.rating) AS avg_rating,
        RANK() OVER (PARTITION BY m.genre ORDER BY AVG(r.rating) DESC) AS genre_rank
    FROM 
        ratings_fact r
    JOIN 
        movies_dim m ON r.movie_id = m.movie_id
    GROUP BY 
        m.movie_id, m.movie_title, m.genre
)
SELECT 
    movie_id,
    movie_title,
    genre,
    avg_rating,
    genre_rank
FROM 
    RankedMovies
WHERE 
    genre_rank <= 5
ORDER BY 
    genre, genre_rank;
```

#### output

~~~    
+----------+------------------------------------+-----------+------------+------------+
| movie_id | movie_title                        | genre     | avg_rating | genre_rank |
+----------+------------------------------------+-----------+------------+------------+
|       78 | Iron Man                           | Action    |     6.6667 |          1 |
|        3 | The Dark Knight                    | Action    |     6.1385 |          2 |
|       77 | The Avengers                       | Action    |     6.1250 |          3 |
|       18 | Gladiator                          | Action    |     6.0159 |          4 |
|       30 | Mad Max: Fury Road                 | Action    |     5.9118 |          5 |
|        6 | The Lord of the Rings              | Adventure |     6.8333 |          1 |
|       71 | Indiana Jones and the Last Crusade | Adventure |     6.4231 |          2 |
|       35 | Inglourious Basterds               | Adventure |     6.3231 |          3 |
|       69 | Pirates of the Caribbean           | Adventure |     6.0769 |          4 |
|       24 | Back to the Future                 | Adventure |     6.0615 |          5 |
|       46 | Finding Nemo                       | Animation |     6.4839 |          1 |
|       92 | Tangled                            | Animation |     6.4359 |          2 |
|       95 | Ratatouille                        | Animation |     6.3860 |          3 |
|       94 | Sing                               | Animation |     6.3800 |          4 |
|       89 | The Lego Movie                     | Animation |     6.3455 |          5 |
|       27 | The Wolf of Wall Street            | Biography |     6.1765 |          1 |
|        5 | Schindler's List                   | Biography |     6.1304 |          2 |
|       29 | The Social Network                 | Biography |     6.0492 |          3 |
|       37 | The Imitation Game                 | Biography |     6.0308 |          4 |
|       44 | Braveheart                         | Biography |     5.8868 |          5 |
|       41 | The Truman Show                    | Comedy    |     6.6757 |          1 |
|       42 | The Big Lebowski                   | Comedy    |     6.2963 |          2 |
|       31 | The Grand Budapest Hotel           | Comedy    |     5.9057 |          3 |
|        4 | Pulp Fiction                       | Crime     |     6.4127 |          1 |
|       20 | The Departed                       | Crime     |     6.1667 |          2 |
|       11 | Goodfellas                         | Crime     |     6.0299 |          3 |
|        2 | The Godfather                      | Crime     |     5.8545 |          4 |
|       14 | The Usual Suspects                 | Crime     |     5.7037 |          5 |
|        1 | The Shawshank Redemption           | Drama     |     6.5303 |          1 |
|        9 | Forrest Gump                       | Drama     |     6.2143 |          2 |
|       33 | Parasite                           | Drama     |     5.9623 |          3 |
|       22 | Whiplash                           | Drama     |     5.9286 |          4 |
|       34 | Django Unchained                   | Drama     |     5.8810 |          5 |
|       57 | Insidious                          | Horror    |     6.2879 |          1 |
|       59 | The Conjuring                      | Horror    |     6.2041 |          2 |
|       56 | A Quiet Place                      | Horror    |     6.1636 |          3 |
|       60 | The Exorcist                       | Horror    |     6.0556 |          4 |
|       55 | The Others                         | Horror    |     6.0000 |          5 |
|       54 | The Sixth Sense                    | Mystery   |     6.2568 |          1 |
|       19 | Memento                            | Mystery   |     5.5833 |          2 |
|       28 | Shutter Island                     | Mystery   |     5.0833 |          3 |
|       66 | Silver Linings Playbook            | Romance   |     6.4783 |          1 |
|       52 | Her                                | Romance   |     6.4262 |          2 |
|       53 | Amelie                             | Romance   |     6.2586 |          3 |
|       65 | Pride and Prejudice                | Romance   |     5.9118 |          4 |
|       62 | The Notebook                       | Romance   |     5.8182 |          5 |
|       72 | E.T. the Extra-Terrestrial         | Sci-Fi    |     6.4754 |          1 |
|       74 | Star Trek                          | Sci-Fi    |     6.4412 |          2 |
|       73 | Star Wars: Episode IV A New Hope   | Sci-Fi    |     6.2540 |          3 |
|       36 | Blade Runner 2049                  | Sci-Fi    |     6.1944 |          4 |
|       10 | The Matrix                         | Sci-Fi    |     6.0968 |          5 |
|       51 | The Hunt                           | Thriller  |     6.0588 |          1 |
|       12 | The Silence of the Lambs           | Thriller  |     5.8732 |          2 |
+----------+------------------------------------+-----------+------------+------------+
53 rows in set (0.02 sec)
~~~

### Query-6. Top-5 Users by Number of Ratings per Year

This query finds the top-5 users by the 
number of ratings they provided each year.

2. **Top-5 Users by Number of Ratings per Year**:
    - Joins `ratings_fact`, `users_dim`, and `dates_dim`.
    - Counts the number of ratings each user provided per year.
    - Ranks users by number of ratings within each year.
    - Filters to include only the top-5 users per year.


```sql
WITH RankedUsers AS (
    SELECT 
        u.user_id,
        u.user_name,
        d.year,
        COUNT(r.rating_id) AS num_ratings,
        RANK() OVER (PARTITION BY d.year ORDER BY COUNT(r.rating_id) DESC) AS year_rank
    FROM 
        ratings_fact r
    JOIN 
        users_dim u ON r.user_id = u.user_id
    JOIN 
        dates_dim d ON r.date_id = d.date_id
    GROUP BY 
        u.user_id, u.user_name, d.year
)
SELECT 
    user_id,
    user_name,
    year,
    num_ratings,
    year_rank
FROM 
    RankedUsers
WHERE 
    year_rank <= 5
ORDER BY 
    year, year_rank;
```

#### output:

~~~    
+---------+---------------+------+-------------+-----------+
| user_id | user_name     | year | num_ratings | year_rank |
+---------+---------------+------+-------------+-----------+
|     117 | Alex Batman   | 2022 |          94 |         1 |
|     101 | John Doe      | 2022 |          91 |         2 |
|     134 | Barb Taylor   | 2022 |          88 |         3 |
|     116 | Kun Walter    | 2022 |          87 |         4 |
|     140 | Mo Batman     | 2022 |          87 |         4 |
|     121 | Jane Williams | 2023 |          90 |         1 |
|     123 | Sam Goodman   | 2023 |          87 |         2 |
|     126 | Alan Selman   | 2023 |          85 |         3 |
|     117 | Alex Batman   | 2023 |          85 |         3 |
|     135 | Max Panosian  | 2023 |          84 |         5 |
+---------+---------------+------+-------------+-----------+
10 rows in set (0.10 sec)
~~~

### Query-7. Top-5 Movies by Number of Ratings per Year

This query finds the top-5 movies by the 
number of ratings they received each year.

3. **Top-5 Movies by Number of Ratings per Year**:
    - Joins `ratings_fact`, `movies_dim`, and `dates_dim`.
    - Counts the number of ratings each movie received per year.
    - Ranks movies by number of ratings within each year.
    - Filters to include only the top-5 movies per year.


```sql
WITH RankedMovies AS (
    SELECT 
        m.movie_id,
        m.movie_title,
        d.year,
        COUNT(r.rating_id) AS num_ratings,
        RANK() OVER (PARTITION BY d.year ORDER BY COUNT(r.rating_id) DESC) AS year_rank
    FROM 
        ratings_fact r
    JOIN 
        movies_dim m ON r.movie_id = m.movie_id
    JOIN 
        dates_dim d ON r.date_id = d.date_id
    GROUP BY 
        m.movie_id, m.movie_title, d.year
)
SELECT 
    movie_id,
    movie_title,
    year,
    num_ratings,
    year_rank
FROM 
    RankedMovies
WHERE 
    year_rank <= 5
ORDER BY 
    year, year_rank;
```

#### output

~~~
+----------+-------------------------+------+-------------+-----------+
| movie_id | movie_title             | year | num_ratings | year_rank |
+----------+-------------------------+------+-------------+-----------+
|       54 | The Sixth Sense         | 2022 |          46 |         1 |
|       13 | Se7en                   | 2022 |          45 |         2 |
|       85 | Mulan                   | 2022 |          43 |         3 |
|       45 | Toy Story               | 2022 |          40 |         4 |
|       63 | Casablanca              | 2022 |          40 |         4 |
|       92 | Tangled                 | 2023 |          47 |         1 |
|       76 | Guardians of the Galaxy | 2023 |          41 |         2 |
|       45 | Toy Story               | 2023 |          40 |         3 |
|       43 | American History X      | 2023 |          39 |         4 |
|       90 | Kung Fu Panda           | 2023 |          39 |         4 |
+----------+-------------------------+------+-------------+-----------+
10 rows in set (0.20 sec)
~~~


### Query-8. Top-5 Users by Average Rating Given per Genre

This query finds the top-2 users by average rating 
they have given for each genre.

4. **Top-5 Users by Average Rating Given per Genre**:
    - Joins `ratings_fact`, `users_dim`, and `movies_dim`.
    - Calculates the average rating each user has given per genre.
    - Ranks users by average rating within each genre.
    - Filters to include only the top-2 users per genre.



```sql
WITH RankedUsers AS (
    SELECT 
        u.user_id,
        u.user_name,
        m.genre,
        AVG(r.rating) AS avg_rating,
        RANK() OVER (PARTITION BY m.genre ORDER BY AVG(r.rating) DESC) AS genre_rank
    FROM 
        ratings_fact r
    JOIN 
        users_dim u ON r.user_id = u.user_id
    JOIN 
        movies_dim m ON r.movie_id = m.movie_id
    GROUP BY 
        u.user_id, u.user_name, m.genre
)
SELECT 
    user_id,
    user_name,
    genre,
    avg_rating,
    genre_rank
FROM 
    RankedUsers
WHERE 
    genre_rank <= 2
ORDER BY 
    genre, genre_rank;
```

#### output:

~~~
+---------+-----------------+-----------+------------+------------+
| user_id | user_name       | genre     | avg_rating | genre_rank |
+---------+-----------------+-----------+------------+------------+
|     105 | Max Smith       | Action    |     8.0000 |          1 |
|     120 | Bob Taylor      | Action    |     8.0000 |          1 |
|     101 | John Doe        | Adventure |     7.5000 |          1 |
|     106 | Maggy Taylor    | Adventure |     7.3529 |          2 |
|     139 | Homa Zimmerman  | Animation |     6.8511 |          1 |
|     137 | Jane Seymore    | Animation |     6.8056 |          2 |
|     125 | Sam Altman      | Biography |     7.6667 |          1 |
|     119 | Bob Edward      | Biography |     7.3750 |          2 |
|     139 | Homa Zimmerman  | Comedy    |     9.0000 |          1 |
|     106 | Maggy Taylor    | Comedy    |     8.6667 |          2 |
|     120 | Bob Taylor      | Comedy    |     8.6667 |          2 |
|     130 | Don Knuth       | Crime     |     8.6250 |          1 |
|     126 | Alan Selman     | Crime     |     8.3333 |          2 |
|     115 | Yit Lou         | Drama     |     7.4118 |          1 |
|     101 | John Doe        | Drama     |     7.3846 |          2 |
|     116 | Kun Walter      | Horror    |     8.0000 |          1 |
|     122 | Serena Williams | Horror    |     7.4000 |          2 |
|     102 | Jane Smith      | Mystery   |    10.0000 |          1 |
|     106 | Maggy Taylor    | Mystery   |     7.7500 |          2 |
|     112 | Roger Federer   | Romance   |     7.4286 |          1 |
|     112 | George Fox      | Romance   |     7.4286 |          1 |
|     130 | Don Knuth       | Sci-Fi    |     8.0000 |          1 |
|     111 | Jay Goodman     | Sci-Fi    |     7.7222 |          2 |
|     137 | Jane Seymore    | Thriller  |     9.5000 |          1 |
|     120 | Bob Taylor      | Thriller  |     8.6000 |          2 |
+---------+-----------------+-----------+------------+------------+
25 rows in set (0.02 sec)
~~~

### Query-9. Top-5 Movies by Highest Average Rating in a Specific Year

This query finds the top-5 movies by highest 
average rating in a specific year (e.g., 2023).

**Top-5 Movies by Highest Average Rating in a Specific Year**:
    - Joins `ratings_fact`, `movies_dim`, and `dates_dim`.
    - Calculates the average rating for each movie in a specific year (e.g., 2024).
    - Ranks movies by average rating within the specified year.
    - Filters to include only the top-5 movies by average rating for that year.


```sql
WITH RankedMovies AS (
    SELECT 
        m.movie_id,
        m.movie_title,
        d.year,
        AVG(r.rating) AS avg_rating,
        RANK() OVER (PARTITION BY d.year ORDER BY AVG(r.rating) DESC) AS year_rank
    FROM 
        ratings_fact r
    JOIN 
        movies_dim m ON r.movie_id = m.movie_id
    JOIN 
        dates_dim d ON r.date_id = d.date_id
    WHERE 
        d.year = 2023
    GROUP BY 
        m.movie_id, m.movie_title, d.year
)
SELECT 
    movie_id,
    movie_title,
    year,
    avg_rating,
    year_rank
FROM 
    RankedMovies
WHERE 
    year_rank <= 5
ORDER BY 
    year_rank;
```

#### output:

~~~
+----------+----------------------------+------+------------+-----------+
| movie_id | movie_title                | year | avg_rating | year_rank |
+----------+----------------------------+------+------------+-----------+
|       72 | E.T. the Extra-Terrestrial | 2023 |     7.0690 |         1 |
|       18 | Gladiator                  | 2023 |     6.9000 |         2 |
|       46 | Finding Nemo               | 2023 |     6.8857 |         3 |
|       97 | Madagascar                 | 2023 |     6.8621 |         4 |
|        1 | The Shawshank Redemption   | 2023 |     6.8286 |         5 |
+----------+----------------------------+------+------------+-----------+
5 rows in set (0.03 sec)
~~~


---

### Query-10. **Top 5 Highest Rated Movies (Average Rating)**
Find the top 5 movies with the highest average rating.

```sql
SELECT movie_title, AVG(rating) AS avg_rating
FROM ratings_fact rf
JOIN movies_dim md ON rf.movie_id = md.movie_id
GROUP BY movie_title
ORDER BY avg_rating DESC
LIMIT 5;
```

#### output:

~~~
+-----------------+------------+
| movie_title     | avg_rating |
+-----------------+------------+
| The Dark Knight |     9.5000 |
| Inception       |     9.0000 |
| The Matrix      |     9.0000 |
| Interstellar    |     8.0000 |
| Gladiator       |     8.0000 |
+-----------------+------------+
5 rows in set (0.00 sec)
~~~

---

### Query-11 **Top 5 Most Rated Movies (By Count of Ratings)**
Find the top 5 movies with the highest number of ratings.

```sql
SELECT movie_title, COUNT(rating) AS rating_count
FROM ratings_fact rf
JOIN movies_dim md ON rf.movie_id = md.movie_id
GROUP BY movie_title
ORDER BY rating_count DESC
LIMIT 5;
```

#### output

~~~
+-----------------+--------------+
| movie_title     | rating_count |
+-----------------+--------------+
| Toy Story       |           80 |
| Tangled         |           78 |
| The Truman Show |           74 |
| The Sixth Sense |           74 |
| Casablanca      |           73 |
+-----------------+--------------+
5 rows in set (0.01 sec)
~~~

---

### Query-12. **Ranking Movies by Average Rating (Partitioned by Genre)**
Ranks movies within each genre based on their average rating.

```sql
SELECT genre, movie_title, avg_rating, 
       RANK() OVER (PARTITION BY genre ORDER BY avg_rating DESC) AS rank_in_genre
FROM (
    SELECT md.genre, md.movie_title, AVG(rf.rating) AS avg_rating
    FROM ratings_fact rf
    JOIN movies_dim md ON rf.movie_id = md.movie_id
    GROUP BY md.genre, md.movie_title
) ranked_movies;
```

#### output:

~~~
+-----------+------------------------------------+------------+---------------+
| genre     | movie_title                        | avg_rating | rank_in_genre |
+-----------+------------------------------------+------------+---------------+
| Action    | Iron Man                           |     6.6667 |             1 |
| Action    | The Dark Knight                    |     6.1385 |             2 |
| Action    | The Avengers                       |     6.1250 |             3 |
| Action    | Gladiator                          |     6.0159 |             4 |
| Action    | Mad Max: Fury Road                 |     5.9118 |             5 |
| Adventure | The Lord of the Rings              |     6.8333 |             1 |
| Adventure | Indiana Jones and the Last Crusade |     6.4231 |             2 |
| Adventure | Inglourious Basterds               |     6.3231 |             3 |
| Adventure | Pirates of the Caribbean           |     6.0769 |             4 |
| Adventure | Back to the Future                 |     6.0615 |             5 |
| Adventure | Jurassic Park                      |     5.9077 |             6 |
| Adventure | The Goonies                        |     5.7879 |             7 |
| Adventure | The Revenant                       |     5.7447 |             8 |
| Adventure | The Princess Bride                 |     5.7170 |             9 |
| Animation | Finding Nemo                       |     6.4839 |             1 |
| Animation | Tangled                            |     6.4359 |             2 |
| Animation | Ratatouille                        |     6.3860 |             3 |
| Animation | Sing                               |     6.3800 |             4 |
| Animation | The Lego Movie                     |     6.3455 |             5 |
| Animation | Up                                 |     6.2642 |             6 |
| Animation | Madagascar                         |     6.2500 |             7 |
| Animation | Aladdin                            |     6.2364 |             8 |
| Animation | WALL-E                             |     6.2063 |             9 |
| Animation | Despicable Me                      |     6.1509 |            10 |
| Animation | Frozen                             |     6.1250 |            11 |
| Animation | Toy Story                          |     6.0875 |            12 |
| Animation | Mulan                              |     6.0746 |            13 |
| Animation | Bambi                              |     6.0702 |            14 |
| Animation | Minions                            |     6.0385 |            15 |
| Animation | Happy Feet                         |     6.0213 |            16 |
| Animation | The Incredibles                    |     6.0161 |            17 |
| Animation | The Jungle Book                    |     5.9844 |            18 |
| Animation | Shrek                              |     5.9655 |            19 |
| Animation | Beauty and the Beast               |     5.9153 |            20 |
| Animation | Monsters Inc.                      |     5.7843 |            21 |
| Animation | The Secret Life of Pets            |     5.7759 |            22 |
| Animation | The Lion King                      |     5.7544 |            23 |
| Animation | Zootopia                           |     5.7206 |            24 |
| Animation | How to Train Your Dragon           |     5.5283 |            25 |
| Animation | Coco                               |     5.5208 |            26 |
| Animation | Kung Fu Panda                      |     5.4861 |            27 |
| Animation | Moana                              |     5.3390 |            28 |
| Animation | Spider-Man: Into the Spider-Verse  |     5.1273 |            29 |
| Biography | The Wolf of Wall Street            |     6.1765 |             1 |
| Biography | Schindler's List                   |     6.1304 |             2 |
| Biography | The Social Network                 |     6.0492 |             3 |
| Biography | The Imitation Game                 |     6.0308 |             4 |
| Biography | Braveheart                         |     5.8868 |             5 |
| Biography | The Pianist                        |     5.7571 |             6 |
| Biography | A Beautiful Mind                   |     5.5893 |             7 |
| Biography | The Intouchables                   |     5.4138 |             8 |
| Comedy    | The Truman Show                    |     6.6757 |             1 |
| Comedy    | The Big Lebowski                   |     6.2963 |             2 |
| Comedy    | The Grand Budapest Hotel           |     5.9057 |             3 |
| Crime     | Pulp Fiction                       |     6.4127 |             1 |
| Crime     | The Departed                       |     6.1667 |             2 |
| Crime     | Goodfellas                         |     6.0299 |             3 |
| Crime     | The Godfather                      |     5.8545 |             4 |
| Crime     | The Usual Suspects                 |     5.7037 |             5 |
| Crime     | Se7en                              |     5.4928 |             6 |
| Crime     | Joker                              |     5.1071 |             7 |
| Drama     | The Shawshank Redemption           |     6.5303 |             1 |
| Drama     | Forrest Gump                       |     6.2143 |             2 |
| Drama     | Parasite                           |     5.9623 |             3 |
| Drama     | Whiplash                           |     5.9286 |             4 |
| Drama     | Django Unchained                   |     5.8810 |             5 |
| Drama     | La La Land                         |     5.8382 |             6 |
| Drama     | The Green Mile                     |     5.7872 |             7 |
| Drama     | Saving Private Ryan                |     5.7857 |             8 |
| Drama     | American History X                 |     5.7353 |             9 |
| Drama     | The Prestige                       |     5.7101 |            10 |
| Drama     | Fight Club                         |     5.6429 |            11 |
| Horror    | Insidious                          |     6.2879 |             1 |
| Horror    | The Conjuring                      |     6.2041 |             2 |
| Horror    | A Quiet Place                      |     6.1636 |             3 |
| Horror    | The Exorcist                       |     6.0556 |             4 |
| Horror    | The Others                         |     6.0000 |             5 |
| Horror    | Get Out                            |     5.5625 |             6 |
| Mystery   | The Sixth Sense                    |     6.2568 |             1 |
| Mystery   | Memento                            |     5.5833 |             2 |
| Mystery   | Shutter Island                     |     5.0833 |             3 |
| Romance   | Silver Linings Playbook            |     6.4783 |             1 |
| Romance   | Her                                |     6.4262 |             2 |
| Romance   | Amelie                             |     6.2586 |             3 |
| Romance   | Pride and Prejudice                |     5.9118 |             4 |
| Romance   | The Notebook                       |     5.8182 |             5 |
| Romance   | Gone with the Wind                 |     5.7869 |             6 |
| Romance   | Casablanca                         |     5.5342 |             7 |
| Romance   | Titanic                            |     5.4655 |             8 |
| Sci-Fi    | E.T. the Extra-Terrestrial         |     6.4754 |             1 |
| Sci-Fi    | Star Trek                          |     6.4412 |             2 |
| Sci-Fi    | Star Wars: Episode IV A New Hope   |     6.2540 |             3 |
| Sci-Fi    | Blade Runner 2049                  |     6.1944 |             4 |
| Sci-Fi    | The Matrix                         |     6.0968 |             5 |
| Sci-Fi    | Guardians of the Galaxy            |     6.0000 |             6 |
| Sci-Fi    | Inception                          |     5.9219 |             7 |
| Sci-Fi    | Interstellar                       |     5.8776 |             8 |
| Sci-Fi    | Avatar                             |     5.5893 |             9 |
| Thriller  | The Hunt                           |     6.0588 |             1 |
| Thriller  | The Silence of the Lambs           |     5.8732 |             2 |
+-----------+------------------------------------+------------+---------------+
100 rows in set (0.02 sec)
~~~

---

### Query-13. **Users Who Have Rated the Most Movies**
Find the top 5 users who have provided the most ratings.

```sql
SELECT ud.user_name, COUNT(rf.rating) AS rating_count
FROM ratings_fact rf
JOIN users_dim ud ON rf.user_id = ud.user_id
GROUP BY ud.user_name
ORDER BY rating_count DESC
LIMIT 5;
```

#### output:

~~~
+---------------+--------------+
| user_name     | rating_count |
+---------------+--------------+
| Alex Batman   |          179 |
| Barb Taylor   |          169 |
| John Doe      |          168 |
| Jane Williams |          167 |
| Kun Walter    |          165 |
+---------------+--------------+
5 rows in set (0.01 sec)
~~~
---

### Query-14. **Average Rating Per Year**
Find the average rating given for movies each year.

```sql
SELECT dd.year, AVG(rf.rating) AS avg_rating
FROM ratings_fact rf
JOIN dates_dim dd ON rf.date_id = dd.date_id
GROUP BY dd.year
ORDER BY dd.year;
```

#### output:

~~~
+------+------------+
| year | avg_rating |
+------+------------+
| 2022 |     5.9554 |
| 2023 |     6.0202 |
+------+------------+
2 rows in set (0.00 sec)
~~~

---

### Query-15. **Finding Movies with the Most Ratings in a Given Year (e.g., 2023)**
Find the top 5 most-rated movies in a specific year.

```sql
SELECT md.movie_title, COUNT(rf.rating) AS rating_count
FROM ratings_fact rf
JOIN dates_dim dd ON rf.date_id = dd.date_id
JOIN movies_dim md ON rf.movie_id = md.movie_id
WHERE dd.year = 2023
GROUP BY md.movie_title
ORDER BY rating_count DESC
LIMIT 5;
```

#### output:

~~~
+-------------------------+--------------+
| movie_title             | rating_count |
+-------------------------+--------------+
| Tangled                 |           47 |
| Guardians of the Galaxy |           41 |
| Toy Story               |           40 |
| American History X      |           39 |
| Kung Fu Panda           |           39 |
+-------------------------+--------------+
5 rows in set (0.04 sec)
~~~

---

### Query-16. **Monthly Rating Trend for a Specific Movie**
Find the average rating of a particular movie (`Inception`) for each month.

```sql
SELECT dd.year, dd.month, AVG(rf.rating) AS avg_rating
FROM ratings_fact rf
JOIN dates_dim dd ON rf.date_id = dd.date_id
JOIN movies_dim md ON rf.movie_id = md.movie_id
WHERE md.movie_title = 'Inception'
GROUP BY dd.year, dd.month
ORDER BY dd.year, dd.month;
```

#### output:
~~~
+------+-------+------------+
| year | month | avg_rating |
+------+-------+------------+
| 2022 |     1 |     5.6000 |
| 2022 |     2 |     7.0000 |
| 2022 |     3 |     9.0000 |
| 2022 |     4 |     6.5000 |
| 2022 |     5 |     4.5000 |
| 2022 |     6 |     5.6667 |
| 2022 |     7 |     4.0000 |
| 2022 |     8 |     5.0000 |
| 2022 |     9 |     7.5000 |
| 2022 |    10 |     8.0000 |
| 2022 |    11 |     7.5000 |
| 2022 |    12 |     4.2500 |
| 2023 |     1 |     5.3333 |
| 2023 |     3 |     4.3333 |
| 2023 |     4 |     6.0000 |
| 2023 |     5 |     9.5000 |
| 2023 |     6 |     9.0000 |
| 2023 |     7 |     5.8000 |
| 2023 |     8 |     5.0000 |
| 2023 |     9 |     4.8000 |
| 2023 |    10 |     5.0000 |
| 2023 |    12 |     8.0000 |
+------+-------+------------+
22 rows in set (0.01 sec)
~~~

---

### Query-17. **Top 3 Users Who Rated the Most Movies Each Year**
Find the top 3 users in each year who have rated the most movies.

```sql
SELECT year, user_name, rating_count, rnk
FROM (
    SELECT dd.year, ud.user_name, COUNT(rf.rating) AS rating_count,
           RANK() OVER (PARTITION BY dd.year ORDER BY COUNT(rf.rating) DESC) AS rnk
    FROM ratings_fact rf
    JOIN users_dim ud ON rf.user_id = ud.user_id
    JOIN dates_dim dd ON rf.date_id = dd.date_id
    GROUP BY dd.year, ud.user_name
) ranked_users
WHERE rnk <= 3;
```

#### output:

~~~
+------+---------------+--------------+-----+
| year | user_name     | rating_count | rnk |
+------+---------------+--------------+-----+
| 2022 | Alex Batman   |           94 |   1 |
| 2022 | John Doe      |           91 |   2 |
| 2022 | Barb Taylor   |           88 |   3 |
| 2023 | Jane Williams |           90 |   1 |
| 2023 | Sam Goodman   |           87 |   2 |
| 2023 | Alan Selman   |           85 |   3 |
| 2023 | Alex Batman   |           85 |   3 |
+------+---------------+--------------+-----+
7 rows in set (0.10 sec)
~~~

---

### Query-18. **Movies That Have Never Been Rated**
Find movies that have never received any ratings.

```sql
SELECT md.movie_title
FROM movies_dim md
LEFT JOIN ratings_fact rf ON md.movie_id = rf.movie_id
WHERE rf.rating_id IS NULL;
```

#### output:

~~~
+-------------------------+
| movie_title             |
+-------------------------+
| The Good, Bad, and Ugly |
+-------------------------+
1 row in set (0.00 sec)
~~~

---

### Query-19. **Highest Rated Movie Per Year**
Find the highest-rated movie in each year.

```sql
SELECT year, movie_title, avg_rating
FROM (
    SELECT dd.year, md.movie_title, AVG(rf.rating) AS avg_rating,
           RANK() OVER (PARTITION BY dd.year ORDER BY AVG(rf.rating) DESC) AS rnk
    FROM ratings_fact rf
    JOIN movies_dim md ON rf.movie_id = md.movie_id
    JOIN dates_dim dd ON rf.date_id = dd.date_id
    GROUP BY dd.year, md.movie_title
) yearly_ranked_movies
WHERE rnk = 1;
```

#### output:

~~~
+------+----------------------------+------------+
| year | movie_title                | avg_rating |
+------+----------------------------+------------+
| 2022 | The Lord of the Rings      |     7.1667 |
| 2023 | E.T. the Extra-Terrestrial |     7.0690 |
+------+----------------------------+------------+
2 rows in set (0.19 sec)
~~~

