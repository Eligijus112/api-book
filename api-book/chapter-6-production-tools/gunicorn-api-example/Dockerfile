# Base image. We will use the Ubuntu base image and populate it 
FROM ubuntu:20.04 

# Updating all the base packages and installing python and pip 
RUN apt-get update && apt-get install -y python3-pip

# Installing supervisor to manage the API processes
RUN apt-get install -y supervisor

# Creating the working directory **inside** the container. All the subsequent commands will be executed in this directory. 
WORKDIR /app

# Copying the requirements.txt file to the container. The . means that copy everything to the current WORKDIR (which is /app) 
COPY requirements.txt .

# Installing every package in the requirements.txt file
RUN pip3 install -r requirements.txt

# Copying over the code to the container
COPY get_n_root.py .

# Copying the configuration for the supervisor process 
COPY gunicorn_config.conf /etc/supervisor/conf.d/gunicorn_config.conf

# Running the gunicorn process
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]