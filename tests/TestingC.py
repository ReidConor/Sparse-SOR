# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 20:02:05 2016

@author: Eoghan
"""

import numpy as np
from numpy import *

# print(np.linalg.eigvals(A))

def CreateC(A):
    rowcol = np.shape(A)[1]
    i = 0
    j = 0
    U = []
    L = []
    D = []
    for i in range(rowcol):
        L.append([])
        U.append([])
        D.append([])
        for j in range(rowcol):

            if i > j:
                L[i].append(A[i, j])
                U[i].append(0)
                D[i].append(0)
            elif i == j:
                L[i].append(0)
                U[i].append(0)
                D[i].append(A[i, j])
            else:
                L[i].append(0)
                U[i].append(A[i, j])
                D[i].append(0)

    print("D:", D)
    print("L:", L)
    T = np.add(D, L)
    print("T:", T)
    K = np.invert(T) * -1
    C = np.multiply(K, U)
    print(C)
    print("K:", K)
    print("U:", U)

    print(np.linalg.eigvals(C))
    print(np.linalg.eigvals(A))
    # C = -1*(linalg.inv(D+L))*U
    # print(C)


A = np.matrix(([10, 8], [5, 4]))  # Has large Eigenvectors
CreateC(A)
