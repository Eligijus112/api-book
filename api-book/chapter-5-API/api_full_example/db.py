# ORM functions for the database 
from sqlalchemy.orm import sessionmaker, declarative_base

# Creating the engine for the database
from sqlalchemy import create_engine

# Model creation 
from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql.schema import ForeignKey

# Data wrangling
import pandas as pd

# Dates and times
import datetime

# Connecting to the PSQL database
init_engine = create_engine('postgresql://user:password@localhost:5431/postgres')

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
engine = create_engine(f'postgresql://user:password@localhost:5431/{db_name}')

# Initiating the Base class
Base = declarative_base()

# Defining the models - Request and Response
class Request(Base):
    # Table name in database
    __tablename__ = 'requests'
    
    # If any changes are made to the columns, allow the database to know about it
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    number = Column(Float)
    n = Column(Float)
    request_datetime = Column(DateTime)

    def __init__(self, number, n):
        self.number = number
        self.n = n
        self.request_datetime = datetime.datetime.now()

class Response(Base):
    # Table name in database
    __tablename__ = 'responses'
    
    # If any changes are made to the columns, allow the database to know about it
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    # Each response has to have an associated request. This association is defined by the foreign key.
    # Hence, every response will have an associated request ID column value.
    request_id = Column(Integer, ForeignKey('requests.id'))
    root = Column(Float)
    response_code = Column(Integer)
    response_datetime = Column(DateTime)

    def __init__(self, request_id, root, response_code):
        self.request_id = request_id
        self.root = root
        self.response_code = response_code
        self.response_datetime = datetime.datetime.now()

# Creating the models in the database if they do not exist
tables = pd.read_sql(f"SELECT tablename FROM pg_catalog.pg_tables;", engine)["tablename"].values.tolist()
if 'requests' not in tables or 'responses' not in tables:
    print('Tables do not exist; Creating them')
    Base.metadata.create_all(engine)

# Creating the session
Session = sessionmaker(bind=engine)
session = Session()