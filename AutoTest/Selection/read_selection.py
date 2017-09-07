# -*- coding: utf-8 -*-
import sys
import os
from Selection.create_selection import create_selection,create_selection_file

def read_selection():
    selection = create_selection()
    create_selection_file(selection)
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = os.path.split(curPath)[0]
    sys.path.append(rootPath)   #防止命令行执行只会查找当前目录

    selectionFilePath =os.path.join(curPath , 'all_scripts_selection.txt')
    selection = []
    fd = open(selectionFilePath,'r',encoding= 'utf-8')
    for line in fd.readlines():
        selection.append(line.replace('\n',''))
    #print(selection)
    return  selection


if __name__ == '__main__':
    read_selection()