#!/usr/bin/env python
# coding: utf-8

# # Machine learning API
# 
# Right now we have 3 database tables: 
# 
# * Users
# * Requests
# * Responses
# 
# Additionaly, we have created a machine learning model along with the input schema. It is time to create a working API using FastAPI to serve predictions. 
# 
# # Loading the ML model to memory 
# 
# The most efficient way to load an ML model to memory is to save it during the initiation of the FastAPI application. It is a common mistake to read the model file and the schema file everytime a new request comes in and then apply it. 
# 
# We should import the model objects and create any additional objects at the top of the main **app.py** script where the API object is beeing created. 
# 
# The necessary utilities: 

# In[1]:


get_ipython().system('cat ML_API/machine_learning_utils.py')


# The loading of the model occurs right before defining the endpoints:
# 
# ```
# ...
# 
# # Creating the application object 
# app = FastAPI()
# 
# # Loading the machine learning objects to memory 
# ml_model, type_dict, ml_feature_list = load_ml_model()
# 
# ...
# ```
# 
# By loading the objects in the following way, the objects are saved in runtime memory and are not loaded from disk everytime a new request comes in. This makes the application much faster. 

# # API usage flowchart
# 
# A typical flow of the API is the following: 
# 
# * Register a user: 
# 
# ![registration](media/registration.png)

# The output of the registration logic is a JWT token which we attach in each of the requests to our API. 
# 
# * Prediction flow: 
# 
# 

# ![api-flow](media/API-flow.png)

# Each request to the API needs to have the JWT token attached to it. Then, along with the token, the data for the API is sent ant the following flow starts: 
# 
# 1) The user is beeing authenticated. 
# 
# 2) If the user is authenticated, then the request data is beeing validated for the ML model. 
# 
# 3) If the data is good, then the prediction is beeing made.
# 
# 4) The final response is sent. 
# 
# Along the way, the information is logged to the **Requests** and **Responses** tables. 

# All the code is available in the **app.py** script in the ML_API directory so lets try and apply the above flowchart!

# # API usage

# In[2]:


# Requests making  
import requests 

# Defining the constants for the API
url = 'http://localhost:8081'


# ## Creating a user 

# In[3]:


# Defining the user dict 
user_dict = {
    "username": "eligijus_bujokas",
    "password": "password",
    "email": "eligijus@testmail.com"
}

# Sending the post request to the running API 
response = requests.post(f"{url}/register-user", json=user_dict)

# Getting the user id 
user_id = response.json().get("user_id")

# Printing the response 
print(f"Response code: {response.status_code}; Response: {response.json()}")


# ## Getting the token 

# In[15]:


# Querying the API for the token 
response = requests.post(f"{url}/token", json=user_dict)

# Extracting the token from the response
token = response.json().get("token")

# Printing the response
print(f"Response code: {response.status_code}; JWT token: {token}")


# ## Getting the predictions
# 
# We need to first recap what was the input used to train the model. The features were: 
# 
# ```
# {
#   "input_schema": {
#     "columns": [
#       {
#         "name": "age",
#         "type": "numeric"
#       },
#       {
#         "name": "creatinine_phosphokinase",
#         "type": "numeric"
#       },
#       {
#         "name": "ejection_fraction",
#         "type": "numeric"
#       },
#       {
#         "name": "platelets",
#         "type": "numeric"
#       },
#       {
#         "name": "serum_creatinine",
#         "type": "numeric"
#       },
#       {
#         "name": "serum_sodium",
#         "type": "numeric"
#       },
#       {
#         "name": "sex",
#         "type": "boolean"
#       },
#       {
#         "name": "high_blood_pressure",
#         "type": "boolean"
#       }
#     ]
#   }
# }
# ```

# We will use a POST request to get the probabilities because we want to send the features and their values not as a collection of URL parameters but as a JSON object in the request body.

# In[16]:


# Creating the input dictionary
X = {
    'age': 25,
    'creatinine_phosphokinase': 1000,
    'ejection_fraction': 35,
    'platelets': 500000,
    'serum_creatinine': 8,
    'serum_sodium': 135,
    'sex': 1,
    'high_blood_pressure': 0
}

# Creating the header with the token 
header = {
    'Authorization': token
}

# Sending the request 
response = requests.post(f"{url}/predict", json=X, headers=header)

# Infering the response
print(f"Response code: {response.status_code}; Response: {response.json()}")


# The response dictionary has two keys: 
# 
# `yhat_prob` - probability of a death event 
# 
# `yhat` - the predicted class; 1 - death_event, 0 - no_death_event
# 
# The function `predict_ml` from the **app.py** file handles the request and the whole logic is presented here. 
# 
# The steps are: 
# 
# 1) Extract the token 
# 
# 2) Authenticate it
# 
# 3) Extract the inputs
# 
# 4) Log the request to database 
# 
# 5) Make the prediction 
# 
# 6) Log the response to database
# 
# 7) Return the response to the user 

# # Inspecting the results
# 
# All the sufficient information for tracking the API is in the **Users**, **Requests** and **Responses** tables. We can inspect them after our run of requests and responses.

# In[17]:


# Importing the connection 
import pandas as pd 
from ML_API.database import engine

# There maybe some legacy users beside eligjus_bujokas
users = pd.read_sql('select * from users', engine)
print(f"Users in the database:\n{users}")

# Tail of the requests
requests_data = pd.read_sql('select * from requests', engine)
print(f"--\nLast 5 requests:\n{requests_data.tail(5)}")

# Tail of the responses
response_data = pd.read_sql('select * from responses', engine)
print(f"--\nLast 5 responses:\n{response_data.tail(5)}")


# In[ ]:




