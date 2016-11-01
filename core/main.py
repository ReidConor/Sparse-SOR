
from core.fileIO import *
from core.doMath import *

'''
This will function as the main module of te python project
and call all other modules that are written
'''


# get the problem space from txt file, ie. A and b from "Ax = b"
theProblemSpace = readFileIntoDict()
A = theProblemSpace["A"]
b = theProblemSpace["b"]

'''
check for zeros on the main diag (one of the stopping rules)
use todense() to give the nornal matrix representation of A
'''
if hasZerosOnMainDiag(A.todense()):
    print ("Cant go on")
else:
    print ("Can continue..")
    findX_direct(A, b)

    # passing dummy values until I end up using them correctly in the function
    # if its zero, its not used
    Sparse_SOR (A,b,0,1,1.5,np.zeros(b.shape[0]),0.00000001)