#--------------------------------------------------------
# Let's walk through how to read this `insurance` data 
# into a pandas DataFrame and perform 8 insightful data 
# explorations using Python, including visualization with 
# `matplotlib` and `seaborn`.
#
# These analyses help uncover how features like smoking, age, 
# BMI, and number of children influence insurance charges.
#--------------------------------------------------------

### **Step 1: Load the data into a DataFrame**

#Assuming the data is in a CSV file named `insurance.csv`:

import sys
import pandas as pd

# Load the data from a command line:
#
# python3  sys.argv[0]                            sys.argv[1]
# python3  <name-of-python-program>               <csv-file-name>
# python3  data_exploration_of_insurance_data.py  insurance.csv

insurance_as_csv_file = sys.argv[1]
print("insurance_as_csv_file", insurance_as_csv_file)
# df = pd.read_csv('insurance.csv')
df = pd.read_csv(insurance_as_csv_file)

# Show the first few rows
print(df.head())


# ------------

### **Step 2: 8 Key Data Explorations with Visualizations**

# We'll use `seaborn` and `matplotlib` for plots.

import seaborn as sns
import matplotlib.pyplot as plt

# Set style
sns.set(style="whitegrid")


# -------------

#### **1. Distribution of Charges**

plt.figure(figsize=(8, 5))
sns.histplot(df['charges'], kde=True)
plt.title('Distribution of Insurance Charges')
plt.xlabel('Charges')
plt.ylabel('Frequency')
plt.show()

# --------------

#### **2. Charges by Smoking Status**

plt.figure(figsize=(8, 5))
sns.boxplot(x='smoker', y='charges', data=df)
plt.title('Charges vs Smoking Status')
plt.xlabel('Smoker')
plt.ylabel('Charges')
plt.show()

# ---------------

#### **3. Charges by Region**

plt.figure(figsize=(8, 5))
sns.boxplot(x='region', y='charges', data=df)
plt.title('Charges by Region')
plt.xlabel('Region')
plt.ylabel('Charges')
plt.show()

# ----------------

#### **4. BMI Distribution by Gender**

plt.figure(figsize=(8, 5))
sns.histplot(data=df, x='bmi', hue='gender', kde=True, element='step')
plt.title('BMI Distribution by Gender')
plt.xlabel('BMI')
plt.ylabel('Frequency')
plt.show()

# ---------------

#### **5. Age vs. Charges Scatter Plot (Colored by Smoking Status)**

plt.figure(figsize=(8, 5))
sns.scatterplot(x='age', y='charges', hue='smoker', data=df)
plt.title('Age vs Charges by Smoking Status')
plt.xlabel('Age')
plt.ylabel('Charges')
plt.show()

# ---------------

#### **6. Average Charges by Number of Children**

plt.figure(figsize=(8, 5))
sns.barplot(x='children', y='charges', data=df)
plt.title('Average Charges by Number of Children')
plt.xlabel('Children')
plt.ylabel('Average Charges')
plt.show()

# ----------------

#### **7. Correlation Heatmap**

plt.figure(figsize=(6, 4))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

# ----------------

#### **8. Charges by Gender and Smoking Status**

plt.figure(figsize=(8, 5))
sns.boxplot(x='gender', y='charges', hue='smoker', data=df)
plt.title('Charges by Gender and Smoking Status')
plt.xlabel('Gender')
plt.ylabel('Charges')
plt.show()

# -----------------

