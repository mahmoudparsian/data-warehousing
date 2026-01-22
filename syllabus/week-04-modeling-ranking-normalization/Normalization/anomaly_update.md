# Update Anomaly

An **update anomaly** occurs when redundant 
data in a relational table requires multiple 
rows to be updated to maintain data consistency.   
This typically happens when the table is not 
normalized, leading to data redundancy and 
potential inconsistencies.

### Example of an Update Anomaly

Let's consider a table `employees_projects` that is not normalized:

| employee_id | employee_name | project_id | project_name | project_manager |
|-------------|---------------|------------|--------------|-----------------|
| 1           | Alice         | 101        | Project A    | John            |
| 2           | Bob           | 102        | Project B    | Sarah           |
| 3           | Charlie       | 101        | Project A    | John            |
| 4           | David         | 103        | Project C    | Alice           |
| 5           | Eve           | 102        | Project B    | Sarah           |

### Problems with the Initial Table

- The table contains redundant data. For example, `project_name` and `project_manager` are repeated for each employee working on the same project.
- This redundancy can lead to update anomalies.

### Update Anomaly Scenario

1. **Updating the Project Manager:**
   - Suppose the manager of `Project B` changes from Sarah to Michael.
   - You need to update multiple rows in the table to ensure all occurrences of `Project B` reflect this change.

### Potential Issues

- If you forget to update one of the rows or make a mistake, the data becomes inconsistent.
- This can lead to inaccurate information being stored in the database.

### Solution: Normalization

To avoid this update anomaly, we can normalize the table by creating separate tables for employees, projects, and assignments.

### Step 1: Create Separate Tables

1. **Employees Table**:
    - Contains employee-specific information.
    - `employee_id` is the primary key.

2. **Projects Table**:
    - Contains project-specific information.
    - `project_id` is the primary key.

3. **Assignments Table**:
    - Contains assignment-specific information.
    - Uses `employee_id` and `project_id` as foreign keys.

### Step 2: Define the New Table Structures

#### Employees Table

```sql
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    employee_name TEXT
);
```

#### Projects Table

```sql
CREATE TABLE projects (
    project_id INTEGER PRIMARY KEY,
    project_name TEXT,
    project_manager TEXT
);
```

#### Assignments Table

```sql
CREATE TABLE assignments (
    employee_id INTEGER,
    project_id INTEGER,
    PRIMARY KEY (employee_id, project_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);
```

### Step 3: Populate the New Tables

#### Insert Data into Employees Table

```sql
INSERT INTO employees (employee_id, employee_name) VALUES
(1, 'Alice'),
(2, 'Bob'),
(3, 'Charlie'),
(4, 'David'),
(5, 'Eve');
```

#### Insert Data into Projects Table

```sql
INSERT INTO projects (project_id, project_name, project_manager) VALUES
(101, 'Project A', 'John'),
(102, 'Project B', 'Sarah'),
(103, 'Project C', 'Alice');
```

#### Insert Data into Assignments Table

```sql
INSERT INTO assignments (employee_id, project_id) VALUES
(1, 101),
(2, 102),
(3, 101),
(4, 103),
(5, 102);
```

### Updating the Project Manager

Now, if we need to update the project manager for `Project B`, we only need to update a single row in the `projects` table:

```sql
UPDATE projects
SET project_manager = 'Michael'
WHERE project_id = 102;
```

### Final Tables in Normalized Form

#### Employees Table

| employee_id | employee_name |
|-------------|---------------|
| 1           | Alice         |
| 2           | Bob           |
| 3           | Charlie       |
| 4           | David         |
| 5           | Eve           |

#### Projects Table

| project_id | project_name | project_manager |
|------------|--------------|-----------------|
| 101        | Project A    | John            |
| 102        | Project B    | Michael         |
| 103        | Project C    | Alice           |

#### Assignments Table

| employee_id | project_id |
|-------------|------------|
| 1           | 101        |
| 2           | 102        |
| 3           | 101        |
| 4           | 103        |
| 5           | 102        |

### Explanation

1. **Employees Table**: Contains unique employee records.
2. **Projects Table**: Contains unique project records.
3. **Assignments Table**: Links employees to projects using foreign keys.

By normalizing the table, we eliminate redundant data and prevent update anomalies. This ensures that updates are consistent and data integrity is maintained.