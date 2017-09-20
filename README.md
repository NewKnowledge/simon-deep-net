# Simon 
This repo is built to be the base code for all New Knowledge TA1 primitives. Our Data Cleaning Operations (DCO) primitives will all be built, trained, and tested in separate repos and then pickled to be used by this codebase. All code is written in Python 3.5 and must be run in 3.5 or greater. 

#### There are a few requirements for models for them to be used by the Simon code:
1. They must be pickled with the dill library. Note that I believe that the reasons I went with dill over pickle are no longer valid and we can probably use base pickle instead. 
1. In order to run the model, it must be sufficient to un-pickle the model file with dill and then call "act" with a numpy array as input parameter.
1. The model must only use libraries that are included in the Dockerfile at the same level of this README. If the docker file does not contain a library you need, you can add it, but please test that change before delivering it to a third party.

### Packages
There are two independent libraries in this package, "rest" for responding to requests over a REST api, and "kafka" for using a pair of kafka topics to communicate with caller. The REST api is intended to be hosted in a docker container and used with a thin client that can be found at https://github.com/NewKnowledge/simon-thin-client. 

#### rest
This package consists of a single python file SimonRestListener.py which uses flask to set up REST api on port 5000. This api listens for POST requests where the body of the message is a pickled numpy array, and will respond with a json object representing the output of the model. This code can be run with the following two commands, run at the root of the project:
``` bash
FLASK_APP=rest/SimonRestListener.py
flask run
```

#### kafka
This package consists of two python files, SimonKafkaConsumer.py and MessageHandler.py. MessageHandler is simply a helpful utility for managing json messages used by kafka. SimonKafkaConsumer will set up a consumer on a specified topic and server, and then load and process a file based on messages receive from kafka. The results will be published to a different topic to be consumed by the caller. This code can simply be run with:
``` bash
python -m kafka.SimonKafkaConsumer
```

#### tests
There are two tests inluded with this package, MessageHandler_Test and SimonRestListener_Test. The SimonRestListener_Test is a simple module designed to test the functionality of a pickled model added to this package. To test your model with this code, run the following command, substituting the name of your model file for "model.pkl" (or name your model "localmodel.pkl" and omit the --modelName option completely):
``` bash
python -m test.SimonRestListener_Test --modelName model.pkl
```
In order to run the MessageHandler_Test, which is only used for the kafka version of the api, run the following command (there presently appears to be a bug in this test...):
```bash
python -m unittest -v ./test/MessageHandler_Test.py
```
