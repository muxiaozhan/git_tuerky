#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __Author__ = tuerky
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import pymysql.cursors
from configwx.openConfig import getConfig

def sqllink(db,sql):
    formdir = os.path.dirname(os.getcwd())
    configdata = getConfig(2,formdir + "\configwx", "baseData.conf",db)
    connection = pymysql.connect(**configdata)  # 数据库的链接
    # cur = connection.cursor()  # 获取一个游标
    try:
        with connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql) #执行具体数据库操作
            data = cursor.fetchall()  ##将所有查询结果返回为元组,加上了字典游标返回的是字典
        connection.commit()

    finally:
        return data
        connection.close()