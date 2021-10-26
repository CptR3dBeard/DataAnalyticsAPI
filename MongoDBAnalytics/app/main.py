#Author: CptR3dBeard
#Date Project Started: 25/10/2021
#Used libraries
from fastapi.encoders import jsonable_encoder
import pymongo
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

"""Setting our variables"""   
lr = LinearRegression()
client = pymongo.MongoClient(f'mongodb://localhost:27017') # establish our database connection
db = client['stocks']             # Use this database
col = db['data']                  # Search for this collection within database
pred = db['predictions']
    

def LinearR():
    """This function LinearR queries the MongoDB for the collection.
    In this example; the collection contains 2019/2020 12month Stock prices of MSFT,
    these entries will then undergo linear regression."""
    x =col.find({}, {'_id': 0})   # variable containing pymongo find command aswell as removing the _id 
    for i in x:                   # iterating over x variables results
        df = pd.DataFrame(x)      # this uses pandas on our query to turn all the data/columns into a dataframe
        df.reset_index(drop=True, inplace=True)  # dropping index and modifying data inplace ( will not move)
        X = df.iloc[:, :-1].values  # use location based indexing on 2 columns to determine x axis
        y= df.iloc[:, 1].values     # use location based indexing on 2 columns to determine y axis
        lr.fit(X, y)                # we are now performing linear regression on the data supplied.
        return np.ndarray.tolist(lr.predict(X)) # Converting the X value of linear prediction to a list returning to FastAPI