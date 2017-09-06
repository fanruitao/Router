
import time
from  xml.dom.minidom  import parse
def  login(driver):
    dom = parse("./public/config.xml")
    root = dom.documentElement
    logintag = root.getElementsByTagName('login')
    password = logintag[0].getAttribute('rightpassword')
    time.sleep(2)
    driver.find_element_by_id("admin_Password1").send_keys(password)
    driver.find_element_by_id("logIn_btn").click()
