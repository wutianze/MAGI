#from cgroupspy import trees
import subprocess

def createCgroup(subsystem,name):
    '''
    sS = trees.Tree().get_node_by_path('/'+str(subsystem)+'/')
    if sS.create_cgroup(name) is None:
        print('Err: Wrong Path:',str(subsystem)+str(name)+'/')
        '''
    if subprocess.getstatusoutput("cgcreate -g " + subsystem + ":" + "name") == 1:
        print("Err: create cgroup")

def addProcs(subsystem,path_to_cgroup,pid):
    '''
    if subprocess.getstatusoutput('echo '+str(proId)+' > /sys/fs/cgroup/'+str(path)+'/cgroup.procs') == 1:
        print('Err: Add Process Fail')
'''
    if subprocess.getstatusoutput("cgclassify -g " + subsystem + ":" + path_to_cgroup + str(pid)) == 1:
        print("Err: Add Process Fail")

def startProcs(subprocess,path_to_cgroup,cmd):
    if subprocess.getstatusoutput("cgexec -g " + subsystems + ":" + path_to_cgroup + cmd) == 1:
        print("Err: Start Process in cgroup Fail")
#def quotaSet(name,quota):
    '''
    t = trees.Tree()
    app = t.get_node_by_path('/cpu/'+str(name)+'/')
    if app is None:
        print('Err: Wrong Path:','/cpu/'+str(name)+'/')
        return
    app.controller.cfs_quota_us = int(quota)
'''
    
def cpusSet(value,path_to_cgroup):
    if subprocess.getstatusoutput("cgset -r cpuset.cpus=" + str(value) + path_to_cgroup) == 1:
        print("Err:set cpus Fail")
if __name__ == '__main__':
    #addProcs(input("pid:"),input("path"))
    #createCgroup(input('subsystem:'),input('name:'))
    #quotaSet(input("appName:"),input(" quota value:"))
    addProcs(input("subsystem:"),input("path_to_group:"),input("pid:"))
    cpusSet(input("cpus:"),input("path_to_group:"))
