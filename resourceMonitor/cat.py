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
        pid = rM.cgroup.get_group_pid(group, "run_" + group.split('/')[-1])
        pidsForJoin.append(pid)

    forHandle = subprocess.getoutput('sudo pqos -t 1 -I -p mbl:' + str(','.join(pidsForJoin))).strip().split('\n')
    lineI = 6 + len(pidsForJoin)  #start from second line
    for group in groups:
        values = forHandle[lineI].split()
        gP[group] = float(values[4])  # TODO values[?]
        lineI += 1

    return gP

# groups are like ["cpu/app1","perf_event/app2"]
def getCgroupsLlc(groups):
    gP = {}
    pidsForJoin = []
    for group in groups:
        pid = rM.cgroup.get_group_pid(group, "run_" + group.split('/')[-1])
        pidsForJoin.append(pid)

    forHandle = subprocess.getoutput('sudo pqos -t 1 -I -p llc:' + str(','.join(pidsForJoin))).strip().split('\n')
    #print(forHandle)
    lineI = 6 + len(pidsForJoin) #start from second line
    for group in groups:
        values = forHandle[lineI].split()
        gP[group] = float(values[2])
        lineI += 1
    return gP


#find the most except ex, groups should be ["cpu/app1",..]
def findGroupConsumeMostLlc(groups,ex):
    data = getCgroupsLlc(groups)
    res = ""
    mostL = 0.0
    for key in data.keys():
        if data[key] >= mostL and key != ex:
            mostL = data[key]
            res = key
    return res

#groups should be ["cpu/app1",...]
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
