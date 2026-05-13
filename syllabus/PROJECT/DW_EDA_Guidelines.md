# Exploratory Data Analysis (EDA) Guidelines for Data Warehousing

---

## 🎯 Purpose of EDA in Data Warehousing

Exploratory Data Analysis (EDA) in **data warehousing (DW)** serves a very different purpose than EDA in data science or machine learning.

In DW, EDA is used to:

- Understand the **business meaning** of data
- Identify the **grain** of source tables
- Discover **fact and dimension candidates**
- Detect **data quality issues** impacting ETL
- Justify the final **dimensional (star/snowflake) model**

> **EDA in DW exists to justify the dimensional model.**

---

## 1️⃣ Understand the Business Context

### Key Questions
- What business process does this data represent?
- What real-world event does a row capture?
- Who produces the data and why?

### Deliverable
- A short business description of the dataset
- Clear definition of the business process (e.g., sales, orders, claims, clicks)

---

## 2️⃣ Determine the Grain (Most Critical Step)

### Definition
> **Grain** describes what *one row* in the table represents.

### Questions to Answer
- One transaction? One item? One customer per day?
- Is the data atomic or already aggregated?

### Examples
- One row per order
- One row per product per order
- One row per customer per day

### Deliverable
- Explicit grain statement written in plain English

---

## 3️⃣ Identify Keys and Uniqueness

### Purpose
Understand how records are uniquely identified.

### Checks
- Natural primary keys
- Composite keys
- Duplicate records
- Missing or invalid keys

### DW Insight
- Natural keys help identify dimensions
- Surrogate keys will be introduced in the warehouse

---

## 4️⃣ Separate Facts from Descriptive Attributes

### Facts (Measures)
Characteristics:
- Numeric
- Aggregatable (SUM, COUNT, AVG)
- Represent business performance

Examples:
- Quantity
- Amount
- Duration
- Balance

### Descriptive Attributes
Characteristics:
- Textual or categorical
- Describe *who, what, where, when, how*

Examples:
- Customer name
- Product category
- Region
- Status

### Deliverable
- Clear classification of columns into facts vs attributes

---

## 5️⃣ Discover Dimension Candidates

### Purpose
Group descriptive attributes into logical entities.

### Common Dimension Types
- Date
- Time
- Customer
- Product
- Location
- Organization
- Channel

### EDA Tasks
- Group columns by business meaning
- Check cardinality (distinct counts)
- Identify attributes that may change over time (SCDs)

### Deliverable
- List of dimension candidates with source columns

---

## 6️⃣ Identify Fact Table(s)

### Purpose
Define measurable business events.

### Characteristics
- Contains foreign keys to dimensions
- Contains numeric measures
- Defined at a single grain

### EDA Questions
- How many fact tables are needed?
- Are there multiple business processes?
- Is the data transactional, snapshot, or accumulating snapshot?

---

## 7️⃣ Identify Degenerate Dimensions

### Definition
> Attributes that describe a transaction but do not deserve their own dimension table.

Examples:
- Invoice number
- Order number
- Payment method
- Status flags

### Deliverable
- List of degenerate dimensions to remain in fact tables

---

## 8️⃣ Analyze Time & Date Attributes

### Purpose
Time is central to analytics.

### EDA Tasks
- Identify all date/time columns
- Determine their roles (order date, ship date, event date)
- Decide which date dimensions are needed

### Deliverable
- Mapping of date/time columns to date/time dimensions

---

## 9️⃣ Data Quality Assessment

### Common Issues
- NULL or missing values
- Invalid numeric values
- Inconsistent text (CA vs California)
- Orphan records
- Duplicates

### DW Perspective
- Decide what to fix, default, reject, or flag during ETL

### Deliverable
- List of data quality issues and proposed handling rules

---

## 🔟 Cardinality & Volume Analysis

### Purpose
Anticipate performance and modeling challenges.

### Checks
- Row counts
- Distinct counts per dimension
- High vs low cardinality columns

### DW Insight
- High-cardinality attributes affect indexing and joins
- Low-cardinality attributes often stay in fact tables

---

## 1️⃣1️⃣ Validate Additivity of Measures

### Types of Measures
- Additive (sales amount)
- Semi-additive (account balance)
- Non-additive (ratios, percentages)

### Deliverable
- Classification of each measure’s additivity

---

## 1️⃣2️⃣ Prepare for ETL Decisions

### EDA Should Inform:
- Data cleaning rules
- Surrogate key generation
- Slowly changing dimension strategy
- Default and “unknown” dimension rows

---

## 1️⃣3️⃣ What EDA Is NOT in Data Warehousing

Avoid focusing on:
- Machine learning feature selection
- Correlation matrices
- Predictive modeling
- Heavy visualization without modeling purpose

EDA in DW is **structural and semantic**, not predictive.

---

## 📦 Final EDA Deliverables (DW-Oriented)

A complete DW EDA should produce:

1. Business process description
2. Explicit grain definition
3. Identified facts and measures
4. Dimension candidates and attributes
5. Degenerate dimensions
6. Data quality findings
7. ETL and modeling assumptions
8. Proposed dimensional schema

---

## 🧠 Key Takeaway

> EDA in data warehousing exists to   <br>
> understand structure, grain, facts, <br>
> dimensions, and data quality — so   <br>
> the dimensional model is correct and <br>
> defensible.
