from fastapi import FastAPI
from main import LinearR

app = FastAPI()

@app.get('/')                           # get request of '/'
def index():
    return ['Connection Successful']    # return connection successful

@app.get('/lr')                         # gets /lr request
def request_for_linear_regression():
    return LinearR()                    #returns linear regression model