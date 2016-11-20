import os
import sys
import numpy as np
from scipy import sparse

from core.doMath import *
from core.doMath import Sparse_SOR
from core.fileIO import *

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt


def createSandT(S0, SMax, T, M, k):  # Smax is price so option value is zero #T is maturity
    tm = 0
    S = [S0]
    t = [0]
    matrixsize = int(T / k)
    h = SMax / (M)
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
    fnmDict[M] = fNM
    for i in range(M-1, -1, -1):
        resultsDict = Sparse_SOR(A, fNM, n, maxits, omega, x, error)
        x = resultsDict["x"]
        fnmDict[i] = x
        fNM = x
        x = np.zeros(n)
    return fnmDict

def runBSM(outputLogFile):
    # General parameters
    S0 = 0
    SMax = 150
    T = 12
    M = 40
    k = T / M
    X = 100

    # Parameters for SOR_Sparse
    sigma = 0.3
    r = 0.02
    maxits = 100
    omega = 1.5
    error = 0.0005

    S, t, matrixsize, h = createSandT(S0, SMax, T, M, k)  # Vector of stock price (grid points)
    fnM = vectorB(X, S, h)  # bvec gives fn,m or the option prices at time T.
    a, b, c = abcArrays(S, t, sigma, r)  # a is the bottom diag, b is the centre diag, c is top diag
    A = sparse.csr_matrix(tridiag(a, b, c))
    n = A.shape[1]
    x = np.zeros(n)

    pastfnm = findPastOptionPrices(A, fnM, n, maxits, omega, x, error, T, k)
    target = open(outputLogFile, 'w')


    target.write('Approximation of Option Prices at T+1 : %s' % fnM)
    target.write('')
    for i in range(len(pastfnm) - 1, -1, -1):
        target.write('f_{n, %s } = %s' % (i, pastfnm[i]))
        target.write('\n \n')


    ''' 3D PLOT'''
    genBSMPlot(S, t, pastfnm)