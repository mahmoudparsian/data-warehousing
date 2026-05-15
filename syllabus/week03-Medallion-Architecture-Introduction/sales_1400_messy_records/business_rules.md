# Data and Business Rules

# 0. Sample Data

```text
% head sale_records_1400_messy.csv
sale_id,sale_type,product,customer_name,customer_email,customer_country,quantity,unit_price,discount,store_location,sale_date
1,ON-LINE,IPAD,Megan Carter,megan.carter83@outlook.com,USA,1,700,0.00,USA,06/21/2025
2,ON-LINE,IPAD,Kevin Johnson,kevin.johnson34@yahoo.com,USA,1,700,0.00,USA,11/08/2025
3,ON-LINE,COMPUTER,Rebecca White,rebecca.white18@proton.me,USA,1,1400,0.00,USA,11/23/2025
4,IN-STORE,WATCH,Jack Gonzalez,jack.gonzalez6@yahoo.com,GERMANY,2,250,60.00,USA,11/13/2025
5,ON-LINE,IPHONE,Ryan Jackson,ryan.jackson94@proton.me,CANADA,3,1100,396.00,CANADA,08/01/2025
6,IN-STORE,COMPUTER,Megan Wilson,megan.wilson17@outlook.com,CANADA,3,1400,210.00,ENGLAND,10/24/2025
7,IN-STORE,IPHONE,Jason Perez,jason.perez28@outlook.com,USA,1,1100,88.00,USA,01/11/2025
8,ON-LINE,IPAD,Jeffrey Parker,jeffrey.parker39@proton.me,MEXICO,2,700,0.00,ENGLAND,12/18/2025
9,ON-LINE,WATCH,George Stewart,george.stewart40@yahoo.com,ENGLAND,1,250,0.00,CANADA,04/15/2025
```

# 1. Business Rule: `sale_id`

```
> # 1. if a sale_id is null/missing,
> then it means that the transaction is cancelled.
> This is important to know how many transactions
> are cancelled, and for which products?
```

# 2. Business Rule: `product`

```
> # 2. if a product is missing, then
> the entire record must be dropped
> (not a valid record)
> (it is not a cancelled transaction)
```

# 3. Business Rule: `customer_name`

```
> 3. if a customer_name is null/missing/empty,
> the entire record must be dropped
> (not a valid record)
> (it is not a cancelled transaction)
```

# 4. Business Rule: `discount`

```
> 4. if discount is null/missing/negative,
> then discount is set to 0.00 (zero)
```

# 5. Business Rule: `sale_date`

```
> 5. The sale_date might have the
> following sale formats:
>
>     12/31/2025
>     2025-12-31
>
> If the sale_date format is not one of the
> two formats, the entire record must be dropped
> (it is not a cancelled transaction)
```

# 6. Business Rule: `sale_date: NULL/missing`

```
> 6. If a sale_date is null/missing/malformed/invalid,
> the entire record must be dropped
> 
```

# 7. Business Rule: `deduplication`

> 7. deduplication, drop duplicate records:
> all record fields must be identical
```
```

# 8. email: convert to lowecase

# 9. customer_country: convert to uppercase

# 10: sale_type: convert to Uppercase
