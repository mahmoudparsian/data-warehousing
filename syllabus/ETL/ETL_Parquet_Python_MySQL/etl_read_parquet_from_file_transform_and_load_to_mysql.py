#-----------------------------
# ETL example
#              1. Extract
#              2. Transform
#              3. Load
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
parquet_file = "/tmp/data-warehousing/resources/data/emps_9_records.snappy.parquet"

#------------------------------------------------
# 1. EXTRACT
#
# read parquet file and create a python dataframe
#------------------------------------------------
df = pd.read_parquet(parquet_file, engine='auto')
print("df=", df)


"""
df=    name       city date_creted  salary  bonus
0  alex       Ames   1/21/2020   34000   1200
1  alex  Sunnyvale   3/22/2020   32000   1500
2  alex  Cupertino   1/24/2020   40000    400
3  mary       Ames   2/20/2020   38000    800
4  mary   Stanford   1/19/2022   45000    500
5  mary   Campbell   9/20/2023   55000    600
6  jeff       Ames  12/21/2021   60000    700
7  jeff  Sunnyvale   4/10/2021   70000    300
8  jane     Austin   5/16/2022   80000    800
"""

#-------------------
# 2. TRANSFORM...
#-------------------
# TRANSFORM: 2.1 create a new column salary_and_bonus
# convert the date column into a datetime object
df['salary_and_bonus'] = df['salary'] + df['bonus']


# TRANSFORM 2.2 split the date column into 3 new columns (day, month, year)
# extract the day, month, and year components
df['pd_date'] = pd.to_datetime(df['date_created'])
df['day'] = df['pd_date'].dt.day
df['month'] = df['pd_date'].dt.month
df['year'] = df['pd_date'].dt.year

print("df=", df)

#--------------------------
# 3. LOAD dataframe into MySQL
#--------------------------

# Connect String format:
# mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]

db_user = "root"
db_password = "myrootpassword"
db_name = "test"
db_host = 'localhost'
db_port = 3306

# define connection string
connection_string = "mysql+pymysql://%s:%s@%s:%s/%s" % (db_user, db_password, db_host, db_port, db_name)

# import required library
from sqlalchemy import create_engine

# create engine using connection 
db_connection = create_engine(connection_string)


#----------
# 3. LOAD
#----------
# load to MySQL
# create db table named 'employees'
db_table = "employees"
df.to_sql(name = db_table, con = db_connection, if_exists = 'append', index = False)


"""

mysql> use test;
Database changed

mysql> show tables;
+----------------+
| Tables_in_test |
+----------------+
| employees      |
| emps           |
| iris           |
| my_table       |
| scu_iris       |
+----------------+
5 rows in set (0.00 sec)

mysql> select * from employees;
+------+-----------+--------------+--------+-------+------------------+---------------------+------+-------+------+
| name | city      | date_created | salary | bonus | salary_and_bonus | pd_date             | day  | month | year |
+------+-----------+--------------+--------+-------+------------------+---------------------+------+-------+------+
| alex | Ames      | 1/21/2020    |  34000 |  1200 |            35200 | 2020-01-21 00:00:00 |   21 |     1 | 2020 |
| alex | Sunnyvale | 3/22/2020    |  32000 |  1500 |            33500 | 2020-03-22 00:00:00 |   22 |     3 | 2020 |
| alex | Cupertino | 1/24/2020    |  40000 |   400 |            40400 | 2020-01-24 00:00:00 |   24 |     1 | 2020 |
| mary | Ames      | 2/20/2020    |  38000 |   800 |            38800 | 2020-02-20 00:00:00 |   20 |     2 | 2020 |
| mary | Stanford  | 1/19/2022    |  45000 |   500 |            45500 | 2022-01-19 00:00:00 |   19 |     1 | 2022 |
| mary | Campbell  | 9/20/2023    |  55000 |   600 |            55600 | 2023-09-20 00:00:00 |   20 |     9 | 2023 |
| jeff | Ames      | 12/21/2021   |  60000 |   700 |            60700 | 2021-12-21 00:00:00 |   21 |    12 | 2021 |
| jeff | Sunnyvale | 4/10/2021    |  70000 |   300 |            70300 | 2021-04-10 00:00:00 |   10 |     4 | 2021 |
| jane | Austin    | 5/16/2022    |  80000 |   800 |            80800 | 2022-05-16 00:00:00 |   16 |     5 | 2022 |
+------+-----------+--------------+--------+-------+------------------+---------------------+------+-------+------+
9 rows in set (0.00 sec)

mysql>
"""
