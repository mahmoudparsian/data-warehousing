#------------------------------
# SOURCE:
#        Peek into US used car sales
#        https://www.kaggle.com/code/tsaustin/peek-into-us-used-car-sales/notebook
#------------------------------

import pandas as pd
import os
import sys
# Visualizing transaction distribution
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Distribution graphs (histogram/bar graph) of column data
def plotPerColumnDistribution(df, nGraphShown, nGraphPerRow):
    nunique = df.nunique()
    df = df[[col for col in df if nunique[col] > 1 and nunique[col] < 50]] # For displaying purposes, pick columns that have between 1 and 50 unique values
    nRow, nCol = df.shape
    columnNames = list(df)
    # nGraphRow = (nCol + nGraphPerRow - 1) / nGraphPerRow
    nGraphRow = int((nCol + nGraphPerRow - 1) / nGraphPerRow)
    print("nGraphRow=", nGraphRow)
    #exit()
    plt.figure(num = None, figsize = (6 * nGraphPerRow, 8 * nGraphRow), dpi = 80, facecolor = 'w', edgecolor = 'k')
    for i in range(min(nCol, nGraphShown)):
        plt.subplot(nGraphRow, nGraphPerRow, i + 1)
        columnDf = df.iloc[:, i]
        if (not np.issubdtype(type(columnDf.iloc[0]), np.number)):
            valueCounts = columnDf.value_counts()
            valueCounts.plot.bar()
        else:
            columnDf.hist()
        plt.ylabel('counts')
        plt.xticks(rotation = 90)
        plt.title(f'{columnNames[i]} (column {i})')
    plt.tight_layout(pad = 1.0, w_pad = 1.0, h_pad = 1.0)
    plt.show()
    
# Correlation matrix
def plotCorrelationMatrix(df, graphWidth):
    #filename = df.dataframeName
    # df = df.dropna('columns') # drop columns with NaN
    df = df.dropna() # drop columns with NaN
    df = df[[col for col in df if df[col].nunique() > 1]] # keep columns where there are more than 1 unique values
    if df.shape[1] < 2:
        print(f'No correlation plots shown: The number of non-NaN or constant columns ({df.shape[1]}) is less than 2')
        return
    corr = df.corr()
    plt.figure(num=None, figsize=(graphWidth, graphWidth), dpi=80, facecolor='w', edgecolor='k')
    corrMat = plt.matshow(corr, fignum = 1)
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.gca().xaxis.tick_bottom()
    plt.colorbar(corrMat)
    plt.title(f'Correlation Matrix', fontsize=15)
    plt.show()
    
# Scatter and density plots
def plotScatterMatrix(df, plotSize, textSize):
    df = df.select_dtypes(include =[np.number]) # keep only numerical columns
    # Remove rows and columns that would lead to df being singular
    # df = df.dropna('columns')
    df = df.dropna()
    df = df[[col for col in df if df[col].nunique() > 1]] # keep columns where there are more than 1 unique values
    columnNames = list(df)
    if len(columnNames) > 10: # reduce the number of columns for matrix inversion of kernel density plots
        columnNames = columnNames[:10]
    df = df[columnNames]
    ax = pd.plotting.scatter_matrix(df, alpha=0.75, figsize=[plotSize, plotSize], diagonal='kde')
    corrs = df.corr().values
    for i, j in zip(*plt.np.triu_indices_from(ax, k = 1)):
        ax[i, j].annotate('Corr. coef = %.3f' % corrs[i, j], (0.8, 0.2), xycoords='axes fraction', ha='center', va='center', size=textSize)
    plt.suptitle('Scatter and Density Plot')
    plt.show()
            

used_car_sales_filename = sys.argv[1]
print("used_car_sales_filename=", used_car_sales_filename)

zip_codes_filename = sys.argv[2]
print("zip_codes_filename=", zip_codes_filename)

df = pd.read_csv(used_car_sales_filename, dtype={'zipcode': str})
zip_codes = pd.read_csv(zip_codes_filename, dtype=str)
print("df=", df)
print("df.head()=", df.head())
print("zip_codes=", zip_codes)
print("zip_codes.head()=", zip_codes.head())

nRow, nCol = df.shape
print(f'There are {nRow} rows and {nCol} columns in df')
nRow, nCol = zip_codes.shape
print(f'There are {nRow} rows and {nCol} columns in zip_codes')

# CLEAN ZIP CODES
df = df[df['zipcode'].str.isdigit() == True]
# df['zipcode'] = df['zipcode'].astype(int)
print("df.shape=", df.shape)

# Distribution graphs (histogram/bar graph) of sampled columns: WORKED
plotPerColumnDistribution(df, 10, 5)

# Correlation matrix: DID NOT WORK
# plotCorrelationMatrix(df, 8)

# Scatter and density plots: WORKED
plotScatterMatrix(df, 18, 10)

# CLEAN ZIP CODES:
# For our purpose we only need zip code and state. 
# If we would only copy these columns we would end 
# with duplicates which would duplicate sales data 
# later when we join the two dataframes. To be safe 
# let's create a unique zip,state dataframe.
#
zip_codes_clean = zip_codes.groupby(by=['ZIP','STATE'], as_index=False).first()[['ZIP','STATE']]
print("zip_codes_clean=", zip_codes_clean)
print("zip_codes_clean.head()=", zip_codes_clean.head())


# Adding some features: Age of the car
# Adding some features that don't come with the 
# dataset but are helpful for visualization and 
# building models on top of the dataset.
df['Age'] = df['yearsold'] - df['Year']
print("df.head()=", df.head())

# US States from ZIP Code
# for this to work we need to clean up the zip codes 
# in the sales dataframe first by removing non numeric 
# zip codes and convert the column type to integer. 
# DID NOT DO IT: 
#   I'm converting the zip codes to integer because the 
#   zip data frames stores them as such (i hope there are no 
#    issues with the leading zeroes in the US zip codes)

df = df[df['zipcode'].str.isdigit() == True]
# df['zipcode'] = df['zipcode'].astype(int)
print("df.shape=", df.shape)

# Check for duplicates of ZIP CODES
df = pd.merge(df, zip_codes_clean, left_on='zipcode', right_on='ZIP', how='left')
df.drop('ZIP',axis=1,inplace=True)
print("df.shape=", df.shape)

# Initial Analysis & Cleanup
# Let's start with a pairplot to get an overview of the data.

# Select specific columns for the pairplot
subset = df[['pricesold', 'yearsold', 'zipcode']]
# Create the pairplot
#sns.set(style="whitegrid")
sns.pairplot(subset)
#sns.pairplot(df)
plt.show()


# Selling price by Age
# Let's take a look how the age/price scatter plot looks like
# Scatter plot of 'Age' vs 'pricesold'
sns.scatterplot(x='Age', y='pricesold', data=df)
plt.title('Age vs Price Sold')
plt.xlabel('Age')
plt.ylabel('pricesold')
plt.show()

# There's some outliers, most likely due to a 
# wrong Model year in the data set. Let's clean this up
print("df[df['Age']>100]=", df[df['Age']>100])
# [87 rows x 15 columns]

# Drop rows where Age > 100
df = df[df['Age'] <= 100]
# Optionally reset index
df.reset_index(drop=True, inplace=True)

# Fix the samples that used YY instead of YYYY. 
# The list above showed only 19xx cars. So you'll 
# need to change the code below if you'll see cars 
# that clearly where built in the 2000s.
df = df[df['Year']>0]
df.loc[df['Year']<100,['Year']] += 1900
# And recalculate the Age column again
df['Age'] = df['yearsold'] - df['Year']

print("df=", df)
print("df.shape=", df.shape)
print("df.head()=", df.head())

# Let's do the scatterplot again
sns.scatterplot(x='Age', y='pricesold', data=df)
plt.title('Age vs Price Sold')
plt.xlabel('Age')
plt.ylabel('pricesold')
plt.show()


# cars with a negative age? there's some
# next year models and typos. For now I just delete them
df = df[df['Age']>=0]
sns.scatterplot(x='Age', y='pricesold', data=df)
plt.title('Age vs Price Sold')
plt.xlabel('Age')
plt.ylabel('pricesold')
plt.show()

# Selling price by miles
sns.scatterplot(x='Mileage', y='pricesold', data=df)
plt.title('Mileage vs Price Sold')
plt.xlabel('Mileage')
plt.ylabel('pricesold')
plt.show()

# CLEAN Data by  Mileage
df = df[(df['Mileage']<300000) & (df['Mileage']>0)]
sns.scatterplot(x='Mileage', y='pricesold', data=df)
plt.title('Mileage vs Price Sold')
plt.xlabel('Mileage')
plt.ylabel('pricesold')
plt.show()

# LOOK AT NumCylinders
sns.distplot(df['NumCylinders'],kde=False,bins=20)
plt.show()
# ==> ok - yeah there's something off. In commercial vehicles 
# 16 cylinders are max. Let's print the outliers here.
print("df[df['NumCylinders'] > 16]=", df[df['NumCylinders'] > 16])
"""
df[df['NumCylinders'] > 16]=           ID  pricesold  yearsold zipcode  Mileage       Make  ... Engine  BodyType NumCylinders DriveType Age  STATE
34064  51234       6500      2019   24112    60703  Chevrolet  ...     V8     Coupe          350       RWD  43     VA
36894  26567       2520      2019   60110    66000      Dodge  ...   none       van          440       RWD  45     IL
39104  28786       1200      2019   56554    90343  Chevrolet  ...    NaN       NaN          123       RWD  65     MN

[3 rows x 15 columns]
"""
#Just a few above 16. I'll just delete them.

df = df[df['NumCylinders'] <= 16]
#And do the histogram again.
sns.distplot(df['NumCylinders'],kde=False,bins=16)
plt.show()


# Splitting dataset into Oldtimers and Newtimers
# I think it makes sense to split the dataset into two. 
#   * Historical cars (age >25 years) and 
#   * Normal cars that are younger than 25 years
#
# Let's take a look at the age/selling price distribution side by side

oldtimers = df[df['Age'] > 25]
newtimers = df[df['Age'] <= 25]
#
plt.subplot(1, 2, 1)
plt.scatter(newtimers['Age'],newtimers['pricesold'])
plt.ylabel('Selling Price')
plt.xlabel('Age')
plt.title('Newtimers Selling Prices')
plt.subplot(1, 2, 2)
plt.scatter(oldtimers['Age'],oldtimers['pricesold'])
plt.ylabel('Selling Price')
plt.xlabel('Age')
plt.title('Oldtimers Selling Prices')
plt.tight_layout()
plt.show()

#---------------------------
# More Visualizations
# Sales by Car Makes
# What's the Car Make breakdown in both groups?
#----------------------------
plt.rcParams["figure.figsize"] = [10,5]
plt.subplot(1, 2, 1)
makes = newtimers['Make'].value_counts(ascending=True).tail(10).index
y_pos = np.arange(len(makes))
salescount = newtimers['Make'].value_counts(ascending=True).tail(10).values 
plt.barh(y_pos, salescount, align='center', alpha=0.5)
plt.yticks(y_pos, makes)
plt.ylabel('Makes')
plt.title('Newtimers Top 10 Sales count')
plt.subplot(1, 2, 2)
makes = oldtimers['Make'].value_counts(ascending=True).tail(10).index
y_pos = np.arange(len(makes))
salescount = oldtimers['Make'].value_counts(ascending=True).tail(10).values 
plt.barh(y_pos, salescount, align='center', alpha=0.5)
plt.yticks(y_pos, makes)
plt.ylabel('Makes')
plt.title('Oldtimers Top 10 Sales count')
plt.tight_layout()
plt.show()

#----------------------------------------
# Analysis on a specific model
# Let's focus on newtimers and one of 
# the top selling models, the 2007 Ford Mustang.
#----------------------------------------
newtimers.groupby(by=['Make','Model','Year']).size().sort_values(ascending=False).head()
mileage = newtimers[(newtimers['Make'] == 'Ford') 
          & (newtimers['Model'] == 'Mustang') 
          & (newtimers['Year'] == 2007)]['Mileage']
salesprices = newtimers[(newtimers['Make'] == 'Ford') 
          & (newtimers['Model'] == 'Mustang') 
          & (newtimers['Year'] == 2007)]['pricesold']
plt.scatter(mileage,salesprices)
plt.ylabel('Selling Price')
plt.xlabel('Mileage')
plt.show()

#--------------------
# Sales by Region
#
# pip install --upgrade nbformat
#--------------------
states = df['STATE'].value_counts().index
salescount = df['STATE'].value_counts().values
#
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#
init_notebook_mode(connected=True)

data = [ dict(
        type='choropleth',
        locations = states,
        z = salescount, 
        locationmode = 'USA-states',
        colorbar = dict(
            title = "Salescount")
        ) ]

layout = dict(
    title = 'US used car sales by states',
    geo = dict(
        scope = 'usa',
        projection=dict(type='albers usa')
    )
)

fig = dict(data=data, layout=layout)
iplot(fig, filename='d3-cloropleth-map')

