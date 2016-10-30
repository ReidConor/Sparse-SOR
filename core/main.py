# This will function as the main module of te python project
# and call all other modules that are written
from core.fileIO import *
from core.doMath import *

# get the problem space from txt file, ie. A and b from "Ax = b"
theProblemSpace = readFileIntoDict()

#  check for zeros on the main diag (one of the stopping rules)
# use todense() to give the nornal matrix representation of A
if hasZerosOnMainDiag(theProblemSpace["A"].todense()):
    print ("Cant go on")
else:
    print ("Continue")