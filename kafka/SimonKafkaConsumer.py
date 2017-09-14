from kafka.MessageHandler import MessageHandler
from azure_utils.client import get_adl_client

import sys
import dill
import random
import pandas
import traceback
from typing import List

from kafka import KafkaConsumer, KafkaProducer

class SimonKafkaConsumer:
    def __init__(self, modelName, consumeTopic, publishTopic, serverName):
        # Load this stuff form a config or input parameters:
        self.servername = [serverName]
        self.consumeTopic = consumeTopic
        self.publishTopic = publishTopic

        self.model = dill.load(open(modelName, 'rb'))

        self.consumer = KafkaConsumer(self.consumeTopic, bootstrap_servers=self.servername)
        self.producer = KafkaProducer(bootstrap_servers=self.servername)
        self.messageHandler = MessageHandler()

    # Take an individual message from Kafka, predict on that message,
    # return a message containing the appropriate metadata
    def processMessage(self, msg: str) -> str:
        print("Reading file")
        df = self.getDataFrame(msg)
        print("Predicting file")
        columns, labels = self.model.predictDataFrame(df)
        samples = [random.sample(list(df.ix[:,col].values), 5) for col in columns]
        msg = self.messageHandler.addSamples(msg, columns, samples)
        return self.messageHandler.addColumnLabels(msg, columns, labels)

    # Extract the file path information from the json message and then
    # read the file out of hdfs into a data frame
    def getDataFrame(self,msg: str) -> pandas.DataFrame:
        fileName = str(self.messageHandler.getFileName(msg))
        if fileName.startswith("http") or fileName.startswith("ftp") or fileName.startswith("s3"):
            try:
                df = pandas.read_csv(fileName,dtype='str')
            except:
                df = pandas.DataFrame()
                print("An error occurred reading " + fileName)
                traceback.print_exc()
        else:
            # For now, assume that we're reading from adl, not HDFS
            adl = get_adl_client('nktraining')
            try:
                with adl.open(fileName,blocksize=2**20) as f:   
                    df = pandas.read_csv(f,dtype='str')
            except:
                df = pandas.DataFrame()
                print("An error occurred reading " + fileName)
                traceback.print_exc()
        return df


    # Consume messages from the kafka consumer topic, process the message,
    # and then post to the kafka publish topic
    def listen(self):
        print("Listening...")
        for msg in self.consumer:
            try:
                r_msg = self.processMessage(msg.value.decode('utf-8'))
                r_msg = self.messageHandler.addStatus(r_msg, "Success")
            except:
                print("Could not process file")
                traceback.print_exc()
                r_msg = self.messageHandler.addStatus(msg.value.decode('utf-8'),"Failure")
            self.producer.send(self.publishTopic,value=r_msg.encode('utf-8'))
            print("Delivered message")
