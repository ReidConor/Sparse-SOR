import numpy as np
from scipy import sparse

# this is just to check out how to do tests in python
def add (x,y):
    return x+y

# read text file into A and b
# doesnt use spare matrix storage
def readFileIntoDict():
    lines = open('input.in','r').readlines()
    myDict = {}

    A = []
    dim = int(lines[0])
    b = [lines[dim+1]]
    for x in range (1, dim+1):
        A.append (lines[x])

    # want to use Compressed Sparse Row Format (csr)
    myDict["A"] = sparse.csr_matrix(np.loadtxt(A))
    myDict["b"] = np.loadtxt(b)
    return myDict