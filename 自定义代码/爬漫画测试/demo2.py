# !usr/bin/python3.4
# -*- coding:utf-8 -*-

import os
import random
import re
import time

import execjs
import requests
from lxml import etree


def geturl(url, postdata, image_host, referer):
    header = {'User-Agent':
                  'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
              'Referer': referer,
              'Host': image_host[image_host.index("//") + 2::],
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

    # 解析网页
    html_bytes = requests.get(url, headers=header)
    return html_bytes

# 解析js
def regnext(js):
    arg = re.search(re.compile('\'h 8.*\)\)'), js).group()[:-2]
    ctx = execjs.compile(""" 
        function aa(){
            return function(p,a,c,k,e,d){
                e=function(c){
                    return(c<a?"":e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))
                };
                while(c--){
                   d[e(c)]=k[c]||e(c);
                }
                p=p.replace(/\\b\\w+\\b/g,function(e){
                    return d[e]
                });
                return p;
            }
            (""" + arg + """)
        }
    """)
    x = ctx.call("aa", 1)
    ctx = execjs.compile(x)
    x = ctx.call("dm5imagefun", 1)
    return x


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
    # 获取整本漫画标题
    title = page.xpath("/html/body/div[1]/section/div[2]/div[2]/p[1]/text()")[0].replace(" ", "")
    # 创建以漫画标题为名称的文件夹
    createjia(title)
    # 得到网址后缀
    hrefs = page.xpath('//*[@id="detail-list-select-1"]/li[1]/a/@href')

    href = []

    # 不知道里面那几卷是不是漫画里面的
    # 先抓下来再说
    # 得到网址后缀
    for temp in hrefs:
        href.append(temp)

    url_list = []
    h = 1
    key = ""
    cid = ""
    tempHref = ""
    image_host = ""
    for i in range(0, len(href)):
        for j in range(0, 3):
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
            urls = regnext(html)

            # http://manhua1018-61-174-50-98.cdndm5.com/j/结界师/结界师_CH344/01.jpg?cid=84814&key=c90d64ad63a0073629c57b57ff5cc0c5
            image_host = urls[0][0:urls[0].index('com') + 3]

            key = urls[0][urls[0].index('key=')+4::]
            cid = urls[0][urls[0].index('cid=')+4::]

            # 即使正确的网址也是不能下载
            for image_1url in urls:
                url_list.append(image_1url)

    new_list = list(set(url_list))
    new_list.sort(key=url_list.index)
    for index in range(len(new_list)):
        # 伪装posrdata
        postdata = {
            'cid': cid,
            'page': index + 1,
            'key': key,
            'language': 1,
            'gtk': 6,
            '_cid': cid,
            '_mid': 33771,
            '_dt': '2018-03-11 11:07:50',
            '_sign': '9003915831bd3e2ab955ab09ab682bec',
        }
        pic = geturl(new_list[index], postdata, image_host, 'http://m.1kkk.com' + tempHref)
        filess = open(title + "/" + str(h) + '.jpg', 'wb')
        filess.write(pic.content)
        filess.close()
        print('已经写入第' + str(h) + '张图片')

        # 每一次下载都暂停1-3秒
        loadimg = random.randint(1, 3)
        print('暂停' + str(loadimg) + '秒')
        time.sleep(loadimg)
        h += 1
