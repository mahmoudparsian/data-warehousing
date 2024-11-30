import sys
import urllib.request

#------------------------------
# Download the file from `url` and 
# save it locally under `file_name`:
#------------------------------
url = sys.argv[1]
print("url=", url)
#
file_name = sys.argv[2]
print("file_name=", file_name)
#
#urllib.request.urlretrieve(url, file_name)


with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
    data = response.read() # a `bytes` object
    out_file.write(data)

"""
Example:

% python3 download_url.py https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet yellow_tripdata_2023-01.parquet

"""