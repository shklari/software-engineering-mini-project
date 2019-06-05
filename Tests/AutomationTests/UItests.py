import unittest
from selenium import webdriver
import time
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException as NSEE


class UItests(unittest.TestCase):

    chrome_driver = None

    def setUp(self):
        self.chrome_driver = webdriver.Chrome(r"..\Driver\chromedriver.exe")
        self.chrome_driver.get("http://127.0.0.1:8000/")
        time.sleep(5)

    def check_alert(self):
        wait = WebDriverWait(self.chrome_driver, 5)
        wait.until(EC.alert_is_present())
        alert = self.chrome_driver.switch_to.alert
        alert.accept()
        return True

    def dismiss_alert(self):
        wait = WebDriverWait(self.chrome_driver, 5)
        wait.until(EC.alert_is_present())
        alert = self.chrome_driver.switch_to.alert
        alert.accept()
        return False

    def test_all_buttons_appear(self):
        # checks if "SHOP" button appears
        self.assertTrue(self.chrome_driver.find_element_by_xpath("//body/div[@id='page']/nav[@class='fh5co-nav']/div[@c"
                                                                 "lass='container']/div[@class='row']/div[@class='col"
                                                                 "-md-6 col-xs-6 text-center menu-1']/ul/li[1]/a[1]"))
        # checks if "ABOUT" button appears
        self.assertTrue(self.chrome_driver.find_element_by_xpath("//div[@class='col-md-6 col-xs-6 text-center menu-1']"
                                                                 "//a[contains(text(),'About')]"))
        # checks if "SERVICES" button appears
        self.assertTrue(self.chrome_driver.find_element_by_xpath("//li[@class='has-dropdown']//a[contains(text(),"
                                                                 "'Services')]"))
        # checks if "CONTACT" button appears
        self.assertTrue(self.chrome_driver.find_element_by_xpath("//div[@class='col-md-6 col-xs-6 text-center menu-1']"
                                                                 "//a[contains(text(),'Contact')]"))
        time.sleep(2)
        self.chrome_driver.quit()

    def test_sign_up(self):
        self.chrome_driver.find_element_by_xpath("//div[@class='col-md-3 col-xs-4 text-right hidden-xs menu-2']//a["
                                                 "@id='signup']").click()
        self.chrome_driver.find_element_by_name("username").send_keys("shaioz")
        self.chrome_driver.find_element_by_name("psw").send_keys("1234")
        self.chrome_driver.find_element_by_name("psw-repeat").send_keys("1234")
        self.chrome_driver.find_element_by_name("age").send_keys("34")
        self.chrome_driver.find_element_by_name("country").send_keys("israel")
        self.chrome_driver.find_element_by_id("signupbtn").click()
        time.sleep(3)
        self.assertTrue(self.check_alert())
        time.sleep(3)
        self.chrome_driver.quit()

    def test_login_and_logout(self):
        self.chrome_driver.find_element_by_xpath("//div[@class='col-md-3 col-xs-4 text-right "
                                                 "hidden-xs menu-2']//a[@id='login']").click()
        self.chrome_driver.find_element_by_name("uname").send_keys("avabash")
        self.chrome_driver.find_element_by_name("psw").send_keys("123456")
        self.chrome_driver.find_element_by_id("loginbtn").click()
        time.sleep(3)
        self.assertTrue(self.check_alert())
        time.sleep(3)
        self.chrome_driver.find_element_by_xpath("//div[@class='col-md-3 col-xs-4 text-right hidden-xs menu-2']//a"
                                                 "[@id='logout']").click()
        time.sleep(3)
        self.assertTrue(self.check_alert())
        time.sleep(3)
        self.chrome_driver.quit()

    def test_bad_login(self):
        self.chrome_driver.find_element_by_xpath("//div[@class='col-md-3 col-xs-4 text-right "
                                                 "hidden-xs menu-2']//a[@id='login']").click()
        self.chrome_driver.find_element_by_name("uname").send_keys("shklark")
        self.chrome_driver.find_element_by_name("psw").send_keys("6666")
        self.chrome_driver.find_element_by_id("loginbtn").click()
        time.sleep(3)
        self.assertFalse(self.dismiss_alert())
        time.sleep(3)
        self.chrome_driver.quit()

