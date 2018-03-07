# coding=utf-8   #默认编码格式为utf-8
import requests  # 网络请求
from lxml import html
import re

host = 'http://www.xxshu5.com'
url = 'http://www.xxshu5.com/mushenji/'

# 反爬措施
header = {
    'Host': 'www.xxshu5.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'Upgrade-Insecure-Requests':1,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://www.xxshu5.com/mushenji/',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Anit-Forge-Token': 'None',
    'X-Anit-Forge-Code': '0',
    'Content-Length': '26',
    'Cookie': 'td_cookie=436545905; __cfduid=d439c73366354256788f81f67c81801bd1520424100; PHPSESSID=nqbhl0eifqa1osug9obi2flfnt; td_cookie=436456820; UM_distinctid=1620056abd36a2-0ea2942ef9b8ce-4a541326-1fa400-1620056abd4733; CNZZDATA1261503339=2145269000-1520420756-null%7C1520420756',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}

list_title_xpath = '//*[@id="list"]/dl/dd[last()]/a'
content_title_xpath = '//*[@id="wrapper"]/div[5]/div/div[2]/h1/text()'
content_content_xpath = '//*[@id="content"]/text()'

def main():
    response = requests.get(url, header)
    text = response.text
    page = html.fromstring(text)
    titles = page.xpath(list_title_xpath)
    for title in titles:
        print(title.get('href'), title.text)
        href = title.get('href')
        href = '%s%s' % (host, href)
        content_response = requests.get(href, header)
        content_response.encoding = 'utf8'
        content_text = content_response.text
        content_text = re.sub(re.compile('&nbsp;'), '', content_text)
        content_text = re.sub(re.compile('<br><br>|<br>|<br\s?/>'), '', content_text)
        content_page = html.fromstring(content_text)
        content_title = content_page.xpath(content_title_xpath)[0]
        content_content = content_page.xpath(content_content_xpath)[0]

        print(content_title)
        print(content_content)

        f = open("a.txt", "w", encoding="UTF-8")
        f.write(str(content_title) + "\n\n")
        f.write(str(content_content) + "\n")
        f.close()
main()
