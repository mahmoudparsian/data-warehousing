## libraries:
##   pip install matplotlib
##   pip install seaborn
##   pip install plotly
##   pip install scikit-learn

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly as py
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler


csv_data_file = "Iris.csv"
iris = pd.read_csv(csv_data_file) 

print(iris)

#exit()

# Convert a column to float
iris['SepalLengthCm'] = iris['SepalLengthCm'].astype(float)
iris['SepalWidthCm'] = iris['SepalWidthCm'].astype(float)
iris['PetalLengthCm'] = iris['PetalLengthCm'].astype(float)
iris['PetalWidthCm'] = iris['PetalWidthCm'].astype(float)


correlation_matrix = iris.corr()
sns.heatmap(correlation_matrix, annot = True, cmap = "viridis", 
            fmt = "0.2f", linewidth = 0.5)
plt.title('Correlation Heatmap')
plt.xlabel('Features')
plt.ylabel('Features')
plt.xticks(rotation = 45)
plt.show()