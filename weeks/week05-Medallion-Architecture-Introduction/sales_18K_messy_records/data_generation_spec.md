# 🟡 Data Generation Specification (Medallion Architecture Dataset)

## 📘 Purpose

This document defines the **final specifications for generating a synthetic dataset** 
used for teaching:

- Medallion Architecture (Bronze → Silver → Gold)
- Data Warehousing (Star Schema)
- OLAP Analytics

The goal is to create a dataset that is:
- realistic
- intentionally messy
- analytically rich
- pedagogically effective

---

# 📊 Base Dataset Requirements

## 🔹 Volume
- 16,000 clean records

## 🔹 Date Range
- From: **2015-01-01**
- To: **2017-12-31**

## 🔹 Date Formats (for Bronze)
- `MM/DD/YYYY`
- `YYYY-MM-DD`

---

# 🧠 Data Distribution Design (CRITICAL)

## 🔥 1. Time Skew (Realistic Behavior)

The dataset must NOT be uniformly distributed.

### Requirements:
- **Higher sales in November and December**
- **Lower sales in January and February**
- Occasional spikes (simulating promotions)

---

## 🔥 2. Customer Behavior Skew

Total customers: **500**

### Distribution:
- Top 10 customers → **20–30% of total transactions**
- Some customers → 1 transaction only
- Some → frequent buyers

---

## 🔥 3. Geographic Distribution

### Countries:
USA, CHINA, CANADA, MEXICO, ITALY, GERMANY, FRANCE, ENGLAND, INDIA

### Skew:
- Higher frequency: **USA, CHINA, GERMANY**

---

# 🛍️ Product Design

Products:
TV, MACBOOK, COMPUTER, WATCH, IPHONE, IPAD,  
EBIKE, BIKE, HELMET, SCOOTER, HEADPHONES

---

## 🔥 Product Pricing

Define realistic ranges per product.

---

## 🔥 Cost Price

- `cost_price = 60% – 80% of unit_price`

---

# 🏪 Store Design

Locations:
USA, CANADA, ENGLAND, CHINA

---

# 🔗 Channel vs Sale Type Logic

Most rows follow mapping, some intentionally violate.

---

# 💰 Discount Distribution

- Most: 0
- Some: small
- Few: large

---

# 🔁 Duplicate Strategy

- 420 exact duplicates
- Additional conflicting duplicates

---

# ⚠️ Cancelled Records

- 630 records with NULL sale_id

---

# 🧪 Messy Data Injection

- 50–100 records per rule
- mix of single + multi-error rows

---

# 🧾 Data Quality Variations

- casing issues
- whitespace
- type mismatches
- invalid formats

---

# 🎯 Final Objective

Enable full Medallion pipeline + OLAP analytics
