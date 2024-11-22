#-----------------------------
# ETL example
#              1. Extract
#              2. Transform
#              3. Load
#-----------------------------
# Metadata for Green Cab:
# https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_green.pdf
#-----------------------------
#  INSTALL these required libraries:
#
#     pip install flask_sqlalchemy
#     pip install pymysql
#     pip install pandas
#-----------------------------

#-----------------------------
# running this program: 
#      % python3 read_green_cab_data.py
#-----------------------------

# import required library
from sqlalchemy import create_engine

import pandas as pd
import sys


#----------------------------------------
def get_db_connection():

    # Connect String format:
    # mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]

    db_user = "root"
    db_password = "myrootpassword"
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


"""
read a Parquet file and create a Python dataframe
"""

#------------------------------------
# define GREEN Trip data parquet file
#------------------------------------
# parquet URL : https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2023-01.parquet
# parquet_file = "/Users/mparsian/Downloads/new_york_taxi_cab/green_tripdata_2023-01.parquet"

parquet_file = sys.argv[1]
print("parquet_file=", parquet_file)

#------------------------------------------------
# 1. EXTRACT
#
# read parquet file and create a python dataframe
#------------------------------------------------
df = pd.read_parquet(parquet_file, engine='auto')
print("df=", df)
#
print("column names are:\n")
for index, column_name in enumerate(df.columns):
    print(index+1, column_name)
#
#

"""
df=        VendorID lpep_pickup_datetime lpep_dropoff_datetime store_and_fwd_flag  ...  total_amount  payment_type  trip_type  congestion_surcharge
0             2  2023-01-01 00:26:10   2023-01-01 00:37:11                  N  ...         24.18           1.0        1.0                  2.75
1             2  2023-01-01 00:51:03   2023-01-01 00:57:49                  N  ...         15.84           1.0        1.0                  0.00
2             2  2023-01-01 00:35:12   2023-01-01 00:41:32                  N  ...         11.64           1.0        1.0                  0.00
3             1  2023-01-01 00:13:14   2023-01-01 00:19:03                  N  ...         10.20           1.0        1.0                  0.00
4             1  2023-01-01 00:33:04   2023-01-01 00:39:02                  N  ...          8.00           1.0        1.0                  0.00
...         ...                  ...                   ...                ...  ...           ...           ...        ...                   ...
68206         2  2023-01-31 22:29:00   2023-01-31 22:42:00               None  ...         16.70           NaN        NaN                   NaN
68207         2  2023-01-31 22:40:00   2023-01-31 22:48:00               None  ...          5.41           NaN        NaN                   NaN
68208         2  2023-01-31 23:46:00   2023-02-01 00:02:00               None  ...         21.04           NaN        NaN                   NaN
68209         2  2023-01-31 23:01:00   2023-01-31 23:19:00               None  ...         19.18           NaN        NaN                   NaN
68210         2  2023-01-31 23:51:00   2023-02-01 00:07:00               None  ...         29.40           NaN        NaN                   NaN

[68,211 rows x 20 columns]
column names are:

1 VendorID
2 lpep_pickup_datetime
3 lpep_dropoff_datetime
4 store_and_fwd_flag
5 RatecodeID
6 PULocationID
7 DOLocationID
8 passenger_count
9 trip_distance
10 fare_amount
11 extra
12 mta_tax
13 tip_amount
14 tolls_amount
15 ehail_fee
16 improvement_surcharge
17 total_amount
18 payment_type
19 trip_type
20 congestion_surcharge

==========================================================
Meta Data Descriptions
==========================================================
1 VendorID                A code indicating the LPEP provider 
                          that provided the record.
                          1= Creative Mobile Technologies, LLC; 
                          2= VeriFone Inc.

2 lpep_pickup_datetime    The date and time when the meter was engaged. 

3 lpep_dropoff_datetime   The date and time when the meter was disengaged. 

4 store_and_fwd_flag      This flag indicates whether the trip record was 
                          held in vehicle memory before sending to the vendor, 
                          aka “store and forward,”  because the vehicle did 
                          not have a connection to the server.
                          Y= store and forward trip
                          N= not a store and forward trip

5 RatecodeID              The final rate code in effect at the end of the trip.
                          1= Standard rate
                          2=JFK
                          3=Newark
                          4=Nassau or Westchester
                          5=Negotiated fare
                          6=Group ride

6 PULocationID            TLC Taxi Zone in which the taximeter was engaged

7 DOLocationID            TLC Taxi Zone in which the taximeter was disengaged

8 passenger_count         -- The number of passengers in the vehicle.
                          -- This is a driver-entered value.

9 trip_distance           The elapsed trip distance in miles reported by the taximeter

10 fare_amount            The time-and-distance fare calculated by the meter.

11 extra                  Miscellaneous extras and surcharges. Currently, 
                          this only includes the $0.50 and $1 rush hour 
                          and overnight charges

12 mta_tax                $0.50 MTA tax that is automatically triggered 
                          based on the metered rate in use.

13 tip_amount             Tip amount – This field is automatically populated 
                          for credit card tips. Cash tips are not included.

14 tolls_amount           Total amount of all tolls paid in trip

15 ehail_fee              NOT-DOCUMENTED

16 improvement_surcharge  $0.30 improvement surcharge assessed on hailed 
                          trips at the flag drop. The improvement surcharge 
                          began being levied in 2015

17 total_amount           The total amount charged to passengers. 
                          Does not include cash tips.

18 payment_type           A numeric code signifying how the passenger paid for the trip.
                          1= Credit card
                          2= Cash
                          3= No charge
                          4= Dispute
                          5= Unknown
                          6= Voided trip

19 trip_type              A code indicating whether the trip was a 
                          street-hail or a dispatch that is automatically 
                          assigned based on the metered rate in use but
                          can be altered by the driver.
                          1= Street-hail
                          2= Dispatch

20 congestion_surcharge   NOT-DOCUMENTED


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
# df = df.dropna()  # Remove rows with missing data
# number_of_rows_dropped = number_of_rows - len(df.index) 
print("df=", df)
#print("number_of_rows_dropped=", number_of_rows_dropped)

#### number_of_rows_dropped= 68,211

####
#### =>> DO NOT DROP rows with NULL values
####

#------------------------------------------------------------
# 2. rename 'lpep_pickup_datetime' to 'pickup_datetime'
#------------------------------------------------------------
df = df.rename(columns={'lpep_pickup_datetime': 'pickup_datetime'})

#------------------------------------------------------------
# 3. rename 'lpep_dropoff_datetime': 'dropoff_datetime'
#------------------------------------------------------------
df = df.rename(columns={'lpep_dropoff_datetime': 'dropoff_datetime'})

print("after columns are renamed=", df)
print("new column names are:\n")
for index, column_name in enumerate(df.columns):
    print(index+1, column_name)
    
#------------------------------------------------
# 4. convert 'pickup_datetime' to Pandas datetime
#------------------------------------------------
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])

#------------------------------------------------
# 5. convert 'dropoff_datetime' to Pandas datetime
#------------------------------------------------
df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'])

#------------------------------------------------
# 6. Compute trip duration
#------------------------------------------------
df['trip_duration'] = df['dropoff_datetime'] - df['pickup_datetime']

#------------------------------------------------
# 7. Compute trip duration in minutes
#------------------------------------------------
df['trip_duration_minutes'] = df['trip_duration'].dt.total_seconds() / 60

print("df=", df)
for index, column_name in enumerate(df.columns):
    print(index+1, column_name)
    

#--------------------------------
#
# 3. LOAD
#
# Load DataFrame into MySQL table
#
#---------------------------------

# get a database connection 
db_connection = get_db_connection()


#---------------
# Load to MySQL
#---------------
# 
# create db table named 'green_table'
db_table = "green_table"

# write to database
write_to_database(df, db_table, db_connection)


"""
mysql>
mysql> use test;
Database changed
mysql>

mysql> select count(*) from green_table;
+----------+
| count(*) |
+----------+
|    68211 |
+----------+
1 row in set (0.01 sec)

mysql>
mysql> select * from green_table limit 5;
+----------+---------------------+---------------------+--------------------+------------+--------------+--------------+-----------------+---------------+-------------+-------+---------+------------+--------------+-----------+-----------------------+--------------+--------------+-----------+----------------------+---------------+-----------------------+
| VendorID | pickup_datetime     | dropoff_datetime    | store_and_fwd_flag | RatecodeID | PULocationID | DOLocationID | passenger_count | trip_distance | fare_amount | extra | mta_tax | tip_amount | tolls_amount | ehail_fee | improvement_surcharge | total_amount | payment_type | trip_type | congestion_surcharge | trip_duration | trip_duration_minutes |
+----------+---------------------+---------------------+--------------------+------------+--------------+--------------+-----------------+---------------+-------------+-------+---------+------------+--------------+-----------+-----------------------+--------------+--------------+-----------+----------------------+---------------+-----------------------+
|        2 | 2023-01-01 00:26:10 | 2023-01-01 00:37:11 | N                  |          1 |          166 |          143 |               1 |          2.58 |        14.9 |     1 |     0.5 |       4.03 |            0 | NULL      |                     1 |        24.18 |            1 |         1 |                 2.75 |     661000000 |    11.016666666666667 |
|        2 | 2023-01-01 00:51:03 | 2023-01-01 00:57:49 | N                  |          1 |           24 |           43 |               1 |          1.81 |        10.7 |     1 |     0.5 |       2.64 |            0 | NULL      |                     1 |        15.84 |            1 |         1 |                    0 |     406000000 |     6.766666666666667 |
|        2 | 2023-01-01 00:35:12 | 2023-01-01 00:41:32 | N                  |          1 |          223 |          179 |               1 |             0 |         7.2 |     1 |     0.5 |       1.94 |            0 | NULL      |                     1 |        11.64 |            1 |         1 |                    0 |     380000000 |     6.333333333333333 |
|        1 | 2023-01-01 00:13:14 | 2023-01-01 00:19:03 | N                  |          1 |           41 |          238 |               1 |           1.3 |         6.5 |   0.5 |     1.5 |        1.7 |            0 | NULL      |                     1 |         10.2 |            1 |         1 |                    0 |     349000000 |     5.816666666666666 |
|        1 | 2023-01-01 00:33:04 | 2023-01-01 00:39:02 | N                  |          1 |           41 |           74 |               1 |           1.1 |           6 |   0.5 |     1.5 |          0 |            0 | NULL      |                     1 |            8 |            1 |         1 |                    0 |     358000000 |     5.966666666666667 |
+----------+---------------------+---------------------+--------------------+------------+--------------+--------------+-----------------+---------------+-------------+-------+---------+------------+--------------+-----------+-----------------------+--------------+--------------+-----------+----------------------+---------------+-----------------------+
5 rows in set (0.00 sec)

mysql>

"""
