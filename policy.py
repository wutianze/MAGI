import estimator as es
import resourceControll as rC
import resourceMonitor as rM

RULEIPCBOUND = 1
RULEMPKIBOUND = 5
RULEMEMBWBOUND = 35

class Policy:
    def __init__(self,group,groups,control_config,accuracy):
        self.own = group
        self.controlConfig = control_config
        self.estimator = es.Estimator(accuracy)
        self.groups = groups
        self.currentInfo = {}
    
    def generate_one_train_data(self,infoList):
        mainD = []
        otherD = []
        for (group,event_name,lineCon) in infoList:
            if group == self.name:
                pass



    def select_throttle_target(self,group):
        pass


    # RULE Model
    def rule_update(self):
        boundPart = rM.pmu.topDownGroup(self.own)
        curGI = self.currentInfo[self.own]
        if boundPart == "Backend_Bound":
            # memory-bound
            if float(curGI["instructions"])/float(curGI["cycles"]) < RULEIPCBOUND and float(curGI["cache-misses"])*1000.0/float(curGI["instructions"]) > RULEMPKIBOUND:
                # llc-bound
                if float(rM.cat.getCgroupsMbw([self.own])[self.own])/1024.0 < RULEMEMBWBOUND:
                    # different from paper,need to find a better way
                    if self.groupCOS[self.own] != 0:
                        if rC.llcManager.moreLlc(self.groupCOS[self.own], 2) == -1:# give 2 more cache
                            badGroup = rM.findGroupConsumeMostLlc(self.groups, self.own)
                            if rC.llcManager.lessLlc(self.groupCOS[badGroup],2) == -1:
                                rC.cfs_quotaCut(badGroup)
                # mem-bw-bound
                else:
                    rC.cfs_quotaCut(rM.findGroupConsumeMostMbw(self.groups,self.own),0.8)
            # core-bound
            else:
                rC.cfs_quotaCut(rM.getCoGroup(self.own,self.groups),0.8)
        elif boundPart == "Frontend_Bound":
            rC.cfs_quotaCut(rM.getCoGroup(self.own, self.groups), 0.8)

        else:
            print("Err: Rule Model can do Nothing more")
            return -1
        return 0

if __name__ == '__main__':
    pass


