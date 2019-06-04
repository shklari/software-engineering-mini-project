from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import unittest


class UIauto(unittest.TestCase):
    def setUp(self):
        self.chrome_driver = webdriver.Chrome(r"..\Driver\chromedriver.exe")
        self.chrome_driver.get("http://www.google.com")

    def test_search_google(self):
        self.chrome_driver.find_element_by_name("q").send_keys("automation tests")
        self.chrome_driver.find_element_by_name("q").send_keys(Keys.ARROW_DOWN)
        self.chrome_driver.find_element_by_name("btnK").send_keys(Keys.ENTER)
        time.sleep(4)

    def tearDown(self):
        self.chrome_driver.quit()
        print("Test passed")


if __name__ == "__main__":
    unittest.main()
