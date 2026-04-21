# Week 5 Lab — Instructor Guide (ELITE — Medallion Mapping)

---

# PART A — PIPELINE MAPPING

## A1 — Bronze
- all raw files (2021–2024)
- no cleaning
- append-only

WHY:
- preserve original data
- enable replay/debugging

---

## A2 — Silver
- region standardization
- null removal
- outlier handling
- derived columns

WHY:
- data quality layer
- consistent + validated

---

## A3 — Gold
- fact_insurance
- dim_region, dim_smoker, dim_person
- aggregates

WHY:
- optimized for analytics
- stable definitions

---

# PART B — TRANSFORMATION JUSTIFICATION

B1 Remove NULL → Silver (data quality)  
B2 Standardize region → Silver (normalization)  
B3 Create age_group → Silver (enrichment)  
B4 Compute revenue → Gold (aggregation)  
B5 Deduplicate → Silver (quality/consistency)  

---

# PART C — PIPELINE REDESIGN

Traditional:
Raw → ETL → Star

Medallion:
Raw → Bronze → Silver → Gold

Detailed:
Bronze: ingest raw  
Silver: clean + validate  
Gold: model + aggregate  

---

# PART D — ERROR ANALYSIS

1. Check Gold (query logic)  
2. Then Silver (transformation issues)  
3. Then Bronze (raw inconsistencies)  

Fix:
- correct Silver logic
- rebuild downstream layers

---

# PART E — BAD DESIGN

E1 Cleaning in Bronze ❌ (destroys raw)  
E2 Aggregation in Silver ❌ (belongs in Gold)  
E3 Skipping Silver ❌ (no quality layer)  
E4 Raw → Gold ❌ (no structure/cleaning)  

---

# PART F — MULTI-USE

Auditing → Bronze  
ML features → Silver  
Dashboard → Gold  

---

# TEACHING NOTES

Ask:
- Why this layer?
- What happens if misplaced?
- What is the business impact?

---

# FINAL MESSAGE

Medallion = structure + flexibility + trust
