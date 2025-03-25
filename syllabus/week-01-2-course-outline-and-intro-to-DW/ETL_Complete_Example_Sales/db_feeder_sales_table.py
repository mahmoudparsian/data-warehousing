#!/usr/bin/env python
#
# Example: how to use Faker to create fake data 
# and inject them in a mysql database

#--------------------
# REQUIRED Libraries
#--------------------
# pip install Faker
# pip install mysql-connector
# pip install mysql-connector-python
# pip install simplejson

import sys
import json
import time
import os
import random
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from faker import Faker

# to create a DATE, we use the following
# we need start_date and end_date
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)

# products_list = [(product_id, price)]
products_list = [
    (100,  900),
    (200,  450),
    (300,  280),
    (400,  700),
    (500,  200),
    (600,  820),
    (650,   55),
    (700,  120),
    (800,  300),
    (900,   50),
    (950,   40),
    (960,  170),
    (965,  770),
    (967,  970),
    (970,   18),
    (975,   68),
    (980,   12),
    (985,  190),
    (986,   35),
    (987,   30),
    (988,   55)
]

#-----------------------------------------
# Database config is given as a JSON file
# read a JSON file and return a dictionary
def read_json(json_config_file):
    with open(json_config_file) as f:
        # Load the JSON data into a Python dictionary
        config_as_dict = json.load(f)
        return config_as_dict
#end-def
#-------------------------------------------
# quantity of 1 is favored
QUANTITY_LIST = [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3]
def get_quantity():
    return random.choice(QUANTITY_LIST) 
#end-def
#-------------------------------------------
def test_get_quantity():
    for i in range(10):
        print("test_get_quantity: get_quantity()=", get_quantity())
#-------------------------------------------
# get a (quantity, product_id, total price)
def get_quantity_and_product_id_and_total_price():
    quantity = get_quantity()
    #print("quantity=", quantity)
    product_and_price = random.choice(products_list)
    #print("product_and_price=", product_and_price)
    product_id = product_and_price[0]
    price = product_and_price[1]
    total_price = quantity * price
    return (quantity, product_id, total_price)
#end-def
#-------------------------------------------
def test_get_quantity_and_product_id_and_total_price():
    for i in range(10):
        quantity, product_id, total_price = get_quantity_and_product_id_and_total_price()
        print("test(): quantity=", quantity) 
        print("test(): product_id=", product_id)
        print("test(): total_price=", total_price)
#end-def
#-------------------------------------------
# get a customer_id in range {10, 11, ..., 29}
# customer_id = 28 and 29 not used: 
# these 2 customers did not buy any products
def get_customer_id():
    return random.randint(10, 27)
#end-def
#-------------------------------------------
# location_id = {1000, 1001, ..., 1013}
def get_location_id():
    return random.randint(1000, 1013)
#end-def
#-------------------------------------------
def get_database_connection(db_config):
    db_host = db_config["host"]
    db_name = db_config["database"]
    db_user = db_config["user"]
    db_pass = db_config["password"]
    #
    conn = mysql.connector.connect(
        host = db_host, 
        user = db_user, 
        password = db_pass,
        database = db_name
    )

    return conn
#end-def
#-------------------------------------------
def get_faker():
    Faker.seed(33422)
    the_faker = Faker()
    return the_faker
#-------------------------------------------
def test_faker(the_faker):
    print(the_faker.first_name()) 
    print(the_faker.last_name())
    print(the_faker.email())
    print(the_faker.city())
    print(the_faker.state())
    print(the_faker.date())
#end_def   
#-------------------------------------------
def test_dates(the_faker):
    for i in range(10):
        date_created = the_faker.date_between(start_date=start_date, end_date=end_date)
        print("date_created=", date_created)
#end_def   
#-------------------------------------------
# Transaction table: sales_transactions
create_table_sql = """
CREATE TABLE IF NOT EXISTS sales_transactions (
    sale_id INT  PRIMARY KEY,
    product_id INT,
    customer_id INT,
    location_id INT,
    sale_date DATE,
    quantity INT,
    total_amount INT
);
"""
#------------------------------------
# the main DRIVER program...
#------------------------------------
the_faker = get_faker()

test_faker(the_faker)

test_get_quantity()

test_get_quantity_and_product_id_and_total_price()


start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
#
test_dates(the_faker)

#-------------------------
# Command Line Parameters:
#-------------------------

#--------------------------------------------------
# Command Line Parameter 1: "db_config_source.json"
#--------------------------------------------------

# This is for a Transactional Database
# db_config_source_file = "db_config_source.json"
db_config_source_file = sys.argv[1]
source_db_config = read_json(db_config_source_file)

#---------------------------------------------------
# Command Line Parameter 2: number_of_rows
#---------------------------------------------------
number_of_rows = int(sys.argv[2])
print("number_of_rows=", number_of_rows)

# Create a Database Connection
conn = get_database_connection(source_db_config)
print("conn=",conn)

#----------------------------------------------------------
# Create Sales records and insert in Transactional Database
#----------------------------------------------------------
try:
    if conn.is_connected():
        cursor = conn.cursor()

        try:
            cursor.execute(create_table_sql)
            print("Table created")
        except Exception as e:
            print("Error creating table", e)
            exit()
        
        sale_id = 0
        #
        # (sale_id, product_id, customer_id, location_id, 
        # sale_date, quantity, total_amount) 
        #
        for i in range(number_of_rows):
            sale_id += 1 # sale_id as INT
            quantity, product_id, total_amount = get_quantity_and_product_id_and_total_price()
            customer_id = get_customer_id()
            location_id = get_location_id()
            sale_date = the_faker.date_between(start_date=start_date, end_date=end_date)
            
            sql_query = 'INSERT INTO sales_transactions (sale_id, product_id, customer_id, location_id, sale_date, quantity, total_amount) \
                VALUES (%d, %d, %d, %d, "%s", %d, %d); ' % (sale_id, product_id, customer_id, location_id, sale_date, quantity, total_amount)
            #
            # print("sql_query=", sql_query)
            #
            cursor.execute(sql_query)
            
            if sale_id % 1000 == 0:
                print("iteration %s" % sale_id)
                time.sleep(0.5)
                conn.commit()
            #end-if
        #end-for
except Error as e :
    print ("error: %s", e)
    pass
except Exception as e:
    print ("Unknown error: %s", e)
finally:
    #closing database connection.
    if(conn and conn.is_connected()):
        conn.commit()
        cursor.close()
        conn.close()