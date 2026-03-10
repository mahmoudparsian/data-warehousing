# About Dataset

## source of data

https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data

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


# Some additional 4 rows of data from the CSV file: vehicles.csv

7310292522,https://pittsburgh.craigslist.org/ctd/d/oliver-2009-nissan-rogue-awd/7310292522.html,pittsburgh,https://pittsburgh.craigslist.org,4999,2009,nissan,rogue,good,4 cylinders,gas,193193,clean,automatic,JN8AS58V19W448032,4wd,full-size,SUV,black,https://images.craigslist.org/01111_2biWphHqfdtz_0cU09G_600x450.jpg,"2009 Nissan Rogue S AWDPrice:  $4,999  Year: 2009 Make:Nissan Model:Rogue Trim:S AWD Mileage:193,193 Stock #:4895 VIN:JN8AS58V19W448032 Trans:Automatic Color:Black Vehicle Type:SUV State:PA Drive Train:AWD Engine:2.5L L4 DOHC 16VVehicle Disclaimer:DOWN PAYMENT / ADVERTISED PRICE / RETAIL PRICE IN THIS AD DOES NOT INCLUDE TAX, TITLE, PLATES AND DEALER FEES.  THESE WILL BE AN ADDITIONAL COST.  THE FEES WILL VARY WHETHER YOU DO FINANCING, BUY HERE PAY HERE OR CASH.  IT WILL ALSO DEPEND ON WHERE YOU LIVE.  PLEASE CALL US AT 724-437-5274 FOR MORE DETAILS.  HOME OF THE 100% GUARANTEED CREDIT APPROVAL!  EVERYBODY GETS APPROVED!  THE DOWN PRICES ON THIS LISTING MAY VARY DEPENDING ON A PERSONS CREDIT OR INCOME VERIFICATION.  LBSI AUTOMOTIVE IS NOT RESPONSIBLE FOR TYPOGRAPHICAL ERRORS.  PUBLISHED PRICE SUBJECT TO CHANGE WITHOUT NOTICE. ALL FEATURES AND EQUIPMENT LISTED MAY NOT BE ON VEHICLE. PLEASE VERIFY ACTUAL OPTIONS WITH INTERNET DEPARTMENT BY EMAIL OR PHONE.  IF YOU ARE COMING TO OUR OFFICE AND PLAN ON PURCHASING A VEHICLE PLEASE BE HERE TWO HOURS PRIOR TO CLOSING.  PLEASE SEE OUR WEBSITE FOR HOURS AND TIMES AS THEY MAY CHANGE.  WE DO NOT STAY OPEN AFTER HOURS AND CAN NOT GET YOUR CAR TITLED AFTER HOURS.  WE DO TAKE CASH IN PERSON, VISA AND MASTER CARD ONLY FOR A CERTAIN AMOUNT (PLEASE CALL FIRST) CREDIT CARDS WILL ONLY BE ACCEPTED WITH A VALID DRIVERS LICENSE AVAILABLE WITH THE SAME INFORMATION ON IT AS THE CUSTOMER MAKING THE PURCHASE.  WE LOOK FORWARD TO SEEING YOU SOON.  Vehicle Options 4WD/AWDABS BrakesAir ConditioningAM/FM RadioCargo Area TiedownsCD PlayerChild Safety Door LocksCruise ControlDriver AirbagElectronic Brake AssistanceFront Air DamFront Side AirbagInterval WipersKeyless EntryPassenger AirbagPower Adjustable Exterior MirrorPower Door LocksPower WindowsRear Window DefoggerRear WiperSecond Row Folding SeatSide Head Curtain AirbagSteel WheelsSteering Wheel Mounted ControlsTachometerTilt SteeringTilt Steering ColumnTire Pressure MonitorTraction ControlVehicle Anti-TheftVehicle Stability Control System  LBSI Automotive LLC Jim Antolik 109 Pittsburgh St. Uniontown PA 15401 724-437-5274BatchID: 4VOY35IBQWID: 17446040 Updated 5/2/2021 9:08:04 PM EST",,pa,39.905181,-79.727095,2021-04-21T10:02:30-0400
7310292528,https://pittsburgh.craigslist.org/ctd/d/oliver-2008-pontiac-g6-1sv-sedan/7310292528.html,pittsburgh,https://pittsburgh.craigslist.org,2499,2008,pontiac,g6,good,4 cylinders,gas,198641,clean,automatic,1G2ZF57B984247276,fwd,,sedan,red,https://images.craigslist.org/00q0q_1MTlyWLpwawz_0cU09G_600x450.jpg,"2008 Pontiac G6 1SV SedanPrice:  $2,499  Year: 2008 Make:Pontiac Model:G6 Trim:1SV Sedan Mileage:198,641 Stock #:4896 VIN:1G2ZF57B984247276 Trans:Automatic Color:Red Vehicle Type:Sedan State:PA Drive Train:FWD Engine:2.4L L4 DOHC 16VVehicle Disclaimer:DOWN PAYMENT / ADVERTISED PRICE / RETAIL PRICE IN THIS AD DOES NOT INCLUDE TAX, TITLE, PLATES AND DEALER FEES.  THESE WILL BE AN ADDITIONAL COST.  THE FEES WILL VARY WHETHER YOU DO FINANCING, BUY HERE PAY HERE OR CASH.  IT WILL ALSO DEPEND ON WHERE YOU LIVE.  PLEASE CALL US AT 724-437-5274 FOR MORE DETAILS.  HOME OF THE 100% GUARANTEED CREDIT APPROVAL!  EVERYBODY GETS APPROVED!  THE DOWN PRICES ON THIS LISTING MAY VARY DEPENDING ON A PERSONS CREDIT OR INCOME VERIFICATION.  LBSI AUTOMOTIVE IS NOT RESPONSIBLE FOR TYPOGRAPHICAL ERRORS.  PUBLISHED PRICE SUBJECT TO CHANGE WITHOUT NOTICE. ALL FEATURES AND EQUIPMENT LISTED MAY NOT BE ON VEHICLE. PLEASE VERIFY ACTUAL OPTIONS WITH INTERNET DEPARTMENT BY EMAIL OR PHONE.  IF YOU ARE COMING TO OUR OFFICE AND PLAN ON PURCHASING A VEHICLE PLEASE BE HERE TWO HOURS PRIOR TO CLOSING.  PLEASE SEE OUR WEBSITE FOR HOURS AND TIMES AS THEY MAY CHANGE.  WE DO NOT STAY OPEN AFTER HOURS AND CAN NOT GET YOUR CAR TITLED AFTER HOURS.  WE DO TAKE CASH IN PERSON, VISA AND MASTER CARD ONLY FOR A CERTAIN AMOUNT (PLEASE CALL FIRST) CREDIT CARDS WILL ONLY BE ACCEPTED WITH A VALID DRIVERS LICENSE AVAILABLE WITH THE SAME INFORMATION ON IT AS THE CUSTOMER MAKING THE PURCHASE.  WE LOOK FORWARD TO SEEING YOU SOON.  Vehicle Options ABS BrakesAir ConditioningAM/FM RadioAutomatic HeadlightsCD PlayerChild Safety Door LocksDaytime Running LightsDriver AirbagDriver Multi-Adjustable Power SeatFront Side AirbagInterval WipersPassenger AirbagPower Adjustable Exterior MirrorPower Door LocksPower WindowsRear Window DefoggerSecond Row Folding SeatSide Head Curtain AirbagSteel WheelsTachometerTelematics SystemTelescopic Steering ColumnTilt SteeringTilt Steering ColumnTraction ControlTrunk Anti-Trap DeviceVehicle Anti-TheftVoice Activated Telephone  LBSI Automotive LLC Jim Antolik 109 Pittsburgh St. Uniontown PA 15401 724-437-5274BatchID: 4VOY35IBQWID: 17446042 Updated 4/28/2021 9:56:14 PM EST",,pa,39.905181,-79.727095,2021-04-21T10:02:31-0400
7310287588,https://pittsburgh.craigslist.org/cto/d/lawrence-2012-honda-accord-coupe-ex/7310287588.html,pittsburgh,https://pittsburgh.craigslist.org,10800,2012,,EX-L,good,4 cylinders,gas,91000,clean,automatic,1HGCS1B80CA020104,fwd,mid-size,coupe,red,https://images.craigslist.org/00b0b_kDDo88a24pJz_0ak07K_600x450.jpg,"Loaded, with heated seats, sunroof, sport seats, 270 Watt Honda premium stereo 7 speakers, like new Parelli tires, 190 HP 2.4liter 16 valve engine, 17"" Alloy wheels, cosmetic body scratches on front bumper cover (see photo). Very well maintained with all synthetic oil changes, newer battery and very recent transmission flush by Valvoline.  Front Wheel Drive Excellent mechanical condition very clean car.  Very reliable runs like a top! Email number or any questions and I will call or email you back.  BMW LEXUS SUV TOYOTA NISSAN SUBARU MAZDA",,pa,40.284741,-80.112385,2021-04-21T09:53:36-0400
7310283592,https://pittsburgh.craigslist.org/ctd/d/gibsonia-2008-porsche-911-carrera/7310283592.html,pittsburgh,https://pittsburgh.craigslist.org,62900,2008,porsche,911,,,gas,22618,clean,manual,WP0CB29958S775981,rwd,,,silver,https://images.craigslist.org/00H0H_h9lkffsOwzHz_09Q07m_600x450.jpg,"Krebs Chrysler Jeep Dodge address:    100 Krebs Drive & RT 8 Gibsonia PA, 15044phone:      ☎ (724) 602-2588 ext 32text:       Text 32 to (724) 602-2588 for more details  link:       https://11576.bestusedcarmarket.com/v/44959746/2/22297926/32  contact:    Brian Boyle   2008 PORSCHE 911 CARRERA S Vehicle InfoStock #: KP4217AVIN: WP0CB29958S775981Condition: UsedOdometer: 22618Fuel Efficiency: 17/25DrivetrainEngine: 3.8Fuel Type: GasolineTransmission Type: 6-Speed ManualDrivetrain: RWDBody & InteriorExterior Color: SilverOEM Color Name: Arctic Silver MetallicInterior Color: BlackDoors: 2Description This Arctic Silver Metallic 2008 Porsche 911 Carrera S might be just the convertible for you.  For a good-looking vehicle from the inside out, this convertible features a dazzling arctic silver metallic exterior along with a black interior.  This convertible has a sporty look with the rear spoiler feature.  Good cars sell fast! Give us a call and schedule an appointment today!  Contact Information: Krebs Chrysler Dodge Jeep RAM, 100 Krebs Drive & RT 8, Gibsonia, PA, 15044, Phone: (724) 444-8000, E-mail: sales@krebscjd.com.OptionsStability Control.,             Suspension Active.,             Headlights HID.,                Headlights Self-Leveling.,      Rollover Protection System.,    Airbags - Front - Side.,        Convertible Roof Power.,        Cruise Control.,                ABS Brakes (4-Wheel).,          Headlight Cleaners.,            Power Door Locks.,              Power Windows.,                 Exterior Mirrors Power.,        Exterior Mirrors Heated.,       Daytime Running Lights.,        Front Fog Lights.,              Rear Seats Bucket.,             Floor Mat Material Carpet.,     Windows Rear Defogger.,         Braking Assist.,                Airbags - Front - Dual.,        Rear Seats Split Folding.,      Rear Spoiler.,                  Security Engine Immobilizer.,   Front 12V Power Outlet(s).,     Rear Fog Lights.,               External Temperature Display.,  Traction Control.,              Child Seat Anchors.,            Reading Lights Front.,          Tachometer.,                    Cargo Area Light.,              One-Touch Windows: 2.,          2-stage Unlocking.,             Clock.,                         Convertible Rear Window Glass., Front Headrests Adjustable.,    Front Headrests Integrated.,    Number Of Front Headrests 2.,   Trip Odometer.,                 Security Anti-Theft Alarm System.,                              Air Conditioning - Front - Automatic Climate Control.,          Windows Front Wipers: Rain Sensing.,                            Seats Front Seat Type: Sport Bucket.,                           Driver Adjustable Suspension: Ride Control.,                    Air Conditioning Air Filtration: Active Charcoal.,              Power Steering Speed-Proportional.,                             Windows Heated Windshield Washer Jets.,                         Exterior Mirrors Heated Driver Mirror.,                         Driver Seat Power Adjustments: 4.,                              Windows Front Wipers: Variable Intermittent.,                   Steering Wheel Tilt And Telescopic.,                            Front Suspension Classification: Independent.,                  Front Suspension Type: Macpherson Struts.,                      Electronic Brakeforce Distribution.,                            Convertible Roof Remote Operation.,                             Airbags - Passenger - Occupant Sensing Deactivation.,           Center Console Front Console With Storage.,                     Driver Seat Power Adjustments: Recline.,                        Passenger Seat Power Adjustments: 4.,                           Passenger Seat Power Adjustments: Recline.,                     Seatbelts Seatbelt Force Limiters: Front.,                      Seatbelts Seatbelt Pretensioners: Front.,                       Seats - Driver Seat Power Adjustments: Height.,                 Seats - Passenger Seat Power Adjustments: Height.,              Vanity Mirrors Dual Illuminating.,                              Suspension Stabilizer Bar(s): Front.,                           Suspension Stabilizer Bar(s): Rear.,                            Air Conditioning - Front - Single Zone.,                        Convertible Roof With Wind Blocker.,                            Driver Seat Manual Adjustments: 2.,                             Emergency Interior Trunk Release.,                              Passenger Seat Manual Adjustments: 2.,                          Warnings And Reminders Low Fuel Level.,                          Krebs Chrysler Jeep Dodge address:    100 Krebs Drive & RT 8 Gibsonia PA, 15044phone:      ☎ (724) 602-2588 ext 32text:       Text 32 to (724) 602-2588 for more details  link:       https://11576.bestusedcarmarket.com/v/44959746/2/22297926/32  contact:    Brian Boyle",,pa,40.622694,-79.942979,2021-04-21T09:46:11-0400


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
    
     
Before generating anything, please let me know if this is worth it?


Yes — this is worth it, especially for teaching Bronze/Silver/Gold with DuckDB, because vehicles.csv has the exact “real-world messiness” that makes the architecture feel necessary (missing values, messy text fields, multiple categorical columns, time + location). It’s a much better lakehouse demo than a toy dataset.

That said, it’s worth it only if we do it the right way, because your file is big (≈1.45 GB, 426,881 rows) and has very wide + messy columns (e.g., description, VIN, lat/long, lots of nulls). A naive notebook that loads everything into pandas will be slow, memory-heavy, and frustrating.

What makes it worth it (educational value)
	•	Bronze: demonstrates raw landing at scale (CSV + messy schema inference).
	•	Silver: demonstrates why cleaning, typing, normalization, and feature engineering matters (posting_date parsing, price sanity, odometer sanity, standardizing categories, dropping unusable rows, trimming strings).
	•	Gold: demonstrates business analytics outputs (market pricing trends, manufacturer comparisons, state/regional insights, year-of-car vs price, condition vs price, fuel/transmission patterns, outlier detection).
	•	Great for SQL patterns: WITH, window functions, percentiles, ranking, cohorts by time, geo bucketing.

What would make it not worth it

If the expectation is:
	•	“Load the whole 1.45GB file into pandas and do everything in pandas”
	•	or “Make many charts without sampling/aggregation”
	•	or “Treat Bronze/Silver/Gold as just naming, without real transformations”

Then it becomes pain with little learning.

The right approach (so it’s 100% worth it)

Performance-safe design (recommended)
	•	Use DuckDB for all heavy lifting
	•	Use pandas only for small result sets (aggregations) used in charts
	•	In Silver, convert the cleaned dataset into Parquet (or a DuckDB table) for fast reuse
	•	Use posting_date to create a time partition (month/year) for Gold trends

Minimal but “real” lakehouse transformations

Bronze (raw view)
	•	read_csv_auto('vehicles.csv', ...) (don’t over-clean)
	•	metadata inspection: DESCRIBE, null counts, distinct counts

Silver (clean table)
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

Gold (curated views/tables)
	•	KPIs: median price by state/manufacturer/month
	•	segment tables: top manufacturers by listings, average/median price trends, condition mix
	•	outlier tables: top 1% price listings by market, etc.

About your mixed requirements (vehicles + insurance)

You listed items 3–6 about insurance.csv and 4 yearly files. That’s still worth keeping as a small “warm-up lakehouse”, then vehicles.csv becomes the capstone.

If you want, I can structure the deliverables as:
	•	Part A (Insurance, small): clean teaching lakehouse (fast, simple)
	•	Part B (Vehicles, big): realistic lakehouse + full EDA + deeper SQL

One practical note

Because vehicles.csv is huge, the final notebook should:
	•	avoid SELECT * LIMIT ... on wide text fields repeatedly
	•	avoid pulling description into pandas
	•	sample for certain plots (or aggregate first)

⸻

If you say “go”, I’ll generate:
	•	a complete EDA notebook for vehicles.csv (DuckDB-first, MD documentation, safe charts)
	•	a Bronze/Silver/Gold DuckDB lakehouse notebook for vehicles
	•	10 meaningful English/SQL insights + charts
	•	a MD/MARP data story
	•	6 student questions + instructor solutions (MD/MARP)

(And I’ll keep everything runnable on a laptop without blowing up memory.)

-------

Done — I generated everything (DuckDB-only, no Parquet), and packaged it as a single downloadable bundle.

Download

Download the full vehicles lakehouse bundle (ZIP)￼

What’s inside the ZIP
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

How to run (important)

Place vehicles.csv next to the notebooks (or edit the path at the top of each notebook):

vehicles.csv
Vehicles_EDA_DuckDB.ipynb
Vehicles_Lakehouse_Bronze_Silver_Gold_DuckDB.ipynb

Then Run All. The notebooks are designed to keep pandas usage small (only aggregated results), so they remain laptop-friendly. ￼


Great — I’m glad the EDA notebook worked well. 👍
That’s actually the hardest part of this dataset because:
	•	vehicles.csv is 1.4 GB
	•	it contains 426K rows
	•	many columns are messy / sparse / text-heavy
	•	posting_date type inference can vary

So if the EDA runs correctly, the rest should be smooth.

⸻

What to test next (recommended order)

1️⃣ Lakehouse notebook

Run:

Vehicles_Lakehouse_Bronze_Silver_Gold_DuckDB.ipynb

Check these steps in order:

Bronze

SELECT COUNT(*) FROM bronze_vehicles;

Expected: ~426k rows.

⸻

Silver

SELECT COUNT(*) FROM silver_vehicles;

Expected: slightly fewer rows because of cleaning rules.

⸻

Gold

SELECT * FROM gold_kpi_month LIMIT 10;

You should see something like:

month	listings	median_price
2021-01	…	…
2021-02	…	…


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

issue	example
price = 0	fake ads
price = 1	placeholder
year = 0	missing
year = 1900	invalid
odometer = 0	unknown

The Silver layer already filters most of these, but you may still see some outliers.

This is actually excellent for teaching data cleaning.

⸻

Teaching tip (this dataset works extremely well for it)

You can ask students:

Why does the median price differ so much from the average price?

Because the distribution is extremely skewed.

That naturally leads to:

median()
percentiles()
robust statistics

which is exactly what a Gold layer should use.

⸻

If you’d like, I can also give you (very useful additions)

These would make the material even stronger for class:

📊 1. A Craigslist Data Warehouse star schema

Fact table + dimensions for OLAP.

🧠 2. 10 advanced OLAP queries

Using:
	•	RANK()
	•	DENSE_RANK()
	•	ROLLUP
	•	WINDOW functions

🎓 3. A final course project version

Students build:

Bronze → Silver → Gold
+
EDA
+
10 insights
+
Data story presentation

which works beautifully as a final assignment.

⸻

Enjoy testing the rest tonight — and if any cell breaks,
just paste the error and I’ll fix it quickly.


Excellent — this output actually looks correct and meaningful. 👍
Let’s interpret it because it tells a real data story.

Your Gold table produced:

month	listings	median_price	p90_price	avg_price
2021-04-01	284,845	16,300	38,990	19,797
2021-05-01	97,525	13,995	35,995	17,899


⸻

What this means (the insight)

1️⃣ April dominates the dataset

Most listings occurred in April 2021:

April listings ≈ 284k
May listings   ≈ 97k

This happens because the dataset snapshot was collected around April–May 2021, so April is the main crawl month.

For teaching, this is a good discussion point:

Data collection processes influence observed distributions.

⸻

2️⃣ Median vs Average price difference

Example for April:

Median price = $16,300
Average price = $19,797

Average is higher because the distribution contains expensive outliers (luxury cars).

This is why Gold layer uses MEDIAN and percentiles, not only averages.

Great teaching moment:

mean ≠ robust statistic
median = better for skewed distributions


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

• More older / cheaper vehicles posted
• Regional mix changed
• Sampling bias due to scraping window

This becomes a great classroom question.

⸻

Recommended additional Gold KPI (very useful)

Add vehicle age trends, which students love:

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

Then plot:

df = con.execute("SELECT * FROM gold_price_by_age").df()

plt.figure()
plt.plot(df["vehicle_age"], df["median_price"])
plt.title("Vehicle price vs age")
plt.xlabel("vehicle age")
plt.ylabel("median price")
plt.show()

Students immediately see the depreciation curve.

⸻

Your lakehouse pipeline is now working

You now have a realistic teaching pipeline:

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

⸻

If you want, I can also give you something extremely useful for teaching

A perfect final slide for students:

10 Real Business Questions Answered by the Dataset

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

These map exactly to the Gold queries you already built.

If you’d like, I can also give you a much stronger Gold layer 
(5 analytic tables) that turns this notebook into a very polished 
graduate-level lakehouse example.
