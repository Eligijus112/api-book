# ORM functions for the database 
from sqlalchemy.orm import declarative_base

# Model creation 
from sqlalchemy import Column, Integer, DateTime, JSON, ForeignKey

# Dates and times
import datetime

# Users
from Users import User

# Initiating the Base class
Base = declarative_base()


class MLRequests(Base):
    # Table name in database
    __tablename__ = 'requests'
    
    # If any changes are made to the columns, allow the database to know about it
    __table_args__ = {'extend_existing': True} 

    # Database columns
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    input = Column(JSON)
    created_datetime = Column(DateTime)
    updated_datetime = Column(DateTime)

    def __init__(
        self,
        user_id: int, 
        input: JSON
        ):
        # Infering the time of creation 
        _cur_time = datetime.datetime.now()

        # Variables for the object
        self.user_id = user_id
        self.input = input
        self.created_datetime = _cur_time
        self.updated_datetime = _cur_time


class MLResponses(Base):
    # Table name in database
    __tablename__ = 'responses'
    
    # If any changes are made to the columns, allow the database to know about it
    __table_args__ = {'extend_existing': True} 

    # Database columns
    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey('requests.id'))
    output = Column(JSON)
    created_datetime = Column(DateTime)
    updated_datetime = Column(DateTime)

    def __init__(
        self,
        request_id: int, 
        output: JSON
        ):
        # Infering the time of creation 
        _cur_time = datetime.datetime.now()

        # Variables for the object
        self.request_id = request_id
        self.output = output
        self.created_datetime = _cur_time
        self.updated_datetime = _cur_time
