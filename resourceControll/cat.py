import subprocess

ALLLLC = 0xfffff
FREELLC = 0x3ffff
FORCHECK = 0x80000
TOTALLLC = 20
FREELLCNUM = 18
# the manager is not thread safe !!
class llcManager:
    def __init__(self,numCOS):# numCOS doesn't have COS0,COS0 should keep at least 2 cache,and COS0's own caches are always remain in the left like: 0xc0000
        self.freeLlc = FREELLC
        self.cosLlc = {}
        self.cosLlc[0] = ALLLLC
        self.avaCOS = set()
        self.groupCOS = {}
        for i in range(numCOS):
            self.avaCOS.add(i+1)



    def cosLlcNum(self,cos):
        #print("cosLlcNum")
        llcs = 0x0
        res = 0
        if cos == -1:# count free num,COS0 has at least 2 cache
            llcs = self.freeLlc
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
            llc += 2 ** i
        for i in range(TOTALLLC):# because there are 2 caches for COS0
            if (self.freeLlc >> i) & llc == llc:
                return llc << i
        print("No enough excessive free llc")#may do a clear up
        return -2 # mean no excessive free llc


    # in this function, the controll part of  llc is hard to check, so we just give up checking
    # pids is a list,groupName is like "app1"
    def givePidSepLlc(self, pids, num, groupName):
        if len(self.avaCOS) == 0:
            print("No available COS")
            return -1
        else:
            cos = self.avaCOS.pop()
            if self.assoProcessCOS([pids], [cos]) == -1:
                #self.avaCOS.add(cos)
                print("Warning: assoProcessCOS fail, may not affect")
                #return -1
            llcs = self.findFreeLlc(num)
            if llcs == -1:
                print("Find free llc fail")
                self.avaCOS.add(cos)
                return -1
            if self.allocCache([cos], [llcs]) == -1:
                self.avaCOS.add(cos)
                return -1
            if groupName != "":
                self.groupCOS[groupName] = cos
            return cos

    def tryCombineFreeCOS0(self):
        cos0End = TOTALLLC - 1
        while cos0End >= 0:
            if self.cosLlc[0] >> cos0End & 1 != 1:
                break
            cos0End -= 1
        cos0End += 1
        freeLeftEnd = FREELLCNUM - 1
        while freeLeftEnd >= 0:
            if self.freeLlc >> freeLeftEnd & 1 != 1:
                break
            freeLeftEnd -= 1
        freeLeftEnd += 1
        if freeLeftEnd < cos0End:  # mean can combine cache to cos0
            newCOS0 = ((self.freeLlc >> freeLeftEnd) << freeLeftEnd)|self.cosLlc[0]
            self.allocCache([0],[newCOS0])

    # recycleCOS should be invoked after the pid moved to another COS or it just finishes
    def recycleCOS(self,cos):# num can be all
        #if self.allocCache(coslist, str(ALLLLC)) == -1:
        #    return -1
        self.freeLlc = self.freeLlc | self.cosLlc[cos]
        self.avaCOS.add(cos)


    # cut the llc in cos by num
    def lessLlc(self, cos, num):
        print("do lessLlc")
        if cos == 0:
            print("Err: lessLlc have cos=0")
            return -1
        if int(num) >= self.cosLlcNum(cos):
            print("Err:No enough llc to cut in lessLlc")
            return -1
        else:
            num = self.cosLlcNum(cos) - num
            self.recycleCOS(cos)
            llcs = self.findFreeLlc(num)
            if llcs == -1:
                print("Err:some other process may change COS")
                return -1
            self.allocCache([cos], [llcs])
            self.avaCOS.remove(cos)
            self.tryCombineFreeCOS0()
            return 0

    def moreLlc(self, cos, num):
        print("do moreLlc")
        if cos == 0:
            self.tryCombineFreeCOS0()
            print("Warning: Try to give more llc to COS0, tried best")
            return 0
        if int(num) >= self.cosLlcNum(cos) + self.cosLlcNum(-1):
            print("Err: No enough llc to give in moreLlc")
            return -1
        else:
            old_num = self.cosLlcNum(cos)
            old_llc = self.cosLlc[cos]
            num = old_num + num
            self.recycleCOS(cos)
            llcs = self.findFreeLlc(num)
            if llcs == -1:
                print("Err: No enough cache")
                print(self.cosLlc)
                self.avaCOS.remove(cos)
                self.allocCache([cos],[old_llc])
                return -1
            if llcs == -2:
                print("do big reallocation")
                for g in self.groupCOS.keys():
                    tmpc = self.groupCOS[g]
                    if tmpc != cos:
                        self.recycleCOS(tmpc)
                for g in self.groupCOS.keys():
                    tmpc = self.groupCOS[g]
                    newF = 0
                    if tmpc == cos:
                        newF = self.findFreeLlc(num)
                    else:
                        newF = self.findFreeLlc(self.cosLlcNum(tmpc))
                    self.allocCache([tmpc],[newF])
                    self.avaCOS.remove(tmpc)
                self.tryCombineFreeCOS0()
                return 0
            self.allocCache([cos], [llcs])
            self.avaCOS.remove(cos)
            return 0
    '''
    def reAlloc(self):
        for g in self.groupCOS.keys():
            self.lessLlc()
            '''

    # Sets all COS to default (fill into all ways) and associates all cores with COS 0
    def resetCAT(self, numCOS):
        if subprocess.getstatusoutput('sudo pqos -R')[0] != 0:
            print("Err: resetCAT fail")
        self.__init__(numCOS)

    # set COS i to the x cache ways
    # both pqos -e and pqos -I -e can be used,llcs must be str !!
    # ex:"llc:1=0x000f;llc:2=0x0ff0"
    def allocCache(self, coses, llcs):
        cmd = "sudo pqos -I -e \""
        for cos, llc in zip(coses,llcs):
            cmd += "llc:" + str(cos) + "=" + str(llc) + ";"
        cmd += "\""
        if subprocess.getstatusoutput(cmd)[0] != 0:
            print("Err: allocCache Fail")
            print(self.cosLlc)
            raise Exception('CAT Controller Err')
        for cos, llc in zip(coses,llcs):
            self.cosLlc[cos] = llc
            if cos != 0:
                self.freeLlc = self.freeLlc ^ llc
                self.cosLlc[0] = (self.cosLlc[0] & llc) ^ self.cosLlc[0]
                if subprocess.getstatusoutput("sudo pqos -I -e \"llc:0=" + str(self.cosLlc[0]) + ";\"")[0] != 0:
                    print("Err: allocCache for COS0 Fail")
                    print(self.cosLlc)
                    raise Exception('CAT Controller Err')
        return 0


# although one pid is not exist , the other can still be associated correctly
    def assoProcessCOS(self, pidss, coses):
        cmd = "sudo pqos -I -a \""
        for cos,pids in zip(coses, pidss):
            cmd += "pid:" + str(cos) + "=" + str(pids) + ";"
        cmd += "\""
#print("debug " + cmd)
        if subprocess.getstatusoutput(cmd)[0] != 0:
            print("Err:assoProcessCOS Fail")
            return -1

        #print(subprocess.getstatusoutput(cmd))
        return 0

        

if __name__ == '__main__':
    lm = llcManager(3)
    cos = lm.givePidSepLlc("33931",4,"")
    if cos == -1:
        print("give wrong")
    lm.moreLlc(cos, 2)
    cos2 = lm.givePidSepLlc("3479",5,"")
    lm.lessLlc(cos2,3)
    lm.recycleCOS(cos)
    lm.recycleCOS(cos2)
    lm.resetCAT(3)
    #print("%x",lm.findFreeLlc(4))

