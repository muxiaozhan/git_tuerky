# -*- coding: utf-8 -*-
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath) #防止命令行找不到模块
formdir = os.path.dirname(os.getcwd())  # 获取上一级目录

import unittest
import datetime

nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
import logging

logging.basicConfig(filename=formdir + '\Logging\DateLog\%s.log' % nowTime,
                    format='%(asctime)s -%(name)s-%(levelname)s-%(module)s-%(funcName)s-[line:%(lineno)d]:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p', level=logging.INFO)

from HTMLTestRunner import HTMLTestRunner
# from Logging.LogConfig import LogAdd
from configwx.openConfig import getConfig
from configwx.dbConnect import sqllink
import json
import traceback
import requests
import time
#import pymysql.cursors
from decimal import Decimal


class MyTestSuite(unittest.TestCase):
    def sedUp(self):
        print("start...")

    def testCode(self):
        config = getConfig(0,formdir + "\configwx", "baseData.conf","gzwl_url")  # 获取前台url
        request_url = "/home/hot-car"
        url = config + request_url
        headers = {
            "Content-Type": "application/json",
            "cache-control": "no-cache"
        }
        response = requests.request("GET", url, headers=headers)  # Post接口调用
        results = response.text  # 对返回结果
        if response.status_code == 200:
            logging.info("Success:Status code is 200")  # 验证接口返回状态码
        else:
            logging.info("Http error code:%d" % response.status_code)
            raise Exception("Http error code:%d" % response.status_code)
            # else:
            # logging.info("Http error code:%d" %response.status_code)

    def testDatamatch(self):
        # 返回结果验证
        config = getConfig(0,formdir + "\configwx", "baseData.conf","gzwl_url")  # 获取前台url
        request_url = "/home/hot-car"
        url = config + request_url
        headers = {
            "Content-Type": "application/json",
            "cache-control": "no-cache"
        }
        response = requests.request("GET", url, headers=headers)  # Post接口调用
        results = response.text  # 对返回结果
        result = json.loads(results)
        # print(result)
        sql = "SELECT t.id,t.code,t.name,t.suitable_number,t.brand_id,p.id AS pid,p.name AS pname,m.id AS month_id,m.year,m.month,MIN(m.min_price)AS price FROM (SELECT * FROM `touring_car` WHERE is_delete = b'0' AND is_recommend = b'1' AND ENABLE = b'1') AS t LEFT JOIN  (SELECT * FROM touring_car_price_type WHERE `is_delete`= b'0' AND ENABLE = b'1') AS p ON p.`touring_car_id` = t.id  LEFT JOIN  (SELECT * FROM (SELECT *,base_price AS min_price FROM `touring_car_price_month` WHERE IF((LENGTH(CONCAT(YEAR,'-',MONTH))=6),INSERT(CONCAT(YEAR,'-',MONTH),5,1,'-0'),CONCAT(YEAR,'-',MONTH)) IN (IF(LEFT(DATE_SUB(NOW(),INTERVAL 0 MONTH),7)< LEFT(DATE_ADD(NOW(),INTERVAL (SELECT config_value FROM sys_config WHERE config_key = 'LeastAdvanceReserveDays' AND config_group = 'TouringCar' AND ENABLE = 1) DAY),7),NULL,LEFT(DATE_SUB(NOW(),INTERVAL 0 MONTH),7)),IF(LEFT(DATE_SUB(NOW(),INTERVAL -1 MONTH),7)< LEFT(DATE_ADD(NOW(),INTERVAL (SELECT config_value FROM sys_config WHERE config_key = 'LeastAdvanceReserveDays' AND config_group = 'TouringCar' AND ENABLE = 1) DAY),7),NULL,LEFT(DATE_SUB(NOW(),INTERVAL -1 MONTH),7)),IF(LEFT(DATE_SUB(NOW(),INTERVAL -2 MONTH),7)< LEFT(DATE_ADD(NOW(),INTERVAL (SELECT config_value FROM sys_config WHERE config_key = 'LeastAdvanceReserveDays' AND config_group = 'TouringCar' AND ENABLE = 1) DAY),7),NULL,LEFT(DATE_SUB(NOW(),INTERVAL -2 MONTH),7)),IF(LEFT(DATE_SUB(NOW(),INTERVAL -3 MONTH),7)< LEFT(DATE_ADD(NOW(),INTERVAL (SELECT config_value FROM sys_config WHERE config_key = 'LeastAdvanceReserveDays' AND config_group = 'TouringCar' AND ENABLE = 1) DAY),7),NULL,LEFT(DATE_SUB(NOW(),INTERVAL -3 MONTH),7)),IF(LEFT(DATE_SUB(NOW(),INTERVAL -4 MONTH),7)< LEFT(DATE_ADD(NOW(),INTERVAL (SELECT config_value FROM sys_config WHERE config_key = 'LeastAdvanceReserveDays' AND config_group = 'TouringCar' AND ENABLE = 1) DAY),7),NULL,LEFT(DATE_SUB(NOW(),INTERVAL -4 MONTH),7)),IF(LEFT(DATE_SUB(NOW(),INTERVAL -5 MONTH),7)< LEFT(DATE_ADD(NOW(),INTERVAL (SELECT config_value FROM sys_config WHERE config_key = 'LeastAdvanceReserveDays' AND config_group = 'TouringCar' AND ENABLE = 1) DAY),7),NULL,LEFT(DATE_SUB(NOW(),INTERVAL -5 MONTH),7))) AND is_delete = b'0' AND base_price <> 0 ORDER BY MONTH) g GROUP BY g.price_type_id ORDER BY MONTH) m ON m.price_type_id = p.id AND m.touring_car_id = p.touring_car_id WHERE p.id IS NOT NULL AND m.id IS NOT NULL GROUP BY t.code;"
        data = sqllink("db_gzwl", sql)
        # 校验数据数量，id，price匹配
        lenapi = len(result.get('data'))  # 获取列表内对象数量
        lensql = len(data)

        def toDecimal(numf):
            return Decimal.from_float(numf).quantize(Decimal("0.00"))

        if lenapi != lensql:
            logging.info(u"Result error:筛选结果数量不一致！")
            raise Exception(u"Result error:筛选结果数量不一致！")
        else:
            n = 0  # 初始化验证数量
            for i in range(lenapi):
                d = int(result.get('data')[i].get('id'))
                x = result.get('data')[i].get('price')
                p = toDecimal(x)
                for j in list(range(lensql)):
                    a = toDecimal(float(data[j].get('price')))
                    b = int(data[j].get('id'))
                    if b == d and a == p:
                        n += 1
                        del list(range(lensql))[j]  # 删除查找到的index
                        break
                    elif data[j].get('id') == data[-1].get('id'):
                        logging.info(u"Check error:id为%s的房车未在数据库中查询到！" % d)  # api的数据在数据库查询的结果中没有找到，说明数据有问题
                        raise Exception(u"Check error:id为%s的房车未在数据库中查询到！" % d)

                    else:
                        continue
        if n < lenapi:
            logging.info(u"Check count error:有%d条数据有误！" % (lenapi - n))
            raise Exception(u"Check count error:有%d条数据有误！" % (lenapi - n))
        else:
            logging.info(u"Success:数据查询无误！")

    def tearDown(self):
        pass


if __name__ == '__main__':
    # 构造测试集合
    suite = unittest.TestSuite()
    suite.addTest(MyTestSuite("testCode"))
    suite.addTest(MyTestSuite("testDatamatch"))
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = formdir + '\Results\\'+ now + 'result.html'
    fp = open(filename, 'wb')

    # 执行测试
    runner = HTMLTestRunner(stream=fp, title=u'测试报告', description=u'用例执行情况：')
    runner.run(suite)
    fp.close()  # 关闭报告文件
