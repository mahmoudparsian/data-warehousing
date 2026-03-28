---
marp: true
theme: default
paginate: true
size: 16:9
---

# Week 5  
## Medallion Architecture (Elite v5 — Master Level)

---

# PART 0 — THE REAL SHIFT

---

## What You Learned So Far

- SQL (Week 1–2)
- Star Schema (Week 3)
- ETL Pipeline (Week 4)

---

## What You Now Learn

👉 Data is NOT just processed  
👉 Data is **managed over time**

---

## Core Transition

Traditional mindset:
👉 build pipeline

Modern mindset:
👉 design **data lifecycle**

---

# PART 1 — LIMITATIONS (DEEP + NUMERICAL)

---

## Example Dataset

| region | charges |
|--------|--------|
| NE | 1000 |
| north-east | 1200 |
| NE | 1500 |

---

## Traditional ETL Result

After cleaning:
👉 northeast → 3700

---

## Hidden Problem

👉 We LOST original distribution

---

## Business Question

What % came from "NE" vs "north-east"?

❌ Impossible to answer

---

## Insight

👉 Traditional DW destroys INFORMATION

---

# PART 2 — MEDALLION = INFORMATION PRESERVATION

---

## Key Idea

👉 Preserve ALL versions of data

---

## Layers Represent:

- Bronze → raw truth  
- Silver → interpreted truth  
- Gold → business truth  

---

## Critical Concept

👉 Truth evolves across layers

---

# PART 3 — BRONZE (DEEP SEMANTICS)

---

## Definition

Raw, immutable data

---

## Properties

- append-only  
- no deletes  
- no updates  
- schema-on-read  

---

## Example (Realistic)

| file | region | charges |
|------|--------|--------|
| 2021 | NE | 1000 |
| 2022 | north-east | 1200 |

---

## Why Append-Only?

👉 Enables replay + audit  

---

## Key Insight

👉 Bronze = TIME MACHINE

---

# PART 4 — SILVER (DEEP LOGIC)

---

## Definition

Data after applying rules

---

## What Happens Here?

- cleaning  
- validation  
- normalization  
- enrichment  

---

## Example Transformation

| raw | silver |
|-----|--------|
| NE | northeast |
| north-east | northeast |

---

## Advanced Idea

👉 Silver = CONTRACTED DATA

Meaning:
👉 rules are agreed upon

---

## Failure Example

Wrong rule:

NE → northwest ❌  

---

## Impact

👉 Entire analytics is wrong

---

# PART 5 — GOLD (BUSINESS LAYER)

---

## Definition

Data structured for consumption

---

## Examples

- star schema  
- aggregates  
- dashboards  

---

## Example

fact_insurance  
dim_region  

---

## Key Idea

👉 Gold = PERFORMANCE + STABILITY

---

## Important Insight

👉 Gold should change LESS frequently

---

# PART 6 — LAYER INTERACTION (CRITICAL)

---

## Flow

Bronze → Silver → Gold

---

## But Also:

Gold depends on Silver  
Silver depends on Bronze  

---

## Reverse Flow

If issue found:

Gold → Silver → Bronze  

---

## Insight

👉 Medallion supports BI-DIRECTIONAL thinking

---

# PART 7 — DEEP PIPELINE COMPARISON

---

## Traditional

```
Raw → ETL → Star
```

---

## Medallion

```
Raw → Bronze → Silver → Gold
```

---

## Difference

Traditional:
👉 one irreversible step  

Medallion:
👉 multiple reversible steps  

---

## Key Insight

👉 Medallion = CONTROLLED TRANSFORMATION

---

# PART 8 — STEP-BY-STEP PIPELINE (DETAILED)

---

## Bronze Step

Load everything

---

## Silver Step

Apply rules:

- remove NULL  
- standardize  
- derive columns  

---

## Gold Step

Build:

- fact  
- dimensions  

---

## Important

👉 Each step adds VALUE  

---

# PART 9 — KPI IMPACT (CRITICAL SLIDE)

---

## Without Cleaning

AVG = (1000 + 1200 + 1500)/3 = 1233

---

## With Cleaning (correct grouping)

AVG per region changes significantly

---

## Business Impact

👉 Pricing decisions  
👉 Risk analysis  

---

## Insight

👉 Data modeling impacts MONEY

---

# PART 10 — ADVANCED CASE STUDY

---

## Scenario

Dashboard shows:

👉 "Region West has lowest cost"

---

## Step 1 — Check Gold

Query correct  

---

## Step 2 — Check Silver

Find:
- incorrect mapping  

---

## Step 3 — Check Bronze

Find:
- mixed region labels  

---

## Root Cause

👉 transformation error  

---

## Fix

Update Silver logic  

---

## Insight

👉 Medallion = DEBUGGABLE SYSTEM

---

# PART 11 — INTERACTIVE THINKING (ELITE)

---

## Question 1

Where do we enforce business rules?

👉 Silver

---

## Question 2

Where do we store original errors?

👉 Bronze

---

## Question 3

Where do executives query data?

👉 Gold

---

## Question 4 (Advanced)

Where do we build ML features?

👉 Silver (mostly)

---

# PART 12 — MULTI-CONSUMER ARCHITECTURE

---

## One Pipeline → Many Uses

- Bronze → auditing  
- Silver → ML / data science  
- Gold → BI  

---

## Insight

👉 Medallion = PLATFORM, not pipeline

---

# PART 13 — COMMON FAILURES (ADVANCED)

---

## Failure 1

Skipping Bronze ❌  

---

## Failure 2

Overloading Silver ❌  

---

## Failure 3

Putting business logic in Bronze ❌  

---

## Failure 4

Recomputing Gold incorrectly ❌  

---

## Insight

👉 Layer discipline is CRITICAL

---

# PART 14 — FINAL COMPARISON

---

## Traditional DW

- rigid  
- destructive  
- single-use  

---

## Medallion

- flexible  
- non-destructive  
- multi-use  

---

## Final Insight

👉 Medallion = Modern Data Platform Foundation

---

# FINAL MESSAGE

---

You are no longer:

- building ETL  

You are:

👉 designing DATA SYSTEMS  
👉 preserving DATA HISTORY  
👉 enabling TRUSTED DECISIONS  
