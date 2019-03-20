import subprocess

# example input:cpu/app1
def getCgroupPids(group):
    return subprocess.getoutput("cat /sys/fs/cgroup/"+str(group)+"/cgroup.procs").strip().split()

if __name__ == "__main__":
    print(getCgroupPids(input("group:")))
