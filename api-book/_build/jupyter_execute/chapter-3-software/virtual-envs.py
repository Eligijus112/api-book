#!/usr/bin/env python
# coding: utf-8

# # Virtual environments

# ## Introduction

# From the official documentation of Python{cite}`python:docs`: 
# 
# **"Python applications will often use packages and modules that don’t come as part of the standard library. Applications will sometimes need a specific version of a library, because the application may require that a particular bug has been fixed or the application may be written using an obsolete version of the library’s interface.** 
# 
# **This means it may not be possible for one Python installation to meet the requirements of every application. If application A needs version 1.0 of a particular module but application B needs version 2.0, then the requirements are in conflict and installing either version 1.0 or 2.0 will leave one application unable to run.** 
# 
# **The solution for this problem is to create a virtual environment, a self-contained directory tree that contains a Python installation for a particular version of Python, plus a number of additional packages. Different applications can then use different virtual environments. To resolve the earlier example of conflicting requirements, application A can have its own virtual environment with version 1.0 installed while application B has another virtual environment with version 2.0. If application B requires a library be upgraded to version 3.0, this will not affect application A’s environment."**
# 
# Throughout this book we will use a library called **virtualenv** to create the virtual environments. It is assummed that Python and pip are installed on a machine. To install virtual environment creation framework in Ubuntu use the command: 
# 
# ```
# pip install virtualenv==20.10.0
# ```
# 
# Official page of the project: https://virtualenv.pypa.io/en/latest/. 

# ## Global Python Interpreter 

# By default, Python interpreter (or just Python) is installed in the directory: 
# 
# ```
# /usr/local/bin
# ```
# 
# or 
# 
# ```
# /usr/bin
# ```
# 
# For example, on my machine the full path to the Python interpreter is: 
# 
# ```
# /usr/bin/python3.8
# ```
# 
# Every time the machine I am working on tries to run a Python a script, it uses that interpreter. Note that the version of that interpreter is **3.8**. 
# 
# The default path for the libraries are via: 
# 
# ```
# /usr/lib/python3.8
# ```
# 
# To get the full list of installed libraries use the command: 
# 
# ```
# pip freeze
# ```
# 
# In the default library directory, the command outputs alot of installed packages:
# 
# ```
# ...
# pyarrow==3.0.0
# pyasn1==0.4.8
# pyasn1-modules==0.2.8
# pycairo==1.16.2
# pycparser==2.20
# pycups==1.9.73
# pydata-google-auth==1.2.0
# pydot==1.4.1
# Pygments==2.9.0
# PyGObject==3.36.0
# PyJWT==1.7.1
# pymacaroons==0.13.0
# PyNaCl==1.3.0
# pyOpenSSL==19.1.0
# pyparsing==2.4.7
# pyRFC3339==1.1
# ...
# ```
# 
# The numbers after **==** symbolize the version of the package.
# 
# # Ramen ratings dataset
# 
# The dataset is taken from https://www.kaggle.com/residentmario/ramen-ratings. The data is about various ramen shops around the world and their ratings. The head of the data: 

# In[1]:


get_ipython().system('head ramen-ratings/ramen-ratings.csv')


# The objective of the **get_best_ramen.csv** script is to aggregate all the reviews around the world and create a ranking of the best ramen brands, regardless of Country, Style and Variety. 
# 
# The project ramen-ratings/ has two files: the data file and the python script. 
# 
# ```
# ├── get_best_ramen.py
# └── ramen-ratings.csv
# ```
# The command 
# 
# ## Using the Global Interpreter
# 
# ```
# python3 get_best_ramen.py 
# ```
# 
# will:
# 
# 1) Search for the default Python interpreter, which is **/usr/bin/python3.8**
# 2) When loading all the libraries for the script (*pandas*, *os* and *numpy*), the command will use the default libraries in **/usr/lib/python3.8/**
# 3) Run the script (convert it to machine language, wait for the compiler to respond and print out the input in human readable form) 

# In[2]:


get_ipython().system('python3 ramen-ratings/get_best_ramen.py')


# As we can see, the script outputed 10 best and 10 worst ramen brands. 

# ## Using virtualenv

# Imagine that a someone else wants to use the script **get_best_ramen.py** on their machine. If any package is missing (mainly, pandas or numpy) or their python version is too old, the script will not work.
# 
# This is a classic situation of **"I don't know, worked on my machine"**. In order to have a robust collaboration, we need to freeze both the Python interpreter and the packages it is using. That is the main usecase of virtualenv!
# 
# To create an empty environment (with no packages) with a Python version of 3.8 and the environment name of "ramen_env", use the command: 
# 
# ```
# virtualenv --python 3.8 ramen_env
# ```
# 
# The command will create a new directory in the ramen project: 
# 
# ```
# ├── get_best_ramen.py
# ├── ramen_env
# │   ├── bin
# │   ├── lib
# │   └── pyvenv.cfg
# └── ramen-ratings.csv
# ```
# 
# The two most important directories are ramen_env/bin - interprete directory - and ramen_env/lib - the library path for the virtual environment. 
# 
# To activate the environment use the command: 
# 
# ```
# source ramen_env/bin/activate
# ```
# 
# The *pip freeze* command will now show no installed packages. It is very encouraged to keep a file to track the package versions. A common file used is **requirements.txt**. To install all the libraries in the file, use the command (**be sure to activate the environment first!**):
# 
# ```
# pip install -r requirements.txt
# ```
# 
# Now the command **pip freeze** will output 5 packages (some of the packages are automatically included in pandas and numpy installation):
# 
# ```
# numpy==1.21.4
# pandas==1.3.0
# python-dateutil==2.8.2
# pytz==2021.3
# six==1.16.0
# ```
# 
# Now to use the Python interpreter created by virtualenv and the specific packages of that environment, we can use the command: 
# 
# ```
# <path-to-ramen-project>/ramen_env/bin/python <path-to-ramen-project>/get_best_ramen.py
# ```

# In[3]:


get_ipython().system('ramen-ratings/ramen_env/bin/python ramen-ratings/get_best_ramen.py')


# As we can see, the main difference is the outputed package versions: the default python installation uses Pandas 1.2.3 (versus 1.3.0 in the virtual env) and Numpy 1.21.3 (versus 1.24.4).

# # Summary 

# The term **virtual environment** sounds very fancy but in reality, it is just a location of Python interpreter, reference to its version and the path to the libraries. 
# 
# To create, activate and populate the virtual environment with packages use the bash template: 
# 
# ```
# virtualenv python --version <python version> <name of environment>
# source <name of environment>/bin/activate
# pip install -r requirements.txt
# ```
# 
# To use the enviroment: 
# 
# ```
# python <python script name>.py # If the environment is activated
# <name of environment>/bin/python <python script name>.py # If the environment is NOT activated
# ```

# 
