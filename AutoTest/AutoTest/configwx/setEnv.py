# -*- coding: utf-8 -*-
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath) #防止命令行找不到模块
formdir = os.path.dirname(os.getcwd())  # 获取上一级目录


def setVariable(key,value):
    envPath = os.path.join(curPath,"envariable.txt")
    fd= open(envPath,'r')
    lines = []
    for line in fd:
        lines.append(line)
    fd.close()
    fd = open(envPath, 'r')
    n = 0
    for i in fd.readlines():
       n+= 1
       if i.split(':')[0] == key: #判断键重复
         if n == len(lines):
          modify = key + ':' + value
         else:
          modify = key + ':' + value + '\n'
         lines[n-1] =  modify#判断时不是以|n为判断值的，修改是需要加上
         s = "".join(lines)
         n = -1  # 标记流程的进出
         fw = open(envPath, 'w')
         fw.write(s)
         break
    if n == len(lines):
        lines.append('\n' + key + ':' + value)
        p = "".join(lines)
        fc = open(envPath, 'w')
        fc.write(p)




if __name__ == '__main__':
    setVariable('__Author__','mytest')


