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

explode = (0.1,0,0,0,0)
colors = sns.color_palette('pastel')[0:5]
plt.style.use("fivethirtyeight")
ethnicity_counts = df_students["race/ethnicity"].value_counts()
plt.pie(df_students["race/ethnicity"].value_counts(), 
        labels = df_students["race/ethnicity"].value_counts().index, 
        autopct=lambda pct: f"{pct:.1f}%\n({int(pct/100*ethnicity_counts.sum())})",
        colors = colors,
        pctdistance = 1.2,
        labeldistance  =0.5,
        explode =explode,
        shadow = True)
plt.title("Distribution of Different Ethnicties in the Class", size = 12)
plt.show()