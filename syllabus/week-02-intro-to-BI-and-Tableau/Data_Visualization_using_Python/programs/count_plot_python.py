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

sns.countplot(data = df_students, 
              x = "race/ethnicity", 
              hue = "gender", 
              palette = "plasma")
plt.show()

