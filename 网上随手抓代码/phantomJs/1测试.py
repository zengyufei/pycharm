from selenium import webdriver
import os
os.environ["webdriver.chrome.driver"] = "d:/py/chromedriver.exe"

driver = webdriver.PhantomJS(executable_path="D:/py/phantomjs-2.1.1-windows/bin/phantomjs.exe")
driver.get("http://www.baidu.com")
data = driver.title
print (data)