
import numpy as np
from scipy.sparse import csc_matrix
from matplotlib import pylab as plt
import sys
# from core.tridiagM import *
from core.visualize import *
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
    for i in range(rowcol):
        sumrow = 0
        for j in range(rowcol):
            if i != j:
                sumrow = sumrow + abs(A[i,j])
                # print(sumrow)
        if abs(A[i, i]) > sumrow:
            count += 1
    return count == 0


def isStrictlyDiagonallyDominant(A):

    # check columns for dominance
    col_sum = np.sum(A, axis=0)
    diags = np.diagonal(A)
    col_difference = col_sum - diags
    col_dom = (np.all(np.greater(diags, col_difference)))

    # check rows for dominance
    row_sum = np.sum(A, axis=1)
    diags_transpose = np.array([diags]).T
    row_difference = row_sum - diags_transpose
    row_dom = (np.all(np.greater(diags_transpose, row_difference)))

    return col_dom & row_dom


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
    return x


'''
omega must be > 1 to be the successive over-relaxation method.
< 1 its the successive under-relaxation
'''


# def Sparse_SOR(A, b, n, maxits, omega, x, error):
#     k = 0
#     while k < maxits:
#         # omega_prev_prev = omega + 0.1
#         # omega_prev = omega + 0.05
#         rows = b.shape[0]
#         D = A.diagonal()
#         err = 10000
#         xnorm = 0
#         xnorm1 = 100
#         while abs(err) > error:
#             s = np.zeros(b.shape[0])
#             for row in range(rows):
#                 y = x[row]
#                 cols = A.indices[A.indptr[row]:A.indptr[row + 1]]
#                 for j, col in enumerate(cols):
#                     if col != row:
#                         s[row] += A.data[A.indptr[row]:A.indptr[row + 1]][j] * x[col]
#
#                 if D[row] != 0.0:
#                     x[row] += omega * ((b[row] - s[row]) / D[row] - x[row])
#
#                 xnorm1 = xnorm
#                 xnorm = np.linalg.norm(y - x, ord=rows)
#                 err = xnorm
#                 k += 1
#                 if abs(xnorm) > abs(xnorm1):
#                     print('divergence')
#                     break
#         break
#
#     resultsDict = {}
#     resultsDict["x"] = x
#     resultsDict["iterations"] = k
#     resultsDict["finalError"] = err
#     return x


def Sparse_SOR(A,b,n,maxits,omega,x, error):
    n = A.get_shape()[1]
    k = 0
    diff = 5555555.0
    xnorm=0
    x0 = x
    diffnorm = 0
    while k <= maxits and diff > error:
        diffnorm0 = diffnorm
        xnorm0 = xnorm
        for i in range(0, n):
            thesum = 0
            for j in range(int(A.indptr[i]), int(A.indptr[i+1])):
                thesum = thesum + A.data[j]*x[A.indices[j]]
                if A.indices[j] == i:
                    d = A.data[j]
            # print(i, j)

            x[i] = x[i] + omega *(b[i]-thesum)/d
            diffnorm = np.linalg.norm(x - x0, ord=n)

        # print(diffnorm)
        # print(diffnorm0)
        xnorm = np.linalg.norm(x, ord=2)
        diff = abs(xnorm - xnorm0)
        if abs(diffnorm) > abs(diffnorm0):
                print('divergence')
                stoppingReason = "x Sequence divergence"
                break
        k += 1
    resultsDict = {}
    resultsDict["x"] = x
    resultsDict["iterations"] = k
    resultsDict["diffnorm"] = diffnorm
    resultsDict["diffnorm0"] = diffnorm0

    if k == maxits:
        stoppingReason = "Max Iterations reached"
    else:
        stoppingReason = "x Sequence convergence"
    resultsDict["stoppingReason"] = stoppingReason

    return resultsDict






'''
From the notes:
There are two common ways to measure the discrepancy between the true solution x and the computed solution xˆ:
    Error: δx=x−xˆ
    Residual: r = b − Axˆ
'''
def find_residual(A,x,b):
    return np.linalg.norm(b - A.dot(x))
