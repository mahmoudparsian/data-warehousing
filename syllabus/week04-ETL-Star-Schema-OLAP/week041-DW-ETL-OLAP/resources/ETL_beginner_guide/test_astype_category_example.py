import pandas as pd

# Create a DataFrame
df = pd.DataFrame({'Class': ['A', 'B', 'C', 'A', 'B']})
print(df)
"""
  Class
0     A
1     B
2     C
3     A
4     B
"""

# Convert the 'Class' column to categorical
df['Class_as_category_type'] = df['Class'].astype('category')
print(df)
"""
      Class                  Class_as_category_type
0     A                      A
1     B                      B
2     C                      C
3     A                      A
4     B                      B
"""

print("df.dtypes=\n", df.dtypes)
"""
df.dtypes=
 Class                       object
Class_as_category_type    category
dtype: object
"""