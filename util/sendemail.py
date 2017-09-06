from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

from  xml.dom.minidom  import parse
import smtplib

def send_email_address():
    dom = parse("./public/config.xml")
    root=dom.documentElement
    #从config 文件中读取，发送地址和接受地址
    send_email=root.getElementsByTagName("emailaddress")[0].getAttribute("sendaddress")
    receiver_email=root.getElementsByTagName("emailaddress")[0].getAttribute("receiveaddress")
    return send_email,receiver_email

def send_mail(report):
    #测试报告会以html的形式显示在邮件中，并且会作为附件附带到邮件里
    #print(open('./result/2017-08-29 16_18_59_result.html', 'rb+').read())
    f=open(report,'rb+')
    mailbody=f.read()
    f.close()
    #构建带有附件的邮件
    msg=MIMEMultipart()
    sendmail=send_email_address()[0]
    msg['From']=sendmail
    receivegroup=send_email_address()[1].split(',')
    msg['To']=','.join(receivegroup)
    msg['Subject']=Header('墙壁wifi自动化测试报告','utf-8')
    #编写html 类型的邮件正文
    html=MIMEText(mailbody,'html','utf-8')
    msg.attach(html)
    #增加附件
    att = MIMEText(open(report, 'rb').read(), 'html', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename=testreport.html"'
    msg.attach(att)

    smtpsever='mail.gongniu.cn'
    username='fanrt@gongniu.cn'
    password='ZAQ!2wsx'
    server= smtplib.SMTP()
    server.connect(smtpsever)
    server.login(username, password)
    server.sendmail(sendmail, receivegroup, msg.as_string())
    server.quit()












