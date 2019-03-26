import subprocess

# now only support one network card
def netInOut(count):
    re = subprocess.getoutput("ifstat 1 "+str(count))
    res = re.strip().split()
    #print(re)
    inN = 0.0
    outN = 0.0
    for i in range(count):
        inN = inN + float(res[5+i*2])
        outN = outN + float(res[6+i*2])
        #print(inN,outN)
    inN = inN/float(count)
    outN = outN/float(count)
    return inN, outN

if __name__ == '__main__':
    print(netInOut(int(input('how many counts:'))))
