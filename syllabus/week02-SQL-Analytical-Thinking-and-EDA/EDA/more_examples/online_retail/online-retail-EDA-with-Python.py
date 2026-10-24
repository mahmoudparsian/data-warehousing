import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Online Retail Exploratory Data Analysis with Python
    ### source: https://www.kaggle.com/code/manishvkamble/online-retail-eda-with-python/notebook
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![Online retail](public/online_retail_header.jpg)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Case Study
    In this project, I worked with transactional data from an online retail store. The dataset contained valuable information about customer purchases, including product details, quantities, prices, and timestamps. My main task was to explore and analyze this dataset to gain crucial insights into the store's sales trends, customer behavior, and popular products.

    By conducting thorough exploratory data analysis, I was able to identify meaningful patterns, outliers, and correlations in the data.

    Throughout the project, I utilized various data visualizations and statistical analysis techniques to uncover key trends, such as the busiest sales months, best-selling products, and the store's most valuable customers. These insights proved to be invaluable in driving strategic business decisions and improving the store's overall performance in the highly competitive online retail market.

    ## Prerequisites

    Before starting this project, you should have some basic knowledge of Python programming and Pandas. In addition, you may want to use the following packages in your Python environment:

    - pandas
    - numpy
    - seaborn
    - matplotlib

    These packages should already be installed in Coursera's Jupyter Notebook environment, however if you'd like to install additional packages that are not included in this environment or are working off platform you can install additional packages using `!pip install packagename` within a notebook cell such as:

    - `!pip install pandas`
    - `!pip install matplotlib`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Dataset

    During my analysis, I worked with the "Online Retail" dataset, which contains transactional data from an online retail store spanning from 2010 to 2011. The dataset was provided as a .xlsx file named Online Retail.xlsx. I had access to this data file within the Coursera Jupyter Notebook environment, making it convenient for my analysis, however if you are working off-platform it can also be downloaded [here](https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx).

    The dataset contains the following columns:

    - InvoiceNo: Invoice number of the transaction
    - StockCode: Unique code of the product
    - Description: Description of the product
    - Quantity: Quantity of the product in the transaction
    - InvoiceDate: Date and time of the transaction
    - UnitPrice: Unit price of the product
    - CustomerID: Unique identifier of the customer
    - Country: Country where the transaction occurred
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 1: Load the Data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ***Before loading the data and performing any data analysis or visualization tasks, ensure that the required Python packages are installed in project environment.***

    > Upgrade Pip: If pip version is not up-to-date, upgrade it using the following command:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ***Below are the libraries that are used in order to perform EDA (Exploratory data analysis).***
    """)
    return


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt

    return np, pd, plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ***Input data files are available in the read-only "../input/" directory.***

    > For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.1 Loading the Data into the DataFrame

    > To load data from an Excel file (.xlsx) into a pandas DataFrame, we can use the read_excel function provided by pandas.
    """)
    return


@app.cell
def _(pd):
    online_retail = pd.read_excel("./online_retail.xlsx")
    return (online_retail,)


@app.cell
def _(online_retail):
    online_retail.head(10)   # To display the first 10 rows
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.2 Types of Data

    > It's essential to check the data types of the columns when loading data from an Excel file or any other source. Sometimes, data may be stored in a different format than expected, such as numbers stored as strings or dates stored as text.

    ***To check the data types of the columns in the DataFrame, you can use the dtypes.***
    """)
    return


@app.cell
def _(online_retail):
    online_retail.dtypes
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ***Here, in this case, the data is already in integer format so nothing to worry.***
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 2: Data Cleaning

    > Data cleaning is a crucial step in every EDA process. It involves identifying and handling errors, inconsistencies, and missing values in the dataset to ensure the data is accurate, complete, and reliable.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.1 Check for Missing Values

    > To check for missing values in the DataFrame, we can use the isnull() function along with the sum() function. The isnull() function returns a DataFrame of the same shape as the input with True for missing values (NaN) and False for non-missing values. The sum() function then sums the True values (1) for each column, giving the count of missing values in each column.
    """)
    return


@app.cell
def _(online_retail):
    print(online_retail.isnull().sum())
    online_retail.shape
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.2 Replacing Null Values

    > The count of missing values for CustomerId can not be neglected as considerable data is missing, so I replaced them with the string 'Unknown', however for Description null values are negligible so I just dropped those values.
    """)
    return


@app.cell
def _(np, online_retail):
    # Replace null customerID's with unknown
    online_retail['CustomerID'].replace(np.nan,"Unknown", inplace=True)

    # Replace null description with Not Available
    online_retail.dropna(subset=['Description'], inplace=True)

    online_retail.shape
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.3 Removing Redundant or Unnecessary Columns

    > In this case, the columns such as InvoiceNo, StockCode doesn't make any sense to me so I just dropped for this instance.
    """)
    return


@app.cell
def _(online_retail):
    # Specify the column names to be removed
    columns_to_drop = ["InvoiceNo", "StockCode"]
    cleaned_online_retail = online_retail.drop(columns=columns_to_drop)
    return (cleaned_online_retail,)


@app.cell
def _(cleaned_online_retail):
    cleaned_online_retail.head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.4 Dropping the Duplicate Rows

    > Duplicate rows are rows that have the same values in all columns, and dropping them helps to ensure data integrity and avoid potential issues during analysis.
    """)
    return


@app.cell
def _(cleaned_online_retail):
    cleaned_online_retail_2 = cleaned_online_retail.drop_duplicates()
    cleaned_online_retail_2.shape
    return (cleaned_online_retail_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.5 Total Sell Amount

    > To calculate the total sell amount for each transaction, we can create a new column in the DataFrame that represents the product of 'Quantity' and 'UnitPrice'.
    """)
    return


@app.cell
def _(cleaned_online_retail_2):
    # Calculate the total sell amount for each transaction (Quantity * UnitPrice)
    cleaned_online_retail_2['Totalsell'] = cleaned_online_retail_2['Quantity'] * cleaned_online_retail_2['UnitPrice']
    cleaned_online_retail_2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 3: Statistical Summary

    > Here, the method describe() can be use to obtain a statistical summary of the dataframe.
    """)
    return


@app.cell
def _(cleaned_online_retail_2):
    cleaned_online_retail_2.describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > ***Having a negative quantity of a product in a dataset typically indicates that there was a return or a product was taken back from the customer, likewise for unitprice, a negative value would imply that refunds were made.***
    """)
    return


@app.cell
def _(cleaned_online_retail_2):
    # Calculate measures of central tendency
    median = cleaned_online_retail_2.median(numeric_only=True)   # pandas ≥ 2: skip text columns
    median
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > ***The mean for Totalsell is greater than the median, which indicates that the data may be right-skewed (positively skewed), and vice versa for left-skewed (negatively skewed) data.***
    """)
    return


@app.cell
def _(cleaned_online_retail_2):
    # Create a new column 'MonthYear' with the month and year only for Data Visualization
    cleaned_online_retail_2['MonthYear'] = cleaned_online_retail_2['InvoiceDate'].dt.to_period('M')

    # Print the DataFrame with the 'MonthYear' column
    cleaned_online_retail_2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 4: Data Visualization

    ### 4.1 Line Plot

    > Plotly express is a great library for creating a interactive line plot.
    """)
    return


@app.cell
def _(cleaned_online_retail_2, plt):
    # Group the data by 'MonthYear' and calculate the total purchase for each month
    monthly_data = cleaned_online_retail_2.groupby('MonthYear')['Totalsell'].sum().reset_index()

    # Convert the 'MonthYear' column to string format for plotly
    monthly_data['MonthYear'] = monthly_data['MonthYear'].astype(str)

    # Set the figure size using subplots
    fig, ax = plt.subplots(figsize=(6, 4)) # Width: 10 inches, Height: 5 inches

    # Automatic formatting to the x-axis labels when dealing with dates. 
    fig.autofmt_xdate()  

    # Display the plot
    plt.plot(monthly_data['MonthYear'], monthly_data['Totalsell'], marker='o', linestyle='-', color='b')

    # Customize the plot
    plt.title('Total Purchase by Month')
    plt.xlabel('MonthYear')
    plt.ylabel('TotalSell')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ***From the line plot of monthly sales it can be clearly seen that there is a significant rise in sales from august to november, then it drops in December 2011.***
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.2 Heat Maps
    > Heat Maps is a type of plot which is necessary when we need to find the dependent variables. One of the best way to find the relationship between the features can be done using heat maps.

    ***In the below heat map we know that the Totalsell feature depends mainly on the quantity of the product.***
    """)
    return


@app.cell
def _(cleaned_online_retail_2, plt, sns):
    #We can use the Pandas method corr() to find the feature that is most correlated with TotalPurchase.
    plt.figure(figsize=(10,5))
    corr = cleaned_online_retail_2.corr(numeric_only=True)
    sns.heatmap(corr,cmap="BrBG",annot=True)
    corr
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 5: Analyze the Sales Trends over Time

    > To analyze the sales trends over time and identify the busiest months and days of the week in terms of sales, we can use the pandas library in Python to perform the necessary data manipulations and calculations.
    """)
    return


@app.cell
def _(cleaned_online_retail_2):
    # Extract the month from the 'InvoiceDate'
    cleaned_online_retail_2['Month'] = cleaned_online_retail_2['InvoiceDate'].dt.month

    # Extract the day of the week from the 'InvoiceDate'
    cleaned_online_retail_2['DayOfWeek'] = cleaned_online_retail_2['InvoiceDate'].dt.day_name()

    # Calculate total sales for each month
    monthly_sales = cleaned_online_retail_2.groupby('Month')['Totalsell'].sum()

    # Calculate total sales for each day of the week
    daily_sales = cleaned_online_retail_2.groupby('DayOfWeek')['Totalsell'].sum()

    # Identify the busiest month
    busiest_month = monthly_sales.idxmax()

    # Identify the busiest day of the week
    busiest_day = daily_sales.idxmax()

    # Print the results
    print('\033[1m' + "Busiest Month (in terms of sells):" +'\033[0m', busiest_month)
    print('\033[1m' + "Busiest Day of the Week (in terms of sales):" +'\033[0m', busiest_day)
    return (daily_sales,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 5.1 Bar Plot
    > We can plot a bar graph to visualize the sales trend by the day of the week. The busiest day of the week will have the highest bar on the graph. The x-axis represents the days of the week, and the y-axis represents the total sell amount for each day.
    """)
    return


@app.cell
def _(daily_sales, plt):
    plt.figure(figsize=(6, 4))
    plt.bar(daily_sales.index, daily_sales.values)
    plt.xlabel('Day of Week')
    plt.ylabel('Total Sell Amount')
    plt.title('Sales Trend by Day of Week')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 5.2 Who were the Best Customers Throughtout the Year?

    > Knowing your top customers is essential for several reasons, as they play a crucial role in the success and growth of your business. Understanding and prioritizing top customers can lead to improved customer satisfaction, increased revenue, and better long-term business relationships.
    """)
    return


@app.cell
def _(cleaned_online_retail_2, pd):
    # Calculate the total purchase amount for each customer
    customer_total_purchase = cleaned_online_retail_2.groupby('CustomerID')['Totalsell'].sum()

    # Sort the customers based on the total purchase amount in descending order
    most_valuable_customers = customer_total_purchase.sort_values(ascending=False)

    # Convert the Series to a DataFrame
    most_valuable_customers_df = pd.DataFrame(most_valuable_customers, columns=['Totalsell']).reset_index()

    # Count the total number of customers
    total_customers = cleaned_online_retail_2['CustomerID'].nunique()

    # Print the total number of customers and the top 10 customers
    print('\033[1m' + f"Among {total_customers} customers, the top 10 customers are:" +'\033[0m', list(most_valuable_customers_df['CustomerID'][:10]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ***Here we get 'Unknown' value for top customer as we have replaced null values in the data, for now we can ignore that and focus on other customer Ids, and create Market Segmentation around them.***
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 6: Top-selling Products and Countries

    > Understanding the performance of products and sales in different regions can lead to better decision-making, improved marketing strategies, and overall business growth.
    """)
    return


@app.cell
def _(cleaned_online_retail_2, pd):
    # Find most valualble Items in the list
    items_total_sell = cleaned_online_retail_2.groupby('Description')['Totalsell'].sum()

    # Sort the items based on the total sells in ascending order
    most_valuable_items = items_total_sell.sort_values(ascending=False)

    # Convert the Series to a DataFrame
    most_valuable_items_df = pd.DataFrame(most_valuable_items, columns=['Totalsell']).reset_index()

    # Count the total number of items
    total_items = cleaned_online_retail_2['Description'].nunique()

    # Print the total number of Items and the top 10 items
    print('\033[1m' + f"Among {total_items} items, the 10 most valuable items are:" +'\033[0m', list(most_valuable_items_df['Description'][:10]))
    return


@app.cell
def _(cleaned_online_retail_2, pd):
    # Find country with most sells in the list
    countrywise_sell = cleaned_online_retail_2.groupby('Country')['Totalsell'].sum()

    # Sort countries based on the total sells in ascending order
    top_selling_country = countrywise_sell.sort_values(ascending=False)

    # Convert the Series to a DataFrame
    top_selling_country_df = pd.DataFrame(top_selling_country, columns=['Totalsell']).reset_index()

    # Count the total countries
    total_countries = cleaned_online_retail_2['Country'].nunique()

    # Print the total countries and the top 10 countries
    print('\033[1m' + f"Among {total_countries} countries, the top 10 selling countries are:" +'\033[0m', list(top_selling_country_df['Country'][:10]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ***Here, knowing the most valuable items ('DOTCOM POSTAGE', 'REGENCY CAKESTAND 3 TIER','PARTY BUNTING'....) and top selling countries ('United Kingdom', 'Netherlands', 'EIRE'...), we can make data-driven decisions, optimize operations, and stay competitive in the market. It provides critical insights into customer behavior, market trends, and business performance, allowing companies to better serve their customers and achieve long-term success.***
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 7: Identify any Outliers or Anomalies in the Dataset

    > An outlier refers to a data point or a group of points that deviate significantly from the rest of the data. These outliers can be unusually high or low values. Detecting and handling outliers is crucial as they can adversely impact the accuracy of statistical models and analyses. Therefore, it is recommended to identify and remove outliers from the dataset. One effective technique for outlier detection is the Z-Score method.

    ***Often outliers can be seen with visualizations using a box plot. Shown below is the box plot of Totalsell, you can find some points are outside the box they are none other than outliers.***
    """)
    return


@app.cell
def _(cleaned_online_retail_2, plt, sns):
    # Create a box plot
    sns.boxplot(data=cleaned_online_retail_2, y='Totalsell')

    # Display the plot
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 7.1 Z-Score

    > The Z-Score measures how many standard deviations a data point is from the mean, beyond a threshold (e.g., Z-Score > 3) as potential outliers.
    """)
    return


@app.cell
def _(cleaned_online_retail_2):
    from scipy import stats

    # Calculate the Z-Score for the 'Quantity' column
    z_scores = stats.zscore(cleaned_online_retail_2['Totalsell'])

    # Create a boolean mask to identify outliers (both positive and negative Z-scores)
    threshold = 3
    outlier_mask = abs(z_scores) > threshold

    # Extract outliers from the DataFrame
    outliers = cleaned_online_retail_2[outlier_mask]

    outliers.shape
    return (outlier_mask,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 7.2 Data without Outliers
    """)
    return


@app.cell
def _(cleaned_online_retail_2, outlier_mask):
    # Remove outliers from the main dataset
    without_outliers_online_retail = cleaned_online_retail_2[~outlier_mask]

    # Statistical Summary of data without outliers
    without_outliers_online_retail.describe()
    return (without_outliers_online_retail,)


@app.cell
def _(cleaned_online_retail_2):
    cleaned_online_retail_2.describe() # Statistical Summary of data with outliers
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### With Outliers (std = 218) and Without Outliers (std = 50)

    > The significant difference in standard deviation implies that the outliers have a substantial impact on the overall variability of the data. Removing the outliers has resulted in a more focused and less variable dataset.
    """)
    return


@app.cell
def _(plt, sns, without_outliers_online_retail):
    # Create a box plot of without_outliers_online_retail data
    sns.boxplot(data=without_outliers_online_retail, y='Totalsell')

    # Display the plot
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ***While considering the context of the data and the goals of the analysis we can not remove the outliers as it will have potential implications on the analysis.*
    *Here outliers might represents valuable or rare events that may carry essential information, which might impact the results of overall analysis.***
    """)
    return


if __name__ == "__main__":
    app.run()
