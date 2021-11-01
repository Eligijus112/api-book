# API creation for data people

A book about how to create a production level API with Flask, Gunicorn and Docker for people who have more of a mathematical background than computer science. 

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

# Rendering the book 

Before rendering the book be sure to activate the virtual environment! 

```
source api_book/bin/activate
```

Building of the book:

```
jupyter-book build api-book
```