import mysql.connector

db_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mp22pass",
  database="test"
)

db_cursor = db_connection.cursor()

"""
CREATE TABLE customers (
    cust_id     INT             NOT NULL,
    cust_fname  VARCHAR(40)     NOT NULL,
    cust_lname  VARCHAR(40)     NOT NULL,
    address     VARCHAR(60)     NOT NULL,
    PRIMARY KEY (cust_id)
);
"""

# prepare SQL query
db_cursor.execute("SELECT * FROM customers")

result_set = db_cursor.fetchall()

for x in result_set:
  print(x)