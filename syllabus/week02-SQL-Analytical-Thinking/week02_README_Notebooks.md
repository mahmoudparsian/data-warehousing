Given the following data:

% head insurance
head: insurance: No such file or directory
example_1_insurance (main *) % head insurance.csv
age,gender,bmi,children,smoker,region,charges
19,female,27.9,0,yes,southwest,16884.924
18,male,33.77,1,no,southeast,1725.5523
28,male,33,3,no,southeast,4449.462
33,male,22.705,0,no,northwest,21984.47061
32,male,28.88,0,no,northwest,3866.8552
31,female,25.74,0,no,southeast,3756.6216
46,female,33.44,1,no,southeast,8240.5896
37,female,27.74,3,no,northwest,7281.5056
37,male,29.83,2,no,northeast,6406.4107


Create a Jupyter notebook with the following cells:
For each Cell: 
   a. NL Query
   b. SQL Query
   c. very nice plot (select the best plotting)
   d. what is the business insight?

1. create a duckdb connection

2. read insurance.csv and create a table called insurance

3. write query for top 3 per region

4. Compare to Regional Average

5. Above-Average Customers

6. % of Total Contribution

7. Running Total by Age

8. Do smokers pay more for insurance?

9. Does BMI impact insurance charges

10. Are smokers related to high BMI?

======

This is a great exam-quality + teaching-quality notebook design. I’ll give you a clean, modular Jupyter notebook (DuckDB + Pandas + Matplotlib) with:
	•	✅ NL Query
	•	✅ SQL Query
	•	✅ Plot (well chosen per question)
	•	✅ Business Insight

You can copy-paste directly into a notebook.

⸻

📓 Jupyter Notebook: Insurance Data Analytics (DuckDB)

⸻

🧱 Cell 1 — Create DuckDB Connection

# NL Query:
# Create a connection to DuckDB for in-memory analytics

import duckdb
import pandas as pd
import matplotlib.pyplot as plt

con = duckdb.connect(database=':memory:')

Business Insight:
We are setting up an in-memory analytical engine (DuckDB), ideal for fast OLAP-style queries.

⸻

📥 Cell 2 — Load CSV into DuckDB

# NL Query:
# Load insurance.csv into a DuckDB table called 'insurance'

con.execute("""
CREATE OR REPLACE TABLE insurance AS
SELECT *
FROM read_csv_auto('insurance.csv');
""")

con.execute("SELECT COUNT(*) FROM insurance").df()

Business Insight:
We now have structured data ready for analytical SQL queries.

⸻

🏆 Cell 3 — Top 3 Charges per Region

# NL Query:
# Find top 3 highest charges per region

query = """
SELECT *
FROM (
    SELECT 
        region,
        age,
        charges,
        RANK() OVER (PARTITION BY region ORDER BY charges DESC) AS rnk
    FROM insurance
) t
WHERE rnk <= 3
ORDER BY region, charges DESC;
"""

df = con.execute(query).df()
df

# Plot
plt.figure(figsize=(10,5))
for region in df['region'].unique():
    subset = df[df['region'] == region]
    plt.bar(subset['region'] + "_" + subset['age'].astype(str), subset['charges'], label=region)

plt.xticks(rotation=45)
plt.title("Top 3 Charges per Region")
plt.ylabel("Charges")
plt.tight_layout()
plt.show()

Business Insight:
High-cost customers cluster differently across regions—useful for regional pricing strategies.

⸻

📊 Cell 4 — Compare to Regional Average

# NL Query:
# Compare each customer's charge to their regional average

query = """
SELECT 
    region,
    age,
    charges,
    AVG(charges) OVER (PARTITION BY region) AS regional_avg
FROM insurance;
"""

df = con.execute(query).df()
df.head()

# Plot
plt.figure(figsize=(8,5))
plt.scatter(df['regional_avg'], df['charges'], alpha=0.5)
plt.xlabel("Regional Average")
plt.ylabel("Customer Charges")
plt.title("Customer vs Regional Average")
plt.tight_layout()
plt.show()

Business Insight:
Identifies customers significantly above average → potential risk group.

⸻

🚨 Cell 5 — Above-Average Customers

# NL Query:
# Find customers whose charges exceed their regional average

query = """
SELECT *
FROM (
    SELECT 
        *,
        AVG(charges) OVER (PARTITION BY region) AS regional_avg
    FROM insurance
) t
WHERE charges > regional_avg;
"""

df = con.execute(query).df()
df.head()

# Plot
plt.hist(df['charges'], bins=30)
plt.title("Above-Average Customer Charges")
plt.xlabel("Charges")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

Business Insight:
These customers drive disproportionate cost → key for insurance risk modeling.

⸻

📈 Cell 6 — % of Total Contribution

# NL Query:
# Compute each customer's percentage contribution to total charges

query = """
SELECT 
    age,
    charges,
    charges * 100.0 / SUM(charges) OVER () AS pct_total
FROM insurance
ORDER BY pct_total DESC;
"""

df = con.execute(query).df()
df.head()

# Plot (Top contributors)
top = df.head(20)

plt.figure(figsize=(10,5))
plt.bar(range(len(top)), top['pct_total'])
plt.title("Top 20 % Contribution")
plt.xlabel("Customers")
plt.ylabel("% Contribution")
plt.tight_layout()
plt.show()

Business Insight:
A small number of customers contribute heavily → classic Pareto effect.

⸻

📉 Cell 7 — Running Total by Age

# NL Query:
# Compute cumulative charges ordered by age

query = """
SELECT 
    age,
    SUM(charges) AS total_charges,
    SUM(SUM(charges)) OVER (ORDER BY age) AS running_total
FROM insurance
GROUP BY age
ORDER BY age;
"""

df = con.execute(query).df()
df.head()

# Plot
plt.figure(figsize=(10,5))
plt.plot(df['age'], df['running_total'], marker='o')
plt.title("Running Total of Charges by Age")
plt.xlabel("Age")
plt.ylabel("Running Total")
plt.grid()
plt.tight_layout()
plt.show()

Business Insight:
Costs accumulate with age → strong signal for actuarial pricing.

⸻

🚬 Cell 8 — Do Smokers Pay More?

# NL Query:
# Compare average charges between smokers and non-smokers

query = """
SELECT 
    smoker,
    AVG(charges) AS avg_charges
FROM insurance
GROUP BY smoker;
"""

df = con.execute(query).df()
df

# Plot
plt.figure(figsize=(6,4))
plt.bar(df['smoker'], df['avg_charges'])
plt.title("Average Charges: Smokers vs Non-Smokers")
plt.ylabel("Charges")
plt.tight_layout()
plt.show()

Business Insight:
Smokers typically pay significantly more → strong risk factor.

⸻

⚖️ Cell 9 — Does BMI Impact Charges?

# NL Query:
# Analyze relationship between BMI and charges

query = """
SELECT bmi, charges
FROM insurance;
"""

df = con.execute(query).df()

# Plot
plt.figure(figsize=(8,5))
plt.scatter(df['bmi'], df['charges'], alpha=0.5)
plt.title("BMI vs Charges")
plt.xlabel("BMI")
plt.ylabel("Charges")
plt.tight_layout()
plt.show()

Business Insight:
Higher BMI tends to correlate with higher charges → health risk indicator.

⸻

🔥 Cell 10 — Are Smokers Related to High BMI?

# NL Query:
# Compare BMI distribution for smokers vs non-smokers

query = """
SELECT smoker, bmi
FROM insurance;
"""

df = con.execute(query).df()

# Plot
for label in df['smoker'].unique():
    subset = df[df['smoker'] == label]
    plt.hist(subset['bmi'], bins=30, alpha=0.5, label=label)

plt.legend()
plt.title("BMI Distribution: Smokers vs Non-Smokers")
plt.xlabel("BMI")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

Business Insight:
If smokers skew toward higher BMI → compounded health risk.

⸻

✅ Summary (Teaching Value)

This notebook teaches:
	•	Window functions (RANK, AVG OVER, SUM OVER)
	•	Analytical thinking (comparison, contribution, trends)
	•	Data storytelling with plots
	•	Real-world insurance insights

⸻

If you want next step, I can:

✅ Turn this into MD/MARP slides
✅ Create Student vs Instructor versions
✅ Add grading rubric + expected outputs
✅ Convert into a final exam module
