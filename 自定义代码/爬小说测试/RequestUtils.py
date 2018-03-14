import re

import requests
from lxml import html

# 反爬措施
header = {
    'Host': 'www.xxshu5.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'Upgrade-Insecure-Requests': 1,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://www.xxshu5.com/mushenji/',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Anit-Forge-Token': 'None',
    'X-Anit-Forge-Code': '0',
    'Content-Length': '26',
    'Cookie': 'td_cookie=436545905; __cfduid=d439c73366354256788f81f67c81801bd1520424100; PHPSESSID=nqbhl0eifqa1osug9obi2flfnt; td_cookie=436456820; UM_distinctid=1620056abd36a2-0ea2942ef9b8ce-4a541326-1fa400-1620056abd4733; CNZZDATA1261503339=2145269000-1520420756-null%7C1520420756',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}


class Tool:
    def __init__(self, url, headers={}):
        resp = requests.get(url, headers)
        resp.encoding = 'utf8'
        text = re.sub(re.compile(r'&gt;(&gt;)+'), ' ', resp.text)
        text = re.sub(re.compile(r'&lt;(&lt;)+'), ' ', text)
        text = re.sub(re.compile(r'<<+'), ' ', text)
        text = re.sub(re.compile(r'>>+'), ' ', text)
        text = re.sub(re.compile('&nbsp;'), ' ', text)
        text = re.sub(re.compile('<br><br>|<br>|<br\s?/>'), '\n', text)
        self.page = html.fromstring(text)

    def xpath(self, path):
        return self.page.xpath(path)

    def xpathOne(self, path):
        doms = self.page.xpath(path)
        if len(doms) == 1:
            return doms[0]
        else:
            return None
