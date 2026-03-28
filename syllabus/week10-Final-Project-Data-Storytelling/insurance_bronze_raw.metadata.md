# Dataset Description — `insurance_bronze_raw.csv`

## Overview

This dataset simulates a real-world raw (Bronze) data ingestion scenario.

It is intentionally messy and imperfect to demonstrate:
- data cleaning (Silver)
- data modeling (Gold)
- pipeline correctness
- KPI reliability

---

## Schema

| Column        | Description |
|--------------|------------|
| `customer_id` | Customer identifier (NOT unique in Bronze) |
| `region`      | Region (messy categorical values) |
| `smoker`      | Smoker flag (inconsistent formatting) |
| `charges`     | Numeric cost (simulated insurance charges) |
| `updated_at`  | Timestamp of last update |

---

## Key Characteristics

### 1. Messy Categorical Data

The region column contains multiple representations:

- NE  
- north-east  
- Northeast  
- SW  
- southwest  

These must be standardized in the Silver layer.

---

### 2. Inconsistent Values

The smoker column includes:

- Yes / yes  
- No / no  

Requires normalization.

---

### 3. Duplicate Records

Same `customer_id` appears multiple times with different `updated_at`.

This enables:

- deduplication logic
- latest record selection

---

### 4. Time-Based Data

`updated_at` supports:

- incremental pipelines  
- sliding window logic  
- late data simulation  

---

## Why This Dataset Matters

### Bronze

- inconsistent  
- unreliable  

### Silver

- cleaned  
- trustworthy  

### Gold

- structured  
- KPI-ready  

---

## Example KPI Impact

Raw:

```sql
SELECT region, 
       AVG(charges) 
FROM bronze 
GROUP BY region;
```

Incorrect due to messy values.

Gold:

```sql
SELECT region, 
       AVG(charges) 
FROM fact 
GROUP BY region;
```

Correct and consistent.

---

## Final Insight

This dataset is not about insurance.

It is about:

- data quality  
- pipeline correctness  
- KPI trust  

---

## Final Message

* Bronze → data exists  

* Silver → data is trusted  

* Gold → data drives decisions  

If the pipeline is weak, the KPI is wrong.
