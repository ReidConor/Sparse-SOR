from core.fileIO import *
from core.doMath import *
from core.tridiagM import *
from core.visualize import *
import logging
import os
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt

'''
check if params are passed to the program, and use them if they are
'''
import os
dir = os.path.dirname(__file__)
inputFile = (sys.argv[1] if len(sys.argv) == 2 else os.path.join(dir, './docs/input.in'))
outputFile = (sys.argv[2] if len(sys.argv) == 3 else os.path.join(dir, './logs/nas_SOR.out'))
file_extension = os.path.splitext(inputFile)[1]

'''
start logging for part one
'''
target = open(outputFile, 'w')

maxits = 200
resultsDict = {}
resultsDict["x"] = ""
resultsDict["iterations"] = 0
resultsDict["diffnorm"] = ""
resultsDict["diffnorm0"] = ""
resultsDict["stoppingReason"] = "Unknown"
resultsDict["ResidualSeqTolerance"] = "Not used"

X_seq_tolerance = 0.0005

if file_extension == ".in":
    theProblemSpace = readFileIntoDict(inputFile)
    A = theProblemSpace["A"]
    b = theProblemSpace["b"]

    if hasZerosOnMainDiag(A.todense()):
        resultsDict["stoppingReason"] = "Zero on diagonal"

    elif not isStrictlyDiagonallyDominant(A.todense()):
        resultsDict["stoppingReason"] = "Cannot proceed"
    else:
        if np.shape(A) <= (300, 300):
            genHeatMap(A.todense(), os.path.join(dir, './docs/A(.in).png'))
        resultsDict = Sparse_SOR(A, b, 1, maxits, 1.5, np.zeros(b.shape[0]), X_seq_tolerance)



elif file_extension == ".mtx":
    theProblemSpaceMtx = readFileMtx(inputFile)
    A = theProblemSpaceMtx["A"]
    b = theProblemSpaceMtx["b"]

    if hasZerosOnMainDiag(A.todense()):
        resultsDict["stoppingReason"] = "Zero on diagonal"

    elif not isStrictlyDiagonallyDominant(A.todense()):
        resultsDict["stoppingReason"] = "Cannot proceed."

    else:
        if np.shape(A) <= (300, 300):
            genHeatMap(A.todense(), os.path.join(dir, './docs/A(.in).png'))
        resultsDict = Sparse_SOR(A, b, 1, maxits, 1.5, np.zeros(b.shape[0]), X_seq_tolerance)

else:
    resultsDict["stoppingReason"] = "input file error"


target.write('%-30s %-30s %-30s %-30s %-30s %-30s' % ('Stopping reason', 'Max num of iterations', 'Num of iterations', 'Machine epsilon', 'X seq tolerance', 'Residual seq tolerance'))
target.write('\n')
target.write('%-30s %-30s %-30s %-30s %-30s %-30s' % (resultsDict["stoppingReason"], maxits, resultsDict["iterations"], np.finfo(np.float).eps, X_seq_tolerance, resultsDict["ResidualSeqTolerance"]))

if resultsDict["x"] != "":
    target.write('\n')
    target.write('%s' % (resultsDict["x"]))


'''
Part two - BSM Equation
'''
# takes an argument for logging location
runBSM(os.path.join(dir, './logs/BSM_logs.out'))



