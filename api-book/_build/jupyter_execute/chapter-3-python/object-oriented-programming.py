#!/usr/bin/env python
# coding: utf-8

# # Classes and objects
# 
# ## Basic definitions
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

# ### Python "magic" methods
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


# ### Constructors 

# A constructor is a special type of function of a class which initializes objects of a class. In Python, the constructor is automatically called when an object is beeing created. 
# 
# The constructor is a magic function denoted as `__init__()`. 

# In[6]:


# Equivalent statements
Bob = Employee("Bob", "Smith", "Sales")
Rob = Employee.__init__(Employee, "Rob", "Smith", "Sales")


# ### Object attributes 
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

# ### Object methods 
# 
# An object method is a callable function that is associated with an object. Each object method only uses the attributes of the object it is called on. For example, to get the full names of the employees, we can use the method `get_full_name()`:

# In[9]:


print(f"Jane's full name: {Jane.get_full_name()}")
print(f"John's full name: {John.get_full_name()}")


# ## Object state
# 
# An object state is all the data that is stored in the object. The data includes attributes, methods and other data. The state of an object is dynamic because it can change over time. 
# 
# For example, let's create a new class **Human**:

# In[10]:


class Human: 
    def __init__(self, name, surname, age):
        """
        Template for human object; Attributes:

        name - name of the human
        surname - surname of the human
        age - age of the person
        """
        self.name = name 
        self.surname = surname
        self.age = age

    def increase_age(self, amount):
        """
        Method to increase the age of the human by the given amount
        """
        self.age += amount
    
    def get_age(self):
        """
        Method to get the age of the human
        """
        return f"My name is {self.name} and my age is: {self.age}"


# In[11]:


# Creating a 25 year old John Doe
John = Human("John", "Doe", 25) 

# Initial age value 
print(f"{John.get_age()}")


# The initial state of the age of John Doe is 25. We can change that using the method `increase_age()`:

# In[12]:


# Increasting the age 
John.increase_age(1)

# What is the age now?
print(f"{John.get_age()}")


# The internal state of the object has changed and it effected **only** John.

# ## Class inheritance 
# 
# Class inheritence in programming is a mechanism that allows one class to inherit the attributes and methods of another class. 
# 
# In Python, the syntax is very simple:
# 
# ```
# class DerivedClass(BaseClass):
#     ...
#     ...
# ```
# 
# All the methods in the `DerivedClass` are inherited from the `BaseClass`.

# For example, lets a new class called `President` that inherits from the `Human` class:

# In[13]:


class President(Human):
    def __init__(self, name, surname, age, country, years_in_service):
        """
        Template for president object; Attributes:

        name - name of the president
        surname - surname of the president
        age - age of the president
        country - country of the president
        years_in_service - years of service of the president
        """
        super().__init__(name, surname, age)
        self.country = country
        self.years_in_service = years_in_service

    def introduce(self):
        """
        Method to introduce the president
        """
        return f"My name is {self.name} {self.surname} and I am a president of {self.country} serving for {self.years_in_service} years"


# The constructor of `President` has a function called `super()` that calls the constructor of the base class and provides it with all the necessary arguments.

# In[14]:


# Lets create the past president of USA
Donald = President("Donald", "Trump", 62, "USA", 8)

# Introduce yourself 
print(Donald.introduce())


# ## Encapsulation 
# 
# Encapsulation is the packing of data and functions that work on that data within a single object. By doing so, you can hide the internal state of the object from the outside. This is done by defining the attributes of an object as either: 
# 
# * Public
# * Protected
# * Private
# 
# All the public variables in a class are accessible from outside the class and do not have any underscores infront of them `<name>`. 
# 
# The members of a class that are declared protected are only accessible to a class derived from it and have 1 underscore in front of them `_<name>`.
# 
# All the private variables are not accessible from outside the class and have a double underscore infront of them `__<name>`.

# In[15]:


# Lets create an example class of an animal 
class Animal:
    def __init__(self, name, species, age):
        """
        Template for animal object; Attributes:

        name - name of the animal
        species - species of the animal
        """
        self.name = name 
        self._species = species
        self.__age = age
    
    def increase_age(self, amount):
        """
        Method to increase the age of the animal by the given amount
        """
        self.__age += amount

    def print_info(self):
        """
        Get the animal information 
        """
        return f"My name is {self.name}, I am a {self._species} and my age is: {self.__age}"

# Lets create penguin 
penguin = Animal("Happy Feet", "Penguin", 1)

# Trying to access the private variable will result in an error
try:
    print(penguin.__age)
except AttributeError as e:
    print(f"Error: {e}")


# The above error is a bit missleading, because the private variable is not accessible from outside the class but it DOES exist. Only methods of the same class can access it and modify it.

# In[16]:


# Initial information
print(penguin.print_info())

# Adding one year to the age
penguin.increase_age(1) 

# New information
print(penguin.print_info())


# Secondly, in Python, there is no existence of **private** instance variables that cannot be accessed except inside an object. We can freely access the private variables of an object (`_species`).
# 
# However, a convention is being followed by most Python coders that a name prefixed with an underscore should be treated as a non-public part of the API or any Python code, whether it is a function, a method, or a data member.
# 
# What happens to the inherited public, private and protected members of the base class? Lets extend the above class: 

# In[17]:


# Lets create a domesticated animal class 
class DomesticatedAnimal(Animal):
    def __init__(self, name, species, age, owner):
        """
        Template for domesticated animal object; Attributes:

        name - name of the animal
        species - species of the animal
        age - age of the animal
        owner - owner of the animal
        """
        super().__init__(name, species, age)
        self.owner = owner
    
    def increase_age(self, amount):
        return super().increase_age(amount)

    def print_info(self):
        """
        Prints all the information about the animal
        """
        return f"My name is {self.name}, I am a {self._species} and my age is: {self.__age} and I am owned by {self.owner}"

# Lets create an instancte of the class
domesticated_penguin = DomesticatedAnimal("Happy Feet", "Penguin", 1, "Old McDonald")

# Lets try increasing the age 
domesticated_penguin.increase_age(1)

# Lets try to access the private variable 
try:
    print(domesticated_penguin.print_info())
except AttributeError as e:
    print(f"Error: {e}")


# Even though we inherited everything from the `Animal` class to the `DomesticatedAnimal` class, we still cannot access the private variable `__age` from the other class. 
# 
# Altough we can augment the internal variable `__age` with a new method `increase_age()` which calls the base class method. 

# # Summary 
# 
# The most important thing from this chapter to remember is that **everything in Python is an object**. This means that:
# 
# * The created object has a template class. 
# * The template class has a constructor.
# * The object has attributes and methods which can be reached via the `(.)` operator.
# * You can chain multiple classes together using class inheritence. 
