# Writing Excel Data to MySQL using Pandas

# This is going to be a very basic and simple way 
# of migrating excel data to a mysql table with 
# the help of Pandas . Being a popular data analysis 
# and manipulation python library, it provides a 
# lot of features to work with data. Let us see one 
# of those here.

# Install packages
# As we are going to work with an excel using pandas 
# and mysql database, first we need to install the 
#required packages.

"""
pip install pandas
pip install openpyxl
pip install sqlalchemy
pip install pymysql

openpyxl is required to work with .xlsx files. 
sqlalchemy and pymysql is required for connecting with mysql.

Be ready with a sample .xlsx file: financial_sample.xlsx

Make a connection to your mysql
You should have your MySQL database ready. 

create_engine() lets you create an engine instance, 
basically a starting point of sqlalchemy application. 
You have to pass here a URL string that indicates 
database dialect and connection parameters. 
Replace username, password, host, port, database with 
your corresponding values.
"""

import sys
import json
import pandas as pd
from sqlalchemy import create_engine

#-----------------------------------------
# Database config is given as a JSON file
# read a JSON file and return a dictionary
#
def read_json(json_config_file):
    with open(json_config_file) as f:
        # Load the JSON data into a Python dictionary
        config_as_dict = json.load(f)
        return config_as_dict
#end-def
#-----------------------------------------
#
def create_db_connection(db_config):
    # engine = create_engine("mysql+pymysql://" + "username" + ":" + "password" + "@" + "host" + ":" + "port" + "/" + "database" + "?" + "charset=utf8mb4")
    #
    db_user = db_config["user"]
    db_password = db_config["password"]
    db_name = db_config["database"]
    db_host = db_config["host"]
    #
    engine = create_engine("mysql+pymysql://" + db_user + ":" + db_password + "@" + db_host + ":" + "3306" + "/" + db_name + "?" + "charset=utf8mb4")
    # After creating the instance, now you 
    # should establish a connection to the 
    # database using connect().    
    return engine.connect();
#
#end-def
#-------------------------------------------------
# Python main driver program ....
#-------------------------------------------------
# Command Line Parameter 1: 
# excel_file_name = "data_financial_sample.xlsx"
#-------------------------------------------------
excel_file_name = sys.argv[1]
# excel_file_name = "data_financial_sample.xlsx"
print("excel_file_name=", excel_file_name)


#-------------------------------------------------
# Command Line Parameter 2: "db_config.json"
#-------------------------------------------------
# This is for a "Star Schema" Database
# db_config_file = "db_config.json"
db_config_file = sys.argv[2]

db_config = read_json(db_config_file)
print("db_config=", db_config)


# create Excel file as an excel_file object
excel_file = pd.ExcelFile(excel_file_name)
print("excel_file=", excel_file)

# After creating the excel file obj, now it's 
# time to parse the excel sheet using parse() function. 
# Pass the sheet name that you want to process.

excel_dataframe = excel_file.parse(sheet_name="Sheet1")
#print("excel_dataframe=", excel_dataframe)

# And yes! The data has been copied to a dataframe.
# Let's move on to the last step where we load this 
# into our mysql table.

print("excel_dataframe=",excel_dataframe)

# Load the data into mysql
# To load our excel_dataframe to mysql, we use 
# to_sql() with table name and sql connection 
# arguments. Here I have given table name as 
# financial_table. 

# The parameter if_exists checks if the table 
# already exists in the database. If yes, in 
# this case it will append the data.

# After creating the instance, now you 
# should establish a connection to the 
# database using connect().

conn = create_db_connection(db_config)
print("conn=", conn)

excel_dataframe.to_sql("financial_table_2", conn, if_exists="append")

# Do not worry if you don't have the table already. 
# A table gets created with the name that you pass into to_sql().

# Now go and query for the table results. You will see the data inserted.

