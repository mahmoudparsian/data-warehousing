
# MySQL + LLM Integration
using mysql, can you provide a complete Python example of LLM integration with my tables in a database; what do I need to do with my metadata?

Certainly! Below is a **complete example** of how to integrate an **LLM (Large Language Model, such as OpenAI's GPT models)** with your **MySQL database tables** using **Python**. I’ll explain the key components:

---

## ✅ **Step 1: Requirements**

### Install Required Libraries:

```bash
pip install mysql-connector-python openai
```

---

## ✅ **Step 2: Example Database Setup**

Assume you have a **MySQL database** called `company_db` with a table `employees`:

```sql
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department VARCHAR(50),
    salary FLOAT
);
```

You can replace this with your real tables.

---

## ✅ **Step 3: Metadata Consideration**

🔍 **Why Metadata Matters:**

* LLMs **do not inherently know your table names, columns, or relationships.**
* You need to **extract metadata** from your database (`information_schema`) and provide it to the LLM as context.

Example Metadata for Prompting:

```
Database: company_db
Table: employees
Columns: emp_id (INT), first_name (VARCHAR), last_name (VARCHAR), department (VARCHAR), salary (FLOAT)
```

You could store this in a Python string, or dynamically query it.

---

## ✅ **Step 4: Complete Python Example**

```python
import mysql.connector
import openai

# ---------- CONFIGURATION ----------

# MySQL Configuration
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'company_db'
}

# OpenAI API Key
openai.api_key = "sk-Your-API-Key"

# ---------- STEP 1: Extract Metadata ----------

def extract_metadata():
    cnx = mysql.connector.connect(**mysql_config)
    cursor = cnx.cursor()

    cursor.execute("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = %s
    """, (mysql_config['database'],))

    metadata = {}
    for table_name, column_name, data_type in cursor.fetchall():
        if table_name not in metadata:
            metadata[table_name] = []
        metadata[table_name].append(f"{column_name} ({data_type})")

    cursor.close()
    cnx.close()
    return metadata

# ---------- STEP 2: Generate SQL Query Using LLM ----------

def generate_sql(user_question, metadata):
    metadata_context = "\n".join(
        f"Table: {table}\nColumns: {', '.join(columns)}" 
        for table, columns in metadata.items()
    )

    prompt = f"""
You are an expert SQL generator.
Given the following database schema:
{metadata_context}

Write a MySQL query for the following request:
{user_question}

Only output the SQL query.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",  # or gpt-4-turbo, gpt-4.5-turbo
        messages=[{"role": "system", "content": "You generate SQL queries for MySQL databases."},
                  {"role": "user", "content": prompt}]
    )

    sql_query = response['choices'][0]['message']['content'].strip()
    return sql_query

# ---------- STEP 3: Execute SQL ----------

def execute_sql(sql_query):
    cnx = mysql.connector.connect(**mysql_config)
    cursor = cnx.cursor()
    cursor.execute(sql_query)

    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    cursor.close()
    cnx.close()

    # Convert to list of dicts
    return [dict(zip(columns, row)) for row in results]

# ---------- STEP 4: Example Flow ----------

if __name__ == "__main__":
    # Example user question
    user_question = "Show me the first names and salaries of employees in the Engineering department."

    # Extract metadata
    metadata = extract_metadata()

    # Generate SQL
    sql_query = generate_sql(user_question, metadata)
    print(f"Generated SQL:\n{sql_query}\n")

    # Execute SQL and display results
    results = execute_sql(sql_query)
    for row in results:
        print(row)
```

---

## ✅ **Example Output**

```
Generated SQL:
SELECT first_name, salary FROM employees WHERE department = 'Engineering';

{'first_name': 'John', 'salary': 90000.0}
{'first_name': 'Alice', 'salary': 95000.0}
```

---

## ✅ **Step 5: What to Do With Metadata**

✔️ Extract the schema from `information_schema.columns`
✔️ Pass the **schema and column data types as part of your prompt context**
✔️ Update metadata dynamically if your database changes
✔️ Optionally, cache metadata to avoid frequent schema lookups

---

## ✅ **Optional Improvements**

* Add SQL injection prevention (e.g., review generated queries)
* Add error handling for failed queries
* Allow LLM to ask clarifying questions
* Store schema in a JSON or YAML file for simplicity
* Log user queries and generated SQL for auditing

---

If you'd like, I can:
✔️ Build a **FastAPI service** around this
✔️ Add a **natural language frontend (streamlit, react, etc.)**
✔️ Connect to Snowflake, PostgreSQL, or other databases
✔️ Use **LangChain SQL agents** instead of raw OpenAI API

Would you like any of these enhancements?

Add a natural language frontend (streamlit, react, etc.)

Great! Let’s create a **simple natural language SQL query app** with a **Streamlit frontend**, so you can type in a question and see the results from your MySQL database.

This will be a **complete working app**, with the backend from your earlier request and a user-friendly web interface.

---

# ✅ **Final Architecture**

```
+---------------------+        +-------------------+        +--------------------+
|  Streamlit Frontend | -----> |  OpenAI GPT Model | -----> | MySQL Database     |
| (Natural Language)  | <----- | Generates SQL     | <----- | Executes SQL Query |
+---------------------+        +-------------------+        +--------------------+
```

---

# ✅ **Full Solution**

## 🔧 **1. Install Required Libraries**

```bash
pip install streamlit openai mysql-connector-python
```

---

## 🗂️ **2. Final Folder Structure**

```
my_nl_sql_app/
├── app.py                  # Streamlit frontend
├── sql_generator.py        # SQL generation and database logic
```

---

## 🛠️ **3. `sql_generator.py` (Backend Logic)**

```python
# sql_generator.py
import mysql.connector
import openai

# MySQL Config
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'company_db'
}

# OpenAI API Key
openai.api_key = "sk-your-api-key"

def extract_metadata():
    cnx = mysql.connector.connect(**mysql_config)
    cursor = cnx.cursor()
    cursor.execute("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = %s
    """, (mysql_config['database'],))

    metadata = {}
    for table_name, column_name, data_type in cursor.fetchall():
        metadata.setdefault(table_name, []).append(f"{column_name} ({data_type})")

    cursor.close()
    cnx.close()
    return metadata

def generate_sql(user_question, metadata):
    metadata_context = "\n".join(
        f"Table: {table}\nColumns: {', '.join(columns)}" for table, columns in metadata.items()
    )

    prompt = f"""
You are an expert MySQL SQL generator.
Given the following database schema:
{metadata_context}

Write a MySQL query for the following request:
{user_question}

Only output the SQL query.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You generate SQL queries for MySQL databases."},
            {"role": "user", "content": prompt}
        ]
    )

    return response['choices'][0]['message']['content'].strip()

def execute_sql(sql_query):
    cnx = mysql.connector.connect(**mysql_config)
    cursor = cnx.cursor()
    cursor.execute(sql_query)

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    cursor.close()
    cnx.close()

    return [dict(zip(columns, row)) for row in rows]
```

---

## 🌐 **4. `app.py` (Streamlit Frontend)**

```python
# app.py
import streamlit as st
from sql_generator import extract_metadata, generate_sql, execute_sql

st.set_page_config(page_title="Natural Language SQL App", layout="centered")

st.title("🔍 Natural Language SQL Query on MySQL Database")

# User input
user_question = st.text_input("Ask your question about the database:")

if st.button("Run Query") and user_question:
    try:
        with st.spinner("🔍 Extracting metadata..."):
            metadata = extract_metadata()

        with st.spinner("🤖 Generating SQL query..."):
            sql_query = generate_sql(user_question, metadata)

        st.code(sql_query, language='sql')

        with st.spinner("📊 Executing query..."):
            results = execute_sql(sql_query)

        st.success(f"✅ Query executed. Found {len(results)} rows.")
        st.dataframe(results)

    except Exception as e:
        st.error(f"❌ Error: {e}")
```

---

## ▶️ **5. Run the App**

From your project folder:

```bash
streamlit run app.py
```

Then open:
`http://localhost:8501`

---

## ✅ Example Usage

| **Question**                                        | **Generated SQL**                                                           |
| --------------------------------------------------- | --------------------------------------------------------------------------- |
| Show all employees in the Sales department          | SELECT \* FROM employees WHERE department = 'Sales';                        |
| What are the salaries of employees in Engineering?  | SELECT first\_name, salary FROM employees WHERE department = 'Engineering'; |
| List all departments and count of employees in each | SELECT department, COUNT(\*) FROM employees GROUP BY department;            |

---

# ✅ **What Next?**

✔️ Add authentication for production
✔️ Add query review before execution for safety
✔️ Allow user to edit generated SQL before running
✔️ Add support for Snowflake, PostgreSQL, or other databases
✔️ Dockerize for deployment

---

⚙️ **Would you like me to generate a complete Dockerfile and deployment instructions? Or convert this into a React + FastAPI full-stack app?**

Use LangChain SQL agents instead of raw OpenAI API

Response 1
Great decision! Using LangChain SQL agents allows you to leverage LLMs to understand your SQL schema and execute queries intelligently, with built-in tools for SQL database access. Below is a complete working app that integrates:

🧠 LangChain + OpenAI

🗃️ MySQL database

🌐 Streamlit frontend

🛠️ LangChain SQL Agent

✅ Key Benefits of LangChain SQL Agent
Automatically understands schema from metadata

Allows natural language to SQL using tools

Executes SQL and returns results

Handles clarifying follow-ups with memory (optional)

✅ 1. 📦 Install Required Packages
bash
pip install langchain openai mysql-connector-python sqlalchemy streamlit
✅ 2. 🛠️ Python App Folder Structure
graphql
my_langchain_app/
├── app.py             # Streamlit frontend
├── sql_agent.py       # LangChain SQL agent logic
✅ 3. 🧠 sql_agent.py: LangChain SQL Agent Setup
python
# sql_agent.py
import os
import openai
from sqlalchemy import create_engine
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase

# Set your OpenAI key
openai.api_key = os.getenv("OPENAI_API_KEY") or "sk-<your-api-key>"

# MySQL connection
MYSQL_URI = "mysql+mysqlconnector://root:your_password@localhost/company_db"

# Create SQLAlchemy engine and LangChain database wrapper
engine = create_engine(MYSQL_URI)
db = SQLDatabase(engine)

# Load OpenAI chat model
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Build SQL agent with toolkit
def get_sql_agent():
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        handle_parsing_errors=True,
    )
    return agent_executor
✅ 4. 🌐 app.py: Streamlit Frontend
python
# app.py
import streamlit as st
from sql_agent import get_sql_agent

st.set_page_config(page_title="LangChain + MySQL", layout="centered")
st.title("💬 LangChain Natural Language SQL on MySQL")

question = st.text_input("Ask a question about your database:", placeholder="e.g., Show all employees in Sales")

if st.button("Run Query") and question:
    with st.spinner("Processing your question..."):
        try:
            agent = get_sql_agent()
            response = agent.run(question)
            st.success("✅ Done!")
            st.write(response)
        except Exception as e:
            st.error(f"❌ Error: {e}")
✅ 5. ▶️ Run the App
bash
streamlit run app.py
Visit http://localhost:8501

✅ Example Natural Language Prompts
Prompt	What LangChain Does
"List all employees in the Engineering department."	Generates and runs: SELECT * FROM employees WHERE department='Engineering';
"What is the average salary per department?"	Uses GROUP BY and AVG()
"How many employees are there?"	Uses SELECT COUNT(*) FROM employees
✅ Why Use LangChain Over Raw OpenAI API?
Feature	Raw OpenAI API	LangChain SQL Agent
Schema awareness	Manual prompt engineering	Automatic schema introspection
Query generation	One-shot generation	Iterative + tool-based reasoning
Execution integration	Must be added manually	Built-in SQL tool
Error handling	Basic	Recovery and retries built-in
✅ Next Steps (Optional)
Add memory to support follow-up questions

Add authentication (Streamlit or Auth0)

Extend with LangGraph or LangServe

Add SQL query approval UI before execution

Log and monitor all queries/responses

Would you like me to:

✅ Add conversational memory for multi-turn Q&A?

✅ Convert this to FastAPI + React full-stack app?

✅ Dockerize the whole app for deployment?

Let me know!

Response 2
Excellent choice! LangChain SQL Agents provide a more structured and secure way to let an LLM interact with your SQL database. This approach lets the LLM generate and run SQL queries directly against the database, with better control and safety.

Below is a complete Streamlit app example using LangChain's SQL Agent to query a MySQL database from natural language questions.

✅ Final Architecture (LangChain Version)
sql
+---------------------+       +--------------------+       +--------------------+
|  Streamlit Frontend | --->  |  LangChain SQL Agent| ---> | MySQL Database     |
| (Natural Language)  |       | (Uses OpenAI + SQL) |       | Executes SQL Query |
+---------------------+       +--------------------+       +--------------------+
🔧 1. Install Required Libraries
bash
pip install streamlit langchain openai mysql-connector-python sqlalchemy pymysql
🛠️ 2. Setup: LangChain + MySQL
LangChain uses SQLAlchemy to connect to the database.
Example connection string for MySQL:

bash
mysql+pymysql://username:password@host:port/dbname
🗂️ 3. Folder Structure
graphql
my_nl_sql_app/
├── app.py                  # Streamlit frontend
└── langchain_sql_agent.py   # LangChain SQL agent logic
🛠️ 4. langchain_sql_agent.py: LangChain SQL Agent Logic
python
# langchain_sql_agent.py
from langchain_openai import ChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

# MySQL Connection URL
# Example: mysql+pymysql://root:your_password@localhost:3306/company_db
MYSQL_URL = "mysql+pymysql://root:your_password@localhost:3306/company_db"

# OpenAI API Key (set as env var or directly here)
import os
os.environ["OPENAI_API_KEY"] = "sk-your-api-key"

# Create the SQLDatabase instance
db = SQLDatabase.from_uri(MYSQL_URL)

# Create LLM instance
llm = ChatOpenAI(model="gpt-4o")

# Create SQL Chain Agent
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

def run_nl_query(user_question):
    # Pass the question to LangChain SQL agent
    response = db_chain.run(user_question)
    return response
🌐 5. app.py: Streamlit Frontend
python
# app.py
import streamlit as st
from langchain_sql_agent import run_nl_query

st.set_page_config(page_title="LangChain SQL Agent", layout="centered")

st.title("🔍 Natural Language SQL Query (LangChain + MySQL)")

user_question = st.text_input("Ask your question about the database:")

if st.button("Run Query") and user_question:
    try:
        with st.spinner("🤖 Generating and running SQL query..."):
            response = run_nl_query(user_question)

        st.success("✅ Query executed.")
        st.write(response)

    except Exception as e:
        st.error(f"❌ Error: {e}")
▶️ 6. Run the App
bash
streamlit run app.py
Then open in your browser:

arduino
http://localhost:8501
✅ Example Usage
Natural Language	Agent Response (Example)
Show all employees in the Engineering department.	Table with employee rows filtered by Engineering department
List departments and how many employees each has.	Aggregated results per department
What is the average salary of employees?	Single number representing average salary
✅ Advantages of LangChain SQL Agent
✔️ Uses database introspection: the LLM knows about your tables and columns
✔️ Safer than letting the LLM write raw queries blindly
✔️ Supports multiple LLMs (OpenAI, Anthropic, Cohere, etc.)
✔️ No need to manually pass metadata

🔒 Security Tip
✅ The LangChain SQL Agent is powerful but can still produce queries like DROP TABLE.
➡️ You should restrict the database user to read-only access, or use LangChain toolkits with query guards.

🔧 Optional Enhancements
Add SQL query previews before execution

Add a SQL query sandbox and limit query runtime

Use LangChain Agents (SQL Agent with conversation memory)

Add user authentication to Streamlit

Support Snowflake, PostgreSQL, SQL Server (just change the connection string)

Would you like me to:

Add Docker support for this app?

Add conversational memory so users can ask follow-up questions?

Generate a React + FastAPI version of this app?

