import subprocess

# example input:cpu/app1, cmd is used to find the only process which can best represent the group
def get_group_pid(group, cmd):
    pids = subprocess.getoutput("sudo cat /sys/fs/cgroup/"+str(group)+"/cgroup.procs").strip().split()
    for p in pids:
        #print(subprocess.getoutput("ps -A |grep " + cmd).strip().split())
        psOut = subprocess.getoutput("ps -A |grep " + str(p))
        if psOut != None and str(psOut) != "":
            if str(psOut).strip().split()[-1] == str(cmd):
                return p

def get_mem_consume(group):
    pass

#the group is like "app1"
def get_cfs_quota(group):
    return int(subprocess.getoutput("sudo cgget -r cpu.cfs_quota_us " + str(group)).strip().split()[2])
if __name__ == "__main__":
    print(get_group_pid(input("group:"), "run_"))
