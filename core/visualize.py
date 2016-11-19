import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

def genHeatMap(A, path):
    fig, ax = plt.subplots()
    ax.pcolor(np.array(A), cmap=plt.cm.Blues)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    plt.savefig(path)

def genBSMPlot(S,t,pastfnm):
    pastfnmarray = list(pastfnm.values())
    for i in range(len(pastfnmarray)):
        plt.plot(S, pastfnmarray[i])
        plt.title("European Put Option Prices vs Stock Prices")
        plt.ylabel("European Put Option Prices")
        plt.xlabel("Stock Price")

    pastfnmarray = list(pastfnm.values())
    pastfnmarray = np.matrix(pastfnmarray)
    t = np.array(t)
    t = t.astype(float)
    S, t = np.meshgrid(S, t)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(S, t, pastfnmarray, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    ax.set_xlabel('Stock Price')
    ax.set_ylabel('t')
    ax.set_zlabel('Put Option Price')

    plt.show()
