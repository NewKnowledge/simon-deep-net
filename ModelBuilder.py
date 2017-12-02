import keras
from Encoder import Encoder
import numpy as np
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

    def predictDataFrame(self, df: pandas.DataFrame,p_threshold) -> List[str]:
        if not self.initialized:
            self.loadModel()
            
        nrows,ncols = df.shape
        ROWDISCREP = False
        if((nrows > 5*self.encoder.cur_max_cells) or (nrows < 1/5*self.encoder.cur_max_cells)):
            print("SIMON::WARNING::Large Discrepancy between original number of rows and CNN input size")
            print("SIMON::WARNING::i.e., original nrows=%d, CNN input size=%d"%(nrows,self.encoder.cur_max_cells))
            print("SIMON::WARNING::column-level statistical variable CNN predictions, e.g., categorical/ordinal, may not be reliable")
            ROWDISCREP = True # may be used to trigger re-run of penny in the near future
        
        X = self.encoder.encodeDataFrame(df)
        y = self.model.predict(X)
        
        # make sure to discard the "entire column empty" edge case
        y[np.all(df.isnull(),axis=0)]=0
        
        labels, label_probs = self.encoder.reverse_label_encode(y,p_threshold)
        return labels, label_probs