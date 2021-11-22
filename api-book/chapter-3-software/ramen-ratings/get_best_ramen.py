# Importing the package to read the data 
import pandas as pd 

# Importing the package for directory traversal
import os 

# Array math 
import numpy as np 

# Some info about the packages
print(f"Pandas version: {pd.__version__}")
print(f"Numpy version: {np.__version__}")

# Setting the directory to the current directory of the file 
_cur_dir = os.path.dirname(os.path.realpath(__file__))

# Naming the path to data 
_data_path = os.path.join(_cur_dir, 'ramen-ratings.csv')

# Reading the data 
d = pd.read_csv(_data_path)

# Renaming the first column
d.rename(columns={'Review #': 'n_reviews'}, inplace=True)

# Only leaving restaurants with >= 100 reviews
d = d[d['n_reviews'] > 100].copy()

# Converting the Stars collumn to float
d = d[d['Stars']!='Unrated'].copy()
d['Stars'] = d['Stars'].astype(float)

# Getting the total number of reviews by brand and country
n_reviews_brand = d.groupby(['Country', 'Brand'], as_index=False)['n_reviews'].sum()
n_reviews_brand.rename(columns={'n_reviews': 'n_reviews_w'}, inplace=True)

# Merging to the origianl dataset
d = pd.merge(d, n_reviews_brand, on=['Country', 'Brand'])

# Grouping by brand and getting the weighted average rating
d_agg = d.groupby(['Country', 'Brand'], as_index=False).apply(lambda x: np.sum(x.n_reviews * x.Stars / x.n_reviews_w))
d_agg.columns = ['Country', 'Brand', 'Rating']

# Sorting by Rating 
d_agg.sort_values(by=['Rating'], ascending=False, inplace=True)

# Reseting the index 
d_agg.reset_index(inplace=True, drop=True)

# Printing out the winners
print("\nTop 10 best ramen shops:")
print(d_agg.head(10))

print("\nTop 10 worst ramen shops:")
print(d_agg.tail(10))