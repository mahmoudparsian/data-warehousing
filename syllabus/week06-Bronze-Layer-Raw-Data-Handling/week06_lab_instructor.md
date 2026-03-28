# Week 6 Lab — Instructor Guide (ELITE)

---

# PART A — PROFILING

Row count:
SELECT COUNT(*) FROM data;

NULL check:
SELECT COUNT(*) FROM data WHERE charges IS NULL;

Distinct region:
SELECT region, COUNT(*) FROM data GROUP BY region;

Outlier scan:
SELECT MIN(charges), MAX(charges), AVG(charges) FROM data;

Teaching:
Students must interpret, not just run queries.

---

# PART B — TRANSFORMATIONS

B1 NULL:
Preferred: remove rows (for teaching clarity)

B2 Region:
CASE mapping → standardized values

B3 Outliers:
WHERE charges < threshold

Discuss:
threshold choice

B4 Dedup:
Use GROUP BY or DISTINCT

---

# PART C — ENRICHMENT

age_group:
CASE WHEN age < 30 THEN 'young' ...

Optional:
bmi_group or charge_band

---

# PART D — VALIDATION

Row counts:
compare before/after

NULL check:
should be zero (if removed)

Region:
distinct values reduced

Distribution:
avg charges changes

---

# PART E — KPI IMPACT

Students should observe:
cleaning changes averages

---

# PART F — REASONING

Look for:
- justification
- awareness of trade-offs
- business thinking

---

# COMMON MISTAKES

- skipping profiling
- arbitrary thresholds
- no explanation
- no validation

---

# FINAL MESSAGE

Silver = trust layer
