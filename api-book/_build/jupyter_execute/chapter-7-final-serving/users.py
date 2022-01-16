#!/usr/bin/env python
# coding: utf-8

# # ML users 
# 
# In this chapter we will build the final production grade API to serve machine learning models. We will expand on all the concepts covered so far and augment them. By the end, we will have a fully working API that can be deployed to production.
# 
# The whole API will be built from the `ML_API/` directory in the current chapter. 
# 
# The first step is to create the user registration, authentification and deletion endpoints. 
# 
# Be sure to start up the api with the command: 
# 
# ```
# uvicorn app:app --port 8001
# ```
# 
# # User registration 
# 
# Just as in the previous chapter, we will create an endpoint that registers a user. This time, we will add a layer of security: we will hash the password before storing it in the database. This is done because we don't want to store plain text passwords in the database in case someone gets access to the database. To decrypt the password one needs to know the `secret key` which is only known to the server.  
# 
# The full script for the `Users` model: 

# In[1]:


get_ipython().system('cat ML_API/Users.py')


# In the `users` data model there are the following collumns:
# 
#     * `id`: the primary key
#     * `username`: the username
#     * `password`: the hashed password
#     * `email`: the email address of the user
#     * `enabled`: whether the user is enabled or not. If the user is not enabled, he/she will not be able to query the ML API.
#     * `created_at`: the date of registration 
#     * `updated_at`: the date of last update
# 
# The above collumns allows to fully control the users when they are using our API. The collumn `enabled` should be changed to True if a certain business rule is met (a monthly subscription, for example). 
# 
# ## Password obfuscation
# 
# One of the main concerns when putting user information on a database is how to store their passwords. If we store them in plain text in the database, anyone who has access to the database can see the passwords. Additionally, if the database is compromised, the passwords can be used to login to the database. To combat this, we will `encrypt` the passwords before storing them in the database.
# 
# `Encription` is a process of converting a piece of information into random data which can be deciphered with a key. 
# 
# In our case, the key is stored in the file `config.yml` which is stored in the server. Additionaly, we add `salt` - a random string that is added to the password before hashing. This is done to make the password more secure, because even if the password is compromised, the salt will be different on different servers.
# 
# Thus, the full flow of obfuscating the user defined passwords:
# 
# 1) Salt is added to the original password. 
# 2) The `Fernet` object is created with the secret key. 
# 3) The salt and the password are passed to the `encrypt` method of the `Fernet` object. 
# 4) The encrypted password is stored in the database. 
# 
# The `Fernet` class implement the symetric encryption algorithm. The basis of the symetric encryption is the **key** - the random string which we must save and not share with anyone. Only having the key can we decrypt the data. 

# ## User registration endpoints 
# 
# The endpoints are: 
# 
# **/register-user** - registers a user. The endpoint accepts a POST request with the following data: 
# 
# ```
# {
#     "username": <username>,
#     "password": <password>,
#     "email": <email>
# }
# ```
# 
# **/toggle-user-permission/<user_id>/<0 to disable or 1 to enable>** - PUT type endpoint. Toggles the `enabled` collumn of a user.
# 
# **/remove-user/<user_id>** - a DELETE request that removes a user via the user_id. 

# In[2]:


# Importing the request lib  
import requests

# Defining the base URL
url = "http://localhost:8001"

# Defining the user dict 
user_dict = {
    "username": "test",
    "password": "test",
    "email": "test@testmail.com"
}

# Sending the post request to the running API 
response = requests.post(f"{url}/register-user", json=user_dict)

# Getting the user id 
user_id = response.json().get("user_id")

# Printing the response 
print(f"Response code: {response.status_code}; Response: {response.json()}")


# In[3]:


# Querying the whole user database
from ML_API.database import engine 
import pandas as pd 

users = pd.read_sql_table("users", engine)

print(users)
print(f"\nObfuscated password:\n{users['password'].values[0]}")


# In[4]:


# Deleting the test user 
response = requests.delete(f"{url}/remove-user/{user_id}")

print(f"Response code: {response.status_code}; Response: {response.json()}")


# In[5]:


# Adding the test user once again and disabling it 
response = requests.post(f"{url}/register-user", json=user_dict)
print(f"Response code: {response.status_code}; Response: {response.json()}")

# Saving the user id 
user_id = response.json().get("user_id")

response = requests.put(f"{url}/toggle-user-permission/{user_id}/0")
print(f"Response code: {response.status_code}; Response: {response.json()}")


# # Summary 
# 
# To summarize, we have created a table called `users` in the database and the only way to interact with it is through 3 endpoints: 
# 
#     * (POST) `/register-user` 
#     * (PUT) `/toggle-user-permission/<user_id>/<0 to disable or 1 to enable>`
#     * (DELETE) `/remove-user/<user_id>` 
# 
# The passwords in the `users` table are encrypted and safe. 
