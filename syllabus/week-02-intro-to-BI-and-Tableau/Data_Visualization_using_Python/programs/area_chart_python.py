## libraries:
##   pip install matplotlib
##   pip install seaborn
##   pip install plotly

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly as py
import plotly.express as px
import plotly.graph_objects as go

# Getting the data
Data = {'Year': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010, 2020],
        'Unemployment_Rate': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3, 7.9]
       }

df = pd.DataFrame(Data, columns = ['Year', 'Unemployment_Rate'])

# Creating the chart using matplotlib
fig = plt.figure(figsize = (5,4))
plt.fill_between(df['Year'], df['Unemployment_Rate'], color='skyblue', 
alpha=0.7)
plt.plot(df['Year'], df['Unemployment_Rate'], color='skyblue', linewidth = 2)
plt.xlabel("Year", size = 10)
plt.ylabel("Unemployment Rate", size = 10)
plt.title("Unemployment Rate Trend", size = 12)
plt.show()
