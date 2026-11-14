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
    ```text
    '''
    This Notebook is for doing Expanatory Data Analysis on
    Car Sales Data
    '''
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Importing the Packages
    """)
    return


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patheffects as path_effects
    import matplotlib.pylab as pl
    import matplotlib.gridspec as gridspec
    import seaborn as sns
    import warnings
    # '%matplotlib inline' command supported automatically in marimo
    sns.set(style='ticks', font_scale=1.2)

    warnings.filterwarnings('ignore')
    return gridspec, np, path_effects, pd, pl, plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # UDFs
    """)
    return


@app.cell
def _(pd):
    def conti_var_summary(x):
        '''
        UDF for getting customised summary for continuous variables
        '''
        # freq and missings
        n_total = x.shape[0]
        n_miss = x.isna().sum()
        perc_miss = n_miss * 100 / n_total

        # outliers - iqr
        q1 = x.quantile(0.25)
        q3 = x.quantile(0.75)
        iqr = q3 - q1
        lc_iqr = q1 - 1.5 * iqr
        uc_iqr = q3 + 1.5 * iqr

        return pd.Series([
            x.dtype,
            x.nunique(), n_total,
            x.count(), n_miss, perc_miss,
            x.sum(),
            x.mean(),
            x.std(),
            x.var(), lc_iqr, uc_iqr,
            x.min(),
            x.quantile(0.01),
            x.quantile(0.05),
            x.quantile(0.10),
            x.quantile(0.25),
            x.quantile(0.5),
            x.quantile(0.75),
            x.quantile(0.90),
            x.quantile(0.95),
            x.quantile(0.99),
            x.max()
        ],
            index=[
            'dtype', 'cardinality', 'n_tot', 'n', 'nmiss',
            'perc_miss', 'sum', 'mean', 'std', 'var', 'lc_iqr',
            'uc_iqr', 'min', 'p1', 'p5', 'p10', 'p25', 'p50',
                             'p75', 'p90', 'p95', 'p99', 'max'
        ])

    return (conti_var_summary,)


@app.cell
def _(pd):
    def cat_var_summary(x):
        '''
        UDF for getting customised summary for categorical variables
        '''
        Mode = x.value_counts().sort_values(ascending=False)[0:1].reset_index()
        return pd.Series([
            x.count(),
            x.nunique(),
            x.isnull().sum(), Mode.iloc[0, 0], Mode.iloc[0, 1],
            round(Mode.iloc[0, 1] * 100 / x.count(), 2)
        ],
                         index=['N', 'CARDINALITY', 'NMISS', 'MODE', 'FREQ', 'PERCENT'])

    return (cat_var_summary,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Importing Data
    """)
    return


@app.cell
def _(pd):
    cars = pd.read_excel('Car_Sales.xlsx')
    return (cars,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Data Inspection
    """)
    return


@app.cell
def _(cars):
    cars.info()
    return


@app.cell
def _(cars):
    cars.head()
    return


@app.cell
def _(cars):
    cars.shape
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Dropping Duplicates
    """)
    return


@app.cell
def _(cars):
    cars.drop_duplicates(inplace=True)
    cars.shape
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Summary
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Continuous variables :
    """)
    return


@app.cell
def _(cars, conti_var_summary):
    cars.select_dtypes(['int64','float64']).apply(conti_var_summary)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Categorical variables :
    """)
    return


@app.cell
def _(cars, cat_var_summary):
    cars.select_dtypes(['object']).apply(cat_var_summary)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Anomalies
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```text
    price <= 0 - dropping these rows
    mileage == 0 - replacing with medians with groupby(['car', 'body', 'engType'])
    ```
    """)
    return


@app.cell
def _(cars, np):
    # Dropping Prices <= 0
    cars.drop(cars[cars.price <= 0].index, inplace=True)

    # Fixing Mileage column
    cars['mileage'].replace(0, np.nan, inplace = True)
    cars['mileage'] = cars.groupby(['car', 'body', 'engType'])['mileage'].transform(lambda x: x.fillna(x.median()))

    cars.shape
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ***Skipping the outlier treatment for now. It will be done in EDA section if required for the Analysis.***
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Missing Values
    """)
    return


@app.cell
def _(cars, pd):
    pd.DataFrame([cars.isnull().sum(), cars.isnull().sum() / cars.shape[0] * 100], index=['count', '%']).T
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    >Treating the NaNs as : <br>
    >* Filling values
        1. `drive` - mode() <br>
        2. `endV` - median() based on `car`, `body`, `engType` and `drive` <br>
    >* Dropping Rows
        - `mileage`, `engV` - Whatever left as NaNs
    """)
    return


@app.cell
def _(cars):
    # Filling values
    cars.drive.fillna(value=cars.drive.mode()[0], inplace=True)
    cars['engV'] = cars.groupby(['car', 'body', 'engType', 'drive']).engV.transform(lambda x: x.fillna(x.median()))
    return


@app.cell
def _(cars):
    # Dropping Rows
    cars.dropna(inplace=True)
    cars.shape
    return


@app.cell
def _(cars, pd):
    pd.DataFrame([cars.isnull().sum(), cars.isnull().sum() / cars.shape[0] * 100], index=['count', '%']).T
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Correlation
    """)
    return


@app.cell
def _(cars, plt, sns):
    plt.figure(figsize=(7,7))
    sns.set(font_scale=1.2)
    sns.heatmap(cars.corr(numeric_only=True), square=True, annot=True)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # EDA
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Which type of cars are sold maximum?
    """)
    return


@app.cell
def _(cars, plt, sns):
    plt.figure(figsize=(10,5))
    sns.set(style='ticks', font_scale=1.2)
    sns.countplot(data=cars, x='body', hue='engType').set_title('Count of different cars sold')
    sns.despine()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > Clearly **seadan - Petrol** cars are sold maximum.
    """)
    return


@app.cell
def _(cars, plt, sns):
    sns.set(style='ticks', font_scale=1.2)
    g = sns.FacetGrid(cars, row="drive", col="engType", margin_titles=True, despine=False)
    g.map_dataframe(sns.histplot, x="body")
    g.figure.subplots_adjust(wspace=0.075, hspace=0.075)
    g.add_legend()
    for axes in g.axes.flat:
        _ = axes.set_xticklabels(axes.get_xticklabels(), rotation=45)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > From the above Facet Grid, we can conclude that cars with **body : Sedan, Engine Type : Petrol, Drive : Front** are sold maximum.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. What is the co-relation between price and mileage?
    """)
    return


@app.cell
def _(cars, plt, sns):
    sns.set(style='ticks', font_scale=1.2)
    sns.pairplot(cars.loc[:,['price','mileage','engType']], diag_kind='hist', hue='engType', height=6, aspect=1)
    plt.show()
    return


@app.cell
def _(cars):
    cars.loc[:,['price','mileage']].corr(numeric_only=True).iloc[1,0].round(2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > Price and Mileage are negatively co-related with corelation coefficient = -0.28 <br>
    > From the pairplot above we can conclude that :
    > - Most of the cars gives mileage in [1, 300] with price < 150000
    > - There exists a few excpetions / outliers in case of Petrol cars.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. How many cars are registered?
    """)
    return


@app.cell
def _(cars, plt, sns):
    plt.figure(figsize=(10,5))
    sns.set(style='ticks', font_scale=1.2)
    _plots = sns.countplot(cars['registration'], order = cars['registration'].value_counts().index)
    _plots.set_title('Registered vs Not-registered cars')
    for _bar in _plots.patches:
        _plots.annotate(str(format(_bar.get_height(), '.0f')),
                       (_bar.get_x() + _bar.get_width() / 2, _bar.get_height()),
                       ha='center', va='center', size=15, xytext=(0, 8), textcoords='offset points')
    sns.despine()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > Total **8611** Cars are registered and **552** are not registered.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Price distribution between registered and non-registered cars.
    """)
    return


@app.cell
def _(cars, path_effects, plt, sns):
    # Creating a UDF to add median labels
    def add_median_labels(ax, fmt='.1f'):
        '''
        This function adds median labels at any orientation
        '''
        lines = ax.get_lines()
        boxes = [c for c in ax.get_children() if type(c).__name__ == 'PathPatch']
        lines_per_box = int(len(lines) / len(boxes))
        for median in lines[4:len(lines):lines_per_box]:
            x, y = (data.mean() for data in median.get_data())
            # choosing value depending on horizontal or vertical plot orientation
            value = x if (median.get_xdata()[1] - median.get_xdata()[0]) == 0 else y
            text = ax.text(x, y, f'{value:{fmt}}', ha='center', va='center',
                           fontweight='bold', color='white')
            # creating median-colored border around white text for contrast
            text.set_path_effects([
                path_effects.Stroke(linewidth=3, foreground=median.get_color()),
                path_effects.Normal(),
            ])

    plt.figure(figsize=(16,5))
    sns.set(style='ticks', font_scale=1.2)
    _ax = sns.boxplot(x='price', y='registration', saturation=1, data=cars, showfliers=False)
    _ax.set_title('Registration vs Price [without Outliers]')
    add_median_labels(_ax)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > Clearly we can say that all the cars which are registered have IQR of price between 6000 to 18000 with median at **9900**. And, cars which are not registered have price IQR between 2500 to 4500 with median at **3000**. So, not-registered cars have significantly lower prices compared to the registered cars.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. What is the car price distribution based on Engine Value?
    """)
    return


@app.cell
def _(cars, plt, sns):
    plt.figure(figsize=(8,8))
    sns.set(style='ticks', font_scale=1.2)
    sns.regplot(x='engV', y='price', data=cars, x_jitter=0, y_jitter=0).set_title('Price vs Engine Value')
    plt.show()
    return


@app.cell
def _(cars):
    cars.loc[:,['price','engV']].corr(numeric_only=True).iloc[1,0].round(2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > Clearly This data contains outliers. So, we can better conclude the results after outlier treatement. As of now, the corr value between these two variables is 0.05.
    """)
    return


@app.cell
def _(cars):
    cars1 = cars.loc[:,['price','engV']].apply(lambda x: x.clip(lower = x.quantile(0.01), upper = x.quantile(0.99)))
    return (cars1,)


@app.cell
def _(cars1, plt, sns):
    plt.figure(figsize=(8,8))
    sns.set(style='ticks', font_scale=1.2)
    sns.regplot(x='engV', y='price', data=cars1, x_jitter=0, y_jitter=0).set_title('Price vs Engine Value [without Outliers]')
    plt.show()
    print('Updated Corr Value between Price and Engine Value :', cars1.loc[:,['price','engV']].corr(numeric_only=True).iloc[1,0].round(2))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > As per the observation, price range for most of the cars is in [0, 100000] with Engine Value in [1, 6] with a sighlty positiive trend in the data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Which Engine Type of cars users preferred maximum?
    """)
    return


@app.cell
def _(cars, plt, sns):
    plt.figure(figsize=(8,6))
    sns.set(style='ticks', font_scale=1.2)
    _plots = sns.countplot(cars['engType'], order = cars['engType'].value_counts().index)
    _plots.set_title('Count of cars with different Engine Type sold')
    for _bar in _plots.patches:
        _plots.annotate(str(format(_bar.get_height(), '.0f')),
                       (_bar.get_x() + _bar.get_width() / 2, _bar.get_height()),
                       ha='center', va='center', size=15, xytext=(0, 8), textcoords='offset points')
    sns.despine()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > Clearly, the user preference order is : **Petrol > Diesel > Gas > Other**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Establish corelation between all features using heatmap.
    """)
    return


@app.cell
def _(cars, plt, sns):
    plt.figure(figsize=(8,8))
    sns.set(font_scale=1.2)
    sns.heatmap(cars.corr(numeric_only=True), square=True, annot=True)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > * **Price** is positively co-related with **Engine Value** & **Year** and negatively co-related with **Mileage**.<br>
    > * **Mileage** is positively co-related with **Engine Value** and negatively co-related with **Year**.<br>
    > * **Engine Value**  is negatively co-related with **Year**.<br>
    > * *None of the co-relations is strong. Here, Mileage and Year having the maximum co-relation with coefficient = -0.46.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Distribution of Price
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Original Raw Data
    """)
    return


@app.cell
def _(cars, gridspec, np, pl, plt, sns):
    _params = {'figure.figsize': (15.5, 8), 'axes.labelsize': 14}
    plt.rcParams.update(_params)
    sns.set(style='ticks', font_scale=1.2)
    _gs = gridspec.GridSpec(2, 2, wspace=0.08)
    _f = pl.figure()

    # Boxplot
    _ax = pl.subplot(_gs[0, 0]) # row 0, col 0
    sns.boxplot(x='price', saturation=1, data=cars, showfliers=True, ax=_ax, fliersize=2) \
        .set_title('Distribution of Car Prices [Raw Data]')

    _ax = pl.subplot(_gs[0, 1]) # row 0, col 1
    _ax.axis('off')

    # Distplot
    _ax = pl.subplot(_gs[1, 0]) # row 1, col 0
    _ax = sns.distplot(cars['price'],color ='m')
    plt.ylabel('density')

    # Logarithmic Distribution 
    _ax = pl.subplot(_gs[1, 1]) # row 1, col 1
    _ax = sns.distplot(np.log(cars['price']),color ='r') \
        .set_title('Distribution of Car Prices [Log-Transformed Data]')

    plt.show()
    return


@app.cell
def _(cars):
    cars.price.skew()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 1. We can see that this data contains lots of outliers. <br>
    > 2. The price data is **Right-skewed with skewness value = 6.127** <br>
    > 3. Logarithmic distribution follows close to Normal distribution.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### After Outlier Treatment
    """)
    return


@app.cell
def _(cars1, gridspec, np, pl, plt, sns):
    _params = {'figure.figsize': (15.5, 8), 'axes.labelsize': 14}
    plt.rcParams.update(_params)
    sns.set(style='ticks', font_scale=1.2)
    _gs = gridspec.GridSpec(2, 2, wspace=0.08)
    _f = pl.figure()

    # Boxplot without Outliers (p99)
    _ax = pl.subplot(_gs[0, 0]) # row 0, col 0
    sns.boxplot(x='price', saturation=1, data=cars1, showfliers=True, ax=_ax, fliersize=2) \
        .set_title('Distribution of Car Prices [Outliers clipped at p99]')

    _ax = pl.subplot(_gs[0, 1]) # row 0, col 1
    _ax.axis('off')

    # Distplot without Outliers (p99)
    _ax = pl.subplot(_gs[1, 0]) # row 1, col 0
    _ax = sns.distplot(cars1['price'],color ='m')
    plt.ylabel('density')

    # Logarithmic Distribution without Outliers
    _ax = pl.subplot(_gs[1, 1]) # row 1, col 1
    _ax = sns.distplot(np.log(cars1['price']),color ='r') \
        .set_title('Distribution of Car Prices [Log-Transformed Data]')

    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > After clipping the outliers at p99 value, we can see that - <br>
    > 4. The Price Distribution has its IQR around [5000, 15000] range with median around 10000.<br>
    > 5. The Price varies from 0 to 40000 for maximum no. of instances.
    """)
    return


if __name__ == "__main__":
    app.run()
