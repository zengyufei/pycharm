# !usr/bin/python3.4
# -*- coding:utf-8 -*-

import os
import random
import re
import time

import requests
from lxml import etree
from 自定义代码.爬漫画测试.RequestUtils import Tool, PhantomJSTool as PTool


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

    rs = requests.get(url, headers=header)
    return rs


def get(url):
    header = {'User-Agent':
                  'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
              'Referer': url,
              'Host': 'www.1kkk.com'}

    # 解析网页
    html_bytes = requests.get(url, headers=header)
    return html_bytes

# 递归创建文件夹
def createjia(path):
    try:
        os.makedirs(path)
    except:
        print('目录已经存在：' + path)


if __name__ == '__main__':
    host = 'http://www.1kkk.com'
    tool = Tool('http://tel.1kkk.com/manhua33771/')
    # 获取整本漫画标题
    title = tool.xpathOne("/html/body/div[1]/section/div[2]/div[2]/p[1]/text()").replace(" ", "")
    # 创建以漫画标题为名称的文件夹
    createjia(title)
    # 章节的起始和结束位置
    start = 1
    end = 3
    href = [] # 漫画的所有集数
    j = 0

    # 得到每章节网址
    for i in range(start,end+1):
        hrefs = tool.xpath('//*[@id="detail-list-select-1"]/li[%s]/a/@href' % i)
        for temp in hrefs:
            towurl = temp
            href.append(towurl)

    # 遍历每章节
    for i in range(0, len(href)):
        print(host+href[i])
        ptool = PTool(host+href[i])
        content_page_xpath = '//*[@id="chapterpager"]/a[last()]/text()'
        content_script_xpath = '/html/head/script[20]/text()'
        content_img_xpath = '//*[@id="cp_image"]/@src'
        img_path = ptool.xpathOne(content_img_xpath)
        script_xpath = ptool.xpathOne(content_script_xpath)
        page_xpath = ptool.xpathOne(content_page_xpath)
        if script_xpath == None:
            print('获取 JS 脚本失败')
        if img_path == None:
            print('获取 图片路径 失败')
        if page_xpath == None:
            print('获取 本章所有页数 失败')

        pageTotalNumber = int(page_xpath)

        arr = script_xpath.replace(' ', '').replace('var', '').replace('DM5_', '').lower()
        cid_re = re.compile(r'cid=(.*?);')
        mid_re = re.compile(r'mid=(.*?);')
        sign_re = re.compile(r'viewsign="(.*?)";')
        dt_re = re.compile(r'viewsign_dt="(.*?)";')
        curl_re = re.compile(r'curl="(.*?)";')
        cid = re.search(cid_re, arr).group(1)
        mid = re.search(mid_re, arr).group(1)
        sign = re.search(sign_re, arr).group(1)
        dt = re.search(dt_re, arr).group(1)
        dt = dt[0:10] + " " +dt[10::]
        curl = re.search(curl_re, arr).group(1)
        key = img_path[img_path.index('key=')+4::]
        print(key, sign, cid, mid)
        image_1url = img_path
        image_host = image_1url[0:image_1url.index('com')+3]

        # 构造image网址
        filess = open(title + "/" + str(j + 1) + '.jpg', 'wb')

        # 伪装posrdata
        postdata = {
            'cid': cid,
            'page': i,
            'key': key,
            'language': 1,
            'gtk': 6,
            '_cid': cid,
            '_mid': mid,
            '_dt': dt,
            '_sign': sign,
        }
        # 即使正确的网址也是不能下载
        pic = geturl(image_1url, postdata, image_host, 'http://m.1kkk.com' + curl)
        filess.write(pic.content)
        filess.close()
        print('已经写入第' + str(j + 1) + '张图片')
        j = j + 1

        # 每一次下载都暂停1-3秒
        #loadimg = random.randint(1, 3)
        #print('暂停' + str(loadimg) + '秒')
        #time.sleep(loadimg)
