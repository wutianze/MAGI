from cgroupspy import trees
import subprocess

def createCgroup(subsystem,name):
    sS = trees.Tree().get_node_by_path('/'+str(subsystem)+'/')
    if sS.create_cgroup(name) is None:
        print('Err: Wrong Path:',str(subsystem)+str(name)+'/')

def addProcs(proId,path):
    if subprocess.getstatusoutput('echo '+str(proId)+' > /sys/fs/cgroup/'+str(path)+'/cgroup.procs') == 1:
        print('Err: Add Process Fail')

def quotaC(name,quota):
    t = trees.Tree()
    app = t.get_node_by_path('/cpu/'+str(name)+'/')
    if app is None:
        print('Err: Wrong Path:','/cpu/'+str(name)+'/')
        return
    app.controller.cfs_quota_us = int(quota)

if __name__ == '__main__':
    #addProcs(input("pid:"),input("path"))
    createCgroup(input('subsystem:'),input('name:'))
    #quotaC(input("appName:"),input(" quota value:"))
    addProcs(input("pid:"),input("path"))
