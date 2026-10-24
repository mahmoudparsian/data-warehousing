# MySQL + LLM Integration: a Walkthrough

How to let a Large Language Model (LLM) turn a question in plain English into SQL for **your** tables, in three steps:

1. **A Python script:** read the schema (metadata) → ask the LLM for SQL → run it.
2. **A Streamlit app** around that script.
3. **LangChain SQL agents** that do the schema reading and the SQL execution for you.

> ⚠️ **Before you run anything**
> - Set your OpenAI key in the shell, never in a file: `export OPENAI_API_KEY="sk-..."`. `OpenAI()` and LangChain's
>   `ChatOpenAI` read it from there automatically.
> - LLM-generated SQL can be wrong or harmful (`DROP TABLE`). Read the SQL before running it, and connect with a **read-only** database user.
> - The examples use MySQL (`company_db`); replace `your_password` with your own setting. The same ideas work with DuckDB.

---

## Part 1: Natural language → SQL in Python

### Requirements

```bash
pip install mysql-connector-python openai
```

### Example database

A MySQL database `company_db` with a table `employees` (replace it with your own tables):

```sql
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department VARCHAR(50),
    salary FLOAT
);
```

### Why metadata matters

* An LLM **does not know your table names, columns or relationships.**
* You **extract the metadata** from the database (`information_schema`) and give it to the LLM as context.

Example metadata for the prompt:

```
Database: company_db
Table: employees
Columns: emp_id (INT), first_name (VARCHAR), last_name (VARCHAR), department (VARCHAR), salary (FLOAT)
```

You can write this by hand in a Python string, or query it from the database (below).

### The complete script

```python
import mysql.connector
from openai import OpenAI

# ---------- CONFIGURATION ----------

mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'company_db'
}

client = OpenAI()   # reads the OPENAI_API_KEY environment variable

# ---------- STEP 1: Extract metadata ----------

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

# ---------- STEP 2: Generate SQL with the LLM ----------

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

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You generate SQL queries for MySQL databases."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# ---------- STEP 3: Execute SQL ----------

def execute_sql(sql_query):
    cnx = mysql.connector.connect(**mysql_config)
    cursor = cnx.cursor()
    cursor.execute(sql_query)

    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    cursor.close()
    cnx.close()

    # Convert to a list of dicts
    return [dict(zip(columns, row)) for row in results]

# ---------- STEP 4: Example flow ----------

if __name__ == "__main__":
    user_question = "Show me the first names and salaries of employees in the Engineering department."

    metadata = extract_metadata()
    sql_query = generate_sql(user_question, metadata)
    print(f"Generated SQL:\n{sql_query}\n")   # read it before you trust it

    for row in execute_sql(sql_query):
        print(row)
```

### Example output

```
Generated SQL:
SELECT first_name, salary FROM employees WHERE department = 'Engineering';

{'first_name': 'John', 'salary': 90000.0}
{'first_name': 'Alice', 'salary': 95000.0}
```

### What to do with metadata

* Extract the schema from `information_schema.columns`.
* Pass the **schema and column types** as part of the prompt.
* Refresh the metadata when the database changes (or cache it to avoid frequent lookups).

### Possible improvements

* Review generated queries before running them (and use a read-only user).
* Handle failed queries.
* Let the LLM ask clarifying questions.
* Store the schema in a JSON or YAML file.
* Log user questions and generated SQL for auditing.

---

## Part 2: A Streamlit frontend

Type a question in a web page, see the SQL and the results.

```
+---------------------+        +-------------------+        +--------------------+
|  Streamlit Frontend | -----> |  OpenAI GPT Model | -----> | MySQL Database     |
| (Natural Language)  | <----- | Generates SQL     | <----- | Executes SQL Query |
+---------------------+        +-------------------+        +--------------------+
```

### 1. Install

```bash
pip install streamlit openai mysql-connector-python
```

### 2. Folder structure

```
my_nl_sql_app/
├── app.py                  # Streamlit frontend
├── sql_generator.py        # SQL generation and database logic
```

### 3. `sql_generator.py` (backend)

The three functions `extract_metadata`, `generate_sql` and `execute_sql` from Part 1, with the same configuration
(`mysql_config` and `client = OpenAI()`), saved as `sql_generator.py`.

### 4. `app.py` (frontend)

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

### 5. Run the app

```bash
streamlit run app.py
```

Then open `http://localhost:8501`.

### Example usage

| **Question**                                        | **Generated SQL**                                                           |
| --------------------------------------------------- | --------------------------------------------------------------------------- |
| Show all employees in the Sales department          | SELECT \* FROM employees WHERE department = 'Sales';                        |
| What are the salaries of employees in Engineering?  | SELECT first\_name, salary FROM employees WHERE department = 'Engineering'; |
| List all departments and count of employees in each | SELECT department, COUNT(\*) FROM employees GROUP BY department;            |

### Next steps

* Authentication for production use.
* Show the SQL for review (and allow editing) before it runs.
* Support Snowflake, PostgreSQL or other databases (change the connection).

---

## Part 3: LangChain SQL agents

Instead of building the prompt yourself, a **LangChain SQL agent** reads the schema, writes the SQL, runs it, and can retry when a query fails.

> ⚠️ **LangChain's module paths change often.** The imports below may need updating: check the current LangChain
> documentation before running this code (it was not tested with the current versions).

| Feature | Raw OpenAI API (Parts 1–2) | LangChain SQL agent |
|---|---|---|
| Schema awareness | Manual prompt engineering | Automatic schema introspection |
| Query generation | One-shot generation | Iterative, tool-based reasoning |
| Execution | Must be added manually | Built-in SQL tool |
| Error handling | Basic | Recovery and retries built in |

### Version A: an SQL agent with a toolkit

```bash
pip install langchain openai mysql-connector-python sqlalchemy streamlit
```

```
my_langchain_app/
├── app.py             # Streamlit frontend
├── sql_agent.py       # LangChain SQL agent logic
```

```python
# sql_agent.py
from sqlalchemy import create_engine
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase

# The OpenAI key comes from the OPENAI_API_KEY environment variable (ChatOpenAI reads it).

# MySQL connection
MYSQL_URI = "mysql+mysqlconnector://root:your_password@localhost/company_db"

# SQLAlchemy engine and LangChain database wrapper
engine = create_engine(MYSQL_URI)
db = SQLDatabase(engine)

# OpenAI chat model
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# SQL agent with its toolkit
def get_sql_agent():
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        handle_parsing_errors=True,
    )
    return agent_executor
```

```python
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
```

Run it with `streamlit run app.py` and open `http://localhost:8501`.

| Prompt | What LangChain does |
|---|---|
| "List all employees in the Engineering department." | Generates and runs `SELECT * FROM employees WHERE department = 'Engineering';` |
| "What is the average salary per department?" | Uses `GROUP BY` and `AVG()` |
| "How many employees are there?" | Uses `SELECT COUNT(*) FROM employees` |

### Version B: an SQL chain

```
+---------------------+       +---------------------+       +--------------------+
|  Streamlit Frontend | --->  | LangChain SQL Chain | --->  | MySQL Database     |
| (Natural Language)  |       | (OpenAI + SQL)      |       | Executes SQL Query |
+---------------------+       +---------------------+       +--------------------+
```

```bash
pip install streamlit langchain langchain-openai langchain-experimental openai mysql-connector-python sqlalchemy pymysql
```

LangChain connects through SQLAlchemy. A MySQL connection string looks like
`mysql+pymysql://username:password@host:port/dbname`.

```
my_nl_sql_app/
├── app.py                  # Streamlit frontend
└── langchain_sql_agent.py  # LangChain SQL logic
```

```python
# langchain_sql_agent.py
from langchain_openai import ChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

# MySQL connection URL, e.g. mysql+pymysql://root:your_password@localhost:3306/company_db
MYSQL_URL = "mysql+pymysql://root:your_password@localhost:3306/company_db"

# The OpenAI key comes from the OPENAI_API_KEY environment variable (ChatOpenAI reads it).

db = SQLDatabase.from_uri(MYSQL_URL)
llm = ChatOpenAI(model="gpt-4o")
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

def run_nl_query(user_question):
    return db_chain.run(user_question)
```

```python
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
```

Run it with `streamlit run app.py` and open `http://localhost:8501`.

| Natural language | Response (example) |
|---|---|
| Show all employees in the Engineering department. | Employee rows filtered by the Engineering department |
| List departments and how many employees each has. | Aggregated results per department |
| What is the average salary of employees? | A single number: the average salary |

### Advantages and a security note

* The agent introspects the database: the LLM knows your tables and columns, with no metadata to pass by hand.
* LangChain supports several LLM providers (OpenAI, Anthropic, Cohere, …).
* 🔒 An agent can still produce queries like `DROP TABLE`. Connect with a **read-only** database user, or use query guards.

### Possible enhancements

* SQL previews (and approval) before execution, plus a query time limit.
* Conversation memory for follow-up questions.
* User authentication for the Streamlit app.
* Snowflake, PostgreSQL or SQL Server: change the connection string.
* Logging and monitoring of all questions, queries and answers.
