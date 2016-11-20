import numpy as np
from scipy import sparse
from scipy.io import mmread
from scipy.sparse import csr_matrix
import sys

'''
Read matrix A and b into a dictionary
'''
def readFileIntoDict(inputFile):
    myDict = {}
    try:
        lines = open(inputFile, 'r').readlines()

        A = []
        dim = int(lines[0])
        b = [lines[dim+1]]
        for x in range(1, dim+1):
            A.append(lines[x])

        # want to use Compressed Sparse Row Format (csr)
        myDict["A"] = sparse.csr_matrix(np.loadtxt(A))
        myDict["b"] = np.loadtxt(b)

    except FileNotFoundError:
        print("That file does not exist. Try again")
        sys.exit(0)

    return myDict
    
    
def readFileMtx(inputFile):
    myDict = {}
    # A = sparse.csr_matrix(np.loadtxt(inputFile))
    # m = mmread('/Users/Conor/Google Drive/MSc/NMS_1/Prog_Assignment2/Sparse-SOR/docs/plat1919.mtx')

    try:
        m = mmread(inputFile)
        m = m.asformat("csr")
        dim = m.shape[1]
        b = np.random.randint(0, 10, size=dim)
        myDict["A"] = m
        myDict["b"] = b
    except FileNotFoundError:
        print("That file does not exist. Try again")
        sys.exit(0)

    return myDict
