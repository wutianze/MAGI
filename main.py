import json
import logging
import policy
import resourceMonitor as rM
from enum import Enum

class SubSystem(Enum):
    CPU = 0
    DISK = 1
    NET = 2
    DOWNSTREAM = 3
    QPS = 4

class MAGIcontroller:
    def __init__(self,cpu_policies):
        self.logging.basicConfig(filename='logger.log',level=logging.INFO)
        self.logger = logging.getLogger('example1')
        self.enable_training = True
        self.sleep_interval = 10
    
    def loadConfig(self,subsys,driven,path):
        tmp = json.loads(open(path,'r').read())
        if subsys == CPU:
            self.cpu_policies[driven] = tmp
        elif subsys == DISK:
            self.disk_policies[driven] = tmp
        elif subsys == NET:
            self.net_policies[driven] = tmp
        elif subsys == DOWNSTREAM:
            self.downstream_policies[driven] = tmp
        elif subsys == QPS:
            self.qps_policies[driven] = tmp
        else:
            logger.error("wrong subsys while load config file")

    def run(self):
        if self.enable_training:
            self.try_to_train_model()

        while True:
            if self.sleep_interval > 0:
                time.sleep(self.sleep_interval)

            sample = self.try_to_add_sample()

            if self.enable_detecting:
                self.check_cpu(sample)

# select the least-ipc group in sample
    def select_low_ipc_group(sample):
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


    def do_measure_toplev_l1(self,group):

    def check_cpu(self,sample):
        group = self.select_low_ipc_group(sample) #sample is a list filled with groups needed to be watched

        if group is not None:
            self.start_cpu_throttle_analyst(group,sample)
        elif self.have_cpu_throttled_group():
            self.start_cpu_relax_analyst(sample)

    def start_cpu_throttle_analyst(self,group,sample):
        policies = self.policies[group]

        for p in [POLICYS.DATA_DRIVEN,POLICYS.RULE]:
            policy = policies[p]

            if p == POLICYS.DATA_DRIVEN and (not self.enable_data_driven or not policy.estimator.workable()):
                continue

            if p == POLICYS.RULE:
                l1_sample = self.do_measure_toplev_l1(group)
                deepupdate(sample,l1_sample)

            targets = policy.select_throttle_target(sample)#find interference source

            if len(targets) == 0:
                self.logger.info("Group %s policy %s returns None,fall back",group,policy.name)
                self.set_throttle_setup(targets)                  #do throttle to interference source
                break
if __name__ == '__main__':
	configFileName = input("enter the config file path:")
	configFile = open(configFileName,"r")
	configContent = json.loads(configFile.read())
	print(configContent["/apasra/tubo"]["SLA"])

