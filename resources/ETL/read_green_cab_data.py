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
#      % python3 read_green_cab_data.py
#-----------------------------

import pandas as pd

"""
read a Parquet file and create a Python dataframe
"""

#------------------------------------
# define GREEN Trip data parquet file
#------------------------------------
# parquet URL : https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2023-01.parquet
parquet_file = "/tmp/green_tripdata_2023-01.parquet"

#------------------------------------------------
# 1. EXTRACT
#
# read parquet file and create a python dataframe
#------------------------------------------------
df = pd.read_parquet(parquet_file, engine='auto')
print("df=", df)


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

"""

