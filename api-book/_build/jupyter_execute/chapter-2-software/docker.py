#!/usr/bin/env python
# coding: utf-8

# # Docker
# 
# ![docker-logo](media/docker-logo.png)
# 
# Since it's launch in March 20, 2013, docker has reshaped alot of companies' ideas about development and production. Docker enabled developers to isolate and have reproducable application results across **any** environment where the application is or would be running, given, that an environment has docker engine installed. A developer can simulate any production environment on his/hers computer. This environment isolation and seamless transition between development and production saves alot of time and headaches.    
# 
# ## What is docker?  
# 
# Docker is an **ecosystem of managing containers**. The definition splits into terms with definitions of their own:
# 
# * A **docker ecosystem** is a collection of *docker backend engine*, *docker image registry* and any other helper software for container and image managment.  
# 
# * A **docker container** is a runtime instance of a docker image. An informal definition of a container is that it is an isolated application with all the needed dependencies.
# 
# * **Runtime** is a phase of a program when the instructions (code) are beeing actively run on a CPU. While the program is running (is in *runtime*), it is assigned a PID.  
# 
# * An **instance** is an object that is created using a template (in docker universe - an image).
# 
# * A docker **image** is an ordered collection of root filesystem changes and the corresponding execution parameters for use within a container runtime.
# 
# * A **docker backend engine** is the main program that creates images, containers and manages every other process that is docker related. Nothing will run if docker backend is not installed on a system.  
# 
# * A **docker image registry** is an application that enables the storing, updating and downloading of docker images. The most popular image registry is **https://hub.docker.com/**. This book's image can be publicly accesed via https://hub.docker.com/repository/docker/eligijusbujokas/ml-serving-book
# 
# A high level graph of docker engine on a machine running it: 
# 
# ![docker-overview](media/docker-overview.png)

# At the bottom of the graph there is OS hardware components: RAM, CPU and space to store files, among other things. Docker interacts with the resources of the computer via the OS kernel. Therefore, there may be some glitches and bugs when working on docker in Linux vs on Windows, altough **most** of the time, the containers on both OS work the same. 
# 
# Every docker image has it's own space in the filesystem. 
# 
# Every running docker container has an isolated RAM, CPU, disk space and GPU resources that only it can reach. 

# ## Installing docker on Ubuntu
# 
# First, update the packages in the host machine:
# 
# ```
# sudo apt update
# ``` 
# 
# Next, install some prerequisites for apt package installation via HTTPS:
# 
# ```
# sudo apt install apt-transport-https ca-certificates curl software-properties-common
# ```
# 
# Then add the GPG key for the official Docker repository:
# 
# ```
# curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
# ```
# 
# Add the Docker repository to apt (Ubuntu package manager) sources:
# 
# ```
# sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
# ``` 
# 
# Docker engine installation:
# 
# ```
# sudo apt install docker-ce
# ```
# 
# Docker should now be installed, the daemon started, and the process enabled to start on boot. To check whether everything is OK use the command: 
# 
# ```
# docker run hello-world
# ```

# # Problem to solve 
# 
# We will try to analyze the top bigrams in Netflix movie titles. The code which we want to isolate and run is in `docker-example/get_top_bigrams.py` file. 

# In[1]:


get_ipython().system('cat docker-example/get_top_bigrams.py')


# We want the above code to run without errors and in the same way regardless of the underlying machine or OS. The only thing that is needed is docker. 

# ## Docker images 
# 
# Docker images are like recipes and docker containers are the cakes made out of those recipes. There can be alot of cakes, but only one recipe. 
# 
# ![docker-image-containers](media/image-containers.png)
# 
# Lets say we want to build an image that runs a container that calculates the most popular bigrams (two words separated by whitespace) from the Netflix movie descriptions.
# 
# Docker images are built with commands in **Dockerfiles**. An example dockerfile: 

# In[2]:


get_ipython().system('cat docker-example/Dockerfile')


# To build the image and store it in the local filesystem, use the command: 
# 
# ```
# docker build -t <image name> -f <path to Dockerfile directory>
# ```

# In[3]:


get_ipython().system('docker build -t netflix-bigrams docker-example')


# Note that the first building of the image takes a long time, because everything needs to be downloaded fresh. Additional builds will be faster, because some of the information is cached.
# 
# After the image is built, it is stored in (Ubuntu) */var/lib/docker/image* directory. When we "build" and image, docker engine creates entries and new files in the image directory and prepares to create a container in runtime using the gathered information in build time. 

# ## Docker containers 
# 
# Docker can only run containers with built images. To run a container with an image which has a known tag (in our case - **netflix-bigrams**), we can use the command:
# 
# ```
# docker run <image name>
# ```

# In[4]:


get_ipython().system('docker run netflix-bigrams')


# The container outputed the top bigrams used in netflix movie descriptions. 
# 
# After the container has done it's task, it is shutdown, all the data that was generated in the container is deleted and every bit of resource that the container was using is freed up for all other PIDs in the host machine.  

# ## Sharing docker images 
# 
# To run a container from an image in another computer or the cloud, the first thing to remember is that the host machine which will run the container has to have docker backend engine installed. 
# 
# To share the images, there are multiple options: 
# 
# ### DockerHub account 
# 
# Any user of docker can open a free or a business account in DockerHub via **https://hub.docker.com/**. After signing up, a user can push and pull images directly to and from the cloud. 
# 
# ```
# docker push <docker hub username>/<image name>
# ```
# 
# Then, if the image is public, any person can download the image using the command:
# 
# ```
# docker pull <docker hub username>/<image name>
# ```
# 
# For example, this book has an image in DockerHub and can be pulled using the command:
# 
# ```
# docker pull eligijusbujokas/ml-serving-book
# ```
# 
# ### Saving an image to an archive
# 
# To save an image into a sharable archive, use the command: 
# 
# ```
# docker save -o <name of archive>.tar.gz <image name>
# ```
# 
# This will create a .tar.gz file which can be ingested by docker in any machine with the command 
# 
# ```
# docker load --input <name of archive>.tar.gz
# ```

# # Contributions 
# 
# If you enjoyed the book so far and feel like donating, feel free to do so. The link to do a one time donation is [via Stripe](https://buy.stripe.com/14k17A6lQ8lAat2aEI). 
# 
# Additionaly, if you want me to add another chapter or to expand an existing one, please create an issue on [Github](https://github.com/Eligijus112/api-book).
