# ORM functions for the database 
from sqlalchemy.orm import declarative_base

# Model creation 
from sqlalchemy import Column, Integer, String, DateTime, Boolean

# Farnet package for password encription 
from cryptography.fernet import Fernet

# Configuration reading 
import yaml 

# Dates and times
import datetime

# OS traversal 
import os 

# Importing the current session
from database.database import session

# Initiating the Base class
Base = declarative_base()

# Defining the path of the file 
_path = os.path.dirname(os.path.abspath(__file__))

# Reading the secrets 
with open(os.path.join(_path, "config.yml"), 'r') as f:
    secrets = yaml.safe_load(f.read()).get("secrets")
    secret_key = secrets.get("key").encode()
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
    enabled = Column(Boolean)
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
        # Decrypting the password of the current user object in the database
        _fernet = Fernet(secret_key)
        _decrypted_password = _fernet.decrypt(self.password.encode())
        _decrypted_password = _decrypted_password.decode()

        # Adding the salt to the sent password
        _password_sent = f"{password}{secret_salt}"

        # Checking if the password matches
        if _decrypted_password == _password_sent:
            return True
        else:
            return False

def register_user_view(username: str, password: str, email: str):
    """
    Method for registering a user
    """
    # Checking if a certain user already exists 
    _user = session.query(User).filter_by(username=username).first()

    if _user:
        return {"message": "User already exists", "user_id": _user.id}
    else:
        # Creating the user object
        _user = User(username, password, email)

        # Adding the user to the database
        session.add(_user)
        session.commit()

        # Returning the user object
        return _user

def toggle_user_permission_view(user_id: int, permission: bool):
    """
    Method for disabling/enableing a user. 
    """
    # Getting the user object
    _user = session.query(User).filter_by(id=user_id).first()

    if _user:
        # Converting the permission to boolean type 
        try: 
            permission = bool(permission)
        except ValueError as e:
            return {"message": f"Cannot convert permission to boolean. Error: {e}"}

        # Setting the user status to disabled
        _user.enabled = permission
        _user.updated_datetime = datetime.datetime.now()

        # Committing the changes to the database
        session.commit()

        # Returning the user object
        return _user
    else:
        return None

def remove_user_view(user_id: int):
    """
    Removes the user from the database
    """
    # Getting the user object
    _user = session.query(User).filter_by(id=user_id).first()

    if _user:
        # Deleting the user object
        session.delete(_user)
        session.commit()

        # Returning the user object
        return _user
    else:
        return None
