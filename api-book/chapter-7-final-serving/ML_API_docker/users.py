# Importing the Users model 
from Users import User

# Datewrangling 
import datetime

# Importing the current session
from database import session

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