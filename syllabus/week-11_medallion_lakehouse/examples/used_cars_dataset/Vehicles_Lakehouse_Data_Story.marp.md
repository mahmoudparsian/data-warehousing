---
marp: true
title: Craigslist Vehicles Lakehouse Data Story (DuckDB)
paginate: true
size: 16:9
---

# Craigslist Vehicles Lakehouse Data Story
### Bronze → Silver → Gold using DuckDB

![bg right:45% w:520](vehicles_lakehouse_etl_diagram.png)

---

## Why this dataset works for a lakehouse lesson

`vehicles.csv` is **large, wide, and messy**:
- many missing values
- many categorical columns
- heavy text fields (`description`)
- time (`posting_date`) and location (state/lat/long)

This is exactly why Bronze/Silver/Gold layers matter.

---

## Bronze layer (raw)

**Goal:** preserve raw data as received.

DuckDB Bronze:
- `CREATE VIEW bronze_vehicles AS read_csv_auto('vehicles.csv')`
- inspect schema + missingness
- avoid heavy transformations

Bronze answers: “What did we ingest?”

---

## Silver layer (trusted)

Silver turns raw rows into reliable analytics input:

- typed numerics: price/year/odometer/lat/long
- standardized categoricals (lower/trim)
- parsed timestamps: `posting_ts`, `posting_date`
- added features:
  - `posting_year`, `posting_month`
  - `vehicle_age`
  - `price_per_mile`

Silver answers: “What do we trust for analysis?”

---

## Gold layer (curated)

Gold provides BI-ready KPIs:

- listings per month
- median & p90 price trends
- average price trends
- median odometer trends

Gold answers: “What do stakeholders need repeatedly?”

---

## Insight patterns students learn

1) Trends (time series KPIs)  
2) Ranking (top manufacturers/states)  
3) Segmentation (fuel/transmission/age buckets)  
4) Robust stats (median, percentiles)  
5) Outlier discovery (top prices)

---

## Typical observations

- Listing volume varies over time
- Median price varies by market and mix of vehicles
- Age and odometer strongly influence price
- Price distribution is heavy-tailed (percentiles matter)

---

## Takeaways

- Bronze/Silver/Gold are **quality contracts**
- DuckDB enables “big-ish” analytics on a laptop
- Aggregation-first design avoids memory issues
- SQL patterns map cleanly to lakehouse workflows

---
