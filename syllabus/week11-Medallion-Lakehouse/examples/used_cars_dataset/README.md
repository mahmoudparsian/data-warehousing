# About Dataset

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

# Notebooks using DuckDB

```
1. provide a complete EDA (with proper MD documentation)
   for vehicles.csv data as a Jupyter Notebook

2. analyze vehicles.csv data file for bronze, silver, gold 
   architeture of data lakehouse, to understand these 3 layers 
   of architeture using DuckDB.

3. I want to be able to use DuckDB and get metadata 
   information form insurance.csv file

4. Create tables/views from 4 files with year dimension

5. Create Silver views/tables

6. Create Gold views/tables.

7. Create 10 insightful English/SQL queries, which has a true meaning
   in understanding this dataset.

8. Create a notebook with these 10 queries and write insight,
   SQL, and an associated graph/presentation for each query

9. Create a Data Story for this as MD/MARP downloadable file

10. Create an additional 6 questions for students.
    Provide solutions to instructor as MD/MARP
    
 

What makes it worth it (educational value)

	•	Bronze: demonstrates raw landing at 
	   scale (CSV + messy schema inference).
	   
	•	Silver: demonstrates why cleaning, 
	  typing, normalization, and feature 
	  engineering matters (posting_date 
	  parsing, price sanity, odometer sanity, 
	  standardizing categories, dropping unusable 
	  rows, trimming strings).
	  
	•	Gold: demonstrates business analytics 
	   outputs (market pricing trends, manufacturer 
	   comparisons, state/regional insights, 
	   year-of-car vs price, condition vs price, 
	   fuel/transmission patterns, outlier detection).
	•	Great for SQL patterns: WITH, window functions,
	   percentiles, ranking, cohorts by time, geo.  
	   bucketing.


Minimal but “real” lakehouse transformations
```
Bronze (raw view)

```
	•	read_csv_auto('vehicles.csv', ...) 
	  (don’t over-clean)
	•	metadata inspection: DESCRIBE, null counts, distinct counts
```

Silver (clean table)
```
	•	Parse posting_date to timestamp/date
	•	enforce types: price, odometer, year, lat, long
	•	standardize: lower/trim category columns
	•	quality filters:
	•	price BETWEEN 500 AND 200000 (example)
	•	odometer BETWEEN 0 AND 500000 (example)
	•	year BETWEEN 1950 AND current_year
	•	derived columns:
	•	posting_year, posting_month
	•	vehicle_age = posting_year - year
	•	price_per_mile (guarded)
	•	state_region or “market” segmentation
```

Gold (curated views/tables)

```
	•	KPIs: median price by state/manufacturer/month
	•	segment tables: top manufacturers by listings, average/median price trends, condition mix
	•	outlier tables: top 1% price listings by market, etc.
```
About your mixed requirements (vehicles + insurance)

```
You listed items 3–6 about insurance.csv and 4 
yearly files. That’s still worth keeping as a 
small “warm-up lakehouse”, then vehicles.csv 
becomes the capstone.
```



What’s inside this folder:

```
	•	Vehicles_EDA_DuckDB.ipynb
Complete DuckDB-first EDA with Markdown documentation + charts (aggregation-first so it doesn’t blow up memory).

	•	Vehicles_Lakehouse_Bronze_Silver_Gold_DuckDB.ipynb
Full Bronze → Silver → Gold pipeline in DuckDB + 10 meaningful insight queries, each with:
	•	English insight
	•	SQL
	•	automatic chart (when appropriate)
	•	Vehicles_Lakehouse_Data_Story.marp.md
A teaching-ready MD/MARP “data story” students can follow.

	•	Vehicles_SQL_Exercises_Student.marp.md
6 student questions (SQL exercises), MD/MARP.
	•	Vehicles_SQL_Exercises_Instructor.marp.md
Same 6 questions + full solutions, MD/MARP.

	•	vehicles_lakehouse_etl_diagram.png
A clean “professional” ETL diagram image (Bronze/Silver/Gold) you can drop into slides.

	•	Insurance_Mini_Lakehouse_Reference.ipynb
Small reference notebook for your earlier insurance work: metadata + yearly file Bronze/Silver/Gold (DuckDB).
```

How to run (important)

Place vehicles.csv next to the notebooks (or edit the path at the top of each notebook):

```
vehicles.csv
Vehicles_EDA_DuckDB.ipynb
Vehicles_Lakehouse_Bronze_Silver_Gold_DuckDB.ipynb
```

Then Run All. The notebooks are designed to keep pandas usage small (only aggregated results), so they remain laptop-friendly. ￼



1️⃣ Lakehouse notebook

Bronze:

```
Run:

Vehicles_Lakehouse_Bronze_Silver_Gold_DuckDB.ipynb

Check these steps in order:

Bronze

SELECT COUNT(*) FROM bronze_vehicles;

Expected: ~426k rows.
```

⸻

Silver:

```
SELECT COUNT(*) FROM silver_vehicles;

Expected: slightly fewer rows because of cleaning rules.
```

⸻

Gold:

```
SELECT * FROM gold_kpi_month LIMIT 10;

You should see something like:

month	listings	median_price
2021-01	…	…
2021-02	…	…
```

⸻

2️⃣ Check insight queries

The notebook includes 10 insight queries, for example:

	•	listing volume over time
	•	median price trends
	•	manufacturer distribution
	•	price vs vehicle age
	•	price vs odometer
	•	fuel distribution
	•	state comparisons
	•	outliers

Each query produces a chart automatically.

⸻

One thing you might notice (normal)

Craigslist data has a lot of bad listings:

Examples:

```
issue	example
price = 0	fake ads
price = 1	placeholder
year = 0	missing
year = 1900	invalid
odometer = 0	unknown
```

The Silver layer already filters most of these, 
but you may still see some outliers.

This is actually excellent for teaching data cleaning.

⸻

Teaching tip (this dataset works extremely well for it)

You can ask students:

Why does the median price differ so much from the average price?

Because the distribution is extremely skewed.

That naturally leads to:

```
median()
percentiles()
robust statistics
```

which is exactly what a Gold layer should use.

⸻

What this means (the insight)

1️⃣ April dominates the dataset

Most listings occurred in April 2021:

```
April listings ≈ 284k
May listings   ≈ 97k
```

This happens because the dataset snapshot was collected around April–May 2021, so April is the main crawl month.

For teaching, this is a good discussion point:

Data collection processes influence observed distributions.

⸻

2️⃣ Median vs Average price difference

Example for April:

```
Median price = $16,300
Average price = $19,797
```

Average is higher because the distribution contains expensive outliers (luxury cars).

This is why Gold layer uses MEDIAN and percentiles, not only averages.

Great teaching moment:

```
mean ≠ robust statistic
median = better for skewed distributions
```

⸻

3️⃣ P90 price interpretation

P90 April = $38,990

Meaning:

90% of vehicles cost below $38,990

Top 10% are luxury / newer vehicles.

⸻

4️⃣ Interesting observation

Median dropped in May:

April median = $16,300
May median   = $13,995

Possible explanations:

```
• More older / cheaper vehicles posted
• Regional mix changed
• Sampling bias due to scraping window
```

This becomes a great classroom question.

⸻

Recommended additional Gold KPI (very useful)

Add vehicle age trends, which students love:

```
CREATE VIEW gold_price_by_age AS
SELECT
    vehicle_age,
    COUNT(*) AS listings,
    MEDIAN(price) AS median_price
FROM silver_vehicles
WHERE vehicle_age BETWEEN 0 AND 30
GROUP BY vehicle_age
HAVING COUNT(*) > 100
ORDER BY vehicle_age;
```

Then plot:

```
df = con.execute("SELECT * FROM gold_price_by_age").df()

plt.figure()
plt.plot(df["vehicle_age"], df["median_price"])
plt.title("Vehicle price vs age")
plt.xlabel("vehicle age")
plt.ylabel("median price")
plt.show()
```

Students immediately see the depreciation curve.

⸻

The lakehouse pipeline is now working

We now have a realistic teaching pipeline:

```
vehicles.csv (426k rows)
        ↓
Bronze
(raw ingestion)

        ↓
Silver
(cleaning + feature engineering)

        ↓
Gold
(KPI tables + insights)

And you already demonstrated:

✔ schema inference
✔ data cleaning
✔ feature engineering
✔ robust statistics
✔ analytical SQL

That’s exactly what a lakehouse course should show.
```

⸻


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

These map exactly to the Gold queries you already built.

