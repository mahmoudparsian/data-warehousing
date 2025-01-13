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

colors = ['green', 'salmon']
plt.figure(figsize = (5,7))
violin_parts = plt.violinplot([df_students[df_students['gender'] == 'male']['reading score'],
              df_students[df_students['gender'] == 'female']['reading score']], 
              showmeans = True, showmedians = True,
              widths = 0.1,
              positions = [1,1.4],
              vert = True,
              showextrema = True)
for pc, color in zip(violin_parts['bodies'], colors):
    pc.set_facecolor(color)
labels = ["Male", "Female"]
data = [df_students[df_students['gender'] == 'male']['reading score'], df_students[df_students['gender'] == 'female']['reading score']]
    
plt.text(1,16,"Male" ,ha='center', va = "top")
plt.text(1.4,16,"Female",ha='center', va = "top")

plt.xlabel('Gender', size= 12)
plt.ylabel('Reading Score', size = 12)
plt.title('Reading Score by Gender', size= 14)
plt.xticks([])
plt.grid(True)
plt.show()