import subprocess
import cgroup
# Sets all COS to default (fill into all ways) and associates all cores with COS 0
def resetCAT():
    if subprocess.getstatusoutput('pqos -R') == 1:
        print('err')

def getCpuInfo(pid):
    return subprocess.getoutput('sudo pqos -I -p all:'+str(pid)]) 

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
        pids = cgroup.getCgroupPids(group)
        gP[group] = len(pids)
        pidsForJoin += pids

    forHandle = subprocess.getoutput('pqos -I -p mbl:' + str(','.join(pidsForJoin))).strip().split('\n')
    lineI = 1 #start from second line
    for group in groups:
        tmpSum = 0.0
        for i in range(int(gP[group])):
            values = forHandle[lineI].split(' ')
            tmpSum += float(values[?])
        gP[group] = tmpSum

    return gP

    	
getCpuInfo(6)
    
