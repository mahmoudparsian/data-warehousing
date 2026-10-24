---
marp: true
theme: default
paginate: true
size: 16:9
---

# Week 10  
## Final Project + Data Storytelling (Elite v5 — KPI-Centered, Deep + Case-Driven)

---

# PART 0 — THE BIG IDEA

---

## What This Course Was Really About

Not SQL  
Not tables  
Not pipelines  

👉 **Decision systems**

---

## Full Chain

```text
Raw Data → Pipeline → Model → KPI → Insight → Decision
```

---

## If ANY step breaks

👉 Decision is wrong

---

# PART 1 — WHY DATA WAREHOUSING EXISTS (REAL)

---

## Raw Data Reality

| region | charge |
|--------|--------|
| NE | 100 |
| north-east | 120 |
| Northeast | 110 |

---

## Problem

Aggregation breaks  
Metrics inconsistent  

---

## Data Warehouse Fix

| region | avg_charge |
|--------|------------|
| northeast | 110 |

---

## Insight

👉 DW = **consistency + trust**

---

# PART 2 — WHY MEDALLION EXISTS (MAKE IT SINK)

---

## Traditional DW Limitation

- hard to ingest messy data  
- no intermediate trust layers  

---

## Medallion Layers

```text
Bronze → Silver → Gold
```

---

## Example

Bronze:
"NE", "north-east"

Silver:
"northeast"

Gold:
avg = 110  

---

## Insight

👉 Medallion = **progressive trust building**

---

# PART 3 — FULL SYSTEM VIEW (FINAL ARCHITECTURE)

---

```text
Source
 ↓
Bronze (raw)
 ↓
Silver (clean + conform)
 ↓
Gold (modeled)
 ↓
Marts
 ↓
Dashboard
 ↓
KPI
```

---

## Insight

👉 KPI is the **final product of the system**

---

# PART 4 — WHAT IS A KPI (DEEP)

---

## Definition

KPI = Key Performance Indicator  

👉 measurable representation of business performance  

---

## Examples (From Your Project)

- AVG(charges)  
- SUM(charges)  
- charges by region  
- smoker vs non-smoker  

---

## Insight

👉 KPI = **business truth extracted from data**

---

# PART 5 — KPI IS WHERE EVERYTHING CONVERGES

---

## Pipeline builds data  
## Model organizes data  
## KPI summarizes data  

---

## Example

Bad pipeline:
duplicate rows  

---

## KPI:

SUM(charges) inflated  

---

## Decision:

wrong  

---

## Insight

👉 KPI exposes pipeline correctness

---

# PART 6 — KPI DESIGN (STRONG EXAMPLE)

---

## Data

| values |
|--------|
| 100 |
| 200 |
| 300 |
| 10000 |

---

## KPI 1 (naive)

AVG = 2650  

---

## KPI 2 (business-aware)

exclude outlier → AVG = 200  

---

## Question

Which is correct?

---

## Answer

👉 depends on definition  

---

## Insight

👉 KPI = **definition, not just formula**

---

# PART 7 — KPI DEPENDS ON MODELING

---

## Grain Problem

If grain is wrong:

- duplicate rows  
- wrong averages  
- inflated counts  

---

## Example

One person appears twice  

---

## Result

AVG(charges) distorted  

---

## Insight

👉 modeling defines KPI correctness

---

# PART 8 — KPI DEPENDS ON PIPELINE

---

## Failure Case

No dedup  

---

## Result

duplicate facts  

---

## KPI

inflated revenue  

---

## Insight

👉 pipeline errors → KPI corruption

---

# PART 9 — KPI CONSISTENCY (CRITICAL)

---

## Scenario

Two teams compute KPI differently  

---

## Team A

AVG(charges)

---

## Team B

SUM(charges)/COUNT(DISTINCT customer)

---

## Result

Different answers  

---

## Insight

👉 KPI must be **centralized in Gold**

---

# PART 10 — KPI DRIVES DECISION (FULL CASE)

---

## Question

Do smokers cost more?

---

## SQL

```sql
SELECT smoker, AVG(charges)
FROM fact_insurance
GROUP BY smoker;
```

---

## Result

smokers = 2x  

---

## Insight

higher risk  

---

## Decision

adjust pricing  

---

## Insight

👉 KPI → insight → action

---

# PART 11 — KPI FAILURE CASE (REAL)

---

## Scenario

Late data missed  

---

## Result

under-reported revenue  

---

## Business Impact

bad forecasting  

---

## Insight

👉 missing data is as dangerous as duplicates

---

# PART 12 — STORYTELLING (NOW CONNECTED)

---

## Story = KPI + Context + Decision

---

## Structure

1. question  
2. pipeline (trust)  
3. KPI (evidence)  
4. insight  
5. decision  

---

## Insight

👉 KPI is the center of the story

---

# PART 13 — STRONG STORY EXAMPLE

---

## Question

Which region drives cost?

---

## KPI

avg charges by region  

---

## Chart

(bar chart)

---

## Insight

Region X highest  

---

## Decision

target intervention  

---

# PART 14 — BAD VS GOOD PROJECT

---

## Bad

- SQL only  
- no KPI clarity  
- no story  

---

## Good

- clear pipeline  
- validated KPI  
- strong narrative  

---

## Insight

👉 project = system + KPI + story

---

# PART 15 — VALIDATION (KPI LEVEL)

---

## Must Check

- Silver vs Gold totals  
- duplicates  
- missing data  

---

## Example

```sql
SELECT SUM(charges) FROM silver;
SELECT SUM(charges) FROM fact;
```

---

## Insight

👉 validation ensures KPI trust

---

# PART 16 — DISCUSSION (STRONG)

---

## Q1

Which is worse:
- missing data  
- duplicate data  

---

## Q2

Can a correct pipeline produce a misleading KPI?

---

## Q3

Who defines KPI truth?

---

## Q4

Should KPI logic change over time?

---

# PART 17 — FINAL CHECKLIST

---

- pipeline correct  
- modeling correct  
- KPI defined clearly  
- validation present  
- story leads to action  

---

# PART 18 — FINAL CAPSTONE MESSAGE

---

You built:

- pipelines  
- models  
- systems  

---

Now your responsibility:

👉 define truth (KPI)  
👉 communicate truth  
👉 enable decisions  

---

## FINAL TRUTH

Bad KPI → bad decision  
Good KPI → business impact
