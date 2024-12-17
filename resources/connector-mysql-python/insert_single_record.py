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
vals = (9000, 'Alex', 'Smith', 'Lowstreet 4')

  
print(vals)
#
# Insert one record
db_cursor.execute(sql, vals)

db_connection.commit()

print(db_cursor.rowcount, " record inserted.")
