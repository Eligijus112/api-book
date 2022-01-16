#!/usr/bin/env python
# coding: utf-8

# # Wrapping the API into a production container
# 
# In the previous chapter, we have created an API that can log requests and return responses locally. We need to wrap everything up into a docker container to make it available to the outside world.
# 
# First off all, lets see the file structure and recap what is the logic behind each of the file and directory in the project folder.

# In[1]:


get_ipython().system('tree ML_API_docker -L 2')


# The `alembic` directory manages the migrations and that the changes in the python files get reflected in the database.
# 
# The `alembic.ini` file is the configuration file for the `alembic` package. It holds the connection string to the database and the location of the migration scripts. In a real life application you should not track this file because it contains the full connection URI. 
# 
# The `app.py` file is the main file of the API. It imports all the necesary logic to run and creates the FlaskAPI object which is used in runtime. 
# 
# The `database` directory holds all the database models and other associated logic. 
# 
# The `data_docker` directory links the data from PSQL in a docker container to the local machine. This way, if restart the container, all the data is saved and we do not need to rerun all the migrations.
# 
# The `docker-compose.yml` file creates the two containers: 1 for the PSQL service and 1 for the API service.
# 
# The `Dockerfile` handles the image creation for the API application. 
# 
# The `gunicorn_config.conf` is a configuration file for the supervisor application to serve the API using gunicorn.
# 
# The `__init__.py` file indicates for python that the whole directory is a package. This makes certain imports not break. 
# 
# The `ml_model` holds the files necesary for the machine learning model.
# 
# Lastly, the `requirements.txt` file holds the dependencies for the API.

# # Dockerfile
# 
# The dockerfile commands will create an image which can be used to spin up the docker container.

# In[2]:


get_ipython().system('cat ML_API_docker/Dockerfile')


# To build the image use the command: 
# 
# ```
# docker build -t ml-api .
# ```
# 
# # Running the containers
# 
# The built image is used in the docker-compose.yml file alongside another container for psql: 

# In[3]:


get_ipython().system('cat ML_API_docker/docker-compose.yml')


# The container for the ml-api will will link requests from 8999 port on the local machine to port 8900 inside the container. 
# 
# If the container goes down for some reason, the docker background process will restart it.
# 
# To spin up both the containers use the command: 
# 
# ```
# docker-compose up
# ```
# 
# Be sure to make the necesary migrations if this is the initial run of the containers: 
# 
# ```
# alembic revision -m "Creating migrations" --autogenerate
# ```
# 
# And apply them: 
# 
# ```
# alembic upgrade head
# ```

# # High level schema 
# 
# To get a better view of what processes get start after the command `docker-compose up`, lets illustrate the high level schema:
# 
# ![api-flow](media/api-production.png)

# Both of the containers are managed by docker. 
# 
# The only port where the requests can come in for the machine learning API is through the port **8999**. All the requests get redirected to the port **8900** inside the container. From there, gunicorn gives the request to one of the workers. 
# 
# The container with the PSQL database can be reached via port **5444** on the local machine. The data gets redirected to the port **5432** inside the container.

# # Using the API from the container
# 
# All the API calls will be done to the container which is running on the local machine.
# 
# ## Creating a user 

# In[4]:


# Importing the package 
import requests

# Defining the URL 
url = 'http://localhost:8999'

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

# In[5]:


# Registering the user to docker 
response = requests.post(f"{url}/token", json={"username": "eligijus_bujokas", "password": "password"})

# Extracting the token from the response
token = response.json().get("token")

# Printing the response
print(f"Response code: {response.status_code}; JWT token: {token}")


# ## Getting the predictions

# In[6]:


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


# # Conclusion 
# 
# The container accepts requests via the port 8999. If we have a running docker background process on any server, we can spin up this container and use the machine learning model imediatly. 
# 
# The API itself is served using `gunicorn` with **n** workers. 
# 
# Each worker is an `uvicorn` async server that will handle the requests. 
# 
# Gunicorn itself is managed using `supervisor`. 
# 
# If the container breaks, then docker daemon will automatically restart it. 

# # Contributions 
# 
# If you enjoyed the book and feel like donating, feel free to do so. The link to do a one time donation is [via Stripe](https://buy.stripe.com/14k17A6lQ8lAat2aEI). 
# 
# Additionaly, if you want me to add another chapter or to expand an existing one, please create an issue on [Github](https://github.com/Eligijus112/api-book).
