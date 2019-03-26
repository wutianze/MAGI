import subprocess
class llcManager:
    def __init__(self,numCOS):# numCOS doesn't have COS0
        self.freeLlc = 0xfffff
        self.cosLlc = {}
        self.cosPids = {}
        self.avaCOS = {}
        for i in range(numCOS):
            self.avaCOS.add(i)
    def findFreeLlc(self,num):


    def givePidNewCOS(self,llc):
        if len(self.avaCOS) == 0:
            print("No available COS")
        else:
            cos = self.avaCOS.pop()


    def recycleCOS(self,cos):
        if cos in self.cosLlc.keys():
            self.cosLlc



    # Sets all COS to default (fill into all ways) and associates all cores with COS 0
    def resetCAT(self):
        if subprocess.getstatusoutput('pqos -R') == 1:
            print("Err: resetCAT fail")

    # set COS i to the x cache ways
    # both pqos -e and pqos -I -e can be used
    # ex:"llc:1=0x000f;llc:2=0x0ff0"
    def allocCache(self,coses,llcs):
        cmd = "pqos -e \""
        for cos,llc in zip(coses,llcs):
            cmd += "llc:" + str(cos) + "=" + str(llc) + ";"
        cmd += "\""
        if subprocess.getstatusoutput(cmd) == 1:
            print("Err: allocCache Fail")

    def assoProcessCOS(self,pidss,coses):
        cmd = "pqos -I -a \""
        for cos,pids in zip(coses,pidss):
            cmd += "pid:" + str(cos) + "=" + str(pids) + ";"
        cmd += "\""
        if subprocess.getstatusoutput(cmd) == 1:
            print("Err:assoProcessCOS Fail")

        

if __name__ == '__main__':
    pass
