import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Create a sample dataframe
data = {'a': [1.1, 2.2, 3.3, 4.4, 9.0, 7.0], 
        'b': [1.4, 2.5, 3.5, 4.4, 10.0, 8.0], 
        'c': [3.1, 4.0, 5.0, 5.5, 12.0, 9.0],
        'd': [3.0, 4.2, 5.5, 5.4, 12.0, 10.0]}
df = pd.DataFrame(data)
print(df)

# Create the heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
plt.show()
