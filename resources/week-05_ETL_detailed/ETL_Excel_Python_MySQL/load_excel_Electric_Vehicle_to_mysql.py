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

import pandas as pd
import sys
from sqlalchemy import create_engine

def create_db_connection():
    # engine = create_engine("mysql+pymysql://" + "username" + ":" + "password" + "@" + "host" + ":" + "port" + "/" + "database" + "?" + "charset=utf8mb4")
    db_user = "root"
    db_password = "password"
    db_name = "test"
    engine = create_engine("mysql+pymysql://" + db_user + ":" + db_password + "@" + "localhost" + ":" + "3306" + "/" + db_name + "?" + "charset=utf8mb4")
    return engine.connect()
#end-def


# it is time to work a little with Pandas.

# Reading an excel file using Pandas
# First create an excel file obj using 
# pandas ExcelFile() and pass your filename inside.


# excel_file_name = sys.argv[1]
excel_file_name = "Electric_Vehicle_Population_Data.xlsx"
print("excel_file=", excel_file_name)

# create Excel file as an excel_file object
excel_file = pd.ExcelFile(excel_file_name)

# After creating the excel file obj, now it's 
# time to parse the excel sheet using parse() function. 
# Pass the sheet name that you want to process.

excel_dataframe = excel_file.parse(sheet_name="Electric_Vehicle_Population_Dat")

# And yes! The data has been copied to a dataframe.
# Let's move on to the last step where we load this 
# into our mysql table.

print("excel_dataframe=",excel_dataframe)

# print all column names
for col in excel_dataframe.columns:
    print("col=::"+col+"::")

"""
col=::VIN (1-10)::
col=::County::
col=::City::
col=::State::
col=::Postal Code::
col=::Model Year::
col=::Make::
col=::Model::
col=::Electric Vehicle Type::
col=::Clean Alternative Fuel Vehicle (CAFV) Eligibility::
col=::Electric Range::
col=::Base MSRP::
col=::Legislative District::
col=::DOL Vehicle ID::
col=::Vehicle Location::
col=::Electric Utility::
col=::2020 Census Tract::
"""

# Remove Spaces from column names
excel_dataframe.rename(columns={"VIN (1-10)": "VIN"}, inplace=True)
excel_dataframe.rename(columns={"Postal Code": "Postal_Code"}, inplace=True)
excel_dataframe.rename(columns={"Model Year": "Model_Year"}, inplace=True)
excel_dataframe.rename(columns={"Electric Vehicle Type": "Electric_Vehicle_Type"}, inplace=True)
excel_dataframe.rename(columns={"Clean Alternative Fuel Vehicle (CAFV) Eligibility": "CAFV_Eligibility"}, inplace=True)
excel_dataframe.rename(columns={"Electric Range": "Electric_Range"}, inplace=True)
excel_dataframe.rename(columns={"Base MSRP": "Base_MSRP"}, inplace=True)
excel_dataframe.rename(columns={"Legislative District": "Legislative_District"}, inplace=True)
excel_dataframe.rename(columns={"DOL Vehicle ID": "DOL_Vehicle_ID"}, inplace=True)
excel_dataframe.rename(columns={"Vehicle Location": "Vehicle_Location"}, inplace=True)
excel_dataframe.rename(columns={"Electric Utility": "Electric_Utility"}, inplace=True)
excel_dataframe.rename(columns={"2020 Census Tract": "Census_Tract_2020"}, inplace=True)

# print all revised column names
print("\n Revised column names:\n")
for col in excel_dataframe.columns:
    print("col=::"+col+"::")

"""
Revised column names:

col=::VIN::
col=::County::
col=::City::
col=::State::
col=::Postal_Code::
col=::Model_Year::
col=::Make::
col=::Model::
col=::Electric_Vehicle_Type::
col=::CAFV_Eligibility::
col=::Electric_Range::
col=::Base_MSRP::
col=::Legislative_District::
col=::DOL_Vehicle_ID::
col=::Vehicle_Location::
col=::Electric_Utility::
col=::Census_Tract_2020::
"""
# exit()

# After creating the instance, now you 
# should establish a connection to the 
# database using connect().

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

excel_dataframe.to_sql("ev_table", conn, if_exists="append")

# Do not worry if you don't have the table already. 
# A table gets created with the name that you pass into to_sql().

# Now go and query for the table results. You will see the data inserted.

