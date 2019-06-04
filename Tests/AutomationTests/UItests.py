from selenium import webdriver
import time
from selenium.webdriver.common.alert import Alert
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UIauto():
    def __init__(self):
        self.chrome_driver = webdriver.Chrome(r"..\Driver\chromedriver.exe")
        self.chrome_driver.get("http://127.0.0.1:8000/")
        time.sleep(3)
        self.bool = True

    def test_all_buttons_appear(self):
        # checks if "SHOP" button appears
        if not self.chrome_driver.find_element_by_xpath("//body/div[@id='page']/nav[@class='fh5co-nav']/div[@class='co"
                                                        "ntainer']/div[@class='row']/div[@class='col-md-6 col-xs-6 tex"
                                                        "t-center menu-1']/ul/li[1]/a[1]"):
            self.bool = False
        # checks if "ABOUT" button appears
        if not self.chrome_driver.find_element_by_xpath("//div[@class='col-md-6 col-xs-6 text-center menu-1']//a[conta"
                                                        "ins(text(),'About')]"):
            self.bool = False
        # checks if "SERVICES" button appears
        if not self.chrome_driver.find_element_by_xpath("//li[@class='has-dropdown']//a[contains(text(),'Services')]"):
            self.bool = False
        # checks if "CONTACT" button appears
        if not self.chrome_driver.find_element_by_xpath("//div[@class='col-md-6 col-xs-6 text-center menu-1']//a[contai"
                                                        "ns(text(),'Contact')]"):
            self.bool = False
        time.sleep(2)

    def test_sign_up(self):
        self.chrome_driver.find_element_by_xpath("//div[@class='col-md-3 col-xs-4 text-right hidden-xs menu-2']//a["
                                                 "@id='signup']").click()
        self.chrome_driver.find_element_by_name("username").send_keys("inbar")
        self.chrome_driver.find_element_by_name("psw").send_keys("1234")
        self.chrome_driver.find_element_by_name("psw-repeat").send_keys("1234")
        self.chrome_driver.find_element_by_id("signupbtn").click()
        self.check_alert()
        time.sleep(3)

    def check_alert(self):
        wait = WebDriverWait(self.chrome_driver, 5)
        wait.until(EC.alert_is_present())
        alert = self.chrome_driver.switch_to.alert
        alert.accept()

    def test_login(self):
        self.chrome_driver.find_element_by_xpath("//div[@class='col-md-3 col-xs-4 text-right "
                                                 "hidden-xs menu-2']//a[@id='login']").click()
        self.chrome_driver.find_element_by_name("uname").send_keys("avabash")
        self.chrome_driver.find_element_by_name("psw").send_keys("123456")
        self.chrome_driver.find_element_by_id("loginbtn").click()
        self.check_alert()
        time.sleep(3)

    def tear_down(self):
        self.chrome_driver.quit()
        print("Test passed") if self.bool else print("Test failed")


if __name__ == "__main__":
    auto = UIauto()
    auto.test_all_buttons_appear()
    auto.test_sign_up()
    auto.test_login()
    auto.tear_down()

