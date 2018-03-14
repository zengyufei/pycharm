# !usr/bin/python3.4
# -*- coding:utf-8 -*-

import re
import sys

import requests

import 自定义代码.爬漫画测试.IoUtils as Io
import 自定义代码.爬漫画测试.StringUtils as Strings
from 自定义代码.爬漫画测试.RequestUtils import Tool, PhantomJSTool as PTool, PicTool


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


search_title = '妖神记'
prefix = 1

host = 'http://www.1kkk.com'
tel_host = 'http://tel.1kkk.com'

search_result_page_first_result_xpath = '/html/body/section[1]/div/section/div/section/div/div[2]/p[1]/a'
search_result_page_list_result_xpath = '/html/body/section[2]/div/ul/li/div/div[1]/h2/a'
index_page_chapter_list_xpath = '//*[@id="detail-list-select-1"]/li/a'

if __name__ == '__main__':

    search_href = host + '/search?title=%s&language=1' % search_title
    cid = ""
    mid = ""
    sign = ""
    dt = ""
    dt = ""
    curl = ""
    key = ""
    image_host = ""
    pageTotalNumber = 0

    search_tool = Tool(search_href)
    search_result_page_first_result_page = search_tool.xpathOne(search_result_page_first_result_xpath)
    if search_result_page_first_result_page == None:
        print('搜索错误，搜索不到结果！')
        sys.exit(1)

    # 获取搜素结果的第一条
    search_result_page_first_result_href = search_result_page_first_result_page.get('href')
    search_result_page_first_result_text = Strings.validateTitle(search_result_page_first_result_page.text.strip())

    # 如果搜素结果第一条不匹配，则从列表中搜素来匹配
    if (search_result_page_first_result_text != search_title):
        isFind = False
        print('搜索结果第一条不匹配，遍历搜索结果列表匹配.....')
        search_result_page_list = search_tool.xpath(search_result_page_list_result_xpath)
        for search_result_page_list_a in search_result_page_list:
            search_result_page_list_a_text = Strings.validateTitle(search_result_page_list_a.text.strip())
            search_result_page_list_a_href = search_result_page_list_a.get('href')
            if search_result_page_list_a_text.find(search_title) > -1:
                search_result_page_first_result_text = search_result_page_list_a_text
                search_result_page_first_result_href = search_result_page_list_a_href
                isFind = True
                break
            print('搜索到"', search_result_page_list_a_text, '"，但很可惜匹配失败！')
        if isFind:
            print('搜索结果列表中找到匹配的项，重新设置相关参数。')
        else:
            print('连搜索结果列表中都找不到匹配的项，提前结束下载.......')
            sys.exit(1)
    else:
        print('搜索到第一条是匹配的，开始执行下载....')

    # 创建 搜索结果的漫画标题文件夹
    Io.createDir(search_result_page_first_result_text)
    print('创建文件夹"', search_result_page_first_result_text, '"成功！')

    # 进入漫画主页
    index_tool = Tool(tel_host + search_result_page_first_result_href)
    # 在漫画主页 得到每个章节
    index_page_chapter_list = index_tool.xpath(index_page_chapter_list_xpath)
    # index_page_chapter_list = index_tool.xpath('//*[@id="detail-list-select-1"]/li[18]/a')

    # 循环每个章节
    for index_page_chapter in index_page_chapter_list:
        # 判断是否只爬取最后几个章节
        if prefix == 0:
            sys.exit(0)
        else:
            prefix -= 1

        # 核心代码
        h = 1  # 初始化每个章节的第一页
        image_src_list = []

        # 获取当前章节的名称和链接
        chapter_a_tag_text = Strings.validateTitle(index_page_chapter.text.strip())
        chapter_a_tag_href = index_page_chapter.get("href")
        # 根据章节的名称创建文件夹
        final_dir = search_result_page_first_result_text + "/" + chapter_a_tag_text + "/"
        Io.createDir(final_dir)
        print('创建文件夹"', final_dir, '"成功！')

        # 从第一页获取最最最最关键数据
        cid, mid, sign, dt, curl, key, pageTotalNumber = getPrimaryKey(host + chapter_a_tag_href)

        # 根据页码来遍历
        for j in range(0, pageTotalNumber):
            # 构造图片链接请求，返回的是 js
            jsurl = tel_host + '%schapterfun.ashx?cid=%s&page=%s&language=1&gtk=6&_cid=%s&_mid=%s&_dt=%s&_sign=%s' % (
                curl, cid, str(j + 1), cid, mid, dt, sign)
            print(jsurl)

            # 返回 js 代码，通过解析得到 image 地址
            html = getChapterfun(jsurl, tel_host + curl).content.decode('utf-8', 'ignore')
            resolve_js_url_arr = Strings.regnext(html)
            for image_url in resolve_js_url_arr:
                image_src_list.append(image_url)

            # 构造 header['host']
            image_host = resolve_js_url_arr[0]
            image_host = image_host[image_host.index("//") + 2:image_host.index('com') + 3]

        # 去重
        new_list = list(set(image_src_list))
        new_list.sort(key=image_src_list.index)

        # 遍历所有图片链接
        for index in range(len(new_list)):
            header = {'User-Agent':
                          'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
                      'Referer': 'http://m.1kkk.com' + curl,
                      'Host': image_host,
                      'Accept': 'image/png,image/*;q=0.8,*/*;q=0.5',
                      'Accept-Encoding': 'gzip, deflate',
                      'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                      'Connection': 'keep-alive',
                      }
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
            # 请求下载
            pic_tool = PicTool(new_list[index], postdata, header)
            # pic = geturl(new_list[index], postdata, image_host, 'http://m.1kkk.com' + curl)
            filess = open(final_dir + str(h) + '.jpg', 'wb')
            filess.write(pic_tool.content)
            filess.close()
            print('已经写入第' + str(h) + '张图片')

            # 每一次下载都暂停1-3秒
            # loadimg = random.randint(1, 2)
            # print('暂停' + str(loadimg) + '秒')
            # time.sleep(loadimg)
            h += 1
