import os
import re

import requests
from lxml import html
from selenium import webdriver

os.environ["webdriver.chrome.driver"] = "d:/py/chromedriver.exe"

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 "
)

dcap["phantomjs.page.settings.webSecurityEnabled"] = False
dcap["phantomjs.page.settings.loadImages"] = False
dcap["phantomjs.page.settings.diskCache"] = True
driver = webdriver.PhantomJS(executable_path="D:/py/phantomjs-2.1.1-windows/bin/phantomjs.exe",
                             desired_capabilities=dcap)


class Tool:
    def __init__(self, url, headers={}):
        resp = requests.get(url, headers)
        resp.encoding = 'utf8'
        text = resp.text.lower()
        text = re.sub(re.compile('&nbsp;'), '', text)
        text = re.sub(re.compile('<br><br>|<br>|<br\s?/>'), '', text)
        self.page = html.fromstring(text)
        self.text = text

    def xpath(self, path):
        return self.page.xpath(path)

    def xpathOne(self, path):
        doms = self.page.xpath(path)
        if len(doms) > 0:
            return doms[0]
        else:
            return None


class PhantomJSTool:
    def __init__(self, url):
        driver.get(url)
        self.text = driver.page_source
        self.driver = driver
        text = re.sub(re.compile('&nbsp;'), '', self.text)
        text = re.sub(re.compile('<br><br>|<br>|<br\s?/>'), '', text)
        self.page = html.fromstring(text)

    def getDriver(self):
        return self.driver

    def xpath(self, path):
        return self.page.xpath(path)

    def xpathOne(self, path):
        doms = self.page.xpath(path)
        if len(doms) > 0:
            return doms[0]
        else:
            return None

    def __str__(self):
        return self.text


class PicTool:
    def __init__(self, url, postdata, headers={}):
        s = requests.Session()
        r = s.post('http://m.1kkk.com/userdata.ashx', data=postdata)
        _cookies = r.cookies
        rs = s.get(url, headers=headers, cookies=_cookies)
        self.content = rs.content
