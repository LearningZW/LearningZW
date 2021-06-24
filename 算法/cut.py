# -*- coding:utf-8 -*-

__author__ = "苦叶子"


"""

    关注微信公众号：开源优测

    获取更多关于开源技术在测试工作中的应用实践

"""

from jpype import *

if __name__ == "__main__":


    # 启动java虚拟机
    startJVM(getDefaultJVMPath(), "-ea")

    # 调用println函数
    java.lang.System.out.println("hello python java")

    # 关闭虚拟机
    shutdownJVM()