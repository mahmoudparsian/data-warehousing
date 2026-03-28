I have a single insurance.csv file:

```
% ls -l
-rw-r--r--@ 1 max  staff  55631 Mar  3 10:54 insurance.csv
```

```
% wc -l insurance.csv
    1339 insurance.csv
```

```    
% head insurance.csv
age,gender,bmi,children,smoker,region,charges
19,female,27.9,0,yes,southwest,16884.924
18,male,33.77,1,no,southeast,1725.5523
28,male,33,3,no,southeast,4449.462
33,male,22.705,0,no,northwest,21984.47061
32,male,28.88,0,no,northwest,3866.8552
31,female,25.74,0,no,southeast,3756.6216
46,female,33.44,1,no,southeast,8240.5896
37,female,27.74,3,no,northwest,7281.5056
37,male,29.83,2,no,northeast,6406.4107
```

from this I want to create 4 files
(each file for a year)

```
insurance.2021.csv for year 2021
insurance.2022.csv for year 2022
insurance.2023.csv for year 2023
insurance.2024.csv for year 2024
```

I want these 4 files to be realistic data
like the insurance.csv file. 

Each file should have about 1300 rows.

So when we are reading raw data, we will 
inject the year in the table/view.

Then analyze these 4 data 
files for bronze, silver, gold architeture of 
data lakehouse,  to understand these 3 layers 
of architeture using DuckDB.

```
1. I want to be able to use DuckDB and 
   get metadata information form insurance.csv file

2. Create tables/views from 4 files with year dimension

3. Create Silver views/tables

4. Create Gold views/tables.

5. Create 10 insightful English/SQL queries, 
   which has a true meaning in understanding this dataset.

6. Create a notebook with these 10 queries and 
   write insight, SQL, and an associated graph/ 
   presentation for each query

7. Create a Data Story for this as MD/MARP downloadable file
```


It mirrors a real lakehouse workflow without needing “big data”

	•	Bronze: raw CSVs landed “as-is” 
	  (your 4 yearly files).
	
	•	Silver: cleaned + standardized + typed + 
	   quality rules (null handling, domain 
	   checks, deduping, consistent categories).
	
	•	Gold: curated business views (aggregations, 
	  KPIs, segments like smoker/non-smoker, 
	  region rollups, risk buckets).


DuckDB is perfect for teaching this because it can:

	•	infer schemas from CSV
	•	create views/tables quickly
	•	query across many files (glob)
	•	generate curated layers without 
	  any Spark cluster overhead

Adding “year” is a realistic pattern

In many pipelines, the partition key (like year) comes from file path or ingestion metadata, not from the raw content. So “inject year when reading” is exactly how it’s done.

Your dataset supports meaningful insights

Insurance charges + smoker + BMI + age + region → lots of natural analytics:

	•	driver analysis (smoker effect)
	•	segmentation (age bands, BMI classes)
	•	distribution + outliers
	•	regional comparisons
	•	cost per dependent
	•	model-friendly feature engineering 
	  (even if you don’t model yet)

The one thing to be careful about

“Realistic” yearly files must not be simple copies

If you just duplicate the same 1338 rows four times and add different years, students will learn the architecture but the analytics will feel fake.

A better approach (still realistic and simple):

	•	start from the original distribution
	•	create each year’s file with ~1300 
	  rows via sampling + small controlled drift:
	•	slight year-to-year drift in charges 
	  (e.g., medical inflation)
	•	small shifts in region mix
	•	small shifts in smoker rate
	•	keep categories valid and consistent
	•	maintain realistic correlations (smokers higher charges; higher BMI slightly higher charges)

That makes Gold-layer comparisons across years actually interesting.

What you’ll get educationally

If done right, you’ll be able to teach:

	•	schema inference + metadata inspection 
	   in DuckDB
	•	ingestion patterns (multi-file, partitioned 
	   by year)
	•	data quality rules and “trust” progression
	•	dimensional modeling-ish thinking 
	  (year dimension, derived attributes)
	•	query patterns (rollups, ranking, 
	  cohorts, percentiles)

When it might not be worth it

Only if your goal is pure SQL practice 
(not Lakehouse architecture). If the class 
doesn’t care about layers and data quality, 
then splitting into years adds overhead.

But since you explicitly want Bronze/Silver/Gold + notebook + story, it aligns perfectly.

Recommended structure (simple + effective)

	•	data/bronze/insurance.2021.csv ... 2024.csv
	•	silver as DuckDB tables (typed, cleaned, 
	   standardized)
	•	gold as curated summary tables/views 
	  (KPIs, segments, year-over-year)

My suggestion before we generate

Generated the full bundle (4 realistic yearly CSVs + DuckDB lakehouse notebook + MD/MARP data story).

Download everything (recommended)

Download the full bundle (ZIP)￼

Individual downloads

	•	insurance.2021.csv￼
	•	insurance.2022.csv￼
	•	insurance.2023.csv￼
	•	insurance.2024.csv￼
	•	DuckDB notebook: Insurance_Lakehouse_DuckDB.ipynb￼
	•	Data Story (MD/MARP): 
	  Insurance_Lakehouse_Data_Story.marp.md￼

⸻

	1.	DuckDB metadata from CSV Notebook uses
	  read_csv_auto() + DESCRIBE to show 
	  inferred schema.
	  
	2.	Bronze views from 4 files + injected 
	  year 
	  Notebook reads insurance.*.csv and extracts 
	  year from filename via regexp_extract(filename, '(\\d{4})', 1).
	

Silver table
	
Creates silver_insurance with:

	•	enforced types
	•	normalized category strings
	•	domain checks (age/BMI/region/smoker/etc.)
	•	derived columns: bmi_class, age_band

Gold view

	Creates gold_kpi_year with KPI rollups 
	(avg/median/p90/total + smoker vs non-smoker averages).
	
	10 insightful English/SQL queries Included in 
	notebook, with meaningful analytics patterns 
	(percentiles, ranking, segmentation, contributions).
	
Each query shows:

	•	the SQL result dataframe
	•	a matching matplotlib chart (line/bar/stacked/pie/table)

	7.	MD/MARP data story: A slide deck explaining 
	  Bronze/Silver/Gold and the insights.

⸻


What this notebook includes

```
1️⃣ Clear Bronze / Silver / Gold architecture

With a diagram students can understand:

Raw Files
   │
   ▼
BRONZE  → raw CSV ingestion
   │
   ▼
SILVER  → cleaned + derived columns
   │
   ▼
GOLD    → KPI analytics
```

⸻

```
2️⃣ Clean DuckDB pipeline

Bronze

CREATE VIEW bronze_insurance AS
SELECT *,
       CAST(split_part(filename,'.',2) AS INTEGER) AS year
FROM read_csv_auto(
    'data/bronze/insurance.*.csv',
    header=true,
    filename=true
);
```

Silver

```
Adds:
	•	typed columns
	•	BMI class
	•	age bands
```

Gold

```
Creates KPI table:
	•	members
	•	avg charges
	•	median charges
	•	total charges
```
⸻

```
3️⃣ 10 meaningful analytics queries

Students analyze:
	1.	Average charges by year
	2.	Charges by region
	3.	Charges by smoker
	4.	Charges by BMI class
	5.	Charges by age band
	6.	Total charges by year
	7.	Children vs charges
	8.	Regional cost ranking
	9.	Average BMI by region
	10.	Top 20 highest charges
```
⸻

```
4️⃣ Automatic charts

Each query includes a chart such as:
	•	line trends
	•	bar comparisons
	•	ranking charts

All generated automatically with matplotlib.
```
⸻

```
5️⃣ Data story students can follow

At the end the notebook explains insights such as:
	•	smoking dramatically increases cost
	•	age and BMI drive medical expenses
	•	a few high-cost patients dominate spending
	•	regional differences are smaller than lifestyle effects
```
⸻

How to run it

Place the files like this:

```
data/
   bronze/
      insurance.2021.csv
      insurance.2022.csv
      insurance.2023.csv
      insurance.2024.csv
```

Then open the notebook and Run All.

⸻
