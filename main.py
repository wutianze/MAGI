import json
#import logging
import argparse
import time
import policy as po
import resourceMonitor as rM
import resourceControll as rC
import subprocess
from multiprocessing import Process

avaCpus = {3,4}
def new_help(cmd):
    #print()
    if subprocess.getstatusoutput("sudo " + cmd)[0] != 0:
        print("Err: Start or Running help shell Fail")


class CpuController:
    def __init__(self, controll_config, samples, en_data, en_train, accuracy, sleep_interval, sample_len, llcM):
        #self.logging.basicConfig('logger.log',logging.INFO)
        #self.logger = logging.getLogger('example1')
        self.enable_data_driven = en_data
        self.enable_training = en_train
        self.sleep_interval = sleep_interval
        self.allGroups = samples# ["app1","app2"]
        self.sample_len = sample_len

        self.policies = {}
        for g in controll_config.keys():# g is just "app1", not "cpu/app1"
            self.policies[g] = po.Policy(g, self.allGroups, controll_config, accuracy)

        self.currentInfo = {}
        self.llcM = llcM

        self.throttled_group = set()


    # try to add the groups who break SLA
    def try_to_add_sample(self):
        tmp_info = None
        check_live = 0
        while tmp_info == None:
            if(check_live == 10):
                print("Err: some app may exit!")
                return -1
            check_live += 1
            tmp_info = rM.perf.getAllInfo(self.allGroups, self.sample_len)
        self.currentInfo = tmp_info
        samples = []
        for group in self.currentInfo.keys():
            # now the sla depends on ipc=instructions/cycles
            if float(self.currentInfo[group]["ipc"]) < float(self.policies[group].controlConfig[group]["SLA"]["ipc"]):
                samples.append(group)
        #TODO:sava the currentInfo for future use
        return samples


    def run(self):

        while True:
            if self.sleep_interval > 0:
                time.sleep(self.sleep_interval)
            
            # try_to_add_sample will also collect the current info of all the groups
            sample = self.try_to_add_sample()
            if sample == -1:
                return -1
            for g in self.allGroups: # allGroup should <= self.policies.keys()y
                self.policies[g].with_run(self.currentInfo, self.enable_training)
            self.check_cpu(sample)
            print("round ++")


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
            tmpIpc = float(self.currentInfo[group]["ipc"])
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
            if self.policies[t].controlConfig[t]["maxium_setups"]["llc"] <= self.llcM.cosLlcNum(t) or self.llcM.moreLlc(llcM.groupCOS[t], int((self.policies[t].controlConfig["maxium_setups"]["llc"] - self.llcM.cosLlcNum(t)) / 2) + 1) == -1:
                now_quota = rM.get_cfs_quota(t)
                if self.policies[t].controlConfig[t]["maxium_setups"]["cpu"] > now_quota * 1.25:
                    if rC.cfs_quotaCut(t, 1.25) == -1:
                        return -1
                    else:
                        print("relax action for:" + t + "now: " + str(rM.get_cfs_quota(t)))
                else:
                    if rC.cfs_quotaCut(t,float(self.policies[t].controlConfig[t]["maxium_setups"]["cpu"] / now_quota)) == -1:
                        return -1
                    else:
                        print("relax action for:" + t + "now: " + str(rM.get_cfs_quota(t)))

        return 0


    def start_cpu_throttle_analyst(self, group):
        policy = self.policies[group]
        if self.enable_data_driven and policy.estimator.workable():
            policy.throttle_target_select_setup(self.throttled_group, self.llcM)
        '''
        else:
            if policy.rule_update(self.throttled_group, self.llcM) == -1:
                print("Err: toplev_update Fail")
                return -1
            '''
        return 0

if __name__ == '__main__':
    s_f = []
    try:
        parser = argparse.ArgumentParser(description='help manual')
        parser.add_argument('--config', type=str, default="./testcon")
        parser.add_argument('--enable-training')
        parser.add_argument('--enable-data-driven')
        parser.add_argument('--samples', type=str, default="",
                            help="the groups needed to control")  # here the groups shouldn't be full path,ex: app1 not /cpu/app1
        parser.add_argument('--accuracy', type=float, default=0.1, help="the threshold of model's accuracy")
        parser.add_argument('--sample-length', type=int, default=4,
                            help="how many seconds the sampling measurement should cover")
        parser.add_argument('--sleep', type=int, default=1, help="pause sleep seconds between each round")
        args = parser.parse_args()
        en_data = args.enable_data_driven != None
        en_tra = args.enable_training != None
        samples = args.samples.strip().split(',')
        s_f = samples

        controll_config = json.loads(open(args.config, 'r').read())
        llcM = rC.cat.llcManager(4)

        for s in samples:
            rC.createCgroup("cpu,perf_event,cpuset", s)
            rC.cpusSet(avaCpus.pop(), s)
            rC.cpusetMemsSet(0, s)
            rC.startProcs("cpu,perf_event,cpuset", s, "/home/sauron/MAGI/run_" + s)
            time.sleep(1)
            if s == "xapian":
                cli_cmd = {'/home/sauron/tailbench-v0.9/xapian/run_xapian_client'}
                newP = Process(target=new_help, args=cli_cmd)
                newP.start()

            # initial period is 100000, give app the maximum
            rC.cfs_quotaSet(s, controll_config[s]["maximum_setups"]["cpu"])
            pids = rM.get_group_pids("perf_event/" + s)
            pa_pids = ','.join([str(i) for i in pids])
            if llcM.givePidSepLlc(pa_pids, controll_config[s]["maximum_setups"]["llc"], s) == -1:
                if llcM.givePidSepLlc(pa_pids, controll_config[s]["minimum_setups"]["llc"], s) == -1:
                    print("Err: No enough LLC, maybe you need to change config file")

        # here samples are like : ["app1","app2"]
        c = CpuController(controll_config, samples, en_data, en_tra, args.accuracy, args.sleep, args.sample_length,
                          llcM)
        c.run()
    except Exception as err:
        print(err)
    finally:
        print("do finally")
        for s in s_f:
            pids = subprocess.getoutput("sudo cat /sys/fs/cgroup/perf_event/" + s + "/cgroup.procs").strip().split()
            for pid in pids:
                if subprocess.getstatusoutput("sudo kill -9 " + str(pid))[0] != 0:
                    print("Err: Closing test process fail, pid: " + str(pid))
            rC.deleteCgroup("cpu,perf_event,cpuset", s)
        if subprocess.getstatusoutput("sudo pqos -R")[0] != 0:
            print("Err: Reset llc fail")



