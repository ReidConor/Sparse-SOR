import numpy as np
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
def Sparse_SOR(A, b, maxits, omega, x, error):
    k = 0
    while k < maxits:
        rows = b.shape[0]
        D = A.diagonal()
        xnorm = 0
        err = 100
        while abs(err) > error:
            s = np.zeros(b.shape[0])
            xnorm_0 = xnorm
            err_0 = err
            for row in range(rows):
                cols = A.indices[A.indptr[row]:A.indptr[row + 1]]
                for j, col in enumerate(cols):
                    if col != row:
                        s[row] += A.data[A.indptr[row]:A.indptr[row + 1]][j] * x[col]

                if D[row] != 0.0:
                    x[row] += omega * ((b[row] - s[row]) / D[row] - x[row])
            xnorm = np.linalg.norm(x, ord=2)
            err = xnorm - xnorm_0
            print('iteration', k)
            print('err', abs(err))
            print('err_0', abs(err_0))
            k += 1
            if abs(err) > abs(err_0):
                print('*** Divergence detected ***')
                break
        break

    # print('*** We have convergence ***')
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
def find_residual(A,x,b):
    return np.linalg.norm(b - A.dot(x))
