# -*- coding: utf-8 -*-
#__Author__ = tuerky
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)  # 防止命令行找不到模块
formdir = os.path.dirname(os.getcwd())  # 获取上一级目录

import unittest
import datetime

nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
import logging

logging.basicConfig(filename=formdir + '\Logging\DateLog\%s.log' % nowTime,
                    format='%(asctime)s -%(name)s-%(levelname)s-%(module)s-%(funcName)s-[line:%(lineno)d]:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p', level=logging.INFO)

from HTMLTestRunner import HTMLTestRunner
from configwx.openConfig import getConfig
from configwx.getEnv import getVariable
from configwx.setEnv import setVariable
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
browser = webdriver.Chrome(chrome_options=options)


class MyTestSuite(unittest.TestCase):

    def sedUp(self):
        print("start...")

    def test_appOrder(self):

      web = getConfig(0, formdir + '\configwx', 'baseData.conf', 'gzwl_web')
      webUrl = web + '/account/index'
      browser.get(webUrl)
      time.sleep(2)
      browser.set_window_size(400, 850)
      time.sleep(2)
      info = browser.find_element_by_xpath("//div[@class=\"account custom page-view\"]/div[2]/div[1]/div[1]/div[1]").text
      if info == "":
        browser.find_element_by_xpath("//a[@href=\"/account/entry/sign\"]").click()
        time.sleep(3)
        currentUrl = browser.current_url
        preUrl = web + "/account/entry/sign"
        if currentUrl != preUrl:
            logging.info(u"准备登录页跳转不对！")
            raise Exception(u"准备登录页跳转不对！")

        else:
            browser.find_element_by_xpath("//input[@type=\"tel\"]").send_keys("18701913175")
            browser.find_element_by_xpath("//input[@type=\"password\"]").send_keys("54123456")
            browser.find_element_by_xpath("//button[@class=\"gz-btn\"]").click()
            time.sleep(3)
            currentUrl1 = browser.current_url
            if currentUrl1 != webUrl:
                logging.info(u"点击登录页跳转不对！")
                raise Exception(u"点击登录页跳转不对！")

            else:
                logging.info(u"登录成功！")

      browser.get(web + '/home')
      browser.find_element_by_xpath(
          "//div[@class=\"container\"]/div[@class=\"home-quick-entry\"]/div[3]").click()
      time.sleep(3)
      target = browser.find_element_by_xpath("//div[@class=\"line-section\"]/div[3]/div[@class=\"mask\"]")
      browser.execute_script("arguments[0].scrollIntoView();", target)  # 拖动到可见元素
      target.click()
      time.sleep(3)
      browser.find_element_by_xpath("//span[@class=\"left\"]").click()
      Locat = (By.XPATH, "//div[@class=\"month-data\"]/div[4]/div[6]/div[2]")
      time.sleep(1)
      try:
          WebDriverWait(browser, 20, 0.5).until(
              EC.presence_of_element_located(Locat))  # 每隔0.5秒判断是否存在对应元素，20秒期限
          browser.find_element_by_xpath("//div[@class=\"month-data\"]/div[4]/div[6]/div[2]").click()
      finally:
          pass
      time.sleep(2)
      browser.find_element_by_xpath("//div[@class=\"adult-tourist\"]/div[1]/span[@class=\"plus\"]").click()
      browser.find_element_by_xpath("//button[text()=\"下一步\"]").click()
      time.sleep(1)
      browser.find_element_by_xpath(
          "//div[@class=\"tourist-info\"]/div[2]/div[@class=\"adult\"]/span[text()=\"选择成人游客\"]").click()
      time.sleep(1)
      browser.find_element_by_xpath(
          "//div[@class=\"tourist-list\"]/div[@class=\"tourist-item\"]/div[@class=\"tourist-check\"]").click()
      time.sleep(1)
      browser.find_element_by_xpath("//div[@class=\"submit-btn\"]").click()
      time.sleep(2)
      browser.find_element_by_xpath("//button[text()=\"去支付\"]").click()
      time.sleep(2)
      browser.find_element_by_xpath("//button[text()=\"确认支付\"]").click()
      time.sleep(2)
      browser.find_element_by_xpath("//input[@type=\"number\"]").send_keys("8800886011003434801")
      browser.find_element_by_xpath("//input[@type=\"password\"]").send_keys("880897")
      checkmoney = browser.find_element_by_xpath("//div[@class=\"product-info\"]/div[3]/span[2]").text
      if checkmoney != '¥ 0.01':
          logging.info(u"我只有一分钱！")
          raise Exception(u"真的付不起！")
      else:
          browser.find_element_by_xpath("//button[text()=\"立即支付\"]").click()
          location = (By.XPATH,
                      "//div[@class=\"gz-alert show\"]/div[@class=\"gz-alert-content show\"]/div[@class=\"gz-alert-buttons\"]/div[@class=\"btn-wrap\"]/div[@class=\"gz-button left-button\"]")
          try:
              WebDriverWait(browser, 20, 0.5).until(
                  EC.presence_of_element_located(location))  # 每隔0.5秒判断元素，20秒期限
              time.sleep(1)
              browser.find_element_by_xpath(
                  "//div[@class=\"gz-alert show\"]/div[@class=\"gz-alert-content show\"]/div[@class=\"gz-alert-buttons\"]/div[@class=\"btn-wrap\"]/div[@class=\"gz-button left-button\"]").click()
          finally:
              time.sleep(1)
              lineproductOrderCode = browser.find_element_by_xpath("//div[@class=\"order-detail\"]/div[1]/span[2]").text
              setVariable('lineproductOrderCode', lineproductOrderCode)
              logging.info(u"本次生成的旅游订单code为：%s" % lineproductOrderCode)
              time.sleep(2)


    def test_backOrder(self):

        web = getConfig(1,formdir + '\configwx', 'baseData.conf', 'gzwl_web')
        webUrl = web + '/login'
        browser.get(webUrl)
        browser.maximize_window()
        time.sleep(1)
        browser.find_element_by_xpath("//input[@class=\"j-user\"]").send_keys("jianghao")
        browser.find_element_by_xpath("//input[@class=\"j-pass\"]").send_keys("jh131150")
        browser.find_element_by_xpath("//button[@id=\"btn_login\"]").click()
        browser.implicitly_wait(4)
        browser.find_element_by_xpath(
            "//div[@class=\"sidebar\"]/ul[@class=\"el-menu\"]/li[3]/div[@class=\"el-submenu__title\"]/i[@class=\"el-submenu__icon-arrow el-icon-arrow-down\"]").click()
        browser.find_element_by_xpath(
            "//div[@class=\"sidebar\"]/ul[@class=\"el-menu\"]/li[3]/ul[@class=\"el-menu\"]/li[3]").click()
        orderCode = getVariable('lineproductOrderCode')
        browser.find_element_by_xpath(
            "//form[@class=\"el-form el-form--label-right\"]/div[2]/div[1]/div[@class=\"el-form-item\"]/div[@class=\"el-form-item__content\"]/div[@class=\"el-input\"]/input[@autocomplete=\"off\"]").send_keys(orderCode)
        browser.find_element_by_xpath(
            "//form[@class=\"el-form el-form--label-right\"]/div[2]/div[4]/div[@class=\"el-form-item\"]/div[@class=\"el-form-item__content\"]/button[@type=\"button\"]").click()
        browser.find_element_by_xpath("//tr[@class=\"el-table__row \"]/td[7]/div[@class=\"cell\"]/div[1]/button[@type=\"button\"]").click()
        target = browser.find_element_by_xpath(
            "//form[@class=\"el-form el-form--label-right\"]/div[6]/div[2]/form[@class=\"el-form\"]/div[@class=\"el-row\"]/div[1]/div[1]/div[1]/button[@type=\"button\"]/span[1]")
        browser.execute_script("arguments[0].scrollIntoView();", target)
        target.click()
        time.sleep(2)
        browser.find_element_by_xpath(
            "//form[@class=\"el-form el-form--label-right\"]/div[6]/div[2]/form[@class=\"el-form\"]/div[@class=\"el-row\"]/div[1]/div[1]/div[1]/button[@type=\"button\"]").click()
        time.sleep(1)
        e1 = "//div[@class=\"el-dialog__wrapper dialogTakeLimo\"]/div[1]/div[2]/form[1]/div[1]/div[1]/div[1]/textarea[@type=\"textarea\"]"
        browser.find_element_by_xpath(e1).click()
        browser.find_element_by_xpath(e1).send_keys(u"自动化订单备注订单号：%s" % orderCode)
        time.sleep(1)
        browser.find_element_by_xpath(
            "//div[@class=\"el-dialog__wrapper dialogTakeLimo\"]/div[1]/div[3]/div[1]/button[1]").click()
        time.sleep(1)
        logging.info(u"%s旅游订单已完成！"% orderCode)
        browser.close()

    def test_rebackOrder(self):

        web = getConfig(1, formdir + '\configwx', 'baseData.conf', 'gzwl_web')
        webUrl = web + '/login'
        browser.get(webUrl)
        browser.maximize_window()
        time.sleep(1)
        browser.find_element_by_xpath("//input[@class=\"j-user\"]").send_keys("jianghao")
        browser.find_element_by_xpath("//input[@class=\"j-pass\"]").send_keys("jh131150")
        browser.find_element_by_xpath("//button[@id=\"btn_login\"]").click()
        browser.implicitly_wait(4)
        browser.find_element_by_xpath(
            "//div[@class=\"sidebar\"]/ul[@class=\"el-menu\"]/li[3]/div[@class=\"el-submenu__title\"]/i[@class=\"el-submenu__icon-arrow el-icon-arrow-down\"]").click()
        browser.find_element_by_xpath(
            "//div[@class=\"sidebar\"]/ul[@class=\"el-menu\"]/li[3]/ul[@class=\"el-menu\"]/li[3]").click()
        orderCode = getVariable('lineproductOrderCode')
        browser.find_element_by_xpath(
            "//form[@class=\"el-form el-form--label-right\"]/div[2]/div[1]/div[@class=\"el-form-item\"]/div[@class=\"el-form-item__content\"]/div[@class=\"el-input\"]/input[@autocomplete=\"off\"]").send_keys(
            orderCode)
        browser.find_element_by_xpath(
            "//form[@class=\"el-form el-form--label-right\"]/div[2]/div[4]/div[@class=\"el-form-item\"]/div[@class=\"el-form-item__content\"]/button[@type=\"button\"]").click()
        browser.find_element_by_xpath(
            "//tr[@class=\"el-table__row \"]/td[7]/div[@class=\"cell\"]/div[1]/button[@type=\"button\"]").click()
        target = browser.find_element_by_xpath(
            "//form[@class=\"el-form el-form--label-right\"]/div[6]/div[2]/form[@class=\"el-form\"]/div[@class=\"el-row\"]/div[1]/div[1]/div[1]/button[@type=\"button\"]/span[1]")
        browser.execute_script("arguments[0].scrollIntoView();", target)
        target.click()
        time.sleep(2)
        browser.find_element_by_xpath(
            "//form[@class=\"el-form el-form--label-right\"]/div[6]/div[2]/form[@class=\"el-form\"]/div[@class=\"el-row\"]/div[1]/div[1]/div[1]/button[2]").click()
        time.sleep(1)
        browser.find_element_by_xpath(
            "//div[@class=\"el-dialog__wrapper\"]/div[1]/div[2]/form[1]/div[1]/div[@class=\"el-form-item__content\"]/div[@class=\"el-textarea\"]/textarea[@type=\"textarea\"]").send_keys(u"自动取消订单%s"%orderCode)
        browser.find_element_by_xpath(
            "//div[@class=\"el-dialog__wrapper\"]/div[1]/div[2]/form[1]/div[4]/div[@class=\"el-form-item__content\"]/div[@class=\"el-input\"]/input[@type=\"text\"]").send_keys("0.01")
        browser.find_element_by_xpath(
            "//div[@class=\"el-dialog__wrapper\"]/div[1]/div[2]/form[1]/div[5]/div[@class=\"el-form-item__content\"]/div[@class=\"el-textarea\"]/textarea[@type=\"textarea\"]").send_keys(u"备注取消订单")
        browser.find_element_by_xpath(
            "//div[@class=\"el-dialog__wrapper\"]/div[1]/div[3]/div[1]/button[2]").click()
        time.sleep(1)
        browser.find_element_by_xpath(
            "//div[@class=\"page-content order-detail\"]/form[1]/div[6]/div[2]/form[1]/div[4]/div[4]/button[@type=\"button\"]").click()
        time.sleep(1)
        browser.find_element_by_xpath(
            "//div[@class=\"el-table__body-wrapper\"]/table[@class=\"el-table__body\"]/tbody[1]/tr[1]/td[9]/div[1]/div[1]/button[2]").click()
        browser.find_element_by_xpath(
            "//div[@class=\"el-dialog__wrapper refunds-form\"]/div[1]/div[2]/form[1]/div[7]/div[1]/div[@class=\"el-textarea\"]/textarea[@type=\"textarea\"]").send_keys(u"自动退款")
        time.sleep(2)
        browser.find_element_by_xpath(
            "//div[@class=\"el-dialog__wrapper refunds-form\"]/div[1]/div[3]/span[1]/button[1]").click()
        time.sleep(1)
        browser.find_element_by_xpath(
            "//div[@class=\"el-dialog__wrapper refunds-form\"]/div[1]/div[3]/span[1]/button[3]").click()
        logging.info(u"%s旅游订单已提交退款！"% orderCode)
        time.sleep(1)



    def tearDown(self):
        pass


if __name__ == '__main__':
    # 构造测试集合
    suite = unittest.TestSuite()
    suite.addTest(MyTestSuite("test_appOrder"))
    suite.addTest(MyTestSuite("test_rebackOrder"))
    suite.addTest(MyTestSuite("test_appOrder"))
    suite.addTest(MyTestSuite("test_backOrder"))
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = formdir + '\Results\\'+ now + 'result.html'
    fp = open(filename, 'wb')

    # 执行测试
    runner = HTMLTestRunner(stream=fp, title=u'测试报告', description=u'用例执行情况：')
    runner.run(suite)
    fp.close()  # 关闭报告文件
