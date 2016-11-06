#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 18:59:22 2016

@author: Carnec
"""

"""
Sparse-SOR
"""
from scipy.io import mminfo,mmread
from scipy.sparse import csr_matrix
import numpy as np
import numpy.random
# IMPORTING MATRIX FROM market matrix
 
 
#print(mminfo("/Users/Carnec/Desktop/Business_Analytics/NumAnYr2/assignment2/plat1919.mtx"))
#m = mmread("/Users/Carnec/Desktop/Business_Analytics/NumAnYr2/assignment2/plat1919.mtx")
#print(m)

m = m.asformat("csr") #transform from COO to CSR format

# USER INPUT MATRIX



# Checking if diagonally dominant:
    #sum of column and row has to be smaller than diagonal
mdiag = m.diagonal()
all(i != 0 for i in mdiag)

def isdiagzero(matrix):
    mdiag = matrix.diagonal()
    if all(i != 0 for i in mdiag) == True:
        print("No zeros in the diagonal")
    else:
        print("Zeros in the diagional exist")
        
#print(isdiagzero(m))

# Sparse-SOR

val = m.data #values
rowstart = m.indices #rowstart
col = m.indptr #col

def Sparse_SOR(A,b,maxits,epsilon,w):
    n = A.get_shape()[1]
    k = 0
    x = np.random.rand(n)
    diff = 5555555.0
    while k <= maxits and diff > epsilon:
        for i in range(0,n):
            thesum = 0
            for j in range(int(A.indptr[i]),int(A.indptr[i+1])):
                thesum = thesum + A.data[j]*x[A.indices[j]]
                if col[j] == i:
                    d=val[j]
            x0 = x[i]
            x[i] = x[i] + w *(b[i]-thesum)/d
            diff = abs(x[i] - x0)
            print(diff)
        k = k+1
    return x
        
#    
        
#### Example
m = csr_matrix(np.matrix([[1,0,0],[0,3,0],[0,1,3]]))

n = matrix_example.get_shape()[1]

x = np.ones(n) 

b = np.random.randint(0,5,size=3)


print(Sparse_SOR(matrix_example,b,10,0.005,0.5))
