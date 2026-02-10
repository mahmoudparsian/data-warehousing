# Slowly Changing Dimensions (SCDs)

	Slowly Changing Dimensions (SCDs) are data 
	warehousing techniques to manage attributes 
	in dimension tables (like customer addresses 
	or product descriptions) that change over time,
	preserving historical accuracy or just keeping 
	current data, using methods like
	
	     overwriting (Type 1) or 
	     creating new rows (Type 2) 
	
	for different business needs, crucial for 
	reliable trend analysis and reporting.

# Key Concepts

**Dimension Table**: Stores descriptive attributes about business entities (customers, products, locations).

**SCD**: A strategy for handling changes in these dimension attributes over time, ensuring data integrity for analysis.

**Natural Key**: The unique identifier from the source system (e.g., `customer_id`).

# Common SCD Types

**Type 1 (Overwrite):**

	Overwrites old data with new data; 
	no history kept. Good for correcting 
	errors or when history isn't needed 
	(e.g., fixing a typo in a product name).

**Type 2 (New Row)**: 

	Creates a new record with a unique surrogate 
	key for each change, preserving a complete 
	history. Uses effective dates/flags to identify
	current vs. old records.

**Type 3 (New Column)**: 

	Adds a new column to store the previous value, 
	keeping only the current and one prior state.

**Type 4 (History Table)**: 

	Moves historical changes to a separate history table.

# References

[1. Slowly Changing Dimensions](https://www.geeksforgeeks.org/software-testing/slowly-changing-dimensions/)

[2. VIDEO: SCD Slowly Changing Dimension An Ultimate Guide](https://www.youtube.com/watch?v=7tGPVoq7DK4)
