# Example of financial data set, 
# 5 different data exploration/analysis) using pthon


"""
## **1️⃣ Sample Financial Dataset**
We’ll create a dataset containing **customer transactions** 
with the following columns:

- `Transaction_ID`: Unique ID for each transaction.
- `Customer_ID`: ID representing the customer.
- `Amount`: Transaction amount ($).
- `Transaction_Type`: Purchase or Refund.
- `Date`: Transaction date.

"""

### **Generating Sample Data**

import pandas as pd

# Sample dataset
data = {
    "Transaction_ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    "Customer_ID": ["C1", "C2", "C1", "C3", "C2", "C3", "C1", "C2", "C3", "C1", "C1", "C2", "C3", "C1"],
    "Amount": [120, -30, 200, 340, 150, -50, 180, 260, 390, -20, 90, 120, 300, -50],
    "Transaction_Type": ["Purchase", "Refund", "Purchase", "Purchase", "Purchase", "Refund", "Purchase", "Purchase", "Purchase", "Refund", "Purchase", "Purchase", "Purchase", "Refund"],
    "Date": pd.date_range(start="2025-04-01", periods=14, freq="D").astype(str)
}

# Create DataFrame
df = pd.DataFrame(data)

# Display dataset
print(df)



## **2️⃣ Data Exploration & Analysis**

### **1. Basic Summary & Statistics**
# Get an overview of the dataset, including column info and statistics.


# Check dataset structure
print(df.info())

# Summary statistics (mean, min, max, etc.)
print(df.describe())


### **2. Distribution of Transactions (Purchases vs Refunds)**
# Analyze the count of purchases versus refunds.


# Count transaction types
print(df["Transaction_Type"].value_counts())

# Visualizing transaction distribution
import matplotlib.pyplot as plt

df["Transaction_Type"].value_counts().plot(kind="bar", color=["blue", "red"])
plt.title("Transaction Type Distribution")
plt.xlabel("Transaction Type")
plt.ylabel("Count")
plt.show()


### **3. Customer Spending Analysis**
# Calculate the **total spending per customer**, ignoring refunds.

# Filter out refunds
valid_transactions = df[df["Amount"] > 0]

# Total spending per customer
customer_spending = valid_transactions.groupby("Customer_ID")["Amount"].sum()

print(customer_spending)


### **4. Time-Series Trend (Daily Transactions)**
# Analyze spending trends over time.


# Convert Date to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Group transactions by Date
daily_spending = df.groupby("Date")["Amount"].sum()

# Plot spending trends
daily_spending.plot(kind="line", marker="o", linestyle="-", color="green")
plt.title("Daily Spending Trends")
plt.xlabel("Date")
plt.ylabel("Total Amount ($)")
plt.xticks(rotation=45)
plt.show()


### **5. Identifying Outliers in Transactions**
# Detect unusually high or low transactions.

import seaborn as sns

# Box plot for transaction amounts
sns.boxplot(df["Amount"], color="orange")
plt.title("Transaction Amount Outliers")
plt.xlabel("Amount ($)")
plt.show()

