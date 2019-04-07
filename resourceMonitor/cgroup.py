import subprocess

# example input:cpu/app1
def get_group_pids(group):
    return subprocess.getoutput("sudo cat /sys/fs/cgroup/"+str(group)+"/cgroup.procs").strip().split()

def get_mem_consume(group):
    pass

#the group is like "app1"
def get_cfs_quota(group):
    return int(subprocess.getoutput("sudo cgget -r cpu.cfs_quota_us " + str(group)).strip().split()[2])
if __name__ == "__main__":
    print(get_group_pids(input("group:")))
