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
plt.plot(df.Year, df.Unemployment_Rate, marker = 'o', color = 'black', 
         linewidth = 0.9, linestyle = '--',
         markeredgecolor = 'blue', 
         markeredgewidth = '2.0', 
         markerfacecolor = 'red', markersize = 7.0)
plt.title('Trend of unemployment rate', color = 'Blue', size = 14)
plt.xlabel('Year', size = 14)
plt.ylabel('Unemployment Rate', size = 14)
plt.style.use('fivethirtyeight')
plt.grid(True)
plt.xticks(rotation = 30)
plt.show()
