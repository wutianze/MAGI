import subprocess

avaTar = ["instructions","cycles","cpu/event=0xd0,umask=0x83/","cache-misses","cpu/event=0xd0,umask=0x21/","cpu/event=0xc7,umask=3/","cpu/event=0xc4,umask=0x0/","cpu/event=0xd1,umask=0x8/","cpu/event=0xd1,umask=0x10/","cpu/event=0xa2,umask=0x8/","cpu/event=0xc5,umask=0x4/","cpu/event=0xc3,umask=0x1/",\
          "cpu/event=0x9c,umask=0x01/","cpu/event=0x0e,umask=0x01/","cpu/event=0xc2,umask=0x02/","cpu/event=0x0d,umask=0x03/"]
perfPath = 'perf'
fromEvent = {
        "cpu/event=0xd0,umask=0x83/" : "loads_and_stores",
        "cpu/event=0x0e,umask=0x01/" : "uops_issued.any",
        "cpu/event=0x9c,umask=0x01/" : "idq_uops_not_delivered.core", 
        "cpu/event=0xc2,umask=0x02/" : "uops_retired.retire_slots", 
        "cpu/event=0x0d,umask=0x03/" : "int_misc.recovery_cycles",
        "cpu/event=0xc7,umask=3/" : "fp_uops",
        "cpu/event=0xc4,umask=0x0/" : "branch",
        "cpu/event=0xd0,umask=0x21/" : "lock_loads",
        "cpu/event=0xd1,umask=0x8/" : "l1_misses",
        "cpu/event=0xd1,umask=0x10/" : "l2_misses",
        "cpu/event=0xa2,umask=0x8/" : "stall_sb",
        "cpu/event=0xc5,umask=0x4/" : "branch_misp",
        "cpu/event=0xc3,umask=0x1/" : "machine_clear"
}
toEvent = {
     "loads_and_stores":"cpu/event=0xd0,umask=0x83/",
     "uops_issued.any": "cpu/event=0x0e,umask=0x01/",
     "idq_uops_not_delivered.core":"cpu/event=0x9c,umask=0x01/",
     "uops_retired.retire_slots":"cpu/event=0xc2,umask=0x02/",
     "int_misc.recovery_cycles":"cpu/event=0x0d,umask=0x03/",
    "fp_uops":        "cpu/event=0xc7,umask=3/",
    "branch":           "cpu/event=0xc4,umask=0x0/" ,
     "lock_loads":      "cpu/event=0xd0,umask=0x21/",
    "l1_misses":      "cpu/event=0xd1,umask=0x8/" ,
     "l2_misses":       "cpu/event=0xd1,umask=0x10/",
    "stall_sb":       "cpu/event=0xa2,umask=0x8/" ,
    "branch_misp":      "cpu/event=0xc5,umask=0x4/", 
    "machine_clear":     "cpu/event=0xc3,umask=0x1/" 
}

'''
def getInfoList(configs,time):
    cmd_str = perfPath + " stat -a -x'|'"  # need to add -A ?
    for (event_name, group) in configs:
        cmd_str += " -e " + event_name + " -G " + group
    cmd_str += " -- sleep " + str(time)
    forHandle =  subprocess.getoutput(cmd_str).strip().split('\n')
    res = []
    index = 0
    for (event_name,group) in configs:
        lineCon = forHandle[index].split('|')
        res.append((group,event_name,lineCon[0]))
        index = index + 1
    return res
    #return subprocess.getoutput(cmd_str).strip().split()
    '''
def getInfo(group, sample_len):
    #print("getAllInfo start")
    cmd_str = "sudo " + perfPath + " stat -a -x'|'"
    #cmd_str += " -e "
    for event in avaTar:
        cmd_str += " -e " + event + " -G " + group 
    #cmd_str += ','.join(avaTar)
    #cmd_str += " -G " + group
    #print(cmd_str)
    forHandle = subprocess.getoutput(cmd_str + " sleep " + str(sample_len)).strip().split('\n')
    #print(forHandle)
    index = 0
    ipc = 0
    groupData = {}
    for event in avaTar:
        if event in fromEvent.keys():
            event = fromEvent[event]
        val = forHandle[index].strip().split('|')[0]
        if val == "<not counted>":  # if the app is not running, events like instructions may be not counted
            # val = 1.0
            return None
        if event == "instructions":
            ipc = forHandle[index].strip().split('|')[6]
        index = index + 1
        try:
            groupData[event] = float(val)
        except:
            print("change float fail:" + str(val))
            return None
    groupData["ipc"] = ipc
    return groupData


# groups is like ["app1","app2"]
def getAllInfo(groups, sample_len):
    res = {}
    for group in groups:
        tmpI = getInfo(group, sample_len)
        if  tmpI == None:
            return None
        res[group] = tmpI
    return res

if __name__ == '__main__':
    #tu = ("branch","app1")
    #tu2 = ("cpu-clock","app1")
    #li = [tu,tu2]
    print("start test")
    groups = ["app1"]
    print(getAllInfo(groups,2))
