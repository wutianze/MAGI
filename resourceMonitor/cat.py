import subprocess
import sys
sys.path.append("..")
import resourceMonitor as rM

def getCpuInfo(pid):
    return subprocess.getoutput('sudo pqos -t1 -I -p all:'+str(pid))

# cores like [0,1,2]
def getCoresLlc(cores):
    toHandle = subprocess.getoutput('sudo pqos -t 1 -m llc:' + ','.join([str(i) for i in cores])).strip().split('\n')
    res = {}

    for line in toHandle:
        con = line.split()
        if str(con[0]).isdigit():
            res[int(con[0])] = float(con[-1])
    return res

# cores like [0,1,2]
def getCoresMbl(cores):
    toHandle = subprocess.getoutput('sudo pqos -t 1 -m mbl:' + ','.join([str(i) for i in cores])).strip().split('\n')
    res = {}

    for line in toHandle:
        con = line.split()
        if str(con[0]).isdigit():
            res[int(con[0])] = float(con[-1])
    return res

# group is like app1
def getGroupsSumLlc(group):
    cores = rM.get_group_core(group)
    if isinstance(cores,str):
        return -1
    llcs = getCoresLlc(cores)
    res = 0.0
    for k in llcs.keys():
        res += float(llcs[k])
    return res

# group is like app1
def getGroupsSumMbl(group):
    cores = rM.get_group_core(group)
    if isinstance(cores,str):
        return -1
    mbls = getCoresMbl(cores)
    res = 0.0
    for k in mbls.keys():
        res += float(mbls[k])
    return res

'''
# groups are like ["cpu/app1","perf_event/app2"]
# ! better not use
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
# ! better not use 
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
'''

#find the most except ex, groups should be ["app1",..]
def findGroupConsumeMostLlc(groups,ex):
    res = ""
    mostLlc = 0.0
    for g in groups:
        if g == ex:
            continue
        tmp = getGroupsSumLlc(g)
        if tmp >= mostLlc:
            res = g
            mostLlc = tmp
    return res

#groups should be ["app1",...]
def findGroupConsumeMostMbl(groups,ex):
    res = ""
    mostMbl = 0.0
    for g in groups:
        if g == ex:
            continue
        tmp = getGroupsSumMbl(g)
        if tmp >= mostMbl:
            res = g
            mostMbl = tmp
    return res


if __name__ == '__main__':
    #grps = ["/cpu/app1","/cpu/app2"]
    #findGroupConsumeMostLlc(grps,"")
    getCoresMbl([3,4])
