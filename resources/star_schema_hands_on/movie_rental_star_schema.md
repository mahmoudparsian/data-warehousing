1. A star schema is a dimensional model built in a star configuration. 

2. The star schema typically contains one large table, called the fact table, placed in the center with smaller satellite tables, called dimension tables, joined to the fact table in a radial pattern. A star schema can, optionally, have an outrigger table joined to a dimension table.

3. The following example of a video rental store data warehouse illustrates dimensional modeling features. The REVENUE table is a fact table; Customer, Movie, Market, and Time are dimension tables; and District and Region are outrigger tables. The REVENUE fact table contains revenue data for movies rented by each customer, ina geographic market, over a period of time. The dimension tables in this database define the customers, movies, markets, and time periods used in the fact table.
