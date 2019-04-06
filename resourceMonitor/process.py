import psutil
import time
import resourceMonitor.cgroup as cg

# group is like "cpu/app1"
def getGroupStart(group):
    pids = cg.get_group_pids(group)
    res = time.time()
    for p in pids:
        try:
            tmp = psutil.Process(p).create_time()
            if tmp < res:
                res = tmp
        except:
            continue
    return res

# get the group which co-located with aim for the most of time
# group is like "cpu/app1", allG should be ["cpu/app1", "cpu/perf_event"]
def getCoGroup(group,allG):
    aimS = getGroupStart(group)
    leastGap = time.time()
    res = allG[0]
    for g in allG:
        if g != group:
            tmpS = getGroupStart(g)
            if abs(tmpS - aimS) < leastGap:
                leastGap = tmpS
                res = g
    return res

if __name__ == '__main__':

    a = psutil.Process(1236).create_time()
    print(a)
