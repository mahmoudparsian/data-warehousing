# Pizza Shop Data Warehouse

Is this worth for my data warehousing class?

```
source of original data:
https://mavenanalytics.io/data-playground/pizza-place-sales
```


## Original Data Files

```
      16 data_dictionary.csv
   48621 order_details.csv
   21351 orders.csv
      33 pizza_types.csv
      97 pizzas.csv
   70118 total
```

## Data Dictionary and MetaData

```
% cat data_dictionary.csv
Table,Field,Description
orders,order_id,Unique identifier for each order placed by a table
orders,date,Date the order was placed (entered into the system prior to cooking & serving)
orders,time,Time the order was placed (entered into the system prior to cooking & serving)
order_details,order_details_id,"Unique identifier for each pizza placed within each order (pizzas of the same type and size are kept in the same row, and the quantity increases)"
order_details,order_id,Foreign key that ties the details in each order to the order itself
order_details,pizza_id,"Foreign key that ties the pizza ordered to its details, like size and price"
order_details,quantity,Quantity ordered for each pizza of the same type and size
pizzas,pizza_id,Unique identifier for each pizza (constituted by its type and size)
pizzas,pizza_type_id,Foreign key that ties each pizza to its broader pizza type
pizzas,size,"Size of the pizza (Small, Medium, Large, X Large, or XX Large)"
pizzas,price,Price of the pizza in USD
pizza_types,pizza_type_id,Unique identifier for each pizza type
pizza_types,name,Name of the pizza as shown in the menu
pizza_types,category,"Category that the pizza fall under in the menu (Classic, Chicken, Supreme, or Veggie)"
pizza_types,ingredients,"Comma-delimited ingredients used in the pizza as shown in the menu (they all include Mozzarella Cheese, even if not specified; and they all include Tomato Sauce, unless another sauce is specified)"
```

## fictitious pizza place

A year's worth of sales from a fictitious pizza place, 
including the date and time of each order and the pizzas 
served, with additional details on the type, size, quantity, price, and ingredients.

## Recommended Analysis

* How many customers do we have each day? 
Are there any peak hours?

* How many pizzas are typically in an order? 
Do we have any bestsellers?

* How much money did we make this year? 
Can we indentify any seasonality in the sales?

* Are there any pizzas we should take off the menu, 
or any promotions we could leverage?


## Pizza Orders. Is this worth for my data warehousing class?

Short answer: yes — this is an excellent dataset for a data warehousing class, especially at the undergraduate / early graduate level. In fact, it’s almost ideal for teaching both star schema design + medallion architecture + OLAP.

Let me give you a structured evaluation (and a few ways to elevate it to your teaching level).

⸻

✅ Why this dataset is strong

```
1. Clean, realistic transactional model

You naturally get a fact table + dimensions 
without forcing anything:
	•	Fact candidate
	•	order_details → grain = one pizza line per order
	•	Dimensions
	•	orders → date/time dimension
	•	pizzas → size + price
	•	pizza_types → category, ingredients

👉 This maps perfectly to a star schema exercise.
```
⸻

```
2. Perfect for teaching grain (very important concept)

Students often struggle with:

“What is the grain of my fact table?”

Here it is crystal clear:
	•	One row = one pizza type + size within an order

This allows you to explicitly teach:
	•	Wrong grain → duplicate counting
	•	Correct grain → proper aggregations
```
⸻

```
3. Natural OLAP queries (excellent for BI layer)

Your “Recommended Analysis” is basically a 
ready-made OLAP assignment:
	•	Peak hours → time dimension
	•	Bestsellers → product dimension
	•	Revenue → aggregation
	•	Seasonality → date hierarchy

👉 This is exactly what you want for:
	•	GROUP BY
	•	WINDOW functions
	•	Time-series analysis
```
⸻

```
4. Great size (not too small, not too big)
	•	~70K rows total
	•	Works perfectly in:
	•	DuckDB
	•	Jupyter notebooks
	•	Student laptops

👉 No infrastructure friction → big win for teaching.
```
⸻

⚠️ Limitations (and how to turn them into teaching moments)

```
1. No customer dimension

You don’t have:
	•	customer_id
	•	demographics

👉 Turn this into a design discussion:

“What would a real data warehouse include that 
this dataset is missing?”

You can even ask students to:
	•	simulate a customer dimension
	•	or discuss slowly changing dimensions (SCD)
```
⸻

```
2. No location / store dimension

Everything is from one pizza place.

👉 Opportunity:
	•	Ask students to extend:
	•	Add store_id
	•	Add city, region
```
⸻

```
3. Ingredients column is denormalized

ingredients = "Cheese, Tomato, Basil"

👉 GOLD opportunity to teach:
	•	Normalization vs denormalization
	•	Why BI systems often keep it as-is
	•	Or how to explode it into a bridge table
```
⸻

🏗️ How I would use this in your class (high-value structure)


Given your teaching style (medallion + star schema + SQL), 
this dataset fits perfectly:

⸻

# 🟫 Bronze Layer (raw ingestion)
```
CREATE TABLE bronze_orders AS SELECT * FROM read_csv_auto('orders.csv');
CREATE TABLE bronze_order_details AS SELECT * FROM read_csv_auto('order_details.csv');
CREATE TABLE bronze_pizzas AS SELECT * FROM read_csv_auto('pizzas.csv');
CREATE TABLE bronze_pizza_types AS SELECT * FROM read_csv_auto('pizza_types.csv');

👉 Teach:
	•	Raw ingestion
	•	Schema inference
	•	Data quality issues
```
⸻

# ⚪ Silver Layer (clean + join-ready)

```
CREATE TABLE silver_order_details AS
SELECT 
    od.order_details_id,
    od.order_id,
    od.pizza_id,
    od.quantity,
    o.date,
    o.time
FROM bronze_order_details od
JOIN bronze_orders o
  ON od.order_id = o.order_id;

👉 Teach:
	•	Joins
	•	Data cleaning
	•	Type casting
```
⸻

# 🟡 Gold Layer (star schema)

```
Fact table

CREATE TABLE fact_sales AS
SELECT
    od.order_details_id,
    od.order_id,
    p.pizza_type_id,
    p.size,
    pt.category,
    od.quantity,
    p.price,
    od.quantity * p.price AS sales_amount,
    o.date,
    o.time
FROM bronze_order_details od
JOIN bronze_orders o ON od.order_id = o.order_id
JOIN bronze_pizzas p ON od.pizza_id = p.pizza_id
JOIN bronze_pizza_types pt ON p.pizza_type_id = pt.pizza_type_id;
```

⸻

```
Dimensions (optional separation)
	•	dim_date
	•	dim_pizza
	•	dim_category

👉 Teach:
	•	Star schema vs flat table
	•	Fact vs dimension
```

⸻

📊 BI Layer (perfect for assignments)

```
Example 1: Peak hours

SELECT 
    EXTRACT(hour FROM time) AS hour,
    COUNT(DISTINCT order_id) AS num_orders
FROM fact_sales
GROUP BY hour
ORDER BY num_orders DESC;
```

⸻

```
Example 2: Best-selling pizzas

SELECT 
    name,
    SUM(quantity) AS total_sold
FROM fact_sales
GROUP BY name
ORDER BY total_sold DESC
LIMIT 10;
```


⸻

```
Example 3: Revenue over time

SELECT 
    date,
    SUM(sales_amount) AS revenue
FROM fact_sales
GROUP BY date
ORDER BY date;
```

⸻

🎯 Final verdict

```
👉 Strong YES — this is worth using

Even better:

This dataset supports ALL of your course goals:
	•	✔ Medallion architecture
	•	✔ Star schema design
	•	✔ OLAP queries
	•	✔ Visualization
	•	✔ SQL teaching (WHERE vs HAVING, GROUP BY, etc.)
```
⸻

🚀 Let's take it to “next level”

```
Since you like high-quality teaching materials, I can:
	•	✅ Turn this into a full Jupyter notebook (Bronze → Silver → Gold → BI)
	•	✅ Create 15–20 Marp slides (downloadable)
	•	✅ Add student + instructor assignments
	•	✅ Include advanced queries (window functions, ranking, cohort analysis)
```
# Additions to Data

OK, I have added the following 
3 records to pizza_types.csv

```
deep_dish,The Deep Dish Pizza,Supreme,"Mushrooms, Tomatoes, Red Peppers, Dried Tomatos, Red Onions, Spinach, Garlic"
detroit_style,The Detroit Style Pizza,Supreme, "Mushrooms, Tomatoes, Red Peppers, Red Onions, Spinach, Garlic, Basil"
margherita,Pizza Margherita,Veggie,"Mushrooms, Tomatoes, Red Onions, Garlic, Basil"
```
and have added the following 9 records to pizzas.csv

```
deep_dish_s,deep_dish,S,18
deep_dish_m,deep_dish,M,24
deep_dish_l,deep_dish,L,30
detroit_style_s,detroit_style,S,21
detroit_style_m,detroit_style,M,25
detroit_style_l,detroit_style,L,32
margherita_s,margherita,S,16
margherita_m,margherita,M,22
margherita_l,margherita,L,28
```

## New Data for 2016

``` 
Now, let's regenerate the files for 2016,
for new records in 2016, use the new ones 
(randomly) which I added now.

==============
Business requirements: 

1. orders*.csv
the date column can be in 2 different formats
2015-01-01 (as YYYY-MM-DD)
12/25/2015 (as MM/DD/YYYY)

we need to consolidate these into a uniform
valid date.

2. orders*.csv
If an oreder_id is missing (as NULL), 
then that record should be dropped,
because there will not be an entry 
in order_details*.csv


3. orders*.csv
Duplicate records must be dropped for our analysis.
Duplicate record means all fields are identical.

4. order_details_*.csv

4.1 Every record must have 4 fields/columns.
If there are not exactly 4 columns,
then that record must be dropped.

4.2 If any field/column is NULL/missing,
then that record must be dropped.

=====
This is very solid — you’re already thinking like a real data warehouse architect. 👍

But I’ll push you a bit to make this production-grade + pedagogically stronger.

⸻

🎯 Overall Assessment

✔ Good coverage of:
	•	Data cleaning
	•	Schema validation
	•	Referential thinking

⚠️ Missing:
	•	Business meaning
	•	Edge-case handling
	•	Validation rules beyond NULLs

👉 Right now: good Silver layer
👉 We’ll upgrade it to: excellent DW specification

⸻

🧠 Review + Improvements (by section)

⸻

✅ 1. orders*.csv — Date formats

Your requirement

Multiple formats → unify into valid date

✔ Correct
❗ But incomplete

⸻

🔥 Improve it

Add:

If date cannot be parsed → DROP the record

Revised version

The date column may contain multiple formats:
- YYYY-MM-DD
- MM/DD/YYYY

All dates must be converted to a valid DATE type (YYYY-MM-DD).

If a date cannot be parsed into a valid date, 
the record must be dropped.


⸻

🎓 Teaching value
	•	Introduces data type validation
	•	Not just formatting

⸻

✅ 2. Missing order_id

Your requirement

✔ Correct reasoning

⸻

🔥 Improve it

Be explicit:

If order_id is NULL or missing,
the record must be dropped,
because it cannot be joined with order_details.

👉 Add also:

order_id must be unique

⸻

⚠️ Add THIS (important)

order_id must be unique in orders.
If duplicates exist (same order_id with different values),
keep the most recent record or drop duplicates based on rule X.

👉 This is a real-world issue

⸻

✅ 3. Duplicate records

Your definition

✔ Good (exact match)

⸻

🔥 Improve it

Add:

Duplicate records are defined as rows where all fields are identical.
Such records must be removed.

Additionally, if multiple records share the same order_id 
but differ in other fields, this must be flagged as a data quality issue.

👉 This introduces:
	•	hard duplicates vs soft duplicates

⸻

⚠️ 4. order_details_*.csv — Needs strengthening

Your current version is too syntactic (column count, NULLs).

We need business + relational validation

⸻

✅ 4.1 Column count

✔ OK but weak in real DW

Improve:

Each record must contain exactly:
(order_details_id, order_id, pizza_id, quantity)

Records with missing or extra columns must be dropped.


⸻

✅ 4.2 NULL handling

✔ Good but incomplete

⸻

🔥 Add CRITICAL rules (missing right now)

⸻

🚨 4.3 Referential integrity (VERY IMPORTANT)

Every order_details.order_id must exist in orders.order_id.

If no matching order exists, the record must be dropped.

👉 This is core DW concept

⸻

🚨 4.4 Pizza validation

Every pizza_id must exist in pizzas.csv.

If not, the record must be dropped.


⸻

🚨 4.5 Quantity validation

quantity must be a positive integer (> 0).

If quantity <= 0 or invalid, the record must be dropped.


⸻

🚨 4.6 Primary key uniqueness

order_details_id must be unique.

Duplicate order_details_id values must be removed.


⸻

🚀 Final Upgraded Version (what I recommend you use)

Here’s your polished version:

⸻

📘 Orders Table Requirements

1. Date Standardization
The date column may contain multiple formats:
- YYYY-MM-DD
- MM/DD/YYYY

All dates must be converted to YYYY-MM-DD.
If a date cannot be parsed, the record must be dropped.

2. Missing order_id
If order_id is NULL or missing, the record must be dropped.

3. order_id Uniqueness
order_id must be unique.
Duplicate order_id values must be resolved or removed.

4. Duplicate Records
Records where all fields are identical must be removed.


⸻

📘 Order Details Requirements

1. Schema Validation
Each record must contain exactly 4 fields:
(order_details_id, order_id, pizza_id, quantity)

Invalid records must be dropped.

2. NULL Handling
If any field is NULL, the record must be dropped.

3. Referential Integrity (Orders)
order_id must exist in orders table.
Otherwise, drop the record.

4. Referential Integrity (Pizzas)
pizza_id must exist in pizzas table.
Otherwise, drop the record.

5. Quantity Validation
quantity must be a positive integer (> 0).
Invalid values must be dropped.

6. Primary Key Constraint
order_details_id must be unique.
Duplicate IDs must be removed.


⸻

🎯 Final Verdict

👉 Your original version: Very Good 
👉 After refinement: Excellent

⸻

🚀 Next Step (high value)

Now you are ready to:
	•	🟫 Define Bronze → Silver transformations
	•	🟡 Build Gold star schema
	•	📊 Create BI queries + assignments

⸻

If you want, I can turn this into:
	•	📘 2–3 Marp slides (very clean for teaching)
	•	🧪 DuckDB cleaning pipeline (SQL + Python)
	•	🎓 Student assignment (clean vs messy data)

====
Now , we have the following data:

pizza_sales  % ls -l
total 8928
-rw-r--r--@ 1 max  staff     1473 Sep 13  2022 data_dictionary.csv
-rw-r--r--@ 1 max  staff  1308417 Apr 19 21:48 order_details_2015.csv
-rw-r--r--@ 1 max  staff  1618618 Apr 19 21:50 order_details_2016.csv
-rw-r--r--@ 1 max  staff   566342 Apr 19 21:34 orders_2015.csv
-rw-r--r--@ 1 max  staff   674326 Apr 19 21:36 orders_2016.csv
-rw-r--r--@ 1 max  staff     4092 Apr 19 21:10 pizza_types.csv
-rw-r--r--@ 1 max  staff     3374 Apr 19 21:21 pizzas.csv

OKay, first define the project: 

📘 5–5 Marp slides (very clean for teaching)
Give a story for pizza shop 
and define our business requirements as detail as possible
and give this in a md/marp/downloadable file.

Once I review this document, then we will move forward
with a Jupyter/Notebook: 
raw -> bronze -> silver -> gold -> OLAP queries

🚀 Next Step:  we move to:

👉 Jupyter Notebook (full pipeline)
with:
	•	Bronze ingestion
	•	Silver cleaning (based on these rules)
	•	Gold star schema
	•	OLAP queries + visualization

First we  create a template for all cells: as detail as possible, then for each cell you will create :  1. why we are doing this step, 2. Impl. in Python+DuckDB, 3. Very Nice Plotting, 4. Business analysis.  The first cell should talk about medallion architecture (very very short). Try to avoid pandas as much as possible, focus is duckdb.

I created the notebook template here:

Download the Jupyter notebook template￼

A couple of notes before you review it:

	•	It is DuckDB-first and keeps Python mostly 
	  for orchestration and plotting.
	  
	•	Each major cell includes the four parts you 
	  asked for: why, implementation, plotting, 
	  and business analysis.
	  
	•	The Bronze ingestion uses DuckDB CSV loading 
	  patterns, and the Silver layer uses try_strptime 
	  for mixed date parsing; if your intentionally 
	  messy order_details files are malformed enough 
	  to break auto-ingestion, the Bronze ingestion 
	  cell is the one to tighten with CSV options 
	  like ignore_errors or related parsing controls.  ￼
