# Key differences: OLAP vs. OLTP

### OLAP = online analytical processing

### OLTP = online transaction processing

[According to Amazon](https://aws.amazon.com/compare/the-difference-between-olap-and-oltp/#:~:text=OLAP%20databases%20store%20data%20in,focus%20on%20one%20data%20aspect.):
The primary purpose of online analytical processing (OLAP) 
is to analyze aggregated data, while the primary purpose of 
online transaction processing (OLTP) is to process database 
transactions.

You use OLAP systems to generate reports, perform complex 
data analysis, and identify trends. In contrast, you use 
OLTP systems to process orders, update inventory, and manage 
customer accounts.

Other major differences include data formatting, 
data architecture, performance, and requirements. 


|     | Data Warehouse (OLAP)                        | Operational Database (OLTP)               |
| --- | -------------------------------------------- | ----------------------------------------- |
|  1  |Involves historical processing of information | Involves day-to-day processing            |
|  2  |OLAP systems are used by knowledge workers such as executives, managers, and analysts     | OLAP systems are used by clerks, DBAs, or database professionals |
|  3  |Useful in analyzing the business              | Useful in running the business    |
|  4  |It focuses on Information out                 | It focuses on Data in |
|  5  |Based on Star/Snowflake schema                | Based on Entitiy-Relationship Model |
|  6  |Contains historical data                      | Contains current data |
|  7  |Provides summarized and consolidated data     | Provides primitive and highly detailed data |
|  8  |Provides summarized and multidimensional view of data     | Provides detailed and flat relational view of data |
|  9  |Number of users in hundreds     | Number of users in thousands |
|  10 |Number of records accessed in millions     | Number of records accessed in tens |
|  11 |Database size is from 100 GB to 100 TB     | Database size is from 100 MB to 100 GB |
|  12 |Highly flexible                      | Provides high performance|
|  13 |Result of queries returned in 1 to 10 seconds | Result of queries returned in 1 to 2 seconds |



