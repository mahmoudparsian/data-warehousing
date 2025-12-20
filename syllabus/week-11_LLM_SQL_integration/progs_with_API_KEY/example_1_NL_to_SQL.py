# Example 1: Employee Database Query Assistant
#
# Scenario: You're building a chatbot interface 
#           that allows users to ask questions 
#           about their company’s workforce data.

"""
MySQL Schema: employee_db

CREATE DATABASE employee_db;
USE employee_db;

CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(100)
);

CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(100),
    hire_date DATE,
    salary DECIMAL(10,2),
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);
"""

# Sample Prompt to OpenAI
prompt = """
You are a helpful assistant converting user questions to SQL.

Schema:
departments(dept_id, dept_name)
employees(emp_id, emp_name, hire_date, salary, dept_id)

User Question: Show total salary by department.
SQL:
"""

#-------------------
# Python Integration
#-------------------

# import required libraries
from openai import OpenAI

# create OpenAI client 
def create_client(openai_api_key):
    return OpenAI(api_key=openai_api_key) 
#end-def

# generate SQL from English
def generate_sql(client, user_question):
    prompt = f"""
    You are a helpful assistant converting user questions to SQL.
    Schema:
    departments(dept_id, dept_name)
    employees(emp_id, emp_name, hire_date, salary, dept_id)

    User Question: {user_question}
    SQL:
    """
     
    response = client.chat.completions.create(
        model="gpt-4o",  # or another chat model like "gpt-3.5-turbo"
        messages=[
            {
             "role": "user", 
             "content": prompt
            }
        ]
    )
    
    return response.choices[0].message.content.strip()
#end-def

# driver program...
openai_api_key="sk-..."
client = create_client(openai_api_key)
print(generate_sql(client, "Show total salary by department"))

