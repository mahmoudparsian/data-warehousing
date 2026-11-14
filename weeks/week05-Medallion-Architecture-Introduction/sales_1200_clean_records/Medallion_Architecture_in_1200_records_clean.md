# Medallion Architecture in 1200 records.


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

* 1200 records
* 100 real-looking customers
* skewed purchasing behavior
* strong sales concentration in November and December 2025
* intentionally imbalanced data
* all fields valid and clean for now

## Generated data:

Files:

* `medallion_sales_1200.csv￼`
* `medallion_sales_1200_summary.txt￼`

What’s included:

* 1200 clean records
* exactly 100 customers
* real-looking customer names and emails
* skewed customer purchasing behavior
* heavier transaction volume in November and December 2025
* intentionally unbalanced product/store/channel distribution
* discount stored as a dollar amount for the whole transaction

A quick sanity check from the generated data:

* total records: 1200
* unique customers: 100
* strongest month: November 2025 with 259 sales
* next strongest month: December 2025 with 192 sales
* dominant customers are clearly present

