# Week 7 Lab — Instructor Guide (ELITE)

---

# PART A — PROFILING

Check per file:
- row counts
- NULLs
- categories
- distributions

Students must interpret differences across years.

---

# PART B — SCHEMA ALIGNMENT

Key points:
- rename columns
- cast types
- align schema BEFORE union

---

# PART C — CONFORMANCE

Region:
CASE mapping

Smoker:
map Y/N, 1/0 → yes/no

Look for:
- consistency
- reduced category count

---

# PART D — INTEGRATION

UNION ALL with year column

Students should verify:
- correct total row count
- per-year distribution

---

# PART E — CLEANING

NULL:
remove or justify alternative

Outliers:
threshold must be justified

Dedup:
define business key or exact duplicate

---

# PART F — ENRICHMENT

age_group required  
bmi_group optional

---

# PART G — VALIDATION

Check:
- row count change
- NULL removal
- category collapse
- distribution sanity

---

# PART H — KPI IMPACT

Students should observe:
- averages change after cleaning
- categories unify

---

# PART I — REASONING

Evaluate:
- justification quality
- understanding of trade-offs
- awareness of impact

---

# COMMON MISTAKES

- union before schema alignment
- no conformance
- ignoring join/union validation
- arbitrary thresholds
- no explanation

---

# FINAL MESSAGE

Silver integration =  
alignment + conformance + validation + trust
