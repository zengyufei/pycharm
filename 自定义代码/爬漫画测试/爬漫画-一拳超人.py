# coding=utf-8   #默认编码格式为utf-8
import requests

from 自定义代码.爬漫画测试.RequestUtils import Tool, PhantomJSTool as PTool, img_header, header

host = 'http://www.1kkk.com'
url = 'http://www.1kkk.com/manhua589/'
data_url = 'http://www.1kkk.com/ch129-583070-p2/userdata.ashx?d=1520577263024'
# !usr/bin/python3.4
# -*- coding:utf-8 -*-

import os
import random
import re
import time

import execjs
import requests
from 自定义代码.爬漫画测试.RequestUtils import Tool, PhantomJSTool as PTool


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
def regnext(str_js):
    find_pattren = re.compile(r'p;}\(\'.*?\)\)')
    arg = re.search(find_pattren, str_js).group()[4:-2]
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
def createDir(path):
    try:
        os.makedirs(path)
    except:
        print('目录已经存在：' + path)

def getPrimaryKey(url):
    # 获取每个章节第一页，从而获取所有必要信息
    ptool = PTool(url)
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
    dt = dt[0:10] + " " + dt[10::]
    curl = re.search(curl_re, arr).group(1)
    key = img_path[img_path.index('key=') + 4::]
    return [cid, mid, sign, dt, curl, key, pageTotalNumber]


if __name__ == '__main__':

    cid = ""
    mid = ""
    sign = ""
    dt = ""
    dt = ""
    curl = ""
    key = ""
    image_host = ""
    pageTotalNumber = 0

    host = 'http://www.1kkk.com'
    tool = Tool('http://tel.1kkk.com/manhua33771/')
    # 获取整本漫画标题
    title = tool.xpathOne("/html/body/div[1]/section/div[2]/div[2]/p[1]/text()").replace(" ", "")
    # 创建以漫画标题为名称的文件夹
    createDir(title)
    # 得到每个章节
    chapter_xpath = tool.xpath('//*[@id="detail-list-select-1"]/li/a')

    # 循环每个章节
    for chapter_a_tag in chapter_xpath:
        h = 1
        image_url_list = []
        chapter_a_tag_text = chapter_a_tag.text.strip()
        chapter_a_tag_href = chapter_a_tag.get("href")
        final_dir = title + "/" + chapter_a_tag_text + "/"
        createDir(final_dir)
        cid, mid, sign, dt, curl, key, pageTotalNumber = getPrimaryKey(host + chapter_a_tag_href)
        for j in range(0, pageTotalNumber):
            # 构造jsurl
            jsurl = 'http://tel.1kkk.com%schapterfun.ashx?cid=%s&page=%s&language=1&gtk=6&_cid=%s&_mid=%s&_dt=%s&_sign=%s' % (curl, cid, str(j + 1), cid, mid, dt, sign)
            print(jsurl)

            # 构造 image 地址
            html = getChapterfun(jsurl, 'http://tel.1kkk.com' + curl).content.decode('utf-8', 'ignore')
            resolve_js_url_arr = regnext(html)

            # 构造 referer
            image_host = resolve_js_url_arr[0][0:resolve_js_url_arr[0].index('com') + 3]

            for image_url in resolve_js_url_arr:
                image_url_list.append(image_url)

        new_list = list(set(image_url_list))
        new_list.sort(key=image_url_list.index)
        for index in range(len(new_list)):
            # 伪装posrdata
            postdata = {
                'cid': int(cid),
                'page': index + 1,
                'key': key,
                'language': 1,
                'gtk': 6,
                '_cid': int(cid),
                '_mid': int(mid),
                '_dt': 'dt',
                '_sign': sign,
            }
            pic = geturl(new_list[index], postdata, image_host, 'http://m.1kkk.com' + curl)
            filess = open(final_dir + str(h) + '.jpg', 'wb')
            filess.write(pic.content)
            filess.close()
            print('已经写入第' + str(h) + '张图片')

            # 每一次下载都暂停1-3秒
            loadimg = random.randint(1, 2)
            print('暂停' + str(loadimg) + '秒')
            # time.sleep(loadimg)
            h += 1
