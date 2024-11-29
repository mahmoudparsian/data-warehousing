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
#      % python3 etl_ev_csv_load_to_mysql.py
#-----------------------------

# Install packages
# As we are going to work with an excel using pandas 
# and mysql database, first we need to install the 
#required packages.

"""
pip install pandas
pip install sqlalchemy
pip install pymysql

sqlalchemy and pymysql is required for connecting with mysql.

Make a connection to your mysql
You should have your MySQL database ready. 

create_engine() lets you create an engine instance, 
basically a starting point of sqlalchemy application. 
You have to pass here a URL string that indicates 
database dialect and connection parameters. 
Replace username, password, host, port, database with 
your corresponding values.
"""

import pandas as pd
import sys
from sqlalchemy import create_engine

#-----------------------------------
def create_db_connection():
    # engine = create_engine("mysql+pymysql://" + "username" + ":" + "password" + "@" + "host" + ":" + "port" + "/" + "database" + "?" + "charset=utf8mb4")
    db_user = "root"
    db_password = "password"
    db_name = "test"
    engine = create_engine("mysql+pymysql://" + db_user + ":" + db_password + "@" + "localhost" + ":" + "3306" + "/" + db_name + "?" + "charset=utf8mb4")
    return engine.connect()
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
csv_file = "Electric_Vehicle_Population_Data.csv"

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

"""
df=         VIN (1-10)     County         City  ... DOL Vehicle ID                                   Electric Utility  2020 Census Tract
0       5YJ3E1EB4L     Yakima       Yakima  ...      127175366                                         PACIFICORP       5.307700e+10
1       5YJ3E1EA7K  San Diego    San Diego  ...      266614659                                                NaN       6.073005e+09
2       7JRBR0FL9M       Lane       Eugene  ...      144502018                                                NaN       4.103900e+10
3       5YJXCBE21K     Yakima       Yakima  ...      477039944                                         PACIFICORP       5.307700e+10
4       5UXKT0C5XH  Snohomish      Bothell  ...      106314946                             PUGET SOUND ENERGY INC       5.306105e+10
...            ...        ...          ...  ...            ...                                                ...                ...
124711  5YJ3E1EB6N  Snohomish       Monroe  ...      192999061                             PUGET SOUND ENERGY INC       5.306105e+10
124712  KNDCM3LD2L     Pierce       Tacoma  ...      113346250  BONNEVILLE POWER ADMINISTRATION||CITY OF TACOM...       5.305306e+10
124713  7SAYGDEE0P    Whatcom   Bellingham  ...      232751305  PUGET SOUND ENERGY INC||PUD NO 1 OF WHATCOM CO...       5.307300e+10
124714  1G1FW6S03J     Pierce       Tacoma  ...      102589007  BONNEVILLE POWER ADMINISTRATION||CITY OF TACOM...       5.305307e+10
124715  1G1RC6E47F     Benton  Benton City  ...      476974718  BONNEVILLE POWER ADMINISTRATION||PUD NO 1 OF B...       5.300501e+10

[124716 rows x 15 columns]
col=::VIN (1-10)::
col=::County::
col=::City::
col=::State::
col=::Postal Code::
col=::Model Year::
col=::Make::
col=::Model::
col=::Electric Vehicle Type::
col=::Electric Range::
col=::Base MSRP::
col=::Legislative District::
col=::DOL Vehicle ID::
col=::Electric Utility::
col=::2020 Census Tract::
"""

#--------------------------------
# Transformation...
#--------------------------------
# Rename column names for MySQL
#--------------------------------
# Remove Spaces from column names
#--------------------------------
df.rename(columns={"VIN (1-10)": "VIN"}, inplace=True)
df.rename(columns={"Postal Code": "Postal_Code"}, inplace=True)
df.rename(columns={"Model Year": "Model_Year"}, inplace=True)
df.rename(columns={"Electric Vehicle Type": "Electric_Vehicle_Type"}, inplace=True)
df.rename(columns={"Clean Alternative Fuel Vehicle (CAFV) Eligibility": "CAFV_Eligibility"}, inplace=True)
df.rename(columns={"Electric Range": "Electric_Range"}, inplace=True)
df.rename(columns={"Base MSRP": "Base_MSRP"}, inplace=True)
df.rename(columns={"Legislative District": "Legislative_District"}, inplace=True)
df.rename(columns={"DOL Vehicle ID": "DOL_Vehicle_ID"}, inplace=True)
#df.rename(columns={"Vehicle Location": "Vehicle_Location"}, inplace=True)
df.rename(columns={"Electric Utility": "Electric_Utility"}, inplace=True)
df.rename(columns={"2020 Census Tract": "Census_Tract_2020"}, inplace=True)

# debug df
print("df=", df)

# print all column names
for col in df.columns:
    print("col=::"+col+"::")

"""
df=                VIN     County         City  ... DOL_Vehicle_ID                                   Electric_Utility  Census_Tract_2020
0       5YJ3E1EB4L     Yakima       Yakima  ...      127175366                                         PACIFICORP       5.307700e+10
1       5YJ3E1EA7K  San Diego    San Diego  ...      266614659                                                NaN       6.073005e+09
2       7JRBR0FL9M       Lane       Eugene  ...      144502018                                                NaN       4.103900e+10
3       5YJXCBE21K     Yakima       Yakima  ...      477039944                                         PACIFICORP       5.307700e+10
4       5UXKT0C5XH  Snohomish      Bothell  ...      106314946                             PUGET SOUND ENERGY INC       5.306105e+10
...            ...        ...          ...  ...            ...                                                ...                ...
124711  5YJ3E1EB6N  Snohomish       Monroe  ...      192999061                             PUGET SOUND ENERGY INC       5.306105e+10
124712  KNDCM3LD2L     Pierce       Tacoma  ...      113346250  BONNEVILLE POWER ADMINISTRATION||CITY OF TACOM...       5.305306e+10
124713  7SAYGDEE0P    Whatcom   Bellingham  ...      232751305  PUGET SOUND ENERGY INC||PUD NO 1 OF WHATCOM CO...       5.307300e+10
124714  1G1FW6S03J     Pierce       Tacoma  ...      102589007  BONNEVILLE POWER ADMINISTRATION||CITY OF TACOM...       5.305307e+10
124715  1G1RC6E47F     Benton  Benton City  ...      476974718  BONNEVILLE POWER ADMINISTRATION||PUD NO 1 OF B...       5.300501e+10

[124716 rows x 15 columns]
col=::VIN::
col=::County::
col=::City::
col=::State::
col=::Postal_Code::
col=::Model_Year::
col=::Make::
col=::Model::
col=::Electric_Vehicle_Type::
col=::Electric_Range::
col=::Base_MSRP::
col=::Legislative_District::
col=::DOL_Vehicle_ID::
col=::Electric_Utility::
col=::Census_Tract_2020::
"""

# After creating the instance, now you 
# should establish a connection to the 
# database using connect().

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

db_table_name = "ev_table_from_csv"
df.to_sql(db_table_name, conn, if_exists="append")

# Do not worry if you don't have the table already. 
# A table gets created with the name that you pass into to_sql().

# Now go and query for the table results. You will see the data inserted.

"""
Electric-Vehicle-Population_Data (main) % mysql -h localhost -u root -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 16
Server version: 8.1.0 MySQL Community Server - GPL

Copyright (c) 2000, 2024, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> use test;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> select count(*) from ev_table_from_csv;
+----------+
| count(*) |
+----------+
|   124716 |
+----------+
1 row in set (0.01 sec)

mysql> select * from ev_table_from_csv limit 5;
+-------+------------+-----------+-----------+-------+-------------+------------+-------+---------+----------------------------------------+----------------+-----------+----------------------+----------------+------------------------+-------------------+
| index | VIN        | County    | City      | State | Postal_Code | Model_Year | Make  | Model   | Electric_Vehicle_Type                  | Electric_Range | Base_MSRP | Legislative_District | DOL_Vehicle_ID | Electric_Utility       | Census_Tract_2020 |
+-------+------------+-----------+-----------+-------+-------------+------------+-------+---------+----------------------------------------+----------------+-----------+----------------------+----------------+------------------------+-------------------+
|     0 | 5YJ3E1EB4L | Yakima    | Yakima    | WA    |       98908 |       2020 | TESLA | MODEL 3 | Battery Electric Vehicle (BEV)         |            322 |         0 |                   14 |      127175366 | PACIFICORP             |       53077000904 |
|     1 | 5YJ3E1EA7K | San Diego | San Diego | CA    |       92101 |       2019 | TESLA | MODEL 3 | Battery Electric Vehicle (BEV)         |            220 |         0 |                 NULL |      266614659 | NULL                   |        6073005102 |
|     2 | 7JRBR0FL9M | Lane      | Eugene    | OR    |       97404 |       2021 | VOLVO | S60     | Plug-in Hybrid Electric Vehicle (PHEV) |             22 |         0 |                 NULL |      144502018 | NULL                   |       41039002401 |
|     3 | 5YJXCBE21K | Yakima    | Yakima    | WA    |       98908 |       2019 | TESLA | MODEL X | Battery Electric Vehicle (BEV)         |            289 |         0 |                   14 |      477039944 | PACIFICORP             |       53077000401 |
|     4 | 5UXKT0C5XH | Snohomish | Bothell   | WA    |       98021 |       2017 | BMW   | X5      | Plug-in Hybrid Electric Vehicle (PHEV) |             14 |         0 |                    1 |      106314946 | PUGET SOUND ENERGY INC |       53061051918 |
+-------+------------+-----------+-----------+-------+-------------+------------+-------+---------+----------------------------------------+----------------+-----------+----------------------+----------------+------------------------+-------------------+
5 rows in set (0.00 sec)

mysql>
"""