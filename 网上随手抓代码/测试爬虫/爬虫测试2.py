#####################
#  获取SF首页的标题
#####################
from lxml.etree import HTML
import requests

url = 'https://segmentfault.com/'
css_selector = '.title>a'  # 这是利用浏览器自动获取的,我甚至都不用知道它是什么意思

text = requests.get(url).text
page = HTML(text)

titles = []
for title in page.cssselect(css_selector):
    titles.append(title.text)

print(titles)

# 这一段程序写下来,不用动脑筋(无脑写),不消耗心智