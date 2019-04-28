import json
# import logging
import argparse
import time
import policy as po
import resourceMonitor as rM
import resourceControll as rC
import subprocess
from multiprocessing import Process

avaCpus = {8,9,10}


def new_help(cmd):
    # print()
    if subprocess.getstatusoutput("sudo " + cmd)[0] != 0:
        print("Err: Start or Running help shell Fail")


if __name__ == '__main__':
    s_f = []
    try:
        control = 4
        llcM = rC.cat.llcManager(4)
        s = "xapian"
        s1 = "mcf"
        s2 = "lbm"
        s3 = "memaslap"
        s4 = "memcached"
        s5 = "ycsb_memcached"
        if control == 0:# xapian run alone ,with resource limit and in one core
            s_f = ["xapian"]
            rC.createCgroup("cpu,perf_event,cpuset", s)
            rC.cpusSet(avaCpus.pop(), s)
            rC.cpusetMemsSet(0, s)
            rC.startProcs("cpu,perf_event,cpuset", s, "/home/sauron/MAGI/run_" + s)
            time.sleep(3)
            cli_cmd = {'/home/sauron/tailbench-v0.9/xapian/run_xapian_client'}
            newP = Process(target=new_help, args=cli_cmd)
            newP.start()

            # initial period is 100000, give app the maximum
            rC.cfs_quotaSet(s, 60000)
            pids = rM.get_group_pids("perf_event/" + s)
            pa_pids = ','.join([str(i) for i in pids])
            if llcM.givePidSepLlc(pa_pids, 5, s) == -1:
                print("Err: No enough LLC, maybe you need to change config file")

        elif control == 1:#xapian run alone, without resource limit
            s_f = ["xapian"]
            rC.createCgroup("perf_event", s)
            rC.startProcs("perf_event", s, "/home/sauron/MAGI/run_" + s)
            time.sleep(3)
            cli_cmd = {'/home/sauron/tailbench-v0.9/xapian/run_xapian_client'}
            newP = Process(target=new_help, args=cli_cmd)
            newP.start()

        elif control == 2:# xapian run with mcf ,without resource limit and in all cores
            s_f = ["xapian","mcf"]
            rC.createCgroup("perf_event", s)
            rC.startProcs("perf_event", s, "/home/sauron/MAGI/run_" + s)
            time.sleep(3)
            cli_cmd = {'/home/sauron/tailbench-v0.9/xapian/run_xapian_client'}
            newP = Process(target=new_help, args=cli_cmd)
            newP.start()

            rC.createCgroup("perf_event", s1)
            rC.startProcs("perf_event", s1, "/home/sauron/MAGI/run_" + s1)
            rC.createCgroup("perf_event", s2)
            rC.startProcs("perf_event", s2, "/home/sauron/MAGI/run_" + s2)

        elif control == 3:# xapian run with mcf ,without resource limit and in own core
            s_f = ["xapian", "mcf"]
            rC.createCgroup("perf_event,cpuset", s)
            rC.cpusSet(avaCpus.pop(), s)
            rC.cpusetMemsSet(0, s)
            rC.startProcs("perf_event,cpuset", s, "/home/sauron/MAGI/run_" + s)
            time.sleep(3)
            cli_cmd = {'/home/sauron/tailbench-v0.9/xapian/run_xapian_client'}
            newP = Process(target=new_help, args=cli_cmd)
            newP.start()

            rC.createCgroup("perf_event,cpuset", s1)
            rC.cpusSet(avaCpus.pop(), s1)
            rC.cpusetMemsSet(0, s1)
            rC.startProcs("perf_event,cpuset", s1, "/home/sauron/MAGI/run_" + s1)

            rC.createCgroup("perf_event,cpuset", s2)
            rC.cpusSet(avaCpus.pop(), s2)
            rC.cpusetMemsSet(0, s2)
            rC.startProcs("perf_event,cpuset", s2, "/home/sauron/MAGI/run_" + s2)

        elif control == 4:
            s_f = ["memcached"]

            #rC.createCgroup("perf_event", s1)
            #rC.cpusSet(avaCpus.pop(), s1)
            #rC.cpusetMemsSet(0, s1)
            #rC.startProcs("perf_event", s1, "/home/sauron/MAGI/run_" + s1)

            #time.sleep(3)
            #rC.createCgroup("perf_event", s2)
            #rC.cpusSet(avaCpus.pop(), s2)
            #rC.cpusetMemsSet(0, s2)
            #rC.startProcs("perf_event", s2, "/home/sauron/MAGI/run_" + s2)

            rC.createCgroup("perf_event,cpu,cpuset", s4)
            rC.cpusSet(avaCpus.pop(), s4)
            rC.cpusetMemsSet(0, s4)
            rC.startProcs("perf_event,cpu,cpuset", s4, "/home/sauron/MAGI/run_" + s4)
            time.sleep(3)

            # initial period is 100000, give app the maximum


            #time.sleep(3)

            rC.cfs_quotaSet(s4, 60000)
            pids = rM.get_group_pids("perf_event/" + s4)
            pa_pids = ','.join([str(i) for i in pids])

            if llcM.givePidSepLlc(pa_pids, 4, s4) == -1:
                print("Err: No enough LLC, maybe you need to change config file")

            #time.sleep(5)
            #print(subprocess.getoutput("/home/sauron/MAGI/run_"+s5))


        '''
        s = "mcf"
        rC.createCgroup("cpu,perf_event,cpuset", s)
        rC.cpusSet(avaCpus.pop(), s)
        rC.cpusetMemsSet(0, s)
        rC.startProcs("cpu,perf_event,cpuset", s, "/home/sauron/MAGI/run_" + s)
        time.sleep(1)
        cli_cmd = {'/home/sauron/tailbench-v0.9/xapian/run_xapian_client'}
        newP = Process(target=new_help, args=cli_cmd)
        newP.start()

        # initial period is 100000, give app the maximum
        rC.cfs_quotaSet(s, 80000)
        pids = rM.get_group_pids("perf_event/" + s)
        pa_pids = ','.join([str(i) for i in pids])
        if llcM.givePidSepLlc(pa_pids, 6, s) == -1:
            print("Err: No enough LLC, maybe you need to change config file")
'''

        while True:
            time.sleep(10)
    except Exception as err:
        print(err)
    finally:
        #resu = subprocess.getoutput("python2 /home/sauron/tailbench-v0.9/utilities/parselats.py /home/sauron/MAGI/lats.bin").strip().split()
        #print(resu[3])
        #print(resu[8])

        print("do finally")
        if subprocess.getstatusoutput("sudo pqos -R")[0] != 0:
            print("Err: Reset llc fail")
        for s in s_f:
            pids = subprocess.getoutput("sudo cat /sys/fs/cgroup/perf_event/" + s + "/cgroup.procs").strip().split()
            for pid in pids:
                if subprocess.getstatusoutput("sudo kill -9 " + str(pid))[0] != 0:
                    print("Err: Closing test process fail, pid: " + str(pid))
            rC.deleteCgroup("cpu,perf_event,cpuset", s)




