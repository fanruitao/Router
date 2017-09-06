
import unittest
import time
import traceback
from  selenium  import webdriver
import HTMLTestRunner
import selenium.common.exceptions as e
from  xml.dom.minidom  import parse
from util.logger import L
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


dom=parse("./public/config.xml")
root=dom.documentElement
class TestLogIn(unittest.TestCase):
    """登录首页测试用例"""
    def setUp(self):

        self.driver= webdriver.Chrome()
        logintag=root.getElementsByTagName('login')
        self.wrongpassword=logintag[0].getAttribute('wrongpassword')
        self.rightpassword = logintag[0].getAttribute('rightpassword')
        self.baseurl=logintag[0].getAttribute("baseurl")

    def test_goto_login(self):
        """登录页跳转测试"""
        L.info("test_goto_login START:登录页面第一个测试用例，测试是否能成功跳转到登录页面")
        driver=self.driver
        print("caseid:011")
        driver.get(self.baseurl)
        L.info("URL 输入后的页面名称：%s" % driver.title)
        self.assertEqual(driver.title,"DIR-823Pro")
        L.info("test_goto_login STOP")

    def test_login_right(self):
        """正确的密码登录"""
        L.info("test_login_right START:输入正确的密码验证是否能成功登录")
        driver=self.driver
        print("caseid:012")
        rightpassword=self.rightpassword
        driver.get(self.baseurl)
        L.info(driver.title)
        L.info("未登录之前的URL: %s"% driver.current_url)
        driver.find_element_by_id("admin_Password1").send_keys(rightpassword)
        driver.find_element_by_id("logIn_btn").click()
        time.sleep(5)
        loginurl=driver.current_url
        L.info("登录成功后的URL:%s" %loginurl)
        expecturl='http://192.168.0.1/Home.html'
        self.assertEqual(loginurl,expecturl)
        L.info("test_login_right STOP")
    def test_login_nopasswordenter(self):
        """不输入密码时的提示信息检查"""
        L.info("test_login_nopasswordenter START:不输入密码时的提示信息检查")
        driver = self.driver
        print("caseid:013")
        driver.get(self.baseurl)
        driver.find_element_by_id("logIn_btn").click()
        error1=driver.find_element_by_id("errorinfo_1")
        time.sleep(1)
        result=True
        try:
            if error1.is_displayed():
                L.info(error1.text)
                self. assertEqual(error1.text,"请输入登录密码。")
            else :
                result=False
        except e.NoSuchElementException:
            L.error(traceback.format_exc())
        self.assertTrue(result)
        L.info("test_login_nopasswordenter STOP")

    def test_login_wrongpassword(self):
        """输入错误密码"""
        L.info("test_login_wrongpassword START:密码错误时的提示语检查")
        driver=self.driver
        print("caseid:014")
        wrongpassword=self.wrongpassword
        driver.get(self.baseurl)
        driver.find_element_by_id("admin_Password1").send_keys("123")
        driver.find_element_by_id("logIn_btn").click()
        time.sleep(1)
        error2 = driver.find_element_by_id("errorinfo_1")
        result=True
        try:

            if error2.is_displayed():
                L.info(error2.text)
                self.assertEqual(error2.text,"密码错误，请重新输入。")
            else:
                result=False
        except e.NoSuchElementException:
            L.error(traceback.format_exc())
        self.assertTrue(result, True)
        L.info("test_login_wrongpassword STOP")
    def tearDown(self):
        self.driver.close()



if __name__ == "__main__":
    suite=unittest.TestSuite()
    suite.addTest(TestLogIn('test_goto_login'))
    suite.addTest(TestLogIn('test_login_right'))
    # suite.addTest(TestLogIn('test_login_nopasswordenter'))
    # suite.addTest(TestLogIn('test_login_wrongpassword'))

    now = time.strftime("%Y-%m-%d %H_%M_%S")

    filename = r'./result/' + now + '_result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"墙壁式无线wifi测试", description=u"用例执行情况:")
    runner.run(suite)
    fp.close()
    # runner = unittest.TextTestRunner()
    # runner.run(suite)




