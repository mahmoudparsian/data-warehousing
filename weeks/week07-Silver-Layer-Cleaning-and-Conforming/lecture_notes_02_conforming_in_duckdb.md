---
marp: true
theme: default
paginate: true
title: Week 7 — Conforming Sources in Practice (DuckDB patterns)
---

# Week 7
## Conforming Sources in Practice: DuckDB Patterns

Every query runs: on this week's messy insurance files (`data_messy/insurance.*.messy.csv`) or on small inline tables.
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

# 🔤 Step 1: Normalize Spellings with a Macro

```sql
CREATE OR REPLACE VIEW bronze_insurance AS
SELECT * FROM read_csv('data_messy/insurance.*.messy.csv', all_varchar = true, filename = true);

CREATE OR REPLACE MACRO norm_region(r) AS
  regexp_replace(lower(trim(r)), '[ -]', '', 'g');   -- ' NORTHEAST', 'north-east', 'north east' → 'northeast'

SELECT norm_region(region) AS region_key, COUNT(DISTINCT region) AS spellings, COUNT(*) AS n_rows
FROM bronze_insurance GROUP BY 1 ORDER BY 2 DESC, 1;
```

<!-- RESULT -->

| region_key | spellings | n_rows |
|------------|----------:|-------:|
| northeast  |         4 |   1284 |
| southwest  |         4 |   1272 |
| mars       |         1 |     40 |
| midwest    |         1 |    293 |
| moon       |         1 |     37 |
| north      |         1 |    220 |
| northwest  |         1 |   1328 |
| south      |         1 |    413 |
| southeast  |         1 |   1537 |
| unknown    |         1 |     43 |

*(10 rows)*

<!-- /RESULT -->

16 raw values → 10 keys: the 4 spellings of `northeast` and of `southwest` collapse. 👉 A **macro** = the rule written once, reused in every query and every pipeline.

---

# 🗺️ Step 2: A Mapping Table (Not a CASE)

```sql
CREATE OR REPLACE TABLE map_region AS
SELECT * FROM (VALUES ('northeast', 'northeast'), ('northwest', 'northwest'),
                      ('southeast', 'southeast'), ('southwest', 'southwest')) t(region_key, region);

-- what is still unmapped?
SELECT norm_region(b.region) AS region_key, COUNT(*) AS n_rows
FROM bronze_insurance b
LEFT JOIN map_region m ON m.region_key = norm_region(b.region)
WHERE m.region IS NULL
GROUP BY 1 ORDER BY 2 DESC;
```

<!-- RESULT -->

| region_key | n_rows |
|------------|-------:|
| south      |    413 |
| midwest    |    293 |
| north      |    220 |
| unknown    |     43 |
| mars       |     40 |
| moon       |     37 |

*(6 rows)*

<!-- /RESULT -->

→ 1,046 rows: `south`, `midwest`, `north` are **ambiguous** (which region?); `unknown`, `mars`, `moon` are **invalid**.

- Mapping tables are **data**: business users can review them; a new spelling = a new row, not new code
- Unmapped values get a **fate**: flagged (kept as `'unknown'` + a flag, as in [slides 1](lecture_notes_01_conformance_and_integration.md)) or rejected with a reason, never a silent guess

---

# 🕒 Step 3: Whose Clock?

```sql
SET TimeZone = 'UTC';   -- make results the same on every laptop

SELECT '2016-07-04 01:30:00+00'                                              AS sent_by_the_app,
       TIMESTAMPTZ '2016-07-04 01:30:00+00' AT TIME ZONE 'America/New_York'  AS shop_time;
```

<!-- RESULT -->

| sent_by_the_app        | shop_time           |
|------------------------|---------------------|
| 2016-07-04 01:30:00+00 | 2016-07-03 21:30:00 |

*(1 row)*

<!-- /RESULT -->

- An evening order in New York (21:30 on July 3) is already **July 4** in UTC
- Report days and hours in the **business's** time zone

---

# ⚠️ The Session Time Zone Trap

`TIMESTAMPTZ::DATE` uses the **session** time zone, so the same query gives different dates on different laptops:

```sql
SET TimeZone = 'America/Los_Angeles';
SELECT 'laptop in California' AS session, (TIMESTAMPTZ '2016-07-04 01:30:00+00')::DATE AS order_date;
```

<!-- RESULT -->

| session              | order_date |
|----------------------|------------|
| laptop in California | 2016-07-03 |

*(1 row)*

<!-- /RESULT -->

```sql
SET TimeZone = 'UTC';
SELECT 'session = UTC' AS session, (TIMESTAMPTZ '2016-07-04 01:30:00+00')::DATE AS order_date
UNION ALL
SELECT 'shop time', (TIMESTAMPTZ '2016-07-04 01:30:00+00' AT TIME ZONE 'America/New_York')::DATE;
```

<!-- RESULT -->

| session       | order_date |
|---------------|------------|
| session = UTC | 2016-07-04 |
| shop time     | 2016-07-03 |

*(2 rows)*

<!-- /RESULT -->

👉 `SET TimeZone = 'UTC'` at the top of every session, and convert to the business's time zone **explicitly**.

---

# ♻️ Step 4: What Is a Duplicate? One Rule, Two Cases

**A duplicate = the same real thing sent twice.** Ask: *could two **different** real things look identical after standardizing?*

| Source | Two different real things identical after standardizing? | So deduplicate on |
|---|---|---|
| insurance customer-year (age, bmi, children, charges to the cent) | practically never | **standardized** values (week 6, slides 1): 287 raw copies → **296** |
| app order line (order, pizza, size, qty), **no line id** | **yes**: two Medium Margheritas in one order | **raw** values only: a re-send is a byte-for-byte copy |

Week 6's rule ("standardize, then deduplicate") and this week's ("deduplicate the raw lines, then conform") are the **same rule** applied to different data.

---

# ♻️ Step 4 in SQL: Order Lines Without a Line Id

```sql
CREATE OR REPLACE TABLE app_raw AS SELECT * FROM (VALUES
    ('DLV-1', 'Margherita',           'Medium', 1),
    ('DLV-1', 'The Margherita Pizza', 'medium', 1),   -- a 2nd Margherita, typed on another screen
    ('DLV-2', 'Hawaiian',             'Large',  1),
    ('DLV-2', 'Hawaiian',             'Large',  1)    -- the app re-sent this line
) t(order_ref, item, size, qty);

SELECT 'dedup raw, then conform' AS order_of_steps, COUNT(*) AS lines
FROM (SELECT DISTINCT * FROM app_raw)
UNION ALL
SELECT 'conform, then dedup', COUNT(*)
FROM (SELECT DISTINCT order_ref, regexp_replace(lower(item), '^the | pizza$', '', 'g'), lower(size), qty FROM app_raw);
```

<!-- RESULT -->

| order_of_steps          | lines |
|-------------------------|------:|
| dedup raw, then conform |     3 |
| conform, then dedup     |     2 |

*(2 rows)*

<!-- /RESULT -->

Conforming first merges the two Margheritas: a real pizza and its revenue disappear. Lab 7.2's bonus measures this on the app file.

⚠️ Even raw `DISTINCT` is **evidence, not proof**: two identical lines could also be two real pizzas typed the same way.
The real fix is a **line id** from the source (`DLV-1 / line 2`); until you have one, write the assumption down and **count** what you removed.
👉 Keep the raw value next to the conformed one (`item_raw`, `region_raw`) for lineage.

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

```sql no-run
SELECT 'IN-STORE' AS channel, … FROM silver.pos_lines
UNION ALL
SELECT 'DELIVERY',            … FROM silver.app_lines;
```

- `UNION ALL` matches **by position**: same columns, same order, same types
- `UNION ALL BY NAME` matches by **column name** (safer when lists are long):

```sql
SELECT 'by position' AS how, * FROM (SELECT 1 AS a, 'x' AS b UNION ALL SELECT 'y' AS b, 2 AS a)
UNION ALL
SELECT 'by name', * FROM (SELECT 1 AS a, 'x' AS b UNION ALL BY NAME SELECT 'y' AS b, 2 AS a);
```

<!-- RESULT -->

| how         | a | b |
|-------------|---|---|
| by position | 1 | x |
| by position | y | 2 |
| by name     | 1 | x |
| by name     | 2 | y |

*(4 rows)*

<!-- /RESULT -->

By position, the second row puts `'y'` under `a` and `2` under `b`: DuckDB quietly turns both columns into text, **no error**.
By name, every value lands in its own column. Lab 7.2's 🐞 is this bug with two text columns.

- Add a **source / channel** column, and make keys unique across sources (`channel` + id as **text**)

---

# 🧮 Step 7: Reconcile Every Source

For **each** source:

> Bronze rows = valid + flagged + rejected (per reason) + duplicates

Then for the integrated table:

> rows = Σ (valid + flagged) rows of all sources

Slides 1 did it for the insurance files: **6,467 = 4,160 + 1,037 + 974 + 296**.
👉 If the numbers don't add up, **stop**: Gold built on an unexplained gap is a wrong dashboard waiting to happen.

---

# ✅ Summary

| Pattern | DuckDB |
|---|---|
| normalize spellings | `CREATE MACRO …` with `lower`, `trim`, `regexp_replace` |
| map codes | mapping table + `LEFT JOIN`; unmatched → flagged or rejected, never guessed |
| fix clocks | `SET TimeZone = 'UTC'`, `… AT TIME ZONE 'America/New_York'` |
| dedup | a duplicate = the same real thing twice: standardized values for customers, raw lines when there is no line id |
| disagreeing sources | keep both values + a rule |
| integrate | `UNION ALL` (by position) / `UNION ALL BY NAME`, + `channel` |
| trust | reconcile per source |
