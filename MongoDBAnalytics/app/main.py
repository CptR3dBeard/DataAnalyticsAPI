#Author: CptR3dBeard
#Date Project Started: 25/10/2021
#Used libraries
import pymongo
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fastapi.responses import FileResponse
from sklearn import linear_model
from sklearn.linear_model import LinearRegression

"""Setting our variables"""   
lr = LinearRegression()             # defining basic Linear Regression
rig = linear_model.Ridge(alpha=.5)  # defining ridge regression model with alpha of 0.5
client = pymongo.MongoClient(f'mongodb://localhost:27017') # establish our database connection
db = client['stocks']                                      # Use this database
col = db['TestData']                                           # Search for this collection within database

def LinearR():
    """This function LinearR queries the MongoDB for the collection.
    In this example; the collection contains 2019/2020 12month Stock prices of MSFT,
    these entries will then undergo linear regression."""
    x =col.find({}, {'_id': 0})                  # variable containing pymongo find command aswell as removing the _id 
    for i in x:                                  # iterating over x variables results
        df = pd.DataFrame(x)                     # this uses pandas on our query to turn all the data/columns into a dataframe
        df.reset_index(drop=True, inplace=True)  # dropping index and modifying data inplace ( will not move)
        X = df.iloc[:, :-1].values               # use location based indexing on 2 columns to determine x axis
        y= df.iloc[:, 1].values                  # use location based indexing on 2 columns to determine y axis
        lr.fit(X, y)                             # we are now performing linear regression on the data supplied.
        return np.ndarray.tolist(lr.predict(X))  # Converting the X value of linear prediction to a list returning to FastAPI
def Ridge_Regression():
    """This function performs Ridge Regression fomr the MongoDB collection.
    Example; our test data contains microsft stock price over 12months from 2019-2020
    this data undergoes ridge regression."""
    x =col.find({}, {'_id': 0})
    for i in x:
        df = pd.DataFrame(x)                     # here we define out dataframe as a variable DF
        df.reset_index(drop=True, inplace=True)  # reseting & dropping the index of Panda datafrom so Sklearn can process
        X = df.iloc[:, :-1].values               # use location based indexing on 2 columns to determine x axis
        y= df.iloc[:, 1].values                  # use location based indexing on 2 columns to determine y axis
        rig.fit(X, y)
        return np.ndarray.tolist(rig.predict(X)) # convert numpy array into a list for ridge prediction

def insert_new_dataset(file_name):
    """This function allows the user to insert a complete new dataset into a MongoDB collection
    The data can be anything and it will upload to the localhost database for MongoDB"""
    df = pd.read_csv(file_name)                  # Reading the uploaded file contents as CSV
    data = df.to_dict(orient="records")          # Converting the dataframe to a dictionary
    col.insert(data)                             # Executing the collection insert function using the converted dataframe
    return{'Test':'Successful'}                  # Return successful test to API