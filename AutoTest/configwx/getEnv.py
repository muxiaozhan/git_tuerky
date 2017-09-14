# -*- coding: utf-8 -*-
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath) #防止命令行找不到模块
formdir = os.path.dirname(os.getcwd())  # 获取上一级目录

def getVariable(key):
    envPath = os.path.join(curPath, "envariable.txt")
    fd = open(envPath, 'r')

    for i in fd.readlines():
        if i.split(':')[0] == key:  # 判断键重复
           value = i.split(':')[1]
           break
    else:
        value = None
    print(value)
    return value

if __name__ =='__main__':
    getVariable('__Author__')

