import psutil

def processInfo(pid):
    p = psutil.Process(pid)
    print(p.cpu_times().user)
    print(p.memory_percent())

pid = int(input())
processInfo(pid)
