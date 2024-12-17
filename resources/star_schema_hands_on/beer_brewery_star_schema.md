source: https://danischnider.wordpress.com/2022/11/10/star-schema-design-in-oracle-fundamentals/

For this blog post series, I will use an example of a star schema with one fact table and four dimension tables. We want to have an overview of beer deliveries of a craft beer brewery to multiple customers. All customer related descriptions are stored in the dimension table DIM_CUSTOMER. The different beers of the craft beer brewery are defined in dimension table DIM_BEER. Each delivery contains a set of bottles from the bottling of a specific brew batch on a particular day. The bottling information is stored in dimension table DIM_BOTTLING. Finally, we have a dimension table DIM_DATE. This kind of calendar dimension typically exists in each star schema. The fact table FACT_BEER_DELIVERY consists of dimension keys to refer the four dimension table, as well as some measurements, e.g. the number of bottles.

A typical query in a star schema joins the fact table with one or more dimension tables and group the data by descriptive columns of the dimensions. The dimension columns are also used to filter the facts. The measurements are aggregated, usually with a SUM function.

With the following query, we want to find out how many bottles of India Pale Ale were delivered in 2020 to private customers. The facts is grouped by beer name, city of the delivery address and calendar month:

 
SELECT b.beer_name
     , c.delivery_city
     , d.calendar_month_desc
     , SUM(f.number_of_bottles)
  FROM fact_beer_delivery f
  JOIN dim_beer b     ON (b.beer_id = f.beer_id)
  JOIN dim_customer c ON (c.customer_id = f.customer_id)
  JOIN dim_date d     ON (d.date_id = f.delivery_date)
 WHERE d.calendar_year = 2020
   AND c.private_person = 'Y'
   AND b.style = 'India Pale Ale'
GROUP BY 
       b.beer_name
     , c.delivery_city
     , d.calendar_month_desc
 
For this example star schema, we now want to have a look how the physical database design in an Oracle database should be implemented. First, let’s have a look at constraints and indexes.


