#!/usr/bin/env python
# coding: utf-8

# # Python 

# Anecdotally, Python is considered to be **"the second best language in almost every field of computing."**. Due to its versitality, the growth and popularity of this programming language has grown immensly since its first version which was released in 20 February 1991 by Guido van Rossum. As per the PYPL index{cite}`pypl:index`: 
# 
# ![popularity-index](media/popularity-index.png)
# 
# Based on the searched tutorials for a given language, Python is the most popular programming language in the world as of 2021 November.
# 
# The foundational piece of software to create and serve machine learning models is Python. Every other technology and programs which will be covered in this book acts as "helpers" for Python to ingest input from the user and give output.

# ## Zen of Python 

# There are rules of programming which every developer should follow, especially when coding with Python. The rules (or the Zen of Python) are{cite}`python:zen`: 
# 
# * Beautiful is better than ugly.
# * Explicit is better than implicit.
# * Simple is better than complex.
# * Complex is better than complicated.
# * Flat is better than nested.
# * Sparse is better than dense.
# * Readability counts.
# * Special cases aren't special enough to break the rules.
# * Although practicality beats purity.
# * Errors should never pass silently.
# * Unless explicitly silenced.
# * In the face of ambiguity, refuse the temptation to guess.
# * There should be one-- and preferably only one --obvious way to do it.
# * Although that way may not be obvious at first unless you're Dutch.
# * Now is better than never.
# * Although never is often better than *right* now.
# * If the implementation is hard to explain, it's a bad idea.
# * If the implementation is easy to explain, it may be a good idea.
# * Namespaces are one honking great idea -- let's do more of those!
# 
# If you understand all of these concepts and can explain them in simple terms to a non programming friend - congratulations, that is a sign of an experienced developer.

# # What is Python?

# For a great tutorial about Python please visit the official documentation of Python https://docs.python.org/3/.
# 
# Python is both a *programming language* and an *interpreter*, depending on the context.
# 
# A programming language is a language that converts a set of strings into a machine code. A programming language has it's own unique syntax and the way that it converts human readable code to machine readable code. The most essential objective of any programming language is to give instructions to the computer. 
# 
# An example of code in Python syntax is the following: 

# In[1]:


# Definining variables and assigning them values 
a = 5.1
b = 10.5

# Defining a function 
def add(a:float, b:float) -> float:
    """
    Return the sum of a and b
    """
    return a + b

# Invoking the function with the two variables 
print(f"The sum of {a} and {b} is {add(a, b)}")


# In order for my machine to evaluate the code above, **the Python interpreter needs to be installed on my computer**, the code editor which I am working on needs to identify the block to be a Python code snippet and the resources on my computer need to be available. 
# 
# A computer interpreter is a piece of software that translates human readable code to machine code. The phrase **"installing Python"** ussualy means downloading, unpacking and registering the Python interpreter to a machine. On a Linux machine, Python ussualy can be found in: 
# 
# ```
# /usr/local/bin
# ```

# ## Python installation 

# In order to install Python on an Ubuntu OS use the command: 
# 
# ```
# sudo apt install -y build-essential libssl-dev libffi-dev python3-dev python3-pip
# ```
# 
# The above command will install the latest version of Python and the Python package manager called **pip**.

# In[2]:


# Printing out the Python version in code
import sys
print(f"The Python version is {sys.version}")


# The **GCC** version is the version of C++ compiler that Python has access to. It uses C++ when converting code to machine instructions.

# In[3]:


# Printint out python version on Ubuntu command line 
get_ipython().system('python3 -V')


# ## Python process example
# 
# Let us say we have a piece of code in the file called **script.py**. The contents of the file are:

# In[4]:


get_ipython().system('cat scripts/script.py')


# The code in the script sends a very small batch of data to the link "www.google.com" and waits for the response. This process is done 5 times. To invoke the process, we can use the command line: 
# 
# ```
# python3 scripts/script.py 
# ```
# 
# A somewhat high level flow of the code is presented in the chart: 
# 
# ![python-flow](media/python-flowchart.png)
# 
# * First, the whole process gets a number (PID) and the CPU procedes with the thread. 
# * The python interpreter converts the human readable code to a machine code and transfers it to the compiler. 
# * The output from the compiler is returned and then then Python converts the output from the machine to human readable code. 
# * When the process is finished, the PID dissapears and nothing is stored in memory or other places in the computer. 
# 
# The process in action:

# In[5]:


get_ipython().system('python3 scripts/script.py ')


# No matter the complexity of the Python script and the objects it creates, the flow is very similar to all Python processes running on a given machine. 
# 
# This chapter is just a small taste of Python. There are huge frameworks and codes used by millions of users every day which are written in Python. All of the robust and popular packages of Python follow the same guiding programming priciples which will be covered in the next chapter of the book. 
