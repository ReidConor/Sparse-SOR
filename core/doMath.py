import numpy as np
import sys
from pprint import pprint
from numpy import math, linalg, zeros, diag, dot, diagflat,array

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
                print(sumrow)
        if abs(A[i,i]) > sumrow:
            count += 1
    return count > 0


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
# def Sparse_SOR (A,b,n,maxits,omega,x, error):
#     k = 0
#     while k < maxits:
#         # print ("Iteration:" ,k)
#
#         omega_prev_prev = omega + 0.1
#         omega_prev = omega + 0.05
#         rows = b.shape[0]
#         D = A.diagonal()
#         err = find_residual(A, x, b)
#         err_prev = err + 1.0
#         while err > error:
#             s = np.zeros(b.shape[0])
#             for row in range(rows):
#                 cols = A.indices[A.indptr[row]:A.indptr[row + 1]]
#                 for j, col in enumerate(cols):
#                     if col != row:
#                         s[row] += A.data[A.indptr[row]:A.indptr[row + 1]][j] * x[col]
#
#                 if D[row] != 0.0:
#                     x[row] += omega * ((b[row] - s[row]) / D[row] - x[row])
#             k += 1
#             err_prev = err
#             err = find_residual(A, x, b)
#         print("SOR: x=", x)



def Sparse_SOR (A,b,n,maxits,omega,x, error):
    k = 0
    while k < maxits:
        # omega_prev_prev = omega + 0.1
        # omega_prev = omega + 0.05
        rows = b.shape[0]
        D = A.diagonal()
        err = 5
        xnorm = 0
        # errorlist = []
        while abs(err) > error:
            s = np.zeros(b.shape[0])
            xnorm1 = xnorm
            for row in range(rows):
                cols = A.indices[A.indptr[row]:A.indptr[row + 1]]
                for j, col in enumerate(cols):
                    if col != row:
                        s[row] += A.data[A.indptr[row]:A.indptr[row + 1]][j] * x[col]

                if D[row] != 0.0:
                    x[row] += omega * ((b[row] - s[row]) / D[row] - x[row])
            xnorm = np.linalg.norm(x, ord=2)
            err = xnorm - xnorm1
            k += 1
        break

    resultsDict = {}
    resultsDict["x"] = x
    resultsDict["iterations"] = k
    resultsDict["finalError"] = err
    return resultsDict

'''
From the notes:
There are two common ways to measure the discrepancy between the true solution x and the computed solution xˆ:
    Error: δx=x−xˆ
    Residual: r = b − Axˆ
'''
def find_residual (A,x,b):
    return np.linalg.norm(b - A.dot(x))

def jacobi(A,b,N=25,x=None):                                                                                                                                                        
    if x is None:
        x = zeros(len(A[0]))                                                                                                                                                                   
    D = diag(A)
    R = A - diagflat(D)
    for i in range(N):
        x = (b - dot(R,x)) / D
    return x
    
A = array([[9.0,-1.0,2.0],[-2.0,8.0,4.0],[1.0,1.0,8.0]])
b = array([11.0,13.0,13.0])
guess = array([1.0,1.0,1.0])

sol = jacobi(A,b,N=25,x=guess)
pprint(sol)
T = np.matrix(A)

spec_rad=np.max(np.linalg.eigvals(T))
pprint(spec_rad)
if spec_rad <1:
    print("Matrix A will converge!")
else:
    print("Matrix A will not converge!")