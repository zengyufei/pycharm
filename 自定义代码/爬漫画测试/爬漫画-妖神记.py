# !usr/bin/python3.4
# -*- coding:utf-8 -*-

import os
import random
import re
import time

import requests
from lxml import etree


def geturl(url, postdata, image_host, referer):
    header = {'User-Agent':
                  'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
              'Referer': referer,
              'Host': image_host[image_host.index("//")+2::],
              'Accept': 'image/png,image/*;q=0.8,*/*;q=0.5',
              'Accept-Encoding': 'gzip, deflate',
              'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
              'Connection': 'keep-alive',
              }

    s = requests.Session()
    r = s.post('http://m.1kkk.com/userdata.ashx', data=postdata)
    _cookies = r.cookies
    # print(r.content)
    rs = s.get(url, headers=header, cookies=_cookies)
    return rs


def getChapterfun(url, referer):
    header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'tel.1kkk.com',
        'Pragma': 'no-cache',
        'Referer': referer,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    # 解析网页
    html_bytes = requests.get(url, headers=header)
    return html_bytes


def get(url):
    header = {'User-Agent':
                  'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
              'Referer': url,
              'Host': 'www.1kkk.com'}

    s = requests.Session()
    # 解析网页
    html_bytes = s.get(url, headers=header)
    _cookies = html_bytes.cookies
    # for _cookie in _cookies:
    # print(_cookie)
    return html_bytes


def mget(url):
    header = {'User-Agent':
                  'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
              'Referer': 'http://m.1kkk.com/manhua589/',
              'Host': 'm.1kkk.com'}

    # 解析网页
    html_bytes = requests.get(url, headers=header)

    return html_bytes


# 去除标题中的非法字符 (Windows)
def validateTitle(title):
    # '/\:*?"<>|'
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    new_title = re.sub(rstr, "", title)
    return new_title


def prints(timesleep):
    print('暂停' + str(timesleep) + '秒后开始批量下载图片，请保持网络畅通...')
    time.sleep(timesleep)


# 解析js
def regnext(js):
    reg = r'(var.+?.split)'
    all = re.compile(reg);
    alllist = re.findall(all, js)
    return alllist


# 递归创建文件夹
def createjia(path):
    try:
        os.makedirs(path)
    except:
        print('目录已经存在：' + path)


if __name__ == '__main__':
    host = 'http://www.1kkk.com'
    html = get('http://tel.1kkk.com/manhua33771/').content.decode('utf-8', 'ignore')

    page = etree.HTML(html.lower())
    # 得到网址后缀
    hrefs = page.xpath('//*[@id="detail-list-select-1"]/li[1]/a/@href')

    href = []
    number = 1

    # 不知道里面那几卷是不是漫画里面的
    # 先抓下来再说
    # 得到网址后缀
    for temp in hrefs:
        towurl = temp
        href.append(towurl)

    j = 0

    for i in range(0, len(href)):
        tempHref = str(href[i])
        hrefnumber = tempHref.replace("/", "")[tempHref.index('-')::]
        # print(hrefnumber)
        # 构造jsurl
        # 得到
        # http://tel.1kkk.com/ch344-84814/chapterfun.ashx?cid=84814&page=1&language=1&gtk=6&_cid=84814&_mid=589&_dt=2018-03-11+11%3A07%3A50&_sign=5b8bbdea79a4b000e6f3ef7f865e527d
        jsurl = "http://tel.1kkk.com" + str(href[i]) + "chapterfun.ashx?cid=" + str(hrefnumber) + "&page=" + str(
            j + 1) + "&key=&language=1&gtk=6&_cid=" + str(
            hrefnumber) + "&_mid=33771&_dt=2018-03-11 20:45:51&_sign=9003915831bd3e2ab955ab09ab682bec"
        print(jsurl)

        # 构造image网址
        html = getChapterfun(jsurl, 'http://tel.1kkk.com' + tempHref).content.decode('utf-8', 'ignore')
        html1 = regnext(html)
        html1 = html1[0].replace("'.split", "").split('|')

        # http://manhua1018-61-174-50-98.cdndm5.com/j/结界师/结界师_CH344/01.jpg?cid=84814&key=c90d64ad63a0073629c57b57ff5cc0c5
        image_1url = ""
        if(len(html1) == 27):
            image_1url = "http://" + str(html1[14]) + "-" + str(html1[19]) + "-" + str(html1[18]) + "-" + str(
                html1[9]) + "-" + str(html1[10]) + ".cdndm5.com/34/33771/" + str(html1[2]) + "/" + str(html1[24]) + "." + str(html1[3]) + "?cid=" + str(html1[2]) + "&key=" + str(html1[8])
        else:
            image_1url = "http://" + str(html1[16]) + "-" + str(html1[20]) + "-" + str(html1[19]) + "-" + str(
                html1[8]) + "-" + str(html1[9]) + ".cdndm5.com/j/" + str(html1[10]) + "/" + str(html1[21]) + "/" + str(
                html1[26]) + "." + str(html1[27]) + "?cid=" + str(html1[3]) + "&key=" + str(html1[7])
        print(image_1url)
        image_host = image_1url[0:image_1url.index('com')+3]

        # 构造image网址
        filess = open(str(j + 1) + '.jpg', 'wb')

        # 伪装posrdata
        postdata = {
            'cid': html1[2],
            'page': 1,
            'key': str(html1[8]),
            'language': 1,
            'gtk': 6,
            '_cid': html1[2],
            '_mid': 33771,
            '_dt': '2018-03-11 11:07:50',
            '_sign':  str(html1[8]),
        }

        # 即使正确的网址也是不能下载
        pic = geturl(image_1url, postdata, image_host, 'http://m.1kkk.com' + tempHref)
        filess.write(pic.content)
        filess.close()
        print('已经写入第' + str(j + 1) + '张图片')
        j = j + 1

        # 每一次下载都暂停1-3秒
        loadimg = random.randint(1, 3)
        print('暂停' + str(loadimg) + '秒')
        time.sleep(loadimg)
