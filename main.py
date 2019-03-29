import json
#import logging
import time
import policy as po
import resourceMonitor as rM
import resourceControll as rC

class CpuController:
    def __init__(self,configFile,sampleFile, en_data,en_train, en_detect, accuracy):
        #self.logging.basicConfig('logger.log',logging.INFO)
        #self.logger = logging.getLogger('example1')
        self.enable_data_driven = en_data
        self.enable_training = en_train
        self.enable_detecting = en_detect
        self.sleep_interval = 10
        self.allGroups = list(map(str, open(sampleFile, 'r').read().strip().split()))

        controll_config = json.loads(open(configFile,'r').read())
        self.policies = {}
        for g in controll_config.keys():
            self.policies[g] = po.Policy(g, self.allGroups, controll_config[g], accuracy)

        self.currentInfo = {}
        self.llcM = rC.cat.llcManager(4)
        self.groupCOS = {}


    # try to add the groups who break SLA
    def try_to_add_sample(self):
        self.currentInfo = rM.perf.getAllInfo(self.allGroups)
        samples = []
        for group in self.currentInfo.keys():
            # now the sla depends on ipc=instructions/cycles
            if float(self.currentInfo[group]["instructions"])/float(self.currentInfo[group]["cycles"]) < float(self.ipc_policies[group]["SLA"]["ipc"]):
                samples.append(group)
        #TODO:sava the currentInfo for future use
        return samples


    def run(self):
        if self.enable_training:
            self.try_to_train_model()

        while True:
            if self.sleep_interval > 0:
                time.sleep(self.sleep_interval)
            
            # try_to_add_sample will also collect the current info of all the groups
            sample = self.try_to_add_sample()

            if self.enable_detecting:
                self.check_cpu(sample)


# select the least-ipc group in sample
    def select_low_ipc_group(self,sample):
        if len(sample) == 0:
            return None
        '''
        res = ''
        minpA = 999
        for g in sample:
            pids = rM.cgroup.getCgroupPids(g)
            pA = 0.0
            for p in pids:
                pA = pA + rM.cat.getIpc(int(p))
            pA = pA / float(len(pids))
            if minpA >= pA:
                minpA = pA
                res = g
        return res
        '''
        least_ipc = 9999.9
        least_group = ""
        for group in sample:
            tmpIpc = float(self.currentInfo[group]["instructions"])/float(self.currentInfo[group]["cycles"])
            if tmpIpc < least_ipc:
                least_ipc = tmpIpc
                least_group = group
        return least_group


    '''
    # RULE Model
    def rule_update(self,group):
        boundPart = rM.pmu.topDownGroup(group)
        curGI = self.currentInfo[group]
        if boundPart == "Backend_Bound":
            # memory-bound
            if float(curGI["instructions"])/float(curGI["cycles"]) < RULEIPCBOUND and float(curGI["cache-misses"])*1000.0/float(curGI["instructions"]) > RULEMPKIBOUND:
                # llc-bound
                if float(rM.cat.getCgroupsMbw([group])[group])/1024.0 < RULEMEMBWBOUND:
                    # different from paper,need to find a better way
                    if self.groupCOS[group] != 0:
                        if rC.llcManager.moreLlc(self.groupCOS[group], 2) == -1:# give 2 more cache
                            badGroup = rM.findGroupConsumeMostLlc(self.allGroups, group)
                            if rC.llcManager.lessLlc(self.groupCOS[badGroup],2) == -1:
                                rC.cfs_quotaCut(badGroup)
                # mem-bw-bound
                else:
                    rC.cfs_quotaCut(rM.findGroupConsumeMostMbw(self.allGroups,group),0.8)
            # core-bound
            else:
                rC.cfs_quotaCut(rM.getCoGroup(group,self.allGroups),0.8)
        elif boundPart == "Frontend_Bound":
            rC.cfs_quotaCut(rM.getCoGroup(group, self.allGroups), 0.8)

        else:
            print("Err: Rule Model can do Nothing more")
            return -1
        return 0
        '''

    def check_cpu(self,sample):
        group = self.select_low_ipc_group(sample) #sample is a list filled with groups needed to be watched

        if group is not None:
            self.start_cpu_throttle_analyst(group,sample)
        elif self.have_cpu_throttled_group():
            self.start_cpu_relax_analyst(sample)


    def start_cpu_throttle_analyst(self, group, sample):
        policy = self.policies[group]
        if self.enable_data_driven and policy.estimator.workable():
            policy.throttle_target_select_setup(self.groupCOS)
        else:
            if policy.rule_update(self.groupCOS) == -1:
                print("Err: toplev_update Fail")
                return -1
        return 0








if __name__ == '__main__':
    pass

