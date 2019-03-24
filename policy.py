import estimator as es
from enum import Enum
import resourceMonitor as rM
class POLICYS(Enum):
    DATA_DRIVEN = 0 
    RULE = 1

mainExTar = ["lock_loads","fp_uops","branch","l1_misses","l2_misses","stall_sb","branch_misp","machine_clear"]
subTar = ["instructions","cycles","loads_and_stores","cache-misses"]

# a Policy represent a group,it has two models,one is data-driven network the other is rule. It will record what type of data the model need to collect
class Policy:
    def __init__(self,name,groups,control_config):
        self.name = name
        self.controlConfig = control_config
        self.estimator = es.Estimator()
        self.configs = []
        self.groups = groups
        for group in groups:
            for event in subTar:
                add_event(event,group)
            if group == self.name:
                for event in mainExTar:
                    add_event(event,group)

    def add_event(self, event_name, group): 
        if event_name in toEvent.keys(): 
            event_name = toEvent[event_name] 
        self.configs.append((event_name, group)) 
    
    def generate_one_train_data(self,infoList):
        mainD = []
        otherD = []
        for (group,event_name,lineCon) in infoList:
            if group == self.name:

        

    def select_throttle_target(self,group):
        pass

    def test(self):
        if self.estimator.workable() == True:
            print(self.estimator.t)

if __name__ == '__main__':
    p = Policy("f")
    p.estimator.t = False
    p.test()
