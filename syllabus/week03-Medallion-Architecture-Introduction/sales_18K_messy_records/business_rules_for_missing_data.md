# 🟡 Business Rules for Data Quality (Medallion Architecture)

## 📘 Purpose

This document defines the **business rules for handling messy data** in a Medallion Architecture pipeline.

These rules guide transformations from:
- 🟫 Bronze (raw data)
- ⚪ Silver (cleaned, validated data)
- 🟡 Gold (analytical layer)

---

# 🧠 Rule Classification

All rules are categorized into:

| Category | Meaning |
|----------|--------|
| 🟫 Deduplication | Remove duplicate records |
| ❌ Rejection | Drop invalid records |
| ⚠️ Cancellation | Keep but classify separately |
| 🔧 Imputation | Fix missing or invalid values |
| 🔄 Validation | Enforce consistency |
| 🧮 Derived Fields | Compute business metrics |

---

# 🟫 1. Deduplication Rules

- Exact duplicate records (all fields identical) → **DROP**

- Same `sale_id` but different values →  
  → **Flag for inconsistency OR keep latest record (based on timestamp)**

---

# ❌ 2. Rejection Rules (Invalid Records)

Drop record if ANY of the following is true:

- `product_name` is NULL or missing  
- `customer_email` is NULL or does not contain '@'  
- `quantity` ≤ 0 or not an integer  
- `unit_price` ≤ 0 or NULL  
- `cost_price` ≤ 0 or NULL  
- `store_location` is NULL or not in allowed list  
- `sale_date` is NULL, malformed, or invalid  
- `product_name` not in allowed product list  

---

# ⚠️ 3. Cancellation Rules

- If `sale_id` is NULL / missing / not an integer  
  → classify as **CANCELLED transaction**

- Cancelled records:
  - are NOT included in analytical tables
  - are stored separately for business insights

---

# 🔧 4. Imputation Rules (Fixable Data)

- `sales_channel` NULL → set to `'UNKNOWN'`
- `discount` NULL, negative, or invalid → set to `0.00`
- `customer_gender` not in {MALE, FEMALE, OTHER} → set to `UNKNOWN`

---

# 🔄 5. Validation Rules (Consistency Checks)

## 📅 Date Validation
- Allowed formats:
  - `MM/DD/YYYY`
  - `YYYY-MM-DD`
- Invalid formats → **DROP**
- Invalid calendar dates (e.g., Feb 30) → **DROP**

---

## 💰 Pricing Rules
- `discount` ≤ (`quantity * unit_price`)
- If discount exceeds total → cap at total value

---

## 📧 Email Rule
- Must contain `'@'`
- Otherwise → **DROP**

---

## 🌍 Domain Constraints
- `store_location` must be in allowed list
- `product_name` must be valid

---

## 🔗 Channel-Type Consistency

- If `sales_channel = STORE` → `sale_type = IN-STORE`
- If `sales_channel IN (WEB, MOBILE_APP)` → `sale_type = ON-LINE`

- Violations:
  → **Flag OR DROP (based on strictness level)**

---

## 🚚 Delivery Logic (if applicable)
- `delivery_date` ≥ `sale_date`
- Otherwise → **DROP**

---

# 🧮 6. Derived Fields (Silver / Gold)

## Final Sale Price
```
final_sale_price = (quantity * unit_price) - discount
```

## Total Cost
```
total_cost = quantity * cost_price
```

## Profit
```
profit = final_sale_price - total_cost
```

## Delivery Time
```
delivery_time_days = delivery_date - sale_date
```

---

# ⚠️ Notes for Implementation

- All string fields should be:
  - `TRIM()` → remove whitespace
  - `UPPER()` → for categorical values
  - `LOWER()` → for email fields

- Rejection, cancellation, and valid data should be stored in **separate tables**

---

# 🎯 Final Goal

After applying these rules:

- Silver layer contains **trusted, clean data**
- Gold layer enables **accurate business analytics**
- Data pipeline is **auditable and explainable**

---

## 👍 Next Step

Review and refine rules before generating the dataset.
