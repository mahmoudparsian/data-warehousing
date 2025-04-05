# Essential SQL Commands

* Here are 24 essential SQL commands, arranged from simple to more complex, with examples to guide you

* These examples progress from simple commands like creating databases and tables to more advanced operations like `JOIN` and `SUBQUERY`. Let me know if you'd like further clarification or help building your SQL expertise!

* How to learn: practice!

---

### 1. **CREATE DATABASE**
   ```sql
   CREATE DATABASE company_db;
   ```

### 2. **CREATE TABLE**
   ```sql
   CREATE TABLE Employees (
       ID INT,
       Name VARCHAR(50),
       Position VARCHAR(50),
       Salary INT
   );
   ```

### 3. **INSERT INTO**  
   ```sql
   INSERT INTO Employees (ID, Name, Position, Salary)
   VALUES 
       (1, 'Alice Johnson', 'CEO', 150000),
       (2, 'Bob Smith', 'CTO', 140000),
       (3, 'Charlie Brown', 'HR Manager', 75000);
   ```

### 4. **SELECT**  

   Retrieve all columns and rows:

   ```sql
   SELECT * FROM Employees;
   ```
   Retrieve specific columns:
   
   ```sql
   SELECT Name, Position FROM Employees;
   ```

### 5. **WHERE**  
   Filter results based on a condition:
   
   ```sql
   SELECT * 
   FROM Employees 
   WHERE Salary > 100000;
   ```

### 6. **UPDATE**  
   Modify existing data:
   
   ```sql
   UPDATE Employees
   SET Position = 'Chief Operating Officer'
   WHERE ID = 1;
   ```

### 7. **DELETE**
   Remove rows from the table:
   
   ```sql
   DELETE FROM Employees 
   WHERE ID = 3;
   ```

### 8. **ALTER TABLE**  

Add or modify table structure:

* Add a column to an existing table:
   
```sql
     ALTER TABLE Employees
     ADD Department VARCHAR(50);
```

* Modify an existing column data type:
   
```sql
     ALTER TABLE Employees
     MODIFY Salary DECIMAL(12, 2);
```

### 9. **JOIN**  
   Combine rows from two tables. Example with a second table:
   
   ```sql
   CREATE TABLE Departments (
       ID INT PRIMARY KEY,
       DepartmentName VARCHAR(50)
   );
   
   INSERT INTO Departments (ID, DepartmentName)
   VALUES 
       (1, 'Management'),
       (2, 'Technical');
   
   SELECT E.Name, D.DepartmentName
   FROM Employees E
   JOIN Departments D
   ON E.ID = D.ID;
   ```

### 10. **GROUP BY**  
   - Aggregate data: find average salary per department:
   
   ```sql
   SELECT Department, 
          AVG(Salary) AS average_salary
   FROM Employees
   GROUP BY Department;
   ```
- Aggregate data: find number of employees per department:
   
   ```sql
   SELECT Department, 
          count(*) AS number_of_employees
   FROM Employees
   GROUP BY Department;
   ```


### 11. **HAVING**  
   Apply conditions to grouped data:
   
   ```sql
   SELECT Department, 
          AVG(Salary) AS average_salary
   FROM Employees
   GROUP BY Department
   HAVING AVG(Salary) > 80000;
   ```

### 12. **SUBQUERY**  
   Use a query inside another query:
   
   ```sql
   SELECT * FROM Employees
   WHERE Salary > (
                   SELECT AVG(Salary) FROM Employees
                  );
   ```

---

# subqueries and ranking functions


---

### **13. Subquery with `WHERE` Clause**
Find employees whose salary is above the average salary:

```sql
SELECT Name, Salary
FROM Employees
WHERE Salary > (SELECT AVG(Salary) FROM Employees);
```

---

### **14. Subquery with `IN`**
Get employees who work in specific departments by using a subquery:

```sql
SELECT Name, Position
FROM Employees
WHERE DepartmentID IN (SELECT ID FROM Departments WHERE DepartmentName = 'Technical');
```

---

### **15. Subquery with `EXISTS`**
Check if a specific employee exists in the table:

```sql
SELECT Name
FROM Employees
WHERE EXISTS (SELECT 1 FROM Employees WHERE Name = 'Alice Johnson');
```

---

### **16. Ranking with `ROW_NUMBER()`**
Assign a unique rank to each employee based on their salary:

```sql
SELECT Name, 
       Salary,
       ROW_NUMBER() OVER (ORDER BY Salary DESC) AS rnk
FROM Employees;
```

---

### **17. Ranking with `RANK()`**
Rank employees based on their salary, allowing ties to share the same rank:

```sql
SELECT Name, 
       Salary,
       RANK() OVER (ORDER BY Salary DESC) AS rnk
FROM Employees;
```

---

### **18. Ranking with `DENSE_RANK()`**
Rank employees based on their salary without skipping ranks for ties:

```sql
SELECT Name, 
       Salary,
       DENSE_RANK() OVER (ORDER BY Salary DESC) AS rnk
FROM Employees;
```

---


### **19. Subquery with `JOIN` and Ranking with `ROW_NUMBER()`**
Get the top 3 employees with the highest salaries in each department:

```sql
with ranked_emps as 
(
   SELECT DepartmentID, 
          Name, 
          Salary, 
          ROW_NUMBER() OVER (PARTITION BY DepartmentID ORDER BY Salary DESC)
           AS rnk
   FROM Employees
)
SELECT DepartmentID, 
       Name, 
       Salary, 
       rnk
FROM ranked_emps
WHERE rnk <= 3;
```

---

### **20. Subquery with Aggregation and Ranking with `RANK()`**
Rank departments by their average salaries:

```sql
SELECT DepartmentID, 
       AVG(Salary) AS average_salary,
       RANK() OVER (ORDER BY AVG(Salary) DESC) AS department_rank
FROM Employees
GROUP BY DepartmentID;
```

---

### **21. Subquery with `HAVING` Clause**
Find employees with salaries above the department average:

```sql
SELECT Name, 
       Salary, 
       DepartmentID
FROM Employees
WHERE Salary > (
    SELECT AVG(Salary)
    FROM Employees e
    WHERE e.DepartmentID = Employees.DepartmentID
);
```

---

### **22. Correlated Subquery with `DENSE_RANK()`**
Rank employees by salary within each department, handling ties with `DENSE_RANK()`:

```sql
SELECT Name, 
       Salary, 
       DepartmentID,
       DENSE_RANK() OVER (PARTITION BY DepartmentID ORDER BY Salary DESC) 
        AS rnk
FROM Employees;
```

---

### **23. Subquery with Aggregation and Ranking Functions**
Find the highest-paid employee in each department:

```sql
SELECT Name, 
       Salary, 
       DepartmentID
FROM Employees
WHERE Salary = (
    SELECT MAX(Salary)
    FROM Employees e
    WHERE e.DepartmentID = Employees.DepartmentID
);
```

---

### **24. Subquery with `EXISTS` and Ranking Functions**
List employees who work in departments with above-average total salaries:

```sql
SELECT Name, 
       Salary, 
       DepartmentID
FROM Employees
WHERE EXISTS 
   (
     SELECT 1
     FROM Employees e
     WHERE e.DepartmentID = Employees.DepartmentID
     GROUP BY e.DepartmentID
     HAVING SUM(e.Salary) > (
                             SELECT AVG(SUM(Salary)) 
                             FROM Employees 
                             GROUP BY DepartmentID
                            )
  );
```

---

