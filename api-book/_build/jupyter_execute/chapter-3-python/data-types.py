#!/usr/bin/env python
# coding: utf-8

# # Data types 
# 
# ## Strong and dynamic typing
# 
# In programming, a **strong typed** language is one that guarantees that the types of all variables are known at compile time. This means that the compiler can check the types of all variables at compile time and will not allow the program to run if the types are incorrect.
# 
# A **dynamic typed** language is one that allows the types of variables to be checked at run time. This means that the compiler can not check the types of all variables at compile time, but the program will run if the types are correct.
# 
# Python is a dynamic typed language. For example Python allows one to add an integer and a floating point number, but adding an integer to a string produces an error. The gain in flexibility of compiling everything at runtime add big flexibility but hinders performance in some cases.
# 
# In order to reduce the number of errors and make your code as bulletproof as possible, it is essential to understand data types and use them them correctly.

# # Data types in Python
# 
# A data type or simply type is an attribute of data which tells the compiler or interpreter how the programmer intends to use the data {cite}`wiki:data_type`. 
# 
# The most common data types in Python are: 
# 
# * Integer (int)
# * Floating-point number (float)
# * String (str)
# * Boolean (bool)
# * DateTime
# 
# To check for a specific type of data in Python, one can use the built in function **type**.

# In[1]:


# Importing the datetime library which holds the datetime type
import datetime

# Defining the variables
a = 1.0 
b = "1"
c = 1
d = True 
e = datetime.datetime.now()

# Checking the types
print(f"Type of {a} is: {type(a)}")
print(f"Type of {b} is: {type(b)}")
print(f"Type of {c} is: {type(c)}")
print(f"Type of {d} is: {type(d)}")
print(f"Type of {e} is: {type(e)}")


# Each data type takes up different space in computer memory. 

# In[2]:


# Importing the needed package
import sys 

# Checking the size of objects 
print(f"Size of the float object: {sys.getsizeof(a)} bytes")
print(f"Size of the str object: {sys.getsizeof(b)} bytes")
print(f"Size of the int object: {sys.getsizeof(c)} bytes")
print(f"Size of the boolean object: {sys.getsizeof(d)} bytes")
print(f"Size of the boolean object: {sys.getsizeof(e)} bytes")


# # Functionalities of various data types 

# Every Python data type has its own attributes and methods. You can read all of them following the official Python documentation: 
# 
# https://docs.python.org/3/library/datatypes.html
# 
# ## String data type 
# 
# String data type is probably the most popular data type in terms of methods used. To read the full list of string methods available: 
# 
# https://docs.python.org/3/library/stdtypes.html#str
# 
# Some examples:

# In[3]:


# Defining a string 
string = "hello world"
print(f"Original string: {string}")

# Capitalizing the string
print(f"Capitalized string: {string.capitalize()}")

# All calps 
print(f"All caps string: {string.upper()}")

# Checking if the string ends with a specific character
print(f"Does the string end with 'rld'?: {string.endswith('rld')}")

# Checking if the string starts with a specific character
print(f"Does the string starts with 'hell'?: {string.startswith('hell')}")

# Spliting the string into substrings; If no splitting char is defined, it will split by whitespace
print(f"Spliting the string into a list: {string.split()}")


# ## Datetime data type 
# 
# To read the full list of available datetime methods and other documentation visit:
# 
# https://docs.python.org/3/library/datetime.html
# 
# 
# A datetime object is a single object containing all the information from a date object and a time object.
# 
# Like a date object, datetime assumes the current Gregorian calendar extended in both directions; like a time object, datetime assumes there are exactly 3600*24 seconds in every day.
# 
# Some examples:
# 

# In[4]:


# Creating a datetime object
dt = datetime.datetime.now()
print(f"The created datetime object: {dt}")

# Getting the year from the datetime object
print(f"The year from the datetime object: {dt.year}")

# Getting the month from the datetime object
print(f"The month from the datetime object: {dt.month}")

# Getting the day from the datetime object
print(f"The day from the datetime object: {dt.day}")

# Extracting the date from the datetime object 
print(f"The date part: {dt.date()}")

# Converting to string (year - month - day hour:minute)
print(f"The datetime object as a string: {dt.strftime('%Y-%m-%d %H:%M')}")


# ## Float data type
# 
# To read the full list of available float methods and other documentation visit: 
# 
# https://www.geeksforgeeks.org/python-float-type-and-its-methods/
# 
# Some examples:

# In[5]:


# Defining the float data type 
float_number = 67.5
print(f"The float number: {float_number}")

# Is it an integer? 
print(f"Is the float number an integer? (no decimal part): {float_number.is_integer()}")

# Spliting the float into a ratio of two numbers
print(f"Two integers whose ratio produces the original float number: {float_number.as_integer_ratio()}")

# Hexadeciaml representation of the float number
print(f"Hexadecimal representation of the float number: {float_number.hex()}")

