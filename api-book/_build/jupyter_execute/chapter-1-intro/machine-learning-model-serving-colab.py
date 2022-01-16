#!/usr/bin/env python
# coding: utf-8

# # Simulating the ML model serving 

# This notebook is used to simulate the serving of the ML model with an interactive input. This is a suplementary notebook of the **Machine Learning serving** interactive book by Eligijus Bujokas. The whole project can be viewed via: https://github.com/Eligijus112/api-book

# # Loading Python packages 

# All the bellow packages are needed to make the interactive simulation possible. 

# In[1]:


# Json reading 
import json 

# Pickle reading 
import pickle

# Operating system functionality 
import os 

# Input simulation 
from ipywidgets import interactive, widgets, interact
from IPython.display import display

# Data wrangling 
import pandas as pd

# Making requests
import requests


# # Checking the xgboost version 

# We need to make sure that the xboost version in the Google Colab server is on par with the version which was used to create model. 

# In[2]:


# Checking the version 
import xgboost
if xgboost.__version__ != "1.5.0":
    os.system("pip install xgboost==1.5.0")


# # Reading the necesary objects from Github 

# Both of the files can be accesed in the public GitHub repository: https://github.com/Eligijus112/api-book/tree/main/api-book/ml_models. 
# 
# The **JSON** dictionary can be accesed with a simple GET request. 
# 
# The pickled machine learning model can be downloaded with the **wget** command from the terminal. Because the backend on which Google Colab notebooks are running is Linux with the installed wget functionality, we can access it in the notebooks with the **!** prefix. 

# In[3]:


# Loading the features in the master branch 
url = 'https://raw.githubusercontent.com/Eligijus112/api-book/main/api-book/ml_models/ml-features.json'
resp = requests.get(url)
features = json.loads(resp.text)
print(features)


# In[4]:


# Downloading the models
get_ipython().system('wget https://github.com/Eligijus112/api-book/raw/main/api-book/ml_models/ml-model-lr.pkl')
get_ipython().system('wget https://github.com/Eligijus112/api-book/raw/main/api-book/ml_models/ml-model-xgb.pkl')

# Reading the pickled model 
model_lr = pickle.load(open("ml-model-lr.pkl", 'rb'))
model_xgb = pickle.load(open("ml-model-xgb.pkl", 'rb'))

# Deleting the downloaded file 
get_ipython().system('rm ml-model-lr.pkl ')
get_ipython().system('rm ml-model-xgb.pkl ')


# In[5]:


# Defining the input preparation function 
def prepare_input(raw_input_dict: dict, features: dict) -> pd.DataFrame:
    """
    Function that accepts the raw input dictionary and the features dictionary and returns a pandas dataframe with the input prepared for the model.
    """
    # Extracting the key names 
    feature_names = list(raw_input_dict.keys())
    original_feature_names = list(features.keys())

    # Ensuring that all the keys present in **features** are in **raw_input_dict**
    missing_features = set(original_feature_names) - set(feature_names)
    if len(missing_features): 
        return print(f"Missing features in input: {missing_features}")

    # Iterating and preprocesing 
    prepared_features = {}
    for feature in feature_names:
        # Extracting the type of the feature 
        feature_type = features.get(feature) 

        # Converting to that type 
        feature_value = raw_input_dict.get(feature)
        
        if feature_type == "float64":
            feature_value = float(feature_value) 
        
        if feature_type == "int64":
            feature_value = int(feature_value)

        # Saving to the prepared features dictionary
        prepared_features[feature] = feature_value 
    
    # Creating a dataframe from the prepared features 
    df = pd.DataFrame(prepared_features, index=[0])

    # Ensuring that the names are in the exact order 
    df = df[original_feature_names]

    # Returning the dataframe 
    return df 


# # Interactive serving 

# The interactive model serving is done using Python and the ipywidgets framework: https://ipywidgets.readthedocs.io/en/latest/index.html

# ## Defining the input widgets

# In[6]:


# Model selection widget 
model_type_widget = widgets.Dropdown(
    options=['Logistic Regression', 'Xgboost'],
    value='Logistic Regression', 
    description="ML model type",
    disable=False
)

# Boolean for bomb planting event 
bomb_planted_widget = widgets.Checkbox(
    value=False,
    description='Has the bomb been planted?',
    disabled=False
)

# Boolean for the presence of the difusal kit
ct_defuse_kit_present_widget = widgets.Checkbox(
    value=False,
    description='Is there a difusal kit present in CT team?',
    disabled=False
)

# CT health share of total; the range is (0, 1.0)
ct_health_share_widget = widgets.FloatSlider(value=0.5, min=0.0, max=1.0, step=0.05, description='CT health share of total')

# Count of CT and T players which are alive
ct_players_alive_widget = widgets.Dropdown(
    options=list(range(0, 6, 1)),
    value=3,
    description='The number of alive CT players',
    disabled=False,
)

t_players_alive_widget = widgets.Dropdown(
    options=list(range(0, 6, 1)),
    value=3,
    description='The number of alive T players',
    disabled=False,
)

# Number of helmets in a team 
ct_helmets_widget = widgets.Dropdown(
    options=list(range(0, 6, 1)),
    value=3,
    description='CT helmets',
    disabled=False,
)

t_helmets_widget = widgets.Dropdown(
    options=list(range(0, 6, 1)),
    value=3,
    description='T helmets',
    disabled=False,
)


# ## Simulation function

# In[7]:


def get_prob(
    model_type,
    bomb_planted, 
    ct_defuse_kit_present,
    ct_health_share,
    ct_players_alive,
    t_players_alive,
    ct_helmets, 
    t_helmets
    ):
    """
    Interactive session to experiment with the created ML model 
    """
    # Creating the raw input dictionary 
    raw_input = {
        "bomb_planted": bomb_planted,
        "ct_defuse_kit_present": ct_defuse_kit_present,
        "ct_health_share": ct_health_share, 
        "ct_players_alive": ct_players_alive,
        "t_players_alive": t_players_alive,
        "ct_helmets": ct_helmets,
        "t_helmets": t_helmets
    }

    # Preparing the input for the model feature importance plot xgboost
    raw_input_df = prepare_input(raw_input, features)

    # Getting the probabilities 
    p = [0.5, 0.5]
    if model_type == "Logistic Regression":
        p = model_lr.predict_proba(raw_input_df)[0]
    elif model_type == "Xgboost":
        p = model_xgb.predict_proba(raw_input_df)[0]
    
    # Extracting the winning probability
    p_win = round(p[1], 3)

    # Returning the probabilities 
    print(f"Probability of CT winning: {p_win}")


# ## Simulation application 

# In[8]:


# Making the interactive session 
prob_widget = interactive(
    get_prob, 
    model_type=model_type_widget,
    bomb_planted=bomb_planted_widget, 
    ct_defuse_kit_present=ct_defuse_kit_present_widget,
    ct_health_share=ct_health_share_widget,
    ct_players_alive=ct_players_alive_widget,
    t_players_alive=t_players_alive_widget,
    ct_helmets=ct_helmets_widget,
    t_helmets=t_helmets_widget,
)

# Displaying the widget 
prob_widget

