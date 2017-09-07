# -*- coding: utf-8 -*-
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from Selection.read_selection import read_selection


def execute_selection():
    selection = read_selection()
    for scriptPath in selection:
        os.system('python '+scriptPath)