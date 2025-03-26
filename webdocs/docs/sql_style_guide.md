# SQL Style Guide
Keywords
Spell keywords in ALL CAPS:

* SELECT
* WHERE
* GROUP BY
* ...

----

No

~~~sql
select * from foo where x = 17;
~~~

Yes

~~~sql
SELECT x, y, z 
FROM foo 
WHERE x = 17;
~~~

------

No

~~~sql
SELECT * FROM foo JOIN bar ON y = z WHERE x = 17 AND y = 'hello' GROUP BY z HAVING count(*) > 0 ORDER BY y LIMIT 10;
~~~

Yes

~~~sql
SELECT *
FROM foo
JOIN bar ON y = z
WHERE x = 17
AND y = 'hello'
GROUP BY z
HAVING count(*) > 0
ORDER BY y
LIMIT 10;
~~~

-------

No

~~~sql
SELECT a.title,a.year,a.producer
FROM albums AS a
WHERE a.title='Unorthodox Jukebox'
OR a.title='Doo-Wops & Hooligans';
~~~

Yes

~~~sql
SELECT a.title, a.year, a.producer
FROM albums AS a
WHERE (a.title = 'Unorthodox Jukebox') OR
      (a.title = 'Doo-Wops & Hooligans');
~~~

-----

No

~~~sql
CREATE TABLE Course (
  CourseID INT PRIMARY KEY,
  NumberOfStudentsEnrolledInThisClass INT,
  BuildingLocation TEXT,
  MaximumNumberOfStudentCapacity INT
);
~~~

Yes

~~~sql
CREATE TABLE Course (
  id INT PRIMARY KEY,
  num_students INT,
  building TEXT,
  capacity INT
);
~~~

------

Subqueries

* Do not use subqueries in the FROM clause. 
* Instead, use WITH. (Subqueries outside of the FROM clause are fine though.)

No

~~~sql
SELECT * 
FROM (
  SELECT foo, count(*) AS bar
  FROM baz
  GROUP BY foo
) ahh, quux
WHERE ahh.foo = quux.foo
~~~

Yes

~~~sql
WITH yay AS (
  SELECT foo, count(*) AS bar
  FROM baz
  GROUP BY foo
)
SELECT * 
FROM yay, quux
WHERE yay.foo = quux.foo
~~~

