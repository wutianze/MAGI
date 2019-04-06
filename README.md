# MAGI
# work to do:
  - 测试
# working on:  
  - 系统环境配置
# work finished:
  - 基础环境搭建
  - 应用数据采集/所需数据种类工具调研
  - 应用数据采集
  - 规则模型实现
  - 数据驱动模型实现
  
# project init
  - 各种检测工具都需要sudo
  - pqos工具安装
    - resourceControll中常量值须根据实际机器修改
  - perf工具安装
  - pmu工具安装
    - git clone下来之后会提示echo...必须su执行
    - 须根据实际机器更改代码中判断有效行的条件

# test init
  - configs.sh中变量设置
  - xapian
    先进入xapian解压出的文件夹，使用./configure看是否需要安装libuuid-devel等
  - shore
    同样建议先进入shore来安装，需要安装的可能有automake,glib2-devel等库，且centos会出现glibconfig.h找不到的情况，需要将/usr/lib64/glib-2/include/glibconfig.h拷贝到/usr/include/glib-2/中
