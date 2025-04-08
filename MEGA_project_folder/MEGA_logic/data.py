import pandas as pd
from MEGA_project_folder.params import *

"""
basic info
- prints basic characteristics of the merged dataset.
"""
df_de_merged = pd.read_csv("/root/code/senetan/MEGA_project/data/df_de_merged_update_timeline.csv")

print("shape:", df_de_merged.shape)
print("columns:", df_de_merged.columns.tolist())
print("df_de_merged data types:")
print(df_de_merged.dtypes)

nan_counts = df_de_merged.isnull().sum()
print(nan_counts)

"""
ensures that df_de_merged is sorted in ascending order by 'datetime'
"""

# ensure the datetime column is in datetime format
df_de_merged['datetime'] = pd.to_datetime(df_de_merged['datetime'])

# sort the dataframe chronologically and reset the index
df_de_merged = df_de_merged.sort_values(by='datetime', ascending=True).reset_index(drop=True)

#print("df_de_merged sorted in chronological order:")
#print(df_de_merged.head())
