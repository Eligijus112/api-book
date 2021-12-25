# Importing the JWT library
import jwt

# The Users model 
from models import User

# Importing the session 
from db import session

# Datetime functionality
import datetime

# Reading the configuration file 
import yaml 
conf = yaml.safe_load(open("config.yml"))

# JWT constants
_SECRET = conf["jwt"]["secret"]
_ALGORITHM = conf["jwt"]["algorithm"]
_EXPIRATION_TIME = conf["jwt"]["expiration_time"] # Minutes until expiration

# Creating the JWT token
def create_token(user_id: int) -> str:
    """
    Method to create a JWT token for a user using internal user_id
    
    Parameters
    ----------
        user_id (int): The user_id of the user to create the token for

    Returns
    -------
        str: The JWT token
    """
    # Creating the claims dictionary
    claims = {
        # Expiration date of the token
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=_EXPIRATION_TIME),
        
        # Issue time of the token
        "iat": datetime.datetime.now(),

        # Subject of the token
        "sub": user_id
    }

    # Creating the token
    return jwt.encode(claims, _SECRET, algorithm=_ALGORITHM)

# Authenticating the JWT token
def authenticate_token(jwt_token: str) -> bool:
    """
    Function that decodes the token and authenticates it. 

    Parameters
    ----------
        jwt_token (str): The JWT token to authenticate

    Returns
    -------
        bool: True if the token is valid, False otherwise
    """
    try:
        # Decoding the token
        claims = jwt.decode(jwt_token, _SECRET, algorithms=[_ALGORITHM])

        # Extracting the user_id from the token
        user_id = claims["sub"]

        # Extracting the expiration date from the token
        expiration_date = claims["exp"]

        # Checking if the token is expired
        if datetime.datetime.fromtimestamp(expiration_date) < datetime.datetime.utcnow():
            return False

        # Checking if the user exists in the database
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            return True
        else:
            return False
    except:
        # If the token is invalid, return False
        return False