import subprocess
import sys
sys.path.append("..")
import resourceMonitor as rM

def getCpuInfo(pid):
    return subprocess.getoutput('sudo pqos -t1 -I -p all:'+str(pid))


def getIpc(pid):
    return 0.3


# get mem-bw of a single process
def getPidMbw(pid):
    forHandle = subprocess.getoutput('sudo pqos -t 1 -I -p mbl:' + str(pid)).strip()
    return 2.2

# groups are like ["cpu/app1","perf_event/app2"]
def getCgroupsMbw(groups):
    gP = {}
    pidsForJoin = []
    for group in groups:
        pids = rM.cgroup.get_group_pids(group)
        gP[group] = len(pids)
        pidsForJoin += pids

    forHandle = subprocess.getoutput('sudo pqos -t 1 -I -p mbl:' + str(','.join(pidsForJoin))).strip().split('\n')
    lineI = 6 + len(pidsForJoin)  #start from second line
    for group in groups:
        tmpSum = 0.0
        for i in range(int(gP[group])):
            values = forHandle[lineI].split()
            tmpSum += float(values[4])# TODO values[?]
            lineI += 1
        gP[group] = tmpSum

    return gP

# groups are like ["cpu/app1","perf_event/app2"]
def getCgroupsLlc(groups):
    gP = {}
    pidsForJoin = []
    for group in groups:
        pids = rM.cgroup.get_group_pids(group)
        gP[group] = len(pids)
        pidsForJoin += pids

    forHandle = subprocess.getoutput('sudo pqos -t 1 -I -p llc:' + str(','.join(pidsForJoin))).strip().split('\n')
    #print(forHandle)
    lineI = 6 + len(pidsForJoin) #start from second line
    for group in groups:
        tmpSum = 0.0
        for i in range(int(gP[group])):
            values = forHandle[lineI].split()
            tmpSum += float(values[2])
            lineI += 1
        gP[group] = tmpSum
    return gP


#find the most except ex
def findGroupConsumeMostLlc(groups,ex):
    data = getCgroupsLlc(groups)
    res = ""
    mostL = 0.0
    for key in data.keys():
        if data[key] >= mostL and key != ex:
            mostL = data[key]
            res = key
    return res


def findGroupConsumeMostMbw(groups,ex):
    data = getCgroupsMbw(groups)
    res = ""
    mostL = 0.0
    for key in data.keys():
        if data[key] >= mostL and key != ex:
            mostL = data[key]
            res = key
    return res


if __name__ == '__main__':
    grps = ["/cpu/app1","/cpu/app2"]
    findGroupConsumeMostLlc(grps,"")
