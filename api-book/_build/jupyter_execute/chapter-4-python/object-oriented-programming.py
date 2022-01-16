#!/usr/bin/env python
# coding: utf-8

# # Classes and objects
# 
# To put it simply, in object oriented programming, the code is structured around **objects**. 
# 
# An **object** is an instance of a class.
# 
# A **class** is a blueprint for creating objects, defined by its name in the namespace, its attributes and its methods.
# 
# In computing, a namespace is a set of signs (names) that are used to identify and refer to objects of various kinds. The names are saved as pointers somewhere in computer memory. A namespace ensures that all of a given set of objects have unique names so that they can be easily identified. To put it simply, *a namespace is a mapping from names to objects*.
# 
# A class in Python is defined with the keyword `class` following with the class name. Each class has a constructor, which is a method that is called when an object of the class is created. The constructor is called automatically when an object is created. The constructor is defined with an internal function \_\_init\_\_().
# 
# For example, lets create a class that creates an object of class **Employee** (I will explain every detail after the class initialization):

# In[1]:


# Name of the class
class Employee: 
    # The constructor 
    def __init__(self, name, surname, position):
        """
        In order to create an object of the class Employee, we need to pass:
        name - name of the employee
        surname - surname of the employee
        position - position of the employee
        """
        self.name = name 
        self.surname = surname
        self.position = position

        # Calculating the name length of the employee in construction time 
        self.name_length = len(name)

    # Defining a method for the object 
    def get_full_name(self):
        """
        This method returns the full name of the employee
        """
        return f"{self.name} {self.surname}"


# One might be wandering, what is the "**self**" argument in the __init__() function? The argument "self" is a reference to the object being created. The "self" argument is used to access the attributes and methods of the object. 
# 
# When creating an object, we skip the argument "self" and pass the other arguments to the constructor. 

# In[2]:


# Two employees
Jane = Employee("Jane", "Doe", "Manager") 
John = Employee("John", "Doe", "Sales")


# As you can see above, one blueprint (Employee class) was used to create two objects (Jane and John). 
# 
# This is exactly as a recipe works: you can have a recipe (or blueprint) for a cake and with that recipe make hundreds of cakes. 
# 
# One fact that should always be kept in one's mind is that **EVERYTHING in Python is an object**. All the imported packages, all the defined variables even the functions are objects. This means that everything has a **class** with which the object was created, attributes and methods.

# # Python "magic" methods
# 
# *Magic* or *dunder* methods in Python are special methods that start and end with the double underscores `__<name>__`. Magic methods are not meant to be invoked directly by the user, but the invocation happens internally from the class on a certain action. For example, when you add two numbers using the *+* operator, internally, the __add__() method will be called:

# In[3]:


a = 5
b = 4 

print(f"Addition results: {a + b}")
print(f"Addition using the magic method: {a.__add__(b)}")


# Every class has a lot of magic methods. To list them out, use the `dir()` function and search for the `__<name>__` pattern:

# In[4]:


# All the magic methods of the class Employee
magic_methods = [x for x in dir(Employee) if x.startswith("__")]
print(magic_methods)


# In[5]:


# All the methods of the int class in Python
magic_methods = [x for x in dir(int) if x.startswith("__")]
print(magic_methods)


# # Constructors 

# A constructor is a special type of function of a class which initializes objects of a class. In Python, the constructor is automatically called when an object is beeing created. 
# 
# The constructor is a magic function denoted as `__init__()`. 

# In[6]:


# Equivalent statements
Bob = Employee("Bob", "Smith", "Sales")
Rob = Employee.__init__(Employee, "Rob", "Smith", "Sales")


# # Object attributes 
# 
# An object attribute is a piece of data that is associated with an object. It cannot be called as a function. To access an object attribute, we use the dot operator (`.`).

# In[7]:


print(f"Employee position of Jane: {Jane.position}")
print(f"Surname of John: {John.surname}")
print(f"Name length of John: {John.name_length}")


# We can explicitly set any attribute to an object using the (`.`) operator as well. 

# In[8]:


John.salary = 1000 
print(f"John's salary: {John.salary}")

try:
    print(f"Jane's salary: {Jane.salary}")
except AttributeError as e:
    print(f"Jane does not have a salary yet!\nError: {e}")

Jane.salary = 2000
print(f"Jane's salary: {Jane.salary}")


# The objects are completely independent from each other. If we define a new attribute to Jane, it will not affect John and vice versa. 

# # Object methods 
# 
# An object method is a callable function that is associated with an object. Each object method only uses the attributes of the object it is called on. For example, to get the full names of the employees, we can use the method `get_full_name()`:

# In[9]:


print(f"Jane's full name: {Jane.get_full_name()}")
print(f"John's full name: {John.get_full_name()}")


# In[ ]:




