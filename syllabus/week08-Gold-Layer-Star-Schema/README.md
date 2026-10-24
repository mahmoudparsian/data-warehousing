# Week 8 — Gold Layer & Star Schema

**Block C · Medallion architecture + star schema (weeks 5–8)**

The pizza shop's Silver layer is clean and integrated (`silver.sales_lines`: two channels, 2015–2016).
Gold turns it into what the business actually uses: a **star schema** with a clearly declared grain,
**KPIs** computed correctly, and **data marts** for specific users, ending in a Tableau dashboard.
This closes the Medallion block: Bronze (week 6) → Silver (weeks 6–7) → Gold (week 8).

## 🎯 Learning objectives

By the end of the week you can:

1. Declare the grain of a fact table and test it against the data (and add a surrogate key when the natural key isn't unique).
2. Build a date dimension as a full calendar (with an Unknown member), plus hour, product and channel dimensions with surrogate keys.
3. Build and validate a fact table: row counts, totals, orphan keys, measure arithmetic.
4. Classify measures as additive, semi-additive or non-additive, and compute ratios and distinct counts correctly.
5. Build data marts with a declared grain for a specific audience, and reconcile them with the fact table.
6. Deliver a Gold mart to Tableau.

## 📅 Sessions

| Session | Topic | Material | Lab (30 min) |
|---|---|---|---|
| 1 | Gold modeling: business-first design, grain, dimensions, surrogate keys, validation | [slides 1: Gold modeling](week08_slides_1_gold_modeling.md) (Parts 0–8) · `week08_notebook.py` | [Lab 8.1](labs/week_08_lab_01_student.md): pizza star schema · notebook `week_08_lab_01_student.py` |
| 2 | KPIs that add up, data marts, Gold → Tableau | [slides 2: KPIs & marts](week08_slides_2_kpis_and_marts.md) · [slides 1](week08_slides_1_gold_modeling.md) (Parts 9–18) · demo: [`insurance_medallion_example/`](insurance_medallion_example/) (`medallion_executive_dashboard.py`) | [Lab 8.2](labs/week_08_lab_02_student.md): KPIs, 2 marts, dashboard · notebook `week_08_lab_02_student.py` |

## 📂 What's in this folder

| Folder / file | Contents |
|---|---|
| [`labs/`](labs/) | Labs 8.1 and 8.2 (sheet `.md` + Marimo notebook, released in class) · `week_08_lab_setup.sql` (rebuilds weeks 6–7 up to `silver.sales_lines` in about 2 s), [extended practice](labs/week_08_lab_extended_practice_insurance_gold_student.md): Gold on insurance data (optional) |
| `week08_notebook.py` | Gold modeling walkthrough on the insurance data: business questions → grain → dimensions → fact → marts |
| [`insurance_medallion_example/`](insurance_medallion_example/) | A complete second case: 4 years of messy insurance files → Bronze → Silver ([business rules](insurance_medallion_example/business_rules.md)) → Gold star schema → executive dashboard (3 notebooks, run in order: EDA, build, dashboard) |

## ⚙️ Setup

```bash
cd labs
duckdb pizza.duckdb < week_08_lab_setup.sql
```
Start each session with `SET TimeZone = 'UTC';`. Tableau Desktop/Public for Lab 8.2.

## ✅ Before week 9

- Finish both labs; keep `labs/pizza.duckdb` and your dashboard screenshot.
- Week 9 asks: what happens when **new data arrives every day**? Think about which of your weeks 6–8 steps you would have to rerun.
