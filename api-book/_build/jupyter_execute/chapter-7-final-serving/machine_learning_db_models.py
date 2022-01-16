#!/usr/bin/env python
# coding: utf-8

# # ML database models 
# 
# Now that we have ways to handle users and a created machine learning model, we need a couple of more tables in our database to log the inputs to our model and the outputs that our model produces. 
# 
# For this, we will create two new database tables:
# 
# `requests` - logs the requests to the ML API. 
# 
# `responses` - logs the responses from the ML API.
# 
# The full Python code to generate them: 

# In[1]:


get_ipython().system('cat ML_API/MLDB.py')


# `PSQL` can hold a JSON data type in one of the collumns. We will save the what is necesary and used by the API in the `requests` table input `column`. Because we are saving a JSON file, we can be assured that if in the feature the feature inputs for the model changes, we will not have to create or delete any columns in the table. 
# 
# The same logic applies to the `reponses` table - the JSON which will be sent to the user is saved in the `response` column.
