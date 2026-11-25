# Medallion Architecture in 1400 Messy records.


## 📊 Sales Dataset Schema


| Column Name        | Description                                              | Values / Notes |
|--------------------|----------------------------------------------------------|----------------|
| sale_id            | Unique transaction identifier for each sale              | Integer, unique |
| sale_type          | Type of sale                                             | IN-STORE, ON-LINE |
| product            | Product purchased                                        | TV, COMPUTER, WATCH, IPHONE, IPAD, EBIKE 
| customer_name      | Full name of the customer (realistic names)              | e.g., John Smith |
| customer_email     | Email address of the customer                            | e.g., john.smith@email.com |
| customer_country   | Country where the customer resides                       | USA, CHINA, CANADA, MEXICO, ITALY, GERMANY, FRANCE, ENGLAND |
| quantity           | Number of units purchased                                | Integer (≥ 1) |
| unit_price         | Price per unit                                           | Numeric (USD) |
| discount           | Discount applied to the entire transaction               | Numeric (USD, total amount — not percentage) |
| store_location     | Location of the store handling the transaction           | USA, CANADA, ENGLAND |
| sale_date          | Date of the transaction                                  | 01/01/2025 – 12/31/2025 |



## NOTES for creation of records:

1. All records have valid fields/columns
(later on I will add messy data)
   
2. there should be 100 customers, 
some buying more than others, 
some customers dominate

3. Transactions should be heavier for 
November 2025 and December 2025

4. Data should not be balanced at all

## CSV Data

* 1400 records
* 100 real-looking customers
* skewed purchasing behavior
* strong sales concentration in November and December 2025
* intentionally imbalanced data
* all fields valid and clean for now

## Generated data:

Files:

* `sale_records_1400_messy.csv`
* `sale_records_1400_messy.csv.with.annotation`


What’s included:

* 1400 messy records
* exactly 100 customers
* real-looking customer names and emails
* skewed customer purchasing behavior
* heavier transaction volume in November and December 2025
* intentionally unbalanced product/store/channel distribution
* discount stored as a dollar amount for the whole transaction

A quick sanity check from the generated data:

* total records: 1400
* unique customers: 100
* strongest month: November 2025 
* next strongest month: December 2025 
* dominant customers are clearly present


===============

# Added/Modified Data:

## Business rules

The full rules, each with the **fate** of the row (valid, flagged, rejected, duplicate), are in
[`business_rules.md`](business_rules.md). In short:

| # | Rule | Fate |
|---|---|---|
| 1 | missing `sale_id` = cancelled sale | **flagged** (kept in `silver.sales`, `is_cancelled = true`) |
| 2, 3 | missing `product` / `customer_name` | **rejected** (`silver.rejected`, with a reason) |
| 4 | missing or negative `discount` → 0.00 | fixed |
| 5, 6 | `sale_date` not `MM/DD/YYYY` / `YYYY-MM-DD`, missing, or impossible | **rejected** |
| 7 | exact duplicate rows | **duplicate** (removed, counted) |
| 8 | `final_sale_price = (quantity * unit_price) - discount` | computed |

Reconcile: **1,400 = 31 duplicates + 78 rejected + 33 flagged (cancelled) + 1,258 valid**; Gold revenue 1,985,249.50.



