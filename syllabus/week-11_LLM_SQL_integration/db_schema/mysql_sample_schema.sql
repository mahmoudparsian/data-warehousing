
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    name VARCHAR(100),
    dept_id INT,
    salary DECIMAL(10, 2),
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

CREATE TABLE tickets (
    ticket_id INT PRIMARY KEY,
    customer_id INT,
    message TEXT,
    status VARCHAR(20)
);

INSERT INTO departments (dept_id, name) VALUES
(1, 'Engineering'),
(2, 'HR'),
(3, 'Sales');

INSERT INTO employees (emp_id, name, dept_id, salary) VALUES
(101, 'Alice', 1, 75000),
(102, 'Bob', 2, 62000),
(103, 'Charlie', 1, 80000),
(104, 'David', 3, 55000),
(105, 'Eve', 2, 67000);

INSERT INTO tickets (ticket_id, customer_id, message, status) VALUES
(1001, 501, 'I need help with my invoice.', 'open'),
(1002, 502, 'System crashes when I login.', 'open'),
(1003, 503, 'Can someone explain the new HR policy?', 'closed');
