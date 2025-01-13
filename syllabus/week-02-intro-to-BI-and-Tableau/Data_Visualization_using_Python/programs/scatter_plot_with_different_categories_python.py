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

csv_data_file = "Iris.csv"
iris = pd.read_csv(csv_data_file) 

print(iris)

#exit()

sns.set_style("ticks")
sns.scatterplot(x = iris.SepalLengthCm, y = iris.PetalLengthCm, 
                hue = iris.Species, palette = "mako")
plt.xlabel("Sepal Length in cm", size = 10, color = "black")
plt.ylabel("Petal Length in cm", size = 10, color = "black")
plt.title("Sepal Length vs Petal Length", size =12, color = "black")
plt.xticks(color = "black")
plt.yticks(color = "black")
plt.legend(loc = "lower right")
plt.show()