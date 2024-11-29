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
#
#      % python3 etl_insurace_csv_load_to_mysql.py
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

db_table_name = "insurance_from_etl"
df.to_sql(db_table_name, conn, if_exists="append")

# Do not worry if you don't have the table already. 
# A table gets created with the name that you pass into to_sql().

# Now go and query for the table results. You will see the data inserted.

"""

"""