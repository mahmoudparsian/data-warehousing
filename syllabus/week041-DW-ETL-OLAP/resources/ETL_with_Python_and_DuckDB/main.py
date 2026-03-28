import duckdb
from duckdb import DuckDBPyConnection
import os
import logging
import sys

#---------------------------------------------------------------------
# Source:
# 
# This ETL program is copied from the following source:
#     * URL: https://github.com/InosRahul/DuckDB-ETL-Example 
#     * Author: Rahul Soni
#
# Modified by Mahmoud Parsian (for educational purposes)
#     * Parametrized arguments passed by command line
#     * Added more documentation and comments
#----------------------------------------------------------------------

#----------------------
# Configure logging ...
#----------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


CREATE_TABLE_VEHICLES = """
        DROP TABLE IF EXISTS vehicles CASCADE;
        CREATE TABLE vehicles (
            VIN VARCHAR(10),
            County VARCHAR,
            City VARCHAR,
            State VARCHAR(2),
            Postal_Code VARCHAR(10),
            Model_Year INTEGER,
            Make VARCHAR,
            Model VARCHAR,
            Electric_Vehicle_Type VARCHAR,
            CAFV_Eligibility VARCHAR,
            Electric_Range INTEGER,
            Base_MSRP DECIMAL,
            Legislative_District INTEGER,
            DOL_Vehicle_ID VARCHAR(15),
            Vehicle_Location VARCHAR,
            Electric_Utility VARCHAR,
            Census_Tract VARCHAR(11)
    );
"""

SELECT_ALL_VEHICLES = """
    SELECT * from vehicles
"""

DESCRIBE_VEHICLES = """
    DESCRIBE vehicles
"""

#----------------------------------------------------------------
# insert every row of a CSV file as a record in a database table
#----------------------------------------------------------------
def insert_data(cursor: DuckDBPyConnection, csv_file_path: str):
    logger.info("Data insertion started...")
    try:
        cursor.sql(
            f"INSERT INTO vehicles SELECT * FROM read_csv_auto('{csv_file_path}');"
        )
        cursor.commit()
        logger.info("Data insertion successful.")
    except Exception as e:
        logger.error(f"Failed to insert data: {str(e)}")


def count_cars_per_city(cursor: DuckDBPyConnection):
    cars_per_city_query = """
    SELECT city, COUNT(VIN) AS cars_in_city 
    FROM vehicles 
    GROUP BY city
    """

    try:
        cursor.execute(cars_per_city_query)
        results = cursor.fetchall()
        return results
    except Exception as e:
        logger.error(f"Failed to count cars per city: {str(e)}")
        return []


def find_top_three_popular_vehicles(cursor: DuckDBPyConnection):
    top_three_popular_vehicles_query = """
    SELECT CONCAT(make, ' ', model), 
    COUNT(VIN) as vehicle_count 
    FROM vehicles 
    GROUP BY make, model 
    ORDER BY vehicle_count DESC
    LIMIT 3
    """

    try:
        cursor.execute(top_three_popular_vehicles_query)
        results = cursor.fetchall()
        return results
    except Exception as e:
        logger.error(f"Failed to find top three popular vehicles: {str(e)}")
        return []


def find_most_popular_vehicle_by_postal_code(cursor: DuckDBPyConnection):
    most_popular_vehicle_by_postal_code_query = """
    SELECT CONCAT(t1.make, ' ', t1.model),
    t1.postal_code
    FROM (
        SELECT model, make, postal_code, COUNT(vin) as vehicle_count,
        ROW_NUMBER() OVER(PARTITION BY postal_code ORDER BY COUNT(vin) DESC) as rank
        FROM vehicles
        GROUP BY postal_code, model, make
    ) t1
    WHERE t1.rank = 1
    """

    try:
        cursor.execute(most_popular_vehicle_by_postal_code_query)
        results = cursor.fetchall()
        return results
    except Exception as e:
        logger.error(f"Failed to find most popular vehicle by postal code: {str(e)}")
        return []


def count_cars_by_model_year(cursor: DuckDBPyConnection):
    count_cars_by_model_year_query = """
    SELECT model_year, COUNT(vin) as num_cars_year
    FROM vehicles
    GROUP BY model_year
    """

    try:
        cursor.execute(count_cars_by_model_year_query)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        logger.error(f"Failed to count cars by model year: {str(e)}")
        return []

#-----------------------------
# Create output per year ...
#-----------------------------
def create_output_data(rows, output_dir: str):
    
    # create needed directories
    os.makedirs(output_dir, exist_ok=True)

    for row in rows:
        year, count = row
        year_dir = os.path.join(output_dir, str(year))
        os.makedirs(year_dir, exist_ok=True)
        file_path = os.path.join(year_dir, f"{year}.txt")

        try:
            with open(file_path, "w") as file:
                file.write(f"Count: {count}")
            logger.info(f"File saved: {file_path}")
        except Exception as e:
            logger.error(f"Failed to save file: {str(e)}")
        #end-try
    #end-for
#end-def


#------------------
# main driver  ...
#------------------
def main(input_path_as_csv: str, duckdb_database_name: str, output_dir: str):

    # create a database connection object
    conn = duckdb.connect(database=duckdb_database_name)

    # conn.cursor() returns a copy of the DuckDB connection, 
    # with a reference to the existing DuckDB database instance.
    cursor = conn.cursor()

    # Create vehicles table
    try:
        cursor.execute(CREATE_TABLE_VEHICLES)
        logger.info("Vehicles table created.")
    except Exception as e:
        logger.error(f"Failed to create vehicles table: {str(e)}")
        conn.close()
        return

    # Insert data into the table
    insert_data(cursor, input_path_as_csv)

    # Perform data analysis
    cars_per_city = count_cars_per_city(cursor)
    logger.info(f"Cars per city: {cars_per_city}")

    top_three_popular_vehicles = find_top_three_popular_vehicles(cursor)
    logger.info(f"Top three popular vehicles: {top_three_popular_vehicles}")

    most_popular_vehicle_by_postal_code = find_most_popular_vehicle_by_postal_code(cursor)
    logger.info(f"Most popular vehicle by postal code: {most_popular_vehicle_by_postal_code}")

    rows = count_cars_by_model_year(cursor)

    # create output: one folder per year
    create_output_data(rows, output_dir)

    conn.close()
#end-def

if __name__ == "__main__":

    input_path_as_csv = sys.argv[1]
    # input_path_as_csv = "Electric_Vehicle_Population_Data.csv"
    print("input_path_as_csv=", input_path_as_csv)

    duckdb_database_name = sys.argv[2]
    # duckdb_database_name = "electric_vehicles_data"
    print("duckdb_database_name=", duckdb_database_name)
    
    output_dir = sys.argv[3]
    # output_dir = "/tmp/data/results"
    print("output_dir=", output_dir)
        
    main(input_path_as_csv, duckdb_database_name, output_dir)
