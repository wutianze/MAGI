import estimator as es
import resourceControll as rC
import resourceMonitor as rM
import numpy as np
import math

TRAINCIRCLE = 100

RULEIPCBOUND = 1
RULEMPKIBOUND = 5
RULEMEMBWBOUND = 35
mainExTar = ["lock_loads","fp_uops","branch","l1_misses","l2_misses","stall_sb","branch_misp","machine_clear"]
subTar = ["instructions","cycles","loads_and_stores","cache-misses"]


class Policy:
    def __init__(self,group,groups,control_config,accuracy):
        self.own = group
        self.controlConfig = control_config
        self.estimator = es.Estimator(accuracy)
        self.groups = groups
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
        if self.count == TRAINCIRCLE:
            self.estimator.scaler_init(self.roundHistoryX)
            train_X, train_y = self.estimator.pre_data(self.roundHistoryX, self.roundHistoryy)
            self.historyX += train_X
            self.historyy += train_y
            self.roundHistoryX.clear()
            self.roundHistoryy.clear()# can store to local disk for future use
            self.count = 0
            if train_enable:
                self.estimator.train(train_X, train_y)

    def generate_one_train_data(self, infoList):
        train_X = []
        for tar in subTar:
            train_X.append(infoList[self.own][tar])
        for tar in mainExTar:
            train_X.append(infoList[self.own][tar])
        for g in self.groups:
            if g != self.own:
                for tar in subTar:
                    train_X.append(infoList[g][tar])
        train_y = float(train_X[self.own]["instructions"])/float(train_X[self.own]["cycles"])
        return train_X, train_y


    def train_store(self):
        pass


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
        small_set = self.estimator.find_sv_statisfy_v(self.historyX, self.historyy, float(self.controlConfig["SLA"]))
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


    def set_throttle_setup(self, target, groupCOS):
        curGI = self.currentInfo[self.own]
        # memory-bound
        if float(curGI["instructions"]) / float(curGI["cycles"]) < RULEIPCBOUND and float(
                curGI["cache-misses"]) * 1000.0 / float(curGI["instructions"]) > RULEMPKIBOUND:
            # llc-bound
            if float(rM.cat.getCgroupsMbw([self.own])[self.own]) / 1024.0 < RULEMEMBWBOUND:
                if groupCOS[self.own] != 0:
                    if rC.llcManager.moreLlc(groupCOS[self.own], 2) == -1:  # give 2 more cache
                        if rC.llcManager.lessLlc(groupCOS[target], 2) == -1:
                            rC.cfs_quotaCut(target)
            # mem-bw-bound
            else:
                rC.cfs_quotaCut(target, 0.8)
        # core-bound
        else:
            rC.cfs_quotaCut(target, 0.8)


    def throttle_target_select_setup(self, groupCOS):
        target = self.select_throttle_target()
        if target == "":
            # self.logger.info("Group %s policy %s returns None,fall back",group,policy.name)
            print("Have no targets")
            return -1
        else:
            # self.logger.info("using policy %s to make decision",policy.name)
            self.set_throttle_setup(target, groupCOS)


    # RULE Model
    def rule_update(self, groupCOS):
        boundPart = rM.pmu.topDownGroup(self.own)
        curGI = self.currentInfo[self.own]
        if boundPart == "Backend_Bound":
            # memory-bound
            if float(curGI["instructions"])/float(curGI["cycles"]) < RULEIPCBOUND and float(curGI["cache-misses"])*1000.0/float(curGI["instructions"]) > RULEMPKIBOUND:
                # llc-bound
                if float(rM.cat.getCgroupsMbw([self.own])[self.own])/1024.0 < RULEMEMBWBOUND:
                    # different from paper,need to find a better way
                    if groupCOS[self.own] != 0:
                        if rC.llcManager.moreLlc(groupCOS[self.own], 2) == -1:# give 2 more cache
                            badGroup = rM.findGroupConsumeMostLlc(self.groups, self.own)
                            if rC.llcManager.lessLlc(groupCOS[badGroup],2) == -1:
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


