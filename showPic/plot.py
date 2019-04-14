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
    Fi["xapian"]["ipc"] = [float(i) for i in Fi["xapian"]["ipc"]]
    Fi["mcf"]["ipc"] = [float(i) for i in Fi["mcf"]["ipc"]]
    Fi["lbm"]["ipc"] = [float(i) for i in Fi["lbm"]["ipc"]]
    Fi["xapian"]["llc"] = [float(i) for i in Fi["xapian"]["llc"]]
    Fi["mcf"]["llc"] = [float(i) for i in Fi["mcf"]["llc"]]
    Fi["lbm"]["llc"] = [float(i) for i in Fi["lbm"]["llc"]]
    Fi["xapian"]["cpu"] = [float(i) for i in Fi["xapian"]["cpu"]]
    Fi["mcf"]["cpu"] = [float(i) for i in Fi["mcf"]["cpu"]]
    Fi["lbm"]["cpu"] = [float(i) for i in Fi["lbm"]["cpu"]]

    ll = len(Fi["xapian"]["ipc"])
    x = np.linspace(0, ll, ll)
    sla_xapian = []
    for i in range(ll):
        sla_xapian.append(0.21)

    plt.figure(1)
    plt.subplot(311)
    plt.grid(linestyle=':')
    plt.plot(x, Fi["xapian"]["ipc"], ">-", label="xapian")
    plt.plot(x, Fi["mcf"]["ipc"], ">-", label="mcf")
    plt.plot(x, Fi["lbm"]["ipc"], ">-", label="lbm")
    plt.plot(x, sla_xapian, "r-", label='SLA')
    plt.title("Performance of Apps")
    plt.xlabel("time")
    plt.ylabel("ipc")
    plt.legend(loc='best')

    plt.subplot(312)
    plt.grid(linestyle=':')
    plt.plot(x, Fi["xapian"]["llc"], ">-", label="xapian")
    plt.plot(x, Fi["mcf"]["llc"], ">-", label="mcf")
    plt.plot(x, Fi["lbm"]["llc"], ">-", label="lbm")
    plt.title("LLC of Apps")
    plt.xlabel("time")
    plt.ylabel("llc num")
    plt.legend(loc='best')

    plt.subplot(313)
    plt.grid(linestyle=':')
    plt.plot(x, Fi["xapian"]["cpu"], ">-", label="xapian")
    plt.plot(x, Fi["mcf"]["cpu"], ">-", label="mcf")
    plt.plot(x, Fi["lbm"]["cpu"], ">-", label="lbm")
    plt.title("Cpu of Apps")
    plt.xlabel("time")
    plt.ylabel("cpu quota")
    plt.legend(loc='best')
    '''
    plt.figure(1)
    plt.grid(linestyle=':')
    plt.plot(x,Fi["xapian"]["ipc"],">-",label="xapian")
    plt.plot(x,Fi["mcf"]["ipc"],">-",label="mcf")
    plt.plot(x,sla_xapian,"r-",label='SLA')
    plt.title("Performance of Apps")
    plt.xlabel("time")
    plt.ylabel("ipc")
    plt.legend(loc='best')

    plt.figure(2)
    plt.grid(linestyle=':')
    plt.plot(x, Fi["xapian"]["llc"], ">-",label="xapian")
    plt.plot(x, Fi["mcf"]["llc"], ">-",label="mcf")
    plt.title("LLC of Apps")
    plt.xlabel("time")
    plt.ylabel("llc num")
    plt.legend(loc='best')

    plt.figure(3)
    plt.grid(linestyle=':')
    plt.plot(x, Fi["xapian"]["ipc"], ">-",label="ipc")
    plt.plot(x, sla_xapian, label='SLA')
    plt.plot(x, normalize(Fi["xapian"]["llc"],0.4),">-", label="llc")
    plt.plot(x, normalize(Fi["xapian"]["cpu"],0.4), ">-",label="cpu")
    plt.title("Xapian")
    plt.xlabel("time")
    plt.ylabel("normalized data")
    plt.legend(loc='best')

    plt.figure(4)
    plt.grid(linestyle=':')
    plt.plot(x, Fi["mcf"]["ipc"], ">-",label="ipc")
    plt.plot(x, normalize(Fi["mcf"]["llc"],0.4), ">-",label="llc")
    plt.plot(x, normalize(Fi["mcf"]["cpu"],0.4), ">-",label="cpu")
    plt.title("Mcf")
    plt.xlabel("time")
    plt.ylabel("normalized data")
    plt.legend(loc='best')

    plt.figure(5)
    plt.grid(linestyle=':')
    plt.plot(x, Fi["xapian"]["ipc"], ">-",label="Fi["xapian"]["ipc"]")
    plt.plot(x, normalize(Fi["mcf"]["llc"],0.4), ">-",label="Fi["mcf"]["llc"]")
    plt.plot(x, sla_xapian, label='SLA')
    plt.plot(x, normalize(Fi["mcf"]["cpu"],0.4),">-", label='Fi["mcf"]["cpu"]')
    plt.title("Xapian\'s SLA with mcf resource")
    plt.xlabel("time")
    plt.ylabel("normalized data")
    plt.legend(loc='best')
'''
    plt.subplots_adjust(hspace=0.4)
    plt.show()
