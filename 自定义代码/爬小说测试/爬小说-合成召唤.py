# coding=utf-8   #默认编码格式为utf-8

from 自定义代码.爬小说测试.RequestUtils import Tool, header
import 自定义代码.爬小说测试.IoUtils as io
import time

host = 'http://www.mht.la/'
url = 'http://www.mht.la/16/16815/'

list_xpath = '//*[@id="novel16815"]/dl/dd[%s]/a'
title_xpath = '//*[@id="chapter%s"]/div[3]/div[2]/h1/text()'
content_xpath = '//*[@id="con%s"]/text()'

start = 1
end = 909
def main():
    tool = Tool(url, header)
    for i in range(end-start):
        print(start + i)
        newXPath = list_xpath % (start + i)
        for titleAndHref in tool.xpath(newXPath):
            oldHref = titleAndHref.get('href')
            href = '%s%s' % (url, oldHref)
            io.printConsole(href, oldHref)
            content_tool = Tool(href, header)

            no = oldHref[0:oldHref.index('.')]
            new_title_xpath = title_xpath % no
            new_content_xpath = content_xpath % no
            title = content_tool.xpathOne(new_title_xpath)
            content = content_tool.xpathOne(new_content_xpath)
            #time.sleep(0.7)
            io.writeFile(title, content, "合成召唤/")
            # io.printConsole(title, content)
            # io.writeAndSleepReaderTempFile(title, content)
main()
