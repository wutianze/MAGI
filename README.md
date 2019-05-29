# MAGI
# work to do:
  - 更多的测试
# working on:  
  - 模型优化，探索能使准确率上升的办法
  - xapian修改获取实时latency：在harness/client.cpp中Client::finiReq的sjrn代表了实时的延迟
# work finished:
  - 基础环境搭建
  - 应用数据采集/所需数据种类工具调研
  - 应用数据采集
  - 规则模型实现
  - 数据驱动模型实现
  
# project init
  - 各种检测工具都需要sudo
  - pqos工具安装
    - kernel版本需要注意，要4.10以上才能支持os iface上的一些特性，而且需要在config里修改RDT对应项。
    - resourceControll中常量值须根据实际机器修改
  - perf工具安装
  - pmu工具安装
    - git clone下来之后会提示echo...必须su执行
    - 须根据实际机器更改代码中判断有效行的条件

# MAGI运行参数设置
  - 命令行参数指定
  - estimater里指定数据保存文件夹
  - policy里指定每隔多少轮尝试训练
  - main里设置每隔多少轮记录一次运行时数据，可用的核的编号
  - resourceControl里设置当前cache llc数量
  
# test init
  - configs.sh中变量设置
  - xapian
    先进入xapian解压出的文件夹，使用./configure看是否需要安装libuuid-devel等
  - shore
    同样建议先进入shore来安装，需要安装的可能有automake,autoconfig,glib2-devel等库，且centos会出现glibconfig.h找不到的情况，需要将/usr/lib64/glib-2/include/glibconfig.h拷贝到/usr/include/glib-2/中

# xapian usage
控制运行时间：有两个变量TBENCH_MAXREQS和-r，client会一直运行发送请求直到server发送finish信号，而server就是到TBENCH_MAXREQS+TBENCH_WARMUP会发信号。server会在所有client都结束后自动结束，而-r的设置相当于另外给了一个server处理请求的上限，到达这个值即使还有client那server也还是会结束。
本次实验直接将-r设置成无穷大即可。

# memcached usage
使用ycsb来压测，注意它和xapian一样，不提供压力，ipc就是0.
ycsb使用时要注意，load动作的recordcount不知道为什么不能在命令行指定，必须要在配置的workload\*文件里指定，而run动作的operationcount可以在命令行里指定。

# problems found now (* for not solved)
  - \* accuracy一直提不上去，目前对于xapian来说是0.3-0.4左右，对mcf是0.8左右。
