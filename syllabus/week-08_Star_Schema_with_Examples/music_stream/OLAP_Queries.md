# Star Schema & OLAP Queries

~~~text
Given the following 5 tables in mysql: 

users,
songs,
dates,
devices,
plays

Provide 39 OLAP queries:

   10 simple, 
   10 intermediate, 
   10 complex
   7 queries from Blog (as PDF) 
   2 LEFT JOIN

which use joins, sub-queries, and ranking functions:

use music;

-- users table
-- This table defines users of the music streaming service
--
--	user_id: The unique identifier of the user
--	user_name: The name of the user
--	email: The email address of the user
--	country: The country where the user is located
--	plan: The subscription plan of the user, either ‘free’ or ‘premium’
--
create table users (
	user_id int,
	user_name text,
	email text,
	country text,
	plan text
);

-- songs table
-- This table hits the right notes with details on 
-- the service’s song library. It includes:
--
--	song_id: The unique identifier of the song
--  title: The title of the song
--	artist: The name of the artist who performed the song
--	genre: The genre of the song
--	duration: The duration of the song in seconds
--
create table songs (
 song_id int,
 title text,
 artist text,
 genre text,
 duration int
);


-- dates table 
-- This table stores all required dates
--
-- date_id: as PK
-- play_date: play date of a song
-- year: the year of play_date
-- month: the month of play_date
-- day: the day of play_date
-- quarter: the quarter of play_date as {1, 2, 3, 4} 
--
CREATE TABLE dates (
    date_id INT PRIMARY KEY,
    play_date DATE,
    year INT,
    month INT,  -- {1, 2, ..., 12}
    day INT,    -- {1, 2, ..., 31}
    quarter INT -- {1, 2, 3, 4}
);


-- devices table
--
-- this table store various user devices, which played the song
-- device_id: as PK
-- device: name of the device such as 'mobile', 'desktop', 'ipad', or 'watch'
--
CREATE TABLE devices (
   device_id int,
   device text      
);


-- plays table
-- 
-- And here, we track every time a user plays a song. 
-- It’s filled with information on:
--
--	play_id:   The unique identifier of the play
--	user_id:   The user who played the song
--	song_id:   The song that was played
--	date_id:   The date when the song was played
--	device_id: The device used to play the song, either ‘mobile’ or ‘desktop’, ...
--
--
create table plays (
  play_id int,
  user_id int,
  song_id int,
  date_id int, 
  device_id int      -- 'mobile' or 'desktop' or 'ipad',...
);
~~~


## 🔹 SIMPLE OLAP QUERIES (Level 1)

#### 1. Total plays per user name

```sql
SELECT u.user_name, 
       COUNT(*) AS total_plays
FROM 
     plays p
JOIN 
     users u ON p.user_id = u.user_id
GROUP BY 
     u.user_name;
```

#### 2. Total plays per genre

```sql
SELECT s.genre, 
       COUNT(*) AS total_plays
FROM 
     plays p
JOIN 
     songs s ON p.song_id = s.song_id
GROUP BY 
     s.genre;
```

#### 3. Monthly play counts

```sql
SELECT d.year, 
       d.month, 
       COUNT(*) AS total_plays
FROM 
     plays p
JOIN 
     dates d ON p.date_id = d.date_id
GROUP BY 
     d.year, d.month
ORDER BY 
     d.year, d.month;
```

#### 4. Total duration of songs played by device type

```sql
SELECT d.device, 
       SUM(s.duration) AS total_duration
FROM 
     plays p
JOIN 
     songs s ON p.song_id = s.song_id
JOIN 
     devices d ON p.device_id = d.device_id
GROUP BY 
     d.device;
```

#### 5. Number of users per subscription plan

```sql
SELECT plan, 
       COUNT(*) AS user_count
FROM 
     users
GROUP BY 
     plan;
```


#### 6. Total Plays per User name

```sql
   SELECT u.user_name, 
          COUNT(p.play_id) AS total_plays
   FROM 
        users u
   JOIN 
        plays p ON u.user_id = p.user_id
   GROUP BY 
        u.user_name;
```

#### 7. Most Played Songs per Genre 

```sql
   SELECT s.genre, 
          s.title, 
          COUNT(p.play_id) AS play_count
   FROM 
        songs s
   JOIN 
        plays p ON s.song_id = p.song_id
   GROUP BY 
        s.genre, s.title
   ORDER BY 
        s.genre, play_count DESC;
```

#### 8. Songs Played on Each Device Type 
   
```sql
   SELECT d.device, 
          COUNT(p.play_id) AS play_count
   FROM 
       devices d
   JOIN 
       plays p ON d.device_id = p.device_id
   GROUP BY 
       d.device;
```

#### 9. User Subscription Plans Distribution

```sql
   SELECT plan, 
          COUNT(user_id) AS user_count
   FROM 
       users
   GROUP BY 
       plan;
```

#### 10. Monthly Play Trends  
   
```sql
   SELECT d.year,
          d.month, 
          COUNT(p.play_id) AS monthly_play_count
   FROM 
        dates d
   JOIN 
        plays p ON d.date_id = p.date_id
   GROUP BY 
        d.year, d.month
   ORDER BY 
        d.year, d.month;
```

## 🔹 INTERMEDIATE OLAP QUERIES (Level 2)

#### 11. Top-5 most played songs

```sql
SELECT s.song_id,
       s.title, 
       s.artist, 
       COUNT(*) AS play_count
FROM 
     plays p
JOIN 
     songs s ON p.song_id = s.song_id
GROUP BY 
     s.song_id, s.title, s.artist
ORDER BY 
     play_count DESC
LIMIT 
     5;
```

#### 12. Monthly active users

```sql
SELECT d.year, 
       d.month, 
       COUNT(DISTINCT p.user_id) AS active_users
FROM 
     plays p
JOIN 
     dates d ON p.date_id = d.date_id
GROUP BY 
     d.year, d.month
ORDER BY 
     d.year, d.month;
```

#### 13. Plays by country and device

```sql
SELECT 
      u.country, 
      d.device, 
      COUNT(*) AS play_count
FROM 
     plays p
JOIN 
     users u ON p.user_id = u.user_id
JOIN 
     devices d ON p.device_id = d.device_id
GROUP BY 
     u.country, 
     d.device;
```

#### 14. Average duration per genre

```sql
SELECT s.genre, 
       AVG(s.duration) AS avg_duration
FROM 
     plays p
JOIN 
     songs s ON p.song_id = s.song_id
GROUP BY 
     s.genre;
```

#### 15. Top genres by user plan

```sql
SELECT u.plan, 
       s.genre, 
       COUNT(*) AS genre_count
FROM 
     plays p
JOIN 
     users u ON p.user_id = u.user_id
JOIN 
     songs s ON p.song_id = s.song_id
GROUP BY 
     u.plan, s.genre
ORDER BY 
     u.plan, genre_count DESC;
```

#### 16. Top-5 Most Active Users 

```sql
SELECT u.user_name, 
	  COUNT(p.play_id) AS total_plays
FROM 
	users u
JOIN 
	plays p ON u.user_id = p.user_id
GROUP BY 
	u.user_name
ORDER BY 
	total_plays DESC
LIMIT 
	5;
```

#### 17. Ranked Songs by Popularity Per Genre  

```sql
WITH song_play_data as
(   SELECT s.genre, 
           s.title, 
           COUNT(p.play_id) AS play_count
    FROM songs s
    JOIN plays p ON s.song_id = p.song_id
    GROUP BY s.genre, s.title
) 
SELECT 
   genre, 
   title, 
   play_count,
   RANK() OVER(PARTITION BY genre ORDER BY play_count DESC) AS rnk
FROM 
    song_play_data;
```

#### 18. Users Who Played Songs More Than Average 

```sql
WITH user_play_counts AS (
    SELECT user_id, COUNT(play_id) AS play_count
    FROM plays
    GROUP BY user_id
),
average_play_count AS (
    SELECT AVG(play_count) AS avg_count
    FROM user_play_counts
)
SELECT u.user_name
FROM users u
WHERE u.user_id IN (
    SELECT user_id
    FROM user_play_counts
    WHERE play_count > (SELECT avg_count FROM average_play_count)
);

```

#### 19. Most Popular Device for Playing Songs  

```sql
SELECT d.device, 
       COUNT(p.play_id) AS play_count
FROM 
     devices d
JOIN 
     plays p ON d.device_id = p.device_id
GROUP BY 
     d.device
ORDER BY 
     play_count DESC
LIMIT 
     1;
```

#### 20. User's Favorite Genre Based on Plays

```sql
SELECT u.user_name, 
       s.genre, 
       COUNT(p.play_id) AS play_count
FROM 
     users u
JOIN 
     plays p ON u.user_id = p.user_id
JOIN 
     songs s ON p.song_id = s.song_id
GROUP BY 
     u.user_name, s.genre
ORDER BY 
     u.user_name, play_count DESC;
```

## 🔹 COMPLEX OLAP QUERIES (Level 3)

#### 21. Top artist per country based on play count

```sql
WITH ranked_artists as
(
  SELECT u.country, 
         s.artist, 
         COUNT(*) AS play_count,
         RANK() OVER (PARTITION BY u.country ORDER BY COUNT(*) DESC) AS rnk
  FROM plays p
  JOIN users u ON p.user_id = u.user_id
  JOIN songs s ON p.song_id = s.song_id
  GROUP BY u.country, s.artist
) 
SELECT country, 
       artist, 
       play_count
FROM 
    ranked_artists
WHERE 
    rnk = 1;
```

#### 22. Quarterly growth of total plays

```sql
SELECT year, 
       quarter,
       COUNT(*) AS total_plays,
       LAG(COUNT(*)) OVER (ORDER BY year, quarter) AS previous_quarter_plays,
       (COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY year, quarter)) AS growth
FROM 
     plays p
JOIN 
     dates d ON p.date_id = d.date_id
GROUP BY 
     year, quarter
ORDER BY 
     year, quarter;
```

#### 23. Most loyal users (those with most consistent monthly activity)

```sql
WITH ranked_users AS
(
  SELECT p.user_id, 
         COUNT(DISTINCT CONCAT(d.year, '-', d.month)) AS active_months,
         RANK() OVER (ORDER BY COUNT(DISTINCT CONCAT(d.year, '-', d.month)) DESC) AS rnk
  FROM plays p
  JOIN dates d ON p.date_id = d.date_id
  GROUP BY p.user_id
) 
SELECT user_id, 
       active_months
FROM 
    ranked_users
WHERE 
    rnk <= 5;
```

#### 24. Top-3 genres per quarter

```sql
WITH ranked_genres AS
(
  SELECT d.year, 
         d.quarter, 
         s.genre, 
         COUNT(*) AS play_count,
         DENSE_RANK() OVER (PARTITION BY d.year, d.quarter ORDER BY COUNT(*) DESC) AS rnk
  FROM plays p
  JOIN dates d ON p.date_id = d.date_id
  JOIN songs s ON p.song_id = s.song_id
  GROUP BY d.year, d.quarter, s.genre
) 
SELECT year, 
       quarter, 
       genre, 
       play_count
FROM 
    ranked_genres
WHERE 
    rnk <= 3;
```

#### 25. Top-2 devices used by premium users by play time

```sql
WITH ranked_devices AS
(
  SELECT d.device, 
         SUM(s.duration) AS total_play_time,
         RANK() OVER (ORDER BY SUM(s.duration) DESC) AS rnk
  FROM plays p
  JOIN users u ON p.user_id = u.user_id
  JOIN songs s ON p.song_id = s.song_id
  JOIN devices d ON p.device_id = d.device_id
  WHERE u.plan = 'premium'
  GROUP BY d.device
) 
SELECT device, 
       total_play_time
FROM 
    ranked_devices
WHERE 
    rnk <= 2;
```

#### 26. Top-3 Songs Each Quarter Based on Plays  

```sql
WITH quarterly_data AS
(
   SELECT d.year, 
          d.quarter, 
          s.title, 
          COUNT(p.play_id) AS play_count
   FROM plays p
   JOIN songs s ON p.song_id = s.song_id
   JOIN dates d ON p.date_id = d.date_id
   GROUP BY d.year, d.quarter, s.title
)  
, ranked_play_count AS 
(
   SELECT year,
          quarter, 
          title, 
          play_count, 
	        RANK() OVER(PARTITION BY year, quarter ORDER BY play_count DESC) AS rnk
   FROM 
     quarterly_data
)
SELECT year,
       quarter, 
       title, 
       play_count,
       rnk
FROM 
    ranked_play_count
WHERE 
    rnk <= 3;
```

#### 27. Yearly Genre Popularity Trends  

```sql
WITH genre_trends AS
(
   SELECT d.year, 
          s.genre, 
          COUNT(p.play_id) AS play_count
   FROM plays p
   JOIN songs s ON p.song_id = s.song_id
   JOIN dates d ON p.date_id = d.date_id
   GROUP BY d.year, s.genre
) 
SELECT year, 
       genre, 
       play_count,
	   RANK() OVER(PARTITION BY year ORDER BY play_count DESC) AS rnk
FROM 
    genre_trends;
```

#### 28. Average Play Duration Per Device
 
```sql
SELECT d.device, 
       AVG(s.duration) AS avg_duration
FROM 
     plays p
JOIN 
     devices d ON p.device_id = d.device_id
JOIN 
     songs s ON p.song_id = s.song_id
GROUP BY 
     d.device;
```

#### 29. Users Who Played the Most Unique Songs (top-5)

```sql
SELECT u.user_name, 
       COUNT(DISTINCT p.song_id) AS unique_songs_played
FROM 
     users u
JOIN 
     plays p ON u.user_id = p.user_id
GROUP BY 
     u.user_name
ORDER BY 
     unique_songs_played DESC
LIMIT 
     5;
```

#### 30. Total Plays Across All Devices and Subscription Plans
 
```sql
SELECT u.plan, 
       d.device, 
       COUNT(p.play_id) AS total_plays
FROM 
     plays p
JOIN 
     users u ON p.user_id = u.user_id
JOIN 
     devices d ON p.device_id = d.device_id
GROUP BY 
     u.plan, 
     d.device
ORDER BY 
     u.plan, total_plays DESC;
```

-------

#### 31. Find users (by `user_id` and `user_name`), who have NOT played any music.

We use a `LEFT JOIN` between the `users` and `plays` 
tables and filter out users whose `user_id` appears 
in the plays table. 

Here’s the SQL query to achieve that:

~~~sql
SELECT u.user_id, 
       u.user_name
FROM 
     users u
LEFT JOIN 
     plays p ON u.user_id = p.user_id
WHERE 
     p.user_id IS NULL;
~~~

#### Explanation:

* We perform a LEFT JOIN on the users table with 
  the plays table using the `user_id` column.

* If a user has played any music, their `user_id` 
  will exist in the plays table.

* Users who haven't played any music will have 
  NULL values in the plays table after the join.

* The WHERE `p.user_id IS NULL` condition ensures 
that only those users are selected.

------

#### 32. Find songs, where no one has played that music.

We can use a `LEFT JOIN` between the `songs` 
and `plays` tables to find songs that have never 
been played. 

Here’s the SQL query to achieve that:

~~~sql
SELECT s.song_id, 
       s.title, 
       s.artist
FROM 
     songs s
LEFT JOIN 
     plays p ON s.song_id = p.song_id
WHERE 
     p.song_id IS NULL;
~~~

#### Explanation:

* We perform a LEFT JOIN on the songs table 
  with the plays table using the `song_id` column.

* If a song has been played, its song_id will exist 
  in the plays table.

* Songs that haven't been played will have NULL 
  values in the plays table after the join.

* The `WHERE p.song_id IS NULL` condition filters 
  out songs that have been played, leaving only 
  those that haven’t.
  
------
## Queries from PDF

"Practice SQL JOINS with me: A Hands-on Tutorial"

#### 33. Q1: How many songs did each user play?

~~~sql
SELECT u.user_name, 
       COUNT(p.play_id) AS plays_countFROM  users uINNER JOIN 
      plays p ON u.user_id = p.user_idGROUP BY 
   u.user_name;
~~~

#### 34. Q2: What are the titles and genres of the songs played by Alex?

~~~sql
SELECT s.title, 
       s.genreFROM 
     users uINNER JOIN 
     plays p ON u.user_id = p.user_idINNER JOIN 
     songs s ON p.song_id = s.song_idWHERE 
     u.user_name = 'Alex';

~~~

**better answer:**

~~~sql
SELECT DISTINCT
       s.title, 
       s.genreFROM 
     users uINNER JOIN 
     plays p ON u.user_id = p.user_idINNER JOIN 
     songs s ON p.song_id = s.song_idWHERE 
     u.user_name = 'Alex';

~~~

#### 35. Q3: Which users have played songs by Ed Sheeran?

~~~sql
SELECT u.user_nameFROM 
     users uINNER JOIN 
     plays p ON u.user_id = p.user_idINNER JOIN 
     songs s ON p.song_id = s.song_idWHERE 
     s.artist = 'Ed Sheeran';
~~~

**better answer:**

~~~sql
SELECT DISTINCT
       u.user_nameFROM 
     users uINNER JOIN 
     plays p ON u.user_id = p.user_idINNER JOIN 
     songs s ON p.song_id = s.song_idWHERE 
     s.artist = 'Ed Sheeran';

~~~


#### 36. Q4: Which songs have not been played by any users?

~~~sql
SELECT s.title, 
       s.artistFROM 
     songs sLEFT JOIN 
     plays p ON s.song_id = p.song_idWHERE 
     p.play_id IS NULL;
~~~


#### 37. Q5: Which users have a premium plan and have played songs on a mobile device?

~~~sql
SELECT u.user_name, 
       u.emailFROM 
     users uINNER JOIN  
     plays p ON u.user_id = p.user_id
INNER JOIN 
     devices d ON d.device_id = p.device_idWHERE 
     u.plan = 'premium'   AND 
     d.device = 'mobile';
~~~

**better answer:**

~~~sql
SELECT DISTINCT 
       u.user_name, 
       u.emailFROM 
     users uINNER JOIN  
     plays p ON u.user_id = p.user_id
INNER JOIN 
     devices d ON d.device_id = p.device_idWHERE 
     u.plan = 'premium'   AND 
     d.device = 'mobile';
~~~

#### 38. Q6: Which songs have been played by both `Alex` and `Jane`?

~~~sql
SELECT s.title, s.artistFROM users uINNER JOIN plays p ON u.user_id = p.user_idINNER JOIN songs s ON p.song_id = s.song_idWHERE u.user_name = 'alex'INTERSECTSELECT s.title, s.artistFROM users uINNER JOIN plays p ON u.user_id = p.user_idINNER JOIN songs s ON p.song_id = s.song_idWHERE u.user_name = 'jane';

+-------+--------------+
| title | artist       |
+-------+--------------+
| The 1 | Taylor Swift |
| 2step | Ed Sheeran   |
+-------+--------------+
2 rows in set (0.00 sec)
~~~

#### 38. Q7: Which users have played songs from different genres?

~~~sql
SELECT u.user_name, 
       u.countryFROM users uINNER JOIN plays p ON u.user_id = p.user_idINNER JOIN songs s ON p.song_id = s.song_idGROUP BY 
     u.user_name, 
     u.countryHAVING COUNT(DISTINCT s.genre) > 1;

+-----------+---------+
| user_name | country |
+-----------+---------+
| albert    | FRANCE  |
| alex      | USA     |
| betty     | USA     |
| david     | SPAIN   |
| fiona     | SPAIN   |
| jane      | USA     |
| jeff      | CANADA  |
| max       | CANADA  |
| rafa      | USA     |
| ted       | CANADA  |
| vera      | BRAZIL  |
+-----------+---------+
11 rows in set (0.00 sec)~~~

##  Questions for YouNow that you’ve gotten the hang of SQL joins, 
it’s your turn to put those skills to the test.
There are 3 questions for you to tackle using 
the tables and data from our case study. Here’s 
your chance to show off what you’ve learned!### Q8: Can you figure out how many songs from each genre have been enjoyed by users?
	Here’s a hint to get you started: Dive into the 
	‘songs’ and ‘plays’ tables and link them using 
	the ‘song_id’. Then, group the results by genre 
	with the GROUP BY clause and count them up with 
	the COUNT function. This will give you a clear
	picture of the musical diversity our users are 
	exploring.
	### Q9: Who’s been listening to tunes that stretch beyond 200 seconds?
	Here’s how you can find out: Bring together the 
	‘users’, ‘plays’, and ‘songs’ tables by joining 
	them on ‘user_id’ and ‘song_id’. Use the WHERE 
	clause to sift through the tracks based on their    
	‘duration’. This will help you identify the users 
	who have a taste for longer jams.
	
### Q10: ???

### Q11: ???
