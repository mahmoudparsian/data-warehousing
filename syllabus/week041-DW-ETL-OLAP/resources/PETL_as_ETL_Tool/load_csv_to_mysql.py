"""
Install the required libraries:

pip install pandas 
pip install sqlalchemy 
pip install mysql-connector-python

"""
import sys
import pandas as pd
from sqlalchemy import create_engine

# Step 1: Read the CSV file using Pandas and create a DataFrame
csv_file = sys.argv[1]
df = pd.read_csv(csv_file)

# Step 2: Create a connection to the MySQL database
#engine = create_engine('mysql+mysqlconnector://username:password@localhost/mydatabase')
engine = create_engine('mysql+mysqlconnector://root:mp22pass@localhost/homeworks')

# Step 3: Load the data into the MySQL table
df.to_sql(name='my_table', con=engine, if_exists='append', index=False)

print("Data loaded successfully")
