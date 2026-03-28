# Example 2: E-Commerce Order Insights
#
# Scenario:
#          You run an online store and want users 
#          to ask natural-language questions about 
#          orders, products, and customers.

# MySQL Schema: ecommerce_db

"""
CREATE DATABASE ecommerce_db;
USE ecommerce_db;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(8,2)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
"""


# Sample Prompt to OpenAI
prompt = """
You are a SQL expert assistant.
Schema:
customers(customer_id, name, email)
products(product_id, name, price)
orders(order_id, customer_id, order_date)
order_items(order_item_id, order_id, product_id, quantity)

User Question: Which customer spent the most last month?
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
    You are a SQL expert assistant.
    Schema:
    customers(customer_id, name, email)
    products(product_id, name, price)
    orders(order_id, customer_id, order_date)
    order_items(order_item_id, order_id, product_id, quantity)

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
print(generate_sql(client, "Which product was ordered the most in June?"))
