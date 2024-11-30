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
#     pip install sqlalchemy
#-----------------------------

#-----------------------------
# running this program: 
#
#      % python3 etl_insurace_csv_load_to_mysql.py
#-----------------------------

# Install packages
# As we are going to work with an excel using pandas 
# and mysql database, first we need to install the 
#required packages.


import pandas as pd
import sys
from sqlalchemy import create_engine

#-----------------------------------
def create_db_connection():
    # engine = create_engine("mysql+pymysql://" + "username" + ":" + "password" + "@" + "host" + ":" + "port" + "/" + "database" + "?" + "charset=utf8mb4")
    db_user = "root"
    db_password = "mp22pass"
    db_name = "test"
    engine = create_engine("mysql+pymysql://" + db_user + ":" + db_password + "@" + "localhost" + ":" + "3306" + "/" + db_name + "?" + "charset=utf8mb4")
    return engine.connect()
#end-def
#-----------------------------------
# Transformation : healthy BMI :
#
# Doctors recommend most adults keep their 
# BMI between 18 and 24.9. 
# 
# Adults with a BMI over 25 are considered 
# overweight and a BMI over 30 is considered obese. 
#
# We add a new column: bmi_indicator
#
# Transformation
#   bmi < 25 ==> normal 
#   bmi >= 25 and bmi <= 30 ==> overweight
#   bmi > 30  ==> obese
#
def compute_bmi_indicator(bmi):
    if (bmi < 25.0):
        return 'normal'
    elif (bmi >= 25.0 and bmi <= 30.0):
        return 'overweight'
    else:
        return 'obese'
    #end-if
#end-def
#-----------------------------------
# Transformation : compute age group
#
# It is common in demography to split 
# the population into three broad age groups: 
# 1. children and young adolescents (under 13 years old) ==> young
# 2. teenagers: 13-19 ==> teens
# 3. the working-age population (20–64 years) ==> working
# 4. the elderly population (65 years and older) ==> elderly

def compute_age_group(age):
    if age < 13:
        return 'young'
    elif age >= 13 and age < 20:
        return 'teens'
    elif age >= 20 and age < 65:
        return 'working'
    else:
        return 'elderly'
#end-def
#-----------------------------------
"""
1. read a CSV file, create a DataFrame 
2. transform created DataFrame
3. load DataFrame to MySQL
"""

#------------------------------------
# define CSV file
#------------------------------------

# csv_file = "insurance.csv"
csv_file = sys.argv[1]
print("csv_file=", csv_file)

#------------------------------------------------
# 1. EXTRACT
#
# read csv file and create a python dataframe
#------------------------------------------------
df = pd.read_csv(csv_file)
print("df=", df)

# print all column names
for col in df.columns:
    print("col=::"+col+"::")

#------------------------------------------------
# 2. Apply Transformations ...
#------------------------------------------------

# After creating the instance, now you 
# should establish a connection to the 
# database using connect().

#------------------------------------------------
# Transformation 1 : healthy BMI : bmi indicator
#------------------------------------------------
# We add a new column: bmi_indicator
#
df['bmi_indicator'] = df['bmi'].apply(compute_bmi_indicator)

#----------------------------------
# Transformation 2 : find age group
#----------------------------------
# We add a new column: age_group
#
df['age_group'] = df['age'].apply(compute_age_group)


#-------------------
# some debugging...
#-------------------
print("df=", df)

# print all column names
for col in df.columns:
    print("col=::"+col+"::")

# exit()

conn = create_db_connection()
print("conn=::"+str(conn)+"::")

# Now that we have our connection established, 
# Load the data into mysql
# To load our excel_dataframe to mysql, we use 
# to_sql() with table name and sql connection 
# arguments. Here I have given table name as 
# financial_table. 

# The parameter if_exists checks if the table 
# already exists in the database. If yes, in 
# this case it will append the data.

db_table_name = "insurance_from_etl2"
df.to_sql(db_table_name, conn, if_exists="append")

# Do not worry if you don't have the table already. 
# A table gets created with the name that you pass into to_sql().

# Now go and query for the table results. You will see the data inserted.

"""
 % mysql -h localhost -u root -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 35
Server version: 8.1.0 MySQL Community Server - GPL

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> desc test.insurance_from_etl2;
+---------------+--------+------+-----+---------+-------+
| Field         | Type   | Null | Key | Default | Extra |
+---------------+--------+------+-----+---------+-------+
| index         | int    | YES  |     | NULL    |       |
| age           | int    | YES  |     | NULL    |       |
| sex           | text   | YES  |     | NULL    |       |
| bmi           | double | YES  |     | NULL    |       |
| children      | int    | YES  |     | NULL    |       |
| smoker        | text   | YES  |     | NULL    |       |
| region        | text   | YES  |     | NULL    |       |
| charges       | double | YES  |     | NULL    |       |
| bmi_indicator | text   | YES  |     | NULL    |       |
| age_group     | text   | YES  |     | NULL    |       |
+---------------+--------+------+-----+---------+-------+
10 rows in set (0.01 sec)

mysql> select age_group, count(*) as count from test.insurance_from_etl2 group by age_group;
+-----------+-------+
| age_group | count |
+-----------+-------+
| teens     |   137 |
| working   |  1201 |
+-----------+-------+
2 rows in set (0.00 sec)

mysql> select bmi_indicator, count(*) as count from test.insurance_from_etl2 group by bmi_indicator;
+---------------+-------+
| bmi_indicator | count |
+---------------+-------+
| overweight    |   388 |
| obese         |   705 |
| normal        |   245 |
+---------------+-------+
3 rows in set (0.01 sec)

mysql>

mysql> select age_group, bmi_indicator, count(*) as total from insurance_from_etl2 group by age_group, bmi_indicator with ROLLUP;
+-----------+---------------+-------+
| age_group | bmi_indicator | total |
+-----------+---------------+-------+
| teens     | normal        |    32 |
| teens     | obese         |    70 |
| teens     | overweight    |    35 |
| teens     | NULL          |   137 |
| working   | normal        |   213 |
| working   | obese         |   635 |
| working   | overweight    |   353 |
| working   | NULL          |  1201 |
| NULL      | NULL          |  1338 |
+-----------+---------------+-------+
9 rows in set (0.00 sec)

mysql> select bmi_indicator, age_group, count(*) as total from insurance_from_etl2 group by bmi_indicator, age_group  with ROLLUP;
+---------------+-----------+-------+
| bmi_indicator | age_group | total |
+---------------+-----------+-------+
| normal        | teens     |    32 |
| normal        | working   |   213 |
| normal        | NULL      |   245 |
| obese         | teens     |    70 |
| obese         | working   |   635 |
| obese         | NULL      |   705 |
| overweight    | teens     |    35 |
| overweight    | working   |   353 |
| overweight    | NULL      |   388 |
| NULL          | NULL      |  1338 |
+---------------+-----------+-------+
10 rows in set (0.00 sec)

"""