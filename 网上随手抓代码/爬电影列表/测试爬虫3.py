# -*- coding:utf-8 -*-
#####################
#  获取电影列表
#####################
import datetime

import pymysql
import requests
import re
from lxml import html

user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
headers = {'User-Agent': user_agent}

class Tool:
    # 将多余的 \ 剔除
    removeXieGang = re.compile('\\$')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')

    def __init__(self, url, headers):
        resp = requests.get(url, headers)
        resp.encoding = 'gbk'
        text = resp.text
        text = re.sub(self.removeXieGang, "", text)
        text = re.sub(self.replaceBR, "\n", text)
        self.page = html.fromstring(text)

    def xpath(self, path):
        return self.page.xpath(path)

    def xpathOne(self, path):
        content = self.page.xpath(path)
        if (len(content) > 0):
            return content[0]
        return ''

    def getPage(self):
        return self.page

url = 'https://www.loldytt.com/Dongzuodianying/chart/2.html'
path = '//*[@id="classpage10"]/div/a[last()]/@href'
tool = Tool(url, headers)
test = tool.xpathOne(path)
print(test[test.rindex('/')+1:test.rindex('.')])
