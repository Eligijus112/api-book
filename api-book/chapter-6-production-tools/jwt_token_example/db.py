# ORM functions for the database 
from sqlalchemy.orm import sessionmaker

# Creating the engine for the database
from sqlalchemy import create_engine

# Data wrangling
import pandas as pd

# Importing the custom models 
from models import Base

# Connecting to the PSQL database
init_engine = create_engine('postgresql://user:password@localhost:5430/postgres')

# Ensuring that the database ROOT_DB is created in the PSQL server 
conn = init_engine.connect()

# When initiated, the connection object is in a state of an active transation. We need to commit it in order to make the changes permanent.
conn.execute("commit")

# Giving the database a name 
db_name = 'root_db'

# Getting all the database names 
databases = pd.read_sql("SELECT datname FROM pg_database;", init_engine)["datname"].values.tolist()

if db_name in databases:
    print(f'Database {db_name} already exists')
else:
    print('Database does not exist; Creating it')
    # Creating the database
    conn.execute(f"CREATE DATABASE {db_name}")
    conn.execute("commit")
conn.close()

# Creating the engine to the main database
engine = create_engine(f'postgresql://user:password@localhost:5430/{db_name}')

# Creating the models in the database if they do not exist
tables = pd.read_sql(f"SELECT tablename FROM pg_catalog.pg_tables;", engine)["tablename"].values.tolist()
if "users" not in tables:
    print('Tables do not exist; Creating them')
    Base.metadata.create_all(engine)

# Creating the session
Session = sessionmaker(bind=engine)
session = Session()