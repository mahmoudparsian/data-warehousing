# Delete Anomaly

A **delete anomaly** occurs when the deletion 
of a record inadvertently leads to the loss 
of additional, unrelated information. This 
often happens in a non-normalized database 
where multiple pieces of information are stored 
in a single table.

### Example of a Delete Anomaly

Let's consider a table `employees_projects` that is not normalized:

| employee_id | employee_name | project_id | project_name | project_manager |
|-------------|---------------|------------|--------------|-----------------|
| 1           | Alice         | 101        | Project A    | John            |
| 2           | Bob           | 102        | Project B    | Sarah           |
| 3           | Charlie       | 101        | Project A    | John            |
| 4           | David         | 103        | Project C    | Alice           |
| 5           | Eve           | 102        | Project B    | Sarah           |

### Problem with the Unnormalized Table

- The table contains redundant data. For example, `project_name` and `project_manager` are repeated for each employee working on the same project.
- This redundancy can lead to delete anomalies.

#### Delete Anomaly Scenario

1. **Deleting an Employee:**
   - Suppose you want to remove Alice (employee_id 1) from the table.
   - If you delete the record for Alice, you also lose information about `Project A` and its manager, John, if Alice is the only employee working on `Project A`.

### Solution: Normalization

To avoid this delete anomaly, we can normalize the table by creating separate tables for employees, projects, and assignments.

### Step 1: Create Separate Tables

1. **Employees Table**:
    - Contains employee-specific information.
    - `employee_id` is the primary key.

2. **Projects Table**:
    - Contains project-specific information.
    - `project_id` is the primary key.

3. **Instructors Table**:
    - Contains instructor-specific information.
    - `instructor_id` is the primary key.

4. **Assignments Table**:
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
| 102        | Project B    | Sarah           |
| 103        | Project C    | Alice           |

#### Assignments Table

| employee_id | project_id |
|-------------|------------|
| 1           | 101        |
| 2           | 102        |
| 3           | 101        |
| 4           | 103        |
| 5           | 102        |

### Deleting an Employee Without Losing Project Information

Now, if we need to delete Alice (employee_id 1) from the `assignments` table, we can do so without losing information about `Project A` and its manager, John:

```sql
DELETE FROM assignments WHERE employee_id = 1;
```

This approach prevents the delete anomaly by ensuring that each table contains only relevant data and that relationships between entities (employees, projects, and assignments) are properly managed through foreign keys. This ensures that deleting an employee does not result in the loss of important project information.
