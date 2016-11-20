# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 20:02:05 2016

@author: Eoghan
"""

import numpy as np
from numpy import *
import random
import scipy as sp
from scipy import eye, sparse
import os

dir = os.path.dirname(__file__)
def CreateC(A):
    rowcol = np.shape(A)[1]
    # print("Rows:", rowcol)
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
    T = np.add(D, L)
    # print(T)
    K = np.invert(T) * -1
    # print(np.invert(T))
    # print(K)
    C = np.dot(K, U)
    # print("L:" ,L)
    # print("U:" ,U)
    # print("D:" ,D)
    # print("A:" ,A)
    # print("C:" ,C)

    # print("Eigvals of C" ,np.linalg.eigvals(C))
    # print("Eigvals of a" ,np.linalg.eigvals(A))

    Z = np.linalg.eigvals(C)

    # print("Z:",Z)
    return {'Z': Z, 'C': C}


# Matrix 1  - Small Matrix A having 0 on the diagonal
A = np.matrix(([3, 1, 5], [6, 0, 8], [8, 4, 6]))
# Matrix 2  - Small Diagonally dominant Matrix A
A = np.matrix(([5, 2, 3], [1, 6, 3], [2, 3, 7]))
# Matrix 3  - Small Matrix A with no 0 on the main diagonal, not diagonally dominant, none of the eigenvalues of C <1
A = np.matrix(([-1, 0, 0, -2], [1, 1, -1, -2], [0, -2, -2, -1], [-1, 0, -2, -1]))  # Eigenvalue of 1.60341207336e-16
# Matrix 4  - Small Matrix A with no 0 on the main diagonal, not diagonally dominant, one or more of the eigenvalues of C >1
A = np.matrix(([-1, -2, -2, -1], [0, -1, -1, 0], [-1, 0, -2, -1], [1, -1, -2, -2]))  # Has max Eigenvalue of 3.0
# Matrix 5  - Small Matrix A with no 0 on the main diagonal, not diagonally dominant, one or more of the eigenvalues of C >1
A = np.matrix(([-1, 1, 0], [-1, -1, 0], [-1, 1, -1]))  # Eigenvalues: [ 0.  0.  0.]
# Matrix 6  - Large sprarse Diagonally dominant Matrix A

A = sp.eye(5000, 5000)
print(A)
n = 10 ** 3
density = 1e-3
ij = np.random.randint(n, size=(2, n * n * density))
data = np.random.rand(n * n * density)
A = sp.sparse.coo.coo_matrix((data, ij), (n, n))
# print(A.A)
# print("Condition number" ,np.linalg.cond(A))
A = np.matrix(([18, 3], [7, 8]))


def jacobi(A, b, N=25, x=None):
    if x is None:
        x = zeros(len(A[0]))
    D = diag(A)
    R = A - diagflat(D)
    for i in range(N):
        x = (b - dot(R, x)) / D
    return x


# A = array([[9.0,-1.0,2.0],[-2.0,8.0,4.0],[1.0,1.0,8.0]])
# b = array([11.0,13.0,13.0])
# guess = array([1.0,1.0,1.0])
# 
# sol = jacobi(A,b,N=25,x=guess)
#
# T = np.matrix(A)
# 
# spec_rad=np.max(np.linalg.eigvals(T))
##print(spec_rad)
# if spec_rad <1:
#    print("Matrix A will not converge!") 
# else:
#    print("Matrix A will not converge!") 

def CreateMatrix(eig_vals, eig_vects):
    eig_vects_inv = np.linalg.inv(eig_vects)
    A = np.dot(eig_vects, (np.dot(eig_vals, eig_vects_inv)))
    print(A)
    print(np.linalg.eigvals(A))


eig_vals = np.matrix(([1, 0, 0], [0, -2, 0], [0, 0, 2]))
eig_vects = np.matrix(([1, 1, -1], [0, 1, 2], [-1, 1, -1]))


# CreateMatrix(eig_vals,eig_vects)

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
                sumrow = sumrow + abs(A[i, j])
                # print(sumrow)
        if abs(A[i, i]) > sumrow:
            count += 1
    return count > 0


def hasZerosOnMainDiag(A):
    return np.in1d(0, np.diagonal(A))


def findmatrix(maxits):
    k = 0
    while k < maxits:
        rand_matrix = np.random.random_integers(-1, 1, (3, 3))
        resultsDict = CreateC(rand_matrix)
        XC = resultsDict["Z"]
        XC = max(abs(XC))
        k = k + 1
        C = resultsDict["C"]
        CTRans = np.transpose(C)
        NewMatrix = np.dot(CTRans, C)
        XC = max(abs(np.linalg.eigvals(NewMatrix)))
        NormNewMtrix = np.linalg.norm(NewMatrix)
        # print(NormNewMtrix)
        # if XC >1: #For when looking for eigenvalues of a certain condition
        if isStrictlyDiagDom(rand_matrix) == 0 and hasZerosOnMainDiag(
                rand_matrix) == False and XC < 1:  # NormNewMtrix<1 and NormNewMtrix>0:
            print("K:", k)
            print("Ranrand_matrix:", rand_matrix)
            print("Eigenvalues:", np.linalg.eigvals(NewMatrix))
            break


# findmatrix(20000000)

def findsparsematrix(maxits):
    k = 0
    while k < maxits:
        Size = 1000
        k = k + 1
        A = sp.sparse.rand(Size, Size, density=0.1, format="lil")
        for i in range(Size):
            for j in range(Size):
                if A.A[i, j] > 0:
                    new_ran = random.randint(-1, 1)
                    A[i, j] = new_ran
                if i == j:
                    A[i, j] = Size

        print("K:", k)

        if isStrictlyDiagDom(A) == True:  # NormNewMtrix<1 and NormNewMtrix>0:
            print("K:", k)
            print("A:", A.A)

            text_file = open(os.path.join(dir, './tests/outfile.txt'), "w")

            # text_file = open("C:/Users/Eoghan/Documents/outfile.txt", "w")

            for i in range(Size):
                text_file.write("\n")
                for j in range(Size):
                    text_file.write(str(A.A[i, j]))
                    text_file.write(str(" "))

            text_file.write("\n")
            for i in range(Size):
                text_file.write(str(i + 1))
                text_file.write(str(" "))
            text_file.close()
            break


findsparsematrix(2000000)
