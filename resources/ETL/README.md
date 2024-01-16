# ETL: Extract Transform Load

------

## 1. ETL in Picture 

<img src="./etl-process-explained-diagram.png" height=380 width=620>

------

## 2. What is ETL? 

	Extract, transform, and load (ETL) is the 
	process of combining data from multiple 
	sources into a large, central repository 
	called a data warehouse. 
	
	ETL uses a set of business rules to clean 
	and organize raw data and prepare it for 
	storage, data analytics, and machine learning 
	(ML). You can address specific business 
	intelligence needs through data analytics 
	(such as predicting the outcome of business 
	decisions, generating reports and dashboards, 
	reducing operational inefficiency, and more).
	
	source: https://aws.amazon.com/what-is/etl/
	
-------

## 3. The ETL Process

* The most underestimated process in DW development
* The most time-consuming process in DW development
* Up to 80% of the development time is spent on ETL!

### 3.1 Extract

* Extract relevant data
* Extraction can be from many data sources

### 3.2 Transform

* Transform data to DW format
* Build DW keys, etc.
* Cleansing of data

### 3.3 Load

* Load data into DW
* Build aggregates, etc.

-------
## 4. Sample ETL Program

	[Create Parquet File](./create_parquet.py)
	[ETL: 1. extract, 2. transform, and 3. load](./etl_read_parquet_from_file_transform_and_load_to_mysql.py)

-------

## 5. Sample ELT Program

	[`create_parquet.py`](./create_parquet.py)
	[ETL: 1. extract, 2. load, and 3. transform](.elt_read_parquet_from_file_and_load_to_mysql_then_transform.py)

-------

## 6. ETL References

1. [Understanding ETL by O'reilly](./Understanding-ETL-by-Oreilly.pdf)

2. [What is ETL? by IBM](https://www.ibm.com/topics/etl)

3. [What is ETL (Extract Transform Load)?](https://aws.amazon.com/what-is/etl/)

4. [What is ETL? The Ultimate Guide](https://www.matillion.com/blog/what-is-etl-the-ultimate-guide)

5. [Create Your First ETL Pipeline with Python](https://anujsyal.com/create-your-first-etl-pipeline-with-python)

6. [Implementing ETL Process Using Python to Learn Data Engineering](https://www.analyticsvidhya.com/blog/2021/06/implementing-python-to-learn-data-engineering-etl-process/)

7. [Build an ETL Data Pipeline using Python](https://blog.det.life/build-an-etl-data-pipeline-using-python-139c6875b046)

8. [Setting Up ETL Using Python Simplified 101](https://hevodata.com/learn/etl-using-python/)
