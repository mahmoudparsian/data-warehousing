# Week 8 — Extended Practice (optional): Gold Modeling on Insurance Data

> Input: week 7's insurance Silver table `silver.insurance` (5,197 policy-years, 2021–2024, flags for unknown region / smoker / gender).
> Build it from the **week 8 folder** (one level up from `labs/`): `duckdb insurance.duckdb < insurance_silver_week07.sql`, then work in `insurance.duckdb`.
> Worked example of the same steps (try first, then compare): [slides 1](../lecture_notes_01_gold_modeling.md) and
> [`../notebook_01_gold_star_schema.py`](../notebook_01_gold_star_schema.py). A second, larger case: [`../insurance_medallion_example/`](../insurance_medallion_example/).

## 🎯 Objective

Build a star schema and two data marts from `silver.insurance`, prove that they agree with Silver, and answer three business questions with KPIs
that add up.

---

## Part A — Questions first

**A1.** Write 3 business questions the insurer would ask (e.g. "Does a high BMI cost more for smokers than for non-smokers?").
For each: the **measure** and the **dimensions** it needs.

## Part B — Grain

**B1.** Write the grain as a sentence ("One row = …"). **B2.** Test it: number of rows vs number of distinct grain values.
✍️ What would one undetected copy per smoker do to your totals?

## Part C — Dimensions

**C1.** Build `gold.dim_region`, `gold.dim_smoker` (each with an `unknown` member) and `gold.dim_bmi_class`
(`underweight` < 18.5 ≤ `normal` < 25 ≤ `overweight` < 30 ≤ `obese`), each with a surrogate key numbered by an **ordered** `ROW_NUMBER()`
over the **distinct** values (or a `VALUES` list). Row counts?

🐞 **C2.** Run `SELECT COUNT(*) FROM (SELECT DISTINCT ROW_NUMBER() OVER () AS k, region FROM silver.insurance);`. Why isn't it 5?

## Part D — Fact and validation

**D1.** Build `gold.fact_policy_year` (surrogate key, `year`, the 3 dimension keys, `age`, `charges`, `is_flagged`).
**D2.** Four tests that must pass: rows = Silver, `SUM(charges)` = Silver, no NULL keys, unique surrogate key.

## Part E — Marts

**E1.** `gold.mart_region_year` (grain: region × year) and `gold.mart_bmi_smoker` (grain: BMI class × smoker), with **additive parts only**
(`policy_years`, `total_charges`, …). **E2.** Check each mart against the fact (rows and charges).

## Part F — KPIs

**F1.** Average charges per BMI class × smoker (from `mart_bmi_smoker`, as a ratio of sums). ✍️ Answer your BMI question from A1.
**F2.** 🐞 Compute "average charges" as the average of the 5 region averages, and as `SUM / COUNT`. Which is the company's number? Why do they differ?
**F3.** Average charges per year: overall, then per smoker status. ✍️ Is there a trend? What does the overall line hide?

---

## ✅ Deliverables

SQL and results for every part, your grain sentence, and 4–6 sentences: the most surprising answer, and the one test you would never skip.
