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

csv_data_file = "students_performance_in_exams.csv"
df_students = pd.read_csv(csv_data_file) 

print(df_students)

#exit()

sns.violinplot(data = df_students, 
               y = df_students["reading score"], 
               x = df_students["gender"], 
               linewidth =1, 
               scale = "count",
               width = 0.5, 
               inner = "quartile", 
               orient = "v", 
               palette = "Set2")
plt.xlabel('Gender', size= 14)
plt.ylabel('Reading Score', size = 14)
plt.title('Reading Score by Gender', size= 15)
plt.xticks([])
plt.grid(True)
plt.show()