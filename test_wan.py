
from  selenium  import webdriver
from selenium.webdriver.support.ui import Select
import unittest
import time
import HTMLTestRunner
from  xml.dom.minidom  import parse
from util.logger import L
from selenium.common.exceptions import NoSuchElementException

from public.logIn import login
dom=parse("./public/config.xml")
root=dom.documentElement


class TestWan (unittest.TestCase):
    def setUp(self):
        wantag=root.getElementsByTagName('wan')
        self.baseurl=wantag[0].getAttribute("baseurl")
        #self.ipaddress=wantag[0][0].getAttribute("ipaddress")
        print (wantag[0])
        self.ipaddress = wantag[0].getElementsByTagName("static")[0].getAttribute("ipaddress")
        self.mask = wantag[0].getElementsByTagName("static")[0].getAttribute("mask")
        self.gateway = wantag[0].getElementsByTagName("static")[0].getAttribute("gateway")
        self.dns1=wantag[0].getElementsByTagName("static")[0].getAttribute("dns1")
        print (self.ipaddress)
        self.driver = webdriver.Chrome()
    def test_gotowan(self):
        """能否正确跳转"""
        L.info("test_gotowan START:测试能否正确跳转到互联网设置页面")
        driver = self.driver
        print("caseid:027")
        driver.get(self.baseurl)
        login(driver)
        driver.implicitly_wait(30)
        driver.find_element_by_xpath("//div[@id='want_internet_id']/div/span").click()
        self.assertEqual(driver.current_url,"http://192.168.0.1/Network.html")
        L.info("test_gotowan STOP")
    def test_noip(self):
        """不填入IP地址"""
        L.info("test_noip START:不输入IP地址，提示语检查")
        driver = self.driver
        print("caseid:028")
        driver.get(self.baseurl)
        login(driver)
        driver.implicitly_wait(30)
        driver.find_element_by_xpath("//div[@id='want_internet_id']/div/span").click()
        time.sleep(5)
        js='document.querySelectorAll("select")[0].style.display="block";'
        driver.execute_script(js)

        select=Select(driver.find_element_by_name('select_networktype'))
        select.select_by_value('Static')
        driver.find_element_by_id("savebutton").click()
        self.assertEqual(driver.find_element_by_id("errorinfo_4").text,"请输入IP地址。")
        L.info("test_noip STOP")
    def test_wrongip(self):
        """输入错误格式的ip 地址提示信息检查"""
        L.info("test_wrongip START:输入错误格式的ip 地址提示信息检查")
        driver = self.driver
        print("caseid:029")
        result=0

        driver.get(self.baseurl)
        login(driver)
        driver.implicitly_wait(30)
        driver.find_element_by_xpath("//div[@id='want_internet_id']/div/span").click()
        time.sleep(5)
        js='document.querySelectorAll("select")[0].style.display="block";'
        driver.execute_script(js)

        select=Select(driver.find_element_by_name('select_networktype'))
        select.select_by_value('Static')
        wrongip=['192.168.www.4','192.!23.tt.com','192.168.%$.#','1 92.168.  34','192.168.344.2','192.-168.3.2']
        for ip in wrongip:

            driver.find_element_by_id('staticIpaddr').send_keys(ip)
            driver.find_element_by_id("savebutton").click()
            try:
                driver.find_element_by_id("errorinfo_4")
            except NoSuchElementException as msg:
                L.info(msg)
            else:
                if driver.find_element_by_id("errorinfo_4").text=="IP地址含非法字符，请重新输入。":
                    result+=1
        self.assertEqual(len(wrongip),result)
        L.info("test_wrongip START")
    def test_nomask(self):
        """不输入子网掩码的提示信息检查"""
        L.info("test_nomask START:不输入子网掩码的提示信息检查")
        driver = self.driver
        print("caseid:030")
        ip=self.ipaddress
        driver.get(self.baseurl)
        login(driver)
        driver.implicitly_wait(30)
        driver.find_element_by_xpath("//div[@id='want_internet_id']/div/span").click()
        time.sleep(5)
        js = 'document.querySelectorAll("select")[0].style.display="block";'
        driver.execute_script(js)

        select = Select(driver.find_element_by_name('select_networktype'))
        select.select_by_value('Static')
        driver.find_element_by_id('staticIpaddr').send_keys(ip)
        driver.find_element_by_id("savebutton").click()
        try:
            element=driver.find_element_by_id('errorinfo_5')
        except NoSuchElementException as msg:
            L.info("没有找到元素："+msg)
        else:
            self.assertEqual('请输入子网掩码。',element.text)
        L.info("test_nomask STOP")
    def test_nogateway(self):
        """不输入默认网关时的提示信息检查"""
        L.info("test_nogateway START:不输入默认网关时的提示信息检查")
        driver = self.driver
        print("caseid:031")
        ip = self.ipaddress
        mask=self.mask
        driver.get(self.baseurl)
        login(driver)
        driver.implicitly_wait(30)
        driver.find_element_by_xpath("//div[@id='want_internet_id']/div/span").click()
        time.sleep(5)
        js = 'document.querySelectorAll("select")[0].style.display="block";'
        driver.execute_script(js)

        select = Select(driver.find_element_by_name('select_networktype'))
        select.select_by_value('Static')
        driver.find_element_by_id('staticIpaddr').send_keys(ip)
        driver.find_element_by_id('staticmask').send_keys(mask)
        driver.find_element_by_id("savebutton").click()
        try:
            element = driver.find_element_by_id('errorinfo_6')
        except NoSuchElementException as msg:
            L.info("没有找到元素：" + msg)
        else:
            self.assertEqual('请输入默认网关地址。', element.text)
        L.info("test_nogateway STOP")
    def test_wrongmask(self):
        """输入错误的子网掩码时的提示信息检查"""
        print("caseid:032")
        pass
    def test_wronggateway(self):
        """输入错误的默认网关时提示信息检查"""
        print("caseid:033")
        pass
    def test_setwanmethod(self):
        """输入正确的wan 设置参数时能否成功保存检查"""
        L.info("test_setwanmethod START:输入正确的wan 设置参数时能否成功保存检查")

        driver = self.driver
        print("caseid:034")
        ipadress=self.ipaddress
        mask=self.mask
        gateway=self.gateway
        dns1=self.dns1
        driver.get(self.baseurl)
        login(driver)
        driver.implicitly_wait(30)
        driver.find_element_by_xpath("//div[@id='want_internet_id']/div/span").click()
        time.sleep(5)
        #此下拉框不可见所以要调js ，改成可见
        js='document.querySelectorAll("select")[0].style.display="block";'
        driver.execute_script(js)

        select=Select(driver.find_element_by_name('select_networktype'))
        select.select_by_value('Static')
        driver.find_element_by_id('staticIpaddr').send_keys(ipadress)
        driver.find_element_by_id('staticmask').send_keys(mask)
        driver.find_element_by_id('staticgateway').send_keys(gateway)
        driver.find_element_by_id('staticdns1').send_keys(dns1)
        driver.find_element_by_id("savebutton").click()
        time.sleep(10)
        self.assertEqual("手动输入IP(静态IP)",driver.find_element_by_id("networktypeinfo").text)
        L.info("修改完成后恢复到自动获取dhcp")
        js = 'document.querySelectorAll("select")[0].style.display="block";'
        driver.execute_script(js)
        select = Select(driver.find_element_by_name('select_networktype'))
        select.select_by_value('DHCP')
        driver.find_element_by_id("savebutton").click()
        time.sleep(10)
        L.info("test_setwanmethod STOP")
    def tearDown(self):
        #select = Select(self.driver.find_element_by_name('select_networktype'))
        #select.select_by_value('DHCP')
        self.driver.close()


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestWan('test_gotowan'))
    suite.addTest(TestWan('test_noip'))
    suite.addTest(TestWan('test_wrongip'))
    suite.addTest(TestWan('test_nomask'))
    suite.addTest(TestWan('test_nogateway'))
    suite.addTest(TestWan('test_wrongmask'))
    suite.addTest(TestWan('test_wronggateway'))
    suite.addTest(TestWan('test_setwanmethod'))
    now = time.strftime("%Y-%m-%d %H_%M_%S")

    filename = r'./result/' + now + '_result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"墙壁式无线wifi测试", description=u"用例执行情况:")
    runner.run(suite)
    fp.close()
    # runner = unittest.TextTestRunner()
    # runner.run(suite)



