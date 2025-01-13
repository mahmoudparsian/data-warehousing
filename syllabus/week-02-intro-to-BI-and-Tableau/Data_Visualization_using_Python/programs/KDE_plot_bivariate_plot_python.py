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


sns.kdeplot(x=iris["SepalLengthCm"],
            y = iris["PetalLengthCm"],
            linewidth = 0.5,
            fill = True,
            multiple = "layer",
            cbar = False,
            palette = "crest",
            alpha = 0.7)
plt.show()