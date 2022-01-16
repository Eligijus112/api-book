# FastAPI 
from fastapi import FastAPI, status, Response, Request

# Importing the current session from DB 
from database.database import session

# Machine Learning functionalities
from database.ML import MLRequests, MLResponses, load_ml_model, predict

# User functionalities
from database.Users import register_user_view, remove_user_view, toggle_user_permission_view

# Authentification functionalities
from database.jwt_tokens import authenticate_token_view, authenticate_user_view, create_token_view

# Input and output wrangling 
import json

# Array wrangling
import numpy as np

# Creating the application object 
app = FastAPI()

# Loading the machine learning objects to memory 
ml_model, type_dict, ml_feature_list = load_ml_model()

# Endpoint for ML model prediction 
@app.post('/predict')
async def predict_ml(request: Request):
    """
    Endpoint for the ML model prediction
    """
    # Extracting the token from the header
    token = request.headers.get('Authorization')
    if token:
        # Authenticating the token
        user = authenticate_token_view(token)
        if user:
            # Extracting the features from the request
            input_dict = await request.json()
            
            # Creating the request object in database
            ml_request = MLRequests(user_id=user.id, input=json.dumps(input_dict))
            session.add(ml_request)
            session.commit()

            # Getting the prediction 
            prediction = predict(ml_model, type_dict, input_dict)

            if prediction is not None:
                # Creating the response dictionary 
                response_dict = {
                    'yhat_prob': str(prediction[1]),
                    'yhat': str(np.sum(prediction[1] > 0.5))
                }

                # Creating the response object in database
                ml_response = MLResponses(request_id=ml_request.id, output=json.dumps(response_dict))
                session.add(ml_response)
                session.commit()

                # Returning the prediction
                return Response(status_code=status.HTTP_200_OK, content=json.dumps(response_dict))
            else:
                # Returning the message with the bad request status code
                return Response(status_code=status.HTTP_400_BAD_REQUEST, content=json.dumps({'message': 'Bad request'}))
        else:
            # Returning a 401 Unauthorized error
            return Response(status_code=status.HTTP_401_UNAUTHORIZED, content=json.dumps({'error': 'Unauthorized'}))

# Adding the endpoint for user registration 
@app.post("/register-user")
async def register_user(request: Request, response: Response):
    # Extracting the payload 
    input_dict = await request.json()

    # Extracting the username and password from the request
    username = input_dict.get('username')
    password = input_dict.get('password')
    email = input_dict.get('email')

    _user = register_user_view(username, password, email)
    if isinstance(_user, dict):
        if _user.get('message') == "User already exists":
            response.status_code = status.HTTP_409_CONFLICT
            return {"message": "User already exists", "user_id": _user.get("user_id")}
    elif _user:
        # Returning the user object with a response code of 201
        response.status_code = status.HTTP_201_CREATED
        return {"message": "User created successfully", "user_id": _user.id}
    else:
        # Returning a response code of 500
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Cannot create user"}

# Toggling user permissions
@app.put("/toggle-user-permission/{user_id}/{permission}")
async def toggle_user_permission(response: Response, user_id: int, permission: bool):
    _user = toggle_user_permission_view(user_id, permission)
    if _user:
        response.status_code = status.HTTP_200_OK
        return {"message": "User permission updated successfully", "user_id": _user.id}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "User not found"}

# Adding the endpoint for user deletion 
@app.delete("/remove-user/{user_id}")
async def remove_user(response: Response, user_id: int):
    _user = remove_user_view(user_id)
    if _user:
        response.status_code = status.HTTP_200_OK
        return {"message": "User deleted successfully"}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "User not found"}

# Creating the token 
@app.post("/token")
async def get_token(request: Request, response: Response):
    # Extracting the payload 
    input_dict = await request.json()

    # Extracting the username and password from the request
    username = input_dict.get('username')
    password = input_dict.get('password')

    # Authenticating if the user exists and the password is correct
    user = authenticate_user_view(username, password)
    if user:
        # Creating the token
        token = create_token_view(user.id)

        # Returning the token
        response.status_code = status.HTTP_200_OK
        return {"token": token}
    else: 
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Invalid credentials"}

# Endpoint to see if the token is valid
@app.get("/token_status/{token}")
async def verify_token(token: str, response: Response):
    # Authenticating if the token is valid
    if authenticate_token_view(token):
        response.status_code = status.HTTP_200_OK
        return {"message": "Token is valid"}
    else: 
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Invalid token"}

