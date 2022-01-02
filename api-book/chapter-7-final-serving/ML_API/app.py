# FastAPI 
from fastapi import FastAPI, status, Response, Request

# Views 
from users import register_user_view, remove_user_view, toggle_user_permission_view
from jwt_tokens import authenticate_token_view, authenticate_user_view, create_token_view

# Creating the application object 
app = FastAPI()

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

