import subprocess

toplevPath = "/home/sauron/MAGI/pmu-tools/toplev.py "

def topDownGroupCal(currentInfo):
    if currentInfo["cycles"] <= 0 :
        print("Err: cycles = 0")
        return ""
    bounds = {}
    bounds["Frontend_Bound"] = currentInfo["idq_uops_not_delivered.core"] / (4 * currentInfo["cycles"])
    bounds["Bad_Speculation"] = (currentInfo["uops_issued.any"] - currentInfo["uops_retired.retire_slots"] + 4 * currentInfo["int_misc.recovery_cycles"]) / (4 * currentInfo["cycles"])
    bounds["Retiring"] = currentInfo["uops_retired.retire_slots"] / (4 * currentInfo["cycles"])
    bounds["Backend_Bound "] = 1 - bounds["Frontend_Bound"] - bounds["Bad_Speculation"] - bounds["Retiring"]
    return max(bounds, key=bounds.get)
    #return boundName
    #return "Backend_Bound"

def topDownGroup(group):
    cmd = "sudo " + toplevPath + "-l1 -x'|' --no-desc --quiet -G " + str(group) + " sleep 2"
    toHandle = subprocess.getoutput(cmd).strip().split('\n')
    res = {}
    for line in toHandle:
        if(line[0] == 'S'): #!! need to adapt to differnt machines
            lineS = line.split('|')
            #print(lineS)
            if lineS[0] in res.keys():
                if float(lineS[7]) != 100 and res[lineS[0]][1] < float(lineS[2]):# 100 means the percent of time counter used,if 100 we ignore it because the app may not run on that CPU
                    res[lineS[0]] = (lineS[1],float(lineS[2]))
            else:
                if float(lineS[7]) - 100 > -5:
                    continue
                res[lineS[0]] = (lineS[1],float(lineS[2]))
    maxB = 0
    boundName = ""
    for cpus in res.keys():
        if res[cpus][1] >= maxB:
            maxB = res[cpus][1]
            boundName = res[cpus][0]
    # here boundName may be "", I think it means the pmu cannot find the bound so the rule model can do nothing
    return boundName

def topDownPid(pid):
    cmd = toplevPath + "-l1 -x'|' -S --no-desc -p " + str(pid) + " --quiet sleep 3"
    toHandle = subprocess.getoutput(cmd)
    return toHandle
if __name__ == "__main__":
    print(topDownGroup(input("group:")))#ex :app1
    #print(topDownPid(input("pid:")))

