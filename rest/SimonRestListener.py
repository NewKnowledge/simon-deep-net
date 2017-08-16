from flask import Flask, request
from json import JSONEncoder
import dill
import pandas
import pickle
import numpy as np
import configparser

class SimonRestListener:
    """ SimonRestListener accepts a pickled numpy array, unpickles
    it, uses its predictive model to generate labels from that array,
    and then encodes it in JSON to be returned to the caller
    """
    def __init__(self, modelName):
       self.model =  dill.load(open(modelName, 'rb'))
       self.encoder = JSONEncoder()

    def runModel(self, data):
        results = self.model.predictDataFrame(data)
        return self.encoder.encode((results))

    def predict(self, request_data):
        array = pickle.loads(request_data)
        array = pandas.DataFrame(array, columns=[str(i) for i in range(array.shape[1])])
        return self.runModel(array)

    def predictFile(self, fileName):
        frame = pandas.read_csv(str(fileName))
        return self.runModel(frame.values)
        
#config = configparser.ConfigParser()
#config.read('rest/config.ini')
#modelName = config['DEFAULT']['modelName']
#        
#listener = SimonRestListener(modelName)

app = Flask(__name__)

@app.route("/", methods=['POST'])
def predict():
    """ Listen for data being POSTed on root. The data should 
    be a string representation of a pickled numpy array
    """
    request.get_data()
    return listener.predict(request.data)


@app.route("/fileName", methods=['POST'])
def predictFile():
    """ Listen for data being POSTed on root. The data should 
    be a string representation of a pickled numpy array
    """
    request.get_data()
    return listener.predictFile(request.data)


# $env:FLASK_APP="rest/SimonRestListener.py"
# flask run