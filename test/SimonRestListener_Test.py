from rest.SimonRestListener import SimonRestListener
import numpy as np
import pandas
import pickle
import sys
import argparse


def main(modelName):
    """ Pass in the name of the model file relative to the root, and this will 
    read a file on white house salaries and try to predict on taht file using
    the provided model
    """
    frame = pandas.read_csv("https://query.data.world/s/9v623xr0pkvanezo0iawba3rk")

    data = pickle.dumps(frame.values)

    listener = SimonRestListener(modelName)

    vals = listener.predict(data)

    print("THE PREDICTED CLASSES ARE:")
    print(vals)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test primitive with infrastructure.')
    parser.add_argument("--modelName", default="localmodel.pkl")
    args = parser.parse_args()
    main(args.modelName)