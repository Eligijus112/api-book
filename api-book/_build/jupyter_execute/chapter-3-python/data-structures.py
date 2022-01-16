#!/usr/bin/env python
# coding: utf-8

# # Data structures

# In programming, a data structure is the organization, management, and storage format of the data in the computer that enables efficient access and modification of it {cite}`wiki:data_structure`. Data structures lets a programmer write a more efficient and readable code. Knowing data structures may reduce the complexity of your program from **O(n)** to **O(1)**!
# 
# There are popular data structures available accross multiple programming languages like **lists**, **stacks**, **queues**, **dictionaries** and etc. 
# 
# Python is no exception. In this chapter, I will go over the more popular ones used in practise. 

# ## List
# 
# A list is sequence of several variables, grouped together and accesed via one name in the namespace. 
# 
# In Python, a list is defined with square brackets "[" and "]". Each element in the list is separated by a comma ",".  
# 
# To access specific elements in the list we use their index. 

# In[1]:


# A list of all numerics 
a = [1, 4, 7]

# A list of mixed datatypes 
b = [1, "1", True]

# Accessing elements
print(f"First element in the list 'a': {a[0]}; Second: {a[1]}; ...")


# In Python, lists have several built-in methods{cite}`python:data_structures`. One of the most popular used in practise: 

# In[2]:


# Initializing an empty list
a = [1, 1, 2, 3]
print(f"Initial list:\n{a}")

# Adding an element to the "back" of the list (appending to the back)
print(f"--- append() ---")
a.append(5)
print(f"List after appending an element:\n{a}")

# Reversing a list 
print(f"--- reverse() ---")
a.reverse()
print(f"List after reversing it:\n{a}")

# Sorting the elements; Works the best where all the data types of elements are the same
print(f"--- sort() ---")
a.sort()
print(f"Sorted list:\n{a}")

# Counting the number of occurance of elements 
print(f"--- count() ---")
elements = [1, 5, 60]
for element in elements:
    n = a.count(element)
    print(f"Times the number {element} occured in the list: {n}")

# Findining the index of certain elements 
print(f"--- index() ---")
for element in elements:
    try:
        print(f"The first occurance of element {element} in the list is at index {a.index(element)}")
    except ValueError:
        print(f"There is no element {element} in the list")


# A list in Python can be created using a list comprehension. List comprehension offers a shorter syntax when you want to create a new list based on the values of an existing list.

# In[3]:


# Creating a sequence of numbers and cubing them 
seq = list(range(-3, 4))
print(f"Original sequence: {seq}")

# Squering using the for loop
# Initializing an empty list 
a = []
for element in seq:
    a.append(element ** 2)

# Squering using list comprehension
# Note that an empty list namespace link does not need to be created prior
b = [x ** 2 for x in seq]

# Printing out the results 
print(f"For loop list: {a}")
print(f"List comprehension list: {b}")


# ## Dictionary 
# 
# A dictionary is a data type that holds information in *key -> value* pairs. Dictionaries are sometimes found in other languages as **associative memories** or **associative arrays**. Unlike sequences, which are indexed by a range of numbers, dictionaries are indexed by keys, which can be any immutable type. 
# 
# Dictionaries in Python are defined between curly brackets { }.
# 
# All the keys in the dictionary need be unique. To access a value in the dictionary we must use it's key. 

# In[4]:


# Defining a dictionary with two keys 
a = {
    "person_1": "Eligijus Bujokas",
    "person_2": "Bligijus Eujokas"
}

# Printing out the dictionary 
print(f"Initial dictionary: {a}")

# Getting the keys 
keys = list(a.keys())
print(f"Keys in dictionary: {keys}")

# Accessing the elements of the dictionary
print(f"Value of key {keys[0]} is: {a[keys[0]]}")
print(f"Value of key {keys[1]} is: {a.get(keys[1])}")

# To update a dictionary, we use the built in update() method
print(f"--- update() ---")
a.update({'person_3': "Sakojub Sujigile"})
print(f"Updated dictionary: {a}")


# ## Set
# 
# A set in Python is an unordered collection with no duplicate elements. Sets are defined between curly brackets just like dictionaries but do not have a key -> value logic. Each item in a set definition is separated by a comma. Python will only leave unique elements after the initialization. 

# In[5]:


a = {"eligijus", "bujokas", "bujokas"}

print(f"Initial set: {a}")


# A very useful functionality with sets in Python is the set operation functionality. We can obtain the intersection, difference and union of two sets. 

# In[6]:


a = set([x for x in range(-5, 4)])
b = set([x for x in range(-1, 7)])

print(f"Set a: {a}")
print(f"Set b: {b}")

print(f"Intersection of a and b: {a.intersection(b)}")
print(f"Difference a - b: {a.difference(b)}")
print(f"Difference b - a: {b.difference(a)}")
print(f"Union of both sets: {a.union(b)}")


# # Iterators
# 
# Formaly, an iterator in object oriented programming is an object that has methods that allows to proccess a collection of items one at a time.
# 
# Informaly, an iterator is an object that can be iterated upon. 
# 
# In Python, an iterator is an object that has two methods: \_\_iter_\_() and \_\_next\_\_().
# 
# When we iterate over the object, internaly, Python uses two built in methods - **iter()** and **next()** to traverse the iterator. 
# 
# For example, any list in Python has these methods: 

# In[7]:


# Defining a list 
a = [1, 1, 2, 3, 5]

# 'Extracting' the iterrator
a_iter = a.__iter__()

# Listing out all the elements with next 
print(a_iter.__next__())
print(a_iter.__next__())
print(a_iter.__next__())
print(a_iter.__next__())
print(a_iter.__next__())

# The bellow call to the function will rase a StopIteration error
try:
    a_iter.__next__()
except StopIteration:
    print(f"No more elements in the iterrator")


# Python has a built in solutions for going over objects which have \_\_iter_\_() and \_\_next\_\_(): the **for** loop. The built in method will stop at StopIteration error but will throw an error and will strop gracefully.

# In[8]:


for item in a:
    print(item)


# To build a custom object which can be iterated we just need to define the \_\_iter_\_() and \_\_next\_\_() methods.

# In[9]:


class Fibonnaci:
    """
    Class that creates the Fibonaci sequence given of elements n, where n > 2
    """
    def __init__(self, n):
        # Initializing an empty list 
        fib_list = []

        # Adding the first two elements to the list
        fib_list.append(1)
        fib_list.append(1)
        if n > 2:
            # Iterating over the list to add the next element
            for i in range(2, n):
                fib_list.append(fib_list[i-1] + fib_list[i-2])
        
        # Saving the list to memory
        self.fib_list = fib_list

        # Saving the max number of elements to memory
        self.n = n

    def __iter__(self):
        """
        Every time this iter method is called, the counter of the current 
        index is reset to 0.
        """
        self.index = 0
        return self
    
    def __next__(self):
        """
        Returning the element in the list if the index is less than the max number of elements
        """
        if self.index < self.n:
            self.index += 1
            return self.fib_list[self.index-1]
        else:
            raise StopIteration        


# In[10]:


# Initiating the Fibonnaci sequence
fib = Fibonnaci(7)

# Printing out the whole sequence 
print(fib.fib_list)

# Using the iterator to print out the sequence
for fib_element in fib:
    print(fib_element)


# # Data structure types 

# ## Mutable and non mutable
# 
# It is popular to put data structures into two buckets: immutable and mutable. 
# 
# An immutable data strucuture is a data structure that, when defined and saved in memory, cannot be changed (**non mutatable**).
# 
# A mutable data structure is a data structure that, when defined and saved in memory, can be changed (can be **mutated** or changed)

# In[11]:


# Defining a mutable data structure - list 
a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

# Defining an immutable data structure - tuple 
b = (1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89)

print(f"Initial list: {a}")
print(f"Initial tuple: {b}")

# Appending an element to the list
a.append(a[-1] + a[-2])

# List after mutation
print(f"List after mutation: {a}")

# Appending an element to the tuple
try:
    b.append(b[-1] + b[-2])
except:
    print("Tuples are immutable (cannot be changed)")


# In general, mutable objects are more flexible but more taxing on the computer memory and will decrease performance if the objects become larger and larger. For example, a big list of **n** elements holds **2n** pointers in memory (bits). 
# 
# In contrast, immutable objects are not flexible but are more memory efficient. 

# ## Linear and non-linear

# In linear data structures, the elements are arranged in sequence one after the other. Since elements are arranged in particular order, they can be iterated upon. Common examples maybe **lists** and **tuples**. 

# In[12]:


# Example of a linear data type - tuple
a = (1, 2, 3, 4, 5)

# Listing out all the items
for item in a:
    print(item)

# Accesing an item by index 
a[2]


# In non-linear data structures, the elements in the data structure are not in any sequence. Instead they are arranged in a hierarchical manner where one element will be connected to one or more elements. Common examples are **binary search trees** {cite}`geeks:binary_tree`.

# In[13]:


# A very simple binary tree implementation for storing numbers
class Tree:
    """
    Class that implements a binary tree; 
    Bigger than root elements go to the "right";
    Smaller than root elements go to the "left"; 
    """
    def __init__(self, number, level=0):
        self.left = None 
        self.right = None
        self.level = level
        self.number = number

    def insert(self, number):
        if number < self.number:
            if self.left is None:
                self.left = Tree(number, self.level + 1)
            else:
                self.left.insert(number)
        else:
            if self.right is None:
                self.right = Tree(number, self.level + 1)
            else: 
                self.right.insert(number)

    def print_tree(self):
        if self.left:
            self.left.print_tree()
        print(f"Depth {self.level}|{'--' * self.level}({self.number})")
        if self.right:
            self.right.print_tree()


# In[14]:


# Creating a list of numbers to create the binary tree from 
a = [5, 10, 1, 2, 36, -30, -2, 7]

# Initiating the binary tree; The first element is the root
tree = Tree(a[0], 0)

# Populating the tree 
for number in a[1:]:
    tree.insert(number)

# Printing out the tree
print(f"List {a} ({len(a)} elements) representation in a binary tree form:")
tree.print_tree()


# The tree organizes its elements into nodes where each node has a reference to the "right" and the "left" nodes. Each node stores information about it's assigned number. This structure cannot be linearly listed. 
# 
# If we wanted to seach for the the number "7" in the above list, we would have to do 8 compare operations (is a[0] equal to 7? is a[1] equal to 7? ...) 
# 
# If we searched for 7 in the tree representation, we would do only 5 compare operations:
# 
# 1) Is 7 == 5? NO 
# 2) Is 7 < 5? NO => Go to right node from root.
# 3) is 7 == 10? NO
# 4) Is 7 < 10? YES => Go to left node.  
# 5) Is 7 == 7? YES => Node with the element found.
# 
# You can imagine that if we would had thousands of numbers, the difference between the comparisons would be even more apparent. 

# # Contributions 
# 
# If you enjoyed the book so far and feel like donating, feel free to do so. The link to do a one time donation is [via Stripe](https://buy.stripe.com/14k17A6lQ8lAat2aEI). 
# 
# Additionaly, if you want me to add another chapter or to expand an existing one, please create an issue on [Github](https://github.com/Eligijus112/api-book).
