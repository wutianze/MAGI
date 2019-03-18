import subprocess

# Sets all COS to default (fill into all ways) and associates all cores with COS 0
def resetCAT():
    subprocess.run(['pqos','-R'])

def getCpuInfo(pid):
    subprocess.run(['sudo','pqos','-I','-p','all:'+str(pid)]) 
	
getCpuInfo(6)
    
