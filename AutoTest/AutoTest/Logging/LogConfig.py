#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import datetime
import logging
import logging.config

def LogAdd(mat):
    formdir = os.path.dirname(os.getcwd())
    path = sys.path[0]
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
    pathDetail = path + '\\DateLog\\' + nowTime + '.log'
    for i in os.walk(os.path.join(path, 'DateLog')):
        # if not os.path.exists(pathDetail):
        # os.mknod(pathDetail,'w')
        for file in i[2:3][0]:
            open(pathDetail, 'w')
            CONF = formdir + '\\baseData.conf'
            logging.config.fileConfig(CONF)
            Log = logging.getLogger(name='root')
            #fh = logging.FileHandler('D:\AutoTest\Logging\DateLog\%s.log' % nowTime)
            #fh.setLevel(logging.INFO)
            #Log.addHandler(fh)
            return Log.info(mat)

if __name__ == '__main__':
    LogAdd(mat= sys.argv[0])














