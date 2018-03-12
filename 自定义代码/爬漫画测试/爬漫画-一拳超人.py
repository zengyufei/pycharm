# coding=utf-8   #默认编码格式为utf-8
import requests

from 自定义代码.爬漫画测试.RequestUtils import Tool, PhantomJSTool as PTool, img_header, header

host = 'http://www.1kkk.com'
url = 'http://www.1kkk.com/manhua589/'
data_url = 'http://www.1kkk.com/ch129-583070-p2/userdata.ashx?d=1520577263024'

list_href_xpath = '//*[@id="detail-list-select-1"]/ul/li[1]/a/@href'
list_href_title_xpath = '//*[@id="detail-list-select-1"]/li[1]/a/text()'
content_img_xpath = '//*[@id="cp_image"]'
content_img_end_number_xpath = '//*[@id="chapterpager"]/a[8]/text()'


def main():
    tool = Tool(url)
    for a_href in tool.xpath(list_href_xpath):
        href = '%s%s' % (host, a_href)
        print(href)
        content_tool = PTool(href)
        img_url = content_tool.xpathOne(content_img_xpath)
        key = content_tool.xpathOne('//*[@id="dm5_key"]')
        img_src = img_url.get("src")
        print(key, img_src)


#  传入图片地址，文件名，保存单张图片
def saveImg(img, fileName):
    with open(fileName, 'wb') as f:
        f.write(img)
        f.close()


main()
