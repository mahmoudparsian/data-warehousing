# Insertion Anomaly

a·nom·a·ly : something that deviates from what is standard, normal, or expected.

-----

An **insertion anomaly** occurs when the structure 
of a database table forces you to include unnecessary 
or redundant data to insert a new record, 

or 

prevents you from inserting certain data due to missing information. 

This typically happens when the table is not normalized.

### Example of an Insertion Anomaly

Let's consider a `students_courses` table that is not normalized:

| student_id | student_name | course_id | course_name | instructor_id | instructor_name |
|------------|--------------|-----------|-------------|---------------|-----------------|
| 1          | Alice        | 101       | Math        | 501           | Dr. Smith       |
| 2          | Bob          | 102       | History     | 502           | Dr. Jones       |
| 3          | Charlie      | 101       | Math        | 501           | Dr. Smith       |

### Problem

In this table, each row contains information about a student, the course they are enrolled in, and the instructor for that course. 

#### Insertion Anomaly Scenario

1. **Inserting a New Course Without Any Students:**
   - Suppose you want to add a new course (e.g., course_id 103, course_name 'Science', instructor_id 503, instructor_name 'Dr. Brown').
   - If there are no students enrolled in this course yet, you cannot insert this course because the `students_courses` table requires a `student_id` and `student_name`.

### Solution: Normalization

To avoid this insertion anomaly, we can normalize the table into multiple related tables:



### Populated Normalized Tables

#### Students Table

| student_id | student_name |
|------------|--------------|
| 1          | Alice        |
| 2          | Bob          |
| 3          | Charlie      |

#### Courses Table

| course_id | course_name | instructor_id | instructor_name |
|-----------|-------------|---------------|-----------------|
| 101       | Math        | 501           | Dr. Smith       |
| 102       | History     | 502           | Dr. Jones       |
| 103       | Science     | 503           | Dr. Brown       |

#### Enrollments Table

| student_id | course_id |
|------------|-----------|
| 1          | 101       |
| 2          | 102       |
| 3          | 101       |

### Inserting a New Course Without Any Students

Now, we can insert the new course without requiring any student information:

```sql
INSERT INTO courses (course_id, course_name, instructor_id, instructor_name) 
VALUES
(103, 'Science', 503, 'Dr. Brown');
```

This approach prevents the insertion anomaly by ensuring that each table contains only relevant data and that relationships between entities (students, courses, and enrollments) are properly managed through foreign keys.
