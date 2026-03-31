---
marp: true
paginate: true
theme: default
---

# Classic Data Warehousing vs Medallion Architecture

---

---

# 🔹 What Is a Data Warehouse?

---

## Definition

A Data Warehouse (DW) is a system designed to:

👉 collect, store, and analyze data  
👉 from multiple sources  
👉 for decision-making  

---

## Key Idea

####  Operational systems → run the business  

####  Data warehouse → understand the business  

---

## Characteristics

- integrated (multiple sources combined)  
- historical (stores past data)  
- structured (organized for analysis)  
- optimized for queries (not transactions)  

---

## Example

Sales, customers, and products data  
combined into one unified system  

---

## Insight

👉 A Data Warehouse answers:

**“What happened in the business?”**

---


# 🔹 Why Do We Need a Data Warehouse?


## Problem Without DW

Data is scattered:

- sales system  
- customer system  
- marketing system  

---

## Challenges

- inconsistent data  
- duplicate records  
- slow reporting  
- no single source of truth  

---

## What DW Solves

👉 integrates all data  
👉 cleans and standardizes  
👉 enables fast analytics  

---

## Business Value

- better decisions  
- consistent KPIs  
- historical analysis  
- trend identification  

---

## Example

### Instead of:
❌ 3 systems → 3 answers  

### With DW:
✅ 1 system → 1 trusted answer  

---

## Final Insight

👉 A Data Warehouse turns data into:

**trusted, decision-ready information**

---

# 🔹 Classic Data Warehousing (DW)

## Definition

Classic DW = centralized system for  
storing and analyzing structured data  

---

## Architecture Flow

Sources → ETL → Data Warehouse → Data Marts → BI / Reports

---

## Key Components

- ETL (Extract, Transform, Load)  
- Star Schema (fact + dimensions)  
- OLAP queries  

---

## Characteristics

- schema-first  
- batch processing  
- strong structure  

---

## Strengths

- consistent reporting  
- optimized for analytics  
- clear data model  

---

## Limitations

- slow to adapt  
- rigid pipelines  
- heavy ETL upfront  

---

## Insight

Designed for structured, stable analytics

---

# 🔹 Medallion Architecture

## Definition

Medallion = layered data architecture  

Bronze → Silver → Gold  

---

## Architecture Flow

Sources → Bronze → Silver → Gold → BI / ML

---

## Layers

Bronze: raw data  
Silver: cleaned + validated  
Gold: business-ready  

---

## Characteristics

- data-first  
- incremental pipelines  
- flexible  

---

## Strengths

- handles messy data  
- scalable  
- separates concerns  

---

## Insight

Designed for evolving data systems

---

# 🔹 Classic DW vs Medallion

## Visual Comparison

Classic DW:
Sources → ETL → Warehouse → BI  

Medallion:
Sources → Bronze → Silver → Gold → BI  

---

## Key Differences

| Aspect | Classic DW | Medallion |
|-------|-----------|-----------|
| Approach | Model first | Data first |
| Ingestion | Structured | Any |
| Transformation | Upfront ETL | Layered |
| Flexibility | Rigid | Flexible |
| Pipeline | Batch | Incremental |
| Data Quality | Early | Progressive |

---

## Key Insight

Classic DW = single refined layer  
Medallion = progressive refinement  

---

## Final Message

Both aim for trusted data  

Medallion makes the journey visible

## Question

👉 “If you were building a system today, which one would you choose—and why?”
