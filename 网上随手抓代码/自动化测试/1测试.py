from selenium import webdriver
import time
#直接将下载的 chromedriver.exe 路径加到
#driver = webdriver.Chrome(r"E:\Tools\Python\seleniumDriver\chromedriver.exe")
#或者直接改变环境变量
#import os
#os.environ["webdriver.chrome.driver"] = "E:\Tools\Python\seleniumDriver\chromedriver.exe"


url = 'http://www.baidu.com/'
browser = webdriver.Chrome()
browser.get(url)
print(browser.title)
time.sleep(5)
browser.quit()