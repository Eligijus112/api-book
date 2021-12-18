# Importing the fastAPI library
from fastapi import FastAPI

# Importing the session, requests and responses models
from db import session, Request, Response

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
    # Creating a new request object
    request = Request(number, n)

    # Adding the request to the session
    session.add(request)

    # Commiting to database
    session.commit()

    # Calculating the root
    try:
        root = number ** n

        # Creating the response object
        response = Response(request.id, root, 200)

        # Adding the response to the session
        session.add(response)

        # Commiting to database
        session.commit()

        # Returning the response to the user 
        return {"root": number ** n} 
    except Exception as e:
        # Creating the response object
        response = Response(request.id, None, 500)

        # Adding the response to the session
        session.add(response)

        # Commiting to database
        session.commit()

        # Returning the response to the user 
        return {"error": str(e)}