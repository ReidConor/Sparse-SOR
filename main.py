from core.fileIO import *
from core.doMath import *
import logging
import os
from core.tridiagM import *

'''
This will function as the main module of te python project
and call all other modules that are written
'''

'''
check if params are passed to the program, and use them if they are
'''
inputFile = (sys.argv[1] if len(sys.argv) == 2 else "../docs/input.in")
outputFile = (sys.argv[2] if len(sys.argv) == 3 else "./logs/logs.out")
file_extension = os.path.splitext(inputFile)[1]


'''
set up logging
this will function as our way of writing the stopping condition out to a file
'''
fn = os.path.join(os.path.dirname(__file__), outputFile)
logging.basicConfig(filename=fn, filemode='w', level=logging.DEBUG)


'''
start logging for part one
'''
logging.info('Starting SOR...assignment part one')

'''
program flow depends on input file type
.in has matrices represented literally, .mtx as coo / csr
'''
if file_extension == ".in":
    theProblemSpace = readFileIntoDict(inputFile)
    A = theProblemSpace["A"]
    b = theProblemSpace["b"]

    # check for zeros on the main diagonal (one of the stopping rules)
    # use todense() to give the normal matrix representation of A
    if hasZerosOnMainDiag(A.todense()):
        logging.error("Error Found...")
        logging.error("Zeros on the main diagonal!")

    # check to see if the matrix is diagonally dominant
    if not isStrictlyDiagonallyDominant(A.todense()):
        logging.error("Error Found...")
        logging.error("A is not strictly diagonally dominant!")
    else:
        logging.info("Can continue...")
        logging.info("solution (direct) is: ")
        logging.info("The direct answer is: %s", findX_direct(A, b))
        resultsDict = Sparse_SOR(A, b, 1, 200, 1.5, np.zeros(b.shape[0]), 0.0005)
        logging.info("The answer according to SOR is: %s", resultsDict)


elif file_extension == ".mtx":
    theProblemSpaceMtx = readFileMtx(inputFile)
    A = theProblemSpaceMtx["A"]
    b = theProblemSpaceMtx["b"]

    if hasZerosOnMainDiag(A.todense()):
        logging.error("Error Found...")
        logging.error("Zeros on the main diagonal!")

    # look into a module for spectral radius in python
    # check to see if the matrix is diagonally dominant
    if not isStrictlyDiagDom(A.todense()):
        logging.error("Error Found...")
        logging.error("A is not strictly diagonally dominant!")

else:
    logging.error("File input type not recognised")



logging.info('Starting Black Scholes model...assignment part two')

# General parameters
S0 = 0
SMax = 150
T = 12
k = 1
X = 50

# Parameters for SOR_Sparse
sigma = 0.3
r = 0.02
maxits = 100
omega = 1.5
error = 0.0005

S, t, matrixsize, h = createSandT(S0, SMax, T, k)  # Vector of stock price (grid points)
fnM = vectorB(X, S, h)  # bvec gives fn,m or the option prices at time T.
a, b, c = abcArrays(S, t, sigma, r)  # a is the bottom diag, b is the centre diag, c is top diag
A = sparse.csr_matrix(tridiag(a, b, c))
n = A.shape[1]
x = np.zeros(n)
# Sparse_SOR(A, fnM, n, maxits, omega, x, error) #SOR solves Ax = b
# fnm0 is fn,m-1. its the result from solving Ax=b in SOR (A xSOR = bvec)

pastfnm = findPastOptionPrices(A, fnM, n, maxits, omega, x, error, T, k)
logging.info('f_{n,m= %s } (m=M=T=12) = %s', 12, fnM)
logging.info('------')
for i in range(len(pastfnm) - 1, -1, -1):
    logging.info('f_{n, %s } = %s', i, pastfnm[i])
