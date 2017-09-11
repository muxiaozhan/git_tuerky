# -*- coding: utf-8 -*-
# __Author__ = tuerky
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from Selection.execute_selection import execute_selection

if __name__ == '__main__':
    execute_selection()