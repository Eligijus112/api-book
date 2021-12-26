# FastAPI 
from fastapi import FastAPI, Request, Response, status

# Importing the connection and the models 
from db import session
from models import User 

# JWT token creation 
from jwt_tokens import create_token, authenticate_token

# Creating the FastAPI app
app = FastAPI()

# Creating the POST endpoint that registers a new user 
@app.post("/users/register")
async def create_user(request: Request, response: Response):
    try:
        # Extracting the payload 
        input_dict = await request.json()

        # Extracting the username and password from the request
        username = input_dict.get('username')
        password = input_dict.get('password')

        # Checking if the user already exists
        user = session.query(User).filter(User.username == username).first()
        if user:
            return {"message": "User already exists", "user_id": user.id}
        else:
            # Creating the username object 
            user = User(username=username, password=password)

            # Adding the user to the database
            session.add(user)

            # Committing the changes to the database
            session.commit()

            # Returning the user object
            response.status_code = status.HTTP_201_CREATED
            return {"message": "User created successfully", "user_id": user.id}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return f"Cannot create user. Error: {e}"

# Creating the token 
@app.post("/token")
async def get_token(request: Request, response: Response):
    try:
        # Extracting the payload 
        input_dict = await request.json()

        # Extracting the username and password from the request
        username = input_dict.get('username')
        password = input_dict.get('password')

        # Checking if the user exists
        user = session.query(User).filter(User.username == username).first()
        if user:
            # Checking if the password is correct
            if user.password == password:
                # Creating the token
                token = create_token(user.id)

                # Encoding the status code 
                response.status_code = status.HTTP_200_OK
                return {"message": "Token created successfully", "token": token}
            else:
                response.status_code = status.HTTP_401_UNAUTHORIZED
                return {"message": "Password is incorrect"}, 401
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {"message": "User does not exist"}, 401
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return f"Cannot create token. Error: {e}", 500

# The main API 
@app.get("/root")
def root_of_number(number: float, n: float, request: Request, response: Response):
    """
    The function returns the n-th root of the number.
    Parameters
    ----------
    number : float
        The number to find the n-th root of.
    n : float
        The n-th root to find.
    Returns
    -------
    float
        The n-th root of the number.
    """
    # Extracting the JWT token from the request
    jwt_token = request.headers.get("Authorization")

    # Authenticating the token
    if authenticate_token(jwt_token):
        response.status_code = status.HTTP_200_OK
        return {"root": number ** n} 
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Token is not valid"}