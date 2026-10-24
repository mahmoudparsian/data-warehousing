-- Star Schema & OLAP Queries (DuckDB)
-- Run:  duckdb movies_dw.duckdb < step_3_OLAP_queries/OLAP_Queries_DuckDB.sql

-- Query 1: Top 5 Movies by Average Rating
SELECT
    M.movie_title,
    AVG(R.rating) AS avg_rating,
    RANK() OVER (ORDER BY AVG(R.rating) DESC) AS rating_rank
FROM
    ratings_fact R
JOIN
    movies_dim M ON R.movie_id = M.movie_id
GROUP BY
    M.movie_id, M.movie_title
ORDER BY
    avg_rating DESC
LIMIT 5;

-- Query 2: Top 5 Users by Number of Ratings
SELECT
    U.user_name,
    COUNT(R.rating) AS num_ratings,
    RANK() OVER (ORDER BY COUNT(R.rating) DESC) AS num_ratings_rank
FROM
    ratings_fact R
JOIN
    users_dim U ON R.user_id = U.user_id
GROUP BY
    U.user_name
ORDER BY
    num_ratings DESC
LIMIT 5;

-- Query 3: Top 5 Movies by Total Ratings in 2023
SELECT
    M.movie_title,
    COUNT(R.rating) AS total_ratings,
    RANK() OVER (ORDER BY COUNT(R.rating) DESC) AS total_ratings_rank
FROM
    ratings_fact R
JOIN
    movies_dim M ON R.movie_id = M.movie_id
JOIN
    dates_dim D ON R.date_id = D.date_id
WHERE
    D.year = 2023
GROUP BY
    M.movie_id, M.movie_title
ORDER BY
    total_ratings DESC
LIMIT 5;

-- Query 4: Top 3 Movies by Highest Single Rating
SELECT
    M.movie_title,
    MAX(R.rating) AS highest_rating,
    RANK() OVER (ORDER BY MAX(R.rating) DESC) AS highest_rating_rank
FROM
    ratings_fact R
JOIN
    movies_dim M ON R.movie_id = M.movie_id
GROUP BY
    M.movie_id, M.movie_title
ORDER BY
    highest_rating DESC
LIMIT 3;

-- Query-5. Top-5 Movies by Average Rating per Genre
WITH RankedMovies AS (
    SELECT 
        M.movie_id,
        M.movie_title,
        M.genre,
        AVG(R.rating) AS avg_rating,
        RANK() OVER (PARTITION BY M.genre ORDER BY AVG(R.rating) DESC) AS genre_rank
    FROM 
        ratings_fact R
    JOIN 
        movies_dim M ON R.movie_id = M.movie_id
    GROUP BY 
        M.movie_id, M.movie_title, M.genre
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

-- Query-5. Top-5 Movies by Average Rating per Genre
WITH AVG_Rating_Movies AS (
    SELECT 
        M.movie_id,
        M.movie_title,
        M.genre,
        AVG(R.rating) AS avg_rating,
    FROM 
        ratings_fact R
    JOIN 
        movies_dim M ON R.movie_id = M.movie_id
    GROUP BY 
        M.movie_id, M.movie_title, M.genre
),
Ranked_Movies AS (
    SELECT 
        movie_id,
        movie_title,
        genre,
        avg_rating,
        RANK() OVER (PARTITION BY genre ORDER BY avg_rating DESC) AS genre_rank
    FROM 
        AVG_Rating_Movies
)
SELECT 
    movie_id,
    movie_title,
    genre,
    avg_rating,
    genre_rank
FROM 
    Ranked_Movies
WHERE 
    genre_rank <= 5
ORDER BY 
    genre, genre_rank;

-- Query-6. Top-5 Users by Number of Ratings per Year
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

-- Query-7. Top-5 Movies by Number of Ratings per Year
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

-- Query-8. Top-5 Users by Average Rating Given per Genre
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

-- Query-9. Top-5 Movies by Highest Average Rating in a Specific Year
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

-- Query-10. **Top 5 Highest Rated Movies (Average Rating)**
SELECT movie_title, AVG(rating) AS avg_rating
FROM ratings_fact R
JOIN movies_dim M ON R.movie_id = M.movie_id
GROUP BY M.movie_id, movie_title
ORDER BY avg_rating DESC
LIMIT 5;

-- Query-11 **Top 5 Most Rated Movies (By Count of Ratings)**
SELECT movie_title, COUNT(rating) AS rating_count
FROM ratings_fact R
JOIN movies_dim M ON R.movie_id = M.movie_id
GROUP BY M.movie_id, movie_title
ORDER BY rating_count DESC
LIMIT 5;

-- Query-12. **Ranking Movies by Average Rating (Partitioned by Genre)**
SELECT genre, movie_title, avg_rating, 
       RANK() OVER (PARTITION BY genre ORDER BY avg_rating DESC) AS rank_in_genre
FROM (
    SELECT M.genre, M.movie_title, AVG(R.rating) AS avg_rating
    FROM ratings_fact R
    JOIN movies_dim M ON R.movie_id = M.movie_id
    GROUP BY M.genre, M.movie_id, M.movie_title
) ranked_movies;

-- Query-13. **Users Who Have Rated the Most Movies**
SELECT U.user_name, COUNT(R.rating) AS rating_count
FROM ratings_fact R
JOIN users_dim U ON R.user_id = U.user_id
GROUP BY U.user_name
ORDER BY rating_count DESC
LIMIT 5;

-- Query-14. **Average Rating Per Year**
SELECT D.year, AVG(R.rating) AS avg_rating
FROM ratings_fact R
JOIN dates_dim D ON R.date_id = D.date_id
GROUP BY D.year
ORDER BY D.year;

-- Query-15. **Finding Movies with the Most Ratings in a Given Year (e.g., 2023)**
SELECT M.movie_title, COUNT(R.rating) AS rating_count
FROM ratings_fact R
JOIN dates_dim D ON R.date_id = D.date_id
JOIN movies_dim M ON R.movie_id = M.movie_id
WHERE D.year = 2023
GROUP BY M.movie_id, M.movie_title
ORDER BY rating_count DESC
LIMIT 5;

-- Query-16. **Monthly Rating Trend for a Specific Movie**
SELECT D.year, D.month, AVG(R.rating) AS avg_rating
FROM ratings_fact R
JOIN dates_dim D ON R.date_id = D.date_id
JOIN movies_dim M ON R.movie_id = M.movie_id
WHERE M.movie_title = 'Inception'
GROUP BY D.year, D.month
ORDER BY D.year, D.month;

-- Query-17. **Top 3 Users Who Rated the Most Movies Each Year**
SELECT year, user_name, rating_count, rnk
FROM (
    SELECT D.year, 
           U.user_name, 
           COUNT(R.rating) AS rating_count,
           RANK() OVER (PARTITION BY D.year ORDER BY COUNT(R.rating) DESC) AS rnk
    FROM ratings_fact R
    JOIN users_dim U ON R.user_id = U.user_id
    JOIN dates_dim D ON R.date_id = D.date_id
    GROUP BY D.year, U.user_name
) ranked_users
WHERE rnk <= 3;

-- Query-18. **Movies That Have Never Been Rated**
SELECT M.movie_title
FROM movies_dim M
LEFT JOIN ratings_fact R ON M.movie_id = R.movie_id
WHERE R.rating_id IS NULL;

-- Query-19. **Highest Rated Movie Per Year**
SELECT year, movie_title, avg_rating
FROM (
    SELECT D.year, 
           M.movie_title, 
           AVG(R.rating) AS avg_rating,
           RANK() OVER (PARTITION BY D.year ORDER BY AVG(R.rating) DESC) AS rnk
    FROM ratings_fact R
    JOIN movies_dim M ON  R.movie_id = M.movie_id
    JOIN dates_dim D  ON  R.date_id = D.date_id
    GROUP BY D.year, M.movie_id, M.movie_title
) yearly_ranked_movies
WHERE rnk = 1;

-- Query-20: Common Movies Between Users:
WITH active AS (          -- the 2,000 users with the most ratings
    SELECT user_id
    FROM ratings_fact
    GROUP BY user_id
    ORDER BY COUNT(*) DESC, user_id
    LIMIT 2000
),
r AS (
    SELECT DISTINCT user_id, movie_id
    FROM ratings_fact
    WHERE user_id IN (SELECT user_id FROM active)
)
SELECT
    r1.user_id AS user1,
    r2.user_id AS user2,
    COUNT(*)   AS common_movies
FROM r r1
JOIN r r2
  ON r1.movie_id = r2.movie_id
 AND r1.user_id < r2.user_id   -- each pair only once
GROUP BY r1.user_id, r2.user_id
HAVING COUNT(*) >= 4
ORDER BY common_movies DESC, user1, user2;
