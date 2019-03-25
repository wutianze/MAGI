import subprocess

toplevPath = "/home/sauron/MAGI/pmu-tools/toplev.py "
def topDownGroup(group):
    cmd = toplevPath + "-l1 -x'|' --no-desc --quiet -G " + str(group) + " sleep 5"
    toHandle = subprocess.getoutput(cmd).strip().split('\n')
    res = {}
    for line in toHandle:
        if(line[0] == 'C'):
            lineS = line.split('|')
            print(lineS)
            if lineS[0] in res.keys():
                if float(lineS[7]) != 100 and res[lineS[0]][1] < float(lineS[2]):# 100 means the percent of time counter used,if 100 we ignore it because the app may not run on that CPU
                    res[lineS[0]] = (lineS[1],float(lineS[2]))
            else:
                res[lineS[0]] = (lineS[1],float(lineS[2]))
    return res

def topDownPid(pid):
    cmd = toplevPath + "-l1 -x'|' -S --no-desc -p " + str(pid) + " --quiet sleep 3"
    toHandle = subprocess.getoutput(cmd)
    return toHandle
if __name__ == "__main__":
    print(topDownGroup(input("group:")))
    #print(topDownPid(input("pid:")))

