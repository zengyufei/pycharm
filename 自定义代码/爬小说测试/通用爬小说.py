# coding=utf-8   #默认编码格式为utf-8
import sys

import 自定义代码.爬小说测试.IoUtils as Io
import 自定义代码.爬小说测试.Strings as Strings
from 自定义代码.爬小说测试.RequestUtils import Tool, header

search_title = '修真聊天群'
chapter_threshold_page = -1
search_threshold_page = 2
host = 'http://www.mht.la/'

search_url = 'http://zhannei.baidu.com/cse/search?s=7965856832468911224&p=%d&entry=1&q=' + search_title
search_list_title_xpath = '//*[@id="results"]/div[3]/div/div[2]/h3/a'

list_xpath = '//*[@id="novel16815"]/dl/dd[%s]/a'
title_xpath = '//*[@id="chapter%s"]/div[3]/div[2]/h1/text()'
content_xpath = '//*[@id="con%s"]/text()'
author_xpath = '//*[@id="xiaoshuo72021"]/div[2]/div[3]/div[1]/div[2]/h6[1]/a/text()'
chapter_xpath = '//*[@id="novel72021"]/dl/dd/a'

search_result_title = None
search_result_href = None

search_start_page = 0
while search_start_page <= search_threshold_page:
    print('开始搜索第', search_start_page, '页')
    search_tool = Tool(search_url % search_start_page)
    search_tag_a_list = search_tool.xpath(search_list_title_xpath)
    isFind = False
    for search_tag_a in search_tag_a_list:
        title = Strings.validateTitle(search_tag_a.get('title').strip())
        href = search_tag_a.get('href').replace('mianhuatang', 'mht')

        if search_title == title:
            search_result_title = title
            search_result_href = href
            isFind = True
            break

        print('匹配搜索到的', title, '失败。')
    if isFind:
        print('匹配书本', search_result_title, '成功。')
        break
    search_start_page += 1

if search_result_title == None or search_result_href == None:
    print('搜索了', search_threshold_page, '页，且因匹配不到而提前退出程序。')
    sys.exit(1)

Io.createDir(search_result_title)
print('创建', search_result_title, '文件夹成功！')
page_tool = Tool(search_result_href, header)
author = page_tool.xpathOne(author_xpath)
print('作者：', author)
print('设定下载章节阈值为：', chapter_threshold_page, '。即只下载倒数', chapter_threshold_page, '个章节。下载全部设置为 -1。')

chapter_list = page_tool.xpath(chapter_xpath)

for chapter in chapter_list:
    # for chapter in reversed(chapter_list):
    if chapter_threshold_page != -1 and chapter_threshold_page <= 0:
        print('遇到下载章节阈值，程序退出。')
        sys.exit(0)
    if chapter_threshold_page != -1:
        chapter_threshold_page -= 1
    content_href = chapter.get('href')
    print(search_result_href + content_href)
    content_tool = Tool(search_result_href + content_href, header)
    no = content_href[0:content_href.index('.')]
    new_title_xpath = title_xpath % no
    new_content_xpath = content_xpath % no
    title = content_tool.xpathOne(new_title_xpath)

    content = ''
    for content_arr in content_tool.xpath(new_content_xpath):
        content += content_arr

        # content = content_tool.xpathOne(new_content_xpath)
        # if content == None:
        # content = ''

    f = open(search_result_title + '/' + chapter.text + '.txt', 'w', encoding='UTF-8')
    f.write(chapter.text + '\n\n')
    f.write(Strings.replaceText(content) + '\n')
    f.close()
    print('写入', search_result_title + '/' + chapter.text + '.txt', '文件成功！')
