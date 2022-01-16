#!/usr/bin/env python
# coding: utf-8

# # Migrations 
# 
# A `schema migration` (or populary termed just `migration`) is a process of changing the database schema in a trackable and reversible way. To put it simpler, every time we make a change to a table or tables in a database, we make a `migration`. Under the hood, each migration is just an SQL script that is run against the database. What is very important, howerer, is that every migration needs to know what has happened before it. If we lose history of migrations, we will run into huge productions problems and will probably need to start from scratch.  
# 
# # Migrations in Python - Alembic
# 
# Python has a very simple yet powerfull framework for managing database migrations - `Alembic`. As the authors put it: 
# 
# *"Alembic is a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python"*. One can read on the [Alembic website](https://alembic.sqlalchemy.org/en/latest/) for more information.
# 
# To initialize the root folder for alembic, type the command:
# 
# ```
# alembic init alembic-migrations
# ```
# 
# This will create a folder `alembic-migrations` in the current directory along with a `alembic.ini` file:
# 
# ```
# ├── alembic.ini
# ├── alembic-migrations/
# │   ├── env.py
# │   ├── README
# │   ├── script.py.mako
# │   └── versions/
# ```
# 
# The `alembic.ini` file contains the configuration for the database connection and general alembic behaviour.
# 
# The `env.py` file holds the environmental variables for the database connection and where the objects from other Python scripts get impoerted.
#  
# The `script.py.mako` file is the template for the migration scripts. 
# 
# The `versions` folder is where the migration scripts are stored.
# 
# For now, let us imagine that we have a running database in a container on localhost port 5429. The database name is postgres. 
# 
# # Alembic in action 
# 
# ## alembic.ini file 
# 
# The alembic.ini file holds the URI to connect to a database in question. It is a best practise to use on alembic.ini file per database. By default it is populated with some variables. The most important one is `sqlalchemy.url` one. By default, the value is:
# 
# ```
# sqlalchemy.url = driver://user:pass@localhost/dbname
# ```
# 
# We will change it to: 
# 
# ```
# sqlalchemy.url = postgresql://user:password@localhost:5429/postgres
# ```
# 
# Now every time we run a command `alembic ...` it will try to connect via the URL we specified and make changes there. 
# 
# ## models.py file 
# 
# This is a user created file holding all the database models (tables). We define the tables with the already seen SQLAlchemy declarative base class.

# In[1]:


get_ipython().system('cat alembic-migrations/models.py')


# The initial table will have the following columns: `username`, `password`, `create_datetime`. Now we need to somehow tell alembic about this table.
# 
# ## env.py file 
# 
# We will be importing all of our created database tables into this file. 
# 
# On the top of the file, add the following line:
# 
# ```
# from models import Base
# ```
# 
# Alembic will infere (when it is invoked) information about all the classes that extend the `Base` class and will now about all the wanted collumns and relationships.
# 
# The second line that needs to be changed is to change: 
# 
# ```
# target_metadata = None
# ```
# 
# to 
# 
# ```
# target_metadata = Base.metadata
# ```
# 
# We tell alembic which tables we want to track. Every table that is extended from the `Base` class will be tracked. 
# 
# ## Initial migration 
# 
# Have done the above steps, we are ready for our very first migration! As of right now, the directory /versions is empty because we have not made any migrations. 
# 
# To do a migration, we run the command: 
# 
# ```
# alembic revision --autogenerate -m "Initial migration"
# ```
# 
# The --autogenerate flag tells alembic to generate the SQL code automatically for us based on the code in the `models.py` script. 
# 
# The -m flag tells alembic what the migration is called. The info in the terminal should look like: 
# 
# ```
# INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
# INFO  [alembic.runtime.migration] Will assume transactional DDL.
# INFO  [alembic.autogenerate.compare] Detected added table 'users'
#   Generating /home/eligijus/api-book/api-book/chapter-6-production-tools/alembic-migrations/alembic-migrations/versions/8b3bc20f068e_initial_migration.py ...  done
# ```
# 
# Now the versions/ directory is not empty and contains the following file: 

# In[2]:


get_ipython().system('cat alembic-migrations/alembic-migrations/versions/8b3bc20f068e_initial_migration.py')


# Each revision has a unique id. The id is generated by alembic and is used to identify the migration. The id of the initial migration is `8b3bc20f068e`. 
# 
# The upgrade() method will be called when we will run the migration. 
# 
# The downgrade() method will be called when we want to revert the migration. 
# 
# ## Migrating to database 
# 
# Up untill this point, everything was happening locally. To actually run and apply the migration to the database, we run the command: 
# 
# ```
# alembic upgrade head
# ```
# 
# The *upgrade* command will invoke the `upgrade()` method defined in the Python file. 
# 
# The *head* means to upgrade the latest version that is currently in the database.
# 
# The output in the terminal should look like: 
# 
# ```
# INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
# INFO  [alembic.runtime.migration] Will assume transactional DDL.
# INFO  [alembic.runtime.migration] Running upgrade  -> 8b3bc20f068e, Initial migration
# ```
# 
# Now in the database, along with the table `users`, we have another table called `alembic version` which just indicates what is the current version of the database (in our case its `8b3bc20f068e`).
# 
# ## Applying changes 
# 
# Lets say we want to add a collumn called email to the database. The User class in the `models.py` file will be modified to include the new collumn: 

# ```
# class User(Base):
#     # Table name in database
#     __tablename__ = 'users'
#     
#     # If any changes are made to the columns, allow the database to know about it
#     __table_args__ = {'extend_existing': True} 
# 
#     id = Column(Integer, primary_key=True)
#     username = Column(String)
#     password = Column(String)
#     email = Column(String)
#     create_datetime = Column(DateTime)
#     
# 
#     def __init__(self, username: str, password: str, email: str):
#         self.username = username 
#         self.password = password
#         self.email = email
#         self.create_datetime = datetime.datetime.now()
# ```
# 
# To create the local migration files, we once again type the command: 
# 
# ```
# alembic revision --autogenerate -m "Added user email"
# ```
# 
# The output should look like: 
# 
# ```
# INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
# INFO  [alembic.runtime.migration] Will assume transactional DDL.
# INFO  [alembic.ddl.postgresql] Detected sequence named 'users_id_seq' as owned by integer column 'users(id)', assuming SERIAL and omitting
# INFO  [alembic.autogenerate.compare] Detected added column 'users.email'
#   Generating /home/eligijus/api-book/api-book/chapter-6-production-tools/alembic-migrations/alembic-migrations/versions/cd1911ec4399_added_user_email.py ...  done
# ```
# 
# A new revision is created in the versions/ directory. The id of the new revision is `cd1911ec4399`. The contents of the Python file is:

# In[3]:


get_ipython().system('cat alembic-migrations/alembic-migrations/versions/cd1911ec4399_added_user_email.py')


# To apply these changes to the database we run the command:
# 
# ```
# alembic upgrade head
# ```

# # Alembic workflow summary
# 
# In summary, the changing of the database schema most of the time falls into this pattern: 
# 
# ![alembic-flow](media/alembic-flow.png)

# Any time a user modifies any table code in the models.py file (or anywhere else) the same flow is followed:
# 
# * Alembic is used to generate the python script in the **versions/** directory.
# * The user then initiates the migration to the database which sqlalchemy applies.
# * In the database, the latest version of the migrations is saved in the table called **alembic_version**.  
# 
# When managing a database with Alembic we can always review the history of migrations, rollback to previous versions and very easily apply changes to the database.