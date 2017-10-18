from json import JSONDecoder, JSONEncoder
from typing import List

class MessageHandler:
    def __init__(self):
        self.decoder = JSONDecoder()
        self.encoder = JSONEncoder()

    def getFileName(self, msg: str) -> str:
        msgObj = self.decoder.decode(msg)
        return msgObj['path']

    def addColumnLabels(self, msg: str, c: List[str], l: List[str]) -> str:
        return self.addDict(msg, 'labels', c, l)
        
    def addColumnLabelProbabilities(self, msg: str, c: List[str], p: List[str]) -> str:
        return self.addDict(msg, 'label_probabilities', c, p)

    def addSamples(self, msg: str, c: List[str], s: List[str]) -> str:
        return self.addDict(msg, 'samples', c, s)

    def addDict(self, msg: str, header: str, keys: List[str], values: List[str]) -> str:
        labelDict = dict()
        for cl in zip(keys,values):
            labelDict[str(cl[0])] = cl[1]

        msgObj = self.decoder.decode(msg)
        msgObj[header] = labelDict

        return self.encoder.encode(msgObj)

    def addStatus(self, msg: str, status: str) -> str:
        msgObj = self.decoder.decode(msg)

        msgObj['status'] = status

        return self.encoder.encode(msgObj)

    def printMessage(self, msg: str):
        msgObj = self.decoder.decode(msg)
        for key in msgObj['labels'].keys():
            print(key + ": " + msgObj['labels'][key])
