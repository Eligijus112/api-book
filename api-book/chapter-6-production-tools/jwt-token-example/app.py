# FastAPI 
from fastapi import FastAPI, Request

# Importing the connection and the models 
from db import session, engine 
from models import User 

# Creating the FastAPI app
app = FastAPI()

# Creating the POST endpoint that registers a new user 
@app.post("/users/register")
async def create_user(request: Request):
    try:
        # Extracting the username and password from the request
        username = request.json().get('username')
        password = request.json().get('password')

        # Checking if the user already exists
        user = session.query(User).filter(User.username == username).first()
        if user:
            return {"message": "User already exists"}
        else:
            # Creating the username object 
            user = User(username=username, password=password)

            # Adding the user to the database
            session.add(user)

            # Committing the changes to the database
            session.commit()

            # Returning the user object
            return user, 201
    except Exception as e:
        return f"Cannot create user. Error: {e}", 400