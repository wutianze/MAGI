
#
# auto generated TopDown/TMAM 3.5-full description for Intel 6th/7th gen Core (code named Skykale/Kabylake)
# Please see http://ark.intel.com for more details on these CPUs.
#
# References:
# http://halobates.de/blog/p/262
# https://sites.google.com/site/analysismethods/yasin-pubs
# https://download.01.org/perfmon/
#

# Helpers

print_error = lambda msg: False
smt_enabled = False
ebs_mode = False
version = "3.5-full"
base_frequency = -1.0
model = ""
Memory = 0

def handle_error(obj, msg):
    print_error(msg)
    obj.errcount += 1
    obj.val = 0
    obj.thresh = False

def handle_error_metric(obj, msg):
    print_error(msg)
    obj.errcount += 1
    obj.val = 0



# Constants

Errata_Whitelist = "SKL091"
Pipeline_Width = 4
Mem_L2_Store_Cost = 9
Mem_L3_Weight = "NA"
Mem_STLB_Hit_Cost = 9
Mem_4K_Alias_Cost = 7
Mem_XSNP_HitM_Cost = 60
MEM_XSNP_Hit_Cost = 43
MEM_XSNP_None_Cost = 29
BAClear_Cost = 9
MS_Switches_Cost = 2
Avg_Assist_Cost = 100
OneMillion = 1000000
OneBillion = 1000000000
Energy_Unit = 61

# Aux. formulas


# Floating Point computational (arithmetic) Operations Count
def FLOP_Count(self, EV, level):
    return (1 *(EV("FP_ARITH_INST_RETIRED.SCALAR_SINGLE", level) + EV("FP_ARITH_INST_RETIRED.SCALAR_DOUBLE", level)) + 2 * EV("FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE", level) + 4 *(EV("FP_ARITH_INST_RETIRED.128B_PACKED_SINGLE", level) + EV("FP_ARITH_INST_RETIRED.256B_PACKED_DOUBLE", level)) + 8 * EV("FP_ARITH_INST_RETIRED.256B_PACKED_SINGLE", level))

def Fetched_Uops(self, EV, level):
    return (EV("IDQ.DSB_UOPS", level) + EV("IDQ.MITE_UOPS", level) + EV("IDQ.MS_UOPS", level))

def Recovery_Cycles(self, EV, level):
    return (EV("INT_MISC.RECOVERY_CYCLES_ANY", level) / 2) if smt_enabled else EV("INT_MISC.RECOVERY_CYCLES", level)

def Execute_Cycles(self, EV, level):
    return (EV("UOPS_EXECUTED.CORE_CYCLES_GE_1", level) / 2) if smt_enabled else EV("UOPS_EXECUTED.CORE_CYCLES_GE_1", level)

def SQ_Full_Cycles(self, EV, level):
    return (EV("OFFCORE_REQUESTS_BUFFER.SQ_FULL", level) / 2) if smt_enabled else EV("OFFCORE_REQUESTS_BUFFER.SQ_FULL", level)

def Cycles_0_Ports_Utilized(self, EV, level):
    return EV("UOPS_EXECUTED.CORE_CYCLES_NONE", level) / 2 if smt_enabled else EV("EXE_ACTIVITY.EXE_BOUND_0_PORTS", level)

def Cycles_1_Port_Utilized(self, EV, level):
    return (EV("UOPS_EXECUTED.CORE_CYCLES_GE_1", level) - EV("UOPS_EXECUTED.CORE_CYCLES_GE_2", level)) / 2 if smt_enabled else EV("EXE_ACTIVITY.1_PORTS_UTIL", level)

def Cycles_2_Ports_Utilized(self, EV, level):
    return (EV("UOPS_EXECUTED.CORE_CYCLES_GE_2", level) - EV("UOPS_EXECUTED.CORE_CYCLES_GE_3", level)) / 2 if smt_enabled else EV("EXE_ACTIVITY.2_PORTS_UTIL", level)

def Cycles_3m_Ports_Utilized(self, EV, level):
    return EV("UOPS_EXECUTED.CORE_CYCLES_GE_3", level) / 2 if smt_enabled else EV("UOPS_EXECUTED.CORE_CYCLES_GE_3", level)

def ORO_DRD_Any_Cycles(self, EV, level):
    return EV(lambda EV , level :  min(EV("CPU_CLK_UNHALTED.THREAD", level) , EV("OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DATA_RD", level)) , level )

def ORO_DRD_BW_Cycles(self, EV, level):
    return EV(lambda EV , level :  min(EV("CPU_CLK_UNHALTED.THREAD", level) , EV("OFFCORE_REQUESTS_OUTSTANDING.ALL_DATA_RD:c4", level)) , level )

def ORO_Demand_RFO_C1(self, EV, level):
    return EV(lambda EV , level :  min(EV("CPU_CLK_UNHALTED.THREAD", level) , EV("OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DEMAND_RFO", level)) , level )

def Store_L2_Hit_Cycles(self, EV, level):
    return EV("L2_RQSTS.RFO_HIT", level)* Mem_L2_Store_Cost *(1 - Mem_Lock_St_Fraction(self, EV, level))

def LOAD_L1_MISS(self, EV, level):
    return EV("MEM_LOAD_RETIRED.L2_HIT", level) + EV("MEM_LOAD_RETIRED.L3_HIT", level) + EV("MEM_LOAD_L3_HIT_RETIRED.XSNP_HIT", level) + EV("MEM_LOAD_L3_HIT_RETIRED.XSNP_HITM", level) + EV("MEM_LOAD_L3_HIT_RETIRED.XSNP_MISS", level)

def LOAD_L1_MISS_NET(self, EV, level):
    return LOAD_L1_MISS(self, EV, level) + EV("MEM_LOAD_RETIRED.L3_MISS", level)

def LOAD_L2_HIT(self, EV, level):
    return EV("MEM_LOAD_RETIRED.L2_HIT", level)*(1 + EV("MEM_LOAD_RETIRED.FB_HIT", level) / LOAD_L1_MISS_NET(self, EV, level))

def LOAD_L3_HIT(self, EV, level):
    return EV("MEM_LOAD_RETIRED.L3_HIT", level)*(1 + EV("MEM_LOAD_RETIRED.FB_HIT", level) / LOAD_L1_MISS_NET(self, EV, level))

def LOAD_XSNP_HIT(self, EV, level):
    return EV("MEM_LOAD_L3_HIT_RETIRED.XSNP_HIT", level)*(1 + EV("MEM_LOAD_RETIRED.FB_HIT", level) / LOAD_L1_MISS_NET(self, EV, level))

def LOAD_XSNP_HITM(self, EV, level):
    return EV("MEM_LOAD_L3_HIT_RETIRED.XSNP_HITM", level)*(1 + EV("MEM_LOAD_RETIRED.FB_HIT", level) / LOAD_L1_MISS_NET(self, EV, level))

def LOAD_XSNP_MISS(self, EV, level):
    return EV("MEM_LOAD_L3_HIT_RETIRED.XSNP_MISS", level)*(1 + EV("MEM_LOAD_RETIRED.FB_HIT", level) / LOAD_L1_MISS_NET(self, EV, level))

def Few_Uops_Executed_Threshold(self, EV, level):
    EV("EXE_ACTIVITY.2_PORTS_UTIL", level)
    return EV("EXE_ACTIVITY.2_PORTS_UTIL", level) if(IPC(self, EV, level)> 1.8)else 0

def Backend_Bound_Cycles(self, EV, level):
    return (EV("EXE_ACTIVITY.EXE_BOUND_0_PORTS", level) + EV("EXE_ACTIVITY.1_PORTS_UTIL", level) + Few_Uops_Executed_Threshold(self, EV, level)) +(EV("CYCLE_ACTIVITY.STALLS_MEM_ANY", level) + EV("EXE_ACTIVITY.BOUND_ON_STORES", level))

def Memory_Bound_Fraction(self, EV, level):
    return (EV("CYCLE_ACTIVITY.STALLS_MEM_ANY", level) + EV("EXE_ACTIVITY.BOUND_ON_STORES", level)) / Backend_Bound_Cycles(self, EV, level)

def L2_Bound_Ratio(self, EV, level):
    return (EV("CYCLE_ACTIVITY.STALLS_L1D_MISS", level) - EV("CYCLE_ACTIVITY.STALLS_L2_MISS", level)) / CLKS(self, EV, level)

def MEM_Bound_Ratio(self, EV, level):
    return EV("CYCLE_ACTIVITY.STALLS_L3_MISS", level) / CLKS(self, EV, level) + L2_Bound_Ratio(self, EV, level) - self.L2_Bound.compute(EV)

def Mem_Lock_St_Fraction(self, EV, level):
    return EV("MEM_INST_RETIRED.LOCK_LOADS", level) / EV("MEM_INST_RETIRED.ALL_STORES", level)

def Mispred_Clears_Fraction(self, EV, level):
    return EV("BR_MISP_RETIRED.ALL_BRANCHES", level) /(EV("BR_MISP_RETIRED.ALL_BRANCHES", level) + EV("MACHINE_CLEARS.COUNT", level))

def Retire_Uop_Fraction(self, EV, level):
    return EV("UOPS_RETIRED.RETIRE_SLOTS", level) / EV("UOPS_ISSUED.ANY", level)

def DurationTimeInSeconds(self, EV, level):
    return 0 if 0 > 0 else(EV("interval-ms", 0) / 1000 )

def HighIPC(self, EV, level):
    return IPC(self, EV, level) / Pipeline_Width

# Instructions Per Cycle (per logical thread)
def IPC(self, EV, level):
    return EV("INST_RETIRED.ANY", level) / CLKS(self, EV, level)

# Uops Per Instruction
def UPI(self, EV, level):
    return EV("UOPS_RETIRED.RETIRE_SLOTS", level) / EV("INST_RETIRED.ANY", level)

# Instruction per taken branch
def IpTB(self, EV, level):
    return EV("INST_RETIRED.ANY", level) / EV("BR_INST_RETIRED.NEAR_TAKEN", level)

# Branch instructions per taken branch. . Can be used to approximate PGO-likelihood for non-loopy codes.
def BpTB(self, EV, level):
    return EV("BR_INST_RETIRED.ALL_BRANCHES", level) / EV("BR_INST_RETIRED.NEAR_TAKEN", level)

# Rough Estimation of fraction of fetched lines bytes that were likely (includes speculatively fetches) consumed by program instructions
def IFetch_Line_Utilization(self, EV, level):
    return min(1 , EV("UOPS_ISSUED.ANY", level) /(UPI(self, EV, level)* 64 *(EV("ICACHE_64B.IFTAG_HIT", level) + EV("ICACHE_64B.IFTAG_MISS", level)) / 4.1))

# Fraction of Uops delivered by the DSB (aka Decoded ICache; or Uop Cache). See section 'Decoded ICache' in Optimization Manual. http://www.intel.com/content/www/us/en/architecture-and-technology/64-ia-32-architectures-optimization-manual.html
def DSB_Coverage(self, EV, level):
    return EV("IDQ.DSB_UOPS", level) / Fetched_Uops(self, EV, level)

# Fraction of Uops delivered by the LSD (Loop Stream Detector; aka Loop Cache)
def LSD_Coverage(self, EV, level):
    return 0

# Cycles Per Instruction (threaded)
def CPI(self, EV, level):
    return 1 / IPC(self, EV, level)

# Per-thread actual clocks when the logical processor is active.
def CLKS(self, EV, level):
    return EV("CPU_CLK_UNHALTED.THREAD", level)

# Total issue-pipeline slots ( per core )
def SLOTS(self, EV, level):
    return Pipeline_Width * CORE_CLKS(self, EV, level)

# Instructions per Load (lower number means loads are more frequent)
def IpL(self, EV, level):
    return EV("INST_RETIRED.ANY", level) / EV("MEM_INST_RETIRED.ALL_LOADS", level)

# Instructions per Store
def IpS(self, EV, level):
    return EV("INST_RETIRED.ANY", level) / EV("MEM_INST_RETIRED.ALL_STORES", level)

# Instructions per Branch
def IpB(self, EV, level):
    return EV("INST_RETIRED.ANY", level) / EV("BR_INST_RETIRED.ALL_BRANCHES", level)

# Instruction per (near) call
def IpCall(self, EV, level):
    return EV("INST_RETIRED.ANY", level) / EV("BR_INST_RETIRED.NEAR_CALL", level)

# Instructions per FP Arithmetic instruction. Approximated prior to BDW.
def IpArith(self, EV, level):
    return EV("INST_RETIRED.ANY", level) /(EV("FP_ARITH_INST_RETIRED.SCALAR_SINGLE", level) + EV("FP_ARITH_INST_RETIRED.SCALAR_DOUBLE", level) + EV("FP_ARITH_INST_RETIRED.256B_PACKED_DOUBLE", level) + EV("FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE", level) + EV("FP_ARITH_INST_RETIRED.128B_PACKED_SINGLE", level) + EV("FP_ARITH_INST_RETIRED.256B_PACKED_SINGLE", level))

# Instructions per FP Arithmetic Scalar Single-Precision instruction.
def IpArith_Scalar_SP(self, EV, level):
    return EV("INST_RETIRED.ANY", level) / EV("FP_ARITH_INST_RETIRED.SCALAR_SINGLE", level)

# Instructions per FP Arithmetic Scalar Double-Precision instruction.
def IpArith_Scalar_DP(self, EV, level):
    return EV("INST_RETIRED.ANY", level) / EV("FP_ARITH_INST_RETIRED.SCALAR_DOUBLE", level)

# Instructions per FP Arithmetic AVX/SSE 128-bit instruction.
def IpArith_AVX128(self, EV, level):
    return EV("INST_RETIRED.ANY", level) /(EV("FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE", level) + EV("FP_ARITH_INST_RETIRED.128B_PACKED_SINGLE", level))

# Instructions per FP Arithmetic AVX* 256-bit instruction.
def IpArith_AVX256(self, EV, level):
    return EV("INST_RETIRED.ANY", level) /(EV("FP_ARITH_INST_RETIRED.256B_PACKED_DOUBLE", level) + EV("FP_ARITH_INST_RETIRED.256B_PACKED_SINGLE", level))

# Total number of retired Instructions
def Instructions(self, EV, level):
    return EV("INST_RETIRED.ANY", level)

# Instructions Per Cycle (per physical core)
def CoreIPC(self, EV, level):
    return EV("INST_RETIRED.ANY", level) / CORE_CLKS(self, EV, level)

# Floating Point Operations Per Cycle
def FLOPc(self, EV, level):
    return FLOP_Count(self, EV, level) / CORE_CLKS(self, EV, level)

# Actual per-core usage of the Floating Point execution units (regardless of the vector width).
def FP_Arith_Utilization(self, EV, level):
    return EV("UOPS_RETIRED.RETIRE_SLOTS", level)*(self.FP_Scalar.compute(EV) + self.FP_Vector.compute(EV)) /(2 * CORE_CLKS(self, EV, level))

# Instruction-Level-Parallelism (average number of uops executed when there is at least 1 uop executed)
def ILP(self, EV, level):
    return EV("UOPS_EXECUTED.THREAD", level) / Execute_Cycles(self, EV, level)

# Branch Misprediction Cost: Fraction of TopDown slots wasted per non-speculative branch misprediction (jeclear)
def Branch_Misprediction_Cost(self, EV, level):
    return (self.Branch_Mispredicts.compute(EV) + self.Frontend_Latency.compute(EV)* self.Mispredicts_Resteers.compute(EV) / self.Frontend_Latency.compute(EV))* SLOTS(self, EV, level) / EV("BR_MISP_RETIRED.ALL_BRANCHES", level)

# Number of Instructions per non-speculative Branch Misprediction (JEClear)
def IpMispredict(self, EV, level):
    return EV("INST_RETIRED.ANY", level) / EV("BR_MISP_RETIRED.ALL_BRANCHES", level)

# Core actual clocks when any thread is active on the physical core
def CORE_CLKS(self, EV, level):
    return ((EV("CPU_CLK_UNHALTED.THREAD", level) / 2)*(1 + EV("CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE", level) / EV("CPU_CLK_UNHALTED.REF_XCLK", level))) if ebs_mode else(EV("CPU_CLK_UNHALTED.THREAD_ANY", level) / 2) if smt_enabled else CLKS(self, EV, level)

# Actual Average Latency for L1 data-cache miss demand loads (in core cycles)
def Load_Miss_Real_Latency(self, EV, level):
    return EV("L1D_PEND_MISS.PENDING", level) /(EV("MEM_LOAD_RETIRED.L1_MISS", level) + EV("MEM_LOAD_RETIRED.FB_HIT", level))

# Memory-Level-Parallelism (average number of L1 miss demand load when there is at least one such miss. Per-thread)
def MLP(self, EV, level):
    return EV("L1D_PEND_MISS.PENDING", level) / EV("L1D_PEND_MISS.PENDING_CYCLES", level)

# Utilization of the core's Page Walker(s) serving STLB misses triggered by instruction/Load/Store accesses
def Page_Walks_Utilization(self, EV, level):
    return (EV("ITLB_MISSES.WALK_PENDING", level) + EV("DTLB_LOAD_MISSES.WALK_PENDING", level) + EV("DTLB_STORE_MISSES.WALK_PENDING", level) + EV("EPT.WALK_PENDING", level)) /(2 * CORE_CLKS(self, EV, level))

# Average data fill bandwidth to the L1 data cache [GB / sec]
def L1D_Cache_Fill_BW(self, EV, level):
    return 64 * EV("L1D.REPLACEMENT", level) / OneBillion / Time(self, EV, level)

# Average data fill bandwidth to the L2 cache [GB / sec]
def L2_Cache_Fill_BW(self, EV, level):
    return 64 * EV("L2_LINES_IN.ALL", level) / OneBillion / Time(self, EV, level)

# Average per-core data fill bandwidth to the L3 cache [GB / sec]
def L3_Cache_Fill_BW(self, EV, level):
    return 64 * EV("LONGEST_LAT_CACHE.MISS", level) / OneBillion / Time(self, EV, level)

# Average per-core data fill bandwidth to the L3 cache [GB / sec]
def L3_Cache_Access_BW(self, EV, level):
    return 64 * EV("OFFCORE_REQUESTS.ALL_REQUESTS", level) / OneBillion / Time(self, EV, level)

# L1 cache true misses per kilo instruction for retired demand loads
def L1MPKI(self, EV, level):
    return 1000 * EV("MEM_LOAD_RETIRED.L1_MISS", level) / EV("INST_RETIRED.ANY", level)

# L2 cache true misses per kilo instruction for retired demand loads
def L2MPKI(self, EV, level):
    return 1000 * EV("MEM_LOAD_RETIRED.L2_MISS", level) / EV("INST_RETIRED.ANY", level)

# L2 cache misses per kilo instruction for all request types (including speculative)
def L2MPKI_All(self, EV, level):
    return 1000 * EV("L2_RQSTS.MISS", level) / EV("INST_RETIRED.ANY", level)

# L2 cache misses per kilo instruction for all demand loads  (including speculative)
def L2MPKI_Load(self, EV, level):
    return 1000 * EV("L2_RQSTS.DEMAND_DATA_RD_MISS", level) / EV("INST_RETIRED.ANY", level)

# L2 cache hits per kilo instruction for all request types (including speculative)
def L2HPKI_All(self, EV, level):
    return 1000 *(EV("L2_RQSTS.REFERENCES", level) - EV("L2_RQSTS.MISS", level)) / EV("INST_RETIRED.ANY", level)

# L2 cache hits per kilo instruction for all demand loads  (including speculative)
def L2HPKI_Load(self, EV, level):
    return 1000 * EV("L2_RQSTS.DEMAND_DATA_RD_HIT", level) / EV("INST_RETIRED.ANY", level)

# L3 cache true misses per kilo instruction for retired demand loads
def L3MPKI(self, EV, level):
    return 1000 * EV("MEM_LOAD_RETIRED.L3_MISS", level) / EV("INST_RETIRED.ANY", level)

# Average CPU Utilization
def CPU_Utilization(self, EV, level):
    return EV("CPU_CLK_UNHALTED.REF_TSC", level) / EV("msr/tsc/", 0)

# Measured Average Frequency for unhalted processors [GHz]
def Average_Frequency(self, EV, level):
    return base_frequency * Turbo_Utilization(self, EV, level) / 1000

# Giga Floating Point Operations Per Second
def GFLOPs(self, EV, level):
    return (FLOP_Count(self, EV, level) / OneBillion) / EV("interval-s", 0)

# Average Frequency Utilization relative nominal frequency
def Turbo_Utilization(self, EV, level):
    return CLKS(self, EV, level) / EV("CPU_CLK_UNHALTED.REF_TSC", level)

# Fraction of cycles where both hardware threads were active
def SMT_2T_Utilization(self, EV, level):
    return 1 - EV("CPU_CLK_THREAD_UNHALTED.ONE_THREAD_ACTIVE", level) /(EV("CPU_CLK_THREAD_UNHALTED.REF_XCLK_ANY", level) / 2) if smt_enabled else 0

# Fraction of cycles spent in Kernel mode
def Kernel_Utilization(self, EV, level):
    return EV("CPU_CLK_UNHALTED.REF_TSC:sup", level) / EV("CPU_CLK_UNHALTED.REF_TSC", level)

# Average external Memory Bandwidth Use for reads and writes [GB / sec]
def DRAM_BW_Use(self, EV, level):
    return 64 *(EV("UNC_ARB_TRK_REQUESTS.ALL", level) + EV("UNC_ARB_COH_TRK_REQUESTS.ALL", level)) / OneMillion / EV("interval-s", 0) / 1000

# Average latency of all requests to external memory (in Uncore cycles)
def MEM_Request_Latency(self, EV, level):
    return EV("UNC_ARB_TRK_OCCUPANCY.ALL", level) / EV("UNC_ARB_TRK_REQUESTS.ALL", level)

# Average number of parallel requests to external memory. Accounts for all requests
def MEM_Parallel_Requests(self, EV, level):
    return EV("UNC_ARB_TRK_OCCUPANCY.ALL", level) / EV("UNC_ARB_TRK_OCCUPANCY.CYCLES_WITH_ANY_REQUEST", level)

# Average latency of data read request to external memory (in nanoseconds). Accounts for demand loads and L1/L2 prefetches
def DRAM_Read_Latency(self, EV, level):
    return OneBillion *(EV("UNC_ARB_TRK_OCCUPANCY.DATA_READ", level) / EV("UNC_ARB_TRK_REQUESTS.DATA_READ", level)) /(Socket_CLKS(self, EV, level) / Time(self, EV, level))

# Average number of parallel data read requests to external memory. Accounts for demand loads and L1/L2 prefetches
def DRAM_Parallel_Reads(self, EV, level):
    return EV("UNC_ARB_TRK_OCCUPANCY.DATA_READ", level) / EV("UNC_ARB_TRK_OCCUPANCY.DATA_READ:c1", level)

# Average latency of data read request to external DRAM memory [in nanoseconds]. Accounts for demand loads and L1/L2 data-read prefetches
def MEM_DRAM_Read_Latency(self, EV, level):
    return 0

# Run duration time in seconds
def Time(self, EV, level):
    return EV("interval-s", 0)

# Socket actual clocks when any core is active on that socket
def Socket_CLKS(self, EV, level):
    return EV("UNC_CLOCK.SOCKET", level)

# Event groups


class Frontend_Bound:
    name = "Frontend_Bound"
    domain = "Slots"
    area = "FE"
    desc = """
This category represents fraction of slots where the
processor's Frontend undersupplies its Backend. Frontend
denotes the first part of the processor core responsible to
fetch operations that are executed later on by the Backend
part. Within the Frontend; a branch predictor predicts the
next address to fetch; cache-lines are fetched from the
memory subsystem; parsed into instructions; and lastly
decoded into micro-ops (uops). Ideally the Frontend can
issue 4 uops every cycle to the Backend. Frontend Bound
denotes unutilized issue-slots when there is no Backend
stall; i.e. bubbles where Frontend delivered no uops while
Backend could have accepted them. For example; stalls due to
instruction-cache misses would be categorized under Frontend
Bound."""
    level = 1
    htoff = False
    sample = ['FRONTEND_RETIRED.LATENCY_GE_8:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['TopDownL1']
    def compute(self, EV):
        try:
            self.val = EV("IDQ_UOPS_NOT_DELIVERED.CORE", 1) / SLOTS(self, EV, 1)
            self.thresh = (self.val > 0.2)
        except ZeroDivisionError:
            handle_error(self, "Frontend_Bound zero division")
        return self.val

class Frontend_Latency:
    name = "Frontend_Latency"
    domain = "Slots"
    area = "FE"
    desc = """
This metric represents fraction of slots the CPU was stalled
due to Frontend latency issues.  For example; instruction-
cache misses; iTLB misses or fetch stalls after a branch
misprediction are categorized under Frontend Latency. In
such cases; the Frontend eventually delivers no uops for
some period."""
    level = 2
    htoff = False
    sample = ['FRONTEND_RETIRED.LATENCY_GE_16:pp', 'FRONTEND_RETIRED.LATENCY_GE_32:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Frontend_Bound', 'TopDownL2']
    def compute(self, EV):
        try:
            self.val = Pipeline_Width * EV("IDQ_UOPS_NOT_DELIVERED.CYCLES_0_UOPS_DELIV.CORE", 2) / SLOTS(self, EV, 2)
            self.thresh = (self.val > 0.15) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Frontend_Latency zero division")
        return self.val

class ICache_Misses:
    name = "ICache_Misses"
    domain = "Clocks"
    area = "FE"
    desc = """
This metric represents fraction of cycles the CPU was
stalled due to instruction cache misses.. Using compiler's
Profile-Guided Optimization (PGO) can reduce i-cache misses
through improved hot code layout."""
    level = 3
    htoff = False
    sample = ['FRONTEND_RETIRED.L2_MISS:pp', 'FRONTEND_RETIRED.L1I_MISS:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Frontend_Latency']
    def compute(self, EV):
        try:
            self.val = (EV("ICACHE_16B.IFDATA_STALL", 3) + 2 * EV("ICACHE_16B.IFDATA_STALL:c1:e1", 3)) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.05) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "ICache_Misses zero division")
        return self.val

class ITLB_Misses:
    name = "ITLB_Misses"
    domain = "Clocks"
    area = "FE"
    desc = """
This metric represents fraction of cycles the CPU was
stalled due to instruction TLB misses.. Consider large 2M
pages for code (selectively prefer hot large-size function,
due to limited 2M entries). Linux options: standard binaries
use libhugetlbfs; Hfsort.. https://github.com/libhugetlbfs/l
ibhugetlbfs;https://research.fb.com/publications/optimizing-
function-placement-for-large-scale-data-center-
applications-2/"""
    level = 3
    htoff = False
    sample = ['FRONTEND_RETIRED.STLB_MISS:pp', 'FRONTEND_RETIRED.ITLB_MISS:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Frontend_Latency', 'TLB']
    def compute(self, EV):
        try:
            self.val = EV("ICACHE_64B.IFTAG_STALL", 3) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.05) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "ITLB_Misses zero division")
        return self.val

class Branch_Resteers:
    name = "Branch_Resteers"
    domain = "Clocks_Estimated"
    area = "FE"
    desc = """
This metric represents fraction of cycles the CPU was
stalled due to Branch Resteers. Branch Resteers estimates
the Frontend delay in fetching operations from corrected
path; following all sorts of miss-predicted branches. For
example; branchy code with lots of miss-predictions might
get categorized under Branch Resteers. Note the value of
this node may overlap with its siblings."""
    level = 3
    htoff = False
    sample = ['BR_MISP_RETIRED.ALL_BRANCHES:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Bad_Speculation', 'Frontend_Latency']
    def compute(self, EV):
        try:
            self.val = (EV("INT_MISC.CLEAR_RESTEER_CYCLES", 3) + BAClear_Cost * EV("BACLEARS.ANY", 3)) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.05) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Branch_Resteers zero division")
        return self.val

class Mispredicts_Resteers:
    name = "Mispredicts_Resteers"
    domain = "Clocks"
    area = "FE"
    desc = """
This metric represents fraction of cycles the CPU was
stalled due to Branch Resteers as a result of Branch
Misprediction at execution stage."""
    level = 4
    htoff = False
    sample = ['BR_MISP_RETIRED.ALL_BRANCHES:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Branch_Mispredicts']
    def compute(self, EV):
        try:
            self.val = Mispred_Clears_Fraction(self, EV, 4)* EV("INT_MISC.CLEAR_RESTEER_CYCLES", 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.05) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Mispredicts_Resteers zero division")
        return self.val

class Clears_Resteers:
    name = "Clears_Resteers"
    domain = "Clocks"
    area = "FE"
    desc = """
This metric represents fraction of cycles the CPU was
stalled due to Branch Resteers as a result of Machine
Clears."""
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Machine_Clears']
    def compute(self, EV):
        try:
            self.val = (1 - Mispred_Clears_Fraction(self, EV, 4))* EV("INT_MISC.CLEAR_RESTEER_CYCLES", 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.05) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Clears_Resteers zero division")
        return self.val

class Unknown_Branches:
    name = "Unknown_Branches"
    domain = "Clocks_Estimated"
    area = "FE"
    desc = """
This metric represents fraction of cycles the CPU was
stalled due to new branch address clears. These are fetched
branches the Branch Prediction Unit was unable to recognize
(First fetch or hitting BPU capacity limit)."""
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Unknown_Branches']
    def compute(self, EV):
        try:
            self.val = self.Branch_Resteers.compute(EV) - EV("INT_MISC.CLEAR_RESTEER_CYCLES", 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.05) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Unknown_Branches zero division")
        return self.val

class DSB_Switches:
    name = "DSB_Switches"
    domain = "Clocks"
    area = "FE"
    desc = """
This metric represents fraction of cycles the CPU was
stalled due to switches from DSB to MITE pipelines. The DSB
(decoded i-cache; introduced with the Sandy Bridge
microarchitecture) pipeline has shorter latency and
delivered higher bandwidth than the MITE (legacy instruction
decode pipeline). Switching between the two pipelines can
cause penalties. This metric estimates when such penalty can
be exposed. Optimizing for better DSB hit rate may be
considered.. See section 'Optimization for Decoded Icache'
in Optimization Manual:.
http://www.intel.com/content/www/us/en/architecture-and-
technology/64-ia-32-architectures-optimization-manual.html"""
    level = 3
    htoff = False
    sample = ['FRONTEND_RETIRED.DSB_MISS:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['DSB', 'Frontend_Latency']
    def compute(self, EV):
        try:
            self.val = EV("DSB2MITE_SWITCHES.PENALTY_CYCLES", 3) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.05) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "DSB_Switches zero division")
        return self.val

class LCP:
    name = "LCP"
    domain = "Clocks"
    area = "FE"
    desc = """
This metric represents fraction of cycles CPU was stalled
due to Length Changing Prefixes (LCPs). Using proper
compiler flags or Intel Compiler by default will certainly
avoid this."""
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Frontend_Latency']
    def compute(self, EV):
        try:
            self.val = EV("ILD_STALL.LCP", 3) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.05) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "LCP zero division")
        return self.val

class MS_Switches:
    name = "MS_Switches"
    domain = "Clocks"
    area = "FE"
    desc = """
This metric estimates the fraction of cycles when the CPU
was stalled due to switches of uop delivery to the Microcode
Sequencer (MS). Commonly used instructions are optimized for
delivery by the DSB (decoded i-cache) or MITE (legacy
instruction decode) pipelines. Certain operations cannot be
handled natively by the execution pipeline; and must be
performed by microcode (small programs injected into the
execution stream). Switching to the MS too often can
negatively impact performance. The MS is designated to
deliver long uop flows required by CISC instructions like
CPUID; or uncommon conditions like Floating Point Assists
when dealing with Denormals."""
    level = 3
    htoff = False
    sample = ['IDQ.MS_SWITCHES']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Frontend_Latency', 'Microcode_Sequencer']
    def compute(self, EV):
        try:
            self.val = MS_Switches_Cost * EV("IDQ.MS_SWITCHES", 3) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.05) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "MS_Switches zero division")
        return self.val

class Frontend_Bandwidth:
    name = "Frontend_Bandwidth"
    domain = "Slots"
    area = "FE"
    desc = """
This metric represents fraction of slots the CPU was stalled
due to Frontend bandwidth issues.  For example;
inefficiencies at the instruction decoders; or code
restrictions for caching in the DSB (decoded uops cache) are
categorized under Frontend Bandwidth. In such cases; the
Frontend typically delivers non-optimal amount of uops to
the Backend (less than four)."""
    level = 2
    htoff = False
    sample = ['FRONTEND_RETIRED.LATENCY_GE_2_BUBBLES_GE_1:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Frontend_Bound', 'TopDownL2']
    def compute(self, EV):
        try:
            self.val = self.Frontend_Bound.compute(EV) - self.Frontend_Latency.compute(EV)
            self.thresh = (self.val > 0.1) & self.parent.thresh & (HighIPC(self, EV, 2) > 0)
        except ZeroDivisionError:
            handle_error(self, "Frontend_Bandwidth zero division")
        return self.val

class MITE:
    name = "MITE"
    domain = "CoreClocks"
    area = "FE"
    desc = """
This metric represents Core fraction of cycles in which CPU
was likely limited due to the MITE pipeline (Legacy Decode
Pipeline). This pipeline is used for code that was not pre-
cached in the DSB or LSD. For example; inefficiencies in the
instruction decoders are categorized here.. Consider tuning
codegen of 'small hotspots' that can fit in DSB. Read about
'Decoded ICache' in Optimization Manual:.
http://www.intel.com/content/www/us/en/architecture-and-
technology/64-ia-32-architectures-optimization-manual.html"""
    level = 3
    htoff = False
    sample = ['FRONTEND_RETIRED.DSB_MISS:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Frontend_Bandwidth']
    def compute(self, EV):
        try:
            self.val = (EV("IDQ.ALL_MITE_CYCLES_ANY_UOPS", 3) - EV("IDQ.ALL_MITE_CYCLES_4_UOPS", 3)) / CORE_CLKS(self, EV, 3)
            self.thresh = (self.val > 0.1) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "MITE zero division")
        return self.val

class DSB:
    name = "DSB"
    domain = "CoreClocks"
    area = "FE"
    desc = """
This metric represents Core fraction of cycles in which CPU
was likely limited due to DSB (decoded uop cache) fetch
pipeline.  For example; inefficient utilization of the DSB
cache structure or bank conflict when reading from it; are
categorized here."""
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['DSB', 'Frontend_Bandwidth']
    def compute(self, EV):
        try:
            self.val = (EV("IDQ.ALL_DSB_CYCLES_ANY_UOPS", 3) - EV("IDQ.ALL_DSB_CYCLES_4_UOPS", 3)) / CORE_CLKS(self, EV, 3)
            self.thresh = (self.val > 0.3) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "DSB zero division")
        return self.val

class LSD:
    name = "LSD"
    domain = "CoreClocks"
    area = "FE"
    desc = """
This metric represents Core fraction of cycles in which CPU
was likely limited due to LSD (Loop Stream Detector) unit.
LSD typically does well sustaining Uop supply. However; in
some rare cases; optimal uop-delivery could not be reached
for small loops whose size (in terms of number of uops) does
not suit well the LSD structure."""
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Frontend_Bandwidth', 'LSD']
    def compute(self, EV):
        try:
            self.val = 0
            self.thresh = (self.val > 0.1) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "LSD zero division")
        return self.val

class Bad_Speculation:
    name = "Bad_Speculation"
    domain = "Slots"
    area = "BAD"
    desc = """
This category represents fraction of slots wasted due to
incorrect speculations. This include slots used to issue
uops that do not eventually get retired and slots for which
the issue-pipeline was blocked due to recovery from earlier
incorrect speculation. For example; wasted work due to miss-
predicted branches are categorized under Bad Speculation
category. Incorrect data speculation followed by Memory
Ordering Nukes is another example."""
    level = 1
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Bad_Speculation', 'TopDownL1']
    def compute(self, EV):
        try:
            self.val = (EV("UOPS_ISSUED.ANY", 1) - EV("UOPS_RETIRED.RETIRE_SLOTS", 1) + Pipeline_Width * Recovery_Cycles(self, EV, 1)) / SLOTS(self, EV, 1)
            self.thresh = (self.val > 0.1)
        except ZeroDivisionError:
            handle_error(self, "Bad_Speculation zero division")
        return self.val

class Branch_Mispredicts:
    name = "Branch_Mispredicts"
    domain = "Slots"
    area = "BAD"
    desc = """
This metric represents fraction of slots the CPU has wasted
due to Branch Misprediction.  These slots are either wasted
by uops fetched from an incorrectly speculated program path;
or stalls when the out-of-order part of the machine needs to
recover its state from a speculative path.. Using profile
feedback in the compiler may help. Please see the
Optimization Manual for general strategies for addressing
branch misprediction issues..
http://www.intel.com/content/www/us/en/architecture-and-
technology/64-ia-32-architectures-optimization-manual.html"""
    level = 2
    htoff = False
    sample = ['BR_MISP_RETIRED.ALL_BRANCHES:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Bad_Speculation', 'Branch_Mispredicts', 'TopDownL2']
    def compute(self, EV):
        try:
            self.val = Mispred_Clears_Fraction(self, EV, 2)* self.Bad_Speculation.compute(EV)
            self.thresh = (self.val > 0.05) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Branch_Mispredicts zero division")
        return self.val

class Machine_Clears:
    name = "Machine_Clears"
    domain = "Slots"
    area = "BAD"
    desc = """
This metric represents fraction of slots the CPU has wasted
due to Machine Clears.  These slots are either wasted by
uops fetched prior to the clear; or stalls the out-of-order
portion of the machine needs to recover its state after the
clear. For example; this can happen due to memory ordering
Nukes (e.g. Memory Disambiguation) or Self-Modifying-Code
(SMC) nukes.. See \"Memory Disambiguation\" in Optimization
Manual and:. https://software.intel.com/sites/default/files/
m/d/4/1/d/8/sma.pdf"""
    level = 2
    htoff = False
    sample = ['MACHINE_CLEARS.COUNT']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Bad_Speculation', 'Machine_Clears', 'TopDownL2']
    def compute(self, EV):
        try:
            self.val = self.Bad_Speculation.compute(EV) - self.Branch_Mispredicts.compute(EV)
            self.thresh = (self.val > 0.05) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Machine_Clears zero division")
        return self.val

class Backend_Bound:
    name = "Backend_Bound"
    domain = "Slots"
    area = "BE"
    desc = """
This category represents fraction of slots where no uops are
being delivered due to a lack of required resources for
accepting new uops in the Backend. Backend is the portion of
the processor core where the out-of-order scheduler
dispatches ready uops into their respective execution units;
and once completed these uops get retired according to
program order. For example; stalls due to data-cache misses
or stalls due to the divider unit being overloaded are both
categorized under Backend Bound. Backend Bound is further
divided into two main categories: Memory Bound and Core
Bound."""
    level = 1
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['TopDownL1']
    def compute(self, EV):
        try:
            self.val = 1 -(self.Frontend_Bound.compute(EV) + self.Bad_Speculation.compute(EV) + self.Retiring.compute(EV))
            self.thresh = (self.val > 0.1)
        except ZeroDivisionError:
            handle_error(self, "Backend_Bound zero division")
        return self.val

class Memory_Bound:
    name = "Memory_Bound"
    domain = "Slots"
    area = "BE/Mem"
    desc = """
This metric represents fraction of slots the Memory
subsystem within the Backend was a bottleneck.  Memory Bound
estimates fraction of slots where pipeline is likely stalled
due to demand load or store instructions. This accounts
mainly for (1) non-completed in-flight memory demand loads
which coincides with execution units starvation; in addition
to (2) cases where stores could impose backpressure on the
pipeline when many of them get buffered at the same time
(less common out of the two)."""
    level = 2
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Backend_Bound', 'TopDownL2']
    def compute(self, EV):
        try:
            self.val = Memory_Bound_Fraction(self, EV, 2)* self.Backend_Bound.compute(EV)
            self.thresh = (self.val > 0.1) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Memory_Bound zero division")
        return self.val

class L1_Bound:
    name = "L1_Bound"
    domain = "Stalls"
    area = "BE/Mem"
    desc = """
This metric estimates how often the CPU was stalled without
loads missing the L1 data cache.  The L1 data cache
typically has the shortest latency.  However; in certain
cases like loads blocked on older stores; a load might
suffer due to high latency even though it is being satisfied
by the L1. Another example is loads who miss in the TLB.
These cases are characterized by execution unit stalls;
while some non-completed demand load lives in the machine
without having that demand load missing the L1 cache."""
    level = 3
    htoff = False
    sample = ['MEM_LOAD_RETIRED.L1_HIT:pp', 'MEM_LOAD_RETIRED.FB_HIT:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Cache_Misses', 'Memory_Bound']
    def compute(self, EV):
        try:
            self.val = (EV("CYCLE_ACTIVITY.STALLS_MEM_ANY", 3) - EV("CYCLE_ACTIVITY.STALLS_L1D_MISS", 3)) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.1) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "L1_Bound zero division")
        return self.val

class DTLB_Load:
    name = "DTLB_Load"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    desc = """
This metric roughly estimates the fraction of cycles where
the TLB was missed by load accesses. TLBs (Translation Look-
aside Buffers) are processor caches for recently used
entries out of the Page Tables that are used to map virtual-
to physical-addresses by the operating system. This metric
approximates the potential delay of demand loads missing the
first-level data TLB (assuming worst case scenario with back
to back misses to different pages). This includes hitting in
the second-level TLB (STLB) as well as performing a hardware
page walk on an STLB miss.."""
    level = 4
    htoff = False
    sample = ['MEM_INST_RETIRED.STLB_MISS_LOADS:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['TLB']
    def compute(self, EV):
        try:
            self.val = (Mem_STLB_Hit_Cost * EV("DTLB_LOAD_MISSES.STLB_HIT", 4) + EV("DTLB_LOAD_MISSES.WALK_ACTIVE", 4)) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.1) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "DTLB_Load zero division")
        return self.val

class Store_Fwd_Blk:
    name = "Store_Fwd_Blk"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    desc = """
This metric roughly estimates fraction of cycles when the
memory subsystem had loads blocked since they could not
forward data from earlier (in program order) overlapping
stores. To streamline memory operations in the pipeline; a
load can avoid waiting for memory if a prior in-flight store
is writing the data that the load wants to read (store
forwarding process). However; in some cases the load may be
blocked for a significant time pending the store forward.
For example; when the prior store is writing a smaller
region than the load is reading."""
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = 13 * EV("LD_BLOCKS.STORE_FORWARD", 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.1) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Store_Fwd_Blk zero division")
        return self.val

class Lock_Latency:
    name = "Lock_Latency"
    domain = "Clocks"
    area = "BE/Mem"
    desc = """
This metric represents fraction of cycles the CPU spent
handling cache misses due to lock operations. Due to the
microarchitecture handling of locks; they are classified as
L1_Bound regardless of what memory source satisfied them."""
    level = 4
    htoff = False
    sample = ['MEM_INST_RETIRED.LOCK_LOADS:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = Mem_Lock_St_Fraction(self, EV, 4)* ORO_Demand_RFO_C1(self, EV, 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.2) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Lock_Latency zero division")
        return self.val

class Split_Loads:
    name = "Split_Loads"
    domain = "Clocks_Calculated"
    area = "BE/Mem"
    desc = """
This metric estimates fraction of cycles handling memory
load split accesses - load that cross 64-byte cacheline
boundary. . Consider aligning data or hot structure fields.
See the Optimization Manual for more details"""
    level = 4
    htoff = False
    sample = ['MEM_INST_RETIRED.SPLIT_LOADS:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = Load_Miss_Real_Latency(self, EV, 4)* EV("LD_BLOCKS.NO_SR", 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.2) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Split_Loads zero division")
        return self.val

class G4K_Aliasing:
    name = "4K_Aliasing"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    desc = """
This metric estimates how often memory load accesses were
aliased by preceding stores (in program order) with a 4K
address offset. False match is possible; which incur a few
cycles load re-issue. However; the short re-issue duration
is often hidden by the out-of-order core and HW
optimizations; hence a user may safely ignore a high value
of this metric unless it manages to propagate up into parent
nodes of the hierarchy (e.g. to L1_Bound).. Consider
reducing independent loads/stores accesses with 4K offsets.
See the Optimization Manual for more details"""
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("LD_BLOCKS_PARTIAL.ADDRESS_ALIAS", 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.2) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "G4K_Aliasing zero division")
        return self.val

class FB_Full:
    name = "FB_Full"
    domain = "Clocks_Calculated"
    area = "BE/Mem"
    desc = """
This metric does a *rough estimation* of how often L1D Fill
Buffer unavailability limited additional L1D miss memory
access requests to proceed. The higher the metric value; the
deeper the memory hierarchy level the misses are satisfied
from (metric values >1 are valid). Often it hints on
approaching bandwidth limits (to L2 cache; L3 cache or
external memory).. See $issueBW and $issueSL hints. Avoid
software prefetches if indeed memory BW limited."""
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Memory_BW']
    def compute(self, EV):
        try:
            self.val = Load_Miss_Real_Latency(self, EV, 4)* EV("L1D_PEND_MISS.FB_FULL:c1", 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.3)
        except ZeroDivisionError:
            handle_error(self, "FB_Full zero division")
        return self.val

class L2_Bound:
    name = "L2_Bound"
    domain = "Stalls"
    area = "BE/Mem"
    desc = """
This metric estimates how often the CPU was stalled due to
L2 cache accesses by loads.  Avoiding cache misses (i.e. L1
misses/L2 hits) can improve the latency and increase
performance."""
    level = 3
    htoff = False
    sample = ['MEM_LOAD_RETIRED.L2_HIT:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Cache_Misses', 'Memory_Bound']
    def compute(self, EV):
        try:
            self.val = (1 if self.FB_Full.compute(EV)< 1.5 else LOAD_L2_HIT(self, EV, 3) /(LOAD_L2_HIT(self, EV, 3) + EV("L1D_PEND_MISS.FB_FULL:c1", 3)))* L2_Bound_Ratio(self, EV, 3)
            EV("L1D_PEND_MISS.FB_FULL:c1", 3)
            L2_Bound_Ratio(self, EV, 3)
            LOAD_L2_HIT(self, EV, 3)
            self.thresh = (self.val > 0.05) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "L2_Bound zero division")
        return self.val

class L3_Bound:
    name = "L3_Bound"
    domain = "Stalls"
    area = "BE/Mem"
    desc = """
This metric estimates how often the CPU was stalled due to
loads accesses to L3 cache or contended with a sibling Core.
Avoiding cache misses (i.e. L2 misses/L3 hits) can improve
the latency and increase performance."""
    level = 3
    htoff = False
    sample = ['MEM_LOAD_RETIRED.L3_HIT:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Cache_Misses', 'Memory_Bound']
    def compute(self, EV):
        try:
            self.val = (EV("CYCLE_ACTIVITY.STALLS_L2_MISS", 3) - EV("CYCLE_ACTIVITY.STALLS_L3_MISS", 3)) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.05) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "L3_Bound zero division")
        return self.val

class Contested_Accesses:
    name = "Contested_Accesses"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    desc = """
This metric estimates fraction of cycles while the memory
subsystem was handling contested accesses. Contested
accesses occur when data written by one thread are read by
another thread on a different physical core. Examples of
contested accesses include synchronizations such as locks;
true data sharing such as modified locked variables; and
false sharing."""
    level = 4
    htoff = False
    sample = ['MEM_LOAD_L3_HIT_RETIRED.XSNP_HITM:pp', 'MEM_LOAD_L3_HIT_RETIRED.XSNP_MISS:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Data_Sharing']
    def compute(self, EV):
        try:
            self.val = Mem_XSNP_HitM_Cost *(LOAD_XSNP_HITM(self, EV, 4) + LOAD_XSNP_MISS(self, EV, 4)) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.2) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Contested_Accesses zero division")
        return self.val

class Data_Sharing:
    name = "Data_Sharing"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    desc = """
This metric estimates fraction of cycles while the memory
subsystem was handling data-sharing accesses. Data shared by
multiple threads (even just read shared) may cause increased
access latency due to cache coherency. Excessive data
sharing can drastically harm multithreaded performance."""
    level = 4
    htoff = False
    sample = ['MEM_LOAD_L3_HIT_RETIRED.XSNP_HIT:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = MEM_XSNP_Hit_Cost * LOAD_XSNP_HIT(self, EV, 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.2) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Data_Sharing zero division")
        return self.val

class L3_Hit_Latency:
    name = "L3_Hit_Latency"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    desc = """
This metric represents fraction of cycles with demand load
accesses that hit the L3 cache under unloaded scenarios
(possibly L3 latency limited).  Avoiding private cache
misses (i.e. L2 misses/L3 hits) will improve the latency;
reduce contention with sibling physical cores and increase
performance.  Note the value of this node may overlap with
its siblings."""
    level = 4
    htoff = False
    sample = ['MEM_LOAD_RETIRED.L3_HIT:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Memory_Lat']
    def compute(self, EV):
        try:
            self.val = MEM_XSNP_None_Cost * LOAD_L3_HIT(self, EV, 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.1) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "L3_Hit_Latency zero division")
        return self.val

class SQ_Full:
    name = "SQ_Full"
    domain = "CoreClocks"
    area = "BE/Mem"
    desc = """
This metric measures fraction of cycles where the Super
Queue (SQ) was full taking into account all request-types
and both hardware SMT threads. The Super Queue is used for
requests to access the L2 cache or to go out to the Uncore."""
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Memory_BW']
    def compute(self, EV):
        try:
            self.val = SQ_Full_Cycles(self, EV, 4) / CORE_CLKS(self, EV, 4)
            self.thresh = (self.val > 0.3) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "SQ_Full zero division")
        return self.val

class DRAM_Bound:
    name = "DRAM_Bound"
    domain = "Stalls"
    area = "BE/Mem"
    desc = """
This metric estimates how often the CPU was stalled on
accesses to external memory (DRAM) by loads. Better caching
can improve the latency and increase performance."""
    level = 3
    htoff = False
    sample = ['MEM_LOAD_RETIRED.L3_MISS:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Memory_Bound']
    def compute(self, EV):
        try:
            self.val = MEM_Bound_Ratio(self, EV, 3)
            self.thresh = (self.val > 0.1) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "DRAM_Bound zero division")
        return self.val

class MEM_Bandwidth:
    name = "MEM_Bandwidth"
    domain = "Clocks"
    area = "BE/Mem"
    desc = """
This metric estimates fraction of cycles where the core's
performance was likely hurt due to approaching bandwidth
limits of external memory (DRAM).  The underlying heuristic
assumes that a similar off-core traffic is generated by all
IA cores. This metric does not aggregate non-data-read
requests by this thread; requests from other IA
threads/cores/sockets; or other non-IA devices like GPU;
hence the maximum external memory bandwidth limits may or
may not be approached when this metric is flagged (see
Uncore counters for that).. Improve data accesses to reduce
cacheline transfers from/to memory. Examples: 1) Consume all
bytes of a each cacheline before it is evicted (e.g. reorder
structure elements and split non-hot ones), 2) merge
computed-limited with BW-limited loops, 3) NUMA
optimizations in multi-socket system. Note: software
prefetches will not help BW-limited application.."""
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Memory_BW']
    def compute(self, EV):
        try:
            self.val = ORO_DRD_BW_Cycles(self, EV, 4) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.1) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "MEM_Bandwidth zero division")
        return self.val

class MEM_Latency:
    name = "MEM_Latency"
    domain = "Clocks"
    area = "BE/Mem"
    desc = """
This metric estimates fraction of cycles where the
performance was likely hurt due to latency from external
memory (DRAM).  This metric does not aggregate requests from
other threads/cores/sockets (see Uncore counters for that)..
Improve data accesses or interleave them with compute.
Examples: 1) Data layout re-structuring, 2) Software
Prefetches (also through the compiler).."""
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Memory_Lat']
    def compute(self, EV):
        try:
            self.val = ORO_DRD_Any_Cycles(self, EV, 4) / CLKS(self, EV, 4) - self.MEM_Bandwidth.compute(EV)
            self.thresh = (self.val > 0.1) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "MEM_Latency zero division")
        return self.val

class Store_Bound:
    name = "Store_Bound"
    domain = "Stalls"
    area = "BE/Mem"
    desc = """
This metric estimates how often CPU was stalled  due to
store memory accesses. Even though store accesses do not
typically stall out-of-order CPUs; there are few cases where
stores can lead to actual stalls. This metric will be
flagged should any of these cases be a bottleneck."""
    level = 3
    htoff = False
    sample = ['MEM_INST_RETIRED.ALL_STORES:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Memory_Bound']
    def compute(self, EV):
        try:
            self.val = EV("EXE_ACTIVITY.BOUND_ON_STORES", 3) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.2) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Store_Bound zero division")
        return self.val

class Store_Latency:
    name = "Store_Latency"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    desc = """
This metric estimates fraction of cycles the CPU spent
handling L1D store misses. Store accesses usually less
impact out-of-order core performance; however; holding
resources for longer time can lead into undesired
implications (e.g. contention on L1D fill-buffer entries -
see FB_Full). Consider to avoid/reduce unnecessary (or
easily load-able/computable) memory store."""
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Memory_Lat']
    def compute(self, EV):
        try:
            self.val = (Store_L2_Hit_Cycles(self, EV, 4) +(1 - Mem_Lock_St_Fraction(self, EV, 4))* ORO_Demand_RFO_C1(self, EV, 4)) / CLKS(self, EV, 4)
            self.thresh = (self.val > 0.1) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Store_Latency zero division")
        return self.val

class Split_Stores:
    name = "Split_Stores"
    domain = "CoreClocks"
    area = "BE/Mem"
    desc = """
This metric represents rate of split store accesses.
Consider aligning your data to the 64-byte cache line
granularity."""
    level = 4
    htoff = False
    sample = ['MEM_INST_RETIRED.SPLIT_STORES:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("MEM_INST_RETIRED.SPLIT_STORES", 4) / CORE_CLKS(self, EV, 4)
            self.thresh = (self.val > 0.2) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Split_Stores zero division")
        return self.val

class DTLB_Store:
    name = "DTLB_Store"
    domain = "Clocks_Estimated"
    area = "BE/Mem"
    desc = """
This metric represents fraction of cycles spent handling
first-level data TLB store misses.  As with ordinary data
caching; focus on improving data locality and reducing
working-set size to reduce DTLB overhead.  Additionally;
consider using profile-guided optimization (PGO) to
collocate frequently-used data on the same page.  Try using
larger page sizes for large amounts of frequently-used data."""
    level = 4
    htoff = False
    sample = ['MEM_INST_RETIRED.STLB_MISS_STORES:pp']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['TLB']
    def compute(self, EV):
        try:
            self.val = (Mem_STLB_Hit_Cost * EV("DTLB_STORE_MISSES.STLB_HIT", 4) + EV("DTLB_STORE_MISSES.WALK_ACTIVE", 4)) / CORE_CLKS(self, EV, 4)
            self.thresh = (self.val > 0.05) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "DTLB_Store zero division")
        return self.val

class Core_Bound:
    name = "Core_Bound"
    domain = "Slots"
    area = "BE/Core"
    desc = """
This metric represents fraction of slots where Core non-
memory issues were of a bottleneck.  Shortage in hardware
compute resources; or dependencies in software's
instructions are both categorized under Core Bound. Hence it
may indicate the machine ran out of an out-of-order
resource; certain execution units are overloaded or
dependencies in program's data- or instruction-flow are
limiting the performance (e.g. FP-chained long-latency
arithmetic operations).. Tip: consider Port Saturation
analysis as next step."""
    level = 2
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Backend_Bound', 'TopDownL2']
    def compute(self, EV):
        try:
            self.val = self.Backend_Bound.compute(EV) - self.Memory_Bound.compute(EV)
            self.thresh = (self.val > 0.1) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Core_Bound zero division")
        return self.val

class Divider:
    name = "Divider"
    domain = "Clocks"
    area = "BE/Core"
    desc = """
This metric represents fraction of cycles where the Divider
unit was active. Divide and square root instructions are
performed by the Divider unit and can take considerably
longer latency than integer or Floating Point addition;
subtraction; or multiplication."""
    level = 3
    htoff = False
    sample = ['ARITH.DIVIDER_ACTIVE']
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("ARITH.DIVIDER_ACTIVE", 3) / CLKS(self, EV, 3)
            self.thresh = (self.val > 0.2) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Divider zero division")
        return self.val

class Ports_Utilization:
    name = "Ports_Utilization"
    domain = "Clocks"
    area = "BE/Core"
    desc = """
This metric estimates fraction of cycles the CPU performance
was potentially limited due to Core computation issues (non
divider-related).  Two distinct categories can be attributed
into this metric: (1) heavy data-dependency among contiguous
instructions would manifest in this metric - such cases are
often referred to as low Instruction Level Parallelism
(ILP). (2) Contention on some hardware execution unit other
than Divider. For example; when there are too many multiply
operations.. Loop Vectorization -most compilers feature
auto-Vectorization options today- reduces pressure on the
execution ports as multiple elements are calculated with
same uop."""
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = (Backend_Bound_Cycles(self, EV, 3) - EV("CYCLE_ACTIVITY.STALLS_MEM_ANY", 3) - EV("EXE_ACTIVITY.BOUND_ON_STORES", 3)) / CLKS(self, EV, 3) if(EV("ARITH.DIVIDER_ACTIVE", 3)< EV("EXE_ACTIVITY.EXE_BOUND_0_PORTS", 3))else(Backend_Bound_Cycles(self, EV, 3) - EV("CYCLE_ACTIVITY.STALLS_MEM_ANY", 3) - EV("EXE_ACTIVITY.BOUND_ON_STORES", 3) - EV("EXE_ACTIVITY.EXE_BOUND_0_PORTS", 3)) / CLKS(self, EV, 3)
            EV("CYCLE_ACTIVITY.STALLS_MEM_ANY", 3)
            EV("EXE_ACTIVITY.BOUND_ON_STORES", 3)
            EV("ARITH.DIVIDER_ACTIVE", 3)
            EV("EXE_ACTIVITY.EXE_BOUND_0_PORTS", 3)
            Backend_Bound_Cycles(self, EV, 3)
            self.thresh = (self.val > 0.2) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Ports_Utilization zero division")
        return self.val

class G0_Ports_Utilized:
    name = "0_Ports_Utilized"
    domain = "CoreClocks"
    area = "BE/Core"
    desc = """
This metric represents Core fraction of cycles CPU executed
no uops on any execution port. Long-latency instructions
like divides may contribute to this metric.. Check assembly
view and Appendix C in Optimization Manual to find out
instructions with say 5 or more cycles latency..
http://www.intel.com/content/www/us/en/architecture-and-
technology/64-ia-32-architectures-optimization-manual.html"""
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Ports_Utilization']
    def compute(self, EV):
        try:
            self.val = Cycles_0_Ports_Utilized(self, EV, 4) / CORE_CLKS(self, EV, 4)
            self.thresh = (self.val > 0.2) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "G0_Ports_Utilized zero division")
        return self.val

class Serializing_Operation:
    name = "Serializing_Operation"
    domain = "Clocks"
    area = "BE/Core"
    desc = """
This metric represents fraction of cycles the CPU issue-
pipeline was stalled due to serializing operations.
Instructions like CPUID; WRMSR or LFENCE serialize the out-
of-order execution which may limit performance."""
    level = 5
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("PARTIAL_RAT_STALLS.SCOREBOARD", 5) / CLKS(self, EV, 5)
            self.thresh = (self.val > 0.1) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Serializing_Operation zero division")
        return self.val

class G1_Port_Utilized:
    name = "1_Port_Utilized"
    domain = "CoreClocks"
    area = "BE/Core"
    desc = """
This metric represents Core fraction of cycles where the CPU
executed total of 1 uop per cycle on all execution ports.
This can be due to heavy data-dependency among software
instructions; or over oversubscribing a particular hardware
resource. In some other cases with high 1_Port_Utilized and
L1_Bound; this metric can point to L1 data-cache latency
bottleneck that may not necessarily manifest with complete
execution starvation (due to the short L1 latency e.g.
walking a linked list) - looking at the assembly can be
helpful. Tip: consider 'Core Ports Saturation' analysis-type
as next step."""
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Ports_Utilization']
    def compute(self, EV):
        try:
            self.val = Cycles_1_Port_Utilized(self, EV, 4) / CORE_CLKS(self, EV, 4)
            self.thresh = (self.val > 0.2) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "G1_Port_Utilized zero division")
        return self.val

class G2_Ports_Utilized:
    name = "2_Ports_Utilized"
    domain = "CoreClocks"
    area = "BE/Core"
    desc = """
This metric represents Core fraction of cycles CPU executed
total of 2 uops per cycle on all execution ports. Tip:
consider 'Core Port Saturation' analysis-type as next step.
Loop Vectorization -most compilers feature auto-
Vectorization options today- reduces pressure on the
execution ports as multiple elements are calculated with
same uop."""
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Ports_Utilization']
    def compute(self, EV):
        try:
            self.val = Cycles_2_Ports_Utilized(self, EV, 4) / CORE_CLKS(self, EV, 4)
            self.thresh = (self.val > 0.2) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "G2_Ports_Utilized zero division")
        return self.val

class G3m_Ports_Utilized:
    name = "3m_Ports_Utilized"
    domain = "CoreClocks"
    area = "BE/Core"
    desc = """
This metric represents Core fraction of cycles CPU executed
total of 3 or more uops per cycle on all execution ports.
Tip: consider 'Core Port Saturation' analysis-type as next
step"""
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Ports_Utilization']
    def compute(self, EV):
        try:
            self.val = Cycles_3m_Ports_Utilized(self, EV, 4) / CORE_CLKS(self, EV, 4)
            self.thresh = (self.val > 0.7) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "G3m_Ports_Utilized zero division")
        return self.val

class ALU_Op_Utilization:
    name = "ALU_Op_Utilization"
    domain = "CoreClocks"
    area = "BE/Core"
    desc = """
This metric represents Core fraction of cycles CPU
dispatched uops on execution ports for ALU operations."""
    level = 5
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = (EV("UOPS_DISPATCHED_PORT.PORT_0", 5) + EV("UOPS_DISPATCHED_PORT.PORT_1", 5) + EV("UOPS_DISPATCHED_PORT.PORT_5", 5) + EV("UOPS_DISPATCHED_PORT.PORT_6", 5)) /(4 * CORE_CLKS(self, EV, 5))
            self.thresh = (self.val > 0.6)
        except ZeroDivisionError:
            handle_error(self, "ALU_Op_Utilization zero division")
        return self.val

class Load_Op_Utilization:
    name = "Load_Op_Utilization"
    domain = "CoreClocks"
    area = "BE/Core"
    desc = """
This metric represents Core fraction of cycles CPU
dispatched uops on execution port for Load operations"""
    level = 5
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = (EV("UOPS_DISPATCHED_PORT.PORT_2", 5) + EV("UOPS_DISPATCHED_PORT.PORT_3", 5) + EV("UOPS_DISPATCHED_PORT.PORT_7", 5) - EV("UOPS_DISPATCHED_PORT.PORT_4", 5)) /(2 * CORE_CLKS(self, EV, 5))
            self.thresh = (self.val > 0.6)
        except ZeroDivisionError:
            handle_error(self, "Load_Op_Utilization zero division")
        return self.val

class Store_Op_Utilization:
    name = "Store_Op_Utilization"
    domain = "CoreClocks"
    area = "BE/Core"
    desc = """
This metric represents Core fraction of cycles CPU
dispatched uops on execution port for Store operations"""
    level = 5
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("UOPS_DISPATCHED_PORT.PORT_4", 5) / CORE_CLKS(self, EV, 5)
            self.thresh = (self.val > 0.6)
        except ZeroDivisionError:
            handle_error(self, "Store_Op_Utilization zero division")
        return self.val

class Retiring:
    name = "Retiring"
    domain = "Slots"
    area = "RET"
    desc = """
This category represents fraction of slots utilized by
useful work i.e. issued uops that eventually get retired.
Ideally; all pipeline slots would be attributed to the
Retiring category.  Retiring of 100% would indicate the
maximum 4 uops retired per cycle has been achieved.
Maximizing Retiring typically increases the Instruction-Per-
Cycle metric. Note that a high Retiring value does not
necessary mean there is no room for more performance.  For
example; Microcode assists are categorized under Retiring.
They hurt performance and can often be avoided. . A high
Retiring value for non-vectorized code may be a good hint
for programmer to consider vectorizing his code.  Doing so
essentially lets more computations be done without
significantly increasing number of instructions thus
improving the performance."""
    level = 1
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['TopDownL1']
    def compute(self, EV):
        try:
            self.val = EV("UOPS_RETIRED.RETIRE_SLOTS", 1) / SLOTS(self, EV, 1)
            self.thresh = (self.val > 0.75) | self.Microcode_Sequencer.thresh
        except ZeroDivisionError:
            handle_error(self, "Retiring zero division")
        return self.val

class Base:
    name = "Base"
    domain = "Slots"
    area = "RET"
    desc = """
This metric represents fraction of slots where the CPU was
retiring regular uops (ones not originated from the
microcode-sequencer). This correlates with total number of
instructions used by the program. A uops-per-instruction
ratio of 1 should be expected. While this is the most
desirable of the top 4 categories; high values does not
necessarily mean there no room for performance
optimizations.. Focus on techniques that reduce instruction
count or result in more efficient instructions generation
such as vectorization."""
    level = 2
    htoff = False
    sample = ['INST_RETIRED.PREC_DIST']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['TopDownL2']
    def compute(self, EV):
        try:
            self.val = self.Retiring.compute(EV) - self.Microcode_Sequencer.compute(EV)
            self.thresh = (self.val > 0.6) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Base zero division")
        return self.val

class FP_Arith:
    name = "FP_Arith"
    domain = "Uops"
    area = "RET"
    desc = """
This metric represents overall arithmetic floating-point
(FP) uops fraction the CPU has executed (retired)"""
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Retiring']
    def compute(self, EV):
        try:
            self.val = self.X87_Use.compute(EV) + self.FP_Scalar.compute(EV) + self.FP_Vector.compute(EV)
            self.thresh = (self.val > 0.2) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "FP_Arith zero division")
        return self.val

class X87_Use:
    name = "X87_Use"
    domain = "Uops"
    area = "RET"
    desc = """
This metric serves as an approximation of legacy x87 usage.
It accounts for instructions beyond X87 FP arithmetic
operations; hence may be used as a thermometer to avoid X87
high usage and preferably upgrade to modern ISA. Tip:
consider compiler flags to generate newer AVX (or SSE)
instruction sets; which typically perform better and feature
vectors."""
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = EV("UOPS_EXECUTED.X87", 4) / EV("UOPS_EXECUTED.THREAD", 4)
            self.thresh = (self.val > 0.1) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "X87_Use zero division")
        return self.val

class FP_Scalar:
    name = "FP_Scalar"
    domain = "Uops"
    area = "RET"
    desc = """
This metric represents arithmetic floating-point (FP) scalar
uops fraction the CPU has executed (retired).. Investigate
what limits (compiler) generation of vector code."""
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['FLOPS']
    def compute(self, EV):
        try:
            self.val = (EV("FP_ARITH_INST_RETIRED.SCALAR_SINGLE", 4) + EV("FP_ARITH_INST_RETIRED.SCALAR_DOUBLE", 4)) / EV("UOPS_RETIRED.RETIRE_SLOTS", 4)
            self.thresh = (self.val > 0.1) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "FP_Scalar zero division")
        return self.val

class FP_Vector:
    name = "FP_Vector"
    domain = "Uops"
    area = "RET"
    desc = """
This metric represents arithmetic floating-point (FP) vector
uops fraction the CPU has executed (retired) aggregated
across all vector widths.. Check if vector width is expected"""
    level = 4
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['FLOPS']
    def compute(self, EV):
        try:
            self.val = (EV("FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE", 4) + EV("FP_ARITH_INST_RETIRED.128B_PACKED_SINGLE", 4) + EV("FP_ARITH_INST_RETIRED.256B_PACKED_DOUBLE", 4) + EV("FP_ARITH_INST_RETIRED.256B_PACKED_SINGLE", 4)) / EV("UOPS_RETIRED.RETIRE_SLOTS", 4)
            self.thresh = (self.val > 0.2) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "FP_Vector zero division")
        return self.val

class Other:
    name = "Other"
    domain = "Uops"
    area = "RET"
    desc = """
This metric represents non-floating-point (FP) uop fraction
the CPU has executed. If you application has no FP
operations and performs with decent IPC (Instructions Per
Cycle); this node will likely be biggest fraction."""
    level = 3
    htoff = False
    sample = []
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = 1 - self.FP_Arith.compute(EV)
            self.thresh = (self.val > 0.3) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Other zero division")
        return self.val

class Microcode_Sequencer:
    name = "Microcode_Sequencer"
    domain = "Slots"
    area = "RET"
    desc = """
This metric represents fraction of slots the CPU was
retiring uops fetched by the Microcode Sequencer (MS) unit.
The MS is used for CISC instructions not supported by the
default decoders (like repeat move strings; or CPUID); or by
microcode assists used to address some operation modes (like
in Floating Point assists). These cases can often be
avoided.."""
    level = 2
    htoff = False
    sample = ['IDQ.MS_UOPS']
    errcount = 0
    sibling = None
    server = False
    metricgroup = ['Microcode_Sequencer', 'Retiring', 'TopDownL2']
    def compute(self, EV):
        try:
            self.val = Retire_Uop_Fraction(self, EV, 2)* EV("IDQ.MS_UOPS", 2) / SLOTS(self, EV, 2)
            self.thresh = (self.val > 0.05)
        except ZeroDivisionError:
            handle_error(self, "Microcode_Sequencer zero division")
        return self.val

class Assists:
    name = "Assists"
    domain = "Slots_Estimated"
    area = "RET"
    desc = """
This metric estimates fraction of cycles the CPU retired
uops delivered by the Microcode_Sequencer as a result of
Assists. Assists are long sequences of uops that are
required in certain corner-cases for operations that cannot
be handled natively by the execution pipeline. For example;
when working with very small floating point values (so-
called Denormals); the FP units are not set up to perform
these operations natively. Instead; a sequence of
instructions to perform the computation on the Denormals is
injected into the pipeline. Since these microcode sequences
might be hundreds of uops long; Assists can be extremely
deleterious to performance and they can be avoided in many
cases."""
    level = 3
    htoff = False
    sample = ['OTHER_ASSISTS.ANY']
    errcount = 0
    sibling = None
    server = False
    metricgroup = []
    def compute(self, EV):
        try:
            self.val = Avg_Assist_Cost *(EV("FP_ASSIST.ANY", 3) + EV("OTHER_ASSISTS.ANY", 3)) / SLOTS(self, EV, 3)
            self.thresh = (self.val > 0.1) & self.parent.thresh
        except ZeroDivisionError:
            handle_error(self, "Assists zero division")
        return self.val

class Metric_IPC:
    name = "IPC"
    desc = """
Instructions Per Cycle (per logical thread)"""
    domain = "Metric"
    maxval = 5.0
    server = False
    errcount = 0
    area = "Info.Thread"
    metricgroup = ['TopDownL1']

    def compute(self, EV):
        try:
            self.val = IPC(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "IPC zero division")


class Metric_UPI:
    name = "UPI"
    desc = """
Uops Per Instruction"""
    domain = "Metric"
    maxval = 2.0
    server = False
    errcount = 0
    area = "Info.Thread"
    metricgroup = ['Pipeline', 'Retiring']

    def compute(self, EV):
        try:
            self.val = UPI(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "UPI zero division")


class Metric_IpTB:
    name = "IpTB"
    desc = """
Instruction per taken branch"""
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Thread"
    metricgroup = ['Branches', 'PGO']

    def compute(self, EV):
        try:
            self.val = IpTB(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "IpTB zero division")


class Metric_BpTB:
    name = "BpTB"
    desc = """
Branch instructions per taken branch. . Can be used to
approximate PGO-likelihood for non-loopy codes."""
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Thread"
    metricgroup = ['Branches', 'PGO']

    def compute(self, EV):
        try:
            self.val = BpTB(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "BpTB zero division")


class Metric_IFetch_Line_Utilization:
    name = "IFetch_Line_Utilization"
    desc = """
Rough Estimation of fraction of fetched lines bytes that
were likely (includes speculatively fetches) consumed by
program instructions"""
    domain = "Metric"
    maxval = 1.0
    server = False
    errcount = 0
    area = "Info.Thread"
    metricgroup = ['PGO']

    def compute(self, EV):
        try:
            self.val = IFetch_Line_Utilization(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "IFetch_Line_Utilization zero division")


class Metric_DSB_Coverage:
    name = "DSB_Coverage"
    desc = """
Fraction of Uops delivered by the DSB (aka Decoded ICache;
or Uop Cache). See section 'Decoded ICache' in Optimization
Manual. http://www.intel.com/content/www/us/en/architecture-
and-technology/64-ia-32-architectures-optimization-
manual.html"""
    domain = "Metric"
    maxval = 1.0
    server = False
    errcount = 0
    area = "Info.Thread"
    metricgroup = ['DSB', 'Frontend_Bandwidth']

    def compute(self, EV):
        try:
            self.val = DSB_Coverage(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "DSB_Coverage zero division")


class Metric_LSD_Coverage:
    name = "LSD_Coverage"
    desc = """
Fraction of Uops delivered by the LSD (Loop Stream Detector;
aka Loop Cache)"""
    domain = "Metric"
    maxval = 1.0
    server = False
    errcount = 0
    area = "Info.Thread"
    metricgroup = ['LSD']

    def compute(self, EV):
        try:
            self.val = LSD_Coverage(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "LSD_Coverage zero division")


class Metric_CPI:
    name = "CPI"
    desc = """
Cycles Per Instruction (threaded)"""
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Thread"
    metricgroup = ['Pipeline', 'Summary']

    def compute(self, EV):
        try:
            self.val = CPI(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "CPI zero division")


class Metric_CLKS:
    name = "CLKS"
    desc = """
Per-thread actual clocks when the logical processor is
active."""
    domain = "Count"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Thread"
    metricgroup = ['Summary']

    def compute(self, EV):
        try:
            self.val = CLKS(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "CLKS zero division")


class Metric_SLOTS:
    name = "SLOTS"
    desc = """
Total issue-pipeline slots ( per core )"""
    domain = "Count"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Thread"
    metricgroup = ['TopDownL1']

    def compute(self, EV):
        try:
            self.val = SLOTS(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "SLOTS zero division")


class Metric_IpL:
    name = "IpL"
    desc = """
Instructions per Load (lower number means loads are more
frequent)"""
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['Instruction_Type', 'L1_Bound']

    def compute(self, EV):
        try:
            self.val = IpL(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "IpL zero division")


class Metric_IpS:
    name = "IpS"
    desc = """
Instructions per Store"""
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['Instruction_Type', 'Store_Bound']

    def compute(self, EV):
        try:
            self.val = IpS(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "IpS zero division")


class Metric_IpB:
    name = "IpB"
    desc = """
Instructions per Branch"""
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['Branches', 'Instruction_Type', 'Port_5', 'Port_6']

    def compute(self, EV):
        try:
            self.val = IpB(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "IpB zero division")


class Metric_IpCall:
    name = "IpCall"
    desc = """
Instruction per (near) call"""
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['Branches']

    def compute(self, EV):
        try:
            self.val = IpCall(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "IpCall zero division")


class Metric_IpArith:
    name = "IpArith"
    desc = """
Instructions per FP Arithmetic instruction. Approximated
prior to BDW."""
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['FLOPS', 'FP_Arith', 'Instruction_Type']

    def compute(self, EV):
        try:
            self.val = IpArith(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "IpArith zero division")


class Metric_IpArith_Scalar_SP:
    name = "IpArith_Scalar_SP"
    desc = """
Instructions per FP Arithmetic Scalar Single-Precision
instruction."""
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['FLOPS', 'FP_Scalar', 'Instruction_Type']

    def compute(self, EV):
        try:
            self.val = IpArith_Scalar_SP(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "IpArith_Scalar_SP zero division")


class Metric_IpArith_Scalar_DP:
    name = "IpArith_Scalar_DP"
    desc = """
Instructions per FP Arithmetic Scalar Double-Precision
instruction."""
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['FLOPS', 'FP_Scalar', 'Instruction_Type']

    def compute(self, EV):
        try:
            self.val = IpArith_Scalar_DP(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "IpArith_Scalar_DP zero division")


class Metric_IpArith_AVX128:
    name = "IpArith_AVX128"
    desc = """
Instructions per FP Arithmetic AVX/SSE 128-bit instruction."""
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['FLOPS', 'FP_Vector', 'Instruction_Type']

    def compute(self, EV):
        try:
            self.val = IpArith_AVX128(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "IpArith_AVX128 zero division")


class Metric_IpArith_AVX256:
    name = "IpArith_AVX256"
    desc = """
Instructions per FP Arithmetic AVX* 256-bit instruction."""
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['FLOPS', 'FP_Vector', 'Instruction_Type']

    def compute(self, EV):
        try:
            self.val = IpArith_AVX256(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "IpArith_AVX256 zero division")


class Metric_Instructions:
    name = "Instructions"
    desc = """
Total number of retired Instructions"""
    domain = "Count"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Inst_Mix"
    metricgroup = ['Summary']

    def compute(self, EV):
        try:
            self.val = Instructions(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "Instructions zero division")


class Metric_CoreIPC:
    name = "CoreIPC"
    desc = """
Instructions Per Cycle (per physical core)"""
    domain = "CoreMetric"
    maxval = 5.0
    server = False
    errcount = 0
    area = "Info.Core"
    metricgroup = ['SMT']

    def compute(self, EV):
        try:
            self.val = CoreIPC(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "CoreIPC zero division")


class Metric_FLOPc:
    name = "FLOPc"
    desc = """
Floating Point Operations Per Cycle"""
    domain = "CoreMetric"
    maxval = 10.0
    server = False
    errcount = 0
    area = "Info.Core"
    metricgroup = ['FLOPS']

    def compute(self, EV):
        try:
            self.val = FLOPc(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "FLOPc zero division")


class Metric_FP_Arith_Utilization:
    name = "FP_Arith_Utilization"
    desc = """
Actual per-core usage of the Floating Point execution units
(regardless of the vector width)."""
    domain = "CoreMetric"
    maxval = 2.0
    server = False
    errcount = 0
    area = "Info.Core"
    metricgroup = ['FLOPS']

    def compute(self, EV):
        try:
            self.val = FP_Arith_Utilization(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "FP_Arith_Utilization zero division")


class Metric_ILP:
    name = "ILP"
    desc = """
Instruction-Level-Parallelism (average number of uops
executed when there is at least 1 uop executed)"""
    domain = "CoreMetric"
    maxval = 10.0
    server = False
    errcount = 0
    area = "Info.Core"
    metricgroup = ['Pipeline', 'Ports_Utilization']

    def compute(self, EV):
        try:
            self.val = ILP(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "ILP zero division")


class Metric_Branch_Misprediction_Cost:
    name = "Branch_Misprediction_Cost"
    desc = """
Branch Misprediction Cost: Fraction of TopDown slots wasted
per non-speculative branch misprediction (jeclear)"""
    domain = "CoreMetric"
    maxval = 300.0
    server = False
    errcount = 0
    area = "Info.Core"
    metricgroup = ['Branch_Mispredicts']

    def compute(self, EV):
        try:
            self.val = Branch_Misprediction_Cost(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "Branch_Misprediction_Cost zero division")


class Metric_IpMispredict:
    name = "IpMispredict"
    desc = """
Number of Instructions per non-speculative Branch
Misprediction (JEClear)"""
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Core"
    metricgroup = ['Branch_Mispredicts']

    def compute(self, EV):
        try:
            self.val = IpMispredict(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "IpMispredict zero division")


class Metric_CORE_CLKS:
    name = "CORE_CLKS"
    desc = """
Core actual clocks when any thread is active on the physical
core"""
    domain = "Count"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Core"
    metricgroup = ['SMT']

    def compute(self, EV):
        try:
            self.val = CORE_CLKS(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "CORE_CLKS zero division")


class Metric_Load_Miss_Real_Latency:
    name = "Load_Miss_Real_Latency"
    desc = """
Actual Average Latency for L1 data-cache miss demand loads
(in core cycles)"""
    domain = "Metric"
    maxval = 1000.0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Memory_Bound', 'Memory_Lat']

    def compute(self, EV):
        try:
            self.val = Load_Miss_Real_Latency(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "Load_Miss_Real_Latency zero division")


class Metric_MLP:
    name = "MLP"
    desc = """
Memory-Level-Parallelism (average number of L1 miss demand
load when there is at least one such miss. Per-thread)"""
    domain = "Metric"
    maxval = 10.0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Memory_Bound', 'Memory_BW']

    def compute(self, EV):
        try:
            self.val = MLP(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "MLP zero division")


class Metric_Page_Walks_Utilization:
    name = "Page_Walks_Utilization"
    desc = """
Utilization of the core's Page Walker(s) serving STLB misses
triggered by instruction/Load/Store accesses"""
    domain = "CoreMetric"
    maxval = 1
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['TLB']

    def compute(self, EV):
        try:
            self.val = Page_Walks_Utilization(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "Page_Walks_Utilization zero division")


class Metric_L1D_Cache_Fill_BW:
    name = "L1D_Cache_Fill_BW"
    desc = """
Average data fill bandwidth to the L1 data cache [GB / sec]"""
    domain = "CoreMetric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Memory_BW']

    def compute(self, EV):
        try:
            self.val = L1D_Cache_Fill_BW(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "L1D_Cache_Fill_BW zero division")


class Metric_L2_Cache_Fill_BW:
    name = "L2_Cache_Fill_BW"
    desc = """
Average data fill bandwidth to the L2 cache [GB / sec]"""
    domain = "CoreMetric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Memory_BW']

    def compute(self, EV):
        try:
            self.val = L2_Cache_Fill_BW(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "L2_Cache_Fill_BW zero division")


class Metric_L3_Cache_Fill_BW:
    name = "L3_Cache_Fill_BW"
    desc = """
Average per-core data fill bandwidth to the L3 cache [GB /
sec]"""
    domain = "CoreMetric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Memory_BW']

    def compute(self, EV):
        try:
            self.val = L3_Cache_Fill_BW(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "L3_Cache_Fill_BW zero division")


class Metric_L3_Cache_Access_BW:
    name = "L3_Cache_Access_BW"
    desc = """
Average per-core data fill bandwidth to the L3 cache [GB /
sec]"""
    domain = "CoreMetric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Memory_BW']

    def compute(self, EV):
        try:
            self.val = L3_Cache_Access_BW(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "L3_Cache_Access_BW zero division")


class Metric_L1MPKI:
    name = "L1MPKI"
    desc = """
L1 cache true misses per kilo instruction for retired demand
loads"""
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Cache_Misses']

    def compute(self, EV):
        try:
            self.val = L1MPKI(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "L1MPKI zero division")


class Metric_L2MPKI:
    name = "L2MPKI"
    desc = """
L2 cache true misses per kilo instruction for retired demand
loads"""
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Cache_Misses']

    def compute(self, EV):
        try:
            self.val = L2MPKI(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "L2MPKI zero division")


class Metric_L2MPKI_All:
    name = "L2MPKI_All"
    desc = """
L2 cache misses per kilo instruction for all request types
(including speculative)"""
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Cache_Misses']

    def compute(self, EV):
        try:
            self.val = L2MPKI_All(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "L2MPKI_All zero division")


class Metric_L2MPKI_Load:
    name = "L2MPKI_Load"
    desc = """
L2 cache misses per kilo instruction for all demand loads
(including speculative)"""
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Cache_Misses']

    def compute(self, EV):
        try:
            self.val = L2MPKI_Load(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "L2MPKI_Load zero division")


class Metric_L2HPKI_All:
    name = "L2HPKI_All"
    desc = """
L2 cache hits per kilo instruction for all request types
(including speculative)"""
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Cache_Misses']

    def compute(self, EV):
        try:
            self.val = L2HPKI_All(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "L2HPKI_All zero division")


class Metric_L2HPKI_Load:
    name = "L2HPKI_Load"
    desc = """
L2 cache hits per kilo instruction for all demand loads
(including speculative)"""
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Cache_Misses']

    def compute(self, EV):
        try:
            self.val = L2HPKI_Load(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "L2HPKI_Load zero division")


class Metric_L3MPKI:
    name = "L3MPKI"
    desc = """
L3 cache true misses per kilo instruction for retired demand
loads"""
    domain = "Metric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.Memory"
    metricgroup = ['Cache_Misses']

    def compute(self, EV):
        try:
            self.val = L3MPKI(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "L3MPKI zero division")


class Metric_CPU_Utilization:
    name = "CPU_Utilization"
    desc = """
Average CPU Utilization"""
    domain = "Metric"
    maxval = 200.0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Summary']

    def compute(self, EV):
        try:
            self.val = CPU_Utilization(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "CPU_Utilization zero division")


class Metric_Average_Frequency:
    name = "Average_Frequency"
    desc = """
Measured Average Frequency for unhalted processors [GHz]"""
    domain = "SystemMetric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Summary', 'Power']

    def compute(self, EV):
        try:
            self.val = Average_Frequency(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "Average_Frequency zero division")


class Metric_GFLOPs:
    name = "GFLOPs"
    desc = """
Giga Floating Point Operations Per Second"""
    domain = "Metric"
    maxval = 200.0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['FLOPS', 'Summary']

    def compute(self, EV):
        try:
            self.val = GFLOPs(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "GFLOPs zero division")


class Metric_Turbo_Utilization:
    name = "Turbo_Utilization"
    desc = """
Average Frequency Utilization relative nominal frequency"""
    domain = "CoreMetric"
    maxval = 10.0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Power']

    def compute(self, EV):
        try:
            self.val = Turbo_Utilization(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "Turbo_Utilization zero division")


class Metric_SMT_2T_Utilization:
    name = "SMT_2T_Utilization"
    desc = """
Fraction of cycles where both hardware threads were active"""
    domain = "CoreMetric"
    maxval = 1.0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['SMT', 'Summary']

    def compute(self, EV):
        try:
            self.val = SMT_2T_Utilization(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "SMT_2T_Utilization zero division")


class Metric_Kernel_Utilization:
    name = "Kernel_Utilization"
    desc = """
Fraction of cycles spent in Kernel mode"""
    domain = "Metric"
    maxval = 1.0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = []

    def compute(self, EV):
        try:
            self.val = Kernel_Utilization(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "Kernel_Utilization zero division")


class Metric_DRAM_BW_Use:
    name = "DRAM_BW_Use"
    desc = """
Average external Memory Bandwidth Use for reads and writes
[GB / sec]"""
    domain = "SystemMetric"
    maxval = 200.0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Memory_BW']

    def compute(self, EV):
        try:
            self.val = DRAM_BW_Use(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "DRAM_BW_Use zero division")


class Metric_MEM_Request_Latency:
    name = "MEM_Request_Latency"
    desc = """
Average latency of all requests to external memory (in
Uncore cycles)"""
    domain = "Metric"
    maxval = 1000.0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = []

    def compute(self, EV):
        try:
            self.val = MEM_Request_Latency(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "MEM_Request_Latency zero division")


class Metric_MEM_Parallel_Requests:
    name = "MEM_Parallel_Requests"
    desc = """
Average number of parallel requests to external memory.
Accounts for all requests"""
    domain = "Metric"
    maxval = 100.0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = []

    def compute(self, EV):
        try:
            self.val = MEM_Parallel_Requests(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "MEM_Parallel_Requests zero division")


class Metric_DRAM_Read_Latency:
    name = "DRAM_Read_Latency"
    desc = """
Average latency of data read request to external memory (in
nanoseconds). Accounts for demand loads and L1/L2 prefetches"""
    domain = "SystemMetric"
    maxval = 1000.0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Memory_Lat']

    def compute(self, EV):
        try:
            self.val = DRAM_Read_Latency(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "DRAM_Read_Latency zero division")


class Metric_DRAM_Parallel_Reads:
    name = "DRAM_Parallel_Reads"
    desc = """
Average number of parallel data read requests to external
memory. Accounts for demand loads and L1/L2 prefetches"""
    domain = "SystemMetric"
    maxval = 100.0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Memory_BW']

    def compute(self, EV):
        try:
            self.val = DRAM_Parallel_Reads(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "DRAM_Parallel_Reads zero division")


class Metric_MEM_DRAM_Read_Latency:
    name = "MEM_DRAM_Read_Latency"
    desc = """
Average latency of data read request to external DRAM memory
[in nanoseconds]. Accounts for demand loads and L1/L2 data-
read prefetches"""
    domain = "SystemMetric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Memory_Lat']

    def compute(self, EV):
        try:
            self.val = MEM_DRAM_Read_Latency(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "MEM_DRAM_Read_Latency zero division")


class Metric_Time:
    name = "Time"
    desc = """
Run duration time in seconds"""
    domain = "SystemMetric"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = ['Summary']

    def compute(self, EV):
        try:
            self.val = Time(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "Time zero division")


class Metric_Socket_CLKS:
    name = "Socket_CLKS"
    desc = """
Socket actual clocks when any core is active on that socket"""
    domain = "Count"
    maxval = 0
    server = False
    errcount = 0
    area = "Info.System"
    metricgroup = []

    def compute(self, EV):
        try:
            self.val = Socket_CLKS(self, EV, 0)
        except ZeroDivisionError:
            handle_error_metric(self, "Socket_CLKS zero division")


# Schedule



class Setup:
    def __init__(self, r):
        o = dict()
        n = Frontend_Bound() ; r.run(n) ; o["Frontend_Bound"] = n
        n = Frontend_Latency() ; r.run(n) ; o["Frontend_Latency"] = n
        n = ICache_Misses() ; r.run(n) ; o["ICache_Misses"] = n
        n = ITLB_Misses() ; r.run(n) ; o["ITLB_Misses"] = n
        n = Branch_Resteers() ; r.run(n) ; o["Branch_Resteers"] = n
        n = Mispredicts_Resteers() ; r.run(n) ; o["Mispredicts_Resteers"] = n
        n = Clears_Resteers() ; r.run(n) ; o["Clears_Resteers"] = n
        n = Unknown_Branches() ; r.run(n) ; o["Unknown_Branches"] = n
        n = DSB_Switches() ; r.run(n) ; o["DSB_Switches"] = n
        n = LCP() ; r.run(n) ; o["LCP"] = n
        n = MS_Switches() ; r.run(n) ; o["MS_Switches"] = n
        n = Frontend_Bandwidth() ; r.run(n) ; o["Frontend_Bandwidth"] = n
        n = MITE() ; r.run(n) ; o["MITE"] = n
        n = DSB() ; r.run(n) ; o["DSB"] = n
        n = LSD() ; r.run(n) ; o["LSD"] = n
        n = Bad_Speculation() ; r.run(n) ; o["Bad_Speculation"] = n
        n = Branch_Mispredicts() ; r.run(n) ; o["Branch_Mispredicts"] = n
        n = Machine_Clears() ; r.run(n) ; o["Machine_Clears"] = n
        n = Backend_Bound() ; r.run(n) ; o["Backend_Bound"] = n
        n = Memory_Bound() ; r.run(n) ; o["Memory_Bound"] = n
        n = L1_Bound() ; r.run(n) ; o["L1_Bound"] = n
        n = DTLB_Load() ; r.run(n) ; o["DTLB_Load"] = n
        n = Store_Fwd_Blk() ; r.run(n) ; o["Store_Fwd_Blk"] = n
        n = Lock_Latency() ; r.run(n) ; o["Lock_Latency"] = n
        n = Split_Loads() ; r.run(n) ; o["Split_Loads"] = n
        n = G4K_Aliasing() ; r.run(n) ; o["G4K_Aliasing"] = n
        n = FB_Full() ; r.run(n) ; o["FB_Full"] = n
        n = L2_Bound() ; r.run(n) ; o["L2_Bound"] = n
        n = L3_Bound() ; r.run(n) ; o["L3_Bound"] = n
        n = Contested_Accesses() ; r.run(n) ; o["Contested_Accesses"] = n
        n = Data_Sharing() ; r.run(n) ; o["Data_Sharing"] = n
        n = L3_Hit_Latency() ; r.run(n) ; o["L3_Hit_Latency"] = n
        n = SQ_Full() ; r.run(n) ; o["SQ_Full"] = n
        n = DRAM_Bound() ; r.run(n) ; o["DRAM_Bound"] = n
        n = MEM_Bandwidth() ; r.run(n) ; o["MEM_Bandwidth"] = n
        n = MEM_Latency() ; r.run(n) ; o["MEM_Latency"] = n
        n = Store_Bound() ; r.run(n) ; o["Store_Bound"] = n
        n = Store_Latency() ; r.run(n) ; o["Store_Latency"] = n
        n = Split_Stores() ; r.run(n) ; o["Split_Stores"] = n
        n = DTLB_Store() ; r.run(n) ; o["DTLB_Store"] = n
        n = Core_Bound() ; r.run(n) ; o["Core_Bound"] = n
        n = Divider() ; r.run(n) ; o["Divider"] = n
        n = Ports_Utilization() ; r.run(n) ; o["Ports_Utilization"] = n
        n = G0_Ports_Utilized() ; r.run(n) ; o["G0_Ports_Utilized"] = n
        n = Serializing_Operation() ; r.run(n) ; o["Serializing_Operation"] = n
        n = G1_Port_Utilized() ; r.run(n) ; o["G1_Port_Utilized"] = n
        n = G2_Ports_Utilized() ; r.run(n) ; o["G2_Ports_Utilized"] = n
        n = G3m_Ports_Utilized() ; r.run(n) ; o["G3m_Ports_Utilized"] = n
        n = ALU_Op_Utilization() ; r.run(n) ; o["ALU_Op_Utilization"] = n
        n = Load_Op_Utilization() ; r.run(n) ; o["Load_Op_Utilization"] = n
        n = Store_Op_Utilization() ; r.run(n) ; o["Store_Op_Utilization"] = n
        n = Retiring() ; r.run(n) ; o["Retiring"] = n
        n = Base() ; r.run(n) ; o["Base"] = n
        n = FP_Arith() ; r.run(n) ; o["FP_Arith"] = n
        n = X87_Use() ; r.run(n) ; o["X87_Use"] = n
        n = FP_Scalar() ; r.run(n) ; o["FP_Scalar"] = n
        n = FP_Vector() ; r.run(n) ; o["FP_Vector"] = n
        n = Other() ; r.run(n) ; o["Other"] = n
        n = Microcode_Sequencer() ; r.run(n) ; o["Microcode_Sequencer"] = n
        n = Assists() ; r.run(n) ; o["Assists"] = n

        # parents

        o["Frontend_Latency"].parent = o["Frontend_Bound"]
        o["ICache_Misses"].parent = o["Frontend_Latency"]
        o["ITLB_Misses"].parent = o["Frontend_Latency"]
        o["Branch_Resteers"].parent = o["Frontend_Latency"]
        o["Mispredicts_Resteers"].parent = o["Branch_Resteers"]
        o["Clears_Resteers"].parent = o["Branch_Resteers"]
        o["Unknown_Branches"].parent = o["Branch_Resteers"]
        o["DSB_Switches"].parent = o["Frontend_Latency"]
        o["LCP"].parent = o["Frontend_Latency"]
        o["MS_Switches"].parent = o["Frontend_Latency"]
        o["Frontend_Bandwidth"].parent = o["Frontend_Bound"]
        o["MITE"].parent = o["Frontend_Bandwidth"]
        o["DSB"].parent = o["Frontend_Bandwidth"]
        o["LSD"].parent = o["Frontend_Bandwidth"]
        o["Branch_Mispredicts"].parent = o["Bad_Speculation"]
        o["Machine_Clears"].parent = o["Bad_Speculation"]
        o["Memory_Bound"].parent = o["Backend_Bound"]
        o["L1_Bound"].parent = o["Memory_Bound"]
        o["DTLB_Load"].parent = o["L1_Bound"]
        o["Store_Fwd_Blk"].parent = o["L1_Bound"]
        o["Lock_Latency"].parent = o["L1_Bound"]
        o["Split_Loads"].parent = o["L1_Bound"]
        o["G4K_Aliasing"].parent = o["L1_Bound"]
        o["FB_Full"].parent = o["L1_Bound"]
        o["L2_Bound"].parent = o["Memory_Bound"]
        o["L3_Bound"].parent = o["Memory_Bound"]
        o["Contested_Accesses"].parent = o["L3_Bound"]
        o["Data_Sharing"].parent = o["L3_Bound"]
        o["L3_Hit_Latency"].parent = o["L3_Bound"]
        o["SQ_Full"].parent = o["L3_Bound"]
        o["DRAM_Bound"].parent = o["Memory_Bound"]
        o["MEM_Bandwidth"].parent = o["DRAM_Bound"]
        o["MEM_Latency"].parent = o["DRAM_Bound"]
        o["Store_Bound"].parent = o["Memory_Bound"]
        o["Store_Latency"].parent = o["Store_Bound"]
        o["Split_Stores"].parent = o["Store_Bound"]
        o["DTLB_Store"].parent = o["Store_Bound"]
        o["Core_Bound"].parent = o["Backend_Bound"]
        o["Divider"].parent = o["Core_Bound"]
        o["Ports_Utilization"].parent = o["Core_Bound"]
        o["G0_Ports_Utilized"].parent = o["Ports_Utilization"]
        o["Serializing_Operation"].parent = o["G0_Ports_Utilized"]
        o["G1_Port_Utilized"].parent = o["Ports_Utilization"]
        o["G2_Ports_Utilized"].parent = o["Ports_Utilization"]
        o["G3m_Ports_Utilized"].parent = o["Ports_Utilization"]
        o["ALU_Op_Utilization"].parent = o["G3m_Ports_Utilized"]
        o["Load_Op_Utilization"].parent = o["G3m_Ports_Utilized"]
        o["Store_Op_Utilization"].parent = o["G3m_Ports_Utilized"]
        o["Base"].parent = o["Retiring"]
        o["FP_Arith"].parent = o["Base"]
        o["X87_Use"].parent = o["FP_Arith"]
        o["FP_Scalar"].parent = o["FP_Arith"]
        o["FP_Vector"].parent = o["FP_Arith"]
        o["Other"].parent = o["Base"]
        o["Microcode_Sequencer"].parent = o["Retiring"]
        o["Assists"].parent = o["Microcode_Sequencer"]

        # user visible metrics

        n = Metric_IPC() ; r.metric(n) ; o["IPC"] = n
        n = Metric_UPI() ; r.metric(n) ; o["UPI"] = n
        n = Metric_IpTB() ; r.metric(n) ; o["IpTB"] = n
        n = Metric_BpTB() ; r.metric(n) ; o["BpTB"] = n
        n = Metric_IFetch_Line_Utilization() ; r.metric(n) ; o["IFetch_Line_Utilization"] = n
        n = Metric_DSB_Coverage() ; r.metric(n) ; o["DSB_Coverage"] = n
        n = Metric_LSD_Coverage() ; r.metric(n) ; o["LSD_Coverage"] = n
        n = Metric_CPI() ; r.metric(n) ; o["CPI"] = n
        n = Metric_CLKS() ; r.metric(n) ; o["CLKS"] = n
        n = Metric_SLOTS() ; r.metric(n) ; o["SLOTS"] = n
        n = Metric_IpL() ; r.metric(n) ; o["IpL"] = n
        n = Metric_IpS() ; r.metric(n) ; o["IpS"] = n
        n = Metric_IpB() ; r.metric(n) ; o["IpB"] = n
        n = Metric_IpCall() ; r.metric(n) ; o["IpCall"] = n
        n = Metric_IpArith() ; r.metric(n) ; o["IpArith"] = n
        n = Metric_IpArith_Scalar_SP() ; r.metric(n) ; o["IpArith_Scalar_SP"] = n
        n = Metric_IpArith_Scalar_DP() ; r.metric(n) ; o["IpArith_Scalar_DP"] = n
        n = Metric_IpArith_AVX128() ; r.metric(n) ; o["IpArith_AVX128"] = n
        n = Metric_IpArith_AVX256() ; r.metric(n) ; o["IpArith_AVX256"] = n
        n = Metric_Instructions() ; r.metric(n) ; o["Instructions"] = n
        n = Metric_CoreIPC() ; r.metric(n) ; o["CoreIPC"] = n
        n = Metric_FLOPc() ; r.metric(n) ; o["FLOPc"] = n
        n = Metric_FP_Arith_Utilization() ; r.metric(n) ; o["FP_Arith_Utilization"] = n
        n = Metric_ILP() ; r.metric(n) ; o["ILP"] = n
        n = Metric_Branch_Misprediction_Cost() ; r.metric(n) ; o["Branch_Misprediction_Cost"] = n
        n = Metric_IpMispredict() ; r.metric(n) ; o["IpMispredict"] = n
        n = Metric_CORE_CLKS() ; r.metric(n) ; o["CORE_CLKS"] = n
        n = Metric_Load_Miss_Real_Latency() ; r.metric(n) ; o["Load_Miss_Real_Latency"] = n
        n = Metric_MLP() ; r.metric(n) ; o["MLP"] = n
        n = Metric_Page_Walks_Utilization() ; r.metric(n) ; o["Page_Walks_Utilization"] = n
        n = Metric_L1D_Cache_Fill_BW() ; r.metric(n) ; o["L1D_Cache_Fill_BW"] = n
        n = Metric_L2_Cache_Fill_BW() ; r.metric(n) ; o["L2_Cache_Fill_BW"] = n
        n = Metric_L3_Cache_Fill_BW() ; r.metric(n) ; o["L3_Cache_Fill_BW"] = n
        n = Metric_L3_Cache_Access_BW() ; r.metric(n) ; o["L3_Cache_Access_BW"] = n
        n = Metric_L1MPKI() ; r.metric(n) ; o["L1MPKI"] = n
        n = Metric_L2MPKI() ; r.metric(n) ; o["L2MPKI"] = n
        n = Metric_L2MPKI_All() ; r.metric(n) ; o["L2MPKI_All"] = n
        n = Metric_L2MPKI_Load() ; r.metric(n) ; o["L2MPKI_Load"] = n
        n = Metric_L2HPKI_All() ; r.metric(n) ; o["L2HPKI_All"] = n
        n = Metric_L2HPKI_Load() ; r.metric(n) ; o["L2HPKI_Load"] = n
        n = Metric_L3MPKI() ; r.metric(n) ; o["L3MPKI"] = n
        n = Metric_CPU_Utilization() ; r.metric(n) ; o["CPU_Utilization"] = n
        n = Metric_Average_Frequency() ; r.metric(n) ; o["Average_Frequency"] = n
        n = Metric_GFLOPs() ; r.metric(n) ; o["GFLOPs"] = n
        n = Metric_Turbo_Utilization() ; r.metric(n) ; o["Turbo_Utilization"] = n
        n = Metric_SMT_2T_Utilization() ; r.metric(n) ; o["SMT_2T_Utilization"] = n
        n = Metric_Kernel_Utilization() ; r.metric(n) ; o["Kernel_Utilization"] = n
        n = Metric_DRAM_BW_Use() ; r.metric(n) ; o["DRAM_BW_Use"] = n
        n = Metric_MEM_Request_Latency() ; r.metric(n) ; o["MEM_Request_Latency"] = n
        n = Metric_MEM_Parallel_Requests() ; r.metric(n) ; o["MEM_Parallel_Requests"] = n
        n = Metric_DRAM_Read_Latency() ; r.metric(n) ; o["DRAM_Read_Latency"] = n
        n = Metric_DRAM_Parallel_Reads() ; r.metric(n) ; o["DRAM_Parallel_Reads"] = n
        n = Metric_MEM_DRAM_Read_Latency() ; r.metric(n) ; o["MEM_DRAM_Read_Latency"] = n
        n = Metric_Time() ; r.metric(n) ; o["Time"] = n
        n = Metric_Socket_CLKS() ; r.metric(n) ; o["Socket_CLKS"] = n

        # references between groups

        o["Unknown_Branches"].Branch_Resteers = o["Branch_Resteers"]
        o["Frontend_Bandwidth"].Frontend_Bound = o["Frontend_Bound"]
        o["Frontend_Bandwidth"].Frontend_Latency = o["Frontend_Latency"]
        o["Branch_Mispredicts"].Bad_Speculation = o["Bad_Speculation"]
        o["Machine_Clears"].Bad_Speculation = o["Bad_Speculation"]
        o["Machine_Clears"].Branch_Mispredicts = o["Branch_Mispredicts"]
        o["Backend_Bound"].Retiring = o["Retiring"]
        o["Backend_Bound"].Bad_Speculation = o["Bad_Speculation"]
        o["Backend_Bound"].Frontend_Bound = o["Frontend_Bound"]
        o["Memory_Bound"].Retiring = o["Retiring"]
        o["Memory_Bound"].Bad_Speculation = o["Bad_Speculation"]
        o["Memory_Bound"].Frontend_Bound = o["Frontend_Bound"]
        o["Memory_Bound"].Backend_Bound = o["Backend_Bound"]
        o["L2_Bound"].FB_Full = o["FB_Full"]
        o["DRAM_Bound"].FB_Full = o["FB_Full"]
        o["DRAM_Bound"].L2_Bound = o["L2_Bound"]
        o["MEM_Latency"].MEM_Bandwidth = o["MEM_Bandwidth"]
        o["Core_Bound"].Retiring = o["Retiring"]
        o["Core_Bound"].Frontend_Bound = o["Frontend_Bound"]
        o["Core_Bound"].Memory_Bound = o["Memory_Bound"]
        o["Core_Bound"].Backend_Bound = o["Backend_Bound"]
        o["Core_Bound"].Bad_Speculation = o["Bad_Speculation"]
        o["Retiring"].Microcode_Sequencer = o["Microcode_Sequencer"]
        o["Base"].Retiring = o["Retiring"]
        o["Base"].Microcode_Sequencer = o["Microcode_Sequencer"]
        o["FP_Arith"].FP_Scalar = o["FP_Scalar"]
        o["FP_Arith"].X87_Use = o["X87_Use"]
        o["FP_Arith"].FP_Vector = o["FP_Vector"]
        o["Other"].FP_Arith = o["FP_Arith"]
        o["Other"].X87_Use = o["X87_Use"]
        o["Other"].FP_Scalar = o["FP_Scalar"]
        o["Other"].FP_Vector = o["FP_Vector"]
        o["FP_Arith_Utilization"].FP_Vector = o["FP_Vector"]
        o["FP_Arith_Utilization"].FP_Scalar = o["FP_Scalar"]
        o["Branch_Misprediction_Cost"].Bad_Speculation = o["Bad_Speculation"]
        o["Branch_Misprediction_Cost"].Mispredicts_Resteers = o["Mispredicts_Resteers"]
        o["Branch_Misprediction_Cost"].Branch_Mispredicts = o["Branch_Mispredicts"]
        o["Branch_Misprediction_Cost"].Frontend_Latency = o["Frontend_Latency"]

        # siblings cross-tree

        o["Mispredicts_Resteers"].sibling = (o["Clears_Resteers"], o["Branch_Mispredicts"],)
        o["Clears_Resteers"].sibling = (o["Mispredicts_Resteers"], o["Branch_Mispredicts"],)
        o["MS_Switches"].sibling = (o["Serializing_Operation"], o["Microcode_Sequencer"],)
        o["Branch_Mispredicts"].sibling = (o["Mispredicts_Resteers"], o["Clears_Resteers"],)
        o["L1_Bound"].sibling = (o["G1_Port_Utilized"],)
        o["Lock_Latency"].sibling = (o["Store_Latency"],)
        o["FB_Full"].sibling = (o["SQ_Full"], o["MEM_Bandwidth"], o["Store_Latency"],)
        o["L3_Hit_Latency"].sibling = (o["MEM_Latency"],)
        o["L3_Hit_Latency"].overlap = True
        o["SQ_Full"].sibling = (o["FB_Full"], o["MEM_Bandwidth"],)
        o["MEM_Bandwidth"].sibling = (o["FB_Full"], o["SQ_Full"],)
        o["MEM_Latency"].sibling = (o["L3_Hit_Latency"],)
        o["Store_Latency"].sibling = (o["Lock_Latency"], o["FB_Full"],)
        o["Store_Latency"].overlap = True
        o["Serializing_Operation"].sibling = (o["MS_Switches"],)
        o["G1_Port_Utilized"].sibling = (o["L1_Bound"],)
        o["Microcode_Sequencer"].sibling = (o["MS_Switches"],)
