import json
import logging

enum POLICYS
{
    DATA_DRIVEN,
    RULE
    }



class MAGI_Controller:
    def __init__(self):
        logging.basicConfig(filename='logger.log',level=logging.INFO)
        logger = logging.getLogger('example1')
        enable_training = True
        sleep_interval = 10

    def run(self):
        if self.enable_training:
            self.try_to_train_model()

        while True:
            if self.sleep_interval > 0:
                time.sleep(self.sleep_interval)

            sample = self.try_to_add_sample()

            if self.enable_detecting:
                self.check_cpu(sample)

    def check_cpu(self,sample):
        group = self.select_low_ipc_group(sample)

        if group is not None:
            self.start_cpu_throttle_analyst(group,sample)
        elif self.have_cpu_throttled_group():
            self.start_cpu_relax_analyst(sample)

    def start_cpu_throttle_analyst(self,group,sample):
        policies = self.ipc_policies[group]

        for p in [POLICYS.DATA_DRIVEN,POLICYS.RULE]:
            policy = policies[p]

            if p == POLICYS.DATA_DRIVEN and (not self.enable_data_driven or not policy.estimator.workable()):
                continue

            if p == POLICYS.RULE:
                l1_sample = self.do_measure_toplev_l1(group)
                deepupdate(sample,l1_sample)

            targets = policy.select_throttle_target(sample)

            if len(targets) == 0:
                self.logger.info("Group %s policy %s returns None,fall back",group,policy.name)
                self.set_throttle_setup(targets)
                break
if __name__ == '__main__':
	configFileName = input("enter the config file path:")
	configFile = open(configFileName,"r")
	configContent = json.loads(configFile.read())
	print(configContent["/apasra/tubo"]["SLA"])

