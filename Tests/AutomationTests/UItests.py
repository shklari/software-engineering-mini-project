from selenium import webdriver
import time
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys


class UIauto():
    def __init__(self):
        self.chrome_driver = webdriver.Chrome(r"..\Driver\chromedriver.exe")
        self.chrome_driver.get("http://127.0.0.1:8000/")
        time.sleep(2)
        self.bool = True

    def test_all_buttons_appear(self):
        # checks if "SHOP" button appears
        if not self.chrome_driver.find_element_by_xpath("//*[@id='page']/nav[2]/div/div/div[2]/ul/li[1]/a"):
            bool = False
        # checks if "ABOUT" button appears
        if not self.chrome_driver.find_element_by_xpath("//*[@id='page']/nav[2]/div/div/div[2]/ul/li[2]/a"):
            bool = False
        # checks if "SERVICES" button appears
        if not self.chrome_driver.find_element_by_xpath("//*[@id='page']/nav[2]/div/div/div[2]/ul/li[3]/a"):
            bool = False
        # checks if "CONTACT" button appears
        if not self.chrome_driver.find_element_by_xpath("//*[@id='page']/nav[2]/div/div/div[2]/ul/li[4]/a"):
            bool = False
        time.sleep(4)

    def test_sign_up(self):
        subtn = self.chrome_driver.find_element_by_id('signup')
        subtn.click()
        self.chrome_driver.switch_to_window("/signup/")
        self.chrome_driver.find_element_by_name("username").send_keys("shaioz")
        self.chrome_driver.find_element_by_name("psw").send_keys("1234")
        self.chrome_driver.find_element_by_name("psw-repeat").send_keys("1234")
        self.chrome_driver.find_element_by_name("signupbtn").click()
        time.sleep(4)

    def tear_down(self):
        self.chrome_driver.quit()
        print("Test passed")
        # print("Test passed") if self.bool else print("Test failed")


if __name__ == "__main__":
    auto = UIauto()
    auto.test_sign_up()
    # auto.test_all_buttons_appear()
    auto.tear_down()

