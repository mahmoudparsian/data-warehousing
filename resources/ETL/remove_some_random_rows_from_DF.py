# import libraries

import pandas as pd
import numpy as np
np.random.seed(10)

# number of rows to remove
num_of_rows_to_be_removed = 3

df = pd.DataFrame({"a":[1,2,3,4,5,6,7,8,9,10], \
                   "b":[10,20,30,40,50,60,70,80,90,100]})
print("df=", df)

# remove 3 rows
drop_indices = np.random.choice(df.index, num_of_rows_to_be_removed, replace=False)
df_subset = df.drop(drop_indices)
print("df_subset=", df_subset)


