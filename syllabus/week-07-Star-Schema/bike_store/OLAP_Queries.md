# OLAP Queries with a Star Schema 

## Star Schema on MySQL 

~~~sql
-- -------------------------
-- Dimension Table: Products
-- -------------------------
CREATE TABLE Products (
    Product_ID INT PRIMARY KEY AUTO_INCREMENT,
    Product_Name VARCHAR(100) NOT NULL,
    Category VARCHAR(20) NOT NULL
);

-- --------------------------
-- Dimension Table: Customers
-- --------------------------
CREATE TABLE Customers (
    Customer_ID INT PRIMARY KEY AUTO_INCREMENT,
    Customer_Name VARCHAR(100) NOT NULL
);

-- ----------------------
-- Dimension Table: Dates
-- ----------------------
CREATE TABLE Dates (
    Date_ID INT PRIMARY KEY AUTO_INCREMENT,
    Date DATE NOT NULL,
    Year INT NOT NULL,
    Month INT NOT NULL
);

-- ----------------------
-- Fact Table: SalesFact
-- ----------------------
CREATE TABLE SalesFact (
    Sale_ID INT PRIMARY KEY AUTO_INCREMENT,
    Product_ID INT NOT NULL,
    Customer_ID INT NOT NULL,
    Date_ID INT NOT NULL,
    Quantity INT NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (Product_ID) REFERENCES Products(Product_ID),
    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID),
    FOREIGN KEY (Date_ID) REFERENCES Dates(Date_ID)
);
~~~

## 30 OLAP Queries

* Use GROUP BY, sub-queries, joins, and ranking functions.
* Cover a range of analytical scenarios typical in OLAP analysis
* 10 simple 
* 10 intermediate
* 10 complex


-----

## Simple Queries

### 1.  Total sales amount per customer:

This query calculates the sum of sales amounts for each customer.

```sql
    SELECT
        c.Customer_Name,
        SUM(sf.Amount) AS TotalSalesAmount
    FROM
        SalesFact sf
    JOIN
        Customers c ON sf.Customer_ID = c.Customer_ID
    GROUP BY
        c.Customer_Name
    ORDER BY
        TotalSalesAmount DESC;
```

------

### 2.  Total quantity of each product sold:
    
This query shows the total number of units sold for each product.

```sql
    SELECT
        p.Product_Name,
        SUM(sf.Quantity) AS TotalQuantitySold
    FROM
        SalesFact sf
    JOIN
        Products p ON sf.Product_ID = p.Product_ID
    GROUP BY
        p.Product_Name
    ORDER BY
        TotalQuantitySold DESC;
```

------

### 3.  Number of sales transactions per specific date:
    
		This query counts the number of individual 
		sales transactions that occurred on each date 
		present in the `Dates` table.

```sql
    SELECT
        d.Date,
        COUNT(sf.Sale_ID) AS NumberOfTransactions
    FROM
        SalesFact sf
    JOIN
        Dates d ON sf.Date_ID = d.Date_ID
    GROUP BY
        d.Date
    ORDER BY
        d.Date;
```

------

### 4.  Average sales amount per product category:

    This query calculates the average sales amount 
    for products within each category.


 ```sql
    SELECT
        p.Category,
        AVG(sf.Amount) AS AverageSalesAmount
    FROM
        SalesFact sf
    JOIN
        Products p ON sf.Product_ID = p.Product_ID
    GROUP BY
        p.Category
    ORDER BY
        AverageSalesAmount DESC;
 ```
 
 ------

### 5.  Total sales amount for each month:

    		This query aggregates total sales amounts 
    		by month and year.
    
```sql
    SELECT
        d.Month AS SalesMonth, 
        SUM(sf.Amount) AS TotalMonthlySales
    FROM
        SalesFact sf
    JOIN
        Dates d ON sf.Date_ID = d.Date_ID
    GROUP BY
        SalesMonth
    ORDER BY
        SalesMonth;
```

------

### 6. Total Sales per Product

```sql
SELECT P.Product_Name, 
       SUM(S.Quantity) AS Total_Quantity, 
       SUM(S.Amount) AS Total_Sales
FROM 
     SalesFact S
JOIN 
     Products P ON S.Product_ID = P.Product_ID
GROUP BY 
    P.Product_Name;
```

------

### 7. Total Sales per Customer

```sql
SELECT C.Customer_Name, 
       SUM(S.Amount) AS Total_Sales
FROM 
     SalesFact S
JOIN 
     Customers C ON S.Customer_ID = C.Customer_ID
GROUP BY 
     C.Customer_Name;
```

------

### 8. Total Sales per Year

```sql
SELECT D.Year, 
       SUM(S.Amount) AS Total_Sales
FROM 
     SalesFact S
JOIN 
     Dates D ON S.Date_ID = D.Date_ID
GROUP BY 
     D.Year;
```

------

###  9. Total Sales per Month

```sql
SELECT D.Month, 
       SUM(S.Amount) AS Total_Sales
FROM 
     SalesFact S
JOIN 
     Dates D ON S.Date_ID = D.Date_ID
GROUP BY
     D.Month;
```

------

### 10. Count of Sales Transactions per Product

```sql
SELECT P.Product_Name, 
       COUNT(S.Sale_ID) AS Transactions_Count
FROM 
     SalesFact S
JOIN 
     Products P ON S.Product_ID = P.Product_ID
GROUP BY 
     P.Product_Name;
```

-----

## Intermediate Queries

### 1.  Top 3 products by total sales amount using RANK():

    This query identifies the top 3 products 
    based on their total revenue generated.

```sql
    WITH ProductSales AS (
        SELECT
            p.Product_Name,
            SUM(sf.Amount) AS TotalSalesAmount,
            RANK() OVER (ORDER BY SUM(sf.Amount) DESC) AS SalesRank
        FROM
            SalesFact sf
        JOIN
            Products p ON sf.Product_ID = p.Product_ID
        GROUP BY
            p.Product_Name
    )
    SELECT
        Product_Name,
        TotalSalesAmount,
        SalesRank
    FROM
        ProductSales
    WHERE
        SalesRank <= 3;
```

### 2.  Customers whose total purchase amount is above the average total purchase amount of all customers:

    This query lists customers who have spent 
    more than the average customer.

```sql
    SELECT
        c.Customer_Name,
        SUM(sf.Amount) AS CustomerTotalAmount
    FROM
        SalesFact sf
    JOIN
        Customers c ON sf.Customer_ID = c.Customer_ID
    GROUP BY
        c.Customer_Name
    HAVING
        SUM(sf.Amount) > (
            SELECT AVG(TotalAmountPerCustomer)
            FROM (
                SELECT SUM(Amount) AS TotalAmountPerCustomer
                FROM SalesFact
                GROUP BY Customer_ID
            ) AS CustomerTotals
        )
    ORDER BY
        CustomerTotalAmount DESC;
```

-----

### 3.  Monthly sales trend for a specific category (e.g., 'Electronics')

    This query shows how sales for a particular product category 
    have trended month over month.

```sql
    SELECT
        p.Category,
        d.Month AS SalesMonth, 
        SUM(sf.Amount) AS MonthlyCategorySales
    FROM
        SalesFact sf
    JOIN
        Dates d ON sf.Date_ID = d.Date_ID
    JOIN
        Products p ON sf.Product_ID = p.Product_ID
    WHERE
        p.Category = 'Electronics' -- Example Category
    GROUP BY
        p.Category, SalesMonth
    ORDER BY
        SalesMonth;
```

------

### 4.  Customers who purchased items in more than 2 different categories:

    This query identifies customers with diverse purchasing 
    behavior across categories.

```sql
    SELECT
        c.Customer_Name,
        COUNT(DISTINCT p.Category) AS DistinctCategoriesPurchased
    FROM
        SalesFact sf
    JOIN
        Customers c ON sf.Customer_ID = c.Customer_ID
    JOIN
        Products p ON sf.Product_ID = p.Product_ID
    GROUP BY
        c.Customer_Name
    HAVING
        COUNT(DISTINCT p.Category) > 2
    ORDER BY
        DistinctCategoriesPurchased DESC;
```

-----

### 5.  List categories and the number of unique products sold within each:

    This query helps understand the product variety sold per category.


```sql
    SELECT
        p.Category,
        COUNT(DISTINCT sf.Product_ID) AS UniqueProductsSold
    FROM
        SalesFact sf
    JOIN
        Products p ON sf.Product_ID = p.Product_ID
    GROUP BY
        p.Category
    ORDER BY
        UniqueProductsSold DESC;
```

----

### 6. Average Sales per Product

```sql
SELECT P.Product_Name, 
       AVG(S.Amount) AS Avg_Sales
FROM 
     SalesFact S
JOIN 
     Products P ON S.Product_ID = P.Product_ID
GROUP BY 
     P.Product_Name;
```

------

### 7. Top-5 Highest Revenue Generating Products

```sql
SELECT P.Product_Name, 
       SUM(S.Amount) AS Total_Revenue
FROM 
     SalesFact S
JOIN 
     Products P ON S.Product_ID = P.Product_ID
GROUP BY 
     P.Product_Name
ORDER BY 
     Total_Revenue DESC
LIMIT 
     5;
```

------

### 8. Customer with the Highest Spending

```sql
SELECT C.Customer_Name, 
       SUM(S.Amount) AS Total_Spending
FROM 
     SalesFact S
JOIN 
     Customers C ON S.Customer_ID = C.Customer_ID
GROUP BY 
     C.Customer_Name
ORDER BY 
     Total_Spending DESC
LIMIT 1;
```

------

### 9. Top 3 Months with Highest Sales

```sql
SELECT D.Month, 
       SUM(S.Amount) AS Total_Sales
FROM 
     SalesFact S
JOIN 
     Dates D ON S.Date_ID = D.Date_ID
GROUP BY 
     D.Month
ORDER BY 
     Total_Sales DESC
LIMIT 
     3;
```

### 10. Products with Sales Higher than the Average

```sql
SELECT P.Product_Name, 
       SUM(S.Amount) AS Total_Sales
FROM 
     SalesFact S
JOIN 
     Products P ON S.Product_ID = P.Product_ID
GROUP BY 
     P.Product_Name
HAVING 
     Total_Sales > (SELECT AVG(Amount) FROM SalesFact);
```

-----

## Complex Queries

### 1.  For each customer, find their most frequently purchased product category and the count of purchases in that category:

    This query uses a subquery and window function to determine 
    the top category for each customer.

```sql
    WITH CustomerCategoryCounts AS (
        SELECT
            sf.Customer_ID,
            p.Category,
            COUNT(*) AS PurchaseCount,
            ROW_NUMBER() OVER (PARTITION BY sf.Customer_ID ORDER BY COUNT(*) DESC) as rn
        FROM
            SalesFact sf
        JOIN
            Products p ON sf.Product_ID = p.Product_ID
        GROUP BY
            sf.Customer_ID, p.Category
    )
    SELECT
        c.Customer_Name,
        ccc.Category AS MostFrequentCategory,
        ccc.PurchaseCount
    FROM
        CustomerCategoryCounts ccc
    JOIN
        Customers c ON ccc.Customer_ID = c.Customer_ID
    WHERE
        ccc.rn = 1
    ORDER BY
        c.Customer_Name;
```

----

### 2.  Calculate the year-over-year sales growth percentage for each product category:

    This query uses `LAG()` to compare sales with the previous year.

```sql
    WITH YearlyCategorySales AS (
        SELECT
            p.Category,
            d.Year AS SalesYear,
            SUM(sf.Amount) AS YearlySales
        FROM
            SalesFact sf
        JOIN
            Products p ON sf.Product_ID = p.Product_ID
        JOIN
            Dates d ON sf.Date_ID = d.Date_ID
        GROUP BY
            p.Category, SalesYear
    ),
    LaggedSales AS (
        SELECT
            Category,
            SalesYear,
            YearlySales,
            LAG(YearlySales, 1, 0) OVER (PARTITION BY Category ORDER BY SalesYear) AS PreviousYearSales
        FROM
            YearlyCategorySales
    )
    SELECT
        Category,
        SalesYear,
        YearlySales,
        PreviousYearSales,
        CASE
            WHEN PreviousYearSales = 0 THEN NULL -- Avoid division by zero, or show 100% if appropriate
            ELSE (YearlySales - PreviousYearSales) * 100.0 / PreviousYearSales
        END AS GrowthPercentage
    FROM
        LaggedSales
    ORDER BY
        Category, SalesYear;
```

-----

### 3.  Identify "high-value" customers: customers whose average transaction amount is in the top 10% of all customers' average transaction amounts.

    This query uses `NTILE` to segment customers.

```sql
    WITH CustomerAvgTransaction AS (
        SELECT
            c.Customer_ID,
            c.Customer_Name,
            AVG(sf.Amount) AS AvgTransactionAmount
        FROM
            SalesFact sf
        JOIN
            Customers c ON sf.Customer_ID = c.Customer_ID
        GROUP BY
            c.Customer_ID, c.Customer_Name
    ),
    RankedCustomerAvg AS (
        SELECT
            Customer_Name,
            AvgTransactionAmount,
            NTILE(10) OVER (ORDER BY AvgTransactionAmount DESC) AS Decile
        FROM
            CustomerAvgTransaction
    )
    SELECT
        Customer_Name,
        AvgTransactionAmount
    FROM
        RankedCustomerAvg
    WHERE
        Decile = 1 -- Top 10%
    ORDER BY
        AvgTransactionAmount DESC;
```

-----

### 4.  Rank customers within each product category by their total spending in that category, showing the top spender for each category.

    This provides a leader for spending within each product segment.

```sql
    WITH CustomerCategorySpending AS (
        SELECT
            c.Customer_Name,
            p.Category,
            SUM(sf.Amount) AS TotalSpentInCategory,
            RANK() OVER (PARTITION BY p.Category ORDER BY SUM(sf.Amount) DESC) AS RankInCategory
        FROM
            SalesFact sf
        JOIN
            Customers c ON sf.Customer_ID = c.Customer_ID
        JOIN
            Products p ON sf.Product_ID = p.Product_ID
        GROUP BY
            c.Customer_Name, p.Category
    )
    SELECT
        Customer_Name,
        Category,
        TotalSpentInCategory
    FROM
        CustomerCategorySpending
    WHERE
        RankInCategory = 1
    ORDER BY
        Category, TotalSpentInCategory DESC;
```

------

### 5.  Calculate the 3-month moving average of total sales amount across all sales:

    This query provides a smoothed sales trend over time.

```sql
    WITH MonthlySales AS (
        SELECT
            d.Year AS SalesYear, 
            d.Month AS SalesMonth, 
            SUM(sf.Amount) AS TotalAmount
        FROM
            SalesFact sf
        JOIN
            Dates d ON sf.Date_ID = d.Date_ID
        GROUP BY
            SalesYear, 
            SalesMonth
        ORDER BY
            SalesYear,
            SalesMonth
    )
    SELECT
       SalesYear,
       SalesMonth,
        TotalAmount,
        AVG(TotalAmount) OVER (ORDER BY SalesYear, SalesMonth ASC ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS MovingAvg3Months
    FROM
        MonthlySales
    ORDER BY
      SalesYear,
      SalesMonth;
```

------

### 6. Rank Products Based on Sales

```sql
SELECT P.Product_Name, 
       SUM(S.Amount) AS Total_Sales, 
       RANK() OVER (ORDER BY SUM(S.Amount) DESC) AS Sales_Rank
FROM 
     SalesFact S
JOIN 
     Products P ON S.Product_ID = P.Product_ID
GROUP BY 
     P.Product_Name;
```

------

### 7. Running Total Sales per Month

```sql
SELECT D.Month, 
       SUM(S.Amount) AS Total_Sales, 
       SUM(S.Amount) OVER (ORDER BY D.Month) AS Running_Total
FROM 
     SalesFact S
JOIN 
     Dates D ON S.Date_ID = D.Date_ID
GROUP BY 
     D.Month
ORDER BY 
     D.Month;
```

-----

### 8. Top-5 Customers per Year using Ranking Function

```sql
SELECT D.Year, 
       C.Customer_Name, 
       SUM(S.Amount) AS Total_Spending, 
       RANK() OVER (PARTITION BY D.Year ORDER BY SUM(S.Amount) DESC) AS year_rank
FROM 
     SalesFact S
JOIN 
     Customers C ON S.Customer_ID = C.Customer_ID
JOIN 
     Dates D ON S.Date_ID = D.Date_ID
GROUP BY 
     D.Year, C.Customer_Name
HAVING 
     year_rank <= 5;
```

-----


### 9. Percentage Contribution of Each Product to Total Sales

```sql
SELECT P.Product_Name, 
       SUM(S.Amount) AS Product_Sales, 
       (SUM(S.Amount) / (SELECT SUM(Amount) FROM SalesFact)) * 100 AS Sales_Percentage
FROM 
     SalesFact S
JOIN 
     Products P ON S.Product_ID = P.Product_ID
GROUP BY 
     P.Product_Name;
```

-----

### 10. Month-over-Month Sales Growth Rate

```sql
SELECT D.Month, 
       SUM(S.Amount) AS Current_Month_Sales, 
       LAG(SUM(S.Amount)) OVER (ORDER BY D.Month) AS Previous_Month_Sales,
       ((SUM(S.Amount) - LAG(SUM(S.Amount)) OVER (ORDER BY D.Month)) / 
       LAG(SUM(S.Amount)) OVER (ORDER BY D.Month)) * 100 AS Growth_Rate
FROM 
     SalesFact S
JOIN 
     Dates D ON S.Date_ID = D.Date_ID
GROUP BY 
     D.Month
ORDER BY 
     D.Month;
```

