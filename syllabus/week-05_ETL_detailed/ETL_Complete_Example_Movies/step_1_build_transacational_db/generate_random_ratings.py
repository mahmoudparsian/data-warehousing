"""
produce a csv data (with 300 rows) with 5 columns:
column-1: a sequence number 1, 2, 3, ..., 300
column-2: a random integer in range of 1 to 44
column-3: a random integer in range of 101, 102, ..., 120
column-4: a random number in range of 4 to 10
column-5: a random data from 1/1/2022 to 12/31/2023

Sure! Below is a Python script that generates a CSV 
file with 300 rows and 5 columns as specified. The 
script uses the random module to generate random integers 
and the pandas library to handle the data and export it 
to a CSV file.

Please make sure you have pandas installed in your environment. 
You can install it using pip install pandas.

Explanation:
Sequence Number: A simple list of integers from 1 to 1000.
Random Integer (1 to 100): Generated using random.randint(1, 100).
Random Integer (101 to 140): Generated using random.randint(101, 140).
Random Number (4 to 10): Generated using random.randint(4, 10).
Random Date (1/1/2022 to 12/31/2023): A function random_date is used to 
generate a random date between the provided start and end dates.
To generate the CSV file, run the script in your Python environment. 
The resulting file random_data.csv will contain the requested data.


"""
import sys
import pandas as pd
import random
from datetime import datetime, timedelta

# Function to generate a random date between start_date and end_date
def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# Define the range for the random dates
start_date = datetime.strptime("2022-01-01", "%Y-%m-%d")
end_date = datetime.strptime("2023-12-31", "%Y-%m-%d")

number_of_ratings = int(sys.argv[1])
print("number_of_ratings=", number_of_ratings)

# Generate the data
data = {
    "rating_id": list(range(1, number_of_ratings+1)),
    "movie_id": [random.randint(1, 100) for _ in range(number_of_ratings)],
    "user_id": [random.randint(101, 140) for _ in range(number_of_ratings)],
    "rating": [random.randint(2, 10) for _ in range(number_of_ratings)],
    "rating_date": [random_date(start_date, end_date).strftime("%Y-%m-%d") for _ in range(number_of_ratings)]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Export to CSV
df.to_csv("random_data.csv", index=False)

print("CSV file 'random_data.csv' has been created with N rows and 5 columns.")

