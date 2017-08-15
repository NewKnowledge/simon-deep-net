import dill

class SimonPrimitiveWrapper:
	def __init__(self, modelName = 'model.pkl'):
		self.modelName = modelName
		self.model = dill.load(open(modelName, 'rb'))


	def __getitem__(self, key):
		if key == 'accepted_data_types':
			return ['text']


	def predict(self, data, input_data_shape=[], input_data_types=[], first_value_label=False):
		predictions = model.predict(data)
		# how much to pass on to model -- should we be extremely strict and say that predict() must 
		# accept a numpy matrix, and return a list of strings?
		# How to handle differences in how to handle the data -- data type label vs. maximum correlation
		# associating predictions with the indexes/labels of the source data?

		return data
