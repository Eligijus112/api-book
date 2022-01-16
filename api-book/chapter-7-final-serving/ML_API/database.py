# ORM functions for the database 
from sqlalchemy.orm import sessionmaker

# Creating the engine for the database
from sqlalchemy import create_engine

# Directory functions 
import os 

# Configuration reading 
import yaml 

# Configuration reading 
# Defining the path of the file 
_path = os.path.dirname(os.path.abspath(__file__))

# Reading the secrets 
with open(os.path.join(_path, "config.yml"), 'r') as f:
    connection = yaml.safe_load(f.read()).get("connection")
    user = connection.get("username")
    password = connection.get("password")
    port = connection.get("port")
    host = connection.get("host")
    database = connection.get("database")

# Connecting to the PSQL database
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

# Creating the session
Session = sessionmaker(bind=engine)
session = Session()