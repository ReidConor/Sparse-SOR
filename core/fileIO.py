import numpy as np
from scipy import sparse
from scipy.io import mminfo,mmread

#ask for path of file

'''
Ask user to input matrix
'''

def inputMatrix():
    f = input("\n Hello, user. "
        "\n \n Please type in mtx if you are using an mtx file or txt if you are using a text file and press 'Enter': ")
    if f=='mtx':
        inputmtx = input("\n \n Please type in the path of the mtx file and press 'Enter': ")
        m =  mmread(inputmtx)
    elif f == 'txt':
        inputtxt = input("\n \n Please type in the path of the txt file and press 'Enter': ")
        m =  inputtxt 
    return f, m
    

'''
Read matrix A and b into a dictionary
'''

def readFileIntoDict(m):
    lines = open(m, 'r').readlines()
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
    
    
def readFileMtx(m):
    myDict = {}

    
    A = m.asformat("csr")
    dim = m.shape[1]
    b = np.random.randint(0,10,size=dim)
    
    myDict["A"] = A
    myDict["b"] = b
    return myDict
    
