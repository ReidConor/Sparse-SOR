import numpy as np
from scipy import sparse


'''
Read matrix A and b into a dictionary
'''
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
    
    
def readFileMtx(inputFile):
    myDict = {}
    A = sparse.csr_matrix(np.loadtxt(inputFile))
    dim = A.shape[1]
    b = np.random.randint(0, 10, size=dim)
    
    myDict["A"] = A
    myDict["b"] = b
    return myDict
