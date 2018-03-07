# -*- coding:utf-8 -*-
#####################
#  获取电影列表
#####################

import datetime
import re

import CustomMysql
import requests
from lxml import html
import os,base64
from PIL import Image
from io import BytesIO

user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
headers = {'User-Agent': user_agent}

mysql = CustomMysql.Mysql("127.0.0.1", 3306, "root", "root", "dy", "utf8")


class Bean:
    id = 0
    key = ""  # 网站url上面的唯一标识
    title = ""  # 标题
    type = ""  # 电影类型
    content = ""  # 介绍
    img = ""  # 封面
    time = ""  # 日期
    sharpness = ""  # 清晰度 BD HD TC
    starring = ""  # 主演
    url = ""  # 链接
    pageIndex = 0  # 列表的页码
    createId = 0
    createTime = ""

    def __init__(self):
        self.createTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
        self.createId = 0

    def __str__(self):
        return '\n'.join(['%s: %s' % item for item in self.__dict__.items()])

    def insert(self):
        # 新增操作前的查询
        sql = "select count(*) from bean where `key` = '%s' " % (self.key)
        count = mysql.count(sql)
        if (count == 0):
            # 执行SQL，并返回收影响行数
            sql = "insert into bean(`key`, title, type, content, img, time, sharpness, starring, url, pageIndex, createId, createTime) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                self.key, self.title, self.type, self.content, self.img, self.time, self.sharpness, self.starring,
                self.url,
                self.pageIndex, self.createId, self.createTime)
            mysql.insert(sql)


class DownBean:
    beanKey = 0
    downType = 0  # 0 磁力下载 1 迅雷下载
    downTypeName = ""  # downType 别名
    downFileName = ""  # 下载链接的名称
    downFileUrl = ""  # 下载链接的名称

    def __str__(self):
        return '\n'.join(['%s: %s' % item for item in self.__dict__.items()])

    def insert(self):
        # 新增操作前的查询
        sql = "select count(*) from down_bean where downFileUrl = '%s' " % (self.downFileUrl)
        count = mysql.count(sql)
        if (count == 0):
            # 执行SQL，并返回收影响行数
            sql = "insert into down_bean(beanKey, downFileName, downFileUrl, downType, downTypeName) values('%s', '%s', '%s', '%s', '%s')" % (
                self.beanKey, self.downFileName, self.downFileUrl, self.downType, self.downTypeName)
            mysql.insert(sql)


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


class Error:
    id = 0
    errorName = ''  # 存储名词
    errorTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 存储错误时间
    errorKey = ''  # 存储页码
    errorValue = ''  # 存储type

    def __init__(self, errorName, errorKey, errorValue):
        self.errorTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
        self.id = 0
        self.errorName = errorName
        self.errorKey = errorKey
        self.errorValue = errorValue

    def getSql(self):
        return 'insert into error(errorName, errorKey, errorValue, errorTime) values(\'%s\', \'%s\', \'%s\', \'%s\')' % (
            self.errorName, self.errorKey, self.errorValue, self.errorTime)


def find(url, start, end, type):
    for i in range(start, end + 1):
        try:
            searchUrl = url % (i.__str__())
            print('-----------------第 ' + i.__str__() + ' 页----------------', searchUrl)
            tool = Tool(searchUrl, headers)
            links = tool.xpath('//div[@id="classpage"]/div[1]/div[2]/div/ul/li/a/@href')
            for link in links:
                bean = Bean()
                tool = Tool(link, headers)
                bean.title = tool.xpathOne('/html/head/title/text()').replace("《", "").replace("》", "").replace(
                    "电影迅雷下载 - BT种子下载 - LOL电影天堂", "")  # 保存标题
                bean.img = tool.xpathOne('/html/body/center/div[7]/div[2]/div[1]/div[1]/a/img/@src')  # 保存封面
                bean.starring = tool.xpathOne('/html/body/center/div[7]/div[2]/div[1]/div[2]/ul/li/text()')  # 保存主演
                bean.sharpness = tool.xpathOne('/html/body/center/div[7]/div[1]/h1/font/text()')  # 保存清晰度
                bean.time = tool.xpathOne('/html/body/center/div[7]/div[1]/p/text()')  # 保存日期
                bean.content = tool.xpathOne('//*[@class="neirong"]/p/text()')  # 保存介绍
                bean.type = type
                bean.pageIndex = i  # 保存列表的页码
                bean.url = link
                bean.createId = 1
                # 保存 key
                rindex = link.rindex("/", 1, len(link) - 3)
                bean.key = link[rindex + 1:-1]

                ciliDownList = tool.xpath('//*[@id="ul1"]/li/a')  # 遍历下载链接
                for ciliDown in ciliDownList:
                    down_bean = DownBean()
                    down_bean.beanKey = bean.key
                    down_bean.downFileName = ciliDown.get("title")
                    down_bean.downFileUrl = ciliDown.get("href")
                    down_bean.downType = 0
                    down_bean.downTypeName = '磁力下载'
                    down_bean.insert()

                xunleiDownList = tool.xpath('//*[@id="ul2"]/li/a')  # 遍历下载链接
                for xunleiDown in xunleiDownList:
                    down_bean = DownBean()
                    down_bean.beanKey = bean.key
                    down_bean.downFileName = xunleiDown.get("title")
                    down_bean.downFileUrl = xunleiDown.get("href")
                    down_bean.downType = 1
                    down_bean.downTypeName = '迅雷下载'
                    down_bean.insert()

                print("《", bean.title, "》 ====--- ", bean.url, " ---====")
                bean.insert()
        except:
            error = Error("下载失败", i, type)
            print("下载失败。失败 url： ", url, "。错误原因： ", sys.exc_info())
            mysql.insert(error.getSql())


def getPageEndNumber(url, ):
    firstUrl = url % ("1")
    tool = Tool(firstUrl, headers)
    path = '//*[@id="classpage10"]/div/a[last()]/@href'
    firstListPage = tool.xpathOne(path)
    return int(firstListPage[firstListPage.rindex('/') + 1:firstListPage.rindex('.')])


def findByList(list):
    for i in range(0, len(list), 2):
        url = list[i]
        type = list[i + 1]
        end = getPageEndNumber(url)
        find(url, 1, end, type)

def imgToBase64(imgSrc):
    response = requests.get(imgSrc)  # 将这个图片保存在内存
    # 将这个图片从内存中打开，然后就可以用Image的方法进行操作了
    image = Image.open(BytesIO(response.content))
    # 得到这个图片的base64编码
    ls_f = base64.b64encode(BytesIO(response.content).read())
    # 打印出这个base64编码
    print(ls_f)

list = [
#    "https://www.loldytt.com/Dongzuodianying/chart/%s.html", "dongzuo",
#    "https://www.loldytt.com/Kehuandianying/chart/%s.html", "kehuan",
#    "https://www.loldytt.com/Kongbudianying/chart/%s.html", "kongbu",
#    "https://www.loldytt.com/Xijudianying/chart/%s.html", "xiju",
    "https://www.loldytt.com/Aiqingdianying/chart/%s.html", "aiqing",
    "https://www.loldytt.com/Juqingdianying/chart/%s.html", "juqing",
    "https://www.loldytt.com/Zhanzhengdianying/chart/%s.html", "zhanzheng"
]

#findByList(list)

start = 215
end = 266
url = 'https://www.loldytt.com/Juqingdianying/chart/%s.html'
type = 'juqing'
find(url, start, end, type)

# 关闭连接
mysql.close()
