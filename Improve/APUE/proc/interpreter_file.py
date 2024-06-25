#!/usr/bin/python3

# 解释器文件  #!

import sys

# 获取命令行参数列表
args = sys.argv
# args[0] 是脚本名称本身，后续元素是传递给脚本的参数
script_name = args[0]
parameters = args[1:]

# 处理参数
for param in parameters:
    print(f"Received parameter: {param}")
