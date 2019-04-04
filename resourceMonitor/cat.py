import subprocess
import sys
sys.path.append("..")
import resourceMonitor as rM

def getCpuInfo(pid):
    return subprocess.getoutput('sudo pqos -I -p all:'+str(pid))


def getIpc(pid):
    return 0.3


# get mem-bw of a single process
def getPidMbw(pid):
    forHandle = subprocess.getoutput('pqos -I -p mbl:' + str(pid)).strip()
    return 2.2


def getCgroupsMbw(groups):
    gP = {}
    pidsForJoin = []
    for group in groups:
        pids = rM.cgroup.get_group_pids(group)
        gP[group] = len(pids)
        pidsForJoin += pids

    forHandle = subprocess.getoutput('pqos -I -p mbl:' + str(','.join(pidsForJoin))).strip().split('\n')
    lineI = 1 #start from second line
    for group in groups:
        tmpSum = 0.0
        for i in range(int(gP[group])):
            values = forHandle[lineI].split(' ')
            tmpSum += float(values[0])# TODO values[?]
        gP[group] = tmpSum

    return gP


def getCgroupsLlc(groups):
    gP = {}
    pidsForJoin = []
    for group in groups:
        pids = rM.cgroup.get_group_pids(group)
        gP[group] = len(pids)
        pidsForJoin += pids

    forHandle = subprocess.getoutput('pqos -I -p llc:' + str(','.join(pidsForJoin))).strip().split('\n')
    lineI = 1 #start from second line
    for group in groups:
        tmpSum = 0.0
        for i in range(int(gP[group])):
            values = forHandle[lineI].split(' ')
            tmpSum += float(values[0])# TODO values[?]
        gP[group] = tmpSum
    return gP


#find the most except ex
def findGroupConsumeMostLlc(groups,ex):
    data = getCgroupsLlc(groups)
    res = ""
    mostL = 0.0
    for key in data.keys():
        if data[key] > mostL and key != ex:
            mostL = data[key]
            res = key
    return res


def findGroupConsumeMostMbw(groups,ex):
    data = getCgroupsMbw(groups)
    res = ""
    mostL = 0.0
    for key in data.keys():
        if data[key] > mostL and key != ex:
            mostL = data[key]
            res = key
    return res


if __name__ == '__main__':
    pass
    
