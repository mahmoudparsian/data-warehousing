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

green_diamond = dict(markerfacecolor='g', marker='o')

fig = plt.figure(figsize = (4,3))

_bp = plt.boxplot(
    [df_students[df_students['gender'] == 'male']['reading score'],
     df_students[df_students['gender'] == 'female']['reading score']],
    labels=['Male', 'Female'], 
    notch = True, 
    flierprops = green_diamond,
    vert = True, 
    patch_artist = True)

_colors = ['blue', 'red'] 
 
for patch, color in zip(_bp['boxes'], _colors): patch.set_facecolor(color) 
    
plt.xlabel('Gender', size= 8)
plt.ylabel('Reading Score', size = 8)
plt.title('Reading Score by Gender', size= 10)
plt.grid(True)
plt.show()