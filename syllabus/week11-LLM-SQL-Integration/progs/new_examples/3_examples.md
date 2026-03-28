# 3 complete, working examples of mysql integration with openAI api.

Here are two scenarios that go beyond “basic” query execution:
    1.    Natural Language to SQL: User asks a question in 
          plain English → 
          OpenAI generates SQL → 
          Python executes query on MySQL 
          → Returns results.

    2.    Query Summarization & Insights: Run a query on MySQL, 
          then pass the raw query results to OpenAI to get 
          summaries/insights (e.g., trends, anomalies, natural 
          language explanations).

	3. Complex Example: Chat-to-Insights System
⸻

# Example 1: Natural Language → SQL → MySQL Execution

	✅ Example is fully working and intermediate-level:


	•    Example 1: Natural language → SQL.

	This example lets a user type natural language, 
	and OpenAI generates the corresponding SQL query.

🔹 Workflow:
    •    OpenAI generates SQL from English input.
    •    Python executes query on MySQL.
    •    Results are shown to the user.
    
import mysql.connector
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

# MySQL connection setup
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword",
    database="company_db"
)
cursor = conn.cursor()

# Step 1: User natural language question
user_question = "Show me the average salary of employees in each department."

# Step 2: Ask OpenAI to generate SQL
prompt = f"""
You are a helpful assistant that converts natural language questions into SQL.
Database: company_db
Tables:
- employees(id, name, age, salary, dept_id)
- departments(id, dept_name)

Question: {user_question}

Write a valid MySQL query.
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0
)

generated_sql = response.choices[0].message.content.strip()
print("Generated SQL:", generated_sql)

# Step 3: Execute SQL on MySQL
cursor.execute(generated_sql)
results = cursor.fetchall()

# Step 4: Display results
for row in results:
    print(row)

cursor.close()
conn.close()



⸻

# Example 2: SQL Execution → Summarization by OpenAI

	✅ Example is fully working and intermediate-level:

    •    Example 2: SQL results → AI summarization.

	This example runs a fixed SQL query, retrieves results, 
	and asks OpenAI to analyze/summarize them.

🔹 Workflow:
    •    SQL query fetches raw data from MySQL.
    •    Data is passed into OpenAI.
    •    OpenAI generates human-readable insights.
    

import mysql.connector
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

# MySQL connection setup
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword",
    database="company_db"
)
cursor = conn.cursor()

# Step 1: Run a predefined query
query = """
SELECT d.dept_name, AVG(e.salary) as avg_salary
FROM employees e
JOIN departments d ON e.dept_id = d.id
GROUP BY d.dept_name;
"""
cursor.execute(query)
results = cursor.fetchall()

# Convert results into readable format
columns = [desc[0] for desc in cursor.description]
data_str = "\n".join([str(dict(zip(columns, row))) for row in results])

print("Raw SQL Results:\n", data_str)

# Step 2: Ask OpenAI to summarize insights
prompt = f"""
Here are average salaries by department from a company database:

{data_str}

Please summarize the findings in plain English. Highlight the highest and lowest paying departments.
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.3
)

summary = response.choices[0].message.content
print("\nAI Summary:\n", summary)

cursor.close()
conn.close()



⸻

# ✅ Examples with  sample schema + CSV data (employees & departments) 

so you can run these directly in MySQL?

⸻

Step 1: MySQL Schema

Run this SQL script to set up your schema:

CREATE DATABASE IF NOT EXISTS company_db;
USE company_db;

-- Departments table
CREATE TABLE departments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name VARCHAR(50) NOT NULL
);

-- Employees table
CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    age INT,
    salary DECIMAL(10,2),
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES departments(id)
);


⸻

Step 2: Sample CSV Data

departments.csv

id,dept_name
1,Engineering
2,Sales
3,HR
4,Marketing
5,Finance

employees.csv

id,name,age,salary,dept_id
1,John Doe,30,80000,1
2,Jane Smith,28,75000,1
3,Alice Johnson,35,65000,2
4,Bob Brown,40,70000,2
5,Charlie Davis,25,55000,3
6,Diana Evans,32,60000,3
7,Ethan Wilson,29,72000,4
8,Fiona Clark,45,95000,5
9,George King,38,88000,5
10,Hannah Adams,27,78000,1


⸻

Step 3: Import CSV Data into MySQL

If you’re running MySQL locally, you can use:

LOAD DATA INFILE '/path/to/departments.csv'
INTO TABLE departments
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, dept_name);

LOAD DATA INFILE '/path/to/employees.csv'
INTO TABLE employees
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, name, age, salary, dept_id);

⚠️ Note: Make sure secure_file_priv in MySQL allows reading CSV from your chosen folder.
Alternatively, you can insert manually with INSERT INTO employees ... if needed.

⸻

Step 4: Example Query Check

Once loaded, test with:

SELECT d.dept_name, AVG(e.salary) AS avg_salary
FROM employees e
JOIN departments d ON e.dept_id = d.id
GROUP BY d.dept_name;

Should return something like:

Engineering | 77666.67
Sales       | 67500.00
HR          | 57500.00
Marketing   | 72000.00
Finance     | 91500.00


⸻

👉 With this schema + data, both of the Python + OpenAI examples  will run.

# CSV files are ready for use with MySQL

✅ — the CSV files are ready for use with MySQL:
    •    departments.csv
    •    employees.csv

# 🔹 Example 3:  Complex Example: Chat-to-Insights System

This example is a complex, and complete, working examples 
of mysql integration with openAI api.

✅ This example:
	• This example is a complex, and complete, working examples 
	  of mysql integration with openAI api.
	  
    •    Handles multi-step reasoning (question → SQL → execution → analysis).
    
    •    Can chain multiple queries if needed.
    
    •    Produces contextual business insights, not just numbers.



Workflow
    1.    User asks a natural language question 
          (e.g., “Which department has the highest average salary, 
          and why might that be?”).
          
    2.    OpenAI generates SQL queries needed to fetch data.
    
    3.    Python executes the SQL queries against MySQL.
    
    4.    OpenAI takes the raw query results + the original user 
          question and generates a contextual analysis/insight 
          (not just summaries, but reasoning).

⸻

Python Implementation

import mysql.connector
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword",
    database="company_db"
)
cursor = conn.cursor()

# Step 1: User natural language input
user_question = "Which department has the highest average salary, and why might that be?"

# Step 2: Ask OpenAI to generate SQL queries
prompt_sql = f"""
You are an AI assistant that helps query a company database.

Database: company_db
Tables:
- employees(id, name, age, salary, dept_id)
- departments(id, dept_name)

The user asked: "{user_question}"

1. Write the SQL query or queries needed to answer this question.
2. Return only the SQL statements, nothing else.
"""

response_sql = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": prompt_sql}],
    temperature=0
)

generated_sql = response_sql.choices[0].message.content.strip()
print("Generated SQL:\n", generated_sql)

# Step 3: Execute each SQL statement (can be multiple)
sql_statements = [stmt.strip() for stmt in generated_sql.split(";") if stmt.strip()]

results_combined = []
for stmt in sql_statements:
    cursor.execute(stmt)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    results_combined.append({
        "query": stmt,
        "columns": columns,
        "rows": rows
    })

# Step 4: Prepare results for OpenAI analysis
data_for_ai = ""
for result in results_combined:
    data_for_ai += f"\nQuery: {result['query']}\n"
    data_for_ai += "Results:\n"
    for row in result["rows"]:
        data_for_ai += str(dict(zip(result["columns"], row))) + "\n"

print("\nRaw SQL Results:\n", data_for_ai)

# Step 5: Ask OpenAI to analyze results in context of user question
prompt_analysis = f"""
The user asked: "{user_question}"

Here are the SQL query results:

{data_for_ai}

Please provide a detailed answer with reasoning and possible business context.
"""

response_analysis = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": prompt_analysis}],
    temperature=0.4
)

analysis = response_analysis.choices[0].message.content
print("\nAI Insight:\n", analysis)

cursor.close()
conn.close()


⸻

🔹 Example Run

User Question:

“Which department has the highest average salary, and why might that be?”

OpenAI Generates SQL:

SELECT d.dept_name, AVG(e.salary) AS avg_salary
FROM employees e
JOIN departments d ON e.dept_id = d.id
GROUP BY d.dept_name
ORDER BY avg_salary DESC
LIMIT 1;

SQL Results:

{'dept_name': 'Finance', 'avg_salary': 91500.00}


## OpenAI Insight:

	The Finance department has the highest average salary 
	(~$91,500).  This may be due to the specialized expertise 
	required in finance roles, higher demand for experienced 
	professionals, or seniority of positions in this department. 
	
	Compared to HR or Sales, finance jobs often require advanced 
	certifications and come with higher compensation packages.

⸻

