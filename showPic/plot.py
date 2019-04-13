import matplotlib.pyplot as plt
import numpy as np
import json
def normalize(X, up):
    x = np.array(X)
    mi = x.min()
    ma = x.max()
    if mi == ma:
        return (x/ma)*up
    return ((x - mi)/(ma - mi))*up

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
    dataF = open("../data_for_plot.txt",'r')
    Fi = json.loads(dataF.read())
    dataF.close()
    xapian_ipc = [float(i) for i in Fi["xapian"]["ipc"]]
    mcf_ipc = [float(i) for i in Fi["mcf"]["ipc"]]
    xapian_llc = [float(i) for i in Fi["xapian"]["llc"]]
    mcf_llc = [float(i) for i in Fi["mcf"]["llc"]]
    xapian_cpu = [float(i) for i in Fi["xapian"]["cpu"]]
    mcf_cpu = [float(i) for i in Fi["mcf"]["cpu"]]

    ll = len(xapian_ipc)
    x = np.linspace(0, ll, ll)
    sla_xapian = []
    for i in range(ll):
        sla_xapian.append(0.27)


    plt.figure(1)
    plt.plot(x,xapian_ipc,label="xapian")
    plt.plot(x,mcf_ipc,label="mcf")
    plt.plot(x,sla_xapian,label='SLA')
    plt.title("Performance of Apps")
    plt.xlabel("time")
    plt.ylabel("ipc")
    plt.legend()

    plt.figure(2)
    plt.plot(x, xapian_llc, label="xapian")
    plt.plot(x, mcf_llc, label="mcf")
    plt.title("LLC of Apps")
    plt.xlabel("time")
    plt.ylabel("llc num")
    plt.legend()

    plt.figure(3)
    plt.plot(x, xapian_ipc, label="ipc")
    plt.plot(x, sla_xapian, label='SLA')
    plt.plot(x, normalize(xapian_llc,0.4), label="llc")
    plt.plot(x, normalize(xapian_cpu,0.4), label="cpu")
    plt.title("Xapian")
    plt.xlabel("time")
    plt.ylabel("normalized data")
    plt.legend()

    plt.figure(4)
    plt.plot(x, normalize(mcf_ipc,0.4), label="ipc")
    plt.plot(x, normalize(mcf_llc,0.4), label="llc")
    plt.plot(x, normalize(mcf_cpu,0.4), label="cpu")
    plt.title("Mcf")
    plt.xlabel("time")
    plt.ylabel("normalized data")
    plt.legend()

    plt.figure(5)
    plt.plot(x, xapian_ipc, label="xapian_ipc")
    plt.plot(x, normalize(mcf_llc,0.4), label="mcf_llc")
    plt.plot(x, sla_xapian, label='SLA')
    plt.plot(x, normalize(mcf_cpu,0.4), label='mcf_cpu')
    plt.title("Xapian\'s SLA with mcf resource")
    plt.xlabel("time")
    plt.ylabel("normalized data")
    plt.legend()

    plt.show()
