---
marp: true
theme: default
paginate: true
size: 16:9
title: White House Visitor Logs - Data Story and Medallion Architecture with DuckDB
---

# White House Visitor Logs
## Data Story, Log Analysis, and Medallion Architecture with DuckDB

**Teaching use case:** demo for data warehousing  
**Dataset:** White House Visitor Records (Obama White House archive)  
**Analytic style:** raw logs -> Bronze -> Silver -> Gold

---

# Why this dataset is interesting

This dataset is a strong teaching example because it is:

- **real-world**
- **large enough to feel serious**
- **messy enough to justify cleaning**
- **simple enough to explain in one course module**

It behaves like an operational log release, not like a pre-built warehouse.

---

# What the source represents

The archive describes these records as **White House visitor records** released as part of a transparency initiative.

The metadata file explains fields such as:

- `UIN` = appointment number
- `BDGNBR` = badge number
- `ACCESS_TYPE` = access type
- `APPT_START_DATE` = scheduled appointment start
- `APPT_END_DATE` = scheduled appointment end
- `Total_People` = total people scheduled
- `visitee_*` = person being visited
- `MEETING_LOC` / `MEETING_ROOM` = where the meeting was scheduled

---

# What kind of data is this?

This is best understood as a **log-style operational dataset**.

It contains:

- people
- timestamps
- locations
- scheduling information
- release information
- process fields from the source system

This is not yet a clean dimensional model.

---

# Why log files matter in data warehousing

Log-style data is a perfect starting point for warehousing because it shows the gap between:

- **raw operational capture**
- **clean analytical modeling**

Students learn that data warehouses are not born clean.
They are engineered.

---

# The core teaching challenge

A raw file like this raises immediate questions:

- Which columns are essential?
- Which timestamps should we trust?
- Are there duplicates?
- What do null-heavy columns mean?
- How do we treat missing visitor or visitee identity?
- Which fields belong in the final warehouse?

These questions motivate architecture.

---

# Why DuckDB for this demo?

DuckDB is ideal because it lets students:

- query a large CSV locally
- use SQL immediately
- aggregate fast on a laptop
- move naturally from file -> table -> warehouse

DuckDB keeps the focus on **modeling and analysis**, not cluster setup.

---

# Overall architecture

```text
Raw CSV
  -> Bronze
  -> Silver
  -> Gold
  -> OLAP analysis
```

This is the essence of the **Medallion Architecture**:

- **Bronze** = preserve the source
- **Silver** = improve trust and usability
- **Gold** = organize for business insight

---

# Bronze: what it means

Bronze is the **landing zone of truth**.

We keep:

- all rows
- all columns
- raw names
- raw timestamps
- raw quality problems

Bronze is not for elegant reporting.
Bronze is for fidelity, lineage, and recovery.

---

# Bronze questions we ask

At Bronze, we do not clean first.
We inspect first.

Typical questions:

- How many rows?
- What are the columns?
- Which columns are sparse?
- Are there exact duplicates?
- Are timestamps text or typed values?
- How much identity is missing?

Bronze is where evidence begins.

---

# EDA as the bridge to architecture

EDA is not separate from warehousing.
EDA tells us **why Silver rules are needed**.

Examples:

- null-heavy columns justify narrowing the Silver schema
- duplicate checks justify deduplication rules
- missing visitor/visitee identity justifies audit tables
- time analysis justifies a date dimension

EDA creates design intelligence.

---

# Silver: what it means

Silver is the **trusted operational layer**.

Here we:

- remove exact duplicates
- standardize names
- parse dates and times
- derive behavioral features
- quarantine problematic rows
- keep only analytically useful fields

Silver answers:
**What is usable and trustworthy?**

---

# Why we do not delete bad rows blindly

A good pipeline does not hide data quality problems.

Best practice:

- preserve everything in Bronze
- place problematic rows into Silver audit/quarantine tables
- exclude them from the main Gold fact table when necessary

This teaches transparency and reversibility.

---

# About missing visitor / visitee identity

For a **behavioral warehouse**, rows missing a visitor or visitee are difficult to interpret.

So the right teaching pattern is:

- keep them in Bronze
- flag them in Silver
- quarantine them for audit
- build Gold from rows that support the analysis goal

This is more honest than silent deletion.

---

# About special symbols such as "/"

Sometimes raw data includes codes or placeholders.

Even if we suspect a meaning, we should not convert them to a strong business label without documentation.

So in this demo we treat `"/"` as:

- a special unresolved value
- something to flag
- something to preserve for audit

That is good warehouse discipline.

---

# Silver output for this demo

Our Silver layer creates a clean visit table with:

- standardized visitor full name
- standardized visitee full name
- standardized meeting location
- parsed appointment timestamps
- visit date
- visit hour
- cancellation flag
- scheduled duration
- total people

Now the data is much more usable.

---

# Gold: what it means

Gold is the **business-facing warehouse layer**.

We build:

- `dim_visitor`
- `dim_visitee`
- `dim_location`
- `dim_date`
- `fact_visit_behavior`

This is where the architecture becomes recognizably data warehousing.

---

# Why dimensions matter

Dimensions provide meaning and stability.

They answer:

- who?
- where?
- when?

The fact table answers:

- how many?
- how big?
- how long?
- canceled or not?

Together they make OLAP easy.

---

# Why a fact table matters

The fact table gives us a clear grain:

**one cleaned visit row = one fact row**

From there, students can write queries like:

- top 10 visitors
- top 10 visitees
- top 10 visitor-visitee pairs
- visits by location
- visits by month
- cancellation rate by location

The warehouse makes these simple.

---

# Example business questions

After Gold is built, we can ask:

- Who visits most often?
- Who receives the most visits?
- Which relationships repeat most?
- Which buildings receive the most activity?
- When is activity highest?
- Which areas have larger group visits?
- Where are cancellation rates higher?

This is the payoff of Medallion Architecture.

---

# Why this is a behavioral analytics warehouse

The final Gold model is not about money or sales.
It is about **behavioral patterns in visit activity**.

It tracks:

- frequency
- relationships
- time rhythms
- location patterns
- process outcomes
- group size

So the warehouse is best described as a **behavioral analytics warehouse** built from visitor logs.

---

# What students learn from this project

Students learn that warehousing is not just table creation.

They learn:

- profiling
- cleaning
- trust-building
- dimensional design
- grain
- measures
- analytical SQL
- business interpretation

This is a full mini data engineering + warehousing case study.

---

# Suggested teaching flow

1. Start with the raw CSV and metadata  
2. Run EDA to expose data quality and structure  
3. Explain Bronze as preserved truth  
4. Explain Silver as trusted operational data  
5. Build Gold dimensions and fact  
6. Run OLAP queries for insight  
7. Discuss design tradeoffs and limitations  

---

# Final message

This project shows a complete story:

**log files -> evidence -> cleaning -> modeling -> insight**

With DuckDB and Medallion Architecture, students can see how a messy real-world file becomes a usable warehouse.

That is the core lesson of modern data warehousing.

---

# Deliverables in this teaching package

- **EDA notebook** (`.ipynb`)
- **Medallion Architecture notebook** (`.ipynb`)
- **Data story slides** (`.md / Marp`)

These three artifacts work together:

- story first
- evidence second
- architecture third
