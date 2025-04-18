# Data Warehousing Project 

* Last updated date: March 25, 2025, 8:47 PM PST 

		NOTE: This document is a live document 
		and will be updated on a daily basis.

* The goal of this project is to design, build, 
  and demo a data warehouse, and fianlly 
* Provide/show 5 OLAP queries, which will help 
  the businesses to make better decisions
* Based on these 5 OLAP queries: what are your recommendations to the business leaders

## 1. Team 

* Each team is comprised of 3 students
* Each student should act as a co-leader of a team

## 2. Deadlines

| Activity                      | Must be completed before |
|-------------------------------|--------------------------| 
| Team selection                | April 3, 2025            |
| Data selection                | April 10, 2025           |
| Exploratory Data Presentation | TBDL        |
| Final Project Presentation    | TBDL        |



## 3. Points

This project covers 30% of your overall grade.

* 10% points: Exploratory Data Presentation
* 10% points: documentation & implementation
* 10% points: presentation with powerpoint and Tableau

## 4. Data

* must make sense for data warehousing
* your data must span over years (3 to 5 years) 
* with minimum of 1 to 10 million records

### 4.1 data sets

[1. New York Taxi Data: YELLOW Taxi](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

------

[2. New York Taxi Data: GREEN Taxi](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

-------

[3. Million Song Dataset](http://millionsongdataset.com)

------

[4. Chicago Data Portal, bike rides, 21.2 Million](https://data.cityofchicago.org/Transportation/Divvy-Trips/fg6s-gzvg/about_data)

~~~
Downloaded file name: Divvy_Trips_20250121.csv

Downloaded file size: 5,125,844,091 

% head Divvy_Trips_20250121.csv
TRIP ID,START TIME,STOP TIME,BIKE ID,TRIP DURATION,FROM STATION ID,FROM STATION NAME,TO STATION ID,TO STATION NAME,USER TYPE,GENDER,BIRTH YEAR,FROM LATITUDE,FROM LONGITUDE,FROM LOCATION,TO LATITUDE,TO LONGITUDE,TO LOCATION
8546790,12/31/2015 05:35:00 PM,12/31/2015 05:44:00 PM,979,521,117,Wilton Ave & Belmont Ave,229,Southport Ave & Roscoe St,Subscriber,Female,1991,41.94018,-87.65304,POINT (-87.65304 41.94018),41.943739,-87.66402,POINT (-87.66402 41.943739)
8546793,12/31/2015 05:37:00 PM,12/31/2015 05:41:00 PM,1932,256,301,Clark St & Schiller St,138,Clybourn Ave & Division St,Subscriber,Male,1992,41.907993,-87.631501,POINT (-87.631501 41.907993),41.904613,-87.640552,POINT (-87.640552 41.904613)
8546795,12/31/2015 05:37:00 PM,12/31/2015 05:40:00 PM,1693,134,465,Marine Dr & Ainslie St,251,Clarendon Ave & Leland Ave,Subscriber,Female,1987,41.9716,-87.650154,POINT (-87.650154 41.9716),41.967968,-87.650001,POINT (-87.650001 41.967968)
8546797,12/31/2015 05:38:00 PM,12/31/2015 05:55:00 PM,3370,995,333,Ashland Ave & Blackhawk St,198,Green St (Halsted St) & Madison St,Subscriber,Male,1975,41.907066,-87.667252,POINT (-87.667252 41.907066),41.881892,-87.648789,POINT (-87.648789 41.881892)
8546798,12/31/2015 05:38:00 PM,12/31/2015 05:41:00 PM,2563,177,48,Larrabee St & Kingsbury St,111,Sedgwick St & Huron St,Subscriber,Male,1990,41.897764,-87.642884,POINT (-87.642884 41.897764),41.894666,-87.638437,POINT (-87.638437 41.894666)
8546799,12/31/2015 05:39:00 PM,12/31/2015 05:52:00 PM,1039,808,280,Morgan St & 31st St,282,Halsted St & Maxwell St,Subscriber,Male,1980,41.8378,-87.65114,POINT (-87.65114 41.8378),41.864883,-87.647071,POINT (-87.647071 41.864883)
8546803,12/31/2015 05:40:00 PM,12/31/2015 05:43:00 PM,1233,194,174,Canal St & Madison St,198,Green St (Halsted St) & Madison St,Subscriber,Male,1975,41.882091,-87.639833,POINT (-87.639833 41.882091),41.881892,-87.648789,POINT (-87.648789 41.881892)
8546805,12/31/2015 05:40:00 PM,12/31/2015 05:45:00 PM,2489,309,277,Ashland Ave & Grand Ave,30,Ashland Ave & Augusta Blvd,Subscriber,Male,1987,41.891072,-87.666611,POINT (-87.666611 41.891072),41.899643,-87.6677,POINT (-87.6677 41.899643)
8546813,12/31/2015 05:41:00 PM,12/31/2015 05:53:00 PM,436,674,54,Ogden Ave & Chicago Ave,181,LaSalle St & Illinois St,Subscriber,Male,1987,41.896362458,-87.654061273,POINT (-87.654061 41.896362),41.890749,-87.63206,POINT (-87.63206 41.890749)
~~~

------

[5. Flights and Airports Data](https://www.kaggle.com/datasets/tylerx/flights-and-airports-data?select=raw-flight-data.csv)

-------

[6. City of Chicago, Taxi Trips](https://catalog.data.gov/dataset/taxi-trips-2024/resource/89b74374-dec6-473e-a143-8e7bb1dfa5b1)

~~~
Downloaded file name: Taxi_Trips__2024-_.csv

Downloaded file size: 2,686,502,968 

% head Taxi_Trips__2024-_.csv
Trip ID,Taxi ID,Trip Start Timestamp,Trip End Timestamp,Trip Seconds,Trip Miles,Pickup Census Tract,Dropoff Census Tract,Pickup Community Area,Dropoff Community Area,Fare,Tips,Tolls,Extras,Trip Total,Payment Type,Company,Pickup Centroid Latitude,Pickup Centroid Longitude,Pickup Centroid Location,Dropoff Centroid Latitude,Dropoff Centroid Longitude,Dropoff Centroid  Location
0000184e7cd53cee95af32eba49c44e4d20adcd8,f538e6b729d1aaad4230e9dcd9dc2fd9a168826ddadbd67c2f79331875dc586863d73aa3169fb266dc5e5ed6cdc8687537de8071a51556146f5251d4d8e8237f,01/19/2024 05:00:00 PM,01/19/2024 06:00:00 PM,4051,17.12,17031980000,17031320100,76,32,45.50,10.00,0.00,4.00,60.00,Credit Card,Flash Cab,41.97907082,-87.903039661,POINT (-87.9030396611 41.9790708201),41.884987192,-87.620992913,POINT (-87.6209929134 41.8849871918)
000072ee076c9038868e239ca54185eb43959db0,e51e2c30caec952b40b8329a68b498e18ce8a1f40fa75c71e425e9426db562ac617b0a28e1c69f5c579048f75a43a2dc066c17448ab65f5016acca10558df3ed,01/28/2024 02:30:00 PM,01/28/2024 03:00:00 PM,1749,12.7,,,6,,33.75,0.00,0.00,0.00,33.75,Cash,Flash Cab,41.944226601,-87.655998182,POINT (-87.6559981815 41.9442266014),,,
000074019d598c2b1d6e77fbae79e40b0461a2fc,aeb280ef3be3e27e081eb6e76027615b0d40925b84d3eb1301a01293a34c41ec45fe1ff1ceeb0e769565af1573d216d5a6c8bbc260b9f8a8db9be4ef74d31c78,01/05/2024 09:00:00 AM,01/05/2024 09:00:00 AM,517,3.39,,,6,8,10.91,2.78,0.00,1.00,14.69,Mobile,Taxicab Insurance Agency Llc,41.944226601,-87.655998182,POINT (-87.6559981815 41.9442266014),41.899602111,-87.633308037,POINT (-87.6333080367 41.899602111)
00007572c5f92e2ff067e6f838a5ad74e83665d3,7d21c2ca227db8f27dda96612bfe5520ab408fa9a462c8ca4c73a22c362b8022ac8e0f5538c9b820dc3a6be61e06f215654909a3b02770ddf84631e948479436,01/22/2024 08:45:00 AM,01/22/2024 09:30:00 AM,2050,15.06,,,76,,39.25,11.31,0.00,5.50,56.56,Credit Card,Globe Taxi,41.980264315,-87.913624596,POINT (-87.913624596 41.9802643146),,,
00007c3e7546e2c7d15168586943a9c22c3856cf,8ef1056519939d511d24008e394f83e925d2539d668a002c97c441c1d24ab86e29b31a6d8544356006c1eee49dda811760c872d4ddcbaffd55a681b17864a014,01/18/2024 07:15:00 PM,01/18/2024 07:30:00 PM,1004,1.18,17031839100,17031839100,32,32,15.94,3.72,0.00,0.00,19.66,Mobile,5 Star Taxi,41.880994471,-87.632746489,POINT (-87.6327464887 41.8809944707),41.880994471,-87.632746489,POINT (-87.6327464887 41.8809944707)
0000bab44d0d673a222e7f1a0a6026563519aa25,833e49f9757b594a8a6765b93d1f7d8ad483e61c3a89d1a808ef40a33940ccaac349d4aec1e6415a079b1bc3a13f186b5af03683e52ed789153e97a3d59557a8,01/09/2024 05:00:00 PM,01/09/2024 05:00:00 PM,12,0.18,,,3,6,3.50,0.00,0.00,0.00,3.50,Cash,Taxicab Insurance Agency Llc,41.96581197,-87.655878786,POINT (-87.6558787862 41.96581197),41.944226601,-87.655998182,POINT (-87.6559981815 41.9442266014)
0000cf293ada965f89a98c8ccfae7b0ce3a03e41,37073e8c9e454886fe4a916f80a9a3478570e7dd3e663f40c5b81eae90f8f611027c67455f43b426f4c34dcb7fdb6697c82a3c6d00237f11a4a6cf5b1d1ce0c7,01/04/2024 07:15:00 AM,01/04/2024 07:30:00 AM,484,1.59,17031281900,17031320100,28,32,7.75,1.24,0.00,0.00,9.49,Mobile,City Service,41.879255084,-87.642648998,POINT (-87.642648998 41.8792550844),41.884987192,-87.620992913,POINT (-87.6209929134 41.8849871918)
0001235258d46a21317b6691ade9386c4d7e02c4,715b091e1001d1c17938c3b5ed7e23d926c53150ee2d0fac31336b49a14b7f17096d5ab25747e024765899ddc7653b9155ef9b956b8d179066cfe3e2cc16ec0d,01/25/2024 11:15:00 AM,01/25/2024 11:30:00 AM,1686,13.01,17031320100,17031980100,32,56,34.25,7.95,0.00,5.00,47.70,Credit Card,Chicago Independents,41.884987192,-87.620992913,POINT (-87.6209929134 41.8849871918),41.785998518,-87.750934289,POINT (-87.7509342894 41.785998518)
00012902ec577e1a25815a527b4204782daa98c8,4628ef9dfa973bdfe877c5aa9d9738f9dc1204e54f2f1a4cc18141f37e2e66d080533f82510a96d1525b28eee833696f7e1337e9999a38f2fd5babf71585a344,01/09/2024 03:15:00 PM,01/09/2024 03:30:00 PM,1047,3.02,17031330100,17031081500,33,8,11.08,2.00,0.00,0.00,13.08,Mobile,Chicago Independents,41.859349715,-87.617358006,POINT (-87.6173580061 41.859349715),41.892507781,-87.626214906,POINT (-87.6262149064 41.8925077809)
~~~

-------

## 5. Building Your DW Project

1. What is your DW Project? 

2. How you will build a Data Warehouse 

3. Database: MySQL or you choice (must be able to hold at least 10 millions of records per table).
	* source database and files
	* target database (where a data warehouse is built)

4.  Programming Language: Python or your choice

## 6. Project components

Components of your project should cover:

1. Project Document

2. Project Implementation

3. Presentation of your project to the whole class 

	* Presentation time: 15 to 20 minutes
	* Will be done 2 weeks before final exam


## 7. Data Set Descripton

To describe a dataset, you typically need to: 

	1. identify the source and context of the data, 

	2. list the variables and their data types, 

	3. summarize central tendencies (mean, median, mode), 

	4. analyze the distribution and spread (standard 
	   deviation, range), 

	5. identify any outliers, and visualize the data 
	   using appropriate graphs to reveal patterns 
	   and relationships; 
	   
	6. this often involves initial data cleaning 
	   and preparation 


### 7.1 Key steps in describing a dataset:

**Define the objective:**

        Clearly state the purpose of the data collection 
        and what insights you aim to extract. 

**Data collection:**

        Explain how the data was gathered, including 
        the sampling method, timeframe, and any 
        relevant demographics. 

**Data cleaning:**

        Identify and address missing values, inconsistencies, 
        outliers, and potential errors in the data. 

**Variable description:**

        List all variables: Enumerate each variable 
        included in the dataset, specifying whether 
        they are categorical or numerical. 

**Data types:**

        Define the data type for each variable (e.g., 
        integer, string, date). 

**Variable labels:**

        Clearly explain what each variable represents. 

**Descriptive statistics:**

        Central tendency: Calculate measures like mean, 
        median, and mode for each relevant variable to 
        understand the "center" of the data distribution. 

        Spread/Variability: Calculate measures like standard 
        deviation, range, and interquartile range to assess 
        how spread out the data is. 

**Data visualization:**

        Histograms: Visualize the distribution of 
        numerical variables. 

        Boxplots: Compare the distribution of a 
        variable across different groups. 

        Scatter plots: Examine relationships between 
        two numerical variables. 

        Bar charts: Visualize the frequencies of 
        categorical variables. 

**Outlier analysis:**

        Identify and discuss any extreme data points that 
        deviate significantly from the overall pattern. 

**Correlations:**

        Analyze relationships between variables using 
        correlation coefficients to understand how they 
        might be associated. 

**Interpretation:**

        Explain the key findings from your 
        descriptive analysis, highlighting 
        significant patterns, trends, and 
        potential insights. 

**Important considerations:**

         Context matters: Always consider the context of the 
         data when interpreting results. 

         Data quality: Ensure the data is accurate, complete, 
         and reliable before proceeding with analysis. 

         Audience suitability: Tailor your description to the 
         level of understanding of your audience. 


## 8. [Exploratory Data Analysis on Iris Dataset](https://www.geeksforgeeks.org/exploratory-data-analysis-on-iris-dataset/)

The Iris dataset is a well-known dataset in machine learning, 
containing measurements of sepal and petal length and width for 
three different species of Iris flowers (Setosa, Versicolor, and 
Virginica), making it a classic example for classification tasks 
due to its simplicity and clear separation between the species; 
it's often used to test and compare the performance of different 
classification algorithms as beginners learn basic machine learning 
concepts like data preprocessing and model evaluation. 

[Iris Data Set explanation](https://www.google.com/url?sa=i&url=https%3A%2F%2Feminebozkus.medium.com%2Fexploring-the-iris-flower-dataset-4e000bcc266c&psig=AOvVaw1Go-kA_gCR6iyZmW-B5vWF&ust=1737704841918000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCNDpw5uti4sDFQAAAAAdAAAAABAE)


## 9. Project Document Structure

1. Introduction
	* Describe your project in 3 bullet items

2. **Data:**
	* Describe your data, make sense of the data
	* source of data
	* data attributes
	* what features of data are important
	* ...

3. ETL/ELT:  
	* your scripts, what they do ...
	* description of your scripts, what they do ...
	* ETL/ELT: how to load data to DW by year (2020, 2021, 2022, ...)

4. Star schema

	* How to build your star schema, logic and rationale 
	* Star schema description: FACT table(s) and DIM tables
	* BI queries and presentations: list of 5 queries in English and SQL
	* Tableau presentation
	* Your recommendations based on 5 OLAP queries

