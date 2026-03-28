#-----------------------------
# ETL example
#              1. Extract
#              2. Transform
#              3. Load
#-----------------------------
# Metadata for Yellow Cab
# https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
#-----------------------------
#  INSTALL these required libraries:
#
#     pip install flask_sqlalchemy
#     pip install pymysql
#     pip install pandas
#-----------------------------

#-----------------------------
# running this program: 
#      % python3 read_yellow_cab_data.py
#-----------------------------

# import required library
from sqlalchemy import create_engine

import pandas as pd
import sys

"""
Read a Parquet file and create a Python dataframe

Note: Parquet files are binary, which contain data and metadata
"""

#----------------------------------------
def get_db_connection():

    # Connect String format:
    # mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]

    db_user = "root"
    # db_password = "myrootpassword"
    db_name = "test"
    db_host = 'localhost'
    db_port = 3306

    # define connection string
    connection_string = "mysql+pymysql://%s:%s@%s:%s/%s" % (db_user, db_password, db_host, db_port, db_name)

    # create engine using connection 
    db_connection = create_engine(connection_string)
    #
    return db_connection
#end-def
#----------------------------------------
#
def write_to_database(source_dataframe, database_table, database_connection):
    #-----------------------------------------
    # write source dataframe to database table 
    # ----------------------------------------

    # write to database
    source_dataframe.to_sql(name = database_table, con = database_connection, if_exists = 'append', index = False)
    #
#end-def
#-----------------------------------------



#------------------------------------
# define flight data file
#
#------------------------------------
parquet_file = "/Users/mparsian/Downloads/flights_1million.parquet"
# parquet_file = sys.argv[1]
print("parquet_file=", parquet_file)

#------------------------------------------------
# 1. EXTRACT
#
# read parquet file and create a python dataframe
#------------------------------------------------
df = pd.read_parquet(parquet_file, engine='auto')
print("df=", df)
#
#
print("column names are:\n")
for index, column_name in enumerate(df.columns):
    print(index+1, column_name)
#
#

"""

"""

#--------------------
# Transform the data
#--------------------

#------------------------------------------------------------
# 1. we will use dropna() to remove the rows with missing data.
#
# Remove missing values.
# DataFrame with NA (null values) entries dropped from it 
#------------------------------------------------------------
number_of_rows = len(df.index)
df = df.dropna()  # Remove rows with missing data
number_of_rows_dropped = number_of_rows - len(df.index) 
print("df=", df)
print("number_of_rows_dropped=", number_of_rows_dropped)

#### number_of_rows_dropped= ?

#------------------------------------------------------------
# 2. rename 'tpep_pickup_datetime' to 'pickup_datetime'
#------------------------------------------------------------
#df = df.rename(columns={'tpep_pickup_datetime': 'pickup_datetime'})

#------------------------------------------------------------
# 3. rename 'tpep_dropoff_datetime': 'dropoff_datetime'
#------------------------------------------------------------
#df = df.rename(columns={'tpep_dropoff_datetime': 'dropoff_datetime'})
#print("after columns are renamed=", df)
#print("new column names are:\n")
#for index, column_name in enumerate(df.columns):
#    print(index+1, column_name)
    
#------------------------------------------------
# 4. convert 'pickup_datetime' to Pandas datetime
#------------------------------------------------
# df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])

#------------------------------------------------
# 5. convert 'dropoff_datetime' to Pandas datetime
#------------------------------------------------
# df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'])

#------------------------------------------------
# 6. Compute trip duration
#------------------------------------------------
#df['trip_duration'] = df['dropoff_datetime'] - df['pickup_datetime']

#------------------------------------------------
# 7. Compute trip duration in minutes
#------------------------------------------------
#df['trip_duration_minutes'] = df['trip_duration'].dt.total_seconds() / 60

#print("df=", df)
#for index, column_name in enumerate(df.columns):
#    print(index+1, column_name)
  
    
#--------------------------------
#
# 3. LOAD
#
# Load DataFrame into MySQL table
#
#---------------------------------

# get a database connection 
db_connection = get_db_connection()


#--------------
# Load to MySQL
#--------------
# 
# create db table named 'yellow_table'
db_table = "flights"

# write to database
write_to_database(df, db_table, db_connection)


"""

mysql> use test;

Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed

mysql> select count(*) from flights;

mysql> select * from flights limit 5;


"""
