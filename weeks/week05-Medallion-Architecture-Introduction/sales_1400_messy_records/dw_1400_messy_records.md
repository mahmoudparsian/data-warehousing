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

## Rules of Business for a Data Warehousing:

### RULE-1:
if a `sale_id` is null/missing, 

* then it means that the transaction is cancelled.
* This is important to know how many transactions 
are cancelled, and for which products?


### RULE-2:
if a product is missing, then 

* the entire record must be dropped 
* it is not a valid record
* it is not a cancelled transaction

### RULE-3:
if a customer_name is null/missing/empty,

* then entire record must be dropped 
* it is not a valid record
* it is not a cancelled transaction

### RULE-4: 
if discount filed/column is null/missing/negative,

* then discount is set to 0.00 (zero)

### RULE-5:
The `sale_dat`e might have the 
following sale formats:


    		12/31/2025
    		
    		2025-12-31

* If the sale_date format is not one of the 
two formats, the entire record must be dropped 

### RULE-6:
If a `sale_date` is null/missing/malformed/invalid,

* then entire record must be dropped 
* it is not a cancelled transaction

### RULE-7:
deduplication, drop duplicate records:

* drop a record if all record fields are identical

### RULE-8:
The final sale price of a transaction is computed by

		(quantity * unit_price) - discount



