# test: skip — needs a MySQL server (company_db) and an OpenAI API key in OPENAI_API_KEY (bonus module)
import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # MySQL + OpenAI Integration Demo

    This notebook demonstrates how to integrate **MySQL** with **OpenAI API**:
    - Example 1: Convert natural language to SQL using OpenAI, then run it on MySQL.
    - Example 2: Run SQL on MySQL, then use OpenAI to summarize the results.

    We'll use a sample schema with **employees** and **departments** tables.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1: Install dependencies
    You need `mysql-connector-python` and `openai`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2: MySQL Setup
    Run this SQL script in your MySQL shell to create schema and tables:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```sql
    CREATE DATABASE IF NOT EXISTS company_db;
    USE company_db;

    CREATE TABLE departments (
        id INT PRIMARY KEY AUTO_INCREMENT,
        dept_name VARCHAR(50) NOT NULL
    );

    CREATE TABLE employees (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50) NOT NULL,
        age INT,
        salary DECIMAL(10,2),
        dept_id INT,
        FOREIGN KEY (dept_id) REFERENCES departments(id)
    );
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 3: Load Sample Data
    You can either use CSV files (`departments.csv`, `employees.csv`) and `LOAD DATA INFILE`, or insert directly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```sql
    INSERT INTO departments (id, dept_name) VALUES
    (1, 'Engineering'),
    (2, 'Sales'),
    (3, 'HR'),
    (4, 'Marketing'),
    (5, 'Finance');

    INSERT INTO employees (id, name, age, salary, dept_id) VALUES
    (1, 'John Doe', 30, 80000, 1),
    (2, 'Jane Smith', 28, 75000, 1),
    (3, 'Alice Johnson', 35, 65000, 2),
    (4, 'Bob Brown', 40, 70000, 2),
    (5, 'Charlie Davis', 25, 55000, 3),
    (6, 'Diana Evans', 32, 60000, 3),
    (7, 'Ethan Wilson', 29, 72000, 4),
    (8, 'Fiona Clark', 45, 95000, 5),
    (9, 'George King', 38, 88000, 5),
    (10, 'Hannah Adams', 27, 78000, 1);
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 4: Python Integration with MySQL + OpenAI
    Update your **OpenAI API key** and **MySQL credentials** below.
    """)
    return


@app.cell
def _():
    import mysql.connector
    from openai import OpenAI

    # OpenAI client
    client = OpenAI()   # reads the OPENAI_API_KEY environment variable: never put a key in a file

    # MySQL connection
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database="company_db"
    )
    cursor = conn.cursor()
    return client, conn, cursor


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Example 1: Natural Language → SQL → Execute
    We ask OpenAI to generate SQL from a natural language question.
    """)
    return


@app.cell
def _(client, cursor):
    user_question = "Show me the average salary of employees in each department."

    _prompt = f"""
    You are a helpful assistant that converts natural language questions into SQL.
    Database: company_db
    Tables:
    - employees(id, name, age, salary, dept_id)
    - departments(id, dept_name)

    Question: {user_question}
    Write a valid MySQL query.
    """

    _response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": _prompt}],
        temperature=0
    )

    generated_sql = _response.choices[0].message.content.strip()
    print("Generated SQL:", generated_sql)

    cursor.execute(generated_sql).fetchall()
    _results = cursor.fetchall()
    for row in _results:
        print(row)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Example 2: SQL Execution → AI Summary
    We run a predefined query and let OpenAI explain results in plain English.
    """)
    return


@app.cell
def _(client, cursor):
    query = """
    SELECT d.dept_name, AVG(e.salary) as avg_salary
    FROM employees e
    JOIN departments d ON e.dept_id = d.id
    GROUP BY d.dept_name;
    """
    cursor.execute(query).fetchall()
    _results = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]
    data_str = "\n".join([str(dict(zip(columns, row))) for row in _results])
    print("Raw SQL Results:\n", data_str)

    _prompt = f"""
    Here are average salaries by department from a company database:

    {data_str}

    Please summarize the findings in plain English. Highlight the highest and lowest paying departments.
    """

    _response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": _prompt}],
        temperature=0.3
    )

    summary = _response.choices[0].message.content
    print("\nAI Summary:\n", summary)
    return


@app.cell
def _(conn, cursor):
    cursor.close()
    conn.close()
    return


if __name__ == "__main__":
    app.run()
