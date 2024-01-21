source: https://learndatamodeling.com/blog/designing-star-schema/

Star Schem: General Information

<p>In general, an organization is started to earn money by selling a product or by providing service to the product. An organization may be at one place or may have several branches.</p>
<p>When we consider an example of an organization selling products throughout the world, the main four major dimensions are product, location, time and organization. Dimension tables have been explained in detail under the section <a href="https://learndatamodeling.com/blog/dimension-tables/">Dimensions</a>. With this example, we will try to provide detailed explanation about STAR SCHEMA.</p>
<h3><span style="color: #003366;">What is Star Schema?</span></h3>
<p>Star Schema is a relational database schema for representing multidimensional data. It is the simplest form of data warehouse schema that contains one or more dimensions and fact tables. It is called a star schema because the entity-relationship diagram between dimensions and fact tables resembles a star where one fact table is connected to multiple dimensions. The center of the star schema consists of a large fact table and it points towards the dimension tables. The advantage of star schema are slicing down, performance increase and easy understanding of data.</p>
<h4><span style="color: #003366;">Steps in designing Star Schema:</span></h4>
<ul>
<li>Identify a business process for analysis(like sales).</li>
<li>Identify measures or facts (sales dollar).</li>
<li>Identify dimensions for facts(product dimension, location dimension, time dimension, organization dimension).</li>
<li>List the columns that describe each dimension.(region name, branch name, region name).</li>
<li>Determine the lowest level of summary in a fact table(sales dollar).</li>
</ul>
<h4><span style="color: #003366;">Important aspects of Star Schema &amp; Snow Flake Schema:</span></h4>
<ul>
<li>In a star schema every dimension will have a primary key.</li>
<li>In a star schema, a dimension table will not have any parent table.</li>
<li>Whereas in a snow flake schema, a dimension table will have one or more parent tables.</li>
<li>Hierarchies for the dimensions are stored in the dimensional table itself in star schema.</li>
<li>Whereas hierarchies are broken into separate tables in snow flake schema. These hierarchies helps to drill down the data from topmost hierarchies to the lowermost hierarchies.</li>
</ul>

<h4><span style="color: #003366;">Glossary:</span></h4>
<p><span style="color: #800000;"><strong>Hierarchy: </strong></span>A logical structure that uses ordered levels as a means of organizing data. A hierarchy can be used to define data aggregation; for example, in a time dimension, a hierarchy might be used to aggregate data from the Month level to the Quarter level, from the Quarter level to the Year level. A hierarchy can also be used to define a navigational drill path, regardless of whether the levels in the hierarchy represent aggregated totals or not.</p>
<p><span style="color: #800000;"><strong>Level: </strong></span>A position in a hierarchy. For example, a time dimension might have a hierarchy that represents data at the Month, Quarter, and Year levels.</p>
<!-- WP QUADS Content Ad Plugin v. 2.0.80 -->
<div class="quads-location quads-ad2" id="quads-ad2" style="float:none;margin:1px;">

 <!-- WP Q
<p><span style="color: #800000;"><strong>Fact Table: </strong></span>A table in a star schema that contains facts and connected to dimensions. A fact table typically has two types of columns: those that contain facts and those that are foreign keys to dimension tables. The primary key of a fact table is usually a composite key that is made up of all of its foreign keys.</p>
<p>A fact table might contain either detail level facts or facts that have been aggregated (fact tables that contain aggregated facts are often instead called summary tables). A fact table usually contains facts with the same level of aggregation.</p>
<h4 style="text-align: center;"><span style="color: #003366;">Example of Star Schema:</span></h4>
<p><img decoding="async" class=" size-full wp-image-552 aligncenter" style="border: 1px solid #000;" src="https://learndatamodeling.com/wp-content/uploads/2015/07/star_schema.gif" alt="Star Schema Diagram" width="503" height="265" /></p>
<p>In the example sales fact table is connected to dimensions location, product, time and organization. It shows that data can be sliced across all dimensions and again it is possible for the data to be aggregated across multiple dimensions. &#8220;Sales Dollar&#8221; in sales fact table can be calculated across all dimensions independently or in a combined manner which is explained below.</p>


<ul>
<li>Sales Dollar value for a particular product.</li>
<li>Sales Dollar value for a product in a location.</li>
<li>Sales Dollar value for a product in a year within a location.</li>
<li>Sales Dollar value for a product in a year within a location sold or serviced by an employee</li>
</ul>
<p>&nbsp;</p>

<div class="wp_rp_wrap  wp_rp_vertical_s" id="wp_rp_first"><div class="wp_rp_content"><h3 class="related_post_title">Related Posts</h3><ul class="related_post wp_rp"><li data-position="0" data-poid="in-644" data-post-type="none" ><a href="https://learndatamodeling.com/blog/relational-databases/" class="wp_rp_title">Relational Databases</a></li><li data-position="1" data-poid="in-640" data-post-type="none" ><a href="https://learndatamodeling.com/blog/data-warehouse-concepts/" class="wp_rp_title">Data Warehouse Concepts</a></li><li data-position="2" data-poid="in-562" data-post-type="none" ><a href="https://learndatamodeling.com/blog/fact-table/" class="wp_rp_title">Fact Table</a></li><li data-position="3" data-poid="in-23" data-post-type="none" ><a href="https://learndatamodeling.com/blog/data-warehouse-frequently-asked-interview-questions-and-answers/" class="wp_rp_title">Data Warehouse frequently asked interview Questions and Answers</a></li>
