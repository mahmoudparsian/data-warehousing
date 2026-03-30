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
#      % python3 read_csv_file.py
#-----------------------------

import pandas as pd

"""
read a Parquet file and create a Python dataframe
"""

#------------------------------------
# define CSV file
#------------------------------------
csv_file = "/tmp/newyork_taxi_cab/taxi_zone_lookup.csv"

#------------------------------------------------
# 1. EXTRACT
#
# read csv file and create a python dataframe
#------------------------------------------------
df = pd.read_csv(csv_file)
print("df=", df)


"""
df=      LocationID        Borough                     Zone service_zone
0             1            EWR           Newark Airport          EWR
1             2         Queens              Jamaica Bay    Boro Zone
2             3          Bronx  Allerton/Pelham Gardens    Boro Zone
3             4      Manhattan            Alphabet City  Yellow Zone
4             5  Staten Island            Arden Heights    Boro Zone
..          ...            ...                      ...          ...
260         261      Manhattan       World Trade Center  Yellow Zone
261         262      Manhattan           Yorkville East  Yellow Zone
262         263      Manhattan           Yorkville West  Yellow Zone
263         264        Unknown                       NV          NaN
264         265        Unknown                      NaN          NaN

[265 rows x 4 columns]
"""

