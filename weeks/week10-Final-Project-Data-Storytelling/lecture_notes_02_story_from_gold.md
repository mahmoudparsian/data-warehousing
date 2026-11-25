---
marp: true
theme: default
paginate: true
title: Week 10 — From Gold to a Story (in practice)
---

# Week 10
## From Gold to a Story: in Practice

Examples use the online-sales star from week 4 (`week04…/OLAP/OLAP_by_DuckDB/csv/`); the query runs.
Labs 10.1 and 10.2 apply the same steps to the pizza shop's Gold layer.

---

# 🪪 Step 1: A KPI Card for Every Number

| Field | Example: average order value |
|---|---|
| Name | AOV |
| Formula | `SUM(revenue) / COUNT(DISTINCT order_id)` |
| Grain computed at | order |
| Additive? | **No**: recompute from parts, never sum or average |
| Owner | Sales manager |
| Good = | higher, with stable margin |

👉 If two people compute "AOV" differently, the meeting is about the number, not the business

---

# ⚖️ Step 2: Compare Like with Like

| Trap | Fix |
|---|---|
| a new channel / store / product line counted in "growth" | compare **same scope** both periods; report the new part separately |
| partial periods (Jan–Mar vs full year) | compare equal periods (Q1 vs Q1) |
| different definitions across years | one KPI card, applied to both years |
| totals across different-sized groups | rates per order / per customer / per day |

👉 Slide 1 gets the **honest** number; the impressive one goes in context

---

# 🔍 Step 3: Decompose the Headline into Drivers

Revenue = **volume × value**. Example (online sales, 2023 → 2024):

```sql
CREATE OR REPLACE VIEW sales AS SELECT * FROM read_csv('../week04-Star-Schema-and-OLAP/OLAP/OLAP_by_DuckDB/csv/sales.csv');
WITH y AS (SELECT date_key // 10000 AS year, COUNT(*) AS sales_lines, SUM(total_amount) AS revenue
           FROM sales WHERE date_key // 10000 IN (2023, 2024) GROUP BY 1)
SELECT year, sales_lines, ROUND(revenue / sales_lines, 2) AS revenue_per_line, ROUND(revenue / 1e6, 1) AS revenue_millions,
       ROUND(sales_lines / LAG(sales_lines) OVER (ORDER BY year), 3) AS lines_ratio,
       ROUND((revenue / sales_lines) / LAG(revenue / sales_lines) OVER (ORDER BY year), 3) AS per_line_ratio
FROM y ORDER BY year;
```

<!-- RESULT -->

| year | sales_lines | revenue_per_line | revenue_millions | lines_ratio | per_line_ratio |
|-----:|------------:|-----------------:|-----------------:|------------:|---------------:|
| 2023 |      300400 |           236.69 |             71.1 |        NULL |           NULL |
| 2024 |      500083 |           235.49 |            117.8 |       1.665 |          0.995 |

*(2 rows)*

<!-- /RESULT -->

Revenue +65.6% = lines ×1.665 × revenue per line ×0.995

👉 Growth is **all volume**: more transactions, not bigger ones. That's a different story (and different action) than "customers spend more"

---

# 🤨 Step 4: Too Good to Be True? Check Before You Present

Before presenting a surprising driver, check whether the **data changed** rather than the business:

- Did the **recording** change? (e.g. one line per item → one line with a quantity)
- Did a **definition** change? (returns included / excluded)
- Did a **source** change? (new system, new channel, corrected re-send)
- Are there **impossible values**? (quantity 0, negative prices)

👉 Look at the **distribution** behind an average, not just the average

---

# 📉 Step 5: Charts That Don't Lie

| Misleading | Honest |
|---|---|
| total that mixes new + old scope ("revenue doubled!") | like-for-like + new scope shown separately |
| `AVG()` of a ratio across rows of different size | ratio of sums (`SUM(revenue) / SUM(orders)`) |
| truncated y-axis on bars | bars start at 0 (lines may zoom, with labels) |
| 12 colors, 3 chart types on one slide | one message per chart |
| % change on tiny bases | show the base (n) next to the % |

---

# 🧱 Step 6: Situation → Complication → Resolution

- **Situation**: what happened, one honest number
  *"In-store revenue grew X% like-for-like."*
- **Complication**: the tension, risk or open question
  *"…but growth came from Y, while Z is flat / a new channel is small / a data caveat."*
- **Resolution**: one recommendation + **the KPI that will prove it worked**
  *"Do A in 2017; success = KPI B reaches C by Q2."*

👉 One slide, ≤ 60 words, one chart. Details go in the appendix

---

# 📝 Step 7: Caveats Build Trust

A short footnote line:

> *Data: POS 2015–2016 + delivery app 2016 (June re-sent corrected). 23 order lines with quantity 0 flagged for review. Quantities per line recorded differently from 2016.*

- Shows you know your data
- Prevents the "wait, but…" that derails the meeting
- Lets the audience trust the numbers you **didn't** caveat

---

# ✅ Final-Presentation Checklist

- ☐ Every KPI has a card (formula, grain, additive?)
- ☐ Headline is like-for-like; new scope shown separately
- ☐ Growth decomposed into drivers
- ☐ Surprising numbers checked against the raw distribution
- ☐ Dashboard tiles = SQL numbers (no `AVG` of ratios)
- ☐ SCR slide with **one** recommendation and its KPI
- ☐ Caveats in a footnote
