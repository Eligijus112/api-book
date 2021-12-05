# The base image from where we are building the container;
# All the official images can be found in DockerHub
FROM ubuntu:20.04

# Intalling all the packages that will be necessary for the container
# For now, we are only installing python3, pip and c++ compiler for the ubuntu system
RUN apt update && apt install -y \
    python3-pip \
    gcc 

# We can make and set a working directory in the container 
WORKDIR /ramen-app 

# Copying all the files needed from the local computer to the container 
COPY netflix_titles.csv . 
COPY get_top_bigrams.py . 
COPY requirements.txt . 

# Installing all the python packages needed for the analysis 
RUN pip install -r requirements.txt

# Running the python script that will generate the top bigrams
CMD ["python3", "get_top_bigrams.py"]