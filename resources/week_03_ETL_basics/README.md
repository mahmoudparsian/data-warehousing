# What is an ETL
# ETL with Python

### source: [ETL with Python by Dhiraj Patra](https://www.linkedin.com/pulse/etl-python-dhiraj-patra-my2cc/)

# What is an ETL?

## ETL (Extract, Transform, Load)


	ETL (Extract, Transform, Load) systems 
	are essential for data integration and 
	analytics workflows. They facilitate 
	
	1. the extraction of data from various sources, 
	
	2. transformation of the data into a usable format, and 
	
	3. loading it into a target system, 
	   such as a data warehouse or data lake. 
	

Here's a breakdown:

## 1. Extract: 

	This phase involves retrieving data from 
	different sources, including databases, 
	files, APIs, web services, etc. 
	
	The data is typically extracted in its raw form.

## 2. Transform: 

	In this phase, the extracted data undergoes 
	cleansing, filtering, restructuring, and 
	other transformations to prepare it for 
	analysis or storage. 
	
	This step ensures data quality and consistency.
	
## 3. Load: 

	Finally, the transformed data is loaded into 
	the target destination, such as a data warehouse, 
	data mart, or data lake. 
	
	This enables querying, reporting, and analysis 
	of the data.

## ETL Tools:

	There are numerous ETL tools available, 
	both open-source and commercial, offering 
	a range of features for data integration 
	and processing. Some popular ETL tools include:

* Apache NiFi: 

		An open-source data flow automation tool 
		that provides a graphical interface for 
		designing data pipelines.

* Talend: 

		A comprehensive ETL tool suite with support 
		for data integration, data quality, and big 
		data processing.


* AWS Glue: 

		A fully managed ETL service on AWS that 
		simplifies the process of building, running, 
		and monitoring ETL workflows.

* Cloud and ETL:

		Cloud platforms like Azure, AWS, and Google Cloud 
		offer scalable and flexible infrastructure for 
		deploying ETL solutions. They provide managed 
		services for storage, compute, and data processing,
		making it easier to build and manage ETL pipelines 
		in the cloud. Azure, for example, offers services 
		like Azure Data Factory for orchestrating ETL 
		workflows, Azure Databricks for big data processing, 
		and Azure Synapse Analytics for data warehousing 
		and analytics.
		
* Apache Spark: 

		Apache Spark is an open-source analytics engine 
		that processes large amounts of data.

## Example-1: Python ETL 

	Here's a simple Python example using 
	the pandas library for ETL:
	
	This example reads data from a CSV file, 
	applies a transformation to remove rows 
	with missing values, and then saves the 
	transformed data to a new CSV file.

```python
import pandas as pd

# Extract data from a CSV file
data = pd.read_csv("source_data.csv")

# Transform data (e.g., clean, filter, aggregate)
transformed_data = data.dropna()  # Drop rows with missing values

# Load transformed data into a new CSV file
transformed_data.to_csv("transformed_data.csv", index=False)
```


## Example-2: Pyspark ETL

	In this example, we use the PySpark library 
	to read data from Amazon S3, perform a 
	transformation to drop null values, and then 
	write the transformed data back to Amazon S3.


```python
from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder.getOrCreate()

# Read data from Amazon S3
df = spark.read.csv("s3://my_bucket/data/samples/", header=True)

# Perform transformations
transformed_df = df.dropna()

# Write transformed data back to ADLS Gen2
transformed_df.write.csv("s3://my_bucket/output/", mode="overwrite")

# Stop Spark session
spark.stop()
```

## Example-3: Pyspark ETL

Explanation:

	1. Extract: This step reads data from a CSV file 
		into a PySpark DataFrame.

	2. Transform: This step performs transformations 
		on the data, including filtering rows and 
		calculating the average salary.

	3. Load: This step writes the transformed data 
	   to a Parquet file.

Important:

	1. Replace "data.csv" with the path to your 
	   actual data file.
	
	2. You can customize the transformations based 
     on your requirements.

	3. Consider using spark.read.format("...") to 
	   read data from other sources like JSON, 
	   Avro, or databases.

	4. Similarly, use df.write.format("...") to 
	   write data to different destinations.

~~~python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Create a SparkSession object
spark = SparkSession.builder.getOrCreate()

#------------
# 1. Extract
#------------
# Read data from a CSV file
input_path = "/tmp/input/data.csv"
df = spark.read.csv(input_path, header=True, inferSchema=True)

#--------------
# 2. Transform
#--------------

# Filter rows where the "age" column is greater than 18
df = df.filter(col("age") > 18)

# Calculate the average salary
avg_salary = df.agg({"salary": "avg"}).collect()[0][0]

# Add a new column "salary_above_avg" indicating 
# if salary is above average
df = df.withColumn("salary_above_avg", col("salary") > avg_salary)

#---------
# 3. Load
#---------
# Write the transformed data to a Parquet file
output_path = "/tmp/output/transformed_data.parquet"
df.write.parquet(output_path)

# Stop the SparkSession
spark.stop()
~~~

