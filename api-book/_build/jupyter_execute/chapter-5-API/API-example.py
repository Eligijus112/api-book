#!/usr/bin/env python
# coding: utf-8

# # API and PSQL integration example
# 
# In this section we will integrate the Python code with the PostgreSQL database. Each request and response will be stored in the database.
# 
# All the project is in the api-full-example folder:
# 
# ```
# ├── api-full-example
# │   ├── app.py
# │   ├── db.py
# │   ├── docker-compose.yml
# │   └── __init__.py
# ```
# 
# The database will be created in the docker container exactly as in the previous section. 
# 
# The connection and session objects will be created in the **db.py** file. 
# 
# The endpoint logic and the application object will be created in the **app.py** file.

# # Launching the API 
# 
# To launch the API, we will use the uvicorn command:
# 
# ```
# uvicorn api-full-example.app:app
# ```
# 
# The output in the terminal should look like: 
# 
# ```
# ...
# ...
# ...
# 
# INFO:     Started server process [27205]
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
# ```
# 
# Upon launching the API, the all the code will be run from the **db.py** script: 
# 
# * Ensuring that the database ROOT_DB exists
# * Ensuring that the tables requests and responses exist
# * Creating the tables if not 
# * Creating the connection object
# 
# The **docker-compose.yml** file for database creation: 

# In[1]:


get_ipython().system('cat api_full_example/docker-compose.yml')


# 
# The full code of the **db.py** script is:

# In[2]:


get_ipython().system('cat api_full_example/db.py')


# The **app.py** script imports the requests and responses database models from the **db.py** file and creates the API application object.
# 
# Contents of the **app.py** file:

# In[3]:


get_ipython().system('cat api_full_example/app.py')


# # Querying and inspecting the flow of the API
# 
# Lets send a request to the API. 
# 
# NOTE: the API and the database needs to be running on the machine where this notebook is beeing executed. 

# In[4]:


# Import the API querying lib
import requests

# Defining some numbers and roots 
numbers = [1, 2, 3, 4, 5]
roots = [0.5, 0.4, 0.3, 0.2, 0.1]

# Zipping for the loop
numbers_and_roots = zip(numbers, roots)

for number_and_root in numbers_and_roots:
    # Unpacking the numbers and roots
    number, root = number_and_root

    # Creating the request
    response = requests.get(f'http://localhost:7999/root?number={number}&n={root}')

    # Checking the response status code
    print(f"Root {root} of {number}: {response.json()['root']}")


# After the request is sent to the API server, the request is logged immediately in the database. Each request gets a unique ID in the database and when it was created. 
# 
# Then the API server applies the code defined in the view **root_of_number** in app.py. 
# 
# Either the request is processed successfully or not it is logged to the database. 
# 
# The contents of the `requests` and `responses` tables: 

# In[5]:


import pandas as pd 
from api_full_example.db import engine 

# Listing last 5 requests
pd.read_sql("select * from requests", engine).tail(5)


# In[6]:


# Listing last 5 responses
pd.read_sql("select * from responses", engine).tail(5)


# This is the the most basic necessity of when creating an API: you need to track the request and responses in the database. You can add more fields about the requests like user agent, IP address, country of origin, etc. As well as the response: the content type, content length, in depth error messages, etc. 

# # Whats next? 
# 
# We have created an API that receives a request, calculates something, sends the reponse back to the client and logs some information to the database. 
# 
# In the next chapter of the book we will containerize the API and deploy it using Docker. Additionally, we will talk about technologies of Gunicorn and Nginx which will complete the full puzzle of deploying the API. 

# # Contributions 
# 
# If you enjoyed the book so far and feel like donating, feel free to do so. The link to do a one time donation is [via Stripe](https://buy.stripe.com/14k17A6lQ8lAat2aEI). 
# 
# Additionaly, if you want me to add another chapter or to expand an existing one, please create an issue on [Github](https://github.com/Eligijus112/api-book).

# 
