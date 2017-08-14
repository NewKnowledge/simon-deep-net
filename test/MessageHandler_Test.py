import unittest
from kafka.MessageHandler import MessageHandler
from json import JSONDecoder, JSONEncoder

class MessageHandler_Test(unittest.TestCase):

    def test_getFileName(self):
        # Build and encode the JSON input
        fileName = 'success.csv'
        inputMsgDict = {'path': fileName}
        encoder = JSONEncoder()
        inputMsg = encoder.encode(inputMsgDict)

        # Make sure the file name was set correctly
        handler = MessageHandler()
        self.assertEqual(fileName, handler.getFileName(inputMsg))

    def test_addColumnLabels(self):
        # Build and encode the JSON input
        fileName = 'success.csv'
        inputMsgDict = {'path': fileName}
        encoder = JSONEncoder()
        inputMsg = encoder.encode(inputMsgDict)

        # build labels to add to message
        labels = [['label1']]
        columns = ['column1']

        # add the labels, and get the modified JSON message
        handler = MessageHandler()
        decoder = JSONDecoder()
        returnMsg = handler.addColumnLabels(inputMsg, columns, labels)
        returnMsg = decoder.decode(returnMsg)

        # make sure the values were set properly
        self.assertEqual(labels[0][0], returnMsg['labels']['column1'][0])

    def test_addStatus(self):
        # Build and encode the JSON input
        fileName = 'success.csv'
        inputMsgDict = {'path': fileName}
        encoder = JSONEncoder()
        inputMsg = encoder.encode(inputMsgDict)

        status = "Success"
        handler = MessageHandler()
        returnMsg = handler.addStatus(inputMsg, status)

        decoder = JSONDecoder()
        returnMsg = decoder.decode(returnMsg)

        self.assertEqual(returnMsg['status'], status)



if __name__ == '__main__':
    unittest.main()
