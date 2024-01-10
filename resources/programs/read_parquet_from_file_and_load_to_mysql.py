#-----------------------------
#  INSTALL these required libraries:
#
#     pip install flask_sqlalchemy
#     pip install pymysql
#     pip install pandas
#-----------------------------

#-----------------------------
# running this program: 
#      % python3 read_parquet_from_file_and_load_to_mysql.py
#-----------------------------

import pandas as pd

"""
read a Parquet file and create a Python dataframe
"""

#--------------------
# define parquet file
#--------------------
parquet_file = "/tmp/data-warehousing/resources/data/Iris.parquet"


#------------------------------------------------
# read parquet file and create a python dataframe
#------------------------------------------------
df = pd.read_parquet(parquet_file, engine='auto')
print("df=", df)

"""


df=      sepal.length  sepal.width  petal.length  petal.width    variety
0             5.1          3.5           1.4          0.2     Setosa
1             4.9          3.0           1.4          0.2     Setosa
2             4.7          3.2           1.3          0.2     Setosa
3             4.6          3.1           1.5          0.2     Setosa
4             5.0          3.6           1.4          0.2     Setosa
..            ...          ...           ...          ...        ...
145           6.7          3.0           5.2          2.3  Virginica
146           6.3          2.5           5.0          1.9  Virginica
147           6.5          3.0           5.2          2.0  Virginica
148           6.2          3.4           5.4          2.3  Virginica
149           5.9          3.0           5.1          1.8  Virginica

[150 rows x 5 columns]
"""

#--------------------------
# load dataframe into MySQL
#--------------------------

# Connect String format:
# mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]

db_user = "root"
db_password = "myrootpassword"
db_name = "test"

# define connection string
connection_string = "mysql+pymysql://%s:%s@%s:%s/%s" % (db_user, db_password, 'localhost', '3306', db_name)

# import required library
from sqlalchemy import create_engine

# create engine using connection 
db_connection = create_engine(connection_string)


# create db table named 'iris'
df.to_sql(name = "iris", con = db_connection, if_exists = 'append', index = False)


"""
mysql> use test;

mysql> select count(*) from iris ;
+----------+
| count(*) |
+----------+
|      150 |
+----------+
1 row in set (0.00 sec)


mysql> select * from iris;
+--------------+-------------+--------------+-------------+------------+
| sepal.length | sepal.width | petal.length | petal.width | variety    |
+--------------+-------------+--------------+-------------+------------+
|          5.1 |         3.5 |          1.4 |         0.2 | Setosa     |
|          4.9 |           3 |          1.4 |         0.2 | Setosa     |
|          4.7 |         3.2 |          1.3 |         0.2 | Setosa     |
...
|          6.3 |         2.5 |            5 |         1.9 | Virginica  |
|          6.5 |           3 |          5.2 |           2 | Virginica  |
|          6.2 |         3.4 |          5.4 |         2.3 | Virginica  |
|          5.9 |           3 |          5.1 |         1.8 | Virginica  |
+--------------+-------------+--------------+-------------+------------+
150 rows in set (0.00 sec)

mysql>
"""
