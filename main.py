import csv
import json
#import logging
import argparse
import random
import time
import policy as po
import resourceMonitor as rM
import resourceControll as rC
import subprocess
from multiprocessing import Process

avaCpus = {8,9,10}

STORE_PERIOD = 100


def run_com(cmd,flag):
    #print()
    while(True):
        tmpLog = ""
        if (flag):
            tmpLog = subprocess.getoutput("sudo " + cmd)
            #raise KeyboardInterrupt
            # print("Err: Start or Running help shell Fail")
        else:
            tmpLog = subprocess.getoutput(cmd)
            #raise KeyboardInterrupt
            # print("Err: Start or Running help shell Fail")
        logF = open(po.es.SAVE_PATH + "command_log_" + cmd, 'a')
        logF.write(time.asctime(time.localtime(time.time())))
        logF.write(tmpLog)
        # csv.writer(historyyF).writerows(self.historyy)
        # json.dump({str(self.own):self.historyX},historyXF)
        # json.dump({str(self.own):self.historyy},historyyF)
        # historyXF.close()
        logF.close()



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
        for g in samples:
            self.policies[g] = po.Policy(g, self.allGroups, controll_config, accuracy)

        self.currentInfo = {}
        self.llcM = llcM

        self.throttled_group = set()

        self.relax_count = 0




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
        #print("get currentInfo")
        samples = []
        for group in self.currentInfo.keys():
            # now the sla depends on ipc=instructions/cycles
            if float(self.currentInfo[group]["ipc"]) < float(self.policies[group].controlConfig[group]["SLA"]["ipc"]):
                samples.append(group)
        #print("can return samples")

        return samples


    def run(self):
        total_round = 0
        experi_data = []
        dataF = open(po.es.SAVE_PATH + "data_for_plot.csv", 'w')
        headers = []
        for g in self.allGroups:  # allGroup should <= self.policies.keys()y
            headers.append(g + "_ipc")
            headers.append(g + "_cpu")
            headers.append(g + "_llc")
        dict_w = csv.DictWriter(dataF, headers)
        dict_w.writeheader()
        dataF.close()
        while True:
            if self.sleep_interval > 0:
                time.sleep(self.sleep_interval)
            
            # try_to_add_sample will also collect the current info of all the groups
            sample = self.try_to_add_sample()
            if sample == -1:
                return -1
            tmp_data = {}
            for g in self.allGroups: # allGroup should <= self.policies.keys()y
                self.policies[g].with_run(self.currentInfo, self.enable_training)
                print(self.currentInfo[g]["ipc"])
                print(rM.get_cfs_quota(g))
                print(self.llcM.cosLlcNum(llcM.groupCOS[g]))

                tmp_data[g + "_ipc"] = self.currentInfo[g]["ipc"]
                tmp_data[g + "_cpu"] = rM.get_cfs_quota(g)
                tmp_data[g + "_llc"] = self.llcM.cosLlcNum(llcM.groupCOS[g])
            experi_data.append(tmp_data)
            self.check_cpu(sample)
            print("round in a period is:" + str(total_round))
            if total_round == STORE_PERIOD:
                #timeNow = time.asctime(time.localtime(time.time()))
                dataF = open(po.es.SAVE_PATH + "data_for_plot.csv",'a')
                #json.dump(experi_data, dataF)
                dict_w = csv.DictWriter(dataF,headers)
                dict_w.writerows(experi_data)
                experi_data.clear()
                dataF.close()
                total_round = 0
            total_round += 1


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
        print("select_low_ipc_group")
        least_ipc = 9999.9
        least_group = ""
        for group in sample:
            tmpIpc = 0.0
            try:
                tmpIpc = float(self.currentInfo[group]["ipc"])
            except:
                print(self.currentInfo[group])
            if tmpIpc < least_ipc:
                least_ipc = tmpIpc
                least_group = group
        return least_group


    def check_cpu(self,sample):
        print("check_cpu")
        group = self.select_low_ipc_group(sample) #sample is a list filled with groups needed to be watched

        if group is not None:
            self.start_cpu_throttle_analyst(group)
        elif self.relax_count >= 2:
            self.relax_count = 0
            self.start_cpu_relax_analyst()
        else:
            self.relax_count += 1


    def start_cpu_relax_analyst(self):
        print("start_cpu_relax_analyst")
        t = ""
        if len(self.throttled_group) == 0:
            t = random.choice(self.allGroups)
        else:
            t = self.throttled_group.pop()
        #print(self.policies[t].controlConfig[t]["maximum_setups"]["llc"])
        if self.policies[t].controlConfig[t]["maximum_setups"]["llc"] <= self.llcM.cosLlcNum(llcM.groupCOS[t]) \
                or self.llcM.moreLlc(llcM.groupCOS[t], int((self.policies[t].controlConfig[t]["maximum_setups"][
                                                                "llc"] - self.llcM.cosLlcNum(
            llcM.groupCOS[t])) / 4) + 1) == -1:
            now_quota = rM.get_cfs_quota(t)
            print("now_quota is" + str(now_quota))
            if self.policies[t].controlConfig[t]["maximum_setups"]["cpu"] > now_quota * 1.1:
                if rC.cfs_quotaCut(t, 1.1) == -1:
                    return -1
                else:
                    print("relax action for:" + t + " now: " + str(rM.get_cfs_quota(t)))
            else:
                if rC.cfs_quotaCut(t,
                                   float(self.policies[t].controlConfig[t]["maximum_setups"]["cpu"] / now_quota)) == -1:
                    return -1
                else:
                    print("relax action for:" + t + " now: " + str(rM.get_cfs_quota(t)))

        return 0


    def start_cpu_throttle_analyst(self, group):
        policy = self.policies[group]
        print("start_cpu_throttle_anaylyst")
        #if self.enable_data_driven and policy.estimator.workable():
        if self.enable_data_driven:
            policy.throttle_target_select_setup(self.throttled_group, self.llcM)
        else:
            if policy.rule_update(self.throttled_group, self.llcM) == -1:
                print("Err: toplev_update Fail")
                return -1
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
        parser.add_argument('--accuracy', type=float, default=0.5, help="the threshold of model's accuracy")
        parser.add_argument('--sample-length', type=int, default=4,
                            help="how many seconds the sampling measurement should cover")
        parser.add_argument('--sleep', type=int, default=2, help="pause sleep seconds between each round")
        args = parser.parse_args()
        en_data = args.enable_data_driven != None
        en_tra = args.enable_training != None
        samples = args.samples.strip().split(',')
        s_f = samples

        controll_config = json.loads(open(args.config, 'r').read())
        llcM = rC.cat.llcManager(5)

        for s in samples:
            rC.createCgroup("cpu,perf_event,cpuset", s)
            rC.cpusSet(avaCpus.pop(), s)
            rC.cpusetMemsSet(0, s)
            rC.startProcs("cpu,perf_event,cpuset", s, "/home/sauron/MAGI/run_" + s)
            time.sleep(1)
            if s == "xapian":
                cli_cmd = {'/home/sauron/tailbench-v0.9/xapian/run_xapian_client'}
                newP = Process(target=run_com, args=(cli_cmd,True))
                newP.start()

            if s == "memcached":
                time.sleep(5)
                cli_cmd = {'/home/sauron/MAGI/run_ycsb_memcached'}
                newP = Process(target=run_com, args=(cli_cmd,False))
                newP.start()


            # initial period is 100000, give app the maximum
            rC.cfs_quotaSet(s, int((controll_config[s]["maximum_setups"]["cpu"] + controll_config[s]["minimum_setups"]["cpu"]) / 2))
            pids = rM.get_group_pids("perf_event/" + s)
            pa_pids = ','.join([str(i) for i in pids])
            if llcM.givePidSepLlc(pa_pids, int((controll_config[s]["maximum_setups"]["llc"] + controll_config[s]["minimum_setups"]["llc"])/2), s) == -1:
                print("Err: No enough LLC, maybe you need to change config file")
        time.sleep(3)
        # here samples are like : ["app1","app2"]
        c = CpuController(controll_config, samples, en_data, en_tra, args.accuracy, args.sleep, args.sample_length,
                          llcM)
        c.run()
    except Exception as err:
        print(err)
    finally:
        print("do finally")
        if subprocess.getstatusoutput("sudo pqos -I -R")[0] != 0:
            print("Err: Reset llc fail")
        for s in s_f:
            pids = subprocess.getoutput("sudo cat /sys/fs/cgroup/perf_event/" + s + "/cgroup.procs").strip().split()
            for pid in pids:
                if subprocess.getstatusoutput("sudo kill -9 " + str(pid))[0] != 0:
                    print("Err: Closing test process fail, pid: " + str(pid))
            rC.deleteCgroup("cpu,perf_event,cpuset", s)



