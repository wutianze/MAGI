import estimator as es
import resourceControll as rC
import resourceMonitor as rM
import numpy as np
import math

TRAINCIRCLE = 200

RULEIPCBOUND = 1
RULEMPKIBOUND = 5
RULEMEMBWBOUND = 35
mainExTar = ["lock_loads","fp_uops","branch","l1_misses","l2_misses","stall_sb","branch_misp","machine_clear"]
subTar = ["instructions","cycles","loads_and_stores","cache-misses"]


class Policy:
    def __init__(self,group,groups,control_config,accuracy):
        self.own = group# "app1"
        self.controlConfig = control_config
        self.estimator = es.Estimator(accuracy, group)
        self.groups = groups#["app1","app2"]
        self.currentInfo = {}
        self.roundHistoryX = []
        self.roundHistoryy = []
        self.historyX = []
        self.historyy = []

        self.count = 0

    def with_run(self, infoList, train_enable):
        self.currentInfo = infoList
        X, y = self.generate_one_train_data(infoList)
        self.roundHistoryX.append(X)
        self.roundHistoryy.append(y)
        self.count += 1
        #print(self.count)
        if self.count == TRAINCIRCLE:
            self.estimator.scaler_init(self.roundHistoryX)
            train_X, train_y = self.estimator.pre_data(self.roundHistoryX, self.roundHistoryy)
            self.historyX += train_X.tolist()
            self.historyy += train_y.tolist()
            self.roundHistoryX.clear()
            self.roundHistoryy.clear()# can store to local disk for future use
            self.count = 0
            if train_enable:
                self.estimator.train(np.array(self.historyX), np.array(self.historyy))

    def generate_one_train_data(self, infoList):
        train_X = []
        for tar in subTar:
            if tar != "cycles":
                train_X.append(infoList[self.own][tar])#infoList["app1"][...]
        for tar in mainExTar:
            train_X.append(infoList[self.own][tar])
        for g in self.groups:# groups:["app1","app2"] g: "app1"
            if g != self.own:
                for tar in subTar:
                    train_X.append(infoList[g][tar])
        train_y = float(infoList[self.own]["ipc"])
        return train_X, train_y



    def diff_index(self, x1, x2):
        dist = np.linalg.norm(np.array(x1 - x2))

        sepDiff = []
        main1 = []
        main2 = []
        mainNum = len(subTar)+len(mainExTar)
        for i in range(mainNum):
            main1.append(x1[i])
            main2.append(x2[i])
        sepDiff.append(np.linalg.norm(np.array(main1) - np.array(main2)))
        for i in range(len(self.groups) - 1):
            sub1 = []
            sub2 = []
            for j in range(len(subTar)):
                sub1.append(x1[mainNum + j])
                sub2.append(x2[mainNum + j])
            sepDiff.append(np.linalg.norm(np.array(sub1) - np.array(sub2)))
            mainNum += len(subTar)
        diffSum = np.sum(np.array(sepDiff))
        std_entropy = 0.0
        for d in sepDiff:# H = - ∑  Pi * log2 Pi
            p = float(d)/float(diffSum)
            std_entropy -= math.log(p,2) * p
        return dist * (1.0 + std_entropy)


    def find_basic_x(self, curr_x):
        small_set = self.estimator.find_sv_statisfy_v(self.historyX, self.historyy, float(self.controlConfig[self.own]["SLA"]))
        basic_x = None
        least_diff = 9999999.9
        for x in small_set:
            tmp_diff = self.diff_index(curr_x, x)
            if tmp_diff < least_diff:
                least_diff = tmp_diff
                basic_x = x
        return basic_x



    def select_throttle_target(self):
        curr_x = self.roundHistoryX[-1]
        basic_x = self.find_basic_x(curr_x)
        base_ipc = self.estimator.inference(basic_x)
        i = 0
        biggest_delta = 0
        target = ""
        for g in self.groups:
            if g != self.own:
                new_x = basic_x
                g_start = len(mainExTar) + len(subTar) + i * len(subTar)
                i += 1
                for j in range(len(subTar)):
                    new_x[g_start + j] = curr_x[g_start + j]
                guess = self.estimator.inference(new_x)
                if abs(float(guess) - base_ipc) > biggest_delta:
                    biggest_delta = abs(float(guess) - base_ipc)
                    target = g
        return target


    def set_throttle_setup(self, badGroup, throttled_group, llcM):
        if badGroup == "":
            print("Warining: Single process? Just Ignore")
            return 0
        curGI = self.currentInfo[self.own]
        # memory-bound
        if float(curGI["ipc"]) < RULEIPCBOUND and float(
                curGI["cache-misses"]) * 1000.0 / float(curGI["instructions"]) > RULEMPKIBOUND:
            # llc-bound
            if llcM.cosLlcNum(llcM.groupCOS[self.own]) >= self.controlConfig[self.own]["maximum_setups"]["llc"] or llcM.moreLlc(
                    llcM.groupCOS[self.own], int((self.controlConfig[self.own]["maximum_setups"]["llc"] - llcM.cosLlcNum(llcM.groupCOS[
                            self.own])) / 2) + 1) == -1:
                if llcM.cosLlcNum(llcM.groupCOS[badGroup]) <= self.controlConfig[badGroup]["minimum_setups"]["llc"] or llcM.lessLlc(
                        llcM.groupCOS[badGroup], int((llcM.cosLlcNum(llcM.groupCOS[badGroup]) -
                                                 self.controlConfig[badGroup]["minimum_setups"]["llc"]) / 2) + 1) == -1:
                    now_quota = rM.get_cfs_quota(badGroup)
                    if now_quota * 0.8 > self.controlConfig[badGroup]["minimum_setups"]["cpu"]:
                        if rC.cfs_quotaCut(badGroup, 0.8) == -1:
                            return -1
                    else:
                        if rC.cfs_quotaCut(badGroup, float(
                                self.controlConfig[badGroup]["minimum_setups"]["cpu"] / now_quota)) == -1:
                            return -1
            # mem-bw-bound
            else:
                now_quota = rM.get_cfs_quota(badGroup)
                if now_quota * 0.8 > self.controlConfig[badGroup]["minimum_setups"]["cpu"]:
                    if rC.cfs_quotaCut(badGroup, 0.8) == -1:
                        return -1
                else:
                    if rC.cfs_quotaCut(badGroup, float(
                            self.controlConfig[badGroup]["minimum_setups"]["cpu"] / now_quota)) == -1:
                        return -1
        # core-bound
        else:
            now_quota = rM.get_cfs_quota(badGroup)
            if now_quota * 0.8 > self.controlConfig[badGroup]["minimum_setups"]["cpu"]:
                if rC.cfs_quotaCut(badGroup, 0.8) == -1:
                    return -1
            else:
                if rC.cfs_quotaCut(badGroup, float(
                        self.controlConfig[badGroup]["minimum_setups"]["cpu"] / now_quota)) == -1:
                    return -1
        throttled_group.add(badGroup)
        return 0


    def throttle_target_select_setup(self, throttled_group, llcM):
        badGroup = self.select_throttle_target()
        if badGroup == "":
            # self.logger.info("Group %s policy %s returns None,fall back",group,policy.name)
            print("Have no targets")
            return -1
        else:
            # self.logger.info("using policy %s to make decision",policy.name)
            if self.set_throttle_setup(badGroup, throttled_group, llcM) == -1:
                print("Warning: set_throttle_setup fail")
            return 0


    # RULE Model
    def rule_update(self, throttled_group, llcM):
        boundPart = rM.pmu.topDownGroup(self.own)# self.own is like "app1"
        curGI = self.currentInfo[self.own]
        badGroup = ""
        if boundPart == "Backend_Bound":
            # memory-bound
            if float(curGI["ipc"]) < RULEIPCBOUND and float(curGI["cache-misses"])*1000.0/float(curGI["instructions"]) > RULEMPKIBOUND:
                # llc-bound
                if float(rM.cat.getGroupsSumMbl(self.own))/1024.0 < RULEMEMBWBOUND:
                    # different from paper,need to find a better way
                    if llcM.cosLlcNum(llcM.groupCOS[self.own]) >= self.controlConfig[self.own]["maximum_setups"]["llc"] or llcM.moreLlc(llcM.groupCOS[self.own], int((self.controlConfig[self.own]["maximum_setups"]["llc"] - llcM.cosLlcNum(llcM.groupCOS[self.own])) / 2) + 1) == -1:
                        badGroup = rM.findGroupConsumeMostLlc(self.groups,self.own)
                        if badGroup == "":
                            print("Warining: Single process? Just Ignore")
                            return 0
                        if llcM.cosLlcNum(llcM.groupCOS[badGroup]) <= self.controlConfig[badGroup]["minimum_setups"]["llc"] or llcM.lessLlc(llcM.groupCOS[badGroup], int((llcM.cosLlcNum(llcM.groupCOS[badGroup])- self.controlConfig[badGroup]["minimum_setups"]["llc"]) / 2) + 1) == -1:
                            now_quota = rM.get_cfs_quota(badGroup)
                            if now_quota * 0.8 > self.controlConfig[badGroup]["minimum_setups"]["cpu"]:
                                if rC.cfs_quotaCut(badGroup, 0.8) == -1:
                                    return -1
                                else:
                                    print("do quotaCut 0.8 for:" + badGroup + " to:" + str(rM.get_cfs_quota(badGroup)))
                            else:
                                if rC.cfs_quotaCut(badGroup, float(self.controlConfig[badGroup]["minimum_setups"]["cpu"] / now_quota)) == -1:
                                    return -1
                                else:
                                    print("do quotaCut until min for:" + badGroup + " now is:" + str(rM.get_cfs_quota(badGroup)))
                        else:
                            print("cut llc for:" + badGroup + " to llc:" + str(hex(llcM.cosLlcNum(llcM.groupCOS[badGroup]))))
                    else:
                        print("give more llc for:" + self.own + " to llc:" + str(hex(llcM.cosLlcNum(llcM.groupCOS[self.own]))))
                # mem-bw-bound
                else:
                    badGroup = rM.findGroupConsumeMostMbl(self.groups,self.own)
                    if badGroup == "":
                        print("Warining: Single process? Just Ignore")
                        return 0
                    now_quota = rM.get_cfs_quota(badGroup)
                    if now_quota * 0.8 > self.controlConfig[badGroup]["minimum_setups"]["cpu"]:
                        if rC.cfs_quotaCut(badGroup, 0.8) == -1:
                            return -1
                    else:
                        if rC.cfs_quotaCut(badGroup, float(
                                self.controlConfig[badGroup]["minimum_setups"]["cpu"] / now_quota)) == -1:
                            return -1
            # core-bound
            else:
                detail_groups = []
                for g in self.groups:
                    detail_groups.append("perf_event/" + g)
                badGroup = rM.getCoGroup("perf_event/" + self.own, detail_groups)# change the input to "cpu/app1" style
                if badGroup == "":
                    print("Warining: Single process? Just Ignore")
                    return 0
                now_quota = rM.get_cfs_quota(badGroup)
                if now_quota * 0.8 > self.controlConfig[badGroup]["minimum_setups"]["cpu"]:
                    if rC.cfs_quotaCut(badGroup, 0.8) == -1:
                        return -1
                else:
                    if rC.cfs_quotaCut(badGroup, float(
                            self.controlConfig[badGroup]["minimum_setups"]["cpu"] / now_quota)) == -1:
                        return -1
        elif boundPart == "Frontend_Bound":
            detail_groups = []
            for g in self.groups:
                detail_groups.append("perf_event/" + g)
            badGroup = rM.getCoGroup("perf_event/" + self.own,detail_groups)# change the input to "cpu/app1" style
            if badGroup == "":
                print("Warining: Single process? Just Ignore")
                return 0
            now_quota = rM.get_cfs_quota(badGroup)
            if now_quota * 0.8 > self.controlConfig[badGroup]["minimum_setups"]["cpu"]:
                if rC.cfs_quotaCut(badGroup, 0.8) == -1:
                    return -1
            else:
                if rC.cfs_quotaCut(badGroup, float(
                        self.controlConfig[badGroup]["minimum_setups"]["cpu"] / now_quota)) == -1:
                    return -1

        else:
            print("Warning: Rule Model can do Nothing more")
            return 0
        if badGroup != "":
            throttled_group.add(badGroup)
        return 0

if __name__ == '__main__':
    pass


