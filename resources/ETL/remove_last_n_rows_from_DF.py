# Import Required Libraries
import pandas as pd
import sys

# Create a dictionary for the dataframe
dict = {
  'Name': ['Alex', 'Bob', 'Jane', 'Ted', 'Abi', 'Al', 'Rafa'],
  'Age':  [22,     20,     45,    21,     22,   44,    37],
  'Marks': [90,    84,     33,    87,     82,   99,   100]
}
 
# Converting Dictionary to 
# Pandas Dataframe
df = pd.DataFrame(dict)
print('----------')
print('df=', df)


# Number of rows to drop
# n = 3
n = int(sys.argv[1])
print('n=', n)
 
# Dropping last n rows using drop
df.drop(df.tail(n).index, inplace = True)
 
# Printing dataframe
print('----------')
print('df=', df)
