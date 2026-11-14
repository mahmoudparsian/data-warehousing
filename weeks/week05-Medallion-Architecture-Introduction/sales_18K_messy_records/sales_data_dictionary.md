# 🟡 Sales Data Dictionary (Medallion Architecture Dataset)

## 📘 Purpose

This document defines: 

- all columns in the dataset
- their meaning and examples
- calculated fields
- important business distinctions (e.g., **`sale_type` vs `sales_channel`**)

👉 This ensures: 

- consistency in data generation
- clarity in business rules
- alignment across Bronze → Silver → Gold

------------------------------------------------------------------------

# 📊 Core Transaction Table (Raw / Bronze)

| Column Name      | Description                                      | Example |
|------------------|--------------------------------------------------|---------|
| sale_id          | Unique identifier for a transaction               | 1001 |
| sale_type        | How the sale is fulfilled                        | IN-STORE |
| sales_channel    | Customer interaction channel                     | WEB |
| product_name     | Product purchased                                | TV |
| product_category | Category of product                              | ELECTRONICS |
| product_brand    | Brand of product                                 | Apple |
| customer_name    | Full name of customer                            | John Smith |
| customer_email   | Email address                                    | john@email.com |
| customer_country | Country of residence                             | USA |
| customer_city    | City of residence                                | San Jose |
| customer_gender  | Gender of customer                               | MALE |
| customer_segment | Customer segment                                 | PREMIUM |
| quantity         | Number of units purchased                        | 2 |
| unit_price       | Price per unit (USD)                             | 900 |
| cost_price       | Cost per unit (USD)                              | 600 |
| discount         | Discount applied (USD, total transaction)        | 50 |
| store_location   | Country of store                                 | USA |
| store_region     | Region of store                                  | WEST |
| store_manager    | Manager of store                                 | Jay Smith |
| sale_date        | Transaction date                                 | 12/31/2025 |
| order_timestamp  | Exact time of order                              | 2025-12-31 14:35 |
| delivery_date    | Delivery date                                    | 2026-01-02 |
| order_status     | Order status                                     | COMPLETED |

# 🧠 Important Business Concepts

## 🔹 `sale_type` vs `sales_channel` (VERY IMPORTANT)

These are **NOT the same**.

### `sale_type` → fulfillment

-   IN-STORE → fulfilled at store
-   ON-LINE → fulfilled remotely

### `sales_channel` → customer interaction

-   STORE → walk-in
-   WEB → website
-   MOBILE_APP → mobile purchase

------------------------------------------------------------------------

## 📊 Example

| `sale_type` | `sales_channel` | `Meaning`                 |
|-----------|--------------|---------------------------------|
| IN-STORE  | STORE        | Walk-in purchase               |
| IN-STORE  | WEB          | Buy online, pick up in store   |
| ON-LINE   | WEB          | Website purchase               |
| ON-LINE   | MOBILE_APP   | Mobile app purchase            |
------------------------------------------------------------------------

## 🎯 Why this matters

This enables analysis like: 

- online browsing → in-store purchase
- mobile vs web behavior
- channel-driven revenue

------------------------------------------------------------------------

# 🧮 Calculated Fields (Silver / Gold)

These are **NOT stored in Bronze** --- they are derived in Silver or
Gold.

------------------------------------------------------------------------

## 🔹 1. `final_sale_price`

    final_sale_price = (quantity * unit_price) - discount

------------------------------------------------------------------------

## 🔹 2. `total_cost`

    total_cost = quantity * cost_price

------------------------------------------------------------------------

## 🔹 3. `profit`

    profit = final_sale_price - total_cost

------------------------------------------------------------------------

## 🔹 4. `delivery_time_days`

    delivery_time_days = delivery_date - sale_date

------------------------------------------------------------------------

## 🔹 5. `is_discount_applied` (optional)

    is_discount_applied = (discount > 0)

------------------------------------------------------------------------

# ⚠️ Notes for Data Generation

These rules guide how we will create messy data later:

-   some fields will contain:
    -   NULL values
    -   invalid formats
    -   inconsistent casing
-   some records will be:
    -   duplicates
    -   partially missing
-   some fields will violate business rules intentionally

👉 These will be handled in the **Silver layer**

------------------------------------------------------------------------

# 🧠 Final Takeaway

This metadata document defines:

-   **what the data means**
-   **how fields relate to business concepts**
-   **what will be computed later**
-   **what transformations are expected**

👉 This is the foundation for: 

- business rules
- data cleaning (Silver)
- analytics (Gold)

------------------------------------------------------------------------

## 👍 Next Step

👉 **Business Rules Definition (Messy Data Design)**
