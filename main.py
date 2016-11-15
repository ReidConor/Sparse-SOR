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
logging.info('Starting SOR...')

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
        logging.info(findX_direct(A, b))
        logging.info("")

        resultsDict = Sparse_SOR(A, b, 200, 1.5, np.zeros(b.shape[0]), 0.0005)
        logging.info("stopped in: %s iterations ", resultsDict["iterations"])
        logging.info("final error is: %s ", resultsDict["finalError"])
        logging.info("answer according to SOR is: %s ", resultsDict["x"])


elif file_extension == ".mtx":
    theProblemSpaceMtx = readFileMtx(inputFile)
    A = theProblemSpaceMtx["A"]
    b = theProblemSpaceMtx["b"]

    resultsDict = Sparse_SOR(A, b, 200, 1.5, np.zeros(b.shape[0]), 0.00000005)
    logging.info("stopped in: %s iterations ", resultsDict["iterations"])
    logging.info("final error is: %s ", resultsDict["finalError"])
    logging.info("answer according to SOR is: %s ", resultsDict["x"])

else:
    logging.error("File input type not recognised")



'''
start logging for part two
'''
logging.info('Starting Black Scholes model...')
S, t = createSandT(50.0, 12, 1)  # Vector of stock price (grid points)

a, b, c = abcArrays(S, t, 0.3, 0.02)  # a is the bottom diag, b is the centre diag, c is top diag
A = tridiag(a, b, c)
print(A)
