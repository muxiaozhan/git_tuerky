#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __Author__ = tuerky
import os
import sys
import configparser

def getConfig (forward,filePath,fileName,key): #forward 参数0是前台，1是后台,2是数据库
 os.chdir(filePath)  # 打开配置文件所在文件夹
 cf = configparser.ConfigParser()  # 实例化对象
 cf.read(fileName)

 if forward == 0 or forward == 1:

  FrontUrl = cf.get(key, "FrontUrl")
  BackUrl = cf.get(key, "BackUrl")
  config = [FrontUrl, BackUrl]
  return config[forward]

 else:
   host = cf.get(key, "db_host")  # 使用configparser模块获取配置参数
   port = cf.getint(key, "db_port")
   user = cf.get(key, "db_user")
   password = cf.get(key, "db_pass")
   db = cf.get(key, "db")
   charset = cf.get(key, "charset")
   curs = cf.get(key, "curs")
   config = [{'host': host, 'port': port, 'user': user, 'password': password, 'db': db, 'charset': charset,
              'cursorclass': curs}]
   return config[0]




if __name__ == '__main__':
 getConfig(1,filePath='D:/AutoTest/configwx',fileName='test.conf',key="gzwl_url")