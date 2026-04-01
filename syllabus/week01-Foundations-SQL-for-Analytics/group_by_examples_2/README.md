# GROUP BY Tutorial using DuckDB

1. Generate sales.csv for 1000,000 rows

Columns are:

```
transation_date: as a timestamp spanning for 3 years: 2023, 2024, 2025
product_name_ as: {TV, RADIO, TABLE, COMPUTER, BIKE, LAPTOP, WATCH, IPAD, EBIKE}
price: based on product
gender: MALE, FEMALE
country: USA, CANADA, GERMANY, INDIA, CHINA, MEXICO, ITALY, FRANCE, SPAIN
age: 18 to 70
```

Do not generate symmetric data, for example USA will have more sales than
any other country, 

The number of FEMALE will be 2 to 1

Product sales should not be even based on product name

2. Create a Notebook, which reads data,
then
2.1 create 10 cells: using "group by" 
* Give a business insight to each query
    -- monthly sales
    -- yearly sales
    -- sale by country
    -- sale by gender
    -- sale by age group
    ...
    
2.2 create 5 top-N queries
    * Give a business insight to each query
    
2.3 Add plotting for all queries


