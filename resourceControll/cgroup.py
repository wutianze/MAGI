#from cgroupspy import trees
import sys
sys.path.append("..")
import subprocess
import resourceMonitor as rM

# name is like "app1"
def createCgroup(subsystem,name):
    '''
    sS = trees.Tree().get_node_by_path('/'+str(subsystem)+'/')
    if sS.create_cgroup(name) is None:
        print('Err: Wrong Path:',str(subsystem)+str(name)+'/')
        '''
    if subprocess.getstatusoutput("sudo cgcreate -g " + subsystem + ":" + name)[0] != 0:
       print("Err: create cgroup")

# pids split by ' '
# path_to_cgroup is like "app1"
def addProcs(subsystem,path_to_cgroup,pid):
    '''
    if subprocess.getstatusoutput('echo '+str(proId)+' > /sys/fs/cgroup/'+str(path)+'/cgroup.procs') == 1:
        print('Err: Add Process Fail')
'''
    if subprocess.getstatusoutput("sudo cgclassify -g " + subsystem + ":" + path_to_cgroup + " " + str(pid)) [0] != 0:
        print("Err: Add Process Fail")


# path_to_cgroup is like "app1"
def startProcs(subsystem, path_to_cgroup, cmd):
    if subprocess.getstatusoutput("sudo cgexec -g " + subsystem + ":" + path_to_cgroup + " " + cmd)[0] != 0:
        print("Err: Start Process in cgroup Fail")

# group is like "app1"
def cfs_quotaSet(group,quota):
    if subprocess.getstatusoutput("sudo cgset -r cpu.cfs_quota_us=" + str(quota) + " " + group)[0] != 0:
        print("Err: quotaSet Fail")
        return -1
    return 0


#group is like "app1"
def cfs_periodSet(group,period):
    if subprocess.getstatusoutput("sudo cgset -r cpu.cfs_period_us=" + str(period) + " " + group)[0] != 0:
        print("Err: cpu_periodSet Fail")
        return -1
    return 0


# path_to_cgroup is like "app1"
def cpusSet(value,path_to_cgroup):
    if subprocess.getstatusoutput("sudo cgset -r cpuset.cpus=" + str(value) + path_to_cgroup)[0] != 0:
        print("Err:set cpus Fail")
        return -1
    return 0


# group is like "app1"
def cfs_quotaCut(group,percent):
    if cfs_quotaSet(group,int(float(rM.get_cfs_quota(group)) * float(percent))) == -1:
        return -1
    return 0

if __name__ == '__main__':
    #addProcs(input("pid:"),input("path"))
    #createCgroup(input('subsystem:'),input('name:'))
    #quotaSet(input("appName:"),input(" quota value:"))
    addProcs(input("subsystem:"),input("path_to_group:"),input("pid:"))
    #cpusSet(input("cpus:"),input("path_to_group:"))
