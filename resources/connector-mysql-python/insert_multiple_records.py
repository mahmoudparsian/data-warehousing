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
sql = """
          INSERT INTO customers (cust_id, cust_fname, cust_lname, address) 
              VALUES (%s, %s, %s, %s)
"""

# prepare values fro SQL query
vals = [
  (3000, 'Peter', 'Jordan', 'Lowstreet 4'),
  (4000, 'Amy', 'Jackson', 'Apple st 652'),
  (5000, 'Hannah', 'Montana', 'Mountain 21'),
  (6000, 'Michael', 'Taylor', 'Valley 345')]
  
print(vals)
#
# Insert MANY records
db_cursor.executemany(sql, vals)

db_connection.commit()

print(db_cursor.rowcount, " record inserted.")
