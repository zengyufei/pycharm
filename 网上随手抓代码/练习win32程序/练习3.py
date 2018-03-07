import win32api

import win32con

# 修改注册表
keyname='Software\Microsoft\Internet Explorer\Main'
page = 'www.sina.com.cn'
title = 'I love sina web site!'
search_page = 'http://www.baidu.com'

key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, keyname, 0, win32con.KEY_ALL_ACCESS)
win32api.RegSetValueEx(key, 'Start Page', 0, win32con.REG_SZ, page)
win32api.RegSetValueEx(key, 'Window Title', 0, win32con.REG_SZ, title)
win32api.RegSetValueEx(key, 'Search Page', 0, win32con.REG_SZ, search_page)
