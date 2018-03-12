from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
#直接将下载的 chromedriver.exe 路径加到
#driver = webdriver.Chrome(r"E:\Tools\Python\seleniumDriver\chromedriver.exe")
#或者直接改变环境变量
#import os
#os.environ["webdriver.chrome.driver"] = "E:\Tools\Python\seleniumDriver\chromedriver.exe"


url = 'http://www.baidu.com/'
browser = webdriver.Chrome()
browser.get(url)
browser.implicitly_wait(2) # seconds
element = browser.find_element_by_id("kw")
browser.implicitly_wait(1) # seconds
element.send_keys("and some", Keys.ENTER)
#element.clear()
time.sleep(5)
browser.quit()