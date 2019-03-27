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

    def cosLlcNum(self,cos):
        llcs = 0x0
        res = 0
        if cos == -1:# count free num,COS0 has at least 2 cache
            llcs = self.freeLlc
            res -= 2
        else:
            llcs = self.cosLlc[cos]

        for i in range(TOTALLLC):
            if llcs >> i & 1 == 1:
                res += 1
        return res

    def findFreeLlc(self,num):
        if num > self.cosLlcNum(-1):
            print("No enough free llc")
            return -1
        llc = 0
        for i in range(num):
            llc += 2 ^ i
        for i in range(TOTALLLC - 2):# because there are 2 caches for COS0
            if (self.freeLlc >> i) & llc == llc:
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
            if self.allocCache([cos],[str(hex(llcs))]) == -1:
                self.avaCOS.add(cos)
                return -1
            return cos

    def tryCombineFreeCOS0(self):
        cos0End = TOTALLLC - 1
        while cos0End >= 0:
            if self.cosLlc[0] >> cos0End & 1 != 1:
                break
            cos0End -= 1
        cos0End += 1
        freeLeftEnd = TOTALLLC - 1
        while freeLeftEnd >= 0:
            if self.freeLlc >> freeLeftEnd & 1 != 1:
                break
            freeLeftEnd -= 1
        freeLeftEnd += 1
        if freeLeftEnd < cos0End:  # mean can combine cache to cos0
            newCOS0 = (self.freeLlc >> freeLeftEnd) << freeLeftEnd
            if self.allocCache([0],[str(hex(newCOS0))]) == -1:
                return -1
        return 0

    # recycleCOS should be invoked after the pid moved to another COS or it just finishes
    def recycleCOS(self,cos):# num can be all
        #if self.allocCache(coslist, str(ALLLLC)) == -1:
        #    return -1
        self.freeLlc = self.freeLlc | self.cosLlc[cos]
        #self.cosLlc[cos] = ALLLLC
        if self.tryCombineFreeCOS0() == -1:
            print("Warning:when combine freellc with COS0 Fail")  # not big problem
        self.avaCOS.add(cos)
        return 0

    # cut the llc in cos by num
    def lessLlc(self,cos,num):
        if int(num) >= self.cosLlcNum(cos):
            print("Err:No enough llc to cut in lessLlc")
            return -1
        else:
            num = self.cosLlcNum(cos) - num
            if self.recycleCOS(cos) == -1:
                return -1
            llcs = self.findFreeLlc(num)
            if llcs == -1:
                print("Err:some other process may change COS")
                return -1
            if self.allocCache([cos], [str(hex(llcs))]) == -1:
                print("Err:lessLlc when re-allocate cache fail")
                return -1
            return 0

    def moreLlc(self,cos,num):
        if int(num) >= self.cosLlcNum(cos) + self.cosLlcNum(-1):
            print("Err:No enough llc to cut in lessLlc")
            return -1
        else:
            old_num = self.cosLlcNum(cos)
            old_llc = self.cosLlc(cos)
            num = old_num + num
            if self.recycleCOS(cos) == -1:
                return -1
            llcs = self.findFreeLlc(num)
            if llcs == -1:
                print("Err: No enough excessive cache")
                self.allocCache([cos],[str(hex(old_llc))])
                return -1
            if self.allocCache([cos], [str(hex(llcs))]) == -1:
                print("Err:lessLlc when re-allocate cache fail")
                return -1
            return 0

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
        for cos,llc in zip(coses,llcs):
            self.freeLlc = self.freeLlc ^ llc
            self.cosLlc[cos] = llc
            if llc & self.cosLlc[0] != 0 and cos != 0:  # get from COS0
                self.cosLlc[0] = self.cosLlc[0] ^ llc
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
