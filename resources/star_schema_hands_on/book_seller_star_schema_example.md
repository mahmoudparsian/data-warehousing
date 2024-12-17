Output each state and their total `sales_amount`

~~~sql
SELECT ___.___, ___(___)
FROM ___
	-- Join to get book information
    JOIN ___ ON ___.___ = ___.___
	-- Join to get store information
    JOIN ___ ON ___.___ = ___.___
-- Get all books with in the novel genre
WHERE  
    ___.___ = 'novel'
-- Group results by state
GROUP BY
    ___.___;
~~~

Querying the star schema

The novel genre hasn't been selling as well as your company predicted. To help remedy this, you've been tasked to run some analytics on the novel genre to find which areas the Sales team should target. To begin, you want to look at the total amount of sales made in each state from books in the novel genre.

Luckily, you've just finished setting up a data warehouse with the [following star schema](https://campus.datacamp.com/courses/database-design/database-schemas-and-normalization?ex=6).

The tables from this schema have been loaded. Note that you should not use aliases in FROM and JOIN statements.

Instructions

~~~sql
Select state from the appropriate table and the total sales_amount.
Complete the JOIN on book_id.
Complete the JOIN to connect the dim_store_star table
Conditionally select for books with the genre novel.
Group the results by state.
~~~

[Star schema URL](https://assets.datacamp.com/production/repositories/5311/datasets/75bc5e6de9085df105fd4cd1af69752786096617/book-star.png)

