import matplotlib.pyplot as plt
import numpy as np
import json
def normalize(X):
    x = np.array(X)
    mi = x.min()
    ma = x.max()
    if mi == ma:
        return x/ma
    return ((x - x.min())/(x.max() - x.min()))

def drawXY(X, Y):
    x = np.array(X)
    y = np.array(Y)
    plt.plot(x,y)
    plt.show()


def drawTimeY(Y):
    x = np.linspace(0,len(Y[0]),len(Y[0]))
    for y in Y:
        plt.plot(x, np.array(y))
    plt.show()

if __name__ == '__main__':
    #print(open("../data_cpu.txt",'r').read())
    Fi = json.loads(open("../data_for_plot.txt",'r').read())
    #y = [0.2,0.5,0.1,0,4,0,5,0,7,0,8,0,1]
    y = []
    y.append([float(i) for i in Fi["xapian"]["ipc"]])
    y.append([float(i) for i in Fi["mcf"]["ipc"]])
    drawTimeY(y)
    y.append(normalize([float(i) for i in Fi["xapian"]["llc"]]))
    y.append(normalize([float(i) for i in Fi["mcf"]["llc"]]))
    drawTimeY(y)
    y.append(normalize([float(i) for i in Fi["xapian"]["cpu"]]))
    y.append(normalize([float(i) for i in Fi["mcf"]["cpu"]]))
    drawTimeY(y)