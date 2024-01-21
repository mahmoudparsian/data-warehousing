# Designing Star Schema

source: https://learndatamodeling.com/blog/designing-star-schema/

# Star Schema: General Information

In general, an organization is started 
to earn money by selling a product or by 
providing service to the product. An 
organization may be at one place or may 
have several branches.

When we consider an example of an organization 
selling products throughout the world, the main 
four major dimensions are product, location, 
time and organization. 
[Dimension tables](https://learndatamodeling.com/blog/dimension-tables/)
have been explained in detail under the section 
Dimensions.
 
With this example, we will try to provide detailed 
explanation about STAR SCHEMA.

# What is Star Schema?
Star Schema is a relational database schema for 
representing multidimensional data. It is the simplest 
form of data warehouse schema that contains one or more 
dimensions and fact tables. 

It is called a star schema because the entity-relationship 
diagram between dimensions and fact tables resembles a star 
where one fact table is connected to multiple dimensions. 
The center of the star schema consists of a large fact table 
and it points towards the dimension tables. The advantage of 
star schema are slicing down, performance increase and easy 
understanding of data.

# Steps in designing Star Schema

1. Identify a business process for analysis(like sales).

2. Identify measures or facts (sales dollar).

3. Identify dimensions for facts(product dimension, 
   location dimension, time dimension, organization dimension).

4. List the columns that describe each dimension:
	* region name, 
	* branch name,
	* ...
	
5. Determine the lowest level of summary in a fact table (sales dollar).

# Important aspects of Star Schema & Snow Flake Schema

1. In a star schema every dimension will have a primary key.

2. In a star schema, a dimension table will not have any parent table.

3. Whereas in a snow flake schema, a dimension table will have one 
   or more parent tables.

4. Hierarchies for the dimensions are stored in the dimensional table 
   itself in star schema.

5. Whereas hierarchies are broken into separate tables in snow flake schema. 
  These hierarchies helps to drill down the data from topmost hierarchies to 
  the lowermost hierarchies.


# Glossary:

## Hierarchy: 
A logical structure that uses ordered levels as a 
means of organizing data. A hierarchy can be used 
to define data aggregation; for example, in a time 
dimension, a hierarchy might be used to aggregate 
data from the Month level to the Quarter level, from 
the Quarter level to the Year level. A hierarchy 
can also be used to define a navigational drill path, 
regardless of whether the levels in the hierarchy 
represent aggregated totals or not.

## Level: 
A position in a hierarchy. For example, a time 
dimension might have a hierarchy that represents 
data at the Month, Quarter, and Year levels.

## Fact Table:
A table in a star schema that contains facts and 
connected to dimensions. A fact table typically 
has two types of columns: those that contain facts 
and those that are foreign keys to dimension tables. 
The primary key of a fact table is usually a composite 
key that is made up of all of its foreign keys.

A fact table might contain either detail level 
facts or facts that have been aggregated (fact 
tables that contain aggregated facts are often 
instead called summary tables). A fact table 
usually contains facts with the same level of 
aggregation.

![](./https://learndatamodeling.com/wp-content/uploads/2015/07/star_schema.gif)


In the example sales fact table is connected to 
dimensions location, product, time and organization. 
It shows that data can be sliced across all dimensions 
and again it is possible for the data to be aggregated 
across multiple dimensions. Sales Dollar in sales fact 
table can be calculated across all dimensions independently 
or in a combined manner which is explained below.

* Sales Dollar value for a particular product.

* Sales Dollar value for a product in a location.

* Sales Dollar value for a product in a year within a location.

* Sales Dollar value for a product in a year within a location 
  sold or serviced by an employee
