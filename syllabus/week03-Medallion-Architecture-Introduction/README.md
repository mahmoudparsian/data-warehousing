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

### 🎯 Purpose
- Transform **raw data → trusted insights**
- Separate **data quality stages**
- Support **business analytics at scale**

### 💼 Why it matters (Business View)
- Data is **messy at ingestion**
- Analytics requires **clean, validated data**
- Enables **trust in reports and dashboards**

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

### Content of this folder

1. [`Medallion_Architecture_Introduction.md`](./Medallion_Architecture_Introduction.md)

2. [`book_seller_clean_data`: A Complete Example on a Clean data](./book_seller_clean_data)

3. [`book_seller_messy_data`: A Complete Example on a Messy data](./book_seller_messy_data)

4. [`sales_1200_clean_records`: A Complete Example on a Clean data](./sales_1200_clean_records)

5. [`sales_1400_messy_records`: A Complete Example on a Messy data](./sales_1400_messy_records)
