#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 16:25:21 2016

@author: Carnec
"""
import os
import sys
import numpy as np
from scipy import sparse
from core.doMath import *


def createSandT(S0, SMax, T, k):  # Smax is price so option value is zero #T is maturity
    tm = 0
    S = [S0]
    t = [0]
    matrixsize = int(T / k)
    h = SMax / (T)
    for i in range(matrixsize):
        S0 = S0 + h
        S.append(S0)
        tm = tm + k
        t.append(tm)
    return S, t, matrixsize, h


# abcArrays creates the 3 idagonals for tridiagonal matrix
def abcArrays(S, t, sigma, r):
    M = len(S)
    N = len(t)
    sigma2 = sigma ** 2  # sigma squared
    k = t[-1] / S[-1]  # dt #grid sizes (h and k)
    sigma2 = sigma ** 2  # sigma squared
    arrayaj = np.array([])
    arraybj = np.array([])
    arraycj = np.array([])

    for nbj in range(1, N + 1):
        arraybj = np.append(arraybj, (1 + (k * r) + (k * sigma2 * (nbj ** 2))))
    for naj in range(2, N + 1):  # bottom diag, n = from 2 to n-1
        arrayaj = np.append(arrayaj, (-(naj * k) / 2) * (naj * sigma2 - r))
    for ncj in range(1, N):  # top diag, n = from 1 to n-2
        arraycj = np.append(arraycj, (-(ncj * k) / 2) * (ncj * sigma2 - r))
    return arrayaj, arraybj, arraycj


# tridiag function creates the tridiagonal matrix
def tridiag(a, b, c):
    k1 = -1
    k2 = 0
    k3 = 1
    return np.diag(a, k1) + np.diag(b, k2) + np.diag(c, k3)


# function that creates vector b
def vectorB(X, S, h):
    f0m = X
    fNm = 0
    fnm = np.zeros(len(S))
    for i in range(len(fnm)):
        f = 0
        f = max([(X - (i * h)), 0])  # returns values greater or equal to zero (cant have neg option price)
        fnm[i] = f
    return fnm


def findPastOptionPrices(A, fNM, n, maxits, omega, x, error, T, k):
    M = int(T / k)
    fnmDict = {}
    for i in range(M - 1, -1, -k):
        x = Sparse_SOR(A, fNM, n, maxits, omega, x, error)
        fnmDict[i] = x
        fNM = x
        x = np.zeros(n)
    return fnmDict