---
marp: true
theme: default
paginate: true
title: Medallion Data Architecture in Action
---

## 🟡 What is Medallion Data Architecture?
**Medallion Architecture** is a layered design 
for organizing data in a data warehouse:

> 🟫 Bronze → ⚪ Silver → 🟡 Gold
![](./images/medallion_architecture_0.webp)


	The medallion architecture is a Databricks
	conceptualized  data  design  pattern  for 
	lakehouse solutions, structuring data into 
	3 distinct zones
	
		Bronze (raw), 
		Silver (cleansed), and 
		Gold (curated)
	
	to incrementally improve data quality, 
	structure, and reliability. It focuses 
	on enabling ACID transactions, data lineage, 
	and efficient ELT processing, making data 
	suitable for BI, AI, and analytics.


### 🎯 Purpose
- Transform **raw data → trusted insights**
- Separate **data quality stages**
- Support **business analytics at scale**

### 💼 Why it matters (Business View)
- Data is **messy at ingestion**
- Analytics requires **clean, validated data**
- Enables **trust in reports and dashboards**

---

## Core Medallion Architecture Layers

### 1. 🟫 Bronze Layer (Raw Data): 
	The landing zone for data in its native 
	format, often from  streaming  or batch 
	sources. It serves as the single source 
	of truth, retaining full historical data 
	(immutable) for reprocessing needs.

### 2. ⚪ Silver Layer (Cleaned & Validated): 
	Data is transformed from Bronze, involving 
	cleansing, schema enforcement, deduplication, 
	and conformance. It provides an enterprise-wide 
	view of data entities, often modeled using 
	Data Vault techniques.
	
### 3. 🟡 Gold Layer (Curated Business Data): 
	Final analytics-ready data modeled for 
	business requirements (e.g., star schema, 
	dimensional modeling).   This layer  is 
	optimized for high-performance reporting, 
	BI, and machine learning, featuring heavy 
	aggregation.
	 
---

## 🔄 Medallion Architecture Flow

Raw Data (CSV / API / Logs)  <br>
⬇  
🟫 **Bronze — Raw Layer**
- Data stored *as-is*
- Minimal transformation
- Full traceability <br>
⬇  
⚪ **Silver — Clean Layer**
- Apply business rules
- Remove invalid records
- Standardize formats <br>
⬇  
🟡 **Gold — Analytics Layer**
- Star schema (fact + dimensions)
- Optimized for queries
- Used by BI tools <br>
⬇  
📊 **Dashboards & Business Decisions**

---

## 📊 Example + Key Takeaways

### 🔍 Example (Sales Dataset)
**Bronze**
- `sale_id = NULL`  
- `product = "TV"`  
- `sale_date = "2025-99-99"` <br>
⬇  
**Silver**
- invalid date → ❌ dropped  
- `sale_id NULL` → ⚠️ cancelled  
⬇  
**Gold**
- only valid transactions remain  
- ready for analytics  

---

### 🧠 Key Takeaways 1
- Data is **not analytics-ready at ingestion**
- Cleaning happens in **structured layers**
- Gold layer delivers **business value**
---

### 📘 Key Takeaways 2
Medallion architecture is a layered data design where data flows  
from raw (Bronze) → cleaned (Silver) → business-ready (Gold),  
ensuring **data quality, traceability, and reliable analytics**.

---

## Why Medallion Architecture Matters

### Data Quality Assurance: 
	Ensures data accuracy and consistency at each step, 
	enabling easier troubleshooting.

### Reusability: 
	Provides a consistent "single source of truth" 
	(Silver) for multiple reporting use cases (Gold).
	
### Compliance: 
	Facilitates compliance because raw data is preserved 
	and easily audited.


### Content of this folder

1. [`Medallion_Architecture_Introduction.md`](./Medallion_Architecture_Introduction.md)

2. [`book_seller_clean_data`: A Complete Example on a Clean data](./book_seller_clean_data)

3. [`book_seller_messy_data`: A Complete Example on a Messy data](./book_seller_messy_data)

4. [`sales_1200_clean_records`: A Complete Example on a Clean data](./sales_1200_clean_records)

5. [`sales_1400_messy_records`: A Complete Example on a Messy data](./sales_1400_messy_records)
