"""
This example provides a basic framework where users 
input natural language, OpenAI translates it to SQL, 
and the SQL is executed against a MySQL database, with 
results displayed in Streamlit. Remember to replace 
placeholders like YOUR_OPENAI_API_KEY and MySQL credentials 
with your actual values. For production environments, 
consider more robust error handling and security measures.

A working example of a Streamlit application integrating 
with OpenAI and MySQL can be achieved by combining Streamlit's 
UI capabilities, OpenAI's language model for natural language 
processing, and MySQL for data storage and retrieval.

1. Setup and Dependencies:
Install necessary libraries.

    pip install streamlit 
    pip install openai 
    pip install mysql-connector-python

2. Create a .streamlit/secrets.toml file in your project's root 
directory to store your OpenAI API key and MySQL credentials securely:

	openai_api_key = "YOUR_OPENAI_API_KEY"
    mysql_host = "your_mysql_host"
    mysql_user = "your_mysql_user"
    mysql_password = "your_mysql_password"
    mysql_database = "your_mysql_database"

3. Running the Application:
Save the code as app.py and Run from your terminal.
Code

    streamlit run streamlit_app.py


"""

import streamlit as st
import openai
import mysql.connector

# Load secrets
openai.api_key = st.secrets["openai_api_key"]
mysql_config = {
    "host": st.secrets["mysql_host"],
    "user": st.secrets["mysql_user"],
    "password": st.secrets["mysql_password"],
    "database": st.secrets["mysql_database"]
}

def get_mysql_connection():
    """Establishes and returns a MySQL database connection."""
    try:
        conn = mysql.connector.connect(**mysql_config)
        return conn
    except mysql.connector.Error as err:
        st.error(f"Error connecting to MySQL: {err}")
        return None
#end-def

def generate_sql_query(natural_language_query):
    """Uses OpenAI to generate a SQL query from natural language."""
    prompt = f"Convert the following natural language query into a SQL query for a MySQL database: {natural_language_query}"
    response = openai.Completion.create(
        engine="text-davinci-003", # Or a more recent model like gpt-3.5-turbo if using ChatCompletion
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].text.strip()
#end-def

def execute_sql_query(sql_query):
    """Executes a SQL query against the MySQL database and returns results."""
    conn = get_mysql_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True) # Returns results as dictionaries
            cursor.execute(sql_query)
            if sql_query.lower().startswith("select"):
                results = cursor.fetchall()
            else:
                conn.commit() # Commit changes for INSERT, UPDATE, DELETE
                results = {"message": "Query executed successfully."}
            cursor.close()
            conn.close()
            return results
        except mysql.connector.Error as err:
            return {"error": f"Error executing SQL query: {err}"}
    return {"error": "Could not connect to database."}
#end-def

st.title("SQL Query Generator & Executor")

user_query = st.text_area("Enter your natural language query:")

if st.button("Generate SQL & Execute"):
    if user_query:
        with st.spinner("Generating SQL query..."):
            sql_query = generate_sql_query(user_query)
            st.subheader("Generated SQL Query:")
            st.code(sql_query, language="sql")

        with st.spinner("Executing SQL query..."):
            results = execute_sql_query(sql_query)
            st.subheader("Query Results:")
            if "error" in results:
                st.error(results["error"])
            elif isinstance(results, dict) and "message" in results:
                st.success(results["message"])
            else:
                st.dataframe(results)
    else:
        st.warning("Please enter a query.")

