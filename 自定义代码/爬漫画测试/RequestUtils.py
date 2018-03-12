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
driver = webdriver.PhantomJS(executable_path="D:/py/phantomjs-2.1.1-windows/bin/phantomjs.exe", desired_capabilities=dcap)


# 反爬措施
header = {
    'Host': 'www.xxshu5.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Anit-Forge-Token': 'None',
    'X-Anit-Forge-Code': '0',
    'Content-Length': '26',
    'Cookie': 'td_cookie=436545905; __cfduid=d439c73366354256788f81f67c81801bd1520424100; PHPSESSID=nqbhl0eifqa1osug9obi2flfnt; td_cookie=436456820; UM_distinctid=1620056abd36a2-0ea2942ef9b8ce-4a541326-1fa400-1620056abd4733; CNZZDATA1261503339=2145269000-1520420756-null%7C1520420756',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Referer': 'http://www.1kkk.com/ch129-583070/'
}

img_header = {
    'Host': 'manhua1032-61-174-50-98.cdndm5.com',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Referer': 'http://www.1kkk.com/ch129-583070/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',

    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Anit-Forge-Token': 'None',
    'X-Anit-Forge-Code': '0',
    'Content-Length': '26',
}


class Tool:
    def __init__(self, url, headers={}):
        resp = requests.get(url, headers)
        resp.encoding = 'utf8'
        text = resp.text.lower()
        text = re.sub(re.compile('&nbsp;'), '', text)
        text = re.sub(re.compile('<br><br>|<br>|<br\s?/>'), '', text)
        self.page = html.fromstring(text)

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
