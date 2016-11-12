
from core.fileIO import *
from core.doMath import *
import logging
import os

'''
This will function as the main module of te python project
and call all other modules that are written
'''

'''
set up logging
this will function as our way of writing the stopping condition out to a file
'''
fn = os.path.join(os.path.dirname(__file__), '../logs/logs.txt')
logging.basicConfig(filename=fn, filemode='w', level=logging.DEBUG)

# get the problem space from txt file, ie. A and b from "Ax = b"
theProblemSpace = readFileIntoDict()
A = theProblemSpace["A"]
b = theProblemSpace["b"]

logging.info('Starting SOR')  # will not print anything

'''
check for zeros on the main diagonal (one of the stopping rules)
use todense() to give the normal matrix representation of A
'''

if hasZerosOnMainDiag(A.todense()):
    logging.error("Error Found...")
    logging.error("Zeros on the main diagonal!")
if not isStrictlyDiagonallyDominant(A.todense()):
    logging.error("Error Found...")
    logging.error("A is not strictly diagonally dominant!")
else:
    logging.info("Can continue...")
    logging.info("solution (direct) is: ")
    logging.info(findX_direct(A, b))
    logging.info("")

    # passing dummy values until I end up using them correctly in the function
    # if its zero, its not used
    resultsDict = Sparse_SOR(A, b, 0, 200, 1.5, np.zeros(b.shape[0]), 0.0005)
    logging.info("stopped in: %s iterations ", resultsDict["iterations"])
    logging.info("final error is: %s ", resultsDict["finalError"])
    logging.info("answer according to SOR is: %s ", resultsDict["x"])
