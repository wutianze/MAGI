import subprocess

# Sets all COS to default (fill into all ways) and associates all cores with COS 0
def resetCAT():
    if subprocess.getstatusoutput('pqos -R') == 1:
        print('err')

def getCpuInfo(pid):
    return subprocess.getoutput('sudo pqos -I -p all:'+str(pid)]) 

def getIpc(pic):
    return 0.3
    	
getCpuInfo(6)
    
