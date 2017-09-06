import unittest
import time
import re
import  traceback
import HTMLTestRunner
from  xml.dom.minidom  import parse
from  selenium  import webdriver
from  selenium.webdriver.common.by import By
from  selenium.webdriver.support.ui import WebDriverWait
from  selenium.webdriver.support import  expected_conditions as EC
import selenium.common.exceptions  as e
from public.logIn import login
from util.logger import L

dom=parse("./public/config.xml")
root=dom.documentElement
class TestLan(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.ip=root.getElementsByTagName("changeIP")[0].getAttribute("ip")
        self.baseurl=root.getElementsByTagName("lan")[0].getAttribute("baseurl")

    def test_gotolan(self):
        """测试是否能成功跳转到局域网页面"""
        L.info("test_gotolan START:测试是否能成功跳转到局域网页面")
        driver = self.driver
        print("caseid:001")
        driver.get(self.baseurl)
        #调用登录模块登录
        login(driver)
        driver.implicitly_wait(30)
        driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
        time.sleep(2)
        driver.find_element_by_id("lang_dhcpsever").click()
        currenturl=driver.current_url
        L.info("到达局域网页面后的URL:%s" % currenturl)
        self.assertEqual("http://192.168.0.1/DhcpServer.html",currenturl)
        L.info("test_gotolan STOP")
    def test_defaultcheck(self):
        """默认项检查"""

        L.info("test_defaultcheck START:局域网页面默认项检查")
        driver = self.driver
        print("caseid:002")
        driver.get(self.baseurl)
        login(driver)
        time.sleep(3)
        driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
        time.sleep(2)
        driver.find_element_by_id("lang_dhcpsever").click()
        #t=driver.find_element_by_id("lanIP").get_attribute('name')
        js = "document.getElementById('lanIP').value;"
        #js="eval(document.getElementById('lanIP')).value;"
        #js=eval(document.getElementById('lanIP').value)

        t=driver.execute_script(js)
        L.info('###############')
        L.info(t)
        L.info("test_defaultcheck STOP")
    def test_noip(self):
        """不输入IP 地址，检查提示信息"""
        L.info("test_noip Start:不输入IP 地址，检查提示信息")
        driver = self.driver
        print("caseid:003")
        driver.get(self.baseurl)
        login(driver)
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
        driver.find_element_by_id("lang_dhcpsever").click()
        time.sleep(3)
        #清除输入框中的内容
        driver.find_element_by_id("lanIP").clear()
        #driver.find_element_by_id("lanIP").send_keys("4444444")
       #L.info(driver.find_element_by_id("lanIP").text
        driver.find_element_by_id("savebutton5").click()
        try:
            element = driver.find_element_by_id("errorinfo_1")
        except e.NoSuchElementException:
            L.error(traceback.format_exc())
        else:
            self.assertEqual('请输入IP地址。', element.text)
        L.info("test_noip STOP")
    def test_wrongip(self):
        """输入错误格式的ip地址，检查提示语"""
        L.info("test_wrongip:输入错误格式的ip地址，检查提示语")
        driver = self.driver
        print("caseid:004")
        result = 0
        driver.get(self.baseurl)
        login(driver)
        driver.implicitly_wait(2)
        driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
        driver.find_element_by_id("lang_dhcpsever").click()
        time.sleep(3)
        # 清除输入框中的内容
        driver.find_element_by_id("lanIP").clear()
        wrongip = ['192.168.www.4', '192.!23.tt.com', '192.168.%$.#', '1 92.168.  34', '192.168.344.2', '192.-168.3.2']
        for ip in wrongip:
            driver.find_element_by_id("lanIP").send_keys(ip)
            driver.find_element_by_id("savebutton5").click()
            try:
                driver.find_element_by_id("errorinfo_1")
            except e.NoSuchElementException:
                L.error(traceback.format_exc())
            else:
                if (driver.find_element_by_id("errorinfo_1").text == "IP地址含非法字符，请重新输入。")or\
                        (driver.find_element_by_id("errorinfo_1").text == "IP地址格式错误，请重新输入。"):
                    result += 1
                    driver.find_element_by_id("lanIP").clear()
                    time.sleep(2)
                    print("result:"+str(result))
        self.assertEqual(len(wrongip), result)
        L.info("test_wrongip STOP")
    def test_changeip(self):
        """修改局域网ip 地址"""
        L.info("test_changeip:修改局域网ip 地址，并等待修改完重启后，新地址可以登录")
        driver=self.driver
        print("caseid:005")
        baseurl=self.baseurl
        ip=self.ip
        L.info("准备将登录修改为：%s" % ip)
        originalip=re.split("//",self.baseurl)[1]
        L.info("原来的登录地址为 %s" % originalip)
        driver.get(baseurl)
        login(driver)
        driver.implicitly_wait(3)
        driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
        time.sleep(1)
        driver.find_element_by_id("lang_dhcpsever").click()
        time.sleep(1)
        driver.find_element_by_id("lanIP").clear()
        driver.find_element_by_id("lanIP").send_keys(ip)
        driver.find_element_by_id("savebutton5").click()
        time.sleep(2)
        try:
            element = WebDriverWait(driver,60).until(
                EC.invisibility_of_element_located((By.ID, "CreatePopAlertMessage"))
            )
            time.sleep(5)
            self.assertEqual("http://" + str(ip) + "/Login.html", driver.current_url)

        finally:
            L.info("修改成功，二次登录")
            login(driver)
            time.sleep(2)
            L.info("登录后，进入新的配置系统，二次修改局域网ip 地址为原来的地址，")
            driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
            time.sleep(1)
            driver.find_element_by_id("lanIP").clear()
            driver.find_element_by_id("lanIP").send_keys(originalip)
            driver.find_element_by_id("savebutton5").click()
            time.sleep(2)
            try:
                element = WebDriverWait(driver, 60).until(
                    EC.invisibility_of_element_located((By.ID, "CreatePopAlertMessage"))
                )
            finally:
                self.assertEqual("http://" + str(originalip) + "/Login.html", driver.current_url)
            L.info("test_changeip STOP")
    def test_startlaniperror(self):
        """开始ip地址范围非法，提示信息检查"""
        L.info("test_startlaniperror START:开始ip地址范围非法，提示信息检查")
        driver = self.driver
        print("caseid:006")
        driver.get(self.baseurl)
        login(driver)
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
        driver.find_element_by_id("lang_dhcpsever").click()
        time.sleep(3)
        driver.find_element_by_id("startLanIp").clear()
        driver.find_element_by_id("startLanIp").send_keys("-1")
        driver.find_element_by_id("endLanIp").clear()
        driver.find_element_by_id("endLanIp").send_keys("256")
        driver.find_element_by_id("savebutton5").click()
        errorinfo2=driver.find_element_by_id("errorinfo_2")
        result=True
        try:

            if errorinfo2.is_displayed():
                self.assertEqual(errorinfo2.text,"地址池开始值错误，请重新输入。")
            else:
                result=False
        except e.NoSuchElementException:
            L.error(traceback.format_exc())
        self.assertTrue(result)
    def test_endlaniperror(self):
        """结束ip地址非法，提示信息检查"""
        L.info("test_endlaniperror START:结束ip地址非法，提示信息检查")
        driver = self.driver
        print("caseid:007")
        try:
            login(driver)
        except e.NoSuchElementException:
            L.info("登录系统失败")
            L.error(traceback.format_exc())

        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
        driver.find_element_by_id("lang_dhcpsever").click()
        time.sleep(3)
        driver.find_element_by_id("startLanIp").clear()
        driver.find_element_by_id("startLanIp").send_keys("2")
        driver.find_element_by_id("endLanIp").clear()
        driver.find_element_by_id("endLanIp").send_keys("255")
        driver.find_element_by_id("savebutton5").click()
        time.sleep(1)
        errorinfo2 = driver.find_element_by_id("errorinfo_2")
        result = True
        try:
            if errorinfo2.is_displayed():
                self.assertEqual(errorinfo2.text, "地址池结束值错误，请重新输入。")
            else:
                result = False
        except e.NoSuchElementException:
            L.error(traceback.format_exc())
        self.assertTrue(result)
        L.info("test_endlaniperror STOP")
    def test_startipbigger(self):
        """开始ip地址大于结束ip地址"""
        L.info("test_startipbigger START:开始ip地址大于结束ip地址，提示信息检查")
        driver = self.driver
        print("caseid:008")
        driver.get(self.baseurl)
        login(driver)
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
        driver.find_element_by_id("lang_dhcpsever").click()
        time.sleep(3)
        driver.find_element_by_id("startLanIp").clear()
        driver.find_element_by_id("startLanIp").send_keys("234")
        driver.find_element_by_id("endLanIp").clear()
        driver.find_element_by_id("endLanIp").send_keys("12")
        driver.find_element_by_id("savebutton5").click()
        time.sleep(1)
        errorinfo2 = driver.find_element_by_id("errorinfo_2")
        result = True
        try:
            if errorinfo2.is_displayed():
                self.assertEqual(errorinfo2.text, "地址池结束值不能小于开始值，请重新输入。")
            else:
                result = False
        except e.NoSuchElementException:
            L.error(traceback.format_exc())
        self.assertTrue(result)
        L.info("test_startipbigger STOP")
    def test_lanipinrange(self):
        """用例失败的原因是因为元素能定位到，但是拿不到值"""
        L.info("test_lanipinrange START:ip地址填正确是否可以保存成功")
        driver = self.driver
        print("caseid:009")
        driver.get(self.baseurl)
        login(driver)
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
        driver.find_element_by_id("lang_dhcpsever").click()
        time.sleep(3)
        driver.find_element_by_id("startLanIp").clear()
        driver.find_element_by_id("startLanIp").send_keys("100")
        driver.find_element_by_id("endLanIp").clear()
        driver.find_element_by_id("endLanIp").send_keys("150")
        driver.find_element_by_id("savebutton5").click()
        time.sleep(1)
        try:
            element = WebDriverWait(driver, 60).until(
                EC.invisibility_of_element_located((By.ID, "CreatePopAlertMessage"))
            )
        finally:
            self.assertEqual(100,driver.find_element_by_id("startLanIp").text)
            L.info("test_lanipinrange STOP")
    def test_dhcpclose(self):
        """关闭 dhcp 功能检查"""
        L.info("test_dhcpclose START:关闭dhcp功能，检查页面租期和范围不展示")
        driver = self.driver
        print("caseid:010")
        driver.get(self.baseurl)
        login(driver)
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
        driver.find_element_by_id("lang_dhcpsever").click()
        time.sleep(1)
        driver.find_element_by_id("dhcp_statue").click()
        result=True
        if not driver.find_element_by_id("dhcppool").is_displayed():
            self.assertTrue(result)
        else :
            result=False
            self.assertTrue(result)
        #driver.find_element_by_id("savebutton5").click()
        L.info("test_dhcpclose STOP")
    def tearDown(self):
        self.driver.close()
if __name__ == "__main__":
    suite=unittest.TestSuite()
    # suite.addTest(TestLan('test_gotolan'))
    # suite.addTest(TestLan('test_defaultcheck'))
    # suite.addTest(TestLan('test_noip'))
    # suite.addTest(TestLan('test_wrongip'))
    # suite.addTest(TestLan('test_startlaniperror'))
    # suite.addTest(TestLan('test_endlaniperror'))
    # suite.addTest(TestLan('test_startipbigger'))
    # suite.addTest(TestLan('test_endlaniperror'))
    # suite.addTest(TestLan('test_startipbigger'))
    suite.addTest(TestLan('test_lanipinrange'))
    # suite.addTest(TestLan('test_dhcpclose'))

    now = time.strftime("%Y-%m-%d %H_%M_%S")

    filename = r'./result/' + now + '_result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"墙壁式无线wifi测试", description=u"用例执行情况:")
    runner.run(suite)
    fp.close()
    # runner = unittest.TextTestRunner()
    # runner.run(suite)