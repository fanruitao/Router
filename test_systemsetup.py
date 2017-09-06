from  selenium  import webdriver
import HTMLTestRunner
from selenium.webdriver.support.ui import Select
import unittest
import time
from  xml.dom.minidom  import parse
from public.logIn import login
from  selenium.webdriver.common.by import By
import selenium.common.exceptions as e
from  selenium.webdriver.support.ui import WebDriverWait
from  selenium.webdriver.support import  expected_conditions as EC
import traceback
from util.logger import L
import subprocess

dom=parse("./public/config.xml")
root=dom.documentElement
setup=root.getElementsByTagName("setup")
class TestSetup(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.baseurl = root.getElementsByTagName("setup")[0].getAttribute("baseurl")
        self.currpassword=setup[0].getElementsByTagName("modifypassword")[0].getAttribute("currpassword")
        self.newpassword=setup[0].getElementsByTagName("modifypassword")[0].getAttribute("newpassword")
        self.uploadpng=setup[0].getElementsByTagName("updatefw")[0].getAttribute("uploadpng")
    def test_nopassword(self):

        """不输入原密码时，直接点击保存，提示信息检查"""
        L.info("test_nopassword START:不输入原来的登录密码时，提示语检查")
        driver=self.driver
        print("caseid:015")
        driver.get(self.baseurl)
        login(driver)
        driver.implicitly_wait(30)
        driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
        time.sleep(1)

        driver.find_element_by_id("ic_systemSetup").click()
        time.sleep(3)
        driver.find_element_by_xpath("//li[@id='liaccount']/a").click()
        driver.find_element_by_id("savebutton5").click()
        try:
            if (driver.find_element_by_id("errorinfo_1").is_displayed()):
                errorinfo=driver.find_element_by_id("errorinfo_1").text
                self.assertEqual(errorinfo,"原登录密码不能为空，请重新输入。")
        except e.NoSuchElementException:
            L.error(traceback.format_exc())
        L.info("test_nopassword STOP")
    def test_nonewpassword(self):
        """不填入新密码时的提示语检查"""
        L.info("test_nonewpassword START:不填入新密码时的提示语检查")
        driver = self.driver
        print("caseid:016")
        currpassword=self.currpassword
        newpassword=self.newpassword
        driver.get(self.baseurl)
        login(driver)
        driver.implicitly_wait(30)
        driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
        time.sleep(1)
        driver.find_element_by_id("ic_systemSetup").click()
        time.sleep(3)
        driver.find_element_by_xpath("//li[@id='liaccount']/a").click()
        driver.find_element_by_id("current_password").send_keys(currpassword)
        driver.find_element_by_id("savebutton5").click()
        try:
            if (driver.find_element_by_id("errorinfo_2").is_displayed()):
                errorinfo = driver.find_element_by_id("errorinfo_2").text
                self.assertEqual(errorinfo, "请输入新密码。")
        except e.NoSuchElementException:
            L.error(traceback.format_exc())
        L.info("test_nonewpassword STOP")
    def test_noconfirmpassword(self):
        """确认密码不填写时的提示信息检查"""

        L.info("test_noconfirmpassword START:确认密码不填写时的提示信息检查")
        driver = self.driver
        print("caseid:017")
        currpassword = self.currpassword
        newpassword = self.newpassword
        driver.get(self.baseurl)
        login(driver)
        driver.implicitly_wait(30)
        driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
        time.sleep(1)
        driver.find_element_by_id("ic_systemSetup").click()
        time.sleep(3)
        driver.find_element_by_xpath("//li[@id='liaccount']/a").click()
        driver.find_element_by_id("current_password").send_keys(currpassword)
        driver.find_element_by_id("new_password").send_keys(newpassword)
        time.sleep(5)
        driver.find_element_by_id("savebutton5").click()
        try:
            if (driver.find_element_by_id("errorinfo_3").is_displayed()):
                errorinfo = driver.find_element_by_id("errorinfo_3").text
                self.assertEqual(errorinfo, "请输入确认密码。")
        except e.NoSuchElementException:
            L.info(traceback.format_exc())
        L.info("test_noconfirmpassword STOP")
    def test_confirmpswdwrror(self):
        """确认密码和新密码不一致时的提示信息检查"""
        L.info("test_confirmpswdwrror START:确认密码和新密码不一致时的提示信息检查")
        driver = self.driver
        print("caseid:018")
        currpassword = self.currpassword
        newpassword = self.newpassword
        driver.get(self.baseurl)
        login(driver)
        driver.implicitly_wait(30)
        driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
        time.sleep(1)
        driver.find_element_by_id("ic_systemSetup").click()
        time.sleep(3)
        driver.find_element_by_xpath("//li[@id='liaccount']/a").click()
        driver.find_element_by_id("current_password").send_keys(currpassword)
        driver.find_element_by_id("new_password").send_keys(newpassword)
        driver.find_element_by_id("confirm_password").send_keys("1")
        time.sleep(3)
        driver.find_element_by_id("savebutton5").click()
        try:
            if (driver.find_element_by_id("errorinfo_3").is_displayed()):
                errorinfo = driver.find_element_by_id("errorinfo_3").text
                self.assertEqual(errorinfo, "新登录密码和确认密码不一致，请重新输入。")
        except e.NoSuchElementException:
            L.error(traceback.format_exc())

        L.info("test_confirmpswdwrror STOP")
    def test_crrentpswderror(self):
        """原密码错误时的提示语检查"""
        L.info("test_crrentpswderror START:原密码错误时的提示语检查")
        driver = self.driver
        print("caseid:019")
        currpassword = self.currpassword
        newpassword = self.newpassword
        driver.get(self.baseurl)
        login(driver)
        driver.implicitly_wait(30)
        driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
        time.sleep(1)
        driver.find_element_by_id("ic_systemSetup").click()
        time.sleep(3)
        driver.find_element_by_xpath("//li[@id='liaccount']/a").click()
        driver.find_element_by_id("current_password").send_keys("1")
        driver.find_element_by_id("new_password").send_keys(newpassword)
        driver.find_element_by_id("confirm_password").send_keys(newpassword)
        time.sleep(3)
        driver.find_element_by_id("savebutton5").click()
        try:
            if (driver.find_element_by_id("errorinfo_1").is_displayed()):
                errorinfo = driver.find_element_by_id("errorinfo_1").text
                self.assertEqual(errorinfo, "原登录密码错误，请重新输入。")
        except e.NoSuchElementException:
            L.error(traceback.format_exc())
        L.info("test_crrentpswderror STOP")
    def test_newpassworderror(self):
        """新密码格式错误时的，提示信息检查"""
        L.info("newpassworderror START:新密码格式错误时的，提示信息检查")
        driver = self.driver
        print("caseid:020")
        currpassword = self.currpassword
        driver.get(self.baseurl)
        login(driver)
        driver.implicitly_wait(30)
        driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
        time.sleep(1)
        driver.find_element_by_id("ic_systemSetup").click()
        time.sleep(3)
        driver.find_element_by_xpath("//li[@id='liaccount']/a").click()
        driver.find_element_by_id("current_password").send_keys(currpassword)
        driver.find_element_by_id("new_password").send_keys("123")
        time.sleep(3)
        driver.find_element_by_id("savebutton5").click()
        try:
            if (driver.find_element_by_id("errorinfo_2").is_displayed()):
                errorinfo = driver.find_element_by_id("errorinfo_2").text
                self.assertEqual(errorinfo, "新密码长度不正确，请输入8至63个字符。")
        except e.NoSuchElementException:
            L.error(traceback.format_exc())
        L.info("newpassworderror START")

    def test_setpasswordright(self):
        """原密码错误时提示信息检查"""
        L.info("test_crrentpswderror START:原密码错误时的提示语检查")
        driver = self.driver
        print("caseid:021")
        currpassword = self.currpassword
        newpassword = self.newpassword
        driver.get(self.baseurl)
        login(driver)
        driver.implicitly_wait(30)
        driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
        time.sleep(1)
        driver.find_element_by_id("ic_systemSetup").click()
        time.sleep(3)
        driver.find_element_by_xpath("//li[@id='liaccount']/a").click()
        driver.find_element_by_id("current_password").send_keys(currpassword)
        driver.find_element_by_id("new_password").send_keys(newpassword)
        driver.find_element_by_id("confirm_password").send_keys(newpassword)
        time.sleep(3)
        driver.find_element_by_id("savebutton5").click()
        time.sleep(20)
        driver.find_element_by_id("admin_Password1").send_keys(newpassword)
        driver.find_element_by_id("logIn_btn").click()
        time.sleep(5)
        self.assertEqual("http://192.168.0.1/Home.html",driver.current_url)
        #再次改回原密码：
        driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
        time.sleep(1)
        driver.find_element_by_id("ic_systemSetup").click()
        time.sleep(3)
        driver.find_element_by_xpath("//li[@id='liaccount']/a").click()
        driver.find_element_by_id("current_password").send_keys(newpassword)
        driver.find_element_by_id("new_password").send_keys(currpassword)
        driver.find_element_by_id("confirm_password").send_keys(currpassword)
        time.sleep(3)
        driver.find_element_by_id("savebutton5").click()
        time.sleep(20)



    def test_timezone(self):

        """切换时区后的检查"""
        L.info("test_time START:切换时区后的检查")
        driver = self.driver
        print("caseid:022")
        driver.get(self.baseurl)
        login(driver)
        driver.implicitly_wait(30)
        driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
        time.sleep(1)
        driver.find_element_by_id("ic_systemSetup").click()
        time.sleep(3)
        driver.find_element_by_id("lang_time").click()
        select=Select(driver.find_element_by_id("select_zone"))
        time.sleep(2)
        js = 'document.querySelectorAll("select")[0].style.display="block";'
        driver.execute_script(js)
        select.select_by_value("CST+7")
        driver.find_element_by_id("savebutton5").click()

        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located((By.ID, "CreateOnloadMessage"))
        )
        time.sleep(3)
        selecttext=driver.find_element_by_class_name('sbSelector').text
        self.assertEqual(selecttext,"CST+7 (MST-北美山区标准时间)")
        #测试完毕，恢复到正确时区
        select1 = Select(driver.find_element_by_id("select_zone"))
        time.sleep(2)
        js = 'document.querySelectorAll("select")[0].style.display="block";'
        driver.execute_script(js)
        time.sleep(2)
        select1.select_by_value("CST-8")
        time.sleep(2)
        driver.find_element_by_id("savebutton5").click()
        time.sleep(2)
        WebDriverWait(driver, 30).until(
            EC.invisibility_of_element_located((By.ID, "CreateOnloadMessage"))
        )
        self.assertEqual(driver.find_element_by_class_name('sbSelector').text,"CST-8 (EAT-北京，重庆，香港特别行政区，乌鲁木齐)")
        L.info("test_time STOP")
    def test_firwareupdate(self):
        """固件格式错误时提示信息检查"""
        L.info("test_firwareupdate START:固件格式错误时提示信息检查")
        #固件格式错误时提示信息检查，由于目前没有正确的固件，固件升级中暂时只做一个用例，后续完善
        driver = self.driver
        print("caseid:023")
        uploadpng=self.uploadpng
        driver.get(self.baseurl)
        login(driver)
        driver.implicitly_wait(2)
        driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
        time.sleep(1)
        driver.find_element_by_id("ic_systemSetup").click()
        time.sleep(3)
        driver.find_element_by_id("lang_upgrade").click()
        time.sleep(5)
        driver.find_element_by_css_selector('label.styled_button_s').click()
        time.sleep(5)
        cmd="./upgrade/upload.exe"+" "+uploadpng
        print(cmd)

        #调用autoit脚本选择文件
        L.info("开始用autoit3脚本控制选择本地文件")
        ps = subprocess.Popen(cmd)
        ps.wait()
        time.sleep(10)
        try:
            driver.find_element_by_id("btn_begin_upload").click()

            if (driver.find_element_by_id("errorinfo_update").is_displayed()):
                errorinfo = driver.find_element_by_id("errorinfo_update").text
                self.assertEqual(errorinfo, "文件类型错误，应选择*.bin或*.img。")
        except e.ElementNotVisibleException:
            L.error(traceback.format_exc())
        L.info("test_firwareupdate STOP")
    def test_reboot(self):
        """重启功能检查，重启后，进入登录页"""
        L.info("test_reboot START:重启功能检查")
        driver = self.driver
        print("caseid:024")
        uploadpng = self.uploadpng
        driver.get(self.baseurl)
        login(driver)
        driver.implicitly_wait(3)
        try:
            driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
            time.sleep(1)
            driver.find_element_by_id("ic_systemSetup").click()
            time.sleep(2)
            driver.find_element_by_id("lang_reboot").click()
            time.sleep(5)
            driver.find_element_by_id("btn_reboot_router").click()
        except e.NoSuchElementException:
            L.error(traceback.format_exc())
        try:
            driver.find_element_by_id("btn_reboot_confirm").click()
            WebDriverWait(driver, 120).until(
                EC.invisibility_of_element_located((By.ID, "DeviceRebooting"))
            )
            time.sleep(3)
            self.assertEqual(driver.current_url,"http://192.168.0.1/Login.html")
        except e.NoSuchElementException:
            L.error(traceback.format_exc())
        L.info("test_reboot STOP")
    def test_cancelreboot(self):
        """点击重启路由器后，点击取消"""
        L.info(" test_cancelreboot START:点击重启路由器后，点击取消，确认可以成功取消")
        driver = self.driver
        print("caseid:025")
        driver.get(self.baseurl)
        #登录系统
        login(driver)
        #进入无线名称页面将无线名称修改为frt_test
        time.sleep(2)
        try:
            driver.find_element_by_id("wirless").click()
            driver.find_element_by_id('wifiName_24').clear()
            driver.find_element_by_id('wifiName_24').send_keys("frt_test")
            time.sleep(5)
            driver.find_element_by_xpath("//input[@id='savebutton']").click()
        except e.InvalidElementStateException:
            L.error(traceback.format_exc())

        time.sleep(5)
        result=True
        try:
            driver.find_element_by_id("saveconfirm2_5G").click()
            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.ID, "CreatePopAlertMessage"))
            )
            """js = "document.getElementById('wifiName_24').value;"
            t = driver.execute_script(js)

            if t!="frt_test":
                L.info("无线wifi名称未保存成功,测试终止")
                result=False
                self.assertTrue(True,result)

            else:"""
            driver.find_element_by_xpath("//div[@id='want_more_id']/div").click()
            time.sleep(1)
            driver.find_element_by_id("ic_systemSetup").click()
            time.sleep(2)
            driver.find_element_by_id("lang_reboot").click()
            time.sleep(2)
            driver.find_element_by_id("btn_reboot_router").click()
            time.sleep(2)
            driver.find_element_by_id("btn_reboot_cancel").click()
        except e.ElementNotVisibleException:
            L.error(traceback.format_exc())
        L.info("test_cancelreboot STOP")
    def test_logout(self):
        """退出功能测试"""
        L.info(" test_logout START:测试退出功能")
        loginurl=self.baseurl
        driver = self.driver
        print("caseid:026")
        driver.get(self.baseurl)
        # 登录系统
        login(driver)
        try:
            time.sleep(2)
            driver.find_element_by_id("logoutword").click()
            time.sleep(2)
        except e.ElementNotVisibleException:
            L.error(traceback.format_exc())
        current_url=driver.current_url
        self.assertEqual(current_url,loginurl+"/Login.html")
        L.info("test_logout STOP")

    def tearDown(self):
        self.driver.close()
if __name__ == "__main__":
    suite=unittest.TestSuite()
    # suite.addTest(TestSetup('test_nopassword'))
    # suite.addTest(TestSetup('test_nonewpassword'))
    # suite.addTest(TestSetup('test_noconfirmpassword'))
    # suite.addTest(TestSetup('test_confirmpswdwrror'))
    # suite.addTest(TestSetup('test_crrentpswderror'))
    # suite.addTest(TestSetup('test_newpassworderror'))
    # suite.addTest(TestSetup('test_timezone'))
    # suite.addTest(TestSetup('test_firwareupdate'))
    suite.addTest(TestSetup('test_reboot'))
    # suite.addTest(TestSetup('test_cancelreboot'))
    # suite.addTest(TestSetup('test_logout'))

    now = time.strftime("%Y-%m-%d %H_%M_%S")

    filename = r'./result/' + now + '_result.html'
    fp =open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"墙壁式无线wifi测试", description=u"用例执行情况:")
    runner.run(suite)
    fp.close()
    # runner = unittest.TextTestRunner()
    # runner.run(suite)