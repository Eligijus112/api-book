# ORM functions for the database 
from sqlalchemy.orm import declarative_base

# Model creation 
from sqlalchemy import Column, Integer, String, DateTime

# Dates and times
import datetime

# Initiating the Base class
Base = declarative_base()

# Defining the models - Request and Response
class User(Base):
    # Table name in database
    __tablename__ = 'users'
    
    # If any changes are made to the columns, allow the database to know about it
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    create_datetime = Column(DateTime)
    

    def __init__(self, username: str, password: str, email: str):
        self.username = username 
        self.password = password
        self.email = email
        self.create_datetime = datetime.datetime.now()