#-----------------------------
# ELT example:
#              1. Extract
#              2. Load
#              3. Transform
#-----------------------------
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
# 2. LOAD
#----------
# load to MySQL
# create db table named 'employees'
db_table = "employees"
df.to_sql(name = db_table, con = db_connection, if_exists = 'append', index = False)

#-------------------
# 3. TRANSFORM...
#-------------------
"""
mysql> CREATE TABLE new_emps select name, city, date_created, salary, bonus, SUBSTRING_INDEX(date_created, '/', 1) AS month, SUBSTRING_INDEX(SUBSTRING_INDEX(date_created,'/', 2), '/',-1)  AS day, SUBSTRING_INDEX(date_created, '/', -1) as year  from employees;
Query OK, 9 rows affected (0.02 sec)
Records: 9  Duplicates: 0  Warnings: 0

mysql> select * from new_emps;
+------+-----------+--------------+--------+-------+-------+------+------+
| name | city      | date_created | salary | bonus | month | day  | year |
+------+-----------+--------------+--------+-------+-------+------+------+
| alex | Ames      | 1/21/2020    |  34000 |  1200 | 1     | 21   | 2020 |
| alex | Sunnyvale | 3/22/2020    |  32000 |  1500 | 3     | 22   | 2020 |
| alex | Cupertino | 1/24/2020    |  40000 |   400 | 1     | 24   | 2020 |
| mary | Ames      | 2/20/2020    |  38000 |   800 | 2     | 20   | 2020 |
| mary | Stanford  | 1/19/2022    |  45000 |   500 | 1     | 19   | 2022 |
| mary | Campbell  | 9/20/2023    |  55000 |   600 | 9     | 20   | 2023 |
| jeff | Ames      | 12/21/2021   |  60000 |   700 | 12    | 21   | 2021 |
| jeff | Sunnyvale | 4/10/2021    |  70000 |   300 | 4     | 10   | 2021 |
| jane | Austin    | 5/16/2022    |  80000 |   800 | 5     | 16   | 2022 |
+------+-----------+--------------+--------+-------+-------+------+------+
9 rows in set (0.00 sec)

mysql> ALTER TABLE `new_emps` ADD `salary_and_bonus` INT;
Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> select * from new_emps;
+------+-----------+--------------+--------+-------+-------+------+------+------------------+
| name | city      | date_created | salary | bonus | month | day  | year | salary_and_bonus |
+------+-----------+--------------+--------+-------+-------+------+------+------------------+
| alex | Ames      | 1/21/2020    |  34000 |  1200 | 1     | 21   | 2020 |             NULL |
| alex | Sunnyvale | 3/22/2020    |  32000 |  1500 | 3     | 22   | 2020 |             NULL |
| alex | Cupertino | 1/24/2020    |  40000 |   400 | 1     | 24   | 2020 |             NULL |
| mary | Ames      | 2/20/2020    |  38000 |   800 | 2     | 20   | 2020 |             NULL |
| mary | Stanford  | 1/19/2022    |  45000 |   500 | 1     | 19   | 2022 |             NULL |
| mary | Campbell  | 9/20/2023    |  55000 |   600 | 9     | 20   | 2023 |             NULL |
| jeff | Ames      | 12/21/2021   |  60000 |   700 | 12    | 21   | 2021 |             NULL |
| jeff | Sunnyvale | 4/10/2021    |  70000 |   300 | 4     | 10   | 2021 |             NULL |
| jane | Austin    | 5/16/2022    |  80000 |   800 | 5     | 16   | 2022 |             NULL |
+------+-----------+--------------+--------+-------+-------+------+------+------------------+
9 rows in set (0.00 sec)

mysql> update new_emps set salary_and_bonus = salary + bonus;
Query OK, 9 rows affected (0.01 sec)
Rows matched: 9  Changed: 9  Warnings: 0

mysql> select * from new_emps;
+------+-----------+--------------+--------+-------+-------+------+------+------------------+
| name | city      | date_created | salary | bonus | month | day  | year | salary_and_bonus |
+------+-----------+--------------+--------+-------+-------+------+------+------------------+
| alex | Ames      | 1/21/2020    |  34000 |  1200 | 1     | 21   | 2020 |            35200 |
| alex | Sunnyvale | 3/22/2020    |  32000 |  1500 | 3     | 22   | 2020 |            33500 |
| alex | Cupertino | 1/24/2020    |  40000 |   400 | 1     | 24   | 2020 |            40400 |
| mary | Ames      | 2/20/2020    |  38000 |   800 | 2     | 20   | 2020 |            38800 |
| mary | Stanford  | 1/19/2022    |  45000 |   500 | 1     | 19   | 2022 |            45500 |
| mary | Campbell  | 9/20/2023    |  55000 |   600 | 9     | 20   | 2023 |            55600 |
| jeff | Ames      | 12/21/2021   |  60000 |   700 | 12    | 21   | 2021 |            60700 |
| jeff | Sunnyvale | 4/10/2021    |  70000 |   300 | 4     | 10   | 2021 |            70300 |
| jane | Austin    | 5/16/2022    |  80000 |   800 | 5     | 16   | 2022 |            80800 |
+------+-----------+--------------+--------+-------+-------+------+------+------------------+
9 rows in set (0.00 sec)

"""