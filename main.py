from lib.SimonListener import SimonListener
import argparse


def main(modelName, consumeTopic, publishTopic, serverName):
	listener = SimonListener(modelName=modelName, consumeTopic=consumeTopic,
		publishTopic=publishTopic, serverName=serverName)
	listener.listen()

parser = argparse.ArgumentParser(description='Set up primitive listener.')
parser.add_argument('--publishTopic', default="column_datatype_classifications")
parser.add_argument('--consumeTopic', default="classify_column_datatypes")
parser.add_argument('--modelName', default="localmodel.pkl")
parser.add_argument('--serverName', default="nk-davedevkafka.eastus.cloudapp.azure.com")

args = parser.parse_args()
if __name__ == '__main__':
	main(modelName=args.modelName, consumeTopic=args.consumeTopic,
		publishTopic=args.publishTopic, serverName=args.serverName)