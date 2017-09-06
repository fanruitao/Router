
from  selenium  import webdriver
import unittest
import HTMLTestRunner
import time
from  xml.dom.minidom  import parse
from  selenium.webdriver.common.by import By
from  selenium.webdriver.support.ui import WebDriverWait
from  selenium.webdriver.support import  expected_conditions as EC
import traceback
from util.logger import L
from selenium.common.exceptions import NoSuchElementException
import re
from public.logIn import login
import os
import subprocess

dom=parse("./public/config.xml")
root=dom.documentElement
class TestWifi(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.baseurl = root.getElementsByTagName("wifi")[0].getAttribute("baseurl")
    def test_gotowifi(self):
        """是否可以成功跳转到无线设置页面"""
        L.info("test_gotowifi START:是否可以成功跳转到无线设置页面")
        driver = self.driver
        print("caseid:035")
        driver.get(self.baseurl)
        login(driver)
        time.sleep(2)
        driver.find_element_by_id("wirless").click()
        time.sleep(1)
        currenturl=driver.current_url
        self.assertEqual(currenturl,"http://192.168.0.1/Wireless.html")
        L.info("test_gotowifi STOP")
    def test_defaultargument(self):
        """默认项检查"""
        print("caseid:036")
        pass
    def test_wifinameright(self):
        """各种组合下的无线名称是否支持"""
        L.info("test_wifinameright START:各种组合下的无线名称是否支持")
        driver = self.driver
        print("caseid:037")
        driver.get(self.baseurl)
        driver.implicitly_wait(5)
        result=0
        login(driver)
        time.sleep(2)
        driver.find_element_by_id("wirless").click()
        time.sleep(1)
        wifiname=['wer','#￥@','@!$as','@#￥12','1','22222222________!!!!!!!!aaaaaaaa','测试','hello world',"frt_test"]
        #wifiname = ['wer']
        for i in wifiname:
            time.sleep(3)
            driver.find_element_by_id('wifiName_24').clear()
            driver.find_element_by_id('wifiName_24').send_keys(i)
            time.sleep(5)
            driver.find_element_by_xpath("//input[@id='savebutton']").click()
            #driver.find_element_by_id('savebutton').click()
            time.sleep(2)
            try:
                driver.find_element_by_id("saveconfirm2_5G").click()
                WebDriverWait(driver, 20).until(
                    EC.invisibility_of_element_located((By.ID, "CreatePopAlertMessage"))
                )
                js = "document.getElementById('wifiName_24').value;"
                t = driver.execute_script(js)
                if i == t:
                    result += 1
                else:
                    L.info("未保存成功")
            except NoSuchElementException :
                 L.info(traceback.format_exc())

        self.assertEqual(len(wifiname), result, "目前失败的原因是input 元素取不到值")
        L.info("test_wifinameright STOP")
    def test_nowifiname(self):
        """不填写无线用户时的提示信息检查"""
        L.info("test_nowifiname START:不填写无线用户时的提示信息检查")
        driver = self.driver
        print("caseid:038")
        driver.get(self.baseurl)
        login(driver)
        time.sleep(2)
        driver.find_element_by_id("wirless").click()
        time.sleep(3)
        driver.find_element_by_id('wifiName_24').clear()
        driver.find_element_by_xpath("//input[@id='savebutton']").click()
        result=True
        if driver.find_element_by_id("errorinfo_1").is_displayed():
            self.assertEqual("请输入2.4G无线名称。",driver.find_element_by_id("errorinfo_1").text)
        else:
            result=False
        self.assertTrue(result)
        L.info("test_nowifiname STOP")
    def test_nopassword(self):
        """不填写密码时的功能检查"""
        L.info("test_nopassword START:不填写密码时的功能检查")
        driver = self.driver
        print("caseid:039")
        driver.get(self.baseurl)
        login(driver)
        time.sleep(2)
        driver.find_element_by_id("wirless").click()
        time.sleep(3)
        driver.find_element_by_id("password1_24").clear()
        driver.find_element_by_xpath("//input[@id='savebutton']").click()
        try:
            driver.find_element_by_id("saveconfirm2_5G").click()
            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.ID, "CreatePopAlertMessage"))
            )
            js = "document.getElementById('password1_24').value;"
            t = driver.execute_script(js)
            L.info(t)
            self.assertEqual(t,None)
        except NoSuchElementException:
            L.info(traceback.format_exc())
        L.info("test_nopassword STOP")
    def test_wrongpassword(self):
        """无线密码错误，提示语检查"""
        L.info("test_wrongpassword START:错误的无线密码，提示信息检查")
        driver = self.driver
        print("caseid:040")
        driver.get(self.baseurl)
        login(driver)
        time.sleep(2)
        driver.find_element_by_id("wirless").click()
        time.sleep(1)
        wifipassword=["ee","hello world","你好"]
        for i in wifipassword:
            driver.find_element_by_id('password1_24').clear()

            driver.find_element_by_id('password1_24').send_keys(i)
            time.sleep(5)
            driver.find_element_by_xpath("//input[@id='savebutton']").click()
            # driver.find_element_by_id('savebutton').click()
            time.sleep(2)
            if driver.find_element_by_id("errorinfo_2").is_displayed():
                errorinfo=driver.find_element_by_id("errorinfo_2").text
                if (errorinfo=="2.4G无线密码不能包含空格，请重新输入。" )or\
                        (errorinfo=="2.4G无线密码长度错误，请输入8至63个字符。")\
                        or (errorinfo=="2.4G无线密码中存在非法字符，请重新输入。"):
                    result=True

                else:
                    result = False
            self.assertTrue(result)
        L.info("test_wrongpassword STOP")
    def test_wifipasswordright(self):
        """格式正确的wifi 密码输入后是否可以成功保存"""
        L.info("test_wifipasswordright START:格式正确的wifi 密码输入后是否可以成功保存")
        driver = self.driver
        print("caseid:041")
        driver.get(self.baseurl)
        login(driver)
        time.sleep(2)
        driver.find_element_by_id("wirless").click()
        time.sleep(1)
        result=0
        wifipassword = ["werwerwer", ":#$@Q#$@Q#$@Q","@!$as@!$as@!$as","@#$12@#$12","!@#$%^a!","iot123321"]
        for i in wifipassword:
            time.sleep(2)
            driver.find_element_by_id('password1_24').clear()
            driver.find_element_by_id('password1_24').send_keys(i)
            time.sleep(5)
            driver.find_element_by_xpath("//input[@id='savebutton']").click()
            try:

                driver.find_element_by_id("saveconfirm2_5G").click()
                WebDriverWait(driver, 40).until(
                    EC.invisibility_of_element_located((By.ID, "CreatePopAlertMessage"))
                )
                js = "document.getElementById('password1_24').value;"
                t = driver.execute_script(js)
                if t==i:
                    result+=1
                else:
                    L.info("未保存成功")
            except NoSuchElementException:
                L.info(traceback.format_exc())
        self.assertEqual(len(wifipassword), result, "目前失败的原因是input 元素取不到值")
        L.info("test_wifipasswordright STOP")
    def test_wificlose(self):
        """关闭WiFi功能检查"""
        L.info("test_wificlose START:关闭WiFi功能后，查看电脑的无线列表中是否还有wifi 信息")
        driver = self.driver
        print("caseid:042")
        driver.get(self.baseurl)
        login(driver)
        time.sleep(2)
        driver.find_element_by_id("wirless").click()
        time.sleep(1)
        driver.find_element_by_id("wlan_status").click()
        time.sleep(5)
        result = True
        try:
            driver.find_element_by_id("clowifyconfirm2g").click()
            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.ID, "CreatePopAlertMessage"))
            )
        except NoSuchElementException:
            L.error(traceback.format_exc())
        # file=os.popen("netsh wlan show network").read()
        # L.info(file)
        # if not re.search('SSID\s+\d+\s+:\frt_test',file):
        #     L.info("test pass")
        #     result=True
        # else:
        #     result=False
        # self.assertTrue(result)
        # 也可以用subprocess 调用实现

        # p = subprocess.Popen('netsh wlan show network', stdout=subprocess.PIPE)
        # print (p)
        # t=str(p.stdout.read())
        # t = t.split("\\n")
        # print(t)
        # for i in t:
        #     print(i)
        #     if not re.search('SSID\s+\d+\s+:\frt_test', i):
        #         L.info("test pass")
        # 测试完成，再次开启
        result = True
        p = subprocess.Popen('netsh wlan show network', stdout=subprocess.PIPE)
        #print(p.stdout.readlines())
        for line in p.stdout.readlines():
            if not re.search('SSID\s+\d+\s+:\frt_test', str(line)):
                L.info("no found")
            else:
                result = False
                break
        self.assertTrue(result)

        driver.find_element_by_id("wlan_status").click()
        time.sleep(2)
        try:

            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.ID, "CreatePopAlertMessage"))
            )
        except NoSuchElementException:
            L.error(traceback.format_exc())
        L.info("test_wificlose STOP")
    def test_wifinamehide(self):
        """隐藏wifi 名字不被发现"""
        L.info("test_wifinamehide START:隐藏wifi 名字不被发现后，查看电脑的无线wifi列表 是否还有，无线名字 ")
        driver = self.driver
        print("caseid:043")
        driver.get(self.baseurl)
        login(driver)
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
        time.sleep(1)
        driver.find_element_by_id("lang_wirelessSetUp").click()
        time.sleep(1)
        driver.find_element_by_id("lang_advwlanset").click()
        time.sleep(10)
        driver.find_element_by_id("wlan_status").click()
        driver.find_element_by_id("savebutton").click()
        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located((By.ID, "CreatePopAlertMessage"))
        )
        result = True
        p = subprocess.Popen('netsh wlan show network', stdout=subprocess.PIPE)
        # print(p.stdout.readlines())
        for line in p.stdout.readlines():
            if not re.search('SSID\s+\d+\s+:\frt_test', str(line)):
                L.info("no found")
            else:
                result = False
                break
        self.assertTrue(result)
        #测试完成后恢复初始状态
        time.sleep(10)
        driver.find_element_by_id("wlan_status").click()
        time.sleep(2)
        try:

            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.ID, "CreatePopAlertMessage"))
            )
        except NoSuchElementException:
            L.info(traceback.format_exc())
        driver.find_element_by_id("savebutton").click()

        L.info("test_wifinamehide STOP")
    def tearDown(self):
        self.driver.close()
if __name__ == "__main__":
    suite=unittest.TestSuite()
    suite.addTest(TestWifi('test_gotowifi'))
    suite.addTest(TestWifi('test_defaultargument'))
    suite.addTest(TestWifi('test_wifinameright'))
    suite.addTest(TestWifi('test_nowifiname'))
    suite.addTest(TestWifi('test_nopassword'))
    suite.addTest(TestWifi('test_wrongpassword'))
    suite.addTest(TestWifi('test_wifipasswordrigh'))
    suite.addTest(TestWifi('test_wifinamehide'))
    suite.addTest(TestWifi('test_wificlose'))

    now = time.strftime("%Y-%m-%d %H_%M_%S")

    filename = r'./result/' + now + '_result.html'
    fp =open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"墙壁式无线wifi测试", description=u"用例执行情况:")
    runner.run(suite)
    fp.close()
    # runner = unittest.TextTestRunner()
    # runner.run(suite)