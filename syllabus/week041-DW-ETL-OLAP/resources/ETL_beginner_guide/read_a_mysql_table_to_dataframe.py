#-----------------------------------
# Read  MySQL Table into a dataframe 
#-----------------------------------

"""
To read a MySQL table into Pandas DataFrame, 
you can use the 

read_sql_table(): to read entire table

read_sql_query(): to read some/alle table



SQLAlchemy is the Python SQL toolkit and 
           Object Relational Mapper that 
           gives application developers the 
           full power and flexibility of SQL.
"""

import pandas as pd
from sqlalchemy import create_engine


#-----------------------------------
# Read  MySQL Table into a dataframe 
#-----------------------------------
# Create a SQLAlchemy engine to connect to your MySQL database
#engine = create_engine('mysql+mysqlconnector://user:password@host:port/database_name')
engine = create_engine('mysql+mysqlconnector://root:mp22pass@localhost:3306/test_db')

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

#------------------------------------
# Read a MySQL Table into a dataframe 
#------------------------------------
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

#------------------------------------
# Read MySQL Table using a SQL query:
#------------------------------------
sql_query = "SELECT * FROM my_table_name WHERE age > 25"
df3 = pd.read_sql_query(sql_query, engine)
#
print("df3:\n")
print(df3)
"""
df3:

   name  age
0  Mary   30
1  Alex   40
"""
