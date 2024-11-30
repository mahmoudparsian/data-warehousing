import pandas as pd
"""
https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org

Make sure to do:
If you're using macOS go to 
Macintosh HD > Applications > Python3.6 folder 
(or whatever version of python you're using) 
> double click on "Install Certificates.command" file. :D

"""
parquet_file = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"
df = pd.read_parquet(parquet_file, engine='auto')
print("df=", df)

"""
data-warehousing (main *) % python3 read_parquet_from_url.py
df=          VendorID tpep_pickup_datetime tpep_dropoff_datetime  ...  total_amount  congestion_surcharge  airport_fee
0               2  2023-01-01 00:32:10   2023-01-01 00:40:36  ...         14.30                   2.5         0.00
1               2  2023-01-01 00:55:08   2023-01-01 01:01:27  ...         16.90                   2.5         0.00
2               2  2023-01-01 00:25:04   2023-01-01 00:37:49  ...         34.90                   2.5         0.00
3               1  2023-01-01 00:03:48   2023-01-01 00:13:25  ...         20.85                   0.0         1.25
4               2  2023-01-01 00:10:29   2023-01-01 00:21:19  ...         19.68                   2.5         0.00
...           ...                  ...                   ...  ...           ...                   ...          ...
3066761         2  2023-01-31 23:58:34   2023-02-01 00:12:33  ...         23.76                   NaN          NaN
3066762         2  2023-01-31 23:31:09   2023-01-31 23:50:36  ...         29.07                   NaN          NaN
3066763         2  2023-01-31 23:01:05   2023-01-31 23:25:36  ...         26.93                   NaN          NaN
3066764         2  2023-01-31 23:40:00   2023-01-31 23:53:00  ...         26.58                   NaN          NaN
3066765         2  2023-01-31 23:07:32   2023-01-31 23:21:56  ...         21.97                   NaN          NaN

[3066766 rows x 19 columns]

"""