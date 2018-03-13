# !usr/bin/python3.4
# -*- coding:utf-8 -*-

import os
import random
import re
import sys

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


# 解析js
def regnext(str_js):
    find_pattren = re.compile(r'p;}\(\'.*?\)\)')
    arg = ''
    try:
        arg = re.search(find_pattren, str_js).group()[4:-2]
    except:
        print(str_js)
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


# 去除标题中的非法字符 (Windows)
def validateTitle(title):
    # '/\:*?"<>|'
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    new_title = re.sub(rstr, "", title)
    return new_title


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
    content_img_xpath2 = '//*[@id="barChapter"]/img'

    img_path = ptool.xpathOne(content_img_xpath)
    script_xpath = ptool.xpathOne(content_script_xpath)
    page_xpath = ptool.xpathOne(content_page_xpath)
    if script_xpath == None:
        print('获取 JS 脚本失败')
        sys.exit(1)
    if img_path == None:
        img_path = ptool.xpathOne(content_img_xpath2).get('data-src')
        if img_path == None:
            print('获取 图片路径 失败')
            sys.exit(1)
    if page_xpath == None:
        page_xpath = max(page_xpath, 1) if page_xpath is not None else 3
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

    search_title = '一拳超人'
    prefix = 2

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
    tel_host = 'http://tel.1kkk.com'
    search_href = host + '/search?title=%s&language=1' % search_title
    search_result_page_first_result_xpath = '/html/body/section[1]/div/section/div/section/div/div[2]/p[1]/a'
    search_result_page_list_result_xpath = '/html/body/section[2]/div/ul/li/div/div[1]/h2/a'

    search_tool = Tool(search_href)
    search_result_page_first_result_page = search_tool.xpathOne(search_result_page_first_result_xpath)
    if search_result_page_first_result_page == None:
        print('搜索错误，搜索不到结果！')
        sys.exit(1)

    search_result_page_first_result_href = search_result_page_first_result_page.get('href')
    search_result_page_first_result_text = validateTitle(search_result_page_first_result_page.text.strip())

    if (search_result_page_first_result_text != search_title):
        isFind = False
        print('搜索结果第一条不匹配，遍历搜索结果列表匹配.....')
        search_result_page_list = search_tool.xpath(search_result_page_list_result_xpath)
        for search_result_page_list_a in search_result_page_list:
            search_result_page_list_a_text = validateTitle(search_result_page_list_a.text.strip())
            search_result_page_list_a_href = search_result_page_list_a.get('href')
            if search_result_page_list_a_text.find(search_title) > -1:
                search_result_page_first_result_text = search_result_page_list_a_text
                search_result_page_first_result_href = search_result_page_list_a_href
                isFind = True
                break
        if isFind:
            print('搜索结果列表中找到匹配的项，重新设置相关参数。')
        else:
            print('连搜索结果列表中都找不到匹配的项，提前结束下载.......')
            sys.exit(1)
    else:
        print('搜索到第一条是匹配的，开始执行下载....')

    # 创建 搜索结果的漫画标题文件夹
    createDir(search_result_page_first_result_text)
    print('创建文件夹"', search_result_page_first_result_text, '"成功！')

    # 进入漫画主页
    index_tool = Tool(tel_host + search_result_page_first_result_href)
    # 在漫画主页 得到每个章节
    index_page_chapter_list_xpath = '//*[@id="detail-list-select-1"]/li/a'
    index_page_chapter_list = index_tool.xpath(index_page_chapter_list_xpath)
    # index_page_chapter_list = index_tool.xpath('//*[@id="detail-list-select-1"]/li[18]/a')

    # 循环每个章节
    for index_page_chapter in index_page_chapter_list:
        if prefix == 0:
            sys.exit(0)
        else:
            prefix -= 1
        h = 1  # 初始化每个章节的第一页
        image_src_list = []
        chapter_a_tag_text = validateTitle(index_page_chapter.text.strip())
        chapter_a_tag_href = index_page_chapter.get("href")
        final_dir = search_result_page_first_result_text + "/" + chapter_a_tag_text + "/"
        createDir(final_dir)
        print('创建文件夹"', final_dir, '"成功！')
        cid, mid, sign, dt, curl, key, pageTotalNumber = getPrimaryKey(host + chapter_a_tag_href)
        for j in range(0, pageTotalNumber):
            # 构造jsurl
            jsurl = tel_host + '%schapterfun.ashx?cid=%s&page=%s&language=1&gtk=6&_cid=%s&_mid=%s&_dt=%s&_sign=%s' % (
                curl, cid, str(j + 1), cid, mid, dt, sign)
            print(jsurl)

            # 构造 image 地址
            html = getChapterfun(jsurl, tel_host + curl).content.decode('utf-8', 'ignore')
            resolve_js_url_arr = regnext(html)

            # 构造 referer
            image_host = resolve_js_url_arr[0][0:resolve_js_url_arr[0].index('com') + 3]

            for image_url in resolve_js_url_arr:
                image_src_list.append(image_url)

        new_list = list(set(image_src_list))
        new_list.sort(key=image_src_list.index)
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
