# Machine learning serving

A book about how to create a production level machine learning serving API with Flask, Gunicorn and Docker for people who have more of a mathematical background than computer science. 

The framework to create the book is **jupyter books**: https://jupyterbook.org/intro.html

# Creating the virtual environment 

```
virtualenv api_book
source api_book/bin/activate
pip install -r requirements.txt
```

To add the virtual environment to Jupyter notebooks use the command:

```
python -m ipykernel install --user --name=api_book
```

# Creating and editing notebooks 

One of the main types of pages in this book are jupyter notebooks. To start a jupyter notebook session use the command:

```
jupyter notebook
```

# Rendering the book localy 

Before rendering the book be sure to activate the virtual environment! 

```
source api_book/bin/activate
```

Building of the book:

```
jupyter-book build api-book
```

# Serving the book via docker and Nginx

To serve the book across multiple computers, servers or whatever place that Docker is installed in, we can build an image and create a container with which we can access the book. 

The internal container port that serves the book content is **80** (the default Nginx port). 

## Building an image localy

The created html of the book can be accesed via **api-book/_build/html**. To create a docker container that serves the book using nginx, first build the image:

```
docker build -t eligijusbujokas/ml-serving-book[:<tag>] . 
```

Running the container on port 4000 on the local machine:

```
docker run -p 4000:80 eligijusbujokas/ml-serving-book[:<tag>]
```

The **[:<tag>]** part is optional and should be used only for the collaborators of this project.

To access the book, in your web browser go to: 

```
http://localhost:4000
```

And the book should be rendered. 

## Using DockerHub 

The book is publicly available as an image in DockerHub. The address of the repository is: 

https://hub.docker.com/repository/docker/eligijusbujokas/ml-serving-book/general

To pull the latest image use: 

```
docker pull eligijusbujokas/ml-serving-book:latest
```

To create the container with the access to the book use: 

```
docker run -p 4000:80 eligijusbujokas/ml-serving-book
```

## Accessing the book via the Digital Ocean server

The container is built in my custom server and can be reached via: 


http://eligijus.me:4000


