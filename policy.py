import estimator as es
from enum import Enum
class POLICYS(Enum):
    DATA_DRIVEN = 0 
    RULE = 1

class Policy:
    def __init__(self,name,raw_config):
        self.name = name
        self.configJson = raw_config
        self.estimator = es.Estimator()

    def select_throttle_target(self,sample):
        pass

    def test(self):
        if self.estimator.workable() == True:
            print(self.estimator.t)

if __name__ == '__main__':
    p = Policy("f")
    p.estimator.t = False
    p.test()
