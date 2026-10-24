"""
Demo integration of mysql with openAI: 
provide a running  streamlit app with a 
complete mysql schema with sample rows

✅ You want a running Streamlit app that integrates 
   MySQL with OpenAI, along with:

    1.    A complete MySQL schema (with some sample rows).
    
    2.    A Streamlit UI where a user can ask questions in natural language.
    
    3.    OpenAI will convert the natural language into SQL queries, 
          execute them on MySQL, and display the results.


1. MySQL Schema + Sample Data

Let’s use a simple Employee Database with departments and employees tables.

-- Create database
CREATE DATABASE company_db;
USE company_db;

-- Departments table
CREATE TABLE departments (
    dept_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name VARCHAR(100) NOT NULL
);

-- Employees table
CREATE TABLE employees (
    emp_id INT PRIMARY KEY AUTO_INCREMENT,
    emp_name VARCHAR(100) NOT NULL,
    job_title VARCHAR(100),
    salary DECIMAL(10,2),
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

-- Insert sample departments
INSERT INTO departments (dept_name) VALUES
('Engineering'),
('Sales'),
('HR'),
('Finance');

-- Insert sample employees
INSERT INTO employees (emp_name, job_title, salary, dept_id) VALUES
('Alice Johnson', 'Software Engineer', 95000, 1),
('Bob Smith', 'Sales Executive', 70000, 2),
('Carol White', 'HR Manager', 80000, 3),
('David Brown', 'Financial Analyst', 85000, 4),
('Eve Black', 'Senior Engineer', 120000, 1),
('Frank Green', 'Sales Associate', 55000, 2);
"""

# 2. Streamlit App (Python)

Save as app.py:

import streamlit as st
import mysql.connector
import pandas as pd
import openai

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# MySQL connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_mysql_password",
        database="company_db"
    )

# Function to run SQL
def run_sql(query):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return pd.DataFrame(rows)

# Convert natural language to SQL using OpenAI
def nl_to_sql(question, schema_description):
    prompt = f"""
    You are an assistant that converts natural language questions into SQL queries.
    Database schema:
    {schema_description}

    Question: {question}
    SQL:
    """
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0
    )
    return response["choices"][0]["text"].strip()

# Streamlit UI
st.title("💬 MySQL + OpenAI Integration")
st.write("Ask questions about the employee database in plain English.")

# Schema description
schema_description = """
Table: departments(dept_id, dept_name)
Table: employees(emp_id, emp_name, job_title, salary, dept_id)
"""

question = st.text_input("Enter your question:")

if question:
    st.write(f"**Question:** {question}")

    sql_query = nl_to_sql(question, schema_description)
    st.code(sql_query, language="sql")

    try:
        results = run_sql(sql_query)
        st.dataframe(results)
    except Exception as e:
        st.error(f"Error running query: {e}")


⸻

3. Example Queries You Can Try
    •    “Show all employees in the Engineering department”
    •    “What is the average salary in Sales?”
    •    “List employees earning more than 80,000”

⸻

4. Running the Demo
    1.    Install requirements:

pip install streamlit mysql-connector-python openai pandas


    2.    Run the app:

streamlit run app.py


    3.    Open in browser: http://localhost:8501

⸻



