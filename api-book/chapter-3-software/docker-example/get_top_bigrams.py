# Importing the necesary packages 
import os 
import pandas as pd 
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

# Extracting the current directory 
_cur_dir = os.path.dirname(os.path.abspath(__file__))

# Defining the path to data 
_data_path = os.path.join(_cur_dir, 'netflix_titles.csv')

# Reading the descriptions of movies
d = pd.read_csv(_data_path, usecols=["description"])

# Making a list of decsriptions
descriptions = d.values.flatten().tolist()

# Defining the stop words which will be emmited from the desctriptions
STOP_WORDS = [
    'in',
    'to',
    'on',
    'of',
    'by',
    'and',
    'with',
    'the',
    'as'
]

# Initializing the CountVectorizer
cv = CountVectorizer(ngram_range=(2,2), max_features=1000, stop_words=STOP_WORDS) 

# Fitting the cv on text
cv_fit = cv.fit_transform(descriptions)

# Extracting the feature names
feature_names = cv.get_feature_names_out()

# Calculating the number of occurance of features
feature_occurance = cv_fit.toarray().sum(axis=0)

# Creating a dataframe with the vocabulary
vocab_df = pd.DataFrame({
    "term": feature_names,
    "count": feature_occurance
})
vocab_df.sort_values(by='count', ascending=False, inplace=True)

# Printing out the top 20 phrases
print(vocab_df.head(20))