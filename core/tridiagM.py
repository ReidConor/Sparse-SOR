#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 16:25:21 2016

@author: Carnec
"""
import numpy as np

def createSandT(SMax,T,k):
    # Smax is price so option value is zero #T is maturity
    Sn = 0
    tm = 0
    S = [Sn]
    t = [0]
    matrixsize = int(T/k)
    h = SMax/matrixsize
    for i in range(matrixsize):
        Sn = Sn + h
        S.append(Sn)
        tm = tm + k
        t.append(tm)
    return S, t

# abcArrays creates the 3 idagonals for tridiagonal matrix
def abcArrays(S,t,sigma,r):
    M = len(S)-1
    N = len(t)-1
    sigma2 = sigma ** 2  # sigma squared
    k = t[-1] / S[-1]  # dt #grid sizes (h and k)
    sigma2 = sigma ** 2  # sigma squared
    arrayaj = np.array([])
    arraybj = np.array([])
    arraycj = np.array([])

    for nbj in range(1, N+1):
        arraybj = np.append(arraybj, (1 + (k*r) + (k*sigma2*(nbj**2))))
    for naj in range(2, N+1): #bottom diag, n = from 2 to n-1
        arrayaj = np.append(arrayaj, (-(naj*k)/2)*(naj*sigma2-r))
    for ncj in range(1, N): #top diag, n = from 1 to n-2
        arraycj = np.append(arraycj, (-(ncj*k)/2)*(ncj*sigma2-r))
    return arrayaj, arraybj, arraycj
        
# tridiag function creates the tridiagonal matrix
def tridiag(a, b, c):
    k1 = -1
    k2 = 0
    k3 = 1
    return np.diag(a, k1) + np.diag(b, k2) + np.diag(c, k3)    
    
# function that creates vector b
# def vectorB(A):
#    b = np.zeros(A.shape[0])  
#    f1 = 

# Initialise vector of stock price and vector of times
# S, t = createSandT(50.0, 12, 1)  # Vector of stock price (grid points)
#
# a, b, c = abcArrays(S, t, 0.3, 0.02)  # a is the bottom diag, b is the centre diag, c is top diag
# A = tridiag(a, b, c)
# print(A)

