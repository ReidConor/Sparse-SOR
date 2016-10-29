import numpy as np

# this is just to check out how to do tests in python
def add (x,y):
    return x+y

# read text file into A and b
def readFileIntoDict():
    lines = open('input.txt','r').readlines()
    myDict = {}

    A = []
    dim = int(lines[0])
    b = [lines[dim+1]]
    for x in range (1, dim+1):
        A.append (lines[x])

    myDict["A"] = np.loadtxt(A)
    myDict["b"] = np.loadtxt(b)
    return myDict