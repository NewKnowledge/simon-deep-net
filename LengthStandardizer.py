# -*- coding: utf-8 -*-
"""
Created on Fri May 26 18:51:50 2017

@author: azunre
"""

import numpy as np

# standardize all column row number for fixed input-length CNN
def DataLengthStandardizer(X, max_cells):
    nsamples, nx, ny = X.shape
    if nx >= max_cells:
        X = np.delete(X, np.arange(max_cells, nx), axis=1)  # truncate
    else:
        # replicate some randomly-selected cells
        X = np.concatenate(
            (X, X[:, np.random.choice(nx, max_cells - nx), :]), axis=1)
    return X
    
# standardize a single column row number (column as list input, array output, 
# used for data lake column data-length standardization)
def DataLengthColumnStandardizer(column, max_cells):
    nrows = len(column)
    #print(nrows)
    if nrows >= max_cells:
        column = np.asarray(column)
        column = np.delete(column,np.arange(max_cells,nrows))
        
    else:
        # replicate some randomly-selected cells
        column = column.append(column[np.random.choice(nrows, max_cells - nrows)])
        column = np.asarray(column)
        
    return column
