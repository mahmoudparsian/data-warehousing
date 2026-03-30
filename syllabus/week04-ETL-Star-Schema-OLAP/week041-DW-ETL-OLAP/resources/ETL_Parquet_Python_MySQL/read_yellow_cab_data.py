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



#------------------------------------
# define YELLOW Trip data parquet file
#
# Yellow trips data dictionary:
# https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
#------------------------------------
# parquet URL : https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet
# parquet_file = "/Users/mparsian/Downloads/new_york_taxi_cab/yellow_tripdata_2023-01.parquet"
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
#
print("column names are:\n")
for index, column_name in enumerate(df.columns):
    print(index+1, column_name)
#
#

"""
df=          VendorID tpep_pickup_datetime tpep_dropoff_datetime  passenger_count  ...  improvement_surcharge  total_amount congestion_surcharge  airport_fee
0               2  2023-01-01 00:32:10   2023-01-01 00:40:36              1.0  ...                    1.0         14.30                  2.5         0.00
1               2  2023-01-01 00:55:08   2023-01-01 01:01:27              1.0  ...                    1.0         16.90                  2.5         0.00
2               2  2023-01-01 00:25:04   2023-01-01 00:37:49              1.0  ...                    1.0         34.90                  2.5         0.00
3               1  2023-01-01 00:03:48   2023-01-01 00:13:25              0.0  ...                    1.0         20.85                  0.0         1.25
4               2  2023-01-01 00:10:29   2023-01-01 00:21:19              1.0  ...                    1.0         19.68                  2.5         0.00
...           ...                  ...                   ...              ...  ...                    ...           ...                  ...          ...
3066761         2  2023-01-31 23:58:34   2023-02-01 00:12:33              NaN  ...                    1.0         23.76                  NaN          NaN
3066762         2  2023-01-31 23:31:09   2023-01-31 23:50:36              NaN  ...                    1.0         29.07                  NaN          NaN
3066763         2  2023-01-31 23:01:05   2023-01-31 23:25:36              NaN  ...                    1.0         26.93                  NaN          NaN
3066764         2  2023-01-31 23:40:00   2023-01-31 23:53:00              NaN  ...                    1.0         26.58                  NaN          NaN
3066765         2  2023-01-31 23:07:32   2023-01-31 23:21:56              NaN  ...                    1.0         21.97                  NaN          NaN

[3,066,766 rows x 19 columns]

column names are:

1 VendorID
2 tpep_pickup_datetime
3 tpep_dropoff_datetime
4 passenger_count
5 trip_distance
6 RatecodeID
7 store_and_fwd_flag
8 PULocationID
9 DOLocationID
10 payment_type
11 fare_amount
12 extra
13 mta_tax
14 tip_amount
15 tolls_amount
16 improvement_surcharge
17 total_amount
18 congestion_surcharge
19 airport_fee

==========================================================
Meta Data Descriptions
==========================================================
1. VendorID                A code indicating the TPEP provider 
                           that provided the record.
                           1= Creative Mobile Technologies, LLC; 
                           2= VeriFone Inc.
               
2. tpep_pickup_datetime    The date and time when the meter was engaged.

3. tpep_dropoff_datetime   The date and time when the meter was disengaged

4. passenger_count         The number of passengers in the vehicle.
                           This is a driver-entered value
                           
5. trip_distance           The elapsed trip distance in miles 
                           reported by the taximeter.
                           
6. RatecodeID              The final rate code in effect at the end of the trip.
                           1= Standard rate
                           2=JFK
                           3=Newark
                           4=Nassau or Westchester
                           5=Negotiated fare
                           6=Group ride
                           
7. store_and_fwd_flag      This flag indicates whether the trip record 
                           was held in vehicle memory before sending to 
                           the vendor, aka “store and forward,” because 
                           the vehicle did not have a connection to the server.
                           Y= store and forward trip
                           N= not a store and forward trip
                           
8. PULocationID            TLC Taxi Zone in which the taximeter was engaged


9. DOLocationID            TLC Taxi Zone in which the taximeter was disengaged

10. payment_type           A numeric code signifying how the passenger 
                           paid for the trip.
                           1= Credit card
                           2= Cash
                           3= No charge
                           4= Dispute
                           5= Unknown
                           6= Voided trip

11. fare_amount            The time-and-distance fare calculated by the meter

12. extra                  Miscellaneous extras and surcharges. 
                           Currently, this only includes the $0.50 
                           and $1 rush hour and overnight charges.

13. mta_tax                $0.50 MTA tax that is automatically triggered 
                           based on the metered rate in use.

14. tip_amount             -- Tip amount – This field is automatically  
                           populated for credit card tips. 
                           -- Cash tips are not included.

15. tolls_amount           Total amount of all tolls paid in trip. 

16. improvement_surcharge  $0.30 improvement surcharge assessed  
                           trips at the flag drop. The improvement  
                           surcharge began being levied in 2015.

17. total_amount           -- The total amount charged to passengers. 
                           -- Does not include cash tips.

18. congestion_surcharge   Total amount collected in trip for NYS 
                           congestion surcharge

19. airport_fee            $1.25 for pick up only at LaGuardia  
                           and John F. Kennedy Airports


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

#### number_of_rows_dropped= 71,743

#------------------------------------------------------------
# 2. rename 'tpep_pickup_datetime' to 'pickup_datetime'
#------------------------------------------------------------
df = df.rename(columns={'tpep_pickup_datetime': 'pickup_datetime'})

#------------------------------------------------------------
# 3. rename 'tpep_dropoff_datetime': 'dropoff_datetime'
#------------------------------------------------------------
df = df.rename(columns={'tpep_dropoff_datetime': 'dropoff_datetime'})
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


#--------------
# Load to MySQL
#--------------
# 
# create db table named 'yellow_table'
db_table = "yellow_table"

# write to database
write_to_database(df, db_table, db_connection)


"""

mysql> use test;

Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed

mysql> select count(*) from yellow_table;
+----------+
| count(*) |
+----------+
|  2995023 |
+----------+
1 row in set (0.34 sec)

mysql> select * from yellow_table limit 5;
+----------+---------------------+---------------------+-----------------+---------------+------------+--------------------+--------------+--------------+--------------+-------------+-------+---------+------------+--------------+-----------------------+--------------+----------------------+-------------+---------------+-----------------------+
| VendorID | pickup_datetime     | dropoff_datetime    | passenger_count | trip_distance | RatecodeID | store_and_fwd_flag | PULocationID | DOLocationID | payment_type | fare_amount | extra | mta_tax | tip_amount | tolls_amount | improvement_surcharge | total_amount | congestion_surcharge | airport_fee | trip_duration | trip_duration_minutes |
+----------+---------------------+---------------------+-----------------+---------------+------------+--------------------+--------------+--------------+--------------+-------------+-------+---------+------------+--------------+-----------------------+--------------+----------------------+-------------+---------------+-----------------------+
|        2 | 2023-01-01 00:32:10 | 2023-01-01 00:40:36 |               1 |          0.97 |          1 | N                  |          161 |          141 |            2 |         9.3 |     1 |     0.5 |          0 |            0 |                     1 |         14.3 |                  2.5 |           0 |     506000000 |     8.433333333333334 |
|        2 | 2023-01-01 00:55:08 | 2023-01-01 01:01:27 |               1 |           1.1 |          1 | N                  |           43 |          237 |            1 |         7.9 |     1 |     0.5 |          4 |            0 |                     1 |         16.9 |                  2.5 |           0 |     379000000 |     6.316666666666666 |
|        2 | 2023-01-01 00:25:04 | 2023-01-01 00:37:49 |               1 |          2.51 |          1 | N                  |           48 |          238 |            1 |        14.9 |     1 |     0.5 |         15 |            0 |                     1 |         34.9 |                  2.5 |           0 |     765000000 |                 12.75 |
|        1 | 2023-01-01 00:03:48 | 2023-01-01 00:13:25 |               0 |           1.9 |          1 | N                  |          138 |            7 |            1 |        12.1 |  7.25 |     0.5 |          0 |            0 |                     1 |        20.85 |                    0 |        1.25 |     577000000 |     9.616666666666667 |
|        2 | 2023-01-01 00:10:29 | 2023-01-01 00:21:19 |               1 |          1.43 |          1 | N                  |          107 |           79 |            1 |        11.4 |     1 |     0.5 |       3.28 |            0 |                     1 |        19.68 |                  2.5 |           0 |     650000000 |    10.833333333333334 |
+----------+---------------------+---------------------+-----------------+---------------+------------+--------------------+--------------+--------------+--------------+-------------+-------+---------+------------+--------------+-----------------------+--------------+----------------------+-------------+---------------+-----------------------+
5 rows in set (0.01 sec)

"""
