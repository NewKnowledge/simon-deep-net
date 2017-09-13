import pandas
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MultiLabelBinarizer
from keras.utils import np_utils
import json


class StringToIntArrayEncoder:
    def encode(self, string, char_count):
        return [ord(c) for c in string.ljust(char_count)[:char_count]]


class Encoder:
    def __init__(self):
        self._char_indicies = {}
        self._indices_char = {}
        self.cur_max_cells = 0
        self._encoder = LabelEncoder()


    def process(self, raw_data, max_cells):
        chars = {}
        for doc in raw_data:
            for cell in doc:
                for c in cell:
                    if not c in chars:
                        chars[c] = True
        #this line is sounding increasingly unnecesary, probably should just always leave it capped to 500
        self.cur_max_cells = min(raw_data.shape[1], max_cells)
        chars = sorted(list(chars))

        self.char_indices = dict((c, i) for i, c in enumerate(chars))
        self._indices_char = dict((i, c) for i, c in enumerate(chars))

        #print("chars {}".format(chars))
        ##print('Sample column: {}'.format(columns[2]))
        #print('Values: {}'.format(
        #    np.append(header[:, None], raw_data[:, 0:2], axis=1)))
  
    def encode_matrix(self, matrix):
        chars = 20
        new_matrix = np.zeros((matrix.shape[0], matrix.shape[1], chars))
        for row in range(0, matrix.shape[0]):
            # new_array = [_encoder.encode(string, 20) for string in
            # matrix[row,:]]
            new_array = []
            for col in range(0, matrix.shape[1]):
                new_matrix[row, col] = self._encoder.encode(matrix[row, col], chars)
                # new_array[row,col].append(_encoder.encode(matrix[row,col],
                # chars))
            # new_matrix.append(new_array)
        return new_matrix

    def encode_data(self, raw_data, header, max_len):
        
        # print("DEBUG::inside encode_data:")
        # print(raw_data.shape)


        X = np.ones((raw_data.shape[0], self.cur_max_cells,
                     max_len), dtype=np.int64) * -1
        y = self.label_encode(header)
        
        # print(X.shape)
        # print(self.cur_max_cells)
        
        # track unencoded chars
        unencoded_chars = None
        with open('unencoded_chars.json') as data_file:
            unencoded_chars = json.load(data_file)
        unencoded_dict = {k: v for k, v in unencoded_chars.items() if not v in ['']}

        for i, column in enumerate(raw_data):
            for j, cell in enumerate(column):
                if(j < self.cur_max_cells):
                    string = cell[-max_len:].lower()
                    for k, char in enumerate(string):
                        try:
                            X[i, j, (max_len - 1 - k)] = self.char_indices[char]
                        except Exception:
                            # previous unencountered character code
                            # print("error with: {0}".format(self.char_indices))
                            # raise
                            X[i, j, (max_len - 1 - k)] = self.char_indices[' '];
                            if char in unencoded_dict.keys():
                                unencoded_dict[char] = unencoded_dict[char]+1
                            else:
                                unencoded_dict[char] = 1
        with open('unencoded_chars.json','w') as out_file:
            json.dump(unencoded_dict, out_file)
        print("X shape: {0}\ny shape: {1}".format(X.shape, y.shape))
        
        return X, y

    def decode_matrix(self, X):
        ret_val = np.empty((X.shape[0], X.shape[1]), dtype='object')
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                string = ""
                # start at the end since we reversed it
                for k in range(X.shape[2] - 1, -1, -1):
                    if X[i, j, k] < 0:
                        continue
                    string = string + self._indices_char[X[i, j, k]]
                ret_val[i, j] = string
        return ret_val

    def label_encode(self, Y):
        # encode class values as integers
        with open('Categories.txt','r') as f:
            Categories = f.read().splitlines()
        # previous single-label code
        # self._encoder.fit(Categories)
        # encoded_Y = self._encoder.transform(Y)
        # print("DEBUG::encoded_Y")
        # print(encoded_Y)
        # ret_val = np_utils.to_categorical(encoded_Y, num_classes=len(set(Categories)))
        
        # convert integers to dummy variables (i.e.  one hot encoded)
        multi_encoder = MultiLabelBinarizer()
        multi_encoder.fit([Categories])
        # print("DEBUG::Y")
        # print(Y)
        # print(Y.shape)
        # convert into 'iterable of iterables' for multilabel encoder
        # labels = [[Y[0]], ]
        # for i in np.arange(1,len(Y)):
        #    labels.append(list([Y[i]]))
        ret_val = multi_encoder.transform(Y)
        # print("DEBUG::ret_val")
        # print(ret_val)
        

        return ret_val

    def reverse_label_encode(self, y):        
#        return self._encoder.inverse_transform(y.argmax(1))
        with open('Categories.txt','r') as f:
            Categories = f.read().splitlines()
        multi_encoder = MultiLabelBinarizer()
        multi_encoder.fit([Categories])
        
        #print("DEBUG::y:")
        #print(y)
        #print(y.shape)
        
        
        p_threshold = 0.5
        prediction_indices = y > p_threshold
        y_pred = np.zeros(y.shape)
        y_pred[prediction_indices] = 1
        
        
        ret_val = multi_encoder.inverse_transform(y_pred)
        
        #print("DEBUG::ret_val:")
        #print(ret_val)
        
        return ret_val
        
        
        
    def encodeDataFrame(self, df: pandas.DataFrame):    
        raw_data = np.char.lower(np.transpose(df.values).astype('U'))
        
        #print("DEBUG::raw_data")
        #print(raw_data)
        
        return self.x_encode(raw_data, 20)  
        
        
    def x_encode(self, raw_data, max_len):

        X = np.ones((raw_data.shape[0], self.cur_max_cells,
                     max_len), dtype=np.int64) * -1        
        # print(X.shape)
        # print(self.cur_max_cells)
        
        # track unencoded chars
        unencoded_chars = None
        with open('unencoded_chars.json') as data_file:
            unencoded_chars = json.load(data_file)
        unencoded_dict = {k: v for k, v in unencoded_chars.items() if not v in ['']}

        for i, column in enumerate(raw_data):
            for j, cell in enumerate(column):
                if(j < self.cur_max_cells):
                    string = cell[-max_len:].lower()
                    for k, char in enumerate(string):
                        try:
                            X[i, j, (max_len - 1 - k)] = self.char_indices[char]
                        except Exception:
                            # previous unencountered character code
                            # print("error with: {0}".format(self.char_indices))
                            # raise
                            X[i, j, (max_len - 1 - k)] = self.char_indices[' '];
                            if char in unencoded_dict.keys():
                                unencoded_dict[char] = unencoded_dict[char]+1
                            else:
                                unencoded_dict[char] = 1
        with open('unencoded_chars.json','w') as out_file:
            json.dump(unencoded_dict, out_file)
        #print("X shape: {0}".format(X.shape))
        
        return X
