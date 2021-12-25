# Importing the fastAPI library
from fastapi import FastAPI

# Creating an instance of the FastAPI class
app = FastAPI()

# Creating an endpoint with the GET method
@app.get("/root")
def root_of_number(number: float, n: float):
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
    return {"root": number ** n} 