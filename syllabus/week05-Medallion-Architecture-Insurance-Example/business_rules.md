# Business Rules for Insurance Data (Data Warehousing Context)

## Overview
These business rules define the expected quality, 
validity, and semantics of the insurance dataset.  
They are used to guide the transformation from 
**Bronze → Silver → Gold** layers.

---

## Rule 1 — Age Validity
- Age must be between **0 and 120**

**Invalid Examples:**

- -5
- 150
- NULL

**Action:**
- Reject invalid records in Silver

---

## Rule 2 — BMI Validity
- BMI must be between **10 and 60**

**Invalid Examples:**

- -10
- 200
- 'abc'

**Action:**
- Cast to numeric, filter invalid values

---

## Rule 3 — Charges Validity
- Charges must be **≥ 0**

**Invalid Examples:**

- -1000
- NULL
- 'N/A'

**Action:**
- Remove or filter invalid records

---

## Rule 4 — Children Count
- Must be between **0 and 10**

**Invalid Examples:**

- -3
- 25

**Action:**
- Filter invalid values

---

## Rule 5 — Region Standardization (Flexible Domain)

### Valid Regions
- northeast, northwest, southeast, southwest
- central, east, west

### Data Quality Types

| Type                 | Example     | Action       |
|----------------------|------------|--------------|
| Valid                | northeast  | keep         |
| Formatting issue     | north east | standardize  |
| Case issue           | NORTHEAST  | lowercase    |
| Whitespace           |  west      | trim         |
| Invalid              | mars       | reject       |
| New valid            | central    | keep         |

**Action:**

- Normalize: `LOWER(TRIM(region))`
- Remove spaces: `REPLACE(region, ' ', '')`
- Validate against allowed list

---

## Rule 6 — Categorical Integrity

### Gender

- Valid: male, female

### Smoker

- Valid: yes, no

**Invalid Examples:**

- gender: 'X', 'unknown'
- smoker: 'maybe', '1'

**Action:**

- Standardize or reject

---

## Rule 7 — Duplicate Records
- Duplicate rows should not exist

**Action:**
- Deduplicate using DISTINCT or ROW_NUMBER()

---

## Rule 8 — Semantic Consistency (Advanced Rule)
- Smokers should generally have higher charges than non-smokers

**Invalid Examples:**

- smoker = 'yes' AND charges = 100

**Action:**

- Flag anomalies (do not necessarily remove)

---

## Summary

| Rule Type        | Enforcement |
|-----------------|------------|
| Structural      | Silver     |
| Domain          | Silver     |
| Standardization | Silver     |
| Deduplication   | Silver     |
| Semantic        | Silver/Gold|

---

## Final Note
These rules simulate real-world data quality challenges:

- messy ingestion
- evolving schemas
- business-driven validation

They form the foundation for:

- EDA
- Data Cleaning
- Analytical Modeling
