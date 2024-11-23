"""
To write a Pandas DataFrame to MySQL, 
you can use the to_sql() method:

Explanation:
1. Import necessary libraries:
pandas for working with DataFrames
sqlalchemy to create a database connection engine

2. Create a DataFrame:
This is the DataFrame you want to write to MySQL.

3. Create a SQLAlchemy engine:
Replace the placeholders in the connection string 
with your actual MySQL database credentials:
user: Your MySQL username
password: Your MySQL password
host: Your MySQL server hostname or IP address
port: Your MySQL server port (usually 3306)
database_name: The name of the database you want to use

4. Write the DataFrame to MySQL:
Use the to_sql() method:
table_name: The name of the table you want to create or append to in MySQL
engine: The SQLAlchemy engine created in step 3
if_exists: Specifies what to do if the table already exists:
'replace': Replace the existing table with the DataFrame
'append': Append the DataFrame to the existing table
'fail': Raise an error if the table already exists
index: Set to False to avoid writing the DataFrame index as a column in the table

SQLAlchemy is the Python SQL toolkit and 
           Object Relational Mapper that 
           gives application developers the 
           full power and flexibility of SQL.
"""

import pandas as pd
from sqlalchemy import create_engine

# Create a DataFrame
df = pd.DataFrame({'name': ['John', 'Mary', 'Alex'], 
                   'age': [25, 30, 40]})

print("df:\n")
print(df)
"""
df:

   name  age
0  John   25
1  Mary   30
2  Alex   40
"""

#--------------------------------
# write dataframe to MySQL Table
#--------------------------------
# Create a SQLAlchemy engine to connect to your MySQL database
#engine = create_engine('mysql+mysqlconnector://user:password@host:port/database_name')
engine = create_engine('mysql+mysqlconnector://root:mp22pass@localhost:3306/test_db')

# Write the DataFrame to a MySQL table
df.to_sql('my_table_name', engine, if_exists='replace', index=False)
"""
 % mysql -h localhost -u root -p
Enter password: ...

mysql> use test_db;
Database changed

mysql> show tables;
+-------------------+
| Tables_in_test_db |
+-------------------+
| my_table_name     |
+-------------------+
1 row in set (0.00 sec)

mysql> select * from my_table_name;
+------+------+
| name | age  |
+------+------+
| John |   25 |
| Mary |   30 |
| Alex |   40 |
+------+------+
3 rows in set (0.00 sec)
"""

#--------------------------------
# write dataframe to MySQL Table
#--------------------------------
df2 = pd.read_sql_table('my_table_name', engine)
#
print("df2:\n")
print(df2)
"""
df2:

   name  age
0  John   25
1  Mary   30
2  Alex   40
"""

#----------------------------
# Read data using a SQL query:
#----------------------------
# query = "SELECT * FROM table_name WHERE condition"
# df3 = pd.read_sql_query(query, engine)
