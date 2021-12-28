# ORM functions for the database 
from sqlalchemy.orm import declarative_base

# Model creation 
from sqlalchemy import Column, Integer, String, DateTime

# Farnet package for password encription 
from cryptography.fernet import Fernet

# Configuration reading 
import yaml 

# Dates and times
import datetime

# Initiating the Base class
Base = declarative_base()

# Reading the secrets 
with open('conf.yml', 'r') as f:
    secrets = yaml.load(f.read()).get("secrets")
    secret_key = secrets.get("key")
    secret_salt = secrets.get("salt")


class User(Base):
    # Table name in database
    __tablename__ = 'users'
    
    # If any changes are made to the columns, allow the database to know about it
    __table_args__ = {'extend_existing': True} 

    # Database columns
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    enabled = True
    created_datetime = Column(DateTime)
    updated_datetime = Column(DateTime)

    @staticmethod
    def encrypt_string(string: str) -> str:
        """
        Method for encrypting a given string
        """
        # Initiating the encriptor 
        _fernet = Fernet(secret_key)

        # Encrupting the string with the added salt 
        _encrypted_password = _fernet.encrypt(f"{string}{secret_salt}".encode())
        
        # Returning the encrypted string
        return _encrypted_password.decode()

    def __init__(
        self,
        username: str, 
        password: str,
        email: str,
        enabled: bool = True,
        ):
        # Infering the time of creation 
        _cur_time = datetime.datetime.now()

        # Encripting the password at the time of creation
        # This will prevent the password from being stored in plain text and be extracted even by developers
        _encrypted_password = self.encrypt_string(password)

        # Variables for the object
        self.username = username 
        self.password = _encrypted_password
        self.email = email 
        self.enabled = enabled
        self.created_datetime = _cur_time
        self.updated_datetime = _cur_time

    def __str__(self):
        """
        Method for developers to see the object in a readable format 
        """
        return f"User(username='{self.username}', password='{self.password}', email='{self.email}')"

    def check_password_match(self, password: str) -> bool:
        """
        Method to check if the given password matches up with the one stored in object
        """
        # Decrypting the password 
        _fernet = Fernet(secret_key)
        _decrypted_password = _fernet.decrypt(self.password.encode())
        _decrypted_password = _decrypted_password.decode()

        # Checking if the password matches
        if _decrypted_password == self.encrypt_string(password):
            return True
        else:
            return False
