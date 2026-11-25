# Business Rules: 1,400 Messy Sales

These are the rules the **business** agreed on for `sale_records_1400_messy.csv`. Silver turns each rule into SQL.
Words as in [Medallion in a nutshell](../Medallion_Architecture_in_a_Nutshell.md): every row is **valid**, **flagged**, **rejected**
(quarantined in `silver.rejected` with a reason) or a **duplicate** (removed and counted). No row is lost without a count and a reason.

## Sample data

```text
% head sale_records_1400_messy.csv
sale_id,sale_type,product,customer_name,customer_email,customer_country,quantity,unit_price,discount,store_location,sale_date
1,ON-LINE,IPAD,Megan Carter,megan.carter83@outlook.com,USA,1,700,0.00,USA,06/21/2025
2,ON-LINE,IPAD,Kevin Johnson,kevin.johnson34@yahoo.com,USA,1,700,0.00,USA,11/08/2025
3,ON-LINE,COMPUTER,Rebecca White,rebecca.white18@proton.me,USA,1,1400,0.00,USA,11/23/2025
4,IN-STORE,WATCH,Jack Gonzalez,jack.gonzalez6@yahoo.com,GERMANY,2,250,60.00,USA,11/13/2025
5,ON-LINE,IPHONE,Ryan Jackson,ryan.jackson94@proton.me,CANADA,3,1100,396.00,CANADA,08/01/2025
```

## The rules

| # | Column | Rule | Fate of the row |
|---|---|---|---|
| 1 | `sale_id` | missing → the sale was **cancelled**. We must know how many sales were cancelled, and for which products. | **flagged**: kept in `silver.sales` with `is_cancelled = true` |
| 2 | `product` | missing → not a valid record (and **not** a cancellation) | **rejected**: `silver.rejected`, reason "R2 missing product" |
| 3 | `customer_name` | missing or empty → not a valid record (not a cancellation) | **rejected**: reason "R3 missing customer name" |
| 4 | `discount` | missing or negative → set to 0.00 | fixed; the row stays valid |
| 5 | `sale_date` | only two formats are valid: `12/31/2025` (`MM/DD/YYYY`) and `2025-12-31` (`YYYY-MM-DD`) | any other format → **rejected** |
| 6 | `sale_date` | missing, malformed, or not a real date (`2025-02-30`) | **rejected**: reason "R5-6 missing or invalid date" |
| 7 | all columns | exact duplicate rows (every field identical) | **duplicate**: keep one copy, count the others |
| 8 | `final_sale_price` | `quantity * unit_price - discount` (after rule 4) | computed |
| 9 | `customer_email` | lower case | standardized |
| 10 | `customer_country` | upper case | standardized |
| 11 | `sale_type` | upper case | standardized |
| 12 | `product` | trimmed, upper case | standardized |

Rules 9–12 only change how a value is **written**; they never change a row's fate.

## Reconcile

After Silver, this must hold:

> **Bronze rows = valid + flagged (cancelled) + rejected + duplicates**

Gold uses only `silver.sales`, and uses the flag explicitly: revenue = `WHERE NOT is_cancelled`; cancellations = `WHERE is_cancelled`.

**Tip for rules 5–6:** check the shape before parsing (`sale_date LIKE '__/__/____'`): on its own, `try_strptime('31-12-25', '%Y-%m-%d')`
reads year 31 instead of failing.
