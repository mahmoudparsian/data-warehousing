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
#      % python3 read_yellow_cab_data.py
#-----------------------------

import pandas as pd

"""
read a Parquet file and create a Python dataframe
"""

#------------------------------------
# define YELLOW Trip data parquet file
#------------------------------------
# parquet URL : https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet
parquet_file = "/tmp/yellow_tripdata_2023-01.parquet"

#------------------------------------------------
# 1. EXTRACT
#
# read parquet file and create a python dataframe
#------------------------------------------------
df = pd.read_parquet(parquet_file, engine='auto')
print("df=", df)


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
"""

