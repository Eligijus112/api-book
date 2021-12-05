# Importing the fastAPI library
from fastapi import FastAPI

# Creating an instance of the FastAPI class
app = FastAPI()

# Creating an endpoint with the GET method
@app.get("/root_of_number")
def root_of_number(number: float):
    """
    This function returns the square root of a number
    """
    return {"root": number ** 0.5} 