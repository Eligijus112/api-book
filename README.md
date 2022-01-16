# Machine learning serving

A book about how to create a production level machine learning serving API with Flask, Gunicorn and Docker for people who have more of a mathematical background than computer science. 

The framework to create the book is **jupyter books**: https://jupyterbook.org/intro.html

The full rendered book can be viewed via: https://eligijus112.github.io/api-book/

# Contributions 

If you enjoyed the book and feel like donating, feel free to do so. The link to do a one time donation is [via Stripe](https://buy.stripe.com/14k17A6lQ8lAat2aEI). 

Additionaly, if you want me to add another chapter or to expand an existing one, please create an issue on [Github](https://github.com/Eligijus112/api-book).

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

# Necesary command to run before building the book 

There are some APIs that need to be running localy in order for the book to render. The commands to run the APIs: 

## Root calculation API example

```
cd api-book/chapter-5-API/api_full_example
uvicorn app:app --port 7999
```

## JWT token example

```
cd api-book/chapter-6-production-tools/jwt_token_example
uvicorn app:app --port 8000
```

## Local ML API

```
cd api-book/chapter-7-final-serving/ML_API
uvicorn app:app --port 8001
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

# Publishing the book to github 

To publish the rendered book to github use the command:

```
cd api-book
ghp-import -n -p -f _build/html
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

After the building of the image, you can push it to DockerHub. The command to push the image to DockerHub is:

```
docker push eligijusbujokas/ml-serving-book[:<tag>]
```

The book is publicly available as an image in DockerHub. The address of the repository is: 

https://hub.docker.com/repository/docker/eligijusbujokas/ml-serving-book/general

To pull the latest image use: 

```
docker pull eligijusbujokas/ml-serving-book:latest
```

To create the container with the access to the book use: 

```
docker run -d -p 4000:80 eligijusbujokas/ml-serving-book
```