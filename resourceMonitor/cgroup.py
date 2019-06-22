import subprocess

#example input:cpu/app1, get all process(include tmp)

# the return value may contain temp processes
def get_group_pids(group):
    return subprocess.getoutput("sudo cat /sys/fs/cgroup/" + str(group) + "/cgroup.procs").strip().split()


# example input:cpu/app1, cmd is used to find the only process which can best represent the group
def get_group_pid(group, cmd):
    pids = subprocess.getoutput("sudo cat /sys/fs/cgroup/"+str(group)+"/cgroup.procs").strip().split()
    for p in pids:
        #print(subprocess.getoutput("ps -A |grep " + cmd).strip().split())
        psOut = subprocess.getoutput("ps -A |grep " + str(p))
        if psOut != None and str(psOut) != "":
            if str(psOut).strip().split()[-1] == str(cmd):
                return p

# the input should be like app1, may not used if pid takes over core
def get_group_core(group):
    toHandle = subprocess.getoutput("sudo cat /sys/fs/cgroup/cpuset/" + group + "/cpuset.cpus")
    if toHandle.find("-") == -1:
        return toHandle.split(',')
    print("Warning: get_group_core will return a string because it has -")
    return toHandle


def get_mem_consume(group):
    pass

#the group is like "app1"
def get_cfs_quota(group):
    return int(subprocess.getoutput("sudo cgget -r cpu.cfs_quota_us " + str(group)).strip().split()[2])
if __name__ == "__main__":
    print(get_group_pid(input("group:"), "run_"))
