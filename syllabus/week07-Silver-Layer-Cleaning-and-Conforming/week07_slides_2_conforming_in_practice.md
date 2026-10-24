---
marp: true
theme: default
paginate: true
title: Week 7 — Conforming Sources in Practice (DuckDB patterns)
---

# Week 7
## Conforming Sources in Practice: DuckDB Patterns

Examples use this week's messy insurance files (`data_messy/insurance.*.messy.csv`).
The labs apply the same patterns to the pizza shop's **delivery app**.

---

# 🧭 Conformance = Same Columns, Same Codes, Same Meaning

| Problem | Example | Tool |
|---|---|---|
| different column names | `OrderRef` vs `order_id` | **schema mapping** (a table in your notes) |
| different codes / spellings | `north-east`, ` NORTHEAST`, `north east` | **normalize** + **mapping table** |
| different units / types | `'$16.75'`, `'42.0'` | parse + cast |
| different clocks | UTC vs local time | `AT TIME ZONE` |
| different "truths" | app price ≠ menu price | keep both, decide per KPI |

---

# 🔤 Step 1: Normalize Spellings

```sql
SELECT region, COUNT(*) FROM read_csv('data_messy/insurance.*.messy.csv',
                                      union_by_name = true, all_varchar = true)
GROUP BY 1 ORDER BY 2 DESC;
```

16 values for 4 real regions: `southeast`, `northwest`, …, `north-east`, ` NORTHEAST`, `south west`, `south-west`, `north east`, …, `south`, `midwest`, `north`, `unknown`, `mars`, `moon`

```sql
CREATE MACRO norm_region(r) AS
  regexp_replace(lower(trim(r)), '[ -]', '', 'g');   -- ' NORTHEAST', 'north-east', 'north east' → 'northeast'
```

👉 A **macro** = the rule written once, reused everywhere

---

# 🗺️ Step 2: A Mapping Table (Not a CASE)

```sql
CREATE TABLE silver.map_region AS
SELECT * FROM (VALUES ('northeast','northeast'), ('northwest','northwest'),
                      ('southeast','southeast'), ('southwest','southwest'))
       t(region_key, region);

-- what is still unmapped?
SELECT norm_region(region) AS key, COUNT(*)
FROM bronze_insurance
WHERE norm_region(region) NOT IN (SELECT region_key FROM silver.map_region)
GROUP BY 1;
```

→ `south`, `midwest`, `north` (**ambiguous**: which region?) and `unknown`, `mars`, `moon` (**invalid**)

- Mapping tables are **data**: business users can review them; new spellings = new rows, not new code
- Unmapped values → **quarantine with a reason** (or an explicit `'UNKNOWN'` member), never a silent guess

---

# 🕒 Step 3: Whose Clock?

```sql
SET TimeZone = 'UTC';   -- make results the same on every laptop

SELECT TIMESTAMPTZ '2016-07-04 01:30:00+00'                                  AS utc_ts,
       TIMESTAMPTZ '2016-07-04 01:30:00+00' AT TIME ZONE 'America/New_York'  AS local_ts;
```

| utc_ts | local_ts |
|---|---|
| 2016-07-04 01:30:00+00 | **2016-07-03** 21:30:00 |

- An evening order in New York is **tomorrow** in UTC
- Report days and hours in the **business's** time zone
- ⚠️ `TIMESTAMPTZ::DATE` uses the **session** time zone: set it explicitly

---

# ♻️ Step 4: Deduplicate Before You Conform

- Exact duplicates = what the **source** sent twice → remove on the **raw** columns
- After conforming, two **different** source lines can become identical
  (`Medium` vs `medium`, `Hawaiian` vs `The Hawaiian Pizza`) and a real sale disappears

```sql
WITH dedup AS (SELECT DISTINCT <raw source columns> FROM bronze.source)
SELECT <conformed columns> FROM dedup …
```

👉 Keep the raw value next to the conformed one (`item_raw`, `region_raw`) for lineage

---

# ⚖️ Step 5: When Sources Disagree

| Situation | Typical decision |
|---|---|
| two prices (menu vs paid) | keep **both** columns: `list_price`, `paid_price` |
| two addresses for a customer | **precedence** rule: CRM beats web form |
| two timestamps | keep both: `ordered_at`, `delivered_at` |

- Silver records the facts **and** the source of each
- Gold chooses per KPI (revenue = paid; price compliance = list vs paid)

---

# 🔗 Step 6: Integrate

```sql
SELECT 'IN-STORE' AS channel, … FROM silver.pos_lines
UNION ALL
SELECT 'DELIVERY',            … FROM silver.app_lines;
```

- `UNION ALL` matches **by position**: same columns, same order, same types
- `UNION ALL BY NAME` matches by **column name** (safer when lists are long):

```sql
SELECT 1 AS a, 'x' AS b  UNION ALL BY NAME  SELECT 'y' AS b, 2 AS a;   -- → (1,'x'), (2,'y')
```

- Add a **source / channel** column, and make keys unique across sources (`channel` + id as **text**)

---

# 🧮 Step 7: Reconcile Every Source

For **each** source:

> Bronze rows = duplicates + rejected (per reason) + loaded

Then for the integrated table:

> rows = Σ loaded rows of all sources

👉 If the numbers don't add up, **stop**: Gold built on an unexplained gap is a wrong dashboard waiting to happen

---

# ✅ Summary

| Pattern | DuckDB |
|---|---|
| normalize spellings | `CREATE MACRO …` with `lower`, `trim`, `regexp_replace` |
| map codes | mapping table + `LEFT JOIN`, quarantine the unmatched |
| fix clocks | `SET TimeZone = 'UTC'`, `… AT TIME ZONE 'America/New_York'` |
| dedup | raw first, then conform |
| disagreeing sources | keep both values + a rule |
| integrate | `UNION ALL` (by position) / `UNION ALL BY NAME`, + `channel` |
| trust | reconcile per source |
