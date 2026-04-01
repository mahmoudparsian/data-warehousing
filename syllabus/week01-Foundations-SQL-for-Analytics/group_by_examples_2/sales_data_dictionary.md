---
marp: true
theme: default
title: Sales Dataset — Data Dictionary & Business Rules
paginate: true
author: Mahmoud Parsian
---

# 📊 Sales Dataset  
## Data Dictionary & Business Rules

---

# 🧱 Dataset Overview

This dataset represents transactional retail sales across multiple countries over 3 years (2023–2025).

### Key Characteristics:
- ~1,000,000 rows
- Skewed distributions (realistic)
- Includes pricing, discounts, and demographics

---

# 📦 Table: sales

| Column Name        | Type        | Description |
|------------------|------------|-------------|
| transaction_id    | INTEGER     | Unique identifier for each transaction |
| transaction_date  | TIMESTAMP   | Date and time of the transaction |
| product_name      | VARCHAR     | Product purchased |
| price             | DOUBLE      | Base price of the product |
| quantity          | INTEGER     | Number of items purchased |
| discount          | DOUBLE      | Discount applied (0 to 0.30) |
| gender            | VARCHAR     | Customer gender (FEMALE, MALE) |
| country           | VARCHAR     | Country of purchase |
| age               | INTEGER     | Customer age (18–70) |
| sales_amount      | DOUBLE      | Final transaction value |

---

# 🛍️ Product Domain

### Product Categories:
- TV
- RADIO
- TABLE
- COMPUTER
- BIKE
- LAPTOP
- WATCH
- IPAD
- EBIKE

---

# 🌍 Country Distribution

- USA (dominant market)
- INDIA, CHINA (large markets)
- CANADA, GERMANY (mid-tier)
- Others (smaller share)

---

# 👥 Customer Attributes

### Gender:
- FEMALE ≈ 66%
- MALE ≈ 34%

### Age:
- Range: 18–70

---

# 💰 Pricing Model

Each product has a fixed base price.

---

# 🔢 Quantity

- Values: 1 to 5
- Skewed distribution

---

# 🏷️ Discount Model

### Discount Range:
- 0% to 30%

---

# ⚙️ Discount Application

sales_amount = price * quantity * (1 - discount)

---

# 📊 Example

price = 1000  
quantity = 2  
discount = 0.10  

sales_amount = 1800

---

# 📈 Adjustments

- Weekend boost (~20%)
- Higher spending in USA, Germany, Canada

---

# 🧠 Notes

### Bronze Layer:
- Raw data only
- No derived fields

---

# 🥈 Silver Layer:
- Derive:
  - year
  - month
  - quarter
  - day_of_week

---

# 🎯 Key Takeaway

Raw data captures reality — Silver data makes it usable.
