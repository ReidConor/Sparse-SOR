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
import sys

''' 
Checking if zeros on the Diagonal
'''


def hasZerosOnMainDiag (A):
    return np.in1d(0, np.diagonal(A))
 
'''
Checking if matrix is strictly diagonally dominant
'''
    
def isStrictlyDiagDom(A):
    rowcol = np.shape(A)[1]
    i = 0
    j = 0
    sumrow = 0 
    count = 0
    for i in range(n):
        sumrow = 0
        for j in range(n):
            if i != j:
                sumrow = sumrow + abs(A[i,j])
        if abs(A[i,i]) > sumrow:
            count += 1
    return count

'''
findX_noSOR finds solution for x, ie not using SOR
that is, follows the below logic...
Ax = b
(A^-1)(A)(x) = (A^-1)(b)
(1)(x) = (A^-1)(b)
so...x = the dot product of inverse(A) times b

this can be used to check the results of SOR against
'''
def findX_direct(A, b):
    A = A.todense()
    x = np.dot(np.linalg.inv(A), b)
    print ("Solution of x (no sor) = ", x)

def find_residual (A,x,b):
    return np.linalg.norm(b - A.dot(x))


# this is just to check out how to do tests in python
def add (x,y):
    return x+y
# IMPORTING MATRIX FROM market matrix
 
 
#print(mminfo("/Users/Carnec/Desktop/Business_Analytics/NumAnYr2/assignment2/plat1919.mtx"))
#m = mmread("/Users/Carnec/Desktop/Business_Analytics/NumAnYr2/assignment2/plat1919.mtx")
#print(m)

#m = m.asformat("csr") #transform from COO to CSR format

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

def Sparse_SOR(A,b,n,maxits,epsilon,omega):
    n = A.get_shape()[1]
    k = 0
    x = np.random.rand(n)
    diff = 5555555.0
    xnorm=0
    while k <= maxits and diff > epsilon:
        xnorm0 = xnorm
        for i in range(0,n):
            thesum = 0
            for j in range(int(A.indptr[i]),int(A.indptr[i+1])):
                thesum = thesum + A.data[j]*x[A.indices[j]]
                if col[j] == i:
                    d=val[j]
            x0 = x[i]
            x[i] = x[i] + omega *(b[i]-thesum)/d
        xnorm = np.linalg.norm(x, ord=2)
        print('xnorm',xnorm)
        diff = xnorm - xnorm0
        k = k+1
        print(diff)
    return x
        
#    
        
#### Example
matrix_example = csr_matrix(np.matrix([[1,0,0],[0,3,0],[0,1,3]]))

n = matrix_example.get_shape()[1]

x = np.ones(n) 

b = np.random.randint(0,5,size=3)


print(Sparse_SOR(matrix_example,b,n,100,0.00005,1.5))
