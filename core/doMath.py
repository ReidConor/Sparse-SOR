import numpy as np
import sys
def hasZerosOnMainDiag (A):
    return np.in1d(0, np.diagonal(A))

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


'''
omega must be > 1 to be the successive over-relaxation method.
< 1 its the successive under-relaxation
'''
def Sparse_SOR (A,b,n,maxits,omega,x, error):
    k = 0
    while k < maxits:
        # print ("Iteration:" ,k)

        omega_prev_prev = omega + 0.1
        omega_prev = omega + 0.05
        rows = b.shape[0]
        D = A.diagonal()
        err = find_residual(A, x, b)
        err_prev = err + 1.0
        while err > error:
            s = np.zeros(b.shape[0])
            for row in range(rows):
                cols = A.indices[A.indptr[row]:A.indptr[row + 1]]
                for j, col in enumerate(cols):
                    if col != row:
                        s[row] += A.data[A.indptr[row]:A.indptr[row + 1]][j] * x[col]

                if D[row] != 0.0:
                    x[row] += omega * ((b[row] - s[row]) / D[row] - x[row])
            k += 1
            err_prev = err
            err = find_residual(A, x, b)
        print("SOR: x=", x)



'''
From the notes:
There are two common ways to measure the discrepancy between the true solution x and the computed solution xˆ:
    Error: δx=x−xˆ
    Residual: r = b − Axˆ
'''
def find_residual (A,x,b):
    return np.linalg.norm(b - A.dot(x))


# this is just to check out how to do tests in python
def add (x,y):
    return x+y