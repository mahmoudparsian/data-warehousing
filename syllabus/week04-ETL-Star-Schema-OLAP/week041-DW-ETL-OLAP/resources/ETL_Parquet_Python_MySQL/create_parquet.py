from __future__ import print_function 
import sys 
from pyspark.sql import SparkSession 
#-----------------------------------------------------
# 1. Create a sample Spark DataFrame
# 2. Save DataFrame as a Parquet file
#
# Input: NONE
#------------------------------------------------------
# Input Parameters:
#    NONE
#-------------------------------------------------------
# @author Mahmoud Parsian
#-------------------------------------------------------

#==========================================
# create an instance of SparkSession
spark = SparkSession.builder.getOrCreate()

employees = [("alex", "Ames", "1/21/2020", 34000, 1200),\
        ("alex", "Sunnyvale", "3/22/2020", 32000, 1500),\
        ("alex", "Cupertino", "1/24/2020", 40000, 400),\
        ("mary", "Ames", "2/20/2020", 38000, 800),\
        ("mary", "Stanford", "1/19/2022", 45000, 500),\
        ("mary", "Campbell", "9/20/2023", 55000, 600),\
        ("jeff", "Ames", "12/21/2021", 60000, 700),\
        ("jeff", "Sunnyvale", "4/10/2021", 70000, 300),\
        ("jane", "Austin", "5/16/2022", 80000, 800)]

column_names =   ["name", "city", "date_created", "salary", "bonus"]              
#
print("employees = ", employees)
    
# create a Spark DataFrame
df = spark.createDataFrame(employees, column_names)
print("df.count(): ", df.count())
print("df.collect(): ", df.collect())
df.show()
df.printSchema()

# create a single parquet file
df.repartition(1).write.parquet("/tmp/parquet")
