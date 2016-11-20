
#from core.fileIO import *
#from core.doMath import *

import fileIO
import doMath
from scipy.io import mminfo,mmread

# Ask user whether input path is mtx or txt
# ask for file path
f, m = fileIO.inputMatrix()

'''
This will function as the main module of tte python project
and call all other modules that aretx written
'''


# get the problem space from txt file, ie. A and b from "Ax = b"
if f=='txt':
    theProblemSpace = fileIO.readFileIntoDict(m)
    A = theProblemSpace["A"]
    b = theProblemSpace["b"]

# get market matrix and assign to A. create random b matrix.
#m = mmread("/Users/Carnec/Desktop/Business_Analytics/NumAnYr2/assignment2/plat1919.mtx")
elif f == 'mtx':
    theProblemSpaceMtx = fileIO.readFileMtx(m)
    A = theProblemSpaceMtx["A"]
    b = theProblemSpaceMtx["b"]

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
x, errorlist = Sparse_SOR (A,b,0,100,1.5,np.zeros(b.shape[0]),0.00000001)
print(x)
print(errorlist)