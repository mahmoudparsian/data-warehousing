# Week 4 Lab — Student Version
## ETL, OLAP, and Medallion Architecture

## 1) Lab Overview

This lab is designed to help you connect four important ideas:

- raw data is not ready for analytics
- ETL and ELT pipelines improve trust and usability
- Medallion architecture organizes data into meaningful layers
- OLAP queries help transform curated data into business insight

By the end of this lab, you should be able to:

- explain the purpose of Bronze, Silver, and Gold layers
- write SQL to clean and transform messy raw data
- create business-ready aggregate tables
- use OLAP-style queries to answer business questions
- explain results in clear business language

---

## 2) Business Scenario

Assume you work for a retail company.

The company receives transaction data from multiple sources:
- CSV files
- exports from operational systems
- manually entered records
- partner systems

The business leadership wants trustworthy answers to questions such as:

- What is revenue by region?
- Which products or categories perform best?
- Are there bad records affecting our reporting?
- How do we move from raw operational data to dashboard-ready metrics?

Your job is to design a simple pipeline that turns messy raw data into trusted business insight.

---

## 3) Big Ideas from Week 4

### ETL
ETL stands for:
- Extract
- Transform
- Load

It describes how data moves from source systems into analytical systems.

### OLAP
OLAP stands for Online Analytical Processing.

It focuses on:
- aggregations
- multi-dimensional analysis
- fast analytical queries

### Medallion
Medallion architecture organizes data into three layers:

- **Bronze** = raw data
- **Silver** = cleaned and validated data
- **Gold** = curated business-ready metrics

---

## 4) Before You Start

For every task in this lab, do all of the following:

1. Read the business question.
2. Identify which layer the task belongs to:
   - Bronze
   - Silver
   - Gold
3. Decide whether the task is:
   - raw inspection
   - cleaning / transformation
   - aggregation / analysis
4. Write the SQL.
5. Explain the business meaning in plain English.

The goal is not only to write correct SQL.

The goal is to answer:

> Why does this result matter to the business?

---

# Part A — Bronze Layer

## Task 1 — Inspect the Raw Data

### Business Question
What does the raw data look like before any cleaning?

### Why this matters
Before changing anything, analysts must understand:
- what columns exist
- what values look suspicious
- what kinds of quality issues appear

### Your task
Write a query that shows the raw rows from the Bronze table.

### Reflection
After running your query, answer:

- What inconsistencies do you see?
- Which columns look messy?
- Why should you never build dashboards directly from Bronze?

---

## Task 2 — Count Raw Rows

### Business Question
How many rows entered the pipeline at the Bronze stage?

### Why this matters
Row counts are basic but very important:
- validate ingestion
- detect missing files
- support pipeline monitoring

### Your task
Write a query to count all rows in the Bronze table.

### Reflection
After running your query, answer:

- Why are row counts one of the first validation checks?
- Why should Bronze row counts be preserved and monitored?
- How could this help in debugging?

---

## Task 3 — Identify Potentially Bad Numeric Values

### Business Question
Which Bronze rows have values that may not convert to numeric correctly?

### Why this matters
Many raw pipelines fail because numeric fields are stored as text and may contain:
- extra characters
- words like `ERROR`
- empty strings

### Your task
Write a query or analysis pattern that helps identify suspicious `amount` values.

### Reflection
After running your logic, answer:

- Why is type conversion a major ETL challenge?
- What happens if bad numeric values are ignored?
- Should they be fixed, flagged, or removed?

---

# Part B — Silver Layer

## Task 4 — Standardize Region Values

### Business Question
How can we make region values consistent?

### Why this matters
If raw data contains:
- `West`
- `west`
- `West `
- ` WEST`

then grouping by region will produce incorrect results.

### Your task
Write a transformation that:
- removes extra spaces
- converts the text to lowercase

### Hint
Think of:
- `TRIM`
- `LOWER`

### Reflection
After running your query, answer:

- Why does text normalization matter?
- How could inconsistent region values break a report?
- Why is this a Silver-layer responsibility?

---

## Task 5 — Convert Amount to Numeric

### Business Question
How do we safely convert a raw amount column into a real numeric field?

### Why this matters
Analytical queries depend on numeric measures.  
If amount stays as text, then:
- sums may fail
- averages may fail
- validation becomes difficult

### Your task
Write SQL that converts `amount` into a numeric type safely.

### Hint
Use a safe cast approach where possible.

### Reflection
After running your query, answer:

- Why is safe conversion important?
- What should happen to rows that fail conversion?
- Why is this not a Gold-layer task?

---

## Task 6 — Create the Silver Table

### Business Question
How do we build a trusted cleaned layer from Bronze?

### Why this matters
Silver is where we:
- standardize values
- convert types
- remove clearly bad rows
- prepare data for analytical use

### Your task
Create a Silver table that:
- keeps valid rows
- standardizes region
- converts amount to numeric

### Reflection
After creating Silver, answer:

- What changed from Bronze to Silver?
- Which rows were removed or corrected?
- Why does Silver improve trust?

---

## Task 7 — Validate Silver Row Count

### Business Question
How many rows remain after cleaning?

### Why this matters
Cleaning often changes row counts.  
We need to know:
- how many rows survived
- whether too many rows were lost
- whether cleaning rules were too aggressive

### Your task
Count rows in Silver and compare them conceptually with Bronze.

### Reflection
After running your query, answer:

- Is row loss expected here?
- When should row loss become a warning sign?
- Why must row-count changes be explained?

---

## Task 8 — Check for Negative or Invalid Values

### Business Question
Are there still suspicious rows after cleaning?

### Why this matters
Silver should be trusted, but trust should be verified.

### Your task
Write a query to detect rows with:
- negative amounts
- null amounts
- any suspicious numerical values

### Reflection
After running your query, answer:

- Why should Silver still be validated after transformation?
- Why is validation a recurring process?
- What would you do if suspicious rows remain?

---

# Part C — Gold Layer

## Task 9 — Revenue by Region

### Business Question
What is total revenue by region?

### Why this matters
This is a classic business-facing metric:
- easy to explain
- useful for management
- a natural Gold table candidate

### Your task
Create a query that aggregates total revenue by region from Silver.

### Reflection
After running your query, answer:

- Which region performs best?
- Why is this a Gold-layer metric?
- Why should this not be computed directly from Bronze?

---

## Task 10 — Create the Gold Table

### Business Question
How do we store a curated business-ready metric table?

### Why this matters
Gold tables are built for:
- dashboards
- executives
- analysts
- repeatable reporting

### Your task
Create a Gold table with:
- region
- total revenue

### Reflection
After building the Gold table, answer:

- Why is the Gold table simpler than Bronze and Silver?
- Why are Gold tables often smaller?
- Who is the primary audience for Gold?

---

## Task 11 — Interpret the Gold Result

### Business Question
What does the Gold table tell the business?

### Why this matters
Analytical work is incomplete without interpretation.

### Your task
Write 3–5 sentences explaining:
- what the Gold table shows
- what the likely conclusion is
- what business action might follow

### Reflection
Your explanation should go beyond:
> “West is bigger than East.”

Try to explain:
- why the difference matters
- what leadership might do with the result
- what follow-up analysis could be useful

---

# Part D — OLAP Thinking

## Task 12 — Slice

### Business Question
How do we analyze just one region?

### Why this matters
Managers often want to focus on one segment at a time.

### Your task
Write a query that filters to one region only and summarizes revenue.

### Reflection
After running your query, answer:

- What does “slice” mean in OLAP?
- Why is narrowing scope useful?
- In what real business situation would this be used?

---

## Task 13 — Dice

### Business Question
How do we analyze data using more than one filtering condition?

### Why this matters
Real business questions are rarely one-dimensional.

### Your task
Write a query that uses multiple conditions to narrow the data.

Examples:
- one region and one amount threshold
- one region and a subset of rows

### Reflection
After running your query, answer:

- What makes this a dice-style analysis?
- Why is multi-condition analysis common?
- How does this improve business precision?

---

## Task 14 — Roll-Up

### Business Question
How would we conceptually move from detailed rows to a summarized business view?

### Why this matters
Roll-up is a core OLAP idea:
- detail becomes summary
- many rows become a KPI
- operational data becomes management information

### Your task
Use SQL to show a rolled-up view from detailed Silver rows into aggregated Gold-style output.

### Reflection
After running your query, answer:

- Why is roll-up important for management reporting?
- Why do leaders often prefer summaries over raw rows?
- What is lost and what is gained in a roll-up?

---

## Task 15 — Drill-Down

### Business Question
How would we move from a summary back to detailed supporting rows?

### Why this matters
A Gold metric can raise questions.  
Drill-down helps analysts investigate.

### Your task
Write a query that starts from the idea of a Gold metric and returns the detailed Silver rows behind it.

### Reflection
After running your query, answer:

- Why is drill-down important?
- Why should Gold metrics always be traceable back to Silver or Bronze?
- What business questions become possible after drill-down?

---

# Part E — Integrated Thinking

## Task 16 — Describe the Full Pipeline

### Business Question
How would you explain this pipeline to a manager?

### Your task
Write a short explanation of the end-to-end flow:

- Bronze
- Silver
- Gold

Your explanation should describe:
- what each layer contains
- why each layer exists
- who would use each layer

---

## Task 17 — ETL vs ELT

### Business Question
What is the difference between ETL and ELT, and why does it matter?

### Your task
Write a short explanation comparing:
- ETL
- ELT

### Reflection
Be sure to explain:
- where transformation happens
- why modern cloud systems often prefer ELT
- why both still require data quality logic

---

## Task 18 — Final Synthesis Question

### Business Question
Why should businesses invest in pipeline design and layered architecture instead of just running a few SQL queries directly on raw files?

### Your task
Write a thoughtful answer using ideas from:
- ETL
- OLAP
- Medallion architecture
- data trust
- business decisions

---

# Deliverables

Submit:

- your SQL queries
- your outputs or screenshots
- your written reflections

Remember:

> The purpose of this lab is not just to clean data.  
> The purpose is to explain how trustworthy data becomes business value.
