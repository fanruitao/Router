#coding=utf-8
import unittest
import HTMLTestRunner
import time
from util.logger import L
from  xml.dom.minidom  import parse
from util import sendemail


test_dir = "./"


testlist = unittest.defaultTestLoader.discover(test_dir, "test*.py", top_level_dir=None)

if __name__ == "__main__":
    L.info('test start')

    nowtime = time.strftime("%Y-%m-%d %H_%M_%S")

    filename = r'./result/' + nowtime + '_result.html'
    fp =open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"墙壁式无线wifi测试", description=u"用例执行情况:")
    runner.run(testlist)
    #是否发邮件
    dom = parse("./public/config.xml")
    root = dom.documentElement
    ifsendmail = root.getElementsByTagName("emailaddress")[0].getAttribute("ifsendmail")
    if ifsendmail=='True':
        L.info("发送邮件")
        sendemail.send_mail(filename)
    else:
        L.info("不发送邮件")
    fp.close()