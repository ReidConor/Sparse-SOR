import numpy as np

def hasZerosOnMainDiag (A):
    hasZero = False
    diag = np.diagonal(A)
    if np.in1d(0, diag):
        hasZero = True
    return hasZero


# this is just to check out how to do tests in python
def add (x,y):
    return x+y