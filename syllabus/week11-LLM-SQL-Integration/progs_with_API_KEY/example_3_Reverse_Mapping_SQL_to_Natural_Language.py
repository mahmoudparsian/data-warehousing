# Example: Reverse Mapping SQL to Natural Language
# SQL Query
"""
sql
SELECT dept_name, COUNT(*) AS total_employees
FROM departments
JOIN employees ON departments.dept_id = employees.dept_id
GROUP BY dept_name;
"""

# Prompt to OpenAI
prompt = """
You are a helpful assistant that explains SQL queries in natural language.

SQL Query:
SELECT dept_name, COUNT(*) AS total_employees
FROM departments
JOIN employees ON departments.dept_id = employees.dept_id
GROUP BY dept_name;

Natural Language Explanation:
"""



# Python Integration

# import required libraries
from openai import OpenAI

# create OpenAI client 
def create_client(openai_api_key):
    return OpenAI(api_key=openai_api_key) 
#end-def



def explain_sql(client, sql_query):
    prompt = f"""
    You are a helpful assistant that explains SQL queries in natural language.

    SQL Query:
    {sql_query}

    Natural Language Explanation:
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
sql_query = """
SELECT dept_name, COUNT(*) AS total_employees
FROM departments
JOIN employees ON departments.dept_id = employees.dept_id
GROUP BY dept_name;
"""

openai_api_key="sk-..."
client = create_client(openai_api_key)
print(explain_sql(client, sql_query))


# Sample Output from the Model
# "This query retrieves the name of each department  
#  and the total number of employees in that department. 
#  It joins the departments and employees tables using 
#  the department ID and then groups the results by 
#  department name."

