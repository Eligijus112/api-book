#!/usr/bin/env python
# coding: utf-8

# # Docker in production 
# 
# In this section, we will use Docker to create an image which can be used to spawn a container that serves the "root calculating" API. 
# 
# The main logic is the same as in the previous section, but we wrap everything up in a Docker container: 
# 
# ![gunicorn-docker](media/docker-container.png)
# 
# The main technology here is the docker engine, which builds images and runs containers. The API code inside the container is the same as in the previous section. What is needed from a developer is to create a `Dockerfile` that is used for image nad container creation. 
# 
# Having that, we can spawn our containers inside any machine that has Docker installed. 
# 
# # Dockerfile 
# 
# The Dockerfile that creates the image is located in the same directory as the API code. The steps of creating the image are:

# In[1]:


get_ipython().system('cat gunicorn-api-example/Dockerfile')


# To build the image with the name `root_api` use the command (run in the directory with the Dockerfile):
# 
# ```
# docker build -t root_api .
# ```
# 
# To spin up the container, use the command: 
# 
# ```
# docker run root_api
# ```
# 
# The output from the terminal should look like: 
# 
# ```
# ...
# 2021-12-25 10:43:24,742 INFO supervisord started with pid 1
# 2021-12-25 10:43:25,745 INFO spawned: 'gunicorn_api' with pid 8
# 2021-12-25 10:43:27,089 INFO success: gunicorn_api entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
# ```
# 
# This means that inside the container, the API is running on localhost:8000 and is ready to accept requests. 
# 
# But querying the API via http://localhost:8900/root?number=25&n=0.86 will produce an error: "The site cannot be reached". 

# # Setting up the ports 
# 
# By default, docker does not open up any ports so no request can come in. Previously, when we tried to access the localhost:8900 we got an error. This is because no program is listening on the port. What we need to do is to: 
# 
# * Say to to the container to listen to port 8900. 
# * Reroute everything that comes through the port 8900 to the program running `inside` the container on port 8900.
# 
# Keep note that we can choose any free port both on the local machine and inside the container. 
# 
# ![gunicorn-docker](media/port-linking.png)
# 
# To enable the above schema, we need to add the `-p` parameter to the `docker run` command: 
# 
# ```
# docker run -p 8900:8900 root_api
# ```
# 
# Now, if we query the API via http://localhost:8900/root?number=25&n=0.86, we should get the correct results: 
# 
# ```
# {"root":15.93046333819077}
# ```
# 
# The high level flow of the request: 
# 
# 1.) The request comes in to the localhost's port 8900. 
# 
# 2.) The docker container is instructed to listen to that port and redirect the request to the internal port 8900 of the container.
# 
# 3.) Internally, the gunicorn API is binded to port 8900 that handles the request logic. 
# 
# 4.) The response is sent back to the original client.  

# # Whats next?
# 
# The above API is very simple but the concept of using Docker, opening ports and using supervisor, Gunicorn and FastAPI can be generalized to very complex and big applications.
# 
# Before creating our final machine learning API, we need to talk about a few more concepts. One of the most crucial subjects is the user authentification which can use our API. 
