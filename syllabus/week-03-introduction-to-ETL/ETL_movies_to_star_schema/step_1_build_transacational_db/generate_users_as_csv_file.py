# using python, create a list of 100,000 users 
# with 2 columns: 
#                user_id (as an integer), 
#                user_name (as a string). 
#
# Then write  it to a CSV file.

# Here's how you can create a list of 100,000 
# users with user_id as integers and user_name 
# as strings, and then save this data 
# into a CSV file using Python:

import csv

# Step 1: Create the list of 100,000 users
users = []
for user_id in range(1, 100001):  # User IDs from 1 to 100,000
    user_name = f"user_{user_id}"  # Generate user names dynamically
    users.append({"user_id": user_id, "user_name": user_name})  # Add to the list

# Step 2: Write the list to a CSV file
with open("users.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["user_id", "user_name"])
    writer.writeheader()  # Write column headers
    writer.writerows(users)  # Write rows of data

print("CSV file 'users.csv' created successfully!")
