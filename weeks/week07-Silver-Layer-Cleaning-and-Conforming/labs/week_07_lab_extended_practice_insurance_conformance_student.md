# Week 7 — Extended Practice (optional)
## Conform 4 Messy Insurance Files into One Silver Table

> Files: [`../data_messy/`](../data_messy/) (`insurance.2021.messy.csv` … `insurance.2024.messy.csv`, one file per year = one source).
> Worked example of the same ideas: [slides 1](../lecture_notes_01_conformance_and_integration.md) and
> [`../notebook_01_multi_source_conformance.py`](../notebook_01_multi_source_conformance.py). Try it yourself first, then compare.
> DuckDB CLI or a notebook, run from this `labs/` folder: `read_csv('../data_messy/insurance.*.messy.csv', all_varchar = true, filename = true)`.

## 🎯 Objective

Build `silver.insurance` from 4 yearly sources so that **every Bronze row has exactly one fate**
(valid · flagged · rejected · duplicate, as in [week 5](../../week05-Medallion-Architecture-Introduction/Medallion_Architecture_in_a_Nutshell.md)),
every source reconciles, and every test returns 0. Then show how much Silver changes a KPI.

---

## Part A — Bronze and profiling

**A1.** Land all 4 files as `bronze.insurance`: every column as text (`all_varchar = true`), plus `_source_file`, `_batch_id` (the year) and `_ingested_at`.
How many rows per source?

**A2.** Profile **each source** (`GROUP BY _batch_id`): number of distinct `region` values; `smoker` and `gender` values other than `yes`/`no` and
`female`/`male` (NULL included); rows with a missing `age`, `bmi`, `children` or `charges`; minimum and maximum `age`, `bmi`, `children`, `charges`
(use `TRY_CAST(… AS DOUBLE)`).

**A3.** List every `region` value with its row count, and sort them into three groups: a real region in another spelling, **ambiguous**, **invalid**.

✍️ Do the 4 sources have *different* problems or the *same* ones? What does that mean for your rules?

---

## Part B — Rules with fates (write them down before any SQL)

**B1.** Complete this table in your notes. Choose limits for "impossible" values and justify each one in one line.

| # | Rule | Fate |
|---|---|---|
| C1 | region: … | fixed |
| C2 | smoker, gender: … | fixed |
| C3 | values that can't be mapped: … | flagged / rejected? |
| D1 | what counts as a duplicate: … | duplicate |
| R… | missing or impossible values: … | rejected (reason: …) |

✍️ An `unknown` region: flag it (keep the row) or reject it? Decide now; Part E tests your decision.

---

## Part C — Conform

**C1.** Write a macro `norm_region(r)` that turns ` NORTHEAST`, `north-east` and `north east` into one key. How many keys remain?

**C2.** Create mapping tables `silver.map_region`, `silver.map_smoker`, `silver.map_gender`. Use them (with `LEFT JOIN`, not a `CASE`) to build
`silver.step1_standardized`: typed columns (`'42.0'` → `42`), canonical codes, `'unknown'` where nothing maps, and `region_raw` (what the source said).
Row count by `region`?

---

## Part D — Deduplicate, reject, flag

**D1.** Count the exact copies in Bronze (raw text), then the copies after standardizing, **per source**. Why are there more after standardizing?
Look at the extra ones: are they really the same customer?

**D2.** Build `silver.step2_dedup` (one row per copy group, inside the same yearly file). Why must `_batch_id` be part of the comparison?

**D3.** Build `silver.insurance_rejected` (+ `reject_reason`, one reason per row) and `silver.insurance` (+ one `is_…_unknown` flag column per
flagged attribute). Rejected rows per reason?

---

## Part E — Reconcile, test, compare

**E1.** Per source and in total: `bronze = valid + flagged + rejected + duplicates`. Does every source reconcile?

**E2.** Write 4 tests that must return 0 on `silver.insurance`: non-canonical region, missing measure, impossible value, duplicate rows.

**E3.** Average charges and smoker share **by region** in Silver (including `unknown`). Then the average charges of all Silver rows vs Silver without
the unknown regions. ✍️ Was your C3 decision (flag or reject) right? What would a silent `WHERE region <> 'unknown'` do to the company's average charge?

**E4.** "Average charges in the northeast?" Answer it three ways: Bronze with `region = 'northeast'`, Bronze with all spellings, Silver.
✍️ Explain each difference.

---

## ✅ Deliverables

SQL for every part, the result tables, your rules table (B1), and 4–6 sentences: which decision changed the numbers most, and why.
