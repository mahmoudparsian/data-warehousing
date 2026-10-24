# test: skip — needs the Airbnb Melbourne CSVs (listings/calendar/reviews) from the original project, not in this repo (external reference example; see README.md)
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
    <center><br><font size=10>Data Warehouse Project</font><br>
        <br><font size=7>Part 1 - ETL</font>
        <br><b>Industrial Engineering and Management - Tel Aviv University</b>
    <br>2019</center>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Contents:
    **[ETL](#1.-ETL)**
       * [Extract](#Extract)
           - [Listings](#Listings)
           - [Calendar](#Calendar)
           - [Reviews](#Reviews)
       * [Transform](#Transform)
           - [Host dimension](#Host-dimension)
           - [Listing dimension](#Listing-dimension)
           - [Date dimension](#Time-dimension)
           - [Facts Table](#Facts-Table)
       * [Load](#Load)
    """)
    return


@app.cell
def _():
    import numpy as np
    import pandas as pd

    import seaborn as sns
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker

    import warnings
    warnings.filterwarnings('ignore')


    pd.set_option('display.max_columns', None)
    return np, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 1. ETL
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Extract
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ###  Extract csv files and display ( + shapes )
    """)
    return


@app.cell
def _(pd):
    df_listings = pd.read_csv('listings.csv', low_memory=False)
    df_calendar = pd.read_csv('calendar.csv', low_memory=False)
    df_reviews = pd.read_csv('reviews.csv', low_memory=False)
    return df_calendar, df_listings, df_reviews


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Listings
    """)
    return


@app.cell
def _(df_listings):
    df_listings.head(3)
    return


@app.cell
def _(df_listings):
    df_listings.shape
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Calendar
    """)
    return


@app.cell
def _(df_calendar):
    df_calendar.head(3)
    return


@app.cell
def _(df_calendar):
    df_calendar.shape
    return


@app.cell
def _(df_calendar):
    df_calendar.info()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Reviews
    """)
    return


@app.cell
def _(df_reviews):
    df_reviews.head(3)
    return


@app.cell
def _(df_reviews):
    df_reviews.shape
    return


@app.cell
def _(df_reviews):
    df_reviews.info()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    _____
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Transform
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Host dimension
    """)
    return


@app.cell
def _(df_listings):
    _dim_host = df_listings[['host_id', 'host_since', 'host_response_time','host_is_superhost','host_listings_count',\
                            'host_identity_verified']]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Asuming that Null is that host never answered the messages**
    """)
    return


@app.cell
def _():
    dim_host = dim_host.drop_duplicates()
    dim_host.host_response_time.fillna('never', inplace = True)
    return (dim_host,)


@app.cell
def _(dim_host):
    dim_host.host_response_time.value_counts(dropna = False)
    return


@app.cell
def _(dim_host):
    dim_host.isnull().sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **We can see that nulls belongs to the same hosts and these rows gives us nothing, so lets just drop them**
    """)
    return


@app.cell
def _(dim_host):
    dim_host[dim_host.isnull().any(axis=1)]
    return


@app.cell
def _(dim_host):
    dim_host.dropna(inplace = True)
    return


@app.cell
def _(dim_host):
    dim_host.head()
    return


@app.cell
def _(dim_host):
    dim_host.shape
    return


@app.cell
def _(dim_host):
    dim_host.info()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Listing dimension
    """)
    return


@app.cell
def _(df_listings):
    dim_listing = df_listings[['id', 'host_id', 'latitude', 'longitude', 'property_type','room_type','accommodates','bathrooms',\
                              'bedrooms','beds','price','minimum_nights','number_of_reviews','review_scores_rating',\
                               'instant_bookable']]
    return (dim_listing,)


@app.cell
def _(dim_listing):
    dim_listing.head(3)
    return


@app.function
def drop_sign(price):
    temp = price.split(",")
    str = ""
    for i in temp:
        str += i
    return float(str[1:])


@app.cell
def _(dim_listing):
    dim_listing['price'] = dim_listing['price'].apply(drop_sign)
    return


@app.cell
def _(dim_listing):
    dim_listing.head(3)
    return


@app.cell
def _(dim_listing):
    dim_listing.rename(columns = {"id":"listing_id"}, inplace=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Formula to calculate rating based on multiple reviews (using both review score and quantity):**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### $$score = 𝑃𝑝 +100(1−𝑃)(1−𝑒^{-𝑞/𝑄})$$
    where 𝑝 is the review rating, 𝑞 is the quantity of ratings, 𝑄 an appropriate number that shows what importance we attach to the notion "quantity", in the original formula we had 𝑃 = 0.7<br>
    Source : https://math.stackexchange.com/questions/942738/algorithm-to-calculate-rating-based-on-multiple-reviews-using-both-review-score
    """)
    return


@app.cell
def _(df_listings, np):
    rating_score = (0.7*df_listings['review_scores_rating']+100*0.3*(1-np.exp(-(df_listings['number_of_reviews']/10))))
    return (rating_score,)


@app.cell
def _(dim_listing, rating_score):
    dim_listing['rating_score'] = rating_score.round()
    return


@app.cell
def _(dim_listing):
    dim_listing.isnull().sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Assuming that NA in bathrooms, bedrooms, beds means that there is no separate room for bathroom, bedroom or there is no regular bed at this property ( so we will fill NA with zeros )**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Assuming that NA in review_scores_rating and rating_score means that there is no reviews or any given rating to this property ( so we will fill NA with zeros )**
    """)
    return


@app.cell
def _(dim_listing):
    dim_listing.fillna(0, inplace = True)
    return


@app.cell
def _(dim_listing):
    dim_listing.head(3)
    return


@app.cell
def _(dim_listing):
    for_fact_table = dim_listing[['listing_id','host_id']]
    return (for_fact_table,)


@app.cell
def _(dim_listing):
    dim_listing.drop('host_id',axis = 1, inplace = True)
    return


@app.cell
def _(dim_listing):
    dim_listing.tail(3)
    return


@app.cell
def _(dim_listing):
    dim_listing.shape
    return


@app.cell
def _(dim_listing):
    dim_listing.info()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Date dimension
    """)
    return


@app.cell
def _(df_calendar, pd):
    dim_date = pd.DataFrame({'date':df_calendar['date'],
                             'year': pd.DatetimeIndex(df_calendar['date']).year,
                             'quarter': pd.DatetimeIndex(df_calendar['date']).quarter,
                             'month': pd.DatetimeIndex(df_calendar['date']).month,
                             'week': pd.DatetimeIndex(df_calendar['date']).week,
                             'day': pd.DatetimeIndex(df_calendar['date']).day})
    return (dim_date,)


@app.cell
def _(dim_date):
    dim_date.drop_duplicates(inplace = True)
    return


@app.cell
def _(dim_date):
    dim_date.tail(3)
    return


@app.cell
def _(dim_date):
    dim_date.shape
    return


@app.cell
def _(dim_date):
    dim_date.reset_index(inplace = True)
    dim_date.drop('index',axis = 1, inplace = True)
    dim_date.reset_index(inplace = True)
    dim_date.rename(columns = {"index":"date_id"}, inplace=True)
    dim_date.tail()
    return


@app.cell
def _(dim_date):
    dim_date.info()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Facts Table
    """)
    return


@app.cell
def _(df_calendar, for_fact_table, pd):
    pre_fact_rental = pd.merge(df_calendar, for_fact_table, on='listing_id',how = 'left').drop('price',axis = 1)
    return (pre_fact_rental,)


@app.cell
def _(pre_fact_rental):
    pre_fact_rental.head()
    return


@app.cell
def _(dim_date, pd, pre_fact_rental):
    fact_rental = pd.merge(pre_fact_rental, dim_date[['date','date_id']], on='date',how = 'left').drop('date',axis = 1)
    return (fact_rental,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Changing 't' (true) to 1 and 'f' (flase) to 0 in 'available' column to ease the calculations**
    """)
    return


@app.cell
def _(fact_rental):
    fact_rental['available'] = [1 if i=='t' else 0 for i in fact_rental['available']]
    return


@app.cell
def _(fact_rental):
    fact_rental.head()
    return


@app.cell
def _(fact_rental):
    fact_rental.shape
    return


@app.cell
def _(fact_rental):
    fact_rental.info()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ___
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Load
    """)
    return


@app.cell
def _():
    #import MySQLdb
    import pymysql as mdb
    mdb.install_as_MySQLdb()
    #import sqlalchemy
    from sqlalchemy import create_engine
    from sqlalchemy.sql import text

    return (create_engine,)


@app.cell
def _(create_engine):
    engine = create_engine("mysql://root:root@localhost")
    con = engine.connect()

    #create database melbourne
    con.execute('DROP SCHEMA IF EXISTS melbourne').fetchall()
    con.execute('CREATE SCHEMA IF NOT EXISTS melbourne').fetchall()

    #use database melbourne
    con.execute('USE melbourne').fetchall()

    #create the table dim_host
    con.execute("""CREATE OR REPLACE TABLE melbourne.dim_host
               (host_id INT PRIMARY KEY, 
                host_since VARCHAR(45), 
                host_response_time VARCHAR(45),
                host_is_superhost VARCHAR(2),
                host_listings_count FLOAT,
                host_identity_verified VARCHAR(2))""").fetchall();

    #create the table dim_listing
    con.execute("""CREATE OR REPLACE TABLE melbourne.dim_listing
               (listing_id INT PRIMARY KEY, 
                latitude VARCHAR(20), 
                longitude VARCHAR(20),
                property_type VARCHAR(45),
                room_type VARCHAR(45),
                accommodates INT,
                bathrooms FLOAT,
                bedrooms FLOAT,
                beds FLOAT,
                price FLOAT,
                minimum_nights INT,
                number_of_reviews INT,
                review_scores_rating FLOAT,
                instant_bookable VARCHAR(2),
                rating_score FLOAT)""").fetchall();

    #create the table dim_date
    con.execute("""CREATE OR REPLACE TABLE melbourne.dim_date
               (date_id INT PRIMARY KEY, 
                date date, 
                year INT,
                quarter INT,
                month INT,
                week INT,
                day INT)""").fetchall();

    #create the table fact_rental
    con.execute("""CREATE OR REPLACE TABLE melbourne.fact_rental
               (key_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                listing_id INT NOT NULL, 
                available VARCHAR(2),
                host_id INT,
                date_id INT)""").fetchall();
    #con.execute('SET SQL_MODE=ANSI_QUOTES')
    return (con,)


@app.cell
def _(con, dim_listing):
    dim_listing.to_sql(con=con, schema='melbourne', name='dim_listing', if_exists='append',index=False)
    return


@app.cell
def _(con, dim_host):
    dim_host.to_sql(con=con, schema='melbourne', name='dim_host', if_exists='append',index=False)
    return


@app.cell
def _(con, dim_date):
    dim_date.to_sql(con=con, schema='melbourne', name='dim_date', if_exists='append',index=False)
    return


@app.cell
def _(con, fact_rental):
    fact_rental.to_sql(con=con, schema='melbourne', name='fact_rental', if_exists='append',index=False)
    return


@app.cell
def _(con):
    con.close();
    return


if __name__ == "__main__":
    app.run()
