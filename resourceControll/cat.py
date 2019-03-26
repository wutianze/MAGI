import subprocess

ALLLLC = 0xfffff
FORCHECK = 0x80000
TOTALLLC = 20
# the manager is not thread safe !!
class llcManager:
    def __init__(self,numCOS):# numCOS doesn't have COS0,COS0 should keep at least 2 cache,and COS0's own caches are always remain in the left like: 0xc0000
        self.freeLlc = ALLLLC
        self.cosLlc[0] = ALLLLC
        self.avaCOS = set()
        for i in range(numCOS):
            self.avaCOS.add(i+1)
    def findFreeLlc(self,num):
        llc = 0
        for i in range(num):
            llc += 2^i
        for i in range(TOTALLLC - 2):# because there are 2 caches for COS0
            if (self.freeLlc >> i) | llc == llc:
                return llc << i
        print("No enough excessive free llc")#may do a clear up
        return -1 # mean wrong

    def givePidSepLlc(self,num,pids):
        if len(self.avaCOS) == 0:
            print("No available COS")
            return -1
        else:
            cos = self.avaCOS.pop()
            toAss = [pids]
            if self.assoProcessCOS(toAss,cos) == -1:
                self.avaCOS.add(cos)
                return -1
            llcs = self.findFreeLlc(num)
            if llcs == -1:
                print("Find free llc fail")
                return -1
            llclist = [str(hex(llcs))]
            coslist = [cos]
            if self.allocCache(coslist,llclist) == -1:
                self.avaCOS.add(cos)
                return -1
            self.freeLlc = self.freeLlc ^ llcs
            self.cosLlc[cos] = llcs
            return 0

    # recycleCOS should be invoked after the pid moved to another COS or it just finishes
    # will recycle llc from left
    def recycleCOS(self,cos,num):# num can be all
        if str(num) == "all":
            coslist = [cos]
            if self.allocCache(coslist,str(ALLLLC)) == -1:
                return -1
            self.freeLlc = self.freeLlc | self.cosLlc[cos]
            self.cosLlc[cos] = ALLLLC
            toC = self.freeLlc ^ self.cosLlc[0]






    # Sets all COS to default (fill into all ways) and associates all cores with COS 0
    def resetCAT(self,numCOS):
        if subprocess.getstatusoutput('pqos -R') == 1:
            print("Err: resetCAT fail")
        self.freeLlc = ALLLLC
        self.cosLlc = {}
        self.avaCOS = {}
        for i in range(numCOS):
            self.avaCOS.add(i)

    # set COS i to the x cache ways
    # both pqos -e and pqos -I -e can be used,llcs must be str !!
    # ex:"llc:1=0x000f;llc:2=0x0ff0"
    def allocCache(self,coses,llcs):
        cmd = "pqos -e \""
        for cos,llc in zip(coses,llcs):
            cmd += "llc:" + str(cos) + "=" + str(llc) + ";"
        cmd += "\""
        if subprocess.getstatusoutput(cmd) == 1:
            print("Err: allocCache Fail")
            return -1
        return 0

    def assoProcessCOS(self,pidss,coses):
        cmd = "pqos -I -a \""
        for cos,pids in zip(coses,pidss):
            cmd += "pid:" + str(cos) + "=" + str(pids) + ";"
        cmd += "\""
        if subprocess.getstatusoutput(cmd) == 1:
            print("Err:assoProcessCOS Fail")
            return -1
        return 0

        

if __name__ == '__main__':
    pass
