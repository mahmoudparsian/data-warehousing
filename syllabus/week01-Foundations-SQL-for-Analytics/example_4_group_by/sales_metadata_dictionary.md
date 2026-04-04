---
marp: true
theme: default
paginate: true
title: Sales Dataset Metadata Dictionary
---

# Sales Dataset Metadata Dictionary

## Business Rules
- USA has the highest transaction volume.
- FEMALE transactions are approximately 5:3 compared with MALE.
- Product mix is intentionally uneven.
- 2026 includes only January, February, and March.
- `sales_amount = (quantity * price) - discount`

---

# Column Dictionary

| Column | Domain / Rule | Notes |
|---|---|---|
| `transaction_id` | Integer | Not required to be unique |
| `transaction_date` | Timestamp | 2023–2025 full years; 2026 Jan–Mar only |
| `sale_type` | ONLINE, INSTORE | Channel indicator |
| `product_name` | ROBOT, TV, RADIO, TABLE, COMPUTER, BIKE, LAPTOP, WATCH, IPAD, EBIKE | Product categories |
| `price` | Integer | Product-dependent price range |
| `quantity` | 1, 2, 3, 4 | Number of units in transaction |
| `gender` | FEMALE, MALE | Approximate ratio 5:3 |
| `discount` | Integer currency amount | Total discount for the transaction |
| `country` | USA, CANADA, GERMANY, INDIA, CHINA, MEXICO, ITALY, FRANCE, SPAIN | USA dominates volume |
| `age` | Integer 18–80 | Customer age |
| `sales_amount` | Integer | Derived as `(quantity * price) - discount` |

---

# Product Pricing Logic

| Product | Typical Price Position |
|---|---|
| RADIO | Low |
| WATCH | Low to medium |
| TABLE | Medium |
| BIKE | Medium |
| TV | Medium to high |
| IPAD | Medium to high |
| COMPUTER | High |
| LAPTOP | High |
| ROBOT | High |
| EBIKE | High |

---

# Analytical Use Cases
- GROUP BY tutorials
- KPI design
- Top-N by year / country / product
- HAVING clause practice
- Window functions
- Data warehousing demonstrations
