# Using Python and MySQL

## How to Use `pymysql`

* [How to use pymysql - 10 common examples](https://snyk.io/advisor/python/pymysql/example)

* How to Install `pymysql`

	% python3 -m pip install pymysql

* Sample program to read Parquet and Load to MySQL

~~~python
>>># Python 3.11.4

>>> import pyarrow.parquet as pq

>>> parquet_file = '/tmp/yellow_tripdata_2022-01.parquet'
>>> trips = pq.read_table(parquet_file)
>>> trips
pyarrow.Table
VendorID: int64
tpep_pickup_datetime: timestamp[us]
tpep_dropoff_datetime: timestamp[us]
passenger_count: double
trip_distance: double
RatecodeID: double
store_and_fwd_flag: string
PULocationID: int64
DOLocationID: int64
payment_type: int64
fare_amount: double
extra: double
mta_tax: double
tip_amount: double
tolls_amount: double
improvement_surcharge: double
total_amount: double
congestion_surcharge: double
airport_fee: double


>>> trips_df = trips.to_pandas()
>>> trips_df
         VendorID tpep_pickup_datetime tpep_dropoff_datetime  ...  total_amount  congestion_surcharge  airport_fee
0               1  2022-01-01 00:35:40   2022-01-01 00:53:29  ...         21.95                   2.5          0.0
1               1  2022-01-01 00:33:43   2022-01-01 00:42:07  ...         13.30                   0.0          0.0
2               2  2022-01-01 00:53:21   2022-01-01 01:02:19  ...         10.56                   0.0          0.0
3               2  2022-01-01 00:25:21   2022-01-01 00:35:23  ...         11.80                   2.5          0.0
4               2  2022-01-01 00:36:48   2022-01-01 01:14:20  ...         30.30                   2.5          0.0
...           ...                  ...                   ...  ...           ...                   ...          ...
2463926         2  2022-01-31 23:36:53   2022-01-31 23:42:51  ...         13.69                   NaN          NaN
2463927         2  2022-01-31 23:44:22   2022-01-31 23:55:01  ...         24.45                   NaN          NaN
2463928         2  2022-01-31 23:39:00   2022-01-31 23:50:00  ...         16.52                   NaN          NaN
2463929         2  2022-01-31 23:36:42   2022-01-31 23:48:45  ...         15.70                   NaN          NaN
2463930         2  2022-01-31 23:46:00   2022-02-01 00:13:00  ...         35.06                   NaN          NaN

>>> # Connect String:
>>> # mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]

>>> db_user = "root"
>>> db_password = "myrootpassword"
>>> db_table = "test"

>>> connection_string = "mysql+pymysql://%s:%s@%s:%s/%s" % (db_user, db_password, 'localhost', '3306', db_table)
>>> connection_string
'mysql+pymysql://root:myrootpassword@localhost:3306/test'

>>> from sqlalchemy import create_engine
>>> engine = create_engine(connection_string)
>>> engine
Engine(mysql+pymysql://root:***@localhost:3306/test)

>>> # create table named 'my_table'
>>> trips_df.to_sql(name = 'my_table', con = engine, if_exists = 'append', index = False)

2,463,931
>>>
~~~

* Check MySQL Table

~~~SQL
select count(*) from my_table;
2,463,931
~~~