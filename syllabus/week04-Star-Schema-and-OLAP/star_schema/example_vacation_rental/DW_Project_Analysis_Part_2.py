# test: skip — needs a MySQL server with the 'melbourne' star schema (external reference example; see README.md)
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
        <br><font size=7>Part 2 - Analysis</font>
        <br><b>Industrial Engineering and Management - Tel Aviv University</b>
    <br>2019</center>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Contents:
    **[Analysis](#2.-Analysis)**
       * [SQL](#SQL)
       * [Visualization](#Visualization)
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
    return np, pd, plt, sns


@app.cell
def _():
    #import MySQLdb
    import pymysql as mdb
    mdb.install_as_MySQLdb()
    #import sqlalchemy
    from sqlalchemy import create_engine
    from sqlalchemy.sql import text

    return create_engine, text


@app.cell
def _(create_engine):
    engine = create_engine("mysql://root:root@localhost")
    con = engine.connect()
    return (con,)


@app.cell
def _(con):
    #use database melbourne
    con.execute('USE melbourne').fetchall();
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2. Analysis
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## SQL
    """)
    return


@app.cell
def _(con, pd, text):
    _t = text('''SELECT month, year, count(*) as monthly_day_count
                           FROM dim_date
                           GROUP BY dim_date.month, dim_date.year;''')

    _result = con.execute(_t)
    _monthly_day_count = pd.DataFrame(_result.fetchall())

    _monthly_day_count.rename(columns = { 0:"month", 1:"year", 2:"count"}, inplace=True)
    return


@app.cell
def _(np):
    monthly_day_count = monthly_day_count.sort_values(by = 'month')
    monthly_day_count = monthly_day_count.apply(np.roll, shift=1)
    monthly_day_count
    return (monthly_day_count,)


@app.cell
def _(con, monthly_day_count, pd, text):
    availability_vs_rating_by_month_dict = {}
    availability_vs_response_and_instant_by_month_dict = {}

    for i in range(len(monthly_day_count)):
        month = monthly_day_count.iloc[i][0]
        year = monthly_day_count.iloc[i][1]
        _t = text('''SELECT  dim_listing.rating_score, avg(available)  as avg_available
           FROM fact_rental, dim_date, dim_listing
           WHERE fact_rental.date_id = dim_date.date_id AND fact_rental.listing_id = dim_listing.listing_id 
                 AND  dim_date.month = {} and dim_date.year = {}
           GROUP BY  dim_listing.rating_score;'''.format(month, year))
        _result = con.execute(_t)
        date_data = pd.DataFrame(_result.fetchall())
        date_data.rename(columns = {0:"rating_score",1:"avg_availability"}, inplace=True)
        availability_vs_rating_by_month_dict[(month,year)] = date_data
        ######## Getting second query
        _t2 = text('''SELECT  dh.host_response_time, dl.instant_bookable ,avg(available) as Available_Precentage
                     FROM  melbourne.fact_rental AS fr
                     INNER JOIN melbourne.dim_listing dl ON dl.listing_id = fr.listing_id
                     INNER JOIN melbourne.dim_host dh ON dh.host_id = fr.host_id
                     INNER JOIN melbourne.dim_date dd ON dd.date_id = fr.date_id
                     WHERE dd.month = {} and dd.year = {}
                     GROUP BY  host_response_time, instant_bookable
                     ORDER BY host_response_time, instant_bookable;'''.format(month, year))
        _result2 = con.execute(_t2)
        date_data_2 = pd.DataFrame(_result2.fetchall())
        date_data_2.rename(columns = {0:"host_response_time",1:"instant_bookable",2:"avg_availability"}, inplace=True)
        availability_vs_response_and_instant_by_month_dict[(month,year)] = date_data_2
    return (
        availability_vs_rating_by_month_dict,
        availability_vs_response_and_instant_by_month_dict,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ____
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Checking data ( on randomly chosen month )
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Availability vs response and instant by month**
    """)
    return


@app.cell
def _(availability_vs_response_and_instant_by_month_dict):
    df_12_18 = availability_vs_response_and_instant_by_month_dict[(12,2018)]
    df_12_18
    return (df_12_18,)


@app.cell
def _(df_12_18):
    dff = df_12_18.groupby(['instant_bookable','host_response_time']).avg_availability.mean().unstack(0)
    dff
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
    **Availability vs rating by month**
    """)
    return


@app.cell
def _(availability_vs_rating_by_month_dict):
    availability_vs_rating_by_month_dict[(12,2018)].head(10)
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
    # Visualization
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ( + unstack data inplace )
    """)
    return


@app.cell
def _(
    availability_vs_rating_by_month_dict,
    availability_vs_response_and_instant_by_month_dict,
    plt,
    sns,
):
    def plot_graph(date):
        fig, ax =plt.subplots(1,2,figsize=(25,8))
        g = sns.barplot(x = availability_vs_rating_by_month_dict[date]['rating_score'],
                y = availability_vs_rating_by_month_dict[date]['avg_availability'], ax = ax[0])
        for ind, label in enumerate(g.get_xticklabels()):
            if ind % 10 == 0:  # every 10th label is kept
                label.set_visible(True)
            else:
                label.set_visible(False)
        g.xaxis.labelpad = 25
        g.yaxis.labelpad = 15
        g.set_xlabel('Rating Score',fontsize=18)
        g.set_ylabel('Average Availability',fontsize=15)
        availability_vs_response_and_instant_by_month_dict[date].groupby(['instant_bookable',\
                                'host_response_time']).avg_availability.mean().unstack(0).plot.bar(ax = ax[1])
        plt.xlabel('Response Time', labelpad=25, fontsize=18)
        plt.ylabel('Average Availability',labelpad=15, fontsize=15)
        plt.xticks(rotation='horizontal')
        plt.legend(title='Instant Bookable', labels = ["False", "True"])
        fig.legend(["{}, {}".format(date[0],date[1])], loc='upper center', fontsize = 'xx-large',handlelength=0)
        fig.show()

    return (plot_graph,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### December 2018
    """)
    return


@app.cell
def _(plot_graph):
    plot_graph((12,2018))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### January 2019
    """)
    return


@app.cell
def _(plot_graph):
    plot_graph((1,2019))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### February 2019
    """)
    return


@app.cell
def _(plot_graph):
    plot_graph((2,2019))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### March 2019
    """)
    return


@app.cell
def _(plot_graph):
    plot_graph((3,2019))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### April 2019
    """)
    return


@app.cell
def _(plot_graph):
    plot_graph((4,2019))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### May 2019
    """)
    return


@app.cell
def _(plot_graph):
    plot_graph((5,2019))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### June 2019
    """)
    return


@app.cell
def _(plot_graph):
    plot_graph((6,2019))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### July 2019
    """)
    return


@app.cell
def _(plot_graph):
    plot_graph((7,2019))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### August 2019
    """)
    return


@app.cell
def _(plot_graph):
    plot_graph((8,2019))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### September 2019
    """)
    return


@app.cell
def _(plot_graph):
    plot_graph((9,2019))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### October 2019
    """)
    return


@app.cell
def _(plot_graph):
    plot_graph((10,2019))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### November 2019
    """)
    return


@app.cell
def _(plot_graph):
    plot_graph((11,2019))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### December 2019
    """)
    return


@app.cell
def _(plot_graph):
    plot_graph((12,2019))
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
    # Bonus
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Yearly analysis
    """)
    return


@app.cell
def _(con, pd, text):
    _t = text('''SELECT  dim_listing.rating_score, avg(available)  as avg_available
                FROM fact_rental, dim_date, dim_listing
                WHERE fact_rental.date_id = dim_date.date_id AND fact_rental.listing_id = dim_listing.listing_id 
                        AND  dim_date.year = {}
                GROUP BY  dim_listing.rating_score;'''.format(2019))
    _result = con.execute(_t)
    date_data_year = pd.DataFrame(_result.fetchall())
    date_data_year.rename(columns = {0:"rating_score",1:"avg_availability"}, inplace=True)
    return (date_data_year,)


@app.cell
def _(date_data_year):
    date_data_year.head(10)
    return


@app.cell
def _(con, pd, text):
    _t2 = text('''SELECT  dh.host_response_time, dl.instant_bookable ,avg(available) as Available_Precentage
                FROM  melbourne.fact_rental AS fr
                INNER JOIN melbourne.dim_listing dl ON dl.listing_id = fr.listing_id
                 INNER JOIN melbourne.dim_host dh ON dh.host_id = fr.host_id
                 INNER JOIN melbourne.dim_date dd ON dd.date_id = fr.date_id
                 WHERE dd.year = {}
                GROUP BY  host_response_time, instant_bookable
                ORDER BY host_response_time, instant_bookable;'''.format(2019))
    _result2 = con.execute(_t2)
    date_data_2_year = pd.DataFrame(_result2.fetchall())
    date_data_2_year.rename(columns = {0:"host_response_time",1:"instant_bookable",2:"avg_availability"}, inplace=True)
    return (date_data_2_year,)


@app.cell
def _(date_data_2_year):
    date_data_2_year
    return


@app.cell
def _(date_data_2_year):
    date_data_2_year_2 = date_data_2_year.groupby(['instant_bookable',\
                                                 'host_response_time']).avg_availability.mean().unstack(0)
    date_data_2_year_2
    return (date_data_2_year_2,)


@app.cell
def _(date_data_2_year_2, date_data_year, plt, sns):
    fig, ax =plt.subplots(1,2,figsize=(25,8))
    g = sns.barplot(x = date_data_year['rating_score'],
            y = date_data_year['avg_availability'], ax = ax[0])
    for ind, label in enumerate(g.get_xticklabels()):
        if ind % 10 == 0:  # every 10th label is kept
            label.set_visible(True)
        else:
            label.set_visible(False)
    g.xaxis.labelpad = 25
    g.yaxis.labelpad = 15
    g.set_xlabel('Rating Score',fontsize=18)
    g.set_ylabel('Average Availability',fontsize=15)
    date_data_2_year_2.plot.bar(ax = ax[1])
    plt.xlabel('Response Time', labelpad=25, fontsize=18)
    plt.ylabel('Average Availability',labelpad=15, fontsize=15)
    plt.xticks(rotation='horizontal')
    plt.legend(title='Instant Bookable', labels = ["False", "True"])
    fig.legend(["2019"], loc='upper center', fontsize = 'xx-large',handlelength=0)
    fig.show()
    return


@app.cell
def _(con):
    con.close();
    return


if __name__ == "__main__":
    app.run()
