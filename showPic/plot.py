import matplotlib.pyplot as plt
import numpy as np
import json

def drawXY(X, Y):
    x = np.array(X)
    y = np.array(Y)
    plt.plot(x,y)
    plt.show()


def drawTimeY(Y):
    x = np.linspace(0,len(Y),len(Y))
    plt.plot(x, np.array(Y))
    plt.show()

if __name__ == '__main__':
    #print(open("../data_cpu.txt",'r').read())
    y = json.loads(open("../data_ipc.txt",'r').read())["xapian"]

    drawTimeY(y)