import numpy as np

def hasZerosOnMainDiag (A):
    return np.in1d(0, np.diagonal(A))

# this is just to check out how to do tests in python
def add (x,y):
    return x+y