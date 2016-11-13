import numpy as np
from scipy import sparse

# read text file into A and b
def readFileIntoDict(inputFile):
    lines = open(inputFile, 'r').readlines()
    myDict = {}

    A = []
    dim = int(lines[0])
    b = [lines[dim+1]]
    for x in range(1, dim+1):
        A.append(lines[x])

    # want to use Compressed Sparse Row Format (csr)
    myDict["A"] = sparse.csr_matrix(np.loadtxt(A))
    myDict["b"] = np.loadtxt(b)
    return myDict