import json
#import logging
import argparse
import time
import policy as po
import resourceMonitor as rM
import resourceControll as rC

class CpuController:
    def __init__(self, configFile, samples, en_data, en_train, en_detect, accuracy, sleep_interval, sample_len):
        #self.logging.basicConfig('logger.log',logging.INFO)
        #self.logger = logging.getLogger('example1')
        self.enable_data_driven = en_data
        self.enable_training = en_train
        self.enable_detecting = en_detect
        self.sleep_interval = sleep_interval
        self.allGroups = samples
        self.sample_len = sample_len

        controll_config = json.loads(open(configFile,'r').read())
        self.policies = {}
        for g in controll_config.keys():
            self.policies[g] = po.Policy(g, self.allGroups, controll_config[g], accuracy)

        self.currentInfo = {}
        self.llcM = rC.cat.llcManager(4)
        self.groupCOS = {}

        self.throttled_group = []


    # try to add the groups who break SLA
    def try_to_add_sample(self):
        self.currentInfo = rM.perf.getAllInfo(self.allGroups, self.sample_len)
        samples = []
        for group in self.currentInfo.keys():
            # now the sla depends on ipc=instructions/cycles
            if float(self.currentInfo[group]["instructions"])/float(self.currentInfo[group]["cycles"]) < float(self.policies[group].controlConfig["SLA"]["ipc"]):
                samples.append(group)
        #TODO:sava the currentInfo for future use
        return samples


    def run(self):

        while True:
            if self.sleep_interval > 0:
                time.sleep(self.sleep_interval)
            
            # try_to_add_sample will also collect the current info of all the groups
            sample = self.try_to_add_sample()
            for g in self.policies.keys():
                self.policies[g].with_run(self.currentInfo, self.enable_training)
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


    def check_cpu(self,sample):
        group = self.select_low_ipc_group(sample) #sample is a list filled with groups needed to be watched

        if group is not None:
            self.start_cpu_throttle_analyst(group)
        elif len(self.throttled_group) != 0:
            self.start_cpu_relax_analyst()


    def start_cpu_relax_analyst(self):
        for t in self.throttled_group:
            if self.llcM.moreLlc(self.groupCOS[t], 2) == -1:
                if rC.cfs_quotaCut(t, 1.25) == -1:
                    return -1


    def start_cpu_throttle_analyst(self, group):
        policy = self.policies[group]
        if self.enable_data_driven and policy.estimator.workable():
            policy.throttle_target_select_setup(self.groupCOS, self.throttled_group, self.llcM)
        else:
            if policy.rule_update(self.groupCOS, self.throttled_group, self.llcM) == -1:
                print("Err: toplev_update Fail")
                return -1
        return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='help manual')
    parser.add_argument('--config', type=str, default="./config.json")
    parser.add_argument('--enable-detecting')
    parser.add_argument('--enable-training')
    parser.add_argument('--enable-data-driven')
    parser.add_argument('--samples', type=str, default="", help="the groups needed to control")
    parser.add_argument('--accuracy', type=float, default=0.7, help="the threshold of model's accuracy")
    parser.add_argument('--sample-length', type=int, default=3, help="how many seconds the sampling measurement should cover")
    parser.add_argument('--sleep', type=int, default=4, help="pause sleep seconds between each round")
    args = parser.parse_args()
    en_data = args.enable_data_driven != None
    en_det = args.enable_detecting != None
    en_tra = args.enable_training != None
    samples = args.samples.strip().split(',')
    c = CpuController(args.config, samples, en_data, en_tra, en_det, args.accuracy, args.sleep, args.sample_length)
    c.run()

