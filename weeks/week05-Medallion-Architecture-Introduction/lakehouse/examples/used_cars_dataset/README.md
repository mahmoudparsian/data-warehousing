# About Dataset

## ⬇️ Download the data first

`vehicles.csv` (1.4 GB) is too large for GitHub, so it is **not in this repo**.
Download the zip (273 MB) and unzip it into this folder:

* https://mapreduce4hackers.com/data/vehicles.zip

```
cd used_cars_dataset
curl -O https://mapreduce4hackers.com/data/vehicles.zip
unzip vehicles.zip        # creates vehicles.csv
```

Just want to peek at the columns? See `vehicles.csv.head` (first rows, already in the repo).

## source of data

`https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data`

## Context

Craigslist is the world's largest collection of used 
vehicles for sale, yet it's very difficult to collect 
all of them in the same place. I built a scraper for 
a school project and expanded upon it later to create 
this dataset which includes every used vehicle entry 
within the United States on Craigslist.

## Content

This data is scraped every few months, it contains 
most all relevant information that Craigslist provides 
on car sales including columns like price, condition, 
manufacturer, latitude/longitude, and 18 other categories. 
For ML projects, consider feature engineering on location 
columns such as long/lat. For previous listings, check older 
versions of the dataset.

## Data file Specification:

```
Name: vehicles.csv

used_cars_dataset  % ls -l vehicles.csv
-rw-r--r--@ 1 max  staff  1447955215 May  6  2021 vehicles.csv

used_cars_dataset  % wc -l vehicles.csv
  426881 vehicles.csv
  
used_cars_dataset  % head vehicles.csv
id,url,region,region_url,price,year,manufacturer,model,condition,cylinders,fuel,odometer,title_status,transmission,VIN,drive,size,type,paint_color,image_url,description,county,state,lat,long,posting_date
7222695916,https://prescott.craigslist.org/cto/d/prescott-2010-ford-ranger/7222695916.html,prescott,https://prescott.craigslist.org,6000,,,,,,,,,,,,,,,,,,az,,,
7218891961,https://fayar.craigslist.org/ctd/d/bentonville-2017-hyundai-elantra-se/7218891961.html,fayetteville,https://fayar.craigslist.org,11900,,,,,,,,,,,,,,,,,,ar,,,
7221797935,https://keys.craigslist.org/cto/d/summerland-key-2005-excursion/7221797935.html,florida keys,https://keys.craigslist.org,21000,,,,,,,,,,,,,,,,,,fl,,,
7222270760,https://worcester.craigslist.org/cto/d/west-brookfield-2002-honda-odyssey-ex/7222270760.html,worcester / central MA,https://worcester.craigslist.org,1500,,,,,,,,,,,,,,,,,,ma,,,
7210384030,https://greensboro.craigslist.org/cto/d/trinity-1965-chevrolet-truck/7210384030.html,greensboro,https://greensboro.craigslist.org,4900,,,,,,,,,,,,,,,,,,nc,,,
7222379453,https://hudsonvalley.craigslist.org/cto/d/westtown-2007-ford-150/7222379453.html,hudson valley,https://hudsonvalley.craigslist.org,1600,,,,,,,,,,,,,,,,,,ny,,,
7221952215,https://hudsonvalley.craigslist.org/cto/d/westtown-silverado-2000/7221952215.html,hudson valley,https://hudsonvalley.craigslist.org,1000,,,,,,,,,,,,,,,,,,ny,,,
7220195662,https://hudsonvalley.craigslist.org/cto/d/poughquag-2015-acura-rdx-warranty/7220195662.html,hudson valley,https://hudsonvalley.craigslist.org,15995,,,,,,,,,,,,,,,,,,ny,,,
7209064557,https://medford.craigslist.org/cto/d/grants-pass-two-2002-bmw-tii/7209064557.html,medford-ashland,https://medford.craigslist.org,5000,,,,,,,,,,,,,,,,,,or,,,
```

# Files

| File | What it is |
|---|---|
| `Vehicles_EDA_DuckDB.py` | Exploratory analysis of 426,880 listings with DuckDB (aggregate first, so it runs on a laptop) |
| `Vehicles_Lakehouse_Bronze_Silver_Gold_DuckDB.py` | Full Bronze → Silver → Gold pipeline + 10 insight queries with charts |
| [`Vehicles_Lakehouse_Data_Story.marp.md`](Vehicles_Lakehouse_Data_Story.marp.md) | The data story as slides (Marp) |
| [`Vehicles_SQL_Exercises_Student.marp.md`](Vehicles_SQL_Exercises_Student.marp.md) | 6 SQL exercises (practice) |
| `vehicles_lakehouse_duckdb_bundle.zip` | The notebooks + story bundled |
| `vehicles.csv.head` | First rows of the data (for a quick look before downloading) |

Both notebooks need `vehicles.csv` in this folder (see **Download** above). The used-cars data is the
"big" lakehouse capstone; [`../insurance_4_years/`](../insurance_4_years/) is the small warm-up.

# 10 Real Business Questions Answered by the Dataset

```
Example:

1️⃣ What brands dominate Craigslist listings?
2️⃣ How does price change with vehicle age?
3️⃣ What states have the most listings?
4️⃣ Are automatic cars more expensive than manual?
5️⃣ How does mileage affect price?
6️⃣ Which manufacturers keep value longer?
7️⃣ What fuel types dominate the market?
8️⃣ Are SUVs priced higher than sedans?
9️⃣ Which states have the highest vehicle prices?
🔟 What are the top luxury outliers?
```

The Gold layer in `Vehicles_Lakehouse_Bronze_Silver_Gold_DuckDB.py` answers these.
