---
marp: true
theme: default
paginate: true
size: 16:9
title: Week 10 — Session 1 — KPIs and Data Storytelling
---

# Week 10
## Final Project + Data Storytelling (KPI-Centered)

Small inline examples and week 7's insurance files; every query runs. **Lab 10.1** tells the pizza shop's 2016 story from its final Gold layer.
In practice: [slides 2](lecture_notes_02_story_from_gold.md).

---

# PART 0 — The Big Idea

This course was not about SQL, tables or pipelines. It was about **decision systems**:

```text
Raw data → pipeline → model → KPI → insight → decision
```

If any step breaks, the decision is wrong, usually **silently**.

---

# PART 1 — Why Data Warehousing Exists

```sql
CREATE OR REPLACE TABLE raw_claims AS SELECT * FROM (VALUES
    ('NE', 100.00), ('north-east', 120.00), ('Northeast', 110.00), ('SE', 90.00), ('south-east', 70.00)) t(region, charge);

SELECT 'raw' AS version, region, AVG(charge) AS avg_charge, COUNT(*) AS n FROM raw_claims GROUP BY ALL
UNION ALL
SELECT 'conformed', CASE WHEN lower(region) IN ('ne', 'north-east', 'northeast') THEN 'northeast' ELSE 'southeast' END,
       AVG(charge), COUNT(*) FROM raw_claims GROUP BY ALL
ORDER BY version DESC, region;
```

<!-- RESULT -->

| version   | region     | avg_charge | n |
|-----------|------------|-----------:|--:|
| raw       | NE         |      100.0 | 1 |
| raw       | Northeast  |      110.0 | 1 |
| raw       | SE         |       90.0 | 1 |
| raw       | north-east |      120.0 | 1 |
| raw       | south-east |       70.0 | 1 |
| conformed | northeast  |      110.0 | 3 |
| conformed | southeast  |       80.0 | 2 |

*(7 rows)*

<!-- /RESULT -->

Raw: 5 "regions", none of them complete. Conformed: 2 regions, each with all its rows. 👉 A warehouse = **consistency + trust**.

---

# PART 2 — Why the Medallion Architecture

| Layer | Holds | Trust |
|---|---|---|
| Bronze | everything, as received, with lineage | none yet, but nothing lost |
| Silver | one row per real thing; every row valid · flagged · rejected · duplicate | proven by reconciliation |
| Gold | shaped for the business: star schema, marts, KPIs | proven against Silver |

👉 Medallion = **progressive trust**, and an audit trail back to the source for every number.

---

# PART 3 — The Full System

```text
Sources → Bronze → Silver → Gold (star) → marts → dashboard → KPI → decision
                ↑ load log, lineage, tests, reconciliation at every arrow (weeks 6–9)
```

👉 The KPI is the **final product** of the whole system.

---

# PART 4 — What Is a KPI?

A **Key Performance Indicator** = a measurable, **defined** representation of business performance:

| KPI | Formula | Grain | Additive? |
|---|---|---|---|
| total charges | `SUM(charges)` | any | yes |
| average charges per policy-holder | `SUM(charges) / COUNT(*)` | policy-year | no: ratio of sums |
| smoker share | `COUNT(*) FILTER (smoker = 'yes') / COUNT(*)` | policy-year | no |
| average order value (pizza) | `SUM(revenue) / COUNT(DISTINCT order)` | order | no |

👉 A KPI is a **definition** (formula + grain + scope), not just a column.

---

# PART 5 — Where Everything Converges

```sql
CREATE OR REPLACE TABLE sales AS SELECT * FROM (VALUES (1, 50.00), (2, 30.00), (3, 20.00)) t(order_id, revenue);

SELECT 'pipeline OK' AS pipeline, SUM(revenue) AS revenue FROM sales
UNION ALL
SELECT 'order 1 loaded twice', SUM(revenue) FROM (SELECT * FROM sales UNION ALL SELECT * FROM sales WHERE order_id = 1);
```

<!-- RESULT -->

| pipeline             | revenue |
|----------------------|--------:|
| pipeline OK          |  100.00 |
| order 1 loaded twice |  150.00 |

*(2 rows)*

<!-- /RESULT -->

One duplicate row, +50% revenue, no error. 👉 The KPI is where pipeline mistakes **show up**, if anyone looks.

---

# PART 6 — KPI Design: Which Average?

```sql
SELECT AVG(x) AS avg_all, AVG(x) FILTER (WHERE x < 10000) AS avg_without_outlier, MEDIAN(x) AS median
FROM (VALUES (100), (200), (300), (10000)) t(x);
```

<!-- RESULT -->

| avg_all | avg_without_outlier | median |
|--------:|--------------------:|-------:|
|  2650.0 |               200.0 |  250.0 |

*(1 row)*

<!-- /RESULT -->

Which is correct? It depends on the **definition**: an impossible value is rejected in Silver; a real but rare one is kept (and flagged),
and the KPI card says whether the average includes it, or shows the median next to it.

---

# PART 7 — KPIs Depend on the Grain

```sql
CREATE OR REPLACE TABLE policy_rows AS SELECT * FROM (VALUES
    ('A', 'base', 1000.00), ('A', 'rider', 500.00), ('B', 'base', 1200.00), ('C', 'base', 800.00)) t(customer, line, charges);

SELECT 'AVG(charges): per policy LINE' AS kpi, ROUND(AVG(charges), 2) AS value FROM policy_rows
UNION ALL
SELECT 'SUM / COUNT(DISTINCT customer): per CUSTOMER', ROUND(SUM(charges) / COUNT(DISTINCT customer), 2) FROM policy_rows;
```

<!-- RESULT -->

| kpi                                          |   value |
|----------------------------------------------|--------:|
| AVG(charges): per policy LINE                |   875.0 |
| SUM / COUNT(DISTINCT customer): per CUSTOMER | 1166.67 |

*(2 rows)*

<!-- /RESULT -->

Both are "average charges". Customer A has two lines. 👉 Say **per what** (week 8): the grain decides the KPI.

---

# PART 8 — KPIs Depend on the Pipeline

| Pipeline mistake | KPI effect (seen in this course) |
|---|---|
| no dedup | revenue inflated (Part 5: +50%) |
| `DISTINCT` on raw spellings | copies survive (week 7: 287 found instead of 296) |
| silent `WHERE region <> 'unknown'` | average charge understated 7.5% (week 7) |
| naive incremental filter | late changes lost forever (week 9: 10 smokers, $90,845.71 missing) |

---

# PART 9 — One Definition, in Gold

Two teams, the same data, "average charges per customer":

- Team A: `AVG(charges)` over policy lines → **875.00** (Part 7)
- Team B: `SUM(charges) / COUNT(DISTINCT customer)` → **1,166.67**

👉 The meeting ends up arguing about the number, not the business. Define the KPI **once**, in Gold (a view or a mart column), with a **KPI card**,
and have every dashboard read it from there.

---

# PART 10 — From KPI to Decision

Do smokers cost more? (week 7's clean insurance files, 5,200 policy-years)

```sql
SELECT smoker, COUNT(*) AS policy_years, ROUND(SUM(charges) / COUNT(*), 2) AS avg_charges
FROM read_csv('../week07-Silver-Layer-Cleaning-and-Conforming/data/insurance.*.csv', types = {'smoker': 'VARCHAR'})
GROUP BY 1 ORDER BY 1;
```

<!-- RESULT -->

| smoker | policy_years | avg_charges |
|--------|-------------:|------------:|
| no     |         4229 |    12191.12 |
| yes    |          971 |    37149.76 |

*(2 rows)*

<!-- /RESULT -->

**KPI → insight → action:** smokers cost **$37,149.76** vs **$12,191.12**, about 3× → the pricing team reviews the smoker premium, and the KPI that proves the change
worked is the **loss ratio** of smokers next year.

---

# PART 11 — KPI Failure Case: Late Data

Week 9's change feed: a naive daily load (`updated_at > last run`) never saw 12 late changes.
Every run succeeded; the warehouse had **10 smokers too few** and **$90,845.71** less in charges, and the gap grows every month.
👉 Missing data is as dangerous as duplicate data, and harder to see: nothing looks wrong.

---

# PART 12 — Storytelling = KPI + Context + Decision

1. **Question** the business asked
2. **Trust**: where the data comes from, what was rejected or flagged (one line)
3. **KPI**: the evidence, defined
4. **Insight**: what it means (drivers, like-for-like)
5. **Decision**: one recommendation + the KPI that will prove it worked

👉 The KPI is the center; the pipeline is why anyone believes it.

---

# PART 13 — A Strong Story, Step by Step

| Step | Insurance example (weeks 7–8) |
|---|---|
| Question | Which region drives cost? |
| KPI | average charges per policy-year, by region (ratio of sums) |
| Chart | 5 bars: 4 regions + `unknown` |
| Insight | the 4 regions are within ~$850; the `unknown` group costs $25,961 because 53% smoke: **smoking**, not region, drives cost |
| Decision | price by smoker status; ask the source to fix region codes (813 policy-years unmapped) |

---

# PART 14 — Bad vs Good Project

| Bad | Good |
|---|---|
| SQL only, no question | starts from 3 business questions |
| KPIs nobody defined | a KPI card for every number |
| "the data was cleaned" | reconciliation: Bronze = valid + flagged + rejected + duplicates |
| a dashboard of everything | one story, one recommendation, caveats |

---

# PART 15 — Validation at the KPI Level

```sql no-run
SELECT (SELECT SUM(charges) FROM silver.insurance) = (SELECT SUM(charges) FROM gold.fact_policy_year)    AS fact_matches_silver,
       (SELECT SUM(total_charges) FROM gold.mart_region_year) = (SELECT SUM(charges) FROM gold.fact_policy_year) AS mart_matches_fact;
```

(Run it on week 8's tables: both `true`.) A KPI is only as trustworthy as the chain of checks behind it: Bronze → Silver → fact → mart → dashboard.

---

# PART 16 — Discussion

1. Which is worse for a business: missing data or duplicate data? Why?
2. Can a correct pipeline produce a misleading KPI? (Hint: Part 7, week 8's trend that was only a smoker-mix effect.)
3. Who defines KPI truth: the data team, the business, or both?
4. Should a KPI's definition change over time? What must happen to old reports when it does?

---

# PART 17 — Final Checklist

- ☐ pipeline correct: every row has a fate, reconciled
- ☐ model correct: grain tested, fact = Silver
- ☐ every KPI defined (card) and computed as a ratio of sums where needed
- ☐ validation in place (tests that stop the run)
- ☐ story leads to **one** action, with caveats

---

# PART 18 — Final Message

You built pipelines, models and systems. Now your responsibility is to:

- **define** the truth (KPIs)
- **communicate** it (one honest story)
- **enable** decisions

**Bad KPI → bad decision. Good KPI → business impact.**
