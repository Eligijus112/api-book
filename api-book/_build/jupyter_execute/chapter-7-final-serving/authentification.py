#!/usr/bin/env python
# coding: utf-8

# # ML users authentification
# 
# In the previous chapter we have created the user model. Now we need to implement the authentification of those users in the application.
# 
# We will use JWT tokens for authentification. 
# 
# Each token will last for 60 minutes and will only be issued to **existing** and **enabled** users. Additionaly, when requesting the token, the passwords must match the ones in the database.

# The API endpoint for token creation is: 
# 
# **/token** - POST request that accepts the following data: 
# 
# ```
# {
#     "username": "username",
#     "password": "password"
# }
# ```
# 
# If the credentials are correct, we will return a JWT token.

# # Token based functionalities
# 
# All the functionalities are in the **ML_API/jwt_tokens.py** file.

# In[1]:


get_ipython().system('cat ML_API/jwt_tokens.py')


# # Creating a JWT token for a user 
# 
# First of all, lets create a new user. 

# In[2]:


import requests 

# Defining the user dict 
user_dict = {
    "username": "eligijus",
    "password": "123456",
    "email": "eligijus@testmail.com"
}

# Sending the post request to the running API 
response = requests.post("http://localhost:8000/register-user", json=user_dict)

# Getting the user id 
user_id = response.json().get("user_id")

# Printing the response 
print(f"Response code: {response.status_code}; Response: {response.json()}")


# Now that the user is registered, we can try to create a token with the username and password. First, lets send a bad password: 

# In[3]:


response = requests.post("http://localhost:8000/token", json={'username': "eligijus", 'password': "654321"})

print(f"Response code: {response.status_code}; Response: {response.json()}")


# Now lets the send the password with which the user was registered:

# In[4]:


response = requests.post("http://localhost:8000/token", json=user_dict)

print(f"Response code: {response.status_code}; Response: {response.json()}")

# Saving the token 
token = response.json().get("token")


# If get the token successfully, for the remaining 60 minutes we should only use this token to make requests to the API. 

# ## Checking token validity
# 
# To check whether the given token is valid or not, we can use the endpoint: 
# 
# **/token_status/\<token\>** - a GET request that returns either that a token is valid (status code 200) or that it is not valid (status code 401).

# In[5]:


# Sending the request to inspect the token validity 
response = requests.get(f"http://localhost:8000/token_status/{token}")

print(f"Response code: {response.status_code}; Response: {response.json()}")


# In[6]:


# Sending a bad request to inspect the token validity 
response = requests.get(f"http://localhost:8000/token_status/{token[:-1]}")

print(f"Response code: {response.status_code}; Response: {response.json()}")

