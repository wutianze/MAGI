import json
#import logging
import policy
import resourceMonitor as rM
from enum import Enum

sampleFile = 'samples.txt'
RULEIPCBOUND = 1
RULEMPKIBOUND = 5
RULEMEMBWBOUND = 35

class CpuController:
    def __init__(self,configFile,sampleFile):
        self.logging.basicConfig(filename='logger.log',level=logging.INFO)
        self.logger = logging.getLogger('example1')
        self.enable_training = True
        self.sleep_interval = 10
        self.ipc_policies = json.loads(open(configFile,'r').read())
        self.allGroups = list(map(str,open(sampleFile,'r').read().strip().split()) 
        self.currentInfo = {}
    
    # try to add the groups who break SLA
    def try_to_add_sample():
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
    def select_low_ipc_group(sample):
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
            if tmpIpc = float(self.currentInfo[group]["instructions"])/float(self.currentInfo[group]["cycles"] < least_ipc:
                least_ipc = tmpIpc
                least_group = group
        return least_group

    def rule_update(self,group):
        boundPart = rM.pmu.toDownGroup(group)
        curGI = self.currentInfo[group]
        if boundPart == "Backend_Bound":
            # memory-bound
            if float(curGI["instructions"])/float(curGI["cycles"]) < RULEIPCBOUND and float(curGI["cache-misses"])*1000.0/float(curGI["instructions"]) > RULEMPKIBOUND:
                # llc-bound
                if float(rM.cat.getMbw(rM.cgroup.getCgroupPids(group))/1024.0) < RULEMEMBWBOUND:
                    #TODO relax llc of victim etc
                # mem-bw-bound
                else:
            # core-bound
            else:
        elif boundPart == "Frontend_Bound":

        else:
            return 1
        return 0

    def check_cpu(self,sample):
        group = self.select_low_ipc_group(sample) #sample is a list filled with groups needed to be watched

        if group is not None:
            self.start_cpu_throttle_analyst(group,sample)
        elif self.have_cpu_throttled_group():
            self.start_cpu_relax_analyst(sample)

    def start_cpu_throttle_analyst(self,group,sample):
        policy = self.ipc_policies[group]

        for p in [POLICYS.DATA_DRIVEN,POLICYS.RULE]:
            if p == POLICYS.DATA_DRIVEN and (not self.enable_data_driven or not policy.estimator.workable()):
                continue

            if p == POLICYS.RULE:
                if self.rule_update(group) == 1:
                    print("Err: toplev_update Fail")
                break

            targets = policy.select_throttle_target(sample)

            if len(targets) == 0:
                self.logger.info("Group %s policy %s returns None,fall back",group,policy.name)
                continue
            else:
                self.logger.info("using policy %s to make decision",policy.name)
                self.set_throttle_setup(targets)
                break
if __name__ == '__main__':
	configFileName = input("enter the config file path:")
	configFile = open(configFileName,"r")
	configContent = json.loads(configFile.read())
	print(configContent["/apasra/tubo"]["SLA"])

