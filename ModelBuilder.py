import keras
from Encoder import Encoder
import tensorflow
import dill
import pandas
from typing import Callable, List

class ModelBuilder:
    def __init__(self, model: keras.models.Model, encoder: Encoder, compiler: Callable[[keras.models.Model],None]):
        self.modelArchitecture = model.to_json()
        self.modelWeights = model.get_weights()
        self.encoderBytes = dill.dumps(encoder)
        self.compiler = compiler

        self.model = None
        self.encoder = None
        self.initialized = False

    def loadModel(self) -> keras.models.Model:
        self.model = keras.models.model_from_json(self.modelArchitecture)
        self.model.set_weights(self.modelWeights)
        self.compiler(self.model)

        self.encoder = dill.loads(self.encoderBytes)
        self.initialized = True
        return self.model

    def predictDataFrame(self, df: pandas.DataFrame) -> List[str]:
        if not self.initialized:
            self.loadModel()
        X = self.encoder.encodeDataFrame(df)
        y = self.model.predict(X)
        labels, label_probs = self.encoder.reverse_label_encode(y)
        return labels, label_probs