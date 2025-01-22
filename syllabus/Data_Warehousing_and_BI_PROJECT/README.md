# Data Warehousing Project 

* Last updated date: January 14, 2025 

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

| Activity               | Must be completed before |
|------------------------|--------------------------| 
| Team selection         | January 16, 2025         |
| Data selection         | January 23, 2025         |
| Project implementation | February 21, 2025        |



## 3. Points

This project covers 30% of your overall grade.

*  3 points: Team and Data Presentation
*  7 points: documentation
* 10 points: implementation
* 10 points: presentation with powerpoint and Tableau

## 4. Data

* must make sense for data warehousing
* your data must span over years (3 to 5 years) 
* with minimum of 1 to 10 million records

### 4.1 data sets

[1. New York Taxi Data: YELLOW Taxi](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

[2. New York Taxi Data: GREEN Taxi](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

[3. Million Song Dataset](http://millionsongdataset.com)

[4. Chicago Data Portal, bike rides, 21.2 Million](https://data.cityofchicago.org/Transportation/Divvy-Trips/fg6s-gzvg/about_data)

[5. Flights and Airports Data](https://www.kaggle.com/datasets/tylerx/flights-and-airports-data?select=raw-flight-data.csv)

[6. City of Chicago, Taxi Trips](https://catalog.data.gov/dataset/taxi-trips-2024/resource/89b74374-dec6-473e-a143-8e7bb1dfa5b1)

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



## 8. Project Document Structure

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

