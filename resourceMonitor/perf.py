import subprocess


perfPath = '/home/sauron/perf'
fromEvent = {
        "cpu/event=0xd0,umask=0x83/" : "loads-and-stores",
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
     "loads-and-stores":"cpu/event=0xd0,umask=0x83/",
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

#return : [(group,event,count),...]
def getInfoList(configs):
    cmd_str = perfPath + " stat -a -x'|'"  # need to add -A ?
    for (event_name, group) in configs:
        cmd_str += " -e " + event_name + " -G " + group
    cmd_str += " -- sleep 2"
    forHandle =  subprocess.getoutput(cmd_str).strip().split('\n')
    res = []
    index = 0
    for (event_name,group) in configs:
        lineCon = forHandle[index].split('|')
        res.append((group,event_name,lineCon[0]))
        index = index + 1
    return res
    #return subprocess.getoutput(cmd_str).strip().split()

if __name__ == '__main__':
    tu = ("branch","app1")
    tu2 = ("cpu-clock","app1")
    li = [tu,tu2]
    print(getInfoList(li))
