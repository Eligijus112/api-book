#!/usr/bin/env python
# coding: utf-8

# # JWT based authentification 
# 
# In the API world, authentification is a process where we want to authenticate a user. In real world applications, only authenticated users can access the API. Additionaly, we may want to track how much does a specific user query an API. 
# 
# To solve the complex issue of authentification, the current golden standart are the `JWT tokens`. 
# 
# `JWT` stands for JSON Web Token. 
# 
# The high level graph of the process: 
# 
# ![JWT-flow](media/jwt-flow.png)

# 1) The user requests a token, sending over his credentials (username and password). 
# 
# 2) The server checks the credentials and if they are correct, it generates a JWT token. The token gets sent back to the user. 
# 
# 3) Every time the user makes a request to any of the APIs on a certain server, it has to include the JWT token. Only the JWT token is used to authenticate the user.
# 
# # JWT token 
# 
# A JWT token is just a string that has three parts separated by dots:
# 
# ```
# <header>.<payload>.<signature> 
# ```
# 
# An example may look like this:
# 
# `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c` 
# 
# Thats it, the above string is a JWT token that has alot of information encoded into it. There are many libraries that can be used both to create and to decode a JWT token. In the subsequent chapters we will use Python implementations of JWT authentification and go through the details of the JWT token system. 
# 
# # The authentification flow 
# 
# All the code is in the `jwt-toke-example` directory. Be sure to run 
# 
# ```
# docker-compose up 
# ```
# 
# To spin up a PSQL server. 
# 
# Additionaly, start the API from the same directory:
# 
# ```
# uvicorn app:app --port 8000
# ```
# 
# ## Step 1: Requesting a token 
# 
# ### User registration
# 
# In the JWT flow, we still cannot escape the good old username and password combination. We need to store this information somewhere in the server and every time a user requests a new token, we need to check if the user credentials are correct. For this, we need to create an endpoint for user registration and then for token generation. Because of this reason, the whole process of authentification ideally should be done via HTTPS and not HTTP. For the purpose of this tutorial, we will use HTTP, because the concepts are exactly the same. HTTPS only adds a layer of obfuscation and encodes the transactions between user and server. 
# 
# The user database table is very straightforward. It contains the username, the password and the date it was created: 

# In[1]:


get_ipython().system('cat jwt-token-example/models.py')


# The endpoint for user creation is `/users/register`. To register we need to send a POST request with the following data:
# 
# ```
#     {
#         "username": <username>,
#         "password": <password>
#     }
# ```

# In[2]:


# Importing the request making lib 
import requests

# Making the request to the API to register the user 
response = requests.post(
    "http://localhost:8000/users/register", 
    json={"username": "eligijus", "password": "123456"}
)

if response.status_code in [200, 201]:
    print(f"Response: {response.json()}")


# Now that we have a registered user we can start implementing the logic of JWT token creation. 
# 
# ## Step 2: Creating the JWT token 
# 
# The library that creates the JWT token is called `pyjwt`. It is a Python library that can be used to create and decode JWT tokens. It is fully compliant with the [JSON Web Token standard](https://tools.ietf.org/html/rfc7519).
# 
# The token creation and inspection script is: 

# In[3]:


get_ipython().system('cat jwt-token-example/jwt_tokens.py')


# The logic of creating the token is in the `create_token()` function. Remember the JWT token structure: 
# 
# ```
# <header>.<payload>.<signature>
# ```
# 
# The `header` part encodes the algorithm and type needed to decode the token.
# 
# The `payload` part holds the dictionary of claims. The claims are the information that gets encoded into the token as a dictionary. 
# 
# The `signature` part is the signature of the token. It is used to verify the token by the python library. The `_SECRET` constant is used to construct the signature. That it why it should be kept only as a runtime variable in the variable where no one can access it. 
# 
# Lets query the endpoint `/token` using the credentials we used to register the user.

# In[4]:


# Making the request to the API to get the token
response = requests.post(
    "http://localhost:8000/token", 
    json={"username": "eligijus", "password": "123456"}
)

# Extracting the token 
token = response.json().get('token')

# Printing out the gotten token 
print(f"Token: {token}")


# The above token will be valid for 60 minutes and can be used to make requests to the API. If we make a request with a non existing user, we will get a `401 Unauthorized` error:

# In[5]:


# Making the request to the API to get the token
response = requests.post(
    "http://localhost:8000/token", 
    json={"username": "eligijus", "password": "12345"}
)

# Printing out the status code 
print(f"Response code: {response.status_code}")


# ## Step 3: Using the JWT token  
# 
# Every time a user makes a request to the API, we need to include the JWT token in the request. We will use the `Authorization` header to include the token and will send a GET request to our very well know number root calculating API. 

# In[6]:


# Defining the parameteres to send 
number = 88
n = 0.88

# Making the request with the token 
response = requests.get(
    f"http://localhost:8000/root?number={number}&n={n}",
    headers={"Authorization": f"{token}"}
)

# Printing out the status code and the result 
print(f"Response code: {response.status_code}")
print(f"Root {n} of {number} is: {response.json()}")


# If we use a bad JWT code, a user does not exist in the database or the token has expired, we will get a 401 Unauthorized response error:

# In[7]:


# Making the request with the token 
response = requests.get(
    f"http://localhost:8000/root?number={number}&n={n}",
    headers={"Authorization": "Hello I am a really legit token"}
)

# Printing out the status code and the result 
print(f"Response code: {response.status_code}")
print(f"Root {n} of {number} is: {response.json()}")

