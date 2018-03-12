from selenium import webdriver
import os
from lxml import html
import re
os.environ["webdriver.chrome.driver"] = "d:/py/chromedriver.exe"

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 "
)

dcap["phantomjs.page.settings.webSecurityEnabled"] = False
dcap["phantomjs.page.settings.loadImages"] = False
dcap["phantomjs.page.settings.diskCache"] = True
driver = webdriver.PhantomJS(executable_path="D:/py/phantomjs-2.1.1-windows/bin/phantomjs.exe", desired_capabilities=dcap)

driver.get("http://www.1kkk.com/ch129-583070/")
data = driver.page_source # 获取整个页面的内容
text = re.sub(re.compile('&nbsp;'), '', data)
text = re.sub(re.compile('<br><br>|<br>|<br\s?/>'), '', text)
page = html.fromstring(text)
content_img_xpath = '//*[@id="cp_image"]'
imgs = page.xpath(content_img_xpath)
for img in imgs:
    print(img.get("src"))
driver.quit()