# coding=utf-8   #默认编码格式为utf-8

from 自定义代码.爬小说测试.RequestUtils import Tool, header
import 自定义代码.爬小说测试.IoUtils as io

host = 'http://www.xxshu5.com'
url = 'http://www.xxshu5.com/fanrenxiuxianzhixianjiepian/'

list_xpath = '//*[@id="list"]/dl/dd[%s]/a'
title_xpath = '//*[@id="wrapper"]/div[5]/div/div[2]/h1/text()'
content_xpath = '//*[@id="content"]/text()'

start = 10
end = 12
def main():
    tool = Tool(url, header)
    for i in range(12-10):
        print(start + i)
        newXPath = list_xpath % (start + i)
        for titleAndHref in tool.xpath(newXPath):
            href = '%s%s' % (host, titleAndHref.get('href'))
            content_tool = Tool(href, header)
            title = content_tool.xpathOne(title_xpath)
            content = content_tool.xpathOne(content_xpath)

            # io.printConsole(titleAndHref.get('href'), title)
            io.printConsole(title, content)
            # io.writeAndSleepReaderTempFile(title, content)
main()
